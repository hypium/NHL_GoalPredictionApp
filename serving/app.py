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
            app.logger.info(f"Attemping to load model {model_name} version {version}")
            app.logger.info(f"Model files: {artifact.files()}")
            app.logger.info(f"Model file: {artifact.files()[0]}")
            file_wrapper = artifact.files()[0].download()
            model_path = file_wrapper.name
            app.logger.info(f"Model path: {model_path}")
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
        "distance": <value>,
        "angle_to_goal": <value>
    }
    """
    global model

    # Get POST json data
    data = request.get_json()
    app.logger.info(f"Received prediction request: {data}")

    if model is None:
        return jsonify({"error": "Model not yet loaded."}), 400
    
    input_data = pd.DataFrame([data])

    try:
        # Predict the probability of a goal using the loaded model
        prediction = model.predict_proba(input_data)
        response = prediction.tolist()
        app.logger.info(f"Prediction result: {response}")
        return jsonify(response)
    
    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": "Prediction failed"}), 500
    

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)
