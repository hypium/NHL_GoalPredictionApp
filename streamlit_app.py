import streamlit as st
import pandas as pd
import numpy as np
import requests
import sys
import json

if not './ift6758/ift6758/client' in sys.path:
    sys.path.append('./ift6758/ift6758/client')

from ift6758.ift6758.client.game_client import GameClient

# TODO
#? SWITCH FROM select TO text input:
#     st.text_input(
#         "Placeholder for the other text input widget",
#         "This is a placeholder",
#         key="placeholder",
#     )

# """
# General template for your streamlit app. 
# Feel free to experiment with layout and adding functionality!
# Just make sure that the required functionality is included as well
# """

gc = GameClient()
processed_games_events = {}
processed_events_ids = []
game_id_input = None
game_btn = None
game_data = None
data = {}

def get_model():
    gc.set_model(_workspace=workspace_input, _model=model_input, _version=version_input)
    
def get_team_logos(game_id):
    game_data = gc.fetch_game_data(game_id)
    return game_data['awayTeam']['logo'], game_data['homeTeam']['logo']
    
def get_team_names(game_id):
    game_data = gc.fetch_game_data(game_id)
    return game_data['awayTeam']['commonName']["default"], game_data['homeTeam']['commonName']["default"]

def get_clock(game_id):
    game_data = gc.fetch_game_data(game_id)
    return game_data['periodDescriptor']['number'], game_data['clock']['timeRemaining']

def get_score(game_id):
    game_data = gc.fetch_game_data(game_id)
    return game_data['awayTeam']['score'], game_data['homeTeam']['score']
    
def ping_game(game_id):
    if game_id in processed_games_events:
        data = gc.ping_server(game_id_input, processed_games_events[game_id])
    else:
        data = gc.ping_server(game_id_input)
    return data

def get_team_events_ids(game_id):
    data = gc.fetch_game_data(game_id)
    away_team_id = data['awayTeam']['id']
    home_team_id = data['homeTeam']['id']
    away_team_event_ids = []
    home_team_event_ids = []
    for play in data['plays']:
        event_id = play['eventId']
        if play["typeCode"] not in {505, 506}:
            # only consider shots and unhandled events
            continue
        try:
            event_id = play['eventId']
            team_id = play['details']['eventOwnerTeamId']
            if team_id == away_team_id:
                away_team_event_ids.append(event_id)
            elif team_id == home_team_id:
                home_team_event_ids.append(event_id)
            else:
                raise ValueError(f'Incorrect team id for event id: {event_id}') 
        except:
            # The data does not contain the required details, we skip over this shot
            continue
    return away_team_event_ids, home_team_event_ids

def get_total_xg(data, game_id):
    away_team_events_ids, home_team_events_ids = get_team_events_ids(game_id)
    away_team_xgs = []
    home_team_xgs = []
    for event_id, xg in data.items():
        if event_id in away_team_events_ids:
            away_team_xgs.append(xg)
        elif home_team_events_ids:
            home_team_xgs.append(xg)
        else:
            raise ValueError(f'Event {event_id} does not belong to any team')
    return np.sum(away_team_xgs), np.sum(home_team_xgs)

def get_distance_angle(game_id):
    data = gc.fetch_game_data(game_id)
    events_distance = []
    events_angle = []
    for play in data['plays']:
        if play["typeCode"] in {505, 506}:
            x_coord = np.abs(play['details']['xCoord'])
            y_coord = play['details']['yCoord']
            distance = np.hypot(x_coord - 90, y_coord)
            angle_to_goal = np.degrees(np.arctan2(y_coord, 90 - x_coord))
            events_distance.append(distance)
            events_angle.append(angle_to_goal)
    return events_distance, events_angle

st.title("IFT6758 - Hockey Visualization App")

with st.sidebar:
    # TODO: Add input for the sidebar
    workspace_input = st.selectbox(
        "Workspace",
        ("IFT6758-2024-A02/IFT6758.2024-A02"),
        index=None,
        placeholder="Select workspace...",
    )
    model_input = st.selectbox(
        "Model",
        ("base_distance", "base_distance_angle"),
        index=None,
        placeholder="Select model...",
    )
    version_input = st.selectbox(
        "Version",
        ("v1", "v2"),
        index=None,
        placeholder="Select version...",
    )
    if st.button("Get model"):
        get_model()

with st.container():
    # TODO: Add Game ID input
    game_id_input = st.text_input(
        "Game ID",
        value=None,
        placeholder="Select game ID...",
    )
    game_btn = st.button("Ping game")

with st.container():
    # TODO: Add Game info and predictions
    if game_btn:
        if game_id_input is not None:
            with st.spinner("Fetching data..."):
                data, processed_games_events[game_id_input] = ping_game(game_id_input)
            if len(data) == 0:
                st.error(f"Error fetching data: {data['error']}")
            else:
                away_team_name, home_team_name = get_team_names(game_id_input)
                st.markdown(
                    f"<h3><span style='text-decoration: underline;'>Game {game_id_input}</span>: {away_team_name} vs. {home_team_name}</h3>", 
                    unsafe_allow_html=True
                )
                period, time_remaining = get_clock(game_id_input)
                st.write(f"Period {period} | {time_remaining} left")
                away_team_logo, home_team_logo = get_team_logos(game_id_input)
                away_team_score, home_team_score = get_score(game_id_input)
                away_team_xg, home_team_xg = get_total_xg(data, game_id_input)
                col1, col2 = st.columns(2)
                col1.markdown(f"<img style='width: 5rem;' src='{away_team_logo}'/>", unsafe_allow_html=True)
                col2.markdown(f"<img style='width: 5rem;' src='{home_team_logo}'/>", unsafe_allow_html=True)
                col1.metric(f'{away_team_name} xG', f'{away_team_xg:.1f} ({away_team_score})', f'{away_team_xg - away_team_score:.1f}')
                col2.metric(f'{home_team_name} xG', f'{home_team_xg:.1f} ({home_team_score})', f'{home_team_xg - home_team_score:.1f}')

with st.container():
    # TODO: Add data used for predictions
    if game_btn:
        st.markdown(
            f"<h3>Data used for predictions (and predictions)</h3>", 
            unsafe_allow_html=True
        )
        game_data = gc.fetch_game_data(game_id_input)
        model = gc.get_model()
        df = pd.DataFrame(list(data.items()), columns=["id", "Model output"])
        df.index = [f"event {i}" for i in range(len(df))]
        distances, angles = get_distance_angle(game_id_input)
        df = pd.DataFrame(data.values(), columns=["Model output"])
        if model == 'base_distance':
            df['distance'] = distances
        elif model == 'base_distance_angle':
            df['distance'] = distances
            df['angle_to_goal'] = angles
        st.dataframe(df)
