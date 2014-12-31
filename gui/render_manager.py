# -*- coding: utf-8 -*-

__author__ = 'hadware'

from utils import WebClient, DialogSoundRender, DialogParser
from utils.file_manager import VoxPopuliFileManager

class RenderManager():

    def __init__(self):
        self.webclient = WebClient()
        self.file_manager = VoxPopuliFileManager()
        # retrieving the available voice list and giving it to the parser constructor
        self.parser = DialogParser(voices = self.webclient.get_voices())

    def set_progressbar(self, progress_bar):
        self.progress_bar = progress_bar

    def render(self, current_text):
        self.progress_bar.set_fraction(0.0)

        # parsing the file into a "dialog" (list of voices and their lines)
        self.dialog = self.parser.parse_from_string(unicode(current_text, "utf-8"))
        self.progress_bar.set_fraction(0.1)

        #using the web client to retrieve the rendered sound files

        sound_files = []
        line_render_progress_increment = 0.8 / len(self.dialog)
        for line in self.dialog:
            print("line rendered!")
            self.progress_bar.set_fraction(self.progress_bar.get_fraction() + line_render_progress_increment)
            sound_files.append(self.webclient.get_rendered_audio(line["voice"], line["text"]))


        #making the sound manager render the final sound file
        sound_manager = DialogSoundRender(file_list=sound_files)
        rendered_file = sound_manager.render_dialog()
        self.progress_bar.set_fraction(1.0)

        #storing the file in the file manager
        self.file_manager.render_file_path = rendered_file