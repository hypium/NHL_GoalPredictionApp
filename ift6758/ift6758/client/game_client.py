import numpy as np
import pandas as pd
import requests
import sys
print(sys.path)
from serving_client import ServingClient

class GameClient:
    def __init__(self):
        # event_map contains key value pairs where the keys are the event id
        # and the values are the goal probabilities for that event.
        self.event_map = {}
        self.servingClient = ServingClient(ip="127.0.0.1", port=8000)


    def fetch_game_data(self, game_id):
        response = requests.get(f'https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play')
        if response.status_code == 200:
            return response.json()
        else:
            return None
        

    def ping_server(self, game_id, processed_events_ids=[]):
        game_data = self.fetch_game_data(game_id)
        for play in game_data['plays']:
            event_id = play['eventId']
            if (event_id not in processed_events_ids) and (play["typeCode"] not in {505, 506} or event_id in self.event_map):
                # only consider shots and unhandled events
                continue

            try:
                x_coord = np.abs(play['details']['xCoord'])
                y_coord = play['details']['yCoord']
            except:
                # The data does not contain the required details, we skip over this shot
                continue

            distance = np.hypot(x_coord - 90, y_coord)
            angle_to_goal = np.degrees(np.arctan2(y_coord, 90 - x_coord))
            df = pd.DataFrame([{'distance': distance, 'angle_to_goal': angle_to_goal}])
            processed_events_ids.append(event_id)
            
            # There should only be a single probability in the output
            prediction = self.servingClient.predict(X=df)
            goal_proba = prediction.loc[0, 'goal_proba']
            
            self.event_map[event_id] = goal_proba
        
        return self.event_map, processed_events_ids

    
    def set_model(self, _workspace: str, _model: str, _version: str):
        self.servingClient.download_registry_model(workspace=_workspace, 
                                                   model=_model, version=_version)
        
    def get_model(self):
        return self.servingClient.model()['model']
        
    
            

