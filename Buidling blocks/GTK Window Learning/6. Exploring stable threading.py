from gi.repository import Gtk, Gdk, GLib
import Process
import gobject
import threading

class gui():
    def __init__(self):
        self.window = Gtk.Window()
        self.window.connect('delete-event', Gtk.main_quit)

        self.box = Gtk.Box()
        self.window.add(self.box)

        self.label = Gtk.Label('idle')
        self.box.pack_start(self.label, True, True, 0)

        self.progressbar = Gtk.ProgressBar()
        self.box.pack_start(self.progressbar, True, True, 0)

        self.button = Gtk.Button(label='Start')
        self.button.connect('clicked', self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.window.show_all()

        gobject.threads_init()
        GLib.threads_init()
        Gdk.threads_init()
        Gdk.threads_enter()
        Gtk.main()
        Gdk.threads_leave()

def init_progress(self, func, arg):
    self.label.set_text('working1')
    self.worker = threading.Thread(target=func, args=[arg])
    self.running = True
    gobject.timeout_add(200, self.update_progress)
    self.worker.start()

def update_progress(self):
    if self.running:
        self.progressbar.pulse()
    return self.running

def working(self, num):
    Process.heavyworks2(num)    
    gobject.idle_add(self.stop_progress)

def stop_progress(self):
    self.running = False
    self.worker.join()
    self.progressbar.set_fraction(0)
    self.label.set_text('idle') 

def on_button_clicked(self, widget):
    self.init_progress(self.working, 100000)

if __name__ == '__main__':
    gui = gui()