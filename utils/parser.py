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

        #attempt to match a header containing voice assignments
        match_obj = re.compile(r'\[(.*?)\](.*)', re.UNICODE | re.DOTALL).match(self.text)

        self.dialog = Dialog()
        if match_obj is None:
            #match didn't work, there's no voice assignment header
            lines = re.compile(r'[\n]+', re.UNICODE).split(self.text)


            for line in lines:
                if line != "":
                    splitted = line.split(":", 1)
                    self.dialog.add_cue(Cue(voice_ref=self.webclient.get_voice_object_from_name(splitted[0]), line=splitted[1]))
        else:
            #match worked,  we have to parse the voice header which looks like this [ character1 : voicename1, ...]
            voice_defs = match_obj.groups()[0].split(",")
            character_dict = dict()
            for voice_def in voice_defs:
                character, voice = tuple([string.strip() for string in voice_defs.split(":")])
                character_dict[character.upper()] = self.webclient.get_voice_object_from_name(voice)

            #then parsing the dialog using both the defined characters and the regular voices
            #match didn't work, there's no voice assignment header
            lines = re.compile(r'[\n]+', re.UNICODE).split(match_obj.groups()[1])

            for line in lines:
                if line != "":
                    splitted = line.split(":", 1)
                    #checking if the voice is a "character" voice or a regular voice
                    if character_dict.has_key(splitted[0].strip().upper()):
                        voice_obj = character_dict[splitted[0].strip().upper()]
                    else:
                        voice_obj = self.webclient.get_voice_object_from_name(splitted[0])

                    self.dialog.add_cue(Cue(voice_ref=voice_obj, line=splitted[1]))


    def parse_from_string(self, text):
        self.text = text
        self.parse_dialog()
        return self.dialog




