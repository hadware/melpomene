__author__ = 'hadware'
from pydub import AudioSegment
import hashlib

class SoundManager():
    """Takes care of tracking sound files, and makes the final completed sound file"""

    def __init__(self, file_list = [] , tmp_folder = "/tmp/vox_populi"):
        """Constructor"""
        self.tmp_folder = tmp_folder
        self.file_list = file_list


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
        full_dialog = AudioSegment.from_mp3(file_list[0])
        silence = AudioSegment.silent(100)
        for i, filename in enumerate(file_list):
            if i !=0:
                full_dialog += AudioSegment.from_mp3(filename) + silence

        rendered_file_name = self.get_render_path() + hashlib.md5("-".join(file_list)) + ".mp3"
        full_dialog.export(rendered_file_name, format="mp3")
        return rendered_file_name

