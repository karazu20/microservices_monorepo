#!/bin/sh

docker login
docker build -t "podemosprogresar/${SERVICE_IMAGE}:${CI_COMMIT_SHORT_SHA}" -t "podemosprogresar/${SERVICE_IMAGE}:latest" -f "infrastructure/dockerfiles/${DOCKER_FILE}" --no-cache .
docker push "podemosprogresar/${SERVICE_IMAGE}" --all-tags
