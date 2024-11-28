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

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Query_Entsorgung_EinzelItem(Action):
    def name(self) -> str:
        """
        Defines name of custom action (used to map custom action in domain.yml)
        """
        return "action_mülltrennung_entsorgung_einzelitem"

    @staticmethod
    def query_disposal_information(item: str) -> tuple:
        """
        Fetch disposal information from the database for a given item (Abfallart).

        Args:
            item_name (str): Name of the item to query in the database.

        Returns:
            tuple or None: A tuple containing the disposal information:
                - Entsorgungsweg (str): The method or place of disposal (e.g., "Recyclingzentrum").
                - Adresse (str or None): The address of the disposal location, if available.
                - Link (str or None): A URL with more information, if available.
                Returns None if no matching row is found.
        """
        logging.debug(f"Querying database for item: {item}")
        conn = sqlite3.connect("abfallABC_entsorgung.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Entsorgungsweg, Adresse, Link FROM abfallABC_entsorgung WHERE Abfallart = ?", (item,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def run(self, dispatcher: CollectingDispatcher, tracker, domain) -> str:
        """
        Generate a response based on disposal information retrieved from the database.

        Args:
            item_name (str): The name of the item for which disposal information is requested.

        Returns:
            str: A response string providing disposal instructions. The response varies based on the
            completeness of the data retrieved:
                - Case 1: All data (disposal method, address, and link) is available.
                - Case 2: Address is available, but no link is provided.
                - Case 3: Neither address nor link is available.
                - If no data is found, a message indicating the lack of information is returned.
        """
        item = tracker.get_slot("item")
        logging.debug(f"Generating response for item: {item}")

        try:
            entsorgungsinfo = self.query_disposal_information(item)
            logging.debug(f"Database query result for '{item}': {entsorgungsinfo}")

            if entsorgungsinfo:
                entsorgungsort, adresse, link = entsorgungsinfo

                # Case 1: All columns are available
                if adresse and link:
                    response = (
                        f"Der Entsorgungsort für {item} ist {entsorgungsort} "
                        f"bei der folgenden Adresse: {adresse}. "
                        f"Du findest weitere Informationen zu der Adresse hier: {link}"
                    )
                    logging.debug(f"Response for item '{item}' (Case 1): {response}")
                # Case 2: "Link" is empty
                elif adresse and not link:
                    response = (
                        f"Der Entsorgungsort für {item} ist {entsorgungsort} "
                        f"bei der folgenden Adresse: {adresse}."
                    )
                    logging.debug(f"Response for item '{item}' (Case 2): {response}")
                # Case 3: Both "Link" and "Adresse" are empty
                elif not adresse and not link:
                    response = (
                        f"Der Entsorgungsort für {item} ist {entsorgungsort}."
                    )
                    logging.debug(f"Response for item '{item}' (Case 3): {response}")
            else:
                # No results from the database
                response = f"Für {item} konnte ich leider keinen Entsorgungsort finden."
                logging.warning(f"No disposal info found for item '{item}'.")
        except Exception as e:
            # Log any unexpected errors
            logging.error(f"An error occurred while generating response for item '{item}': {e}")
            response = "Es ist ein Fehler aufgetreten. Bitte versuche es später erneut."

        # Send the response to the user and reset slot
        dispatcher.utter_message(text=response)
        return [SlotSet("item", None)]