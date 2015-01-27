# -*- coding: utf-8 -*-

__author__ = 'hadware'
import os
import re
from dialog import Dialog, Cue


class DialogParser():
    """This class takes care of parsing a chuck of text to make it into a simple list of lines"""
    text = ""

    def __init__(self, webclient, **kwargs):
        """Constructor"""
        self.webclient = webclient
        if "filepath" in kwargs:
            self.load_text_file(kwargs["filepath"])

    def load_text_file(self, filepath):
        with open(os.path.abspath(filepath), mode = "r+") as text_file:
            self.text = unicode(text_file.read(), "utf-8")

    def parse_dialog(self):
        """Parses a dialog using the text class attribute"""
        lines = re.compile(r'[\n]+', re.UNICODE).split(self.text)

        self.dialog = Dialog()
        for line in lines:
            if line != "":
                splitted = line.split(":", 1)
                self.dialog.add_cue(Cue(voice_ref=self.webclient.get_voice_object_from_name(splitted[0]), line=splitted[1]))

    def parse_from_string(self, text):
        self.text = text
        self.parse_dialog()
        return self.dialog




