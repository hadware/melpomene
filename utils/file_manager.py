# -*- coding: utf-8 -*-

__author__ = 'hadware'

from gi.repository import Gtk
import shutil
import os

class VoxPopuliFileManager():
    """Stores the current sound render and the current dialog"""
    dialog_file_path = None
    render_file_path = None

    class FileType():
        SOUND, TEXT = range(2)

    def new_file(self):
        self.dialog_file_path = None
        self.render_file_path = None

    def open_file(self, filepath):
        """Opens the filepath, returns the text it contains"""
        with open(os.path.abspath(filepath), mode = "r+") as text_file:
            text = unicode(text_file.read(), "utf-8")
            self.dialog_file_path = filepath

        return text
    def save_file(self, text, filepath = None):
        with open(os.path.abspath(filepath), mode = "wb") as text_file:
            text_file.write(text)
            self.dialog_file_path = filepath

    def save_render(self, filepath = None):
        #copying the rendered file to the specified filepath
        shutil.copyfile(self.render_file_path, filepath)

    def save_render_in_folder(self, folder):
        #copying the rendered file to the specified folder, using the current basename
        shutil.copyfile(self.render_file_path, folder + os.path.basename(self.render_file_path))

    def add_filter(self, dialog, mime_type, name):
        """Adds a filter to dialog"""
        filter = Gtk.FileFilter()
        filter.set_name(name)
        if mime_type == "*":
            filter.add_pattern("*")
        else:
            filter.add_mime_type(mime_type)
        dialog.add_filter(filter)

    def add_text_file_filters(self, dialog):
        self.add_filter(dialog, "text/plain", "Text Files")
        self.add_filter(dialog, "*", "Any Files")

    def add_sound_file_filters(self, dialog):
        self.add_filter(dialog, "application/ogg", "Sound Files")
        self.add_filter(dialog, "*", "Any Files")


    def filedialog(self, window, dialog_type, file_type):
        """Opens a file dialog, returns the dialog's result, or none"""

        dialog = Gtk.FileChooserDialog("Choisissez un fichier", window,
                                       dialog_type,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        #adding file filters to the dialog
        if file_type == self.FileType.TEXT:
            self.add_text_file_filters(dialog)
        elif file_type == self.FileType.SOUND:
            self.add_sound_file_filters(dialog)

        #runnign the dialog, and retrieving the response
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy()
            return filename
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return None
