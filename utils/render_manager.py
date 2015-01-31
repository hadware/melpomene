# -*- coding: utf-8 -*-

__author__ = 'hadware'

from utils import WebClient, DialogSoundRender, DialogParser
from utils.file_manager import VoxPopuliFileManager

class RenderManager():

    def __init__(self):
        self.cache_path = "/tmp/vox_populi/"
        self.webclient = WebClient()
        self.file_manager = VoxPopuliFileManager()
        # retrieving the available voice list and giving it to the parser constructor
        self.parser = DialogParser(webclient = self.webclient)
        self.progress_bar = None

    def set_progressbar(self, progress_bar):
        self.progress_bar = progress_bar

    def increment_progressbar(self, increment):
        """Increments the render's progress bar's value, if there's one"""
        if self.progress_bar is not None:
            self.progress_bar.set_fraction(self.progress_bar.get_fraction() + increment)

    def set_progressbar_value(self, value):
        """Sets the renderer's progress bar's value, if there's one"""
        if self.progress_bar is not None:
            self.progress_bar.set_fraction(value)

    def render(self, current_text):
        self.set_progressbar_value(0.0)

        # parsing the file into a "dialog" (object reprenseting a list of voices and their lines)
        self.dialog = self.parser.parse_from_string(current_text)
        self.set_progressbar_value(0.1)

        #using the web client to retrieve the rendered sound files

        sound_files = []
        line_render_progress_increment = 0.8 / len(self.dialog.cues)
        for cue in self.dialog.cues:
            sound_files.append(cue.get_rendered_audio(self.cache_path + "/audio_fragments/"))
            self.increment_progressbar(line_render_progress_increment)

        #making the sound manager render the final sound file
        sound_manager = DialogSoundRender(file_list=sound_files)
        rendered_file = sound_manager.render_dialog()
        self.set_progressbar_value(1.0)

        #storing the file in the file manager
        self.file_manager.render_file_path = rendered_file