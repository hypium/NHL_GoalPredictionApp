import pandas as pd
import numpy as np
import json
import os
from tqdm import tqdm

class DataCleanerMilestone2:
    def __init__(self):
        self.TYPES = ['season', 'playoffs']
        self.YEARS = [
            '2016',
            '2017',
            '2018',
            '2019',
            '2020',
            '2021',
        ]

    def clean_data_for_season(self, season, season_type):
        path = f'ift6758/data/{season}/{season_type}.json'
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            games_iter = tqdm(data)
            shotcount = 0
            skippedshots = 0
            rows = []
            for game in games_iter:
                games_iter.set_description_str("Game: %s" % game['id'])

                # Filter shots and goals
                shots = [play for play in game['plays'] if play['typeCode'] in [505, 506]]
                away_team_id = game['awayTeam']['id']

                for shot in shots:
                    shotcount += 1
                    # Current shot info
                    try:
                        x_coord = np.abs(shot['details']['xCoord'])
                        y_coord = shot['details']['yCoord']
                        shot_type = shot['details']['shotType']
                        event_owner_team = shot['details']['eventOwnerTeamId']
                    except:
                        # The data does not contain the required details, we can skip over this shot
                        # since this is an error and very rare. This should not introduce significant bias.
                        skippedshots += 1
                        continue

                    situation = str(shot['situationCode'])
                    is_away_team = away_team_id == event_owner_team
                    distance = np.hypot(x_coord - 90, y_coord)
                    angle_to_goal = np.degrees(np.arctan2(y_coord, 90 - x_coord))
                    is_away_goalie_in_net = int(situation[0])
                    is_home_goalie_in_net = int(situation[3])
                    is_empty_net = (is_away_team and not bool(is_home_goalie_in_net)) or (not is_away_team and not bool(is_away_goalie_in_net) or 'goalieInNetId' not in shot['details'])
                    period = shot['periodDescriptor']['number']
                    is_goal = int(shot['typeCode'] == 505)
                    time_in_period_seconds = self._convert_to_seconds(shot['timeInPeriod'])
                    game_seconds = (int(period) - 1) * 20 * 60 + time_in_period_seconds

                    play_index = game['plays'].index(shot)
                    last_event_info = self._get_last_event_info(game, play_index, period, game_seconds, x_coord, y_coord)

                    # include gameid and play# to be able to find it on the interactive debug tool
                    row = {
                        'game_id': game['id'],
                        'play_num': play_index,
                        'period': period, 
                        'is_goal': is_goal, 
                        'x_coord': x_coord, 
                        'y_coord': y_coord,
                        'shot_type': shot_type, 
                        'is_empty_net': int(is_empty_net), 
                        'distance': distance,
                        'angle_to_goal': angle_to_goal, 
                        'game_seconds': game_seconds, 
                        **last_event_info
                    }
                    rows.append(row)

            print(f"Total shots in season: {shotcount}, skipped shots: {skippedshots}, Percent shots skipped: {skippedshots/shotcount * 100}%")
            
            out_dir = f"ift6758/data/milestone2/{season}"
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            out_path = f"{out_dir}/{season_type}.csv"

            df = pd.DataFrame(rows)
            df.to_csv(out_path, index=False)

    def clean_data(self):
        seasons_iter = tqdm(self.YEARS)
        for season in seasons_iter:
            seasons_iter.set_description_str("Season: %s" % season)
            types_iter = tqdm(self.TYPES)
            for game_type in types_iter:
                types_iter.set_description_str("Type: %s" % game_type)
                self.clean_data_for_season(season, game_type)

    def _get_last_event_info(self, game, play_index, period, game_seconds, x_coord, y_coord):
        if play_index == 0:
            return {
                'last_event_type': None, 
                'last_event_x_coord': None, 
                'last_event_y_coord': None,
                'time_since_last_event': None, 
                'distance_from_last_event': None
                }

        previous_play = game['plays'][play_index - 1]
        if period != previous_play['periodDescriptor']['number']:
            return {
                'last_event_type': None, 
                'last_event_x_coord': None, 
                'last_event_y_coord': None,
                'time_since_last_event': None, 
                'distance_from_last_event': None
                }

        last_event_details = previous_play.get('details', {})
        last_event_x = last_event_details.get('xCoord')
        last_event_y = last_event_details.get('yCoord')
        if last_event_x is not None and last_event_y is not None:
            last_event_x = np.abs(last_event_x)
            distance_from_last_event = np.hypot(x_coord - last_event_x, y_coord - last_event_y)
        else:
            distance_from_last_event = None
        last_event_seconds = (int(period) - 1) * 20 * 60 + self._convert_to_seconds(previous_play['timeInPeriod'])
        
        return {
            'last_event_type': previous_play['typeCode'],
            'last_event_x_coord': last_event_x,
            'last_event_y_coord': last_event_y,
            'time_since_last_event': game_seconds - last_event_seconds,
            'distance_from_last_event': distance_from_last_event
        }

    def _convert_to_seconds(self, time: str):
        time_arr = time.split(':')

        if len(time_arr)==2:
            seconds = int(time_arr[0]) * 60 + int(time_arr[1])
        elif len(time_arr)==1:
            seconds = int(time_arr[0])
        else:
            print("Error, too many indices in time_arr")

        return seconds

if __name__ == '__main__':
    data_cleaner_obj = DataCleanerMilestone2()
    data_cleaner_obj.clean_data()
