# -*- coding: utf-8 -*-
from os.path import join

__author__ = 'hadware'

import hashlib
from utils import WebClient, DialogSoundRender, DialogParser
from utils.file_manager import VoxPopuliFileManager
from gi.repository import GLib, GObject
from os import makedirs
import threading


CACHE_PATH = "/tmp/vox_populi/"

class RenderManager():

    def __init__(self):
        GObject.threads_init()

        self.cache_path = CACHE_PATH
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
        return False

    def set_progressbar_value(self, value):
        """Sets the renderer's progress bar's value, if there's one"""
        if self.progress_bar is not None:
            self.progress_bar.set_fraction(value)

    def render(self, current_text, to_zip = False):

        def render_cues(dialog_cues, cache_path, sound_files, progress_update_callback = None):
            line_render_progress_increment = 0.8 / len(dialog_cues)
            for i, cue in enumerate(dialog_cues):
                sound_files.append(cue.get_rendered_audio(cache_path))
                if progress_update_callback is not None:
                    GLib.idle_add(progress_update_callback, line_render_progress_increment)

        self.set_progressbar_value(0.0)

        # parsing the file into a "dialog" (object representing a list of voices and their lines)
        self.dialog = self.parser.parse_from_string(current_text)
        self.set_progressbar_value(0.1)

        #using the web client to retrieve the rendered sound files
        sound_files = []
        thread = threading.Thread(target=render_cues,
                                  args=(self.dialog.cues,
                                        self.cache_path + "audio_fragments/",
                                        sound_files,
                                        self.increment_progressbar))
        thread.daemon = True
        thread.start()
        thread.join()

        #making the sound manager render the final sound file
        sound_manager = DialogSoundRender(file_list=sound_files)
        rendered_file = sound_manager.render_dialog()
        self.set_progressbar_value(1.0)

        #storing the file in the file manager
        self.file_manager.render_file_path = rendered_file

        # if the to_zip flag is raised, we ask the filemanager to create a zipfile
        if to_zip:
            zipfile_filename = hashlib.md5(("".join(sound_files)).encode('utf8')).hexdigest()
            zipfile_folder_path = join(self.cache_path, zipfile_filename)
            try:
                makedirs(join(self.cache_path, zipfile_filename))
            except OSError:
                pass

            # TODO: copy the file to the zip folder, rename them
            # TODO : check if the soundfile list is the absolute files

