# NHL Goal Prediction Application

This project is a machine learning application designed to predict the probability of a shot scoring a goal in NHL games. This app processes detailed game data and generates probabilistic predictions, providing insights into shot success rates.

---

## Overview

* **Interactive Debugging Tool:** Allows users to visualize events on the rink given a game ID.
* **Dataset Creation:** Pulls data using REST API requests from the official NHL API and creates a comprehensive dataset.
* **Data Analysis:** Creates shot heatmaps for teams in a given year, showing their prefered shooting coordinates.
* **Probability-Based Predictions**: Outputs the likelihood of a shot being a goal rather than a binary classification.
* **Comprehensive Feature Set**: Includes key game dynamics like shot type, location, previous events, and more.
* **Interactive Interface**: Allows users to input game data and receive predictions in a dockerized application.

---

## Interactive Debugging Tool

The interactive debugging tool allows users to visualize events as they occur on the rink. This can be helpful in feature engineering new datasets.

![img](blog/public/outil_de_debuggage.png)

---

## Dataset Creation

An extensive dataset was created, filtering all shots made in regular and playoff seasons between 2016 and 2024 (see ift6758/data/mileston2_data_retriever.py and ift6758/data/data_cleaner_milestone2.py).

| Feature                  | Description                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------ |
| game_id                  | Unique game ID.                                                                      |
| play_id                  | Unique play ID in the current game.                                                  |
| period                   | Period during which the play has occured.                                            |
| is_goal                  | Binary value indicating if a goal was scored.                                        |
| x_coord                  | X coordinate on the rink, normalized to one side, in feet.                           |
| y_coord                  | Y coordinate on the rink, normalized to one side, in feet.                           |
| shot_type                | Type of shot (slap, snap, tip-in, wrist, etc.).                                     |
| is_empty_net             | Binary value indicating if the goalie was in the net at the time of the shot.        |
| distance                 | Distance in feet between the player and the net at the time of the shot.             |
| angle_to_goal            | Angle in degrees between the player and the net at the time of the shot.             |
| game_seconds             | Elapsed time in seconds since the start of the game.                                 |
| last_event_type          | Type of the previous of event (event ID).                                            |
| last_event_x_coord       | X coordinates in feet of the previous play.                                          |
| last_event_y_coord       | Y coordinates in feet of the previous play.                                          |
| time_since_last_event    | Elapsed time in seconds since the last event.                                        |
| distance_from_last_event | Distance in feet covered since last play.                                            |
| rebound                  | Boolean value indicating whether the previous play was a shot.                       |
| angle_change             | Change of angle in degrees between last play and current shot.                       |
| speed                    | Speed in feet per second (distance covered since last play divided by elapsed time). |
| time_since_powerplay     | Elapsed time in seconds since the start of a powerplay (0 if no powerplay).)         |
| away_skaters             | Number of opposing players on the ice.                                               |
| home_skaters             | Number of home team players on the ice.                                              |

The dataset contains approximately 276,000 non-goal shots and 29,000 goals.

---

## Data Analysis

From the dataset, shot maps were created by binning all shots by team, year, and coordinates into an array the size of the rink. Gaussian smoothing was then applied to interpolate continous values between grid lines, thus creating a heatmap. The heatmaps were generated for all teams between 2016 and 2020.

<iframe src="blog/public/excess_shot_rates_2016.html" width="100%" height="500"></iframe>

---

## Model Overview

* **Algorithm**: XGBoost classifier, MLP classifier, Logistic Regression, optimized for probabilistic outputs.
* **Feature Engineering**: Includes calculations like shot angle, distance, and speed, as well as handling categorical variables via one-hot encoding.
* **Imbalance Handling**: Incorporates oversampling techniques such as SMOTE and evaluation metrics tailored for imbalanced datasets.

---

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/hypium/NHL_GoalPredictionApp
   cd nhl-goal-prediction-app
   ```
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Run the app:

   ```
   docker-compose up
   ```

---

## Usage

1. **Input Data**: Provide shot information in the required format via the interactive interface or as a batch CSV file.
2. **View Predictions**: The app will output the probability of each shot resulting in a goal.
3. **Analyze Insights**: Utilize the probabilities to gain deeper insights into game strategies and player performance.

---

## Results

The model achieves strong performance in handling highly imbalanced data, offering accurate probability estimates that align with game outcomes. Evaluation metrics include precision, recall, F1 score, and AUC-ROC.

---

## Future Work

* Expand the dataset with additional seasons and game scenarios.
* Integrate live game data for real-time predictions.
* Experiment with other models and ensemble techniques for enhanced accuracy.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

* NHL for providing publicly available game data.
* XGBoost and Python libraries for their robust machine learning frameworks.
* Contributors and open-source community for inspiration and guidance.

---

## Contact

For questions, suggestions, or contributions, please contact daniel.lofeodo@gmail.com, nathan.cormerais@umontreal.ca

---
## Dataset Overview

The
---
