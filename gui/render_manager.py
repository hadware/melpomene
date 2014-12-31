# -*- coding: utf-8 -*-

__author__ = 'hadware'

from utils import WebClient, DialogSoundRender, DialogParser
from utils.file_manager import VoxPopuliFileManager

class RenderManager():

    def __init__(self):
        self.webclient = WebClient()
        self.file_manager = VoxPopuliFileManager()

    def render(self, current_text):

        # retrieving the available voice list and giving it to the parser constructor
        self.parser = DialogParser(voices = self.webclient.get_voices())

        # parsing the file into a "dialog" (list of voices and their lines)
        self.dialog = self.parser.parse_from_string(current_text)

        #using the web client to retrieve the rendered sound files
        sound_files = [self.webclient.get_rendered_audio(line["voice"], line["text"]) for line in self.dialog]

        #making the sound manager render the final sound file
        sound_manager = DialogSoundRender(file_list=sound_files)
        rendered_file = sound_manager.render_dialog()

        #storing the file in the file manager
        self.file_manager.dialog_file_path = rendered_file
