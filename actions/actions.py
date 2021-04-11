# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import secrets
import wikipedia


class ActionTellJoke(Action):

    def name(self) -> Text:
        return "action_tell_joke"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        jokeCat = ["good", "bad", "ok"]

        # Tell a random joke and ask for feedback
        dispatcher.utter_message(response="utter_" + secrets.choice(jokeCat) + "_joke")
        dispatcher.utter_message(response="utter_ask_for_feedback")

        return []


class ActionHandleFeedback(Action):

    def name(self) -> Text:
        return "action_handle_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        recentSentiment = next(tracker.get_latest_entity_values("sentiment"),
                               None)  # Extracts the most recent sentiment
        if recentSentiment == "pos":
            dispatcher.utter_message(response="utter_feedback_good")  # Utter good feedback response, only if feedback
            # is good
        elif recentSentiment is None:
            dispatcher.utter_message(response="utter_default")  # Handle case where there is no intent/sentiment
            # extracted
        else:
            dispatcher.utter_message(response="utter_feedback_bad")  # If feedback is neutral or negative utter bad
            # feedback

        return []


class ActionWikipedia(Action):

    def name(self) -> Text:
        return "action_wikipedia_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        recentSearch = next(tracker.get_latest_entity_values("searchtext"),
                            None)  # Extracts the most recent search text
        try:
            page_py = wikipedia.page(wikipedia.search(recentSearch)[0])
            # Display a summary of the wikipedia page and provide a link to the full page
            outStr = "Here is what I found on Wikipedia: \n " + page_py.summary[
                                                                    0:250] + "...\n Here is the full link to the page: " + page_py.url
            dispatcher.utter_message(text=outStr)
        except wikipedia.exceptions.DisambiguationError as e:
            dispatcher.utter_message(text="Sorry, I couldn't find that page on Wikipedia! It is a disambiguation "
                                          "error, so try saying something more specific, like: 'look up Lexus("
                                          "company)'")
        except wikipedia.exceptions.WikipediaException as e:
            dispatcher.utter_message(text="Sorry, I couldn't find that page on Wikipedia! Please check your spelling "
                                          "or rephrase the word")

        return []
