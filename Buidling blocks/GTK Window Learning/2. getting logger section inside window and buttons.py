import gi
from gi.repository import Gtk
from pprint import pprint
import time

# see all GTk documentation here
# http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Window.html


def window_destroyer(theWindow, event):
    print 'in the doestroyer function'
    del theWindow
    window_destroyer.destroy_count += 1
    if window_destroyer.destroy_count == 1:
        print 'Exiting Program'
        Gtk.main_quit()

# function are really objects. window_destroyer.destroy_count here acts as
# static variable
window_destroyer.destroy_count = 0


class Log_Window(Gtk.Window):
    """
    This class forms a complete log widow, with buttons, log area, tabs and other.

    Attributes:

    log_buffer:  It is actual text of log. (Gtk.TextBuffer object)
    log_pad: It is the log area, on which log text is written/updated. (Gtk.TextView object)

    There are three buttons on it, which are there to perform respective functions:
    button_start_algo
    button_reset_graph
    button_clear_log

    And a tabed panel which is called Notebook
    """
    

    def __init__(self):

        Gtk.Window.__init__(self, title="Log Window")
        self.connect("delete-event", window_destroyer)

        #----------------BASIC INFOMATION PRINTING ABOUT THE WINDOW--------------------

        # Print the current window's Position, Pointer and Size
        print '{:>50} : {}'.format('get_position()', self.get_position())
        print '{:>50} : {}'.format('get_pointer()', self.get_pointer())
        print '{:>50} : {}'.format('get_size()', self.get_size())

        # This is the way to get current monitor height and width
        # http://lazka.github.io/pgi-docs/Gdk-3.0/classes/Screen.html#Gdk.Screen
        print '{:>50} : {}'.format('get_screen().height()', self.get_screen().height())
        print '{:>50} : {}'.format('get_screen().width()', self.get_screen().width())

        # get_monitor_geometry(monitor_number int ) returns Gdk.Rectangle
        # http://lazka.github.io/pgi-docs/Gdk-3.0/classes/Rectangle.html#Gdk.Rectangle

        print '{:>50} : {}'.format('get_screen().get_monitor_geometry(0).height', self.get_screen().get_monitor_geometry(0).height)
        print '{:>50} : {}'.format('get_screen().get_monitor_geometry(0).width', self.get_screen().get_monitor_geometry(0).width)
        print '{:>50} : {}'.format('get_screen().get_monitor_geometry(0).x', self.get_screen().get_monitor_geometry(0).x)
        print '{:>50} : {}'.format('get_screen().get_monitor_geometry(0).y', self.get_screen().get_monitor_geometry(0).y)


        #---------------------SETTING SIZE AND POSITION OF WINDOW----------------------------

        # Set width = 30% of Horizontal Length and Full Height
        # this function sets the size of window
        self.resize(self.get_screen().width() * .3, self.get_screen().height())

        # setting window's position
        # self.set_pointer(0,0) --does not work
        self.move(self.get_screen().width() * .7, 0)

        #------------------------Buidling buttons, log area, algorithm sections----------------     
        

        #------------------------Buttons-------------------------------------------------------
        self.button_start_algo = Gtk.Button(label="Start Algo")
        self.button_start_algo.connect(
            "clicked", self.on_button_start_algo_clicked)
        # self.button_start_algo.set_vexpand(True)
        # self.button_start_algo.set_hexpand(True)


        self.button_reset_graph = Gtk.Button(label="Reset Graph")
        self.button_reset_graph.connect(
            "clicked", self.on_button_reset_graph_clicked)
        # self.button_reset_graph.set_vexpand(True)
        # self.button_reset_graph.set_hexpand(True)


        self.button_clear_log = Gtk.Button(label="Clear Log")
        self.button_clear_log.connect(
            "clicked", self.on_button_clear_log_clicked)
        # self.button_clear_log.set_vexpand(True)
        # self.button_clear_log.set_hexpand(True)
        
        #-----------------------Log and Algorithm lists----------------------------------------

        # Log Area and List of Algorithm is shown in tabs using Notebook class 
        self.notebook = Gtk.Notebook()

        # a scrollbar for the child widget (that is going to be the textview)
        scrolled_window = Gtk.ScrolledWindow()
        
        # we scroll only if needed
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)


        self.log_buffer = Gtk.TextBuffer() 
        self.log_pad = Gtk.TextView(buffer=self.log_buffer)

        # wrap the text, if needed, breaking lines in between words
        self.log_pad.set_wrap_mode(Gtk.WrapMode.WORD)
        self.log_pad.set_editable(False) # Log is only readable 
        self.log_pad.set_cursor_visible(False) # Hiding cursor for read-only area

        # textview is scrolled
        scrolled_window.add(self.log_pad)

        # First tab of Notebook
        self.notebook.append_page(scrolled_window, Gtk.Label('Log'))


        # Adding second tab in Notebook
        self.page2 = Gtk.Box()
        # self.page2.set_border_width(10)
        self.page2.add(Gtk.Label('A page with an image for a Title.'))
        self.notebook.append_page(self.page2, Gtk.Label('Algorithms'))

        # This is required so that the Notebook element streaches to occupy the reaming sections
        # in Log_window. Wthout following code, the Notebooks will be shown in default size only
        # If you did not understand this, try commenting these and observe
        self.notebook.set_vexpand(True)
        self.notebook.set_hexpand(True)
        
        #----------------------Buttons and Notebook is ready---------------------------------
        #---------------------- Its time for laying out the elements using Grid layout------- 

        grid = Gtk.Grid()

        # [attach] and [attach_next_to] functions have following syntax: 

        # attach(child, col #, row #, width--col span, height--row span)
        # attach_next_to(child, sibling, side, width--col span, height--row span)


        grid.add(self.button_start_algo)
        grid.attach(self.button_reset_graph, 1, 0, 1, 1)
        grid.attach(self.button_clear_log, 2, 0, 1, 1)       
        grid.attach_next_to(
            self.notebook, self.button_start_algo, Gtk.PositionType.BOTTOM, 10, 100)

        self.add(grid)

    def on_button_start_algo_clicked(self, widget):
        print("Hello")
        for x in range(0,15):
            self.log_buffer.insert(self.log_buffer.get_end_iter(), "> first log\n")

    def on_button_reset_graph_clicked(self, widget):
        print("Goodbye")

    def on_button_clear_log_clicked(self, widget):
        print("Goodbye")
        self.log_buffer.delete(self.log_buffer.get_start_iter(), self.log_buffer.get_end_iter())

win=Log_Window()

win.show_all()

Gtk.main()