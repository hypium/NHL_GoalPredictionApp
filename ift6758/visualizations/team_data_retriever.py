import pandas as pd
import os

class TeamDataRetriever:
    def __init__(self, team_id):
        self.team_id = team_id
        self.SEASONS = [year for year in range(2016, 2024)]
        self.TYPES = ["season", "playoffs"]
        
    def get_shots(self) -> pd.DataFrame:
        df = pd.DataFrame()
        for season in self.SEASONS:
            season_df = self.get_shots_for_season(season)
            df = pd.concat([df, season_df], axis=0)
        return df
            
    # return a df with all shot info for a given team in a given season
    def get_shots_for_season(self, season) -> pd.DataFrame:
        season_df = pd.read_csv(f"ift6758/data/{season}/season.csv")
        playoffs_df = pd.read_csv(f"ift6758/data/{season}/playoffs.csv")
        df = pd.concat([season_df, playoffs_df], axis=0)
        df = df[df['team_id'] == self.team_id]
        # put all of the shot info on the same side of the rink
        df = df.apply(self._normalize_shot_coordinates, axis=1)
        return df
    
    def _normalize_shot_coordinates(self, row):
        if row['x_coord'] < 0:
            row['x_coord'] = -row['x_coord']
            row['y_coord'] = - row['y_coord']
        return row

if __name__ == "__main__":
    obj = TeamDataRetriever(1)
    # print(obj.get_shots_for_season("2017"))       - tous les tirs de l'equipe `1` pour la saison `2017`
    # print(obj.get_shots())                        - tous les tirs de l'equipe `1` toute saison confondue
    