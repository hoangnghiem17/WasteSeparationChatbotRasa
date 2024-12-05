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

# New action for explaining bin contents
class ActionExplainBinContents(Action):
    def name(self) -> str:
        return "action_mülltrennung_abfallart"

    def run(
        self, dispatcher: CollectingDispatcher, tracker, domain
    ) -> list:
        abfallart = tracker.get_slot("abfallart")
        
        # Define static bin content mappings
        bin_contents = {
        "altpapier": """Die Altpapiertonne hat einen grünen Deckel mit einem grau/schwarzen Korpus. Hierin gehören Papier und Pappe ohne Beschichtung und unbeschmutzt, sowie:
- Pappen und Kartonagen
- Zeitungen, Illustrierte, Kataloge
- Bücher und Hefte

Nicht in die Altpapiertonne kommt:
- Stark verschmutztes Papier (Restmüll)
- Beschichtetes Papier (Restmüll)
- Pergament- und Hygienepapiere, Windeln (Restmüll)""",

"biomüll": """Die Biotonne hat einen braunen Deckel mit einem grau/schwarzen Korpus. 
Feuchte Biofälle wie Salat- oder Obst- und Gemüsereste können Sie in Zeitungs- oder Küchenpapier wickeln, um die Tonne vor starker Verschmutzung und Geruch zu schützen. 
Darin gehören alle biologisch abbaubaren Abfälle aus privaten Haushalten:
- Obst- und Gemüseabfälle (auch Zitrusfrüchte, Bananen- und Nussschalen)
- Rohe und gekochte Speise- und Lebensmittelreste
- Kaffee- und Teesatz, Filtertüten, Eierschalen
- Grünschnitt und Laub

Nicht in die Biotonne kommt:
- Plastiktüten, Verpackungen aus Kunststoff und Metall (gelbe Verpackungstonne)
- Kehricht und Staubsaugerbeutel (Restmüll)
- Zigarettenkippen (Restmüll)
- Windeln und andere gebrauchte Hygieneartikel (Restmüll)""",

        "verpackung": """Die Verpackungstonne hat einen gelben Deckel mit einem grau/schwarzen Korpus. Hierin gehören alle Verpackungen mit oder ohne Symbol wie den grünen Punkt, die nicht ausschließlich aus Papier, Pappe oder Glas bestehen. Die Verpackungen müssen nicht gespült, aber leer sein. Dazu gehören:
- Verpackungen aus Kunststoff wie Folien, Becher und Styropor
- Verbundverpackungen aus Materialmix (z.B. Alu + Papier) wie Getränkekartons und Milchtüten
- Verpackungen aus Metall wie Konserven- und Getränkedosen
- Geschäumte Kunststoffe, z.B. Obst- und Gemüseverpackungen

Nicht in die Verpackungstonne kommt:
- Verpackungen aus Papier und Pappe (Altpapiertonne)
- Verpackungen aus Glas (Altglascontainer)
- Stark verschmutze Fast-Food-Verpackungen wie Pizzakartons (Restmüll)""",

        "restmüll": """Die Restmülltonne hat einen grau/schwarzen Deckel und Korpus. Hierin gehören alle Abfälle, die aufgrund von Verunreinigung oder Vermischung in keine der anderen 3 Tonnen entsorgt werden können:
- Hygieneartikel (z.B. Taschentücher, Damenbinden, Wattebäusche)
- Windeln
- Staub, Asche, Kehricht
- Zigarettenkippen
- Küchentücher, Putzlappen
- Staubsaugerbeutel
- Kleintierstreu
- Trinkgläser, Porzellan, Keramik, alle Scherben

Nicht in die Restmülltonne kommt:
- Elektrogeräte/Schrott (Kleingeräte: Wertstoffhöfe, Großgeräte: Sperrmüll)
- Batterien (spezielle Sammelbehälter in Supermärkten und öffentlichen Gebäuden)
- Sonderabfall/Schadstoffe wie Farben, Lacke Sprays etc. (Schadstoffmobil)
- Verpackung jeglicher Art
- Bauschutt
- Essensreste""",

        "sperrmüll": """Der Sperrmüllservice bietet Haushalten eine Möglichkeit, große und sperrige Gegenstände wie Möbel, Matratzen oder Teppiche, die nicht in den normalen Hausmüll passen, entsorgen zu lassen durch eine Terminvereinbarung. Das wird entsorgt:
- Alte Möbel
- Elektrogeräte ab einer Kantenlänge von ca. 40 cm
- Teppichböden und Laminat in haushaltsüblichen Mengen
- Alle sperrigen Gegenstände, die bei einem Umzug relevant sind

Das wird nicht entsorgt:
- Einbauten wie Fenster und Türen
- Sanitäre Einrichtungen
- Kleinabfälle mit oder ohne Tüte/Behältnis
- Schadstoffe wie Lacke, Farben, Sprays, Batterien oder auch Energiesparlampen/Leuchtstoffröhren
- Gewerbetypische Abfälle, Autoreifen

Beachte, dass zwischen Terminvergabe und Abholservice ca. 10 Arbeitstage liegen können. 
Terminvereinbarung erfolgt über:
- Internet: unter www.fes-frankfurt.de den Sperrmüllservice anmelden
- Telefon: über 0800 2008007-10 rund um die Uhr erreichbar für Sperrmüllanmeldung
- Servicecenter: persönlich besprechen in Liebfrauenberg 52-54""",

        "altglas": """Die blauen Altglascontainer stehen im gesamten Stadtgebiet an zentralen, gut erreichbaren Plätzen und werden in der Regel alle 14 Tage geleert. Bitte nehmen Sie Rücksicht auf Ihre Mitbürgerinnen und Mitbürger und werfen das Altglas nur an Werktagen von 7.00 - 20.00 Uhr ein. In den Altglascontainer gehören gebrauchte Glasverpackungen nach den Farben weiß, grün und braun getrennt, wobei blaues oder buntes Glas zum Grünglas gehört. Das Entfernen der Deckel ist nicht notwendig. Beispiele zu was darein gehört:
- Getränkeflaschen
- Ketchupflaschen
- Arzneimittelflaschen
- Deckelgläser wie Marmeladengläser
- Cremedosen
- Parfumflacons
Nicht in den Altglascontainer gehört:
- Flachglas wie Spiegel und Scheiben
- Trinkgläser und Blumenvasen
- Porzellan und Keramik
- Leuchtmittel jeglicher Art
- Stark verschmutzte Gläser"""
        }

        if abfallart in bin_contents:
            response = bin_contents[abfallart]
        else:
            response = "Für diese Abfallart habe ich leider keine Informationen."

        dispatcher.utter_message(text=response)
        return []
    
# Action for handling specific item disposal queries
class Query_Entsorgung_EinzelItem(Action):
    def name(self) -> str:
        """
        Defines name of custom action (used to map custom action in domain.yml)
        """
        return "action_mülltrennung_entsorgung_einzelitem"

    @staticmethod # Does not rely on instance-specific data from class, avoid creating an instance of class to execute logic
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
        cursor.execute("SELECT Entsorgungsweg, Adresse, Link FROM abfallABC_entsorgung WHERE LOWER(Abfallart) = LOWER(?)", (item,))
        result = cursor.fetchone()
        logging.debug(f"Query result for {item}: {result}")
        conn.close()
        return result
    
    def run(self,
            dispatcher: CollectingDispatcher, # Sends messages back to user providing utter_message method
            tracker, # Provides context about conversation (slot values, conversation history, latest user message and intent)
            domain # # Contains info about chatbot domain configuration (intents, entities, slots and actions)
            ) -> str:
        """
        Generate a response based on disposal information retrieved from the database.

        Args:
            item_name (str): The name of the item for which disposal information is requested.

        Returns:
            str: A response string providing disposal instructions. The response varies based on the
            completeness of the data retrieved.
        """
        item = tracker.get_slot("item")
        if not item:
            dispatcher.utter_message(text="Ich konnte das zu entsorgende Item nicht erkennen. Kannst du das bitte wiederholen?")
            return []

        try:
            entsorgungsinfo = self.query_disposal_information(item)
            if entsorgungsinfo:
                entsorgungsort, adresse, link = entsorgungsinfo
                entsorgungsort_text = f"Der Entsorgungsort für {item} ist {entsorgungsort}."
                adresse_part = f" bei der folgenden Adresse: {adresse}." if adresse else ""
                link_part = f" Du findest weitere Informationen hier: {link}" if link else ""
                response = entsorgungsort_text + adresse_part + link_part 
                logging.debug(f"Response for '{item}': {response}")
            else:
                response = f"Für {item} konnte ich leider keinen Entsorgungsort finden."
                logging.warning(f"No disposal info found for item '{item}'.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            response = "Es ist ein Fehler aufgetreten. Bitte versuche es später erneut."

        # Send the response to the user and reset slot
        dispatcher.utter_message(text=response)
        return [SlotSet("item", None)]