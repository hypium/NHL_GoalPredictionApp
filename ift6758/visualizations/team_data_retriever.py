import pandas as pd
import os

class TeamDataRetriever:
    def __init__(self, team_id):
        self.team_id = team_id
        self.valid_years = [year for year in range(2016, 2024)]
        self.valid_seasons = ["season", "playoffs"]
    
    # return a df with all shot info for a given team in a given season in a given year
    def get_shot_data(self, year, season) -> pd.DataFrame:
        if year not in self.valid_years:
            print(f"TeamDataRetriever - get_shot_data - invalid year: {year}")
            print(f"Valid values: {self.valid_years}")
            return None
        if season not in self.valid_seasons:
            print(f"TeamDataRetriever - get_shot_data - invalid season: {season}")
            print(f"Valid values: {self.valid_seasons}")
            return None
        
        path = f"../data/{year}/{season}.csv"
        if not os.path.exists(path):
            print(f"file not found at {path}")

        raw_data = pd.read_csv(path)
        team_data = raw_data[raw_data['team_id'] == self.team_id]

        return team_data