import requests
import logging

from flask import Flask, request, jsonify, render_template

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Receives user input, forwards it to Rasa and send Rasa's response back to user
app = Flask(__name__)

# Rasa server URL
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# Serves at chat interface
@app.route('/')
def index():
    logging.info("Rendering index.html")
    return render_template('index.html')

# Receives user input, forwards it to Rasa (POST) and send Rasa's response back to user
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        logging.warning("No message provided in user request.")
        return jsonify({"error": "No message provided"}), 400

    # Send the user's message to Rasa
    payload = {"sender": "user", "message": user_message}
    logging.debug(f"Sending payload to Rasa: {payload}")
    try:
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()
        rasa_response = response.json()
        logging.info(f"Received response from Rasa: {rasa_response}")
        return jsonify(rasa_response)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to Rasa server: {str(e)}")
        return jsonify({"error": f"Failed to connect to Rasa server: {str(e)}"}), 500

if __name__ == '__main__':
    logging.info("Starting Flask application...")
    app.run(port=8000, debug=True)
