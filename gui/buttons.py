__author__ = 'hadware'
import gtk

class ImgButton(gtk.Button):
    """A simple button with an icon instead of a simple label"""

    def __init__(self, label=None, icon = None):
        if icon is None:
            super(ImgButton, self).__init__(label)
        else:
            super(ImgButton, self).__init__()
            self.box = gtk.HBox(False, 2)
            self.add(self.box)
            self.icon = gtk.Image()
            self.icon.set_from_stock(icon,  gtk.ICON_SIZE_BUTTON)
            self.label = gtk.Label(label)
            self.box.pack_start(self.icon)
            self.box.pack_end(self.label)
            self.icon.show()
            self.label.show()