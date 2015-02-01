# -*- coding: utf-8 -*-
__author__ = 'hadware'
from gi.repository import Gtk
from utils import Language

class VoiceList(Gtk.Box):

    def __init__(self, webclient):
        super(VoiceList, self).__init__(orientation=Gtk.Orientation.VERTICAL)
        self.webclient = webclient
        self.current_lang = Language.get_language_name(Language.FR)

        #creating the storage
        #name, language
        self.voice_store = Gtk.ListStore(str, str)
        voices_list = self.webclient.get_voices_grouped_by_language()
        for language_index in voices_list:
            for voice in voices_list[language_index]["voices"]:
                self.voice_store.append([voice.name + " (%s)" % voice.webclient.name, Language.get_language_name(voice.language)])

        #setting up the language filter for the treeview
        self.language_filter = self.voice_store.filter_new()
        self.anguage_filter.set_visible_func(self.language_filter, self.current_lang)

        #setting up the treeview and its column
        self.voice_treelist = Gtk.TreeView(self.language_filter)
        cell_renderer = Gtk.CellRendererText()
        name_column = Gtk.TreeViewColumn("Nom", cell_renderer, text=0)
        self.voice_treelist.append_column(name_column)

        #setting up the combo box
        self.languages_combo = Gtk.ComboBox.new_with_model(self.voice_store)
        self.languages_combo.connect("changed", self.on_language_combo_changed)
        self.languages_combo.set_entry_text_column(1)

        #packing those 2 in the box
        self.pack_start(self.languages_combo, False, False, 0)
        self.pack_start(self.voice_treelist, True, True, 0)

        self.show_all()

    def language_filter(self, model, iter, data):
        """Tests if the language specified is the right one"""
        return model[iter][1] == data

    def on_language_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            self.current_lang = model[tree_iter][1]
            self.language_filter.refilter()