__author__ = 'hadware'
import os
import re

class VoiceNotFound(Exception):
    pass

class DialogParser():
    """This class takes care of parsing a chuck of text to make it into a simple list of lines"""
    text = ""
    #a dialog is a list of dicts with {"voice" : voice name, "line": what the voice says }
    dialog = []
    voices = []

    def __init__(self, **kwargs):
        """Constructor"""

        self.voices = kwargs["voices"]
        if "text" in kwargs:
            self.text = kwargs["text"]
        elif "filepath" in kwargs:
            self.load_text_file(kwargs["filepath"])

    def load_text_file(self, filepath):
        with open(os.path.abspath(filepath), "r+") as text_file:
            self.text = text_file.read()

    def check_voice(self, input_voice):
        """Checks if the input voice string is a valid voice, if voice is not found, it raises an error"""
        for voice in self.voices:
            if voice.lower() == input_voice.lower():
                return voice

        raise VoiceNotFound("The voice %s isn't a valid one" % input_voice)

    def parse_dialog(self):
        """Parses a dialog using the text class attribute"""
        lines = re.split(r'[\n]+', self.text)
        self.dialog = []
        for line in lines:
            splitted = line.split(":", 1)
            self.dialog.append({"voice" : self.check_voice(splitted[0].strip()),
                                "text" : splitted[1]})

    def parse_from_string(self, text):
        self.text = text
        self.parse_dialog()
        return self.dialog

    def parse_from_file(self, filepath):
        """Parses a dialog from a file"""
        self.load_text_file(filepath)
        self.parse_dialog()
        return self.dialog



