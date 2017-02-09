#!/bin/bash
cd "$(dirname "$0")"

#export SUPERNADO_PATH=$(pwd)
#export SUPERNADO_SERVICE=$1
#export PATH="~/miniconda/bin:$PATH"

#cd services/$1/

#MD5="$(md5sum services/$1/env.yml | cut -d " " -f 1)"
#NAME="$(head -1 services/$1/env.yml | cut -d " " -f 2)"
MD5="$(md5sum env.yml | cut -d " " -f 1)"
NAME="$(head -1 env.yml | cut -d " " -f 2)"

ENV_NAME=$(echo ${NAME}_${MD5})
ENV_NAME=${ENV_NAME:0:16}


source activate $ENV_NAME
#python services/$1/main.py
python main.py
