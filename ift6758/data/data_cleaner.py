import pandas as pd
import json
from tqdm import tqdm

class DataCleaner:

    def __init__(self):
        self.GAME_TYPE_NAMES = ['season', 'playoffs']
        self.SEASONS = [
            '2016',
            '2017',
            '2018',
            '2019',
            '2020',
            '2021',
            '2022',
            '2023',
            '2024',
        ]

    def get_payer_name(self, df_data, game_id, player_id):
        roster = df_data[df_data['id'] == game_id]['rosterSpots']
        for r in roster:
            for player in r:
                if player['playerId'] == player_id:
                    return f"{player['firstName']['default']} {player['lastName']['default']}"

    def clean_data_for_season(self, season, season_type):
        #? situation_type :
        # 0 -> PK (powerkill)
        # 1 -> force egale 
        # 2 -> PP (powerplay)
        path = f'ift6758/data/{season}/{season_type}.json'
        df = pd.DataFrame(columns=['game_id', 'period', 'time_in', 'time_remaining', 'team_id', 'is_goal', 'x_coord', 'y_coord', 'shooter_name', 'goalie_name', 'shot_type', 'is_empty_net', 'situation_type'])
        with open(path) as f:
            data = json.load(f)
            df_data = pd.read_json(path)
            games_iter = tqdm(data)
            for game in games_iter:
                games_iter.set_description_str("Game: %s" % game['id'])
                plays = [play for play in game['plays'] if play['typeCode'] in [505, 506]]
                away_team_id = game['awayTeam']['id']
                for play in plays:
                    situation = str(play['situationCode'])
                    event_owner_team = play['details']['eventOwnerTeamId']
                    is_away_team = away_team_id == event_owner_team
                    is_away_goalie_in_net = int(situation[0])
                    away_skaters = int(situation[1])
                    home_skaters = int(situation[2])
                    is_home_goalie_in_net = int(situation[3])
                    situation = int(away_skaters == home_skaters) #? PK = 0   E = 1  PP = 2
                    if is_away_team:
                        if away_skaters > home_skaters:
                            situation = 2 # PP
                        elif away_skaters < home_skaters:
                            situation = 0 ## PK
                    if not is_away_team:
                        if home_skaters > away_skaters:
                            situation = 2 # PP
                        elif home_skaters < away_skaters:
                            situation = 0 # PK
                    event_owner_id = None
                    if play['typeCode'] == 506:
                        event_owner_id = play['details']['shootingPlayerId']
                    elif play['typeCode'] == 505:
                        event_owner_id = play['details']['scoringPlayerId']
                    is_empty_net = (is_away_team and not bool(is_home_goalie_in_net)) or (not is_away_team and not bool(is_away_goalie_in_net) or 'goalieInNetId' not in play['details'])
                    goalie_name = None
                    if not is_empty_net:
                        goalie_name = self.get_payer_name(df_data, game['id'], play['details']['goalieInNetId'])
                    try:
                        row = {
                            'game_id': game['id'],
                            'period': play['periodDescriptor']['number'],
                            'time_in': play['timeInPeriod'],
                            'time_remaining': play['timeRemaining'],
                            'team_id': play['details']['eventOwnerTeamId'],
                            'is_goal': int(play['typeCode'] == 505),
                            'x_coord': play['details']['xCoord'],
                            'y_coord': play['details']['yCoord'],
                            'shooter_name': self.get_payer_name(df_data, game['id'], event_owner_id),
                            'goalie_name': goalie_name,
                            'shot_type': int(play['details']['shotType'] == 'slap'),
                            'is_empty_net': int(is_empty_net),
                            'situation_type': situation,
                        }
                    except KeyError as e:
                        if 'shotType' not in play['details'].keys():
                            shot_type = None
                        else:
                            shot_type = play['details']['shotType']
                        if 'xCoord' not in play['details'].keys():
                            x_coord = None
                        else:
                            x_coord = play['details']['xCoord']
                        if 'yCoord' not in play['details'].keys():
                            y_coord = None
                        else:
                            y_coord = play['details']['yCoord']
                        row = {
                            'game_id': game['id'],
                            'period': play['periodDescriptor']['number'],
                            'time_in': play['timeInPeriod'],
                            'time_remaining': play['timeRemaining'],
                            'team_id': play['details']['eventOwnerTeamId'],
                            'is_goal': int(play['typeCode'] == 505),
                            'x_coord': x_coord,
                            'y_coord': y_coord,
                            'shooter_name': self.get_payer_name(df_data, game['id'], event_owner_id),
                            'goalie_name': goalie_name,
                            'shot_type': shot_type,
                            'is_empty_net': int(is_empty_net),
                            'situation_type': situation,
                        }
                    df = df._append(row, ignore_index=True)
            out_path = f'ift6758/data/{season}/{season_type}.csv'
            df.to_csv(out_path, index=False)

    def clean_data(self):
        seasons_iter = tqdm(self.SEASONS)
        for season in seasons_iter:
            seasons_iter.set_description_str("Season: %s" % season)
            types_iter = tqdm(self.GAME_TYPE_NAMES)
            for game_type in types_iter:
                types_iter.set_description_str("Type: %s" % game_type)
                self.clean_data_for_season(season, game_type)

if __name__ == '__main__':
    data_cleaner_obj = DataCleaner()
    data_cleaner_obj.clean_data()
