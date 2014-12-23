#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gui import *
from gi.repository import Gtk


class VoxPopuliMain(Gtk.Window):
    def __init__(self):
        super(VoxPopuliMain, self).__init__()

        self.set_title("VoxPopuli")
        self.connect("destroy", Gtk.main_quit)

        ### the layout
        self.grid = Gtk.Table(12, 6, True)
        self.grid.set_row_spacing(2, 10k)
        self.add(self.grid)

        ### layout elements
        #main text area
        self.dialog_textarea = Gtk.TextView()
        self.dialog_textarea.set_editable(True)
        self.dialog_textarea.set_justification(Gtk.Justification.LEFT)
        self.dialog_textarea.set_wrap_mode(Gtk.WrapMode.WORD)
        #sound and render control buttons
        self.button_render = ImgButton("Rendu", Gtk.STOCK_CONVERT)
        self.button_play = ImgButton("Lecture", Gtk.STOCK_MEDIA_PLAY)
        self.button_pause = ImgButton("Pause", Gtk.STOCK_MEDIA_PAUSE)
        #render progress bar, and playback progress bar
        self.render_progress = Gtk.ProgressBar()
        self.render_progress.set_fraction(0.33)
        self.sound_progress_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.0, 100.0, 0.5)
        self.sound_progress_scale.set_digits(2)
        self.sound_progress_scale.set_draw_value(False)

        ### adding the elements to the grid layout
        self.grid.attach(self.button_render, 1, 2, 0, 1)
        self.grid.attach(self.render_progress, 0, 3, 1, 2)
        self.grid.attach(self.button_play, 3, 4, 0, 1)
        self.grid.attach(self.button_pause, 4, 5, 0, 1)
        self.grid.attach(self.sound_progress_scale, 3, 6, 1, 2)
        self.grid.attach(self.dialog_textarea, 0, 6, 2, 12)

        #self.quit.connect("clicked", self.on_clicked)


        self.show_all()

    def emit_signal(self):

        event = Gtk.gdk.Event(Gtk.gdk.BUTTON_RELEASE)
        event.button = 1
        event.window = self.quit.window
        event.send_event = True

        self.quit.emit("button-release-event", event)


    def on_clicked(self, widget, data = None):
        print "clicked"

if __name__ == "__main__":
    VoxPopuliMain()
    Gtk.main()