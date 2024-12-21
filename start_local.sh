#!/bin/bash

echo "Starting Rasa Server..."
rasa run --enable-api &

echo "Starting Rasa Actions Server..."
rasa run actions &

echo "Starting Flask Application..."
python rasa_app/app.py &

# Wait until Flask (port 8000) is up using Python
while ! python -c "import socket; s = socket.socket(); s.settimeout(1); print(s.connect_ex(('localhost', 8000)) == 0)" | grep -q True; do
  sleep 1
done

echo "Flask is up. Starting Ngrok..."
D:/ngrok-v3-stable-windows-amd64/ngrok http 8000
