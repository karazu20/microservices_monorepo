#!/bin/sh

export ALEJANDRIA_IMAGE=$1 
export CI_COMMIT_SHORT_SHA=$2
export ALEJANDRIA_IMAGE_FULL=$1:$2
make deploy
