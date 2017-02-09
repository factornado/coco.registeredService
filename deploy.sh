#!/bin/bash
cd "$(dirname "$0")"

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

echo $TARGET_DIR
echo $SERVICE_NAME
echo $SERVICE_VERSION
cp -R templates $TARGET_DIR
sed -i s/COCO_SERVICE_NAME/$SERVICE_NAME/g $TARGET_DIR/*
sed -i s/COCO_SERVICE_VERSION/$SERVICE_VERSION/g $TARGET_DIR/*

echo "done. Go to $$TARGET_DIR"