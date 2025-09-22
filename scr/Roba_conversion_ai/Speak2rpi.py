import socket
import threading
import time
import re

class TextToSpeechClient:
    """
    This class provides a client to a Text-to-Speech (TTS) server running on a Raspberry Pi.
    It sends text to the server to be spoken and can also send commands to play songs.
    """

    def __init__(self, host='192.168.0.120', port=13500):
        """
        Initializes the TextToSpeechClient.
        Args:
            host (str): The IP address of the TTS server.
            port (int): The port of the TTS server.
        """
        self.is_running = True
        self.received_data = "Paused"
        self.host = host
        self.port = port
        self.socket_client = None
        self.reconnect()

        self.receive_thread = threading.Thread(target=self._receive_data_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        print("TTS client thread started.")

    def _receive_data_thread(self):
        """
        Listens for data from the TTS server in a separate thread.
        Updates the status of the client (e.g., 'Playing', 'Paused').
        """
        while self.is_running:
            try:
                time.sleep(0.01)
                data = self.socket_client.recv(1024)
                if not data:
                    continue

                # The server sends back status messages that need to be parsed.
                decoded_data = re.split(' |\'|\b', str(data))
                if len(decoded_data) > 1 and decoded_data[1] in ['Playing', 'Paused']:
                    self.received_data = decoded_data[1]
            except socket.error as e:
                print(f"Socket error in receive thread: {e}")
                self.reconnect()
            except Exception as e:
                print(f"An unexpected error occurred in receive thread: {e}")

    def reconnect(self):
        """Handles reconnection to the TTS server."""
        if self.socket_client:
            self.socket_client.close()
        while self.is_running:
            try:
                self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_client.connect((self.host, self.port))
                print("Successfully reconnected to TTS server.")
                break
            except socket.error as e:
                print(f"Failed to reconnect to TTS server: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def _send_command(self, command_type, text):
        """
        Sends a command to the TTS server.
        Args:
            command_type (str): The type of command ('song' or 'ttsc').
            text (str): The text or song name to send.
        """
        try:
            command = f"{{'cmd':'{command_type}','ln':{len(text)}}}"
            self.socket_client.sendall(str.encode(command))
            time.sleep(0.1)
            self.socket_client.sendall(str.encode(text))
        except socket.error as e:
            print(f"Socket error while sending command: {e}")
            self.reconnect()
            # Retry sending the command after reconnecting
            self._send_command(command_type, text)

    def play_song(self, song_name):
        """
        Sends a command to play a song.
        Args:
            song_name (str): The name of the song.
        """
        self._send_command('song', song_name)

    def speak_text(self, text):
        """
        Sends text to be spoken by the TTS server.
        Args:
            text (str): The text to speak.
        """
        self._send_command('ttsc', text)

    def get_host_ip(self):
        """Returns the host IP address."""
        return self.host

    def stop(self):
        """Stops the client and closes the socket connection."""
        self.is_running = False
        if self.socket_client:
            self.socket_client.close()
        self.receive_thread.join()
        print("TTS client stopped.")
 