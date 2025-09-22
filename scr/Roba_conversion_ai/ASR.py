import threading
import time
import speech_recognition as sr
from IPython.display import clear_output
import soundcard as sc


class SpeechToText:
    """
    This class handles Automatic Speech Recognition (ASR) using the speech_recognition library.
    It listens for audio from a microphone and converts it to text in a separate thread.
    """

    def __init__(self, sample_rate=48000, energy_threshold=500, timeout=4, phrase_time_limit=5):
        """
        Initializes the SpeechToText listener.
        Args:
            sample_rate (int): The sample rate for the microphone.
            energy_threshold (int): The energy level threshold for considering speech.
            timeout (int): The maximum number of seconds to wait for a phrase to start.
            phrase_time_limit (int): The maximum number of seconds a phrase can be.
        """
        self.microphone_index = self._find_microphone()
        self.is_listening = True
        self.recognized_text = "&"
        self.is_running = True
        
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        
        self.sample_rate = sample_rate
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit

        self.asr_thread = threading.Thread(target=self._run_asr_listener, daemon=True)
        self.asr_thread.start()

    def _find_microphone(self):
        """
        Finds the index of the preferred microphone.
        It looks for a USB audio device first, then falls back to the default.
        Returns:
            int: The index of the selected microphone.
        """
        microphone_names = sr.Microphone.list_microphone_names()
        print("Available microphones:", microphone_names)

        # Try to find a USB microphone
        for i, name in enumerate(microphone_names):
            if "USB Audio Device" in name:
                print(f"Found USB microphone: {name}")
                return i
        
        # Fallback to default microphone
        print("USB microphone not found, falling back to default.")
        return 0

    def get_recognized_text(self):
        """Returns the last recognized text."""
        return self.recognized_text

    def clear_recognized_text(self):
        """Clears the last recognized text."""
        self.recognized_text = "&"

    def _run_asr_listener(self):
        """
        The main loop for the ASR listener.
        This runs in a separate thread and continuously listens for speech.
        """
        print(f"Starting ASR listener on microphone index: {self.microphone_index}")
        mic = sr.Microphone(device_index=self.microphone_index, sample_rate=self.sample_rate)

        while self.is_running:
            if self.is_listening:
                with mic as source:
                    try:
                        audio = self.recognizer.listen(source, timeout=self.timeout, phrase_time_limit=self.phrase_time_limit)
                        recognized_data = self.recognizer.recognize_google(audio)

                        if recognized_data and recognized_data.strip():
                            self.recognized_text = recognized_data
                            self.is_listening = False # Stop listening after getting a result
                            print(f"Recognized text: {self.recognized_text}")

                    except sr.WaitTimeoutError:
                        # This is expected if no speech is detected.
                        pass
                    except sr.UnknownValueError:
                        # This is expected if the speech is unintelligible.
                        pass
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred in ASR listener: {e}")
            else:
                # Sleep when not actively listening to reduce CPU usage.
                time.sleep(0.1)

        print("Exiting ASR listener thread.")

    def stop(self):
        """Stops the ASR listener thread."""
        self.is_running = False
        self.asr_thread.join()
        print("ASR listener stopped.")