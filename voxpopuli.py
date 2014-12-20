__author__ = 'hadware'
from sound_manager import SoundManager
from parser import DialogParser, VoiceNotFound
from webclient import WebClient
from sys import argv

"""This is the main module"""

if __name__ == "main":
    client = WebClient()
    parser = DialogParser(voice = WebClient.get_voices())
    parser.parse_from_file()

