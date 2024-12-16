#!/bin/bash

# Start the Rasa NLU server in the background
echo "Starting Rasa NLU server..."
rasa run --enable-api --cors "*" --port 5005 &

# Start the Rasa Action server in the foreground
echo "Starting Rasa Action server..."
rasa run actions --port 5055
