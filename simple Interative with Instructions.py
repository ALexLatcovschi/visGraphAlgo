from graph_tool.all import *
from gi.repository import Gtk
import sys
import time


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
        self.resize(self.get_screen().width() * .298, self.get_screen().height())

        # setting window's position
        # self.set_pointer(0,0) --does not work
        self.move(self.get_screen().width() * .708, 0)

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
        self.log_buffer.insert(self.log_buffer.get_end_iter(), "> first log\n")

    def on_button_reset_graph_clicked(self, widget):
        print("Goodbye")

    def on_button_clear_log_clicked(self, widget):
        print("Goodbye")
        self.log_buffer.delete(self.log_buffer.get_start_iter(), self.log_buffer.get_end_iter())



# this is the input graph
g = Graph()
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()
e1 = g.add_edge(v1, v2)
e2 = g.add_edge(v2, v3)
e3 = g.add_edge(v3, v1)
e4 = g.add_edge(v3, v4)

# these are some custom color variables

S = [1, 1, 1, 1]           # White color
I = [0, 0, 0, 1]           # Black color
R = [0.5, 0.5, 0.5, 1.]    # Grey color (will not actually be drawn)

# How to change graph's coloring, size, type, text and so on? Read below 

# All internal properties are listed here: https://graph-tool.skewed.de/static/doc/draw.html
# To use these properties, first create a variable which you can identify as the property e.g. vcolor (color of vertex ) or vHalocolor (color of halo of a vertex).
# These variable aren't internal but user made. Now how does graph knows vcolor is for Vertex's Colors or
# vHaloColor is for Halo Color?  wait...for trick #1. For, now keep reading


# The color property of the graph in graph-tool is of vector<double> type,
# see all types of variable here
# https://graph-tool.skewed.de/static/doc/graph_tool.html#graph_tool.PropertyMap
vcolor = g.new_vertex_property("vector<double>")
for v in g.vertices():
    vcolor[v] = [0.6, 0.6, 0.6, 1]


# vHaloColor = g.new_vertex_property("string")  # format number 2 string
# for v in g.vertices():
#     vHaloColor[v] = "black"

# This is some automatic layout. Will see details later.
pos = sfdp_layout(g)


# trick #1
# Here is the answer to last question:
# Make sure you know names of all internal properties from https://graph-tool.skewed.de/static/doc/draw.html
# Those names include "shape" "color" "fill_color" "size" "aspect"
# "rotation"... "halo" "halo_color"

# Now to say the vHaloColor is "halo_color". You define this mapping in the function below:
# append "vertex_" with "halo_color" and assign it equal to vHaloColor.
# Its done.

graph_window = GraphWindow(g, pos,
                  vertex_halo=False,
                  vertex_fill_color=vcolor,
                  vertex_text=g.vertex_index,
                  vertex_font_size=18,
                   # vertex_halo_size = 0.0,  # this is temporary method to
                   # remove halos, which are formed when a node is mouse
                   # hovered
                    geometry=(1000, 800))




def button_press_event_function(widget, event):
    """
    This function handles Keyboard Keys and Mouse buttons clicks in Graph Window.
    
    Parameters: 

    widget: the window's pointer on which a button (Keyboard or Mouse) is pressed
    event: event object

    It was attached to Graph Window as an event triggered function. 
    (graph_window.graph.connect("button-press-event", button_press_event_function))   

    """

    # Some global variables require modification
    global g, vcolor
    # this when clicked with mouse left butten, returns |vertex| object to
    # |src|
    src = widget.picked
    
    # condition 1 & 2: No vertex is picked
    # Condition 3: same vertex is clicked/selected again 
    if src is not None and src is not False and src != button_press_event_function.last_picked:

        # I am keeping a pointer to last picked vertex
        # Here--last picked vertex color is changed to show that last selected vertex is not longer valid to start any algorithm  
        if button_press_event_function.last_picked :
            vcolor[button_press_event_function.last_picked] = [0.6, 0.6, 0.6, 1]  

        # showing Yellow color for picked vertex
        vcolor[src] = [0.807843137254902, 0.3607843137254902, 0.0, 1.0]
        
        # updating log
        logger_window.log_buffer.insert(logger_window.log_buffer.get_end_iter(), "> You've picked "+str(src)+" vertex\n")

        # setting current selection as last picked for next loop
        button_press_event_function.last_picked = src

        # following is a workaround to, prevent default coloring of vertexes upon mouse clicks
        # Presently, I don't understand the ".fa" thing (see 2nd line below), will see later 
        widget.picked = None
        widget.selected.fa = False

        # Changing colors requires following 2 lines of code to come in effect
        widget.regenerate_surface()
        widget.queue_draw()    


def motion_event_function(widget, event):
    """This function is to handle any mouse movement over graph widget"""
    
    """ for now, I am doing this to disable default mouse hover action,
    that is--all closest edges are highlighted and the focused vertex is
    highlighted with blue halo color   """
    widget.selected.fa = False

def window_destroyer(theWindow, event):
  """
  theWindow: the window to be closed
  event: delete-event object passed as signal

  This function is called by graph and logger windows
  using
    graph_window.connect("delete_event", window_destroyer)
    logger_window.connect("delete_event", window_destroyer)

  This function destroyes the window which user
  clicks to close x (cross) mark at top right corner.
  It also keep tracks of count of closed window and 
  if all windows are closed, it exits the GTK main program 
   """
  print 'In the destroyer function'
  del theWindow  
  window_destroyer.destroy_count += 1
  # exit GTK program upon closure of both windows (Graph and Log Windows)
  if window_destroyer.destroy_count == 2:
    print 'Exiting Program'
    Gtk.main_quit()     

# function are really objects. window_destroyer.destroy_count here acts as static variable 
window_destroyer.destroy_count = 0


""" Bind the function above as a motion notify handler, see all events
here https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html"""
graph_window.graph.connect("button-press-event", button_press_event_function)
# again a static variable for button_press_event_function  
button_press_event_function.last_picked = None 

# Binder for graph_window
graph_window.graph.connect("motion-notify-event", motion_event_function)


# We will give the user the ability to stop the program by closing the window.
graph_window.connect("delete_event", window_destroyer)

logger_window=Log_Window()
# logger_window.connect("delete-event", window_destroyer)


# let us set the graph_window dimensions to show 70% of left of the whole monitor 
# this function sets the size of window
graph_window.resize(graph_window.get_screen().width() *.7,graph_window.get_screen().height())

# setting window position (This works by --moving-- it to required position)
# graph_window.set_pointer(0,0) --does not work
graph_window.move(0,0)



# Time to show the windows, and start the GTK main loop.
logger_window.show_all()
graph_window.show_all()
Gtk.main()

