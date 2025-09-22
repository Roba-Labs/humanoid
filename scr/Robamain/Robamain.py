import sys
import os
import threading
import time

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add the required directories to the python path
sys.path.insert(1, os.path.join(project_root, 'scr', 'Robamain'))
sys.path.insert(1, os.path.join(project_root, 'scr', 'Roba_conversion_ai'))
sys.path.insert(1, os.path.join(project_root, 'scr', 'Roba_vision'))
sys.path.insert(1, os.path.join(project_root, 'scr', 'firmware', 'servo'))

import ASR
import robaaibot
import Speak2rpi


class RobaConversationalAI:
    """
    A class to manage the conversational AI for the Roba robot.
    This class handles speech-to-text, chatbot interaction, and text-to-speech.
    """

    def __init__(self, tts_server_ip="192.168.0.120"):
        """
        Initializes the conversational AI components.
        Args:
            tts_server_ip (str): The IP address of the Text-to-Speech server.
        """
        self.roba_ai_chatbot = robaaibot.RobaChatbot()
        time.sleep(0.2)
        self.speaker = Speak2rpi.TextToSpeechClient(tts_server_ip)
        self.speaker.received_data = "Paused"
        time.sleep(0.2)
        self.is_running = True
        self.asr_service = None

    def run(self):
        """
        The main loop for the conversational AI.
        It continuously listens for user input, processes it, and generates a spoken response.
        """
        self.asr_service = ASR.SpeechToText()
        self.answer_text = ""
        while self.is_running:
            text_query = ""
            time.sleep(0.2)

            if self.speaker.received_data == "Paused":
                text_query = self.asr_service.get_recognized_text()

                if not text_query or text_query.isspace():
                    self.asr_service.clear_recognized_text()
                    self.asr_service.is_listening = True
                    continue

                if len(text_query) > 1 and text_query != "['']":
                    self.asr_service.clear_recognized_text()
                    print(f"User query: {text_query}")
                    self.answer_text = self.roba_ai_chatbot.get_answer(text_query)
                    self.answer_text = str(self.answer_text)

                    if len(self.answer_text) > 1 and self.answer_text != "['']":
                        self.speaker.speak_text(self.answer_text)
                        start_time = time.time()

                        # Wait for the speaking to start
                        while self.speaker.received_data != "Playing":
                            time.sleep(0.1)
                            if time.time() - start_time > 5:
                                print("Error: Speaker did not start playing.")
                                break

                        start_time = time.time()
                        # Wait for the speaking to finish
                        while self.speaker.received_data != "Paused":
                            self.asr_service.is_listening = False
                            time.sleep(0.1)
                            if time.time() - start_time > 50:
                                print("Error: Speaker timed out.")
                                break

                        self.asr_service.is_listening = True
                        time.sleep(1.5)
                        self.asr_service.clear_recognized_text()
                else:
                    self.asr_service.is_listening = True
                    self.asr_service.clear_recognized_text()

        print("Exiting Conversational AI loop.")


def main():
    """
    The main function to start the Roba Conversational AI.
    """
    roba_conversation_ai = RobaConversationalAI()
    time.sleep(0.2)
    roba_conversation_ai.speaker.received_data = "Paused"
    cai_thread = threading.Thread(target=roba_conversation_ai.run, daemon=True)
    cai_thread.start()
    print("Roba Conversational AI started.")


if __name__ == "__main__":
    main()