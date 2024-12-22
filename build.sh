#!/bin/bash

IMAGE_NAME_SERVING="ift6758/serving:latest"
docker build --build-arg WANDB_API_KEY="$WANDB_API_KEY" -t $IMAGE_NAME_SERVING -f Dockerfile.serving .

IMAGE_NAME_STREAMLIT="ift6758/streamlit:latest"
docker build -t $IMAGE_NAME_STREAMLIT -f Dockerfile.streamlit .