#!/bin/bash

IMAGE_NAME="ift6758/serving:latest"
docker build --build-arg WANDB_API_KEY="$WANDB_API_KEY" -t $IMAGE_NAME -f Dockerfile.serving .
