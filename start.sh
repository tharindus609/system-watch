#!/bin/bash
echo "starting system-watch"
nohup python3 drive-watch.py &
PID=$!
echo "drive-watch started with PID $PID and is running in the background."