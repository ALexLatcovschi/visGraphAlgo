import time
import logging
import threading
from gi.repository import Gtk


class Worker(threading.Thread):
    should_record = False
    quit = False

    def run(self):
        while not self.quit:
            if self.should_record:
                logging.warn("recording...")
                # cpu-intensive code here
            else:
                time.sleep(0.1)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.worker = Worker()
        self.worker.start()
        hb = Gtk.Box()
        self.add(hb)
        record = Gtk.Button("Record")
        stop = Gtk.Button("Stop")
        hb.add(record)
        hb.add(stop)

        def command(arg):
            self.worker.should_record = arg

        record.connect("clicked", lambda _b: command(True))
        stop.connect("clicked", lambda _b: command(False))
        # optional, if you want to quit the app on stop as well
        stop.connect("clicked", lambda _b: Gtk.main_quit())

if __name__ == "__main__":
    main = MainWindow()
    try:
        # optional, if you want to support close window to quit app
        main.connect("delete-event", Gtk.main_quit)
        main.show_all()
        Gtk.main()
    finally:
        main.worker.quit = True
        main.worker.join()