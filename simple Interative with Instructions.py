from graph_tool.all import *
from gi.repository import Gtk

# We need some Gtk functions
import sys
import time

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


# Here is the trick
# All internal properties are listed here: https://graph-tool.skewed.de/static/doc/draw.html
# To use it, first create a variable which you can identify as the property e.g. vcolor or vHalocolor.
# These variable aren't internal but user made. Now how does graph knows vcolor is for Vertex Colors or
# vHaloColor is for Halo Color?  wait...for next trick 2


# The color property of the graph in graph tool is of vector<double> type,
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


# trick no 2
# Here is answer to last question:
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
    global g, vcolor, graph_window
    # this when clicked with mouse left butten, returns |vertex| object to
    # |src|
    src = widget.picked
    # import ipdb; ipdb.set_trace()
    # for v in g.vertices():
    if src is not None and src is not False:
        vcolor[src] = [0.807843137254902, 0.3607843137254902, 0.0, 1.0]
        # vHaloColor[src] = "red"

    widget.picked = None
    widget.selected.fa = False

    widget.regenerate_surface()
    widget.queue_draw()

    # graph_window.graph.connect("button-press-event", button_press_event_function)


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
  if window_destroyer.destroy_count == 2:
    print 'Exiting Program'
    Gtk.main_quit()     

# function are really objects. window_destroyer.destroy_count here acts as static variable 
window_destroyer.destroy_count = 0


""" Bind the function above as a montion notify handler, see all events
here https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html"""
graph_window.graph.connect("button-press-event", button_press_event_function)


graph_window.graph.connect("motion-notify-event", motion_event_function)


# We will give the user the ability to stop the program by closing the window.
graph_window.connect("delete_event", window_destroyer)

logger_window=Gtk.Window()
logger_window.connect("delete-event", window_destroyer)


# let us set the logger_window as per logger window requirement
# this function sets the size of window
logger_window.resize(logger_window.get_screen().width() *.3,logger_window.get_screen().height())

# setting window position
# logger_window.set_pointer(0,0) --does not work
logger_window.move(logger_window.get_screen().width() *.7,0)


# let us set the graph_window as per logger window requirement
# this function sets the size of window
graph_window.resize(graph_window.get_screen().width() *.7,graph_window.get_screen().height())

# setting window position
# graph_window.set_pointer(0,0) --does not work
graph_window.move(0,0)



# Actually show the windows, and start the main loop.
logger_window.show_all()
graph_window.show_all()
Gtk.main()

