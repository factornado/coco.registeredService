#!/bin/bash
echo "$(dirname "$0")"
cd "$(dirname "$0")"

# Create the conda environement
###############################

ENV_MD5="$(md5sum env.yml | cut -d " " -f 1)"
ENV_NAME="$(head -1 env.yml | cut -d " " -f 2)"
ENV_NAME=$(echo ${ENV_NAME}_${ENV_MD5})
ENV_NAME=${ENV_NAME:0:16}

conda env create -f env.yml -n $ENV_NAME --force
echo "Created env $ENV_NAME"


# Create the supervisord.conf file
##################################
SERVICE_NAME="$(head -1 config.yml | cut -d " " -f 2)"
SERVICE_VERSION="$(head -2 config.yml | tail -1 | cut -d " " -f 2)"
echo "[program:$SERVICE_NAME-$SERVICE_VERSION]" > supervisord.conf
echo "command=$PWD/run.sh" >> supervisord.conf
echo "stopasgroup=true" >> supervisord.conf
echo "autostart=false" >> supervisord.conf

