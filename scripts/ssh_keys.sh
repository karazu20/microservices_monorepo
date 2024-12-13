#!/bin/sh

DEPLOY_ENV=$1
if [ -z $DEPLOY_ENV ]; then
    DEPLOY_ENV="staging"
fi;

configureKeys(){
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    touch ~/.ssh/known_hosts
    chmod 644 ~/.ssh/known_hosts

    eval $(ssh-agent -s)

    local DEPLOY_ENV=$1

    if [ $DEPLOY_ENV == "production" ]; then
        echo "$SSH_PRODUCTION_APP_PRIVATE_KEY" | ssh-add -
        echo "$SSH_PRODUCTION_APP_KNOWN_HOSTS" >> ~/.ssh/known_hosts
    else
        echo "$SSH_ENOLA_PRIVATE_KEY" | ssh-add -
        echo "$SSH_ENOLA_KNOWN_HOSTS" >> ~/.ssh/known_hosts
    fi
}

configureKeys $DEPLOY_ENV
