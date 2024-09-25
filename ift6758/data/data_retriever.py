import pandas as pd
import requests
import json
import os

class DataRetriever:    
    # 30 teams -> 1230
    # 31 team -> 1271
    # 32 team -> 1353
    
    def __init__(self):
        self.GAME_TYPES = ['02', '03']
        # self.GAME_TYPES = ['01', '02', '03']
        self.GAME_TYPE_NAMES = ['season', 'playoffs']
        # self.GAME_TYPE_NAMES = ['preseason', 'season', 'playoffs']
        self.GAME_COUNTS = {
            '2016': 1230,
            '2017': 1271, 
            '2018': 1271,
            '2019': 1082, # 1271
            '2020': 869,  # 1271
            '2021': 1353, # COVID-19
            '2022': 1353, # 1313 (exact)
            '2023': 1353,
            '2024': 1353, # 1313 (exact)
        }
        self.PLAYOFFS_ROUNDS = 4
        self.PLAYOFFS_GAMES = 7

    def prepare(self):
        for season in self.GAME_COUNTS.keys():
            os.makedirs(f'ift6758/data/{season}', exist_ok=True)
    
    def get_data(self):
        for season in data_obj.GAME_COUNTS.keys():
            data_obj.get_games_for_season(season)
            data_obj.get_playoffs_games_for_season(season)
            
    def get_playoffs_game(self, season, round_id, matchup_id, game_id):
        response = requests.get(f'https://api-web.nhle.com/v1/gamecenter/{season}030{round_id}{matchup_id}{game_id}/play-by-play')
        print(f'{season}03{round_id}{matchup_id}{game_id}\t', response.status_code)
        data = {}
        if response.status_code == 200:
            data = response.json()
        return response.status_code, data
            
    def get_season_game(self, season, game_type_index, formatted_game_id):
        response = requests.get(f'https://api-web.nhle.com/v1/gamecenter/{season}{self.GAME_TYPES[game_type_index]}{formatted_game_id}/play-by-play')
        print(f"{season}{self.GAME_TYPES[game_type_index]}{formatted_game_id}\t", response.status_code)
        data = {}
        if response.status_code == 200:
            data = response.json()
        return response.status_code, data

    def get_games_for_season(self, season):
        data = []
        for game_id in range(1, self.GAME_COUNTS[season] + 1):
            formatted_game_id = str(game_id).zfill(4)
            game_data = self.get_season_game(season, 0, formatted_game_id)
            if game_data[0] == 404:
                with open(f'ift6758/data/{season}/{self.GAME_TYPE_NAMES[0]}.json', 'w') as f:
                    json.dump(data, f)
                return
            data.append(game_data[1])
        with open(f'ift6758/data/{season}/{self.GAME_TYPE_NAMES[0]}.json', 'w') as f:
            json.dump(data, f)

    def get_playoffs_games_for_season(self, season):
        # ROUNDS -> 1 - 4
        # MATCHUPS -> 1 - 8 | 1 - 4 | 1 - 2 | 1
        # GAME -> 1 - 7
        data = []
        for round_id in range(1, self.PLAYOFFS_ROUNDS + 1):
            matchup_nb = 2 ** (4 - round_id)
            for matchup_id in range(1, matchup_nb + 1):
                for game_id in range(1, self.PLAYOFFS_GAMES + 1):
                    game_data = self.get_playoffs_game(season, round_id, matchup_id, game_id)
                    if game_data[0] == 200:
                        data.append(game_data[1])
        with open(f'ift6758/data/{season}/{self.GAME_TYPE_NAMES[1]}.json', 'w') as f:
            json.dump(data, f)

if __name__ == "__main__":
    data_obj = DataRetriever()
    data_obj.prepare()
    data_obj.get_data()
