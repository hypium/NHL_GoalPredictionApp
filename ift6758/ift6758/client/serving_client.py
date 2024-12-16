import json
import requests
import pandas as pd
import logging


logger = logging.getLogger(__name__)


class ServingClient:
    def __init__(self, ip: str = "0.0.0.0", port: int = 5000, features=None):
        self.base_url = f"http://{ip}:{port}"
        logger.info(f"Initializing client; base URL: {self.base_url}")

        if features is None:
            features = ["distance"]
        self.features = features


    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the inputs into an appropriate payload for a POST request, and queries the
        prediction service. Retrieves the response from the server, and processes it back into a
        dataframe that corresponds index-wise to the input dataframe.
        
        Args:
            X (Dataframe): Input dataframe to submit to the prediction service.
        """
        response = requests.post(f"{self.base_url}/predict", json=json.loads(X.to_json()))
        if response.status_code == 200:
            return pd.DataFrame(response.json(), columns=['goal_proba'])
        else:
            logger.error(f"Failed to make predictions: {response.text}")
            return pd.DataFrame(columns=["goal_proba"])


    def logs(self) -> dict:
        """Get server logs"""
        response = requests.get(f"{self.base_url}/logs")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get logs: {response.text}")
            return {}


    def download_registry_model(self, workspace: str, model: str, version: str) -> dict:
        """
        Triggers a "model swap" in the service; the workspace, model, and model version are
        specified and the service looks for this model in the model registry and tries to
        download it. 
        
        Args:
            workspace (str): The wandb workspace and project
            model (str): The model in the wandb artifact registry to download
            version (str): The model version to download
        """

        payload = {"workspace": workspace, "model": model, "version": version}
        response = requests.post(f"{self.base_url}/download_registry_model", payload)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to download registry model: {response.text}")
            return {}
