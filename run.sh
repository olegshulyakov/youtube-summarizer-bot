#!/bin/bash

image_name="youtube-summarizer-bot"
container_name="youtube-summarizer-bot"

docker build -t "$image_name" .
docker stop "$container_name" &>/dev/null || true
docker rm "$container_name" &>/dev/null || true

docker run -d \
    -e TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN" \
    --name "$container_name" \
    --restart always \
    "$image_name"

docker image prune -f