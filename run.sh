#!/bin/bash

IMAGE_NAME="ift6758/serving:latest"
CONTAINER_NAME="ift6758_projet"

docker run -d --name $CONTAINER_NAME \
  -e WANDB_API_KEY="$WANDB_API_KEY" \
  -p 8000:8000 \
  $IMAGE_NAME
