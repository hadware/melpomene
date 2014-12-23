#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

class HelloWorld():

    def hello(self, widget, data = None):
        print("Hello suckers")

    def delete_event(self, widget, event, data = None):
        print("Delete event generated")
        return False

    def destroy(self, widget, data = None):
        print("Destruction!")
        gtk.mainquit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.button = gtk.Button("Hello World")
        self.button.connect("clicked", self.hello, None)
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        self.buttons = [gtk.Button("Button %d" % i) for i in range(10)]
        self.box = gtk.VBox(False, 0)
        self.window.add(self.box)
        for i, button in enumerate(self.buttons):
            if i % 2 == 0:
                self.box.pack_start(button, expand=True, fill=True, padding=0)
            else:
                self.box.pack_end(button, expand=True, fill=True, padding=0)
            button.show()
        self.box.show()
        #self.button.show()
        self.window.show()

    def main(self):
        gtk.main()
        print __name__

if __name__ == "__main__":
    helloword = HelloWorld()
    helloword.main()