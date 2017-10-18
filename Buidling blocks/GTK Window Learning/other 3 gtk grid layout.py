import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Grid Example")

        grid = Gtk.Grid()
        self.add(grid)

        # let us set the self windows as per logger window requirement
        # this function sets the size of window
        self.resize(self.get_screen().width() * .3, self.get_screen().height())

        # setting window position
        # self.set_pointer(0,0) --does not work
        self.move(self.get_screen().width() * .7, 0)
        # grid.set_vexpand(True)
        # grid.set_hexpand(True)
        
        print grid.get_vexpand()
        
        button1 = Gtk.Button(label="Button 1")
        button2 = Gtk.Button(label="Button 2")
        
        button2.set_vexpand(True)
        button2.set_hexpand(True)
        
        button3 = Gtk.Button(label="Button 3")
        button4 = Gtk.Button(label="Button 4")
        button5 = Gtk.Button(label="Button 5")
        button6 = Gtk.Button(label="Button 6")
        button7 = Gtk.Button(label="Button 7")

        """
        attach(child, col #, row #, width--col span, height--row span)
        attach_next_to(child, sibling, side, width--col span, height--row span)
        """

        # grid.add(button1)
        # grid.attach(button2, 1, 0, 2, 1)
        # grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 2)
        # grid.attach_next_to(button4, button3, Gtk.PositionType.RIGHT, 2, 1)
        # grid.attach(button5, 1, 2, 1, 1)
        # grid.attach_next_to(button6, button5, Gtk.PositionType.RIGHT, 1, 1)

        grid.add(button1)
        # grid.attach(button1, 0,0,1,1)
        # grid.attach(button2, 1,0,2,1)
        grid.attach_next_to(button2, button1, Gtk.PositionType.RIGHT, 4,1)



win = GridWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()