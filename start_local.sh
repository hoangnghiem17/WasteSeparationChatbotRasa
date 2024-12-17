#!/bin/bash

echo "Starting Rasa Server..."
rasa run --enable-api &

echo "Starting Rasa Actions Server..."
rasa run actions &

echo "Starting Flask Application..."
python rasa_app/app.py &

# Wait for all background processes to finish
wait
