#!/bin/sh

mv "$SETTINGS" .env
rsync .env $SERVER:$BASE_DIR
rsync Makefile $SERVER:$BASE_DIR
rsync docker-compose.yaml $SERVER:$BASE_DIR
rsync scripts/deploy.sh $SERVER:$BASE_DIR
ssh $SERVER  "cd $BASE_DIR  && chmod 544 deploy.sh && exit"


