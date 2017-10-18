#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This example shows how to create
# and send a custom singal
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
# import gobject


class Sender(GObject.GObject):
    def __init__(self):
        GObject.GObject.__init__(self)
        

GObject.type_register(Sender)
GObject.signal_new("z_signal", Sender, GObject.SIGNAL_RUN_FIRST,
                   GObject.TYPE_NONE, ())


class Receiver(GObject.GObject):
    def __init__(self, sender):
        GObject.GObject.__init__(self)
        
        sender.connect('z_signal', self.report_signal)
        
    def report_signal(self, sender):
        print "Receiver reacts to z_signal"


def user_callback(object):
    print "user callback reacts to z_signal"

if __name__ == '__main__':
    
    sender = Sender()
    receiver = Receiver(sender)

    sender.connect("z_signal", user_callback)
    sender.emit("z_signal")