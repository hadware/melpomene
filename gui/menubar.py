# -*- coding: utf-8 -*-

from gi.repository import Gtk

__author__ = 'hadware'

UI_INFO = """
<ui>
    <menubar name='MenuBar'>
        <menu action='FileMenu'>
            <menuitem action='FileNewStandard' />
            <menuitem action='FileOpenText' />
            <separator />
            <menuitem action='FileSaveText' />
            <menuitem action='FileSaveRenderAs' />
            <separator />
            <menuitem action='FileQuit' />
        </menu>
        <menu action='EditMenu'>
            <menuitem action='EditRender' />
        </menu>
    </menubar>
</ui>
"""

class VoxPopuliMenu():

    def __init__(self, voice_list):
        """Uses the XML description to render a menubar"""

        #creating menu actions
        self.action_group = Gtk.ActionGroup("menu_actions")
        self.set_up_file_actions()
        self.set_up_edit_actions()

        #creating the UI manager
        self.ui_manager = Gtk.UIManager()
        self.ui_manager.add_ui_from_string(UI_INFO)
        self.ui_manager.insert_action_group(self.action_group)
        self.menubar = self.ui_manager.get_widget("/MenuBar")

    def set_up_file_actions(self):
        self.action_filemenu = Gtk.Action("FileMenu", "Fichier", None, None)
        self.action_new_file = Gtk.Action("FileNewStandard", "Nouveau", "Créer un nouveau dialogue", Gtk.STOCK_NEW)
        self.action_open_file = Gtk.Action("FileOpenText", "Ouvrir", "Ouvrir un fichier texte", Gtk.STOCK_OPEN)
        self.action_save_text = Gtk.Action("FileSaveText", "Sauver le dialogue", "Sauvegarder le fichier du dialogue", Gtk.STOCK_SAVE)
        self.action_save_render = Gtk.Action("FileSaveRenderAs", "Sauver le rendu", "Sauvegarder le fichier son du dialogue", None)
        self.action_quit= Gtk.Action("FileQuit", "Quitter", None, None)

        for action in [self.action_filemenu, self.action_new_file, self.action_open_file, self.action_save_text, self.action_save_render, self.action_quit]:
            self.action_group.add_action(action)

    def set_up_edit_actions(self):
        self.action_group.add_action(Gtk.Action("EditMenu", "Editer", None, None))
        self.action_render = Gtk.Action("EditRender", "Rendu", "Faire un rendu sonore du dialogue")

        self.action_group.add_action(self.action_render)


