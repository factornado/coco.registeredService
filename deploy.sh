#!/bin/bash

TARGET_DIR=$1
SERVICE_NAME=$2
SERVICE_VERSION=$3

if [[ $SERVICE_VERSION == "" ]]; then
    echo "ERROR : You must provide 3 arguments:"
    echo "    * TARGET_DIR"
    echo "    * SERVICE_NAME"
    echo "    * SERVICE_VERSION"
    exit 64
fi

if [ -d "$TARGET_DIR" ]; then
  echo ERROR : directory $TARGET_DIR already exists
  exit 64
fi

# We copy the files from template to target.
cp -R $(dirname "$0")/templates $TARGET_DIR

# We rename COCO_ variables to target names.
sed -i s/COCO_SERVICE_NAME/$SERVICE_NAME/g $TARGET_DIR/*
sed -i s/COCO_SERVICE_VERSION/$SERVICE_VERSION/g $TARGET_DIR/*
