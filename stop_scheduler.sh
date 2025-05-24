#!/bin/bash

echo "Stopping reward seat tracker scheduler..."

# Kill the scheduler process
pkill -f scheduler.py

if [ $? -eq 0 ]; then
    echo "✓ Scheduler stopped successfully"
else
    echo "No scheduler process found"
fi