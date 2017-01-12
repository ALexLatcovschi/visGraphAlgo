from graph_tool.all import *
# We need some Gtk functions
from gi.repository import Gtk, Gdk
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

win = GraphWindow(g, pos,
                  vertex_halo=False,
                  vertex_fill_color=vcolor,
                  vertex_text=g.vertex_index,
                  vertex_font_size=18,
                   # vertex_halo_size = 0.0,  # this is temporary method to
                   # remove halos, which are formed when a node is mouse
                   # hovered
                    geometry=(1000, 800))


def button_press_event_function(widget, event):
    global g, vcolor, win
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

    # win.graph.connect("button-press-event", button_press_event_function)


def motion_event_function(widget, event):
    """This function is to handle any mouse movement over graph widget"""
    global g, vcolor, win
    """ for now, I am doing this to disable default mouse hover action,
    that is--all closest edges are highlighted and the focused vertex is
    highlighted with blue halo color   """
    widget.selected.fa = False

""" Bind the function above as a montion notify handler, see all events
here https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html"""
win.graph.connect("button-press-event", button_press_event_function)


win.graph.connect("motion_notif_-event", motion_event_function)


# We will give the user the ability to stop the program by closing the window.
win.connect("delete_event", Gtk.main_quit)

# Actually show the window, and start the main loop.
win.show_all()
Gtk.main()
