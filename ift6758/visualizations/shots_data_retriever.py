import os
import pandas as pd
import requests
from tqdm import tqdm

class ShotsDataRetriever:
    def __init__(self):
        self.YEARS = [year for year in range(2016, 2024)]
        self.TYPES = ["season", "playoffs"]

    def get_all_shots_for_team(self, team_id: int) -> pd.DataFrame:
        df = pd.DataFrame()
        for year in self.YEARS:
            year_df = self.get_year_shots_for_team(year, team_id)
            df = pd.concat([df, year_df], axis=0)

        return df
            
    # return a df with all shot info for a given team in a given year
    def get_year_shots_for_team(self, year: str, team_id: int) -> pd.DataFrame:
        df = self.get_year_shots(year)
        df = df[df['team_id'] == team_id]
        return df
    
    def get_year_shots(self, year: str) -> pd.DataFrame:
        season_path = f"../data/{year}/season.csv"
        if not os.path.exists(season_path):
            print(f"file not found at {season_path}")
            return None

        playoffs_path = f"../data/{year}/playoffs.csv"
        if not os.path.exists(playoffs_path):
            print(f"file not found at {playoffs_path}")
            return None

        season_df = pd.read_csv(f"{season_path}")
        playoffs_df = pd.read_csv(f"{playoffs_path}")

        df = pd.concat([season_df, playoffs_df], axis=0)
        df = df.apply(self._normalize_shot_coordinates, axis=1)
        return df
    
    def _normalize_shot_coordinates(self, row):
        if row['x_coord'] < 0:
            row['x_coord'] = -row['x_coord']

        return row

if __name__ == "__main__":
    obj = ShotsDataRetriever()
    