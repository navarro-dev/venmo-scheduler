#!/usr/bin/env sh

DIRECTORY="venmo-scheduler"

if [ -d "terraform/$DIRECTORY" ]; then
    echo "Deleting old terraform/$DIRECTORY directory"
    rm -drf terraform/$DIRECTORY
fi

mkdir terraform/$DIRECTORY
cp -r $DIRECTORY/* terraform/$DIRECTORY

python -m pip install --upgrade pip
python -m pip install -r requirements.txt -t terraform/$DIRECTORY