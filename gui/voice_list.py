# -*- coding: utf-8 -*-
from utils.locales import Language

__author__ = 'hadware'
from gi.repository import Gtk
from utils import Language, Cue
from sound_player import VoiceTestSoundPlayer

class VoiceList(Gtk.Grid):

    def __init__(self, webclient):
        super(VoiceList, self).__init__()
        self.set_column_homogeneous(True)
        self.webclient = webclient
        self.current_lang = Language.FR #current language displayed in the render box
        self.test_sound_player = VoiceTestSoundPlayer() #test sound player

        #creating the storage
        #name + client, language code, real_name
        self.voice_store = Gtk.ListStore(str, int, str)
        languages_list = []
        #language name, language code
        language_store = Gtk.ListStore(str, int)
        voices_list = self.webclient.get_voices_grouped_by_language()
        for language_index in voices_list:
            for voice in voices_list[language_index]["voices"]:
                self.voice_store.append([voice.name + " (%s)" % voice.webclient.client_name, voice.language, voice.name])
                if not voice.language in languages_list:
                    languages_list.append(voice.language)
                    language_store.append([Language.get_language_name(voice.language), voice.language])

        #setting up the language filter for the treeview
        self.language_filter = self.voice_store.filter_new()
        self.language_filter.set_visible_func(self.language_filter_func)

        #setting up the treeview and its column
        self.voice_treelist = Gtk.TreeView(self.language_filter)
        cell_renderer = Gtk.CellRendererText()
        name_column = Gtk.TreeViewColumn("Voix Disponibles", cell_renderer, text=0)
        self.voice_treelist.append_column(name_column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)

        #setting up the combo box
        self.languages_combo = Gtk.ComboBox.new_with_model(language_store)
        self.languages_combo.connect("changed", self.on_language_combo_changed)
        combo_renderer = Gtk.CellRendererText()
        self.languages_combo.pack_start(combo_renderer, True)
        self.languages_combo.add_attribute(combo_renderer, "text", 0)


        #setting up the text area and the button
        self.play_button = Gtk.Button()
        button_image = Gtk.Image()
        button_image.set_from_stock(Gtk.STOCK_OK, Gtk.IconSize.BUTTON)
        self.play_button.set_image(button_image)
        self.play_button.connect("clicked", self.test_current_voice)
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
        return model[iter][1] == self.current_lang

    def on_language_combo_changed(self, combo):
        """Updates the tree list when the language combo is changed"""
        iter = combo.get_active_iter()
        if iter != None:
            model = combo.get_model()
            self.current_lang = model[iter][1]
            self.language_filter.refilter()

    def test_current_voice(self, widget):
        """Called when the user clicks on the test button. The current text in the textbox is rendered and played"""
        #get the current selected value
        model, iter = self.voice_treelist.get_selection().get_selected()
        if iter is not None:
            selected_voice = self.webclient.get_voice_object_from_name(model[iter][2])
            test_cue = Cue(selected_voice, unicode(self.test_textarea.get_text(),"utf-8"))
            rendered_test_filepath = test_cue.get_rendered_audio(self.webclient.get_cache_path())
            self.test_sound_player.play_file(rendered_test_filepath)
