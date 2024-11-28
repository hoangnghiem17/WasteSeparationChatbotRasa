# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import logging

from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Query_Entsorgung_EinzelItem(Action):
    def name(self) -> str:
        return "action_mülltrennung_entsorgung_einzelitem"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        # Extract the entity
        item = tracker.get_slot("item")
        logging.info(f"Received request to query disposal information for: {item}")
        
        # Query the database
        conn = sqlite3.connect("abfallABC_entsorgung.db")
        cursor = conn.cursor()
        query = "SELECT Entsorgungsweg, Adresse FROM abfallABC_entsorgung WHERE Abfallart = ?"
        cursor.execute(query, (f"%{item}%",))
        result = cursor.fetchone()
        conn.close()
        logging.info(f"Query result: {result}")
        
        # Respond to the user
        if result:
            entsorgungsweg, addresse = result
            response = f"Du kannst '{item}' wie folgt entsorgen: {entsorgungsweg}. Die Adresse ist: {addresse}."
            logging.info(f"Response generated: {response}")
        else:
            response = f"Entschuldigung, ich konnte keine Informationen zur Entsorgung von '{item}' finden."
            logging.warning(f"No data found for item: {item}")
            
        dispatcher.utter_message(text=response)
        return [SlotSet("item", None)]
