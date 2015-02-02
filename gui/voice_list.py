# -*- coding: utf-8 -*-
from utils.locales import Language

__author__ = 'hadware'
from gi.repository import Gtk
from utils import Language
from sound_player import VoiceTestSoundPlayer

class VoiceList(Gtk.Grid):

    def __init__(self, webclient):
        super(VoiceList, self).__init__()
        self.set_column_homogeneous(True)
        self.webclient = webclient
        self.current_lang = Language.get_language_name(Language.FR) #current language displayed in the render box
        self.test_sound_player = VoiceTestSoundPlayer() #test sound player

        #creating the storage
        #name, language
        self.voice_store = Gtk.ListStore(str, str)
        languages_list = []
        voices_list = self.webclient.get_voices_grouped_by_language()
        for language_index in voices_list:
            for voice in voices_list[language_index]["voices"]:
                self.voice_store.append([voice.name + " (%s)" % voice.webclient.name, Language.get_language_name(voice.language)])
                if not voice.language in languages_list:
                    languages_list.append(voice.language)

        #setting up the language filter for the treeview
        self.language_filter = self.voice_store.filter_new()
        self.language_filter.set_visible_func(self.language_filter_func, self.current_lang)

        #setting up the treeview and its column
        self.voice_treelist = Gtk.TreeView(self.language_filter)
        cell_renderer = Gtk.CellRendererText()
        name_column = Gtk.TreeViewColumn("Nom", cell_renderer, text=0)
        self.voice_treelist.append_column(name_column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)

        #setting up the combo box
        self.languages_combo = Gtk.ComboBoxText()
        self.languages_combo.connect("changed", self.on_language_combo_changed)
        self.languages_combo.set_entry_text_column(0)
        for language in languages_list:
            self.languages_combo.append_text(Language.get_language_name(language))

        #setting up the text area and the button
        self.play_button = Gtk.Button()
        button_image = Gtk.Image()
        button_image.set_from_stock(Gtk.STOCK_OK, Gtk.IconSize.BUTTON)
        self.play_button.set_image(button_image)
        self.test_textarea = Gtk.Entry()
        self.test_textarea.set_text("Essayez une voix ici")

        #packing those 4 elements in the grid
        self.attach(self.play_button, 0, 0, 1, 1)
        self.attach_next_to(self.test_textarea, self.play_button, Gtk.PositionType.RIGHT, 4, 1)
        self.attach_next_to(self.languages_combo, self.play_button, Gtk.PositionType.BOTTOM, 5, 1)
        self.attach_next_to(self.scrollable_treelist, self.languages_combo, Gtk.PositionType.BOTTOM, 5, 2)
        self.scrollable_treelist.add(self.voice_treelist)

        self.show_all()

    def language_filter_func(self, model, iter, data):
        """Tests if the language specified is the right one"""
        return model[iter][1] == data

    def on_language_combo_changed(self, combo):
        """Updates the tree list when the language combo is changed"""
        text = combo.get_active_text()
        if tree_iter != None:
            self.current_lang = text
            self.language_filter.refilter()