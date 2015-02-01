# -*- coding: utf-8 -*-
from gi.repository import Gtk

__author__ = 'hadware'

class AboutDialog(Gtk.Dialog):

    about_text = """Voxpopuli utilise les excellents démonstrateur web de <a href=\"http://voxygen.fr\">Voxygen SAS</a> et <a href=\"http://www.acapela-group.com/\">Acapela Group</a>.
                 Ce logiciel est indépendant des services précédemment mentionnés.
                 Les fichiers sonores créés par ces services peuvent être soumis à des droits d'auteurs.

                 Développé par <a href=\"https://github.com/hadware\">hadware</a>. Github du projet :
                 <a href=\"https://github.com/hadware\">https://github.com/hadware/voxpopuli</a>.
                 """

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "A propos", parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label()
        label.set_markup(self.about_text)

        box = self.get_content_area()
        box.add(label)
        self.show_all()
