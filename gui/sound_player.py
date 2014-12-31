# -*- coding: utf-8 -*-

__author__ = 'hadware'

from gi.repository import Gst, GObject
import os


class SoundPlayer():
    """Takes care of playing the rendered dialog"""

    def __init__(self, file_manager, slider):
        self.file_manager = file_manager
        GObject.init_threads()
        Gst.init()
        self.is_playing = False
        self.slider = slider #reference to the GUI slider that manages

        self.playbin = Gst.ElementFactory.make("playbin", "player")


    def play(self):
        if self.playbin.get_property("uri") is None:
            self.playbin.set_property('uri', 'file://'+os.path.abspath(self.file_manager.render_file_path))

        self.playbin.set_state(Gst.State.PLAYING)
        self.is_playing = True

    def pause(self):
        self.playbin.set_state(Gst.State.PAUSED)
        self.is_playing = False

    def on_slider_seek(self, widget):
        pass

    def update_slider(self):
        pass