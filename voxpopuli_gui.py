#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gui import *
from utils import RenderManager
from gi.repository import Gtk
import sys

class VoxPopuliMain(Gtk.Window):
    def __init__(self):
        super(VoxPopuliMain, self).__init__()

        self.set_title("VoxPopuli")
        self.connect("destroy", Gtk.main_quit)

        #initilizing the render manager
        self.render_manager = RenderManager()

        #setting up the layout
        self.set_up_layout()

        #once the progressbar has been created we're givin out its reference to the render manager to be able to display progress
        self.render_manager.set_progressbar(self.render_progressbar)

        #setting up the sound manager (depending on the slider layout)
        self.sound_player = SoundPlayer(self.render_manager.file_manager, self.sound_progress_scale)

        #setting up signal connections
        self.set_up_signals()

        self.show_all()
        self.voxpopuli_menu.menubar.show()

    def set_up_layout(self):

        ### the layout
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)
        self.grid = Gtk.Table(12, 6, True)
        self.grid.set_row_spacing(2, 10)
        self.box.pack_end(self.grid, False, False, 0)

        #rendering and adding the menu
        self.voxpopuli_menu = VoxPopuliMenu(self.render_manager.webclient.get_voices())
        self.box.pack_start(self.voxpopuli_menu.menubar, False, False, 0)

        ### layout elements
        #main text area
        self.textarea_scrollwindow = Gtk.ScrolledWindow()
        self.textarea_scrollwindow.set_vexpand(True)
        self.dialog_textarea = Gtk.TextView(editable = True, justification = Gtk.Justification.LEFT, wrap_mode = Gtk.WrapMode.WORD)
        self.dialog_textbuffer = self.dialog_textarea.get_buffer()
        #sound and render control buttons
        self.button_render = ImgButton("Rendu", Gtk.STOCK_CONVERT)
        self.button_play = ImgButton("Lecture", Gtk.STOCK_MEDIA_PLAY)
        self.button_pause = ImgButton("Pause", Gtk.STOCK_MEDIA_PAUSE)
        #render progress bar, and playback progress bar
        self.render_progressbar = Gtk.ProgressBar()
        self.sound_progress_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.0, 100.0, 0.5)
        self.sound_progress_scale.set_digits(2)
        self.sound_progress_scale.set_draw_value(False)

        ### adding the elements to the grid layout
        self.grid.attach(self.button_render, 1, 2, 0, 1)
        self.grid.attach(self.render_progressbar, 0, 3, 1, 2)
        self.grid.attach(self.button_play, 3, 4, 0, 1)
        self.grid.attach(self.button_pause, 4, 5, 0, 1)
        self.grid.attach(self.sound_progress_scale, 3, 6, 1, 2)
        self.grid.attach(self.textarea_scrollwindow, 0, 6, 2, 12)
        self.textarea_scrollwindow.add(self.dialog_textarea)

    def set_up_signals(self):
        #render button
        self.button_render.connect("clicked", self.do_render)

        #play/pause buttons, audio seek slider
        self.button_pause.connect("clicked", self.sound_player.pause)
        self.button_play.connect("clicked", self.sound_player.play)

        #menu actions
        self.voxpopuli_menu.action_quit.connect("activate", self.quit)
        self.voxpopuli_menu.action_open_file.connect("activate", self.open_text_file)
        self.voxpopuli_menu.action_new_file.connect("activate", self.render_manager.file_manager.new_file)
        self.voxpopuli_menu.action_save_text.connect("activate", self.save_text_file)
        self.voxpopuli_menu.action_save_render.connect("activate", self.save_render_file)
        self.voxpopuli_menu.action_render.connect("activate", self.do_render)

        #window destruction
        self.connect("destroy", self.quit)

    def do_render(self, widget):
        text_buffer = self.dialog_textarea.get_buffer()
        self.render_manager.render(unicode(text_buffer.get_text(text_buffer.get_start_iter(),
                                                        text_buffer.get_end_iter(),
                                                        False), "utf-8"))
        #reset the player to use the new file
        self.sound_player.reset_player()


    def open_text_file(self, widget):
        """Ask the user, via a dialog, to open a text file, update the text buffer with the text"""
        response = self.render_manager.file_manager.filedialog(self,
                                                               Gtk.FileChooserAction.OPEN,
                                                               self.render_manager.file_manager.FileType.TEXT)
        if response is not None:
             self.dialog_textbuffer.set_text(self.render_manager.file_manager.open_file(response))


    def save_text_file(self, widget):
        """Save the currently edited text dialog from the buffer"""
        response = self.render_manager.file_manager.filedialog(self,
                                                               Gtk.FileChooserAction.SAVE,
                                                               self.render_manager.file_manager.FileType.TEXT)


        if response is not None:
            text_buffer = self.dialog_textarea.get_buffer()
            text = text_buffer.get_text(text_buffer.get_start_iter(),
                                        text_buffer.get_end_iter(),
                                        False)

            self.render_manager.file_manager.save_file(text, response)


    def save_render_file(self, widget):
        response = self.render_manager.file_manager.filedialog(self,
                                                               Gtk.FileChooserAction.SAVE,
                                                               self.render_manager.file_manager.FileType.SOUND)
        if response is not None:
             self.render_manager.file_manager.save_render(response)

    def quit(self, widget):
        Gtk.main_quit()

    def load_file_on_start(self, filepath):
        self.dialog_textbuffer.set_text(self.render_manager.file_manager.open_file(filepath))

if __name__ == "__main__":
    main = VoxPopuliMain()
    if len(sys.argv) == 3:
        main.load_file_on_start(sys.argv[2])
    elif len(sys.argv) == 2:
        main.load_file_on_start(sys.argv[1])
    Gtk.main()