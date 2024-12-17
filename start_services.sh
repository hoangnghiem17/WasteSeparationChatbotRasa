#!/bin/bash

# Start the Rasa NLU server on the Heroku-provided $PORT
echo "Starting Rasa NLU server on port $PORT..."
rasa run --enable-api --cors "*" --port $PORT &

# Start the Rasa Action server on port 5055
echo "Starting Rasa Action server..."
rasa run actions --port 5055
