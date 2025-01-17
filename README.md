
# NHL Goal Prediction App

This project is a machine learning application designed to predict the probability of a shot scoring a goal in NHL games. Leveraging XGBoost, this app processes detailed game data and generates probabilistic predictions, providing insights into shot success rates.

---

## Features

* **Probability-Based Predictions**: Outputs the likelihood of a shot being a goal rather than a binary classification.
* **Comprehensive Feature Set**: Includes key game dynamics like shot type, location, previous events, and more.
* **Handles Imbalanced Data**: Utilizes techniques to address class imbalance between goal (class 1) and non-goal (class 0) shots.
* **Interactive Interface**: (If applicable) Allows users to input game data and receive predictions.

---

## Dataset Overview

The dataset includes features such as:

* `period`: Current game period.
* `x_coord`, `y_coord`: Shot location coordinates.
* `shot_type`: One-hot encoded types of shots (e.g., wrist, snap, slap).
* `is_empty_net`: Boolean indicating if the net is empty.
* `distance`, `angle_to_goal`: Calculated features for shot distance and angle.
* `game_seconds`: Timestamp within the game.
* Previous event details:
  * `last_event_type`
  * `last_event_x_coord`, `last_event_y_coord`
  * `time_since_last_event`
  * `distance_from_last_event`
* Contextual features:
  * `rebound`: Whether the shot is a rebound.
  * `angle_change`, `speed`: Calculated features based on previous events.

The dataset contains approximately 276,000 non-goal shots and 29,000 goals, requiring careful handling of class imbalance.

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
