import sys
import os
import wikipedia
from chatterbot import ChatBot
from chatterbot.logic import BestMatch, MathematicalEvaluation

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add the required directories to the python path
sys.path.append(os.path.join(project_root, 'scr', 'Roba_conversion_ai'))
sys.path.append(os.path.join(project_root, 'scr', 'Roba_conversion_ai', 'data'))
sys.path.append(os.path.join(project_root, 'scr', 'Robamain'))


class RobaChatbot:
    """
    The RobaChatbot class handles the conversational AI for the Roba robot.
    It uses the ChatterBot library for responding to queries and falls back to Wikipedia
    if it's not confident about the answer.
    """

    def __init__(self, confidence_threshold=0.55):
        """
        Initializes the RobaChatbot.
        Args:
            confidence_threshold (float): The confidence level above which the chatbot will respond.
        """
        self.stop_words = {"what", "is", "can", "you", "tell", "me", "about", "said", "ok", "i", "understand", "but",
                           "who", "asked", "please", "know", "do", "which"}
        self.confidence_threshold = confidence_threshold

        # The database URI should be configurable.
        db_path = os.path.join(project_root, 'scr', 'Roba_conversion_ai', 'data', 'robadata.db')
        self.chatbot = ChatBot(
            'RobaBot',
            read_only=True,
            storage_adapter={
                'import_path': 'chatterbot.storage.SQLStorageAdapter',
                'database_uri': f'sqlite:///{db_path}'
            },
            logic_adapters=[
                {'import_path': 'chatterbot.logic.MathematicalEvaluation'},
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I am sorry, I do not understand.',
                    'maximum_similarity_threshold': 0.90
                }
            ]
        )
        print("RobaChatbot initialized.")

    def _filter_query(self, query):
        """
        Filters the query by removing stop words.
        Args:
            query (str): The user's query.
        Returns:
            str: The filtered query.
        """
        query_words = query.lower().split()
        filtered_words = [word for word in query_words if word not in self.stop_words]
        return " ".join(filtered_words)

    def _get_wikipedia_summary(self, query):
        """
        Gets a summary from Wikipedia for the given query.
        Args:
            query (str): The search query.
        Returns:
            str: The Wikipedia summary, or None if not found.
        """
        try:
            summary = wikipedia.summary(query, sentences=1)
            # Remove content in parentheses
            summary = "".join(summary.split('(')[::2])
            return summary.replace('"', '')
        except wikipedia.exceptions.PageError:
            print(f"Wikipedia page not found for query: {query}")
            return None
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation error for query: {query}. Options: {e.options}")
            # Try the first option
            return self._get_wikipedia_summary(e.options[0])
        except Exception as e:
            print(f"An error occurred while fetching from Wikipedia: {e}")
            return None

    def get_answer(self, query):
        """
        Gets an answer to the user's query.
        It first tries to get a response from the chatbot. If the confidence is low,
        it queries Wikipedia.
        Args:
            query (str): The user's query.
        Returns:
            str: The answer to the query.
        """
        original_query = query
        query_for_wikipedia = self._filter_query(original_query)

        try:
            response = self.chatbot.get_response(original_query)
            print(f"Query: '{original_query}', Response: '{response}', Confidence: {response.confidence}")

            if response.confidence > self.confidence_threshold and response.text != 'I am sorry, I do not understand.':
                return str(response).replace("*", " multiply ")
            else:
                wikipedia_summary = self._get_wikipedia_summary(query_for_wikipedia)
                if wikipedia_summary:
                    return wikipedia_summary
                else:
                    return "I am sorry, but I could not find an answer to your question."
        except Exception as e:
            print(f"An error occurred while getting answer: {e}")
            return "I encountered an error. Please try again."
