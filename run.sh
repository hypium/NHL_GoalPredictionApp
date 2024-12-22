#!/bin/bash

IMAGE_NAME_SERVING="ift6758/serving:latest"
CONTAINER_NAME_SERVING="ift6758_projet_serving"

docker run -d --name $IMAGE_NAME_SERVING \
  -e WANDB_API_KEY="$WANDB_API_KEY" \
  -p 8000:8000 \
  $IMAGE_NAME_SERVING

IMAGE_NAME_STREAMLIT="ift6758/streamlit:latest"
CONTAINER_NAME_STREAMLIT="ift6758_projet_streamlit"

docker run -d --name $IMAGE_NAME_STREAMLIT \
  -p 8001:8001 \
  $IMAGE_NAME_STREAMLIT