#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

from gui import *


class VoxPopuliMain(gtk.Window):
    def __init__(self):
        super(VoxPopuliMain, self).__init__()

        self.set_title("VoxPopuli")
        self.set_size_request(500, 500)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)

        ### the bottom layout
        self.main_box = gtk.VBox(homogeneous = False, spacing = 2)
        self.controls_box = gtk.HBox(homogeneous = True,spacing =  2)
        self.main_box.pack_start(self.controls_box, False, False, 1)
        self.render_control_resize = gtk.Alignment()
        self.render_control_resize.set(xalign = 0.5, xscale = 0.3, yalign = 0, yscale = 1.0)
        self.controls_box.left_box = gtk.VBox(homogeneous = False, spacing = 1)
        self.controls_box.left_box.pack_start(self.render_control_resize, False, False,0)
        self.controls_box.right_box = gtk.VBox(homogeneous = False, spacing = 1)
        self.controls_box.pack_start(self.controls_box.left_box, False, True, 0)
        self.controls_box.pack_end(self.controls_box.right_box, False, True, 0)
        self.controls_box.right_box.top_box = gtk.HBox(homogeneous = False, spacing = 1)
        self.controls_box.right_box.pack_start(self.controls_box.right_box.top_box, False, True, 0)

        ### layout elements
        #main text area
        self.dialog_textarea = gtk.TextView()
        self.dialog_textarea.set_editable(True)
        self.dialog_textarea.set_justification(gtk.JUSTIFY_LEFT)
        self.dialog_textarea.set_wrap_mode(gtk.WRAP_WORD)
        #sound and render control buttons
        self.button_render = ImgButton("Rendu", gtk.STOCK_CONVERT)
        self.button_play = ImgButton("Lecture", gtk.STOCK_MEDIA_PLAY)
        self.button_pause = ImgButton("Pause", gtk.STOCK_MEDIA_PAUSE)
        #render progress bar, and playback progress bar
        self.render_progress = gtk.ProgressBar()
        self.sound_run_scale = gtk.HScale()
        self.sound_run_scale.set_digits(3)
        self.sound_run_scale.set_draw_value(gtk.FALSE)

        ### adding the elements to the layout
        self.main_box.pack_end(self.dialog_textarea, True, True, 5)
        self.controls_box.left_box.pack_start(self.render_control_resize, False, False, 1)
        self.render_control_resize.add(self.button_render)
        self.controls_box.left_box.pack_start(self.render_progress, False, False, 1)
        self.controls_box.right_box.top_box.pack_start(self.button_play, False, True, 1)
        self.controls_box.right_box.top_box.pack_start(self.button_pause, False, True, 1)
        self.controls_box.right_box.pack_end(self.sound_run_scale, False, True, 3)

        #self.quit.connect("clicked", self.on_clicked)

        self.add(self.main_box)
        self.show_all()
        self.controls_box.show_all()
        self.controls_box.right_box.show_all()

    def emit_signal(self):

        event = gtk.gdk.Event(gtk.gdk.BUTTON_RELEASE)
        event.button = 1
        event.window = self.quit.window
        event.send_event = True

        self.quit.emit("button-release-event", event)


    def on_clicked(self, widget, data = None):
        print "clicked"

if __name__ == "__main__":
    VoxPopuliMain()
    gtk.main()