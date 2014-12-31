# -*- coding: utf-8 -*-

__author__ = 'hadware'

from gi.repository import Gst, GObject, GLib
import os

class SoundPlayerError(Exception):
    pass

class SoundPlayer():
    """Takes care of playing the rendered dialog"""

    def __init__(self, file_manager, slider):
        self.file_manager = file_manager
        GObject.threads_init()
        Gst.init()
        self.is_playing = False
        self.duration_updated = False
        self.slider = slider #reference to the GUI slider that manages
        self.slider_handler_id = self.slider.connect("value-changed", self.on_slider_seek)

        self.playbin = Gst.ElementFactory.make("playbin", "player")

    def reset_current_file(self):
        self.playbin.set_property('uri', 'file://'+os.path.abspath(self.file_manager.render_file_path))

    def reset_player(self):
        self.pause() #pausing everything, in case
        self.playbin.set_state(Gst.State.READY)
        self.reset_current_file()
        self.duration_updated = False
        self.slider.set_value(0.0)


    def play(self):
        #checking if a render has been made
        if self.playbin.get_property("uri") is not None:
            self.playbin.set_state(Gst.State.PLAYING)
            self.is_playing = True

            #starting up a timer to check on the current playback value
            GLib.timeout_add(1000, self.update_slider)

    def pause(self):
        self.playbin.set_state(Gst.State.PAUSED)
        self.is_playing = False

    def on_slider_seek(self, widget):
        if self.playbin.get_property("uri") is not None:
            seek_time_secs = self.slider.get_value()
            self.playbin.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, seek_time_secs * Gst.SECOND)

    def update_slider(self):
        if not self.is_playing:
            return False # cancel timeout

        else:
            #updating the duration only if needed
            if not self.duration_updated:
                success, self.duration = self.playbin.query_duration(Gst.Format.TIME)
                if not success:
                    raise SoundPlayerError("Couldn't fetch song duration")
                else:
                    self.slider.set_range(0, self.duration / Gst.SECOND)
                    self.duration_updated = True

            #fetching the position, in nanosecs
            success, position = self.playbin.query_position(Gst.Format.TIME)
            if not success:
                raise SoundPlayerError("Couldn't fetch current song position to update slider")

            # block seek handler so we don't seek when we set_value()
            self.slider.handler_block(self.slider_handler_id)

            self.slider.set_value(float(position) / Gst.SECOND)

            self.slider.handler_unblock(self.slider_handler_id)

        return True # continue calling every x milliseconds