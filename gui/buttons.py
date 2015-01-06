__author__ = 'hadware'
from gi.repository import Gtk

class ImgButton(Gtk.Button):
    """A simple button with an icon instead of a simple label"""

    def __init__(self, label=None, icon = None):
        if icon is None:
            super(ImgButton, self).__init__(label)
        else:
            super(ImgButton, self).__init__()
            self.box = Gtk.HBox(2)
            self.add(self.box)
            self.icon = Gtk.Image()
            self.icon.set_from_stock(icon,  Gtk.IconSize.BUTTON)
            self.label = Gtk.Label(label)
            self.box.pack_start(self.icon, True, True, 0)
            self.box.pack_start(self.label, True, True, 0)
            self.icon.show()
            self.label.show()