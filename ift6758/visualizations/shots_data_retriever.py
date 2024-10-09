import os
import pandas as pd
import requests

class ShotsDataRetriever:
    def __init__(self):
        self.SEASONS = [year for year in range(2016, 2024)]
        self.TYPES = ["season", "playoffs"]
        self.TEAM_IDS = self._get_team_ids()
        
    def get_all_shots(self):
        df = pd.DataFrame()
        for team_id in self.TEAM_IDS:
            team_df = self.get_all_shots_for_team(team_id)
            df = pd.concat([df, team_df], axis=0)
            print(f"Obtaining data for team {team_id}...")

        return df

    def get_all_shots_for_team(self, team_id) -> pd.DataFrame:
        df = pd.DataFrame()
        for season in self.SEASONS:
            season_df = self.get_season_shots_for_team(season, team_id)
            df = pd.concat([df, season_df], axis=0)

        return df
            
    # return a df with all shot info for a given team in a given season
    def get_season_shots_for_team(self, season, team_id) -> pd.DataFrame:
        season_path = f"../data/{season}/season.csv"
        if not os.path.exists(season_path):
            print(f"file not found at {season_path}")

        playoffs_path = f"../data/{season}/playoffs.csv"
        if not os.path.exists(playoffs_path):
            print(f"file not found at {playoffs_path}")

        season_df = pd.read_csv(f"{season_path}")
        playoffs_df = pd.read_csv(f"{playoffs_path}")

        df = pd.concat([season_df, playoffs_df], axis=0)
        df = df[df['team_id'] == team_id]
        # put all of the shot info on the same side of the rink
        df = df.apply(self._normalize_shot_coordinates, axis=1)
        return df
    
    def _normalize_shot_coordinates(self, row):
        if row['x_coord'] < 0:
            row['x_coord'] = -row['x_coord']
            row['y_coord'] = - row['y_coord']

        return row
    
    def _get_team_ids(self):
        response = requests.get('https://api.nhle.com/stats/rest/en/team')
        data = {}
        if response.status_code == 200:
            data = response.json()
            franchise_ids = [team['franchiseId'] for team in data['data'] if team['franchiseId'] is not None]
            return list(set(franchise_ids))
        
        print("ShotsDataRetriever - _get_team_ids - unable to find teams")
        return None

if __name__ == "__main__":
    obj = ShotsDataRetriever()
    