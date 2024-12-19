import os
from pathlib import Path
import logging
from flask import Flask, jsonify, request, abort
import sklearn
import pandas as pd
import joblib
from waitress import serve
import wandb

WANDB_API_KEY = os.getenv("WANDB_API_KEY", "API key not set")
wandb.login(key=WANDB_API_KEY)
LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

app = Flask(__name__) 

api = wandb.Api()

model = None
model_name = "default_model"

@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""
    try:
        with open(LOG_FILE, 'r') as file:
            log_data = file.read().splitlines()
        return jsonify(log_data)
    except Exception as e:
        app.logger.error(f"Error reading log file: {e}")
        return jsonify({"error": "Failed to read log file"}), 500


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model
    to download and update the model from wandb

    The request body should be in the following JSON format:
    {
        "directory": "<workspace_name>/<project_name>",
        "model": "<model_name>",
        "version": "<model_version>"
    }
    """
    global model
    global model_name

    # Get POST json data
    data = request.get_json()
    workspace = data.get("workspace")
    model_name = data.get("model")
    version = data.get("version")

    app.logger.info(f"Received request to download model: {model_name} version {version} from workspace {workspace}")

    try:
        # Check if the model is already downloaded
        model_path = f"{model_name}.pkl"
        if Path(model_path).exists():
            # Load the saved model
            model = joblib.load(model_path)
            app.logger.info(f"Model {model_name} version {version} loaded from disk.")
        else:
            # Try downloading the model if it is not found on the disk
            artifact_name = f"{workspace}/{model_name}:{version}"
            artifact = api.artifact(artifact_name)
            artifact.download()
            # Load the model
            file_wrapper = artifact.files()[0].download()
            model_path = file_wrapper.name
            app.logger.info(f"Attemping to load model {model_name} version {version}")
            model = joblib.load(model_path)
            app.logger.info(f"Model {model_name} version {version} downloaded and loaded succesfully.")

        return jsonify({"message": f"Model {model_name} version {version} successfully loaded."})

    except Exception as e:
        app.logger.error(f"Error loading model {model_name} version {version}: {e}")
        return jsonify({"error": "Failed to download and load the model"}), 500


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Predicts the probability that a shot will be a goal based on input features.
    
    The request body should be in the following JSON format:
    {
        'distance': {0: ..., 1: ..., ...},
        'angle_to_goal': {0: ..., 1: ..., ...}  # Optional, depending on model
    }

    This is done by passing payload=X.to_dict() where X is the input DataFrame
    """
    global model
    global model_name

    # Get POST json data
    data = request.get_json()
    app.logger.info(f"Received prediction request: {data}")

    if model is None:
        return jsonify({"error": "Model not yet loaded."}), 400
    
    try:
        if model_name == "base_distance_angle":
            if "distance" not in data or "angle_to_goal" not in data:
                return jsonify({"error": "'distance' and 'angle_to_goal' features are required for this model."})
            distance = list(data['distance'].values())
            angle_to_goal = list(data['angle_to_goal'].values())
            X = pd.DataFrame({"distance": distance, "angle_to_goal": angle_to_goal})
        elif model_name == "base_distance":
            if "distance" not in data:
                return jsonify({"error": "'distance' feature is required for this model."})
            distance = list(data['distance'].values())
            X = pd.DataFrame({"distance": distance})
        else:
            return jsonify({f"error": "unknown model: {model_name}"})
    
        prediction = model.predict_proba(X)
        response = prediction[:, 1].tolist() # Class 1 is the goal probability.
        app.logger.info(f"Prediction result: {response}")
        return jsonify(response)
    
    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": "Prediction failed"}), 500

@app.route("/model", methods=["GET"])
def get_model():
    return jsonify({"model": model_name})

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)
