# -*- coding: utf-8 -*-

__author__ = 'hadware'
from pydub import AudioSegment
import hashlib
import os

class SoundManager():
    """Takes care of tracking sound files, and makes the final completed sound file"""

    def __init__(self, file_list = [] , tmp_folder = "/tmp/vox_populi"):
        """Constructor"""
        self.tmp_folder = tmp_folder
        self.file_list = file_list
        try:
            os.mkdir(self.get_cache_path())
        except OSError:
            pass

        try:
            os.mkdir(self.get_render_path())
        except OSError:
            pass

    def get_cache_path(self):
        """Returns the folder where the rendered lines are stored"""
        return self.tmp_folder + "/audio_fragments/"

    def get_render_path(self):
        """returns the foder where the rendered files are stored"""
        return self.tmp_folder + "/renders/"

    def render_dialog(self, file_list = None):
        """Uses a file list to render the dialog"""
        if not file_list is None:
            self.file_list = file_list

        #loading all mp3 files
        full_dialog = AudioSegment.empty()
        silence = AudioSegment.silent(100)
        for i, filename in enumerate(self.file_list):
            full_dialog += AudioSegment.from_mp3(filename) + silence

        print(self.file_list)

        rendered_file_name = self.get_render_path() + hashlib.md5("-".join(self.file_list)).hexdigest() + ".ogg"
        full_dialog.export(rendered_file_name, format="ogg", codec="libvorbis")
        return rendered_file_name


