import pandas as pd
import numpy as np
import json
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
        #? situation_type :
        # 0 -> PK (powerkill)
        # 1 -> force egale 
        # 2 -> PP (powerplay)
        path = f'ift6758/data/{season}/{season_type}.json'
        df = pd.DataFrame(columns=['period', 'is_goal', 'x_coord', 'y_coord', 
                                   'shot_type', 'is_empty_net', 'distance', 'angle_to_goal', 
                                   'game_seconds', 'last_event_type', 'last_event_x_coord', 
                                   'last_event_y_coord', 'time_since_last_event', 'distance_from_last_event'])
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            df_data = pd.read_json(path)
            games_iter = tqdm(data)
            for game in games_iter:
                games_iter.set_description_str("Game: %s" % game['id'])

                # Filter shots and goals
                shots = [play for play in game['plays'] if play['typeCode'] in [505, 506]]
                away_team_id = game['awayTeam']['id']

                for shot in shots:
                    # Current shot info
                    try:
                        x_coord = shot['details']['xCoord']
                        y_coord = shot['details']['yCoord']
                        shot_type = shot['details']['shotType']
                        event_owner_team = shot['details']['eventOwnerTeamId']
                    except:
                        # The data does not contain the required details, we can skip over this shot
                        # to keep the data clean
                        print("Important shot details not found. Shot skipped.")
                        continue

                    situation = str(shot['situationCode'])
                    is_away_team = away_team_id == event_owner_team
                    distance = np.sqrt((x_coord - 90)**2 + y_coord**2)
                    angle_to_goal = np.degrees(np.arctan2(y_coord, 90 - x_coord))
                    is_away_goalie_in_net = int(situation[0])
                    is_home_goalie_in_net = int(situation[3])
                    is_empty_net = (is_away_team and not bool(is_home_goalie_in_net)) or (not is_away_team and not bool(is_away_goalie_in_net) or 'goalieInNetId' not in shot['details'])
                    period = shot['periodDescriptor']['number']
                    is_goal = int(shot['typeCode'] == 505)
                    time_in_period_seconds = self._convert_to_seconds(shot['timeInPeriod'])
                    game_seconds = (int(period) - 1) * 20 * 60 + time_in_period_seconds

                    # Previous shot info
                    play_index = game['plays'].index(shot)
                    if play_index == 0:
                        last_event_type = None
                        last_event_x_coord = None
                        last_event_y_coord = None
                        time_since_last_event = None
                        distance_from_last_event = None
                    else:
                        previous_play = game['plays'][play_index - 1]
                        # Only consider the play if it was in the same period
                        if period == previous_play['periodDescriptor']['number']:
                            try:
                                last_event_x_coord = previous_play['details']['xCoord']
                                last_event_y_coord = previous_play['details']['yCoord']
                            except KeyError as e:
                                # The data does not contain the required info.
                                # Continue to keep the data clean.
                                print("Last event coordinates not found. Shot skipped.")
                                continue

                            # Find a way to convert typeCode using the NHL API endpoint
                            last_event_type = previous_play['typeCode']
                            time_in_period_seconds = self._convert_to_seconds(previous_play['timeInPeriod'])
                            last_event_seconds = (int(period) - 1) * 20 * 60 + time_in_period_seconds
                            time_since_last_event = game_seconds - last_event_seconds
                            distance_from_last_event = np.sqrt((x_coord - last_event_x_coord) ** 2 + (y_coord - last_event_y_coord) ** 2)
                        else:
                            last_event_type = None
                            last_event_x_coord = None
                            last_event_y_coord = None
                            time_since_last_event = None
                            distance_from_last_event = None

                    row = {
                        'period': period,
                        'is_goal': is_goal,
                        'x_coord': x_coord,
                        'y_coord': y_coord,
                        'shot_type': shot_type,
                        'is_empty_net': int(is_empty_net),
                        'distance': distance,
                        'angle_to_goal': angle_to_goal,
                        'game_seconds': game_seconds,
                        'last_event_type': last_event_type,
                        'last_event_x_coord': last_event_x_coord,
                        'last_event_x_coord': last_event_y_coord,
                        'time_since_last_event': time_since_last_event,
                        'distance_from_last_event': distance_from_last_event
                    }

                    df = df._append(row, ignore_index=True)

            out_path = f'ift6758/data/milestone2/{season}/{season_type}.csv'
            df.to_csv(out_path, index=False)

    def clean_data(self):
        seasons_iter = tqdm(self.YEARS)
        for season in seasons_iter:
            seasons_iter.set_description_str("Season: %s" % season)
            types_iter = tqdm(self.TYPES)
            for game_type in types_iter:
                types_iter.set_description_str("Type: %s" % game_type)
                self.clean_data_for_season(season, game_type)

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
