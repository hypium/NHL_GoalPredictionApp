import numpy as np
import os
import pandas as pd
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
    
    # return a df of shots for a given year and season type
    def get_year_shots_for_season_type(self, year: str, season_type: str, milestone: int = 1):
        if milestone == 2:
            dir = f"../data/milestone2/{year}"
        else:
            dir = f"../data/{year}"

        if season_type not in self.TYPES:
            print(f"Invalid season type: {season_type}")
            return None
        
        shots_path = f"{dir}/{season_type}.csv"
        if not os.path.exists(shots_path):
            print(f"file not found at {shots_path}")
            return None
        
        df = pd.read_csv(f"{shots_path}")
        df = df.apply(self._normalize_shot_coordinates, axis=1)

        return df
    
    def get_season_type_shots_in_years(self, years: list[str], season: str, milestone: int = 1):
        df = pd.DataFrame()
        for year in years:
            year_df = self.get_year_shots_for_season_type(year, season, milestone)
            df = pd.concat([df, year_df], axis=0)

        return df
                
    # return a df with all shot info for a given team in a given year
    def get_year_shots_for_team(self, year: str, team_id: int) -> pd.DataFrame:
        df = self.get_year_shots(year)
        df = df[df['team_id'] == team_id]
        return df
    
    def get_year_shots(self, year: str) -> pd.DataFrame:
        season_df = self.get_year_shots_for_season_type(year, "season")
        playoffs_df = self.get_year_shots_for_season_type(year, "playoffs")

        df = pd.concat([season_df, playoffs_df], axis=0)
        return df
    
    def get_df_for_milestone2_part2(self):
        years = [str(year) for year in range(2016,2020)]

        df = self.get_season_type_shots_in_years(years, "season")

        df['distance'] = np.sqrt((df['x_coord'] - 90)**2 + df['y_coord']**2)
        df['angle_to_goal'] = np.degrees(np.arctan2(df['y_coord'], 90 - df['x_coord']))
        
        #? OLD
        # df.drop(['game_id', 'period', 'team_id', 'shooter_name', 'goalie_name', 'time_remaining', 'time_in', 'situation_type', 'x_coord', 'y_coord', 'shot_type'], 
        #         axis=1,
        #         inplace = True)

        return df
    
    def get_df_for_milestone2_part4(self):
        years = [str(year) for year in range(2016,2020)]
        df = self.get_season_type_shots_in_years(years, "season", 2)

        return df
    
    def _normalize_shot_coordinates(self, row):
        if row['x_coord'] < 0:
            row['x_coord'] = -row['x_coord']

        return row
    
    def _convert_to_seconds(self, time: str):
        time_arr = time.split(':')

        if len(time_arr)==2:
            seconds = int(time_arr[0]) * 60 + int(time_arr[1])
        elif len(time_arr)==1:
            seconds = int(time_arr[0])
        else:
            print("Error, too many indices in time_arr")

        return seconds

if __name__ == "__main__":
    obj = ShotsDataRetriever()
    