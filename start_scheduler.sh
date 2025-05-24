#!/bin/bash

# Start the reward seat tracker scheduler
cd /Users/sahil/reward-seat-tracker

echo "Starting Reward Seat Tracker Scheduler..."
echo "Will check flights at 9:00 AM and 8:00 PM daily"
echo "Press Ctrl+C to stop"

python scheduler.py