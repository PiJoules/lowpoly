#!/bin/sh

# Run this every time you install new libraries via pip

sudo rm -rf lib/!(README.md)
sudo pip install -r requirements.txt -t lib/