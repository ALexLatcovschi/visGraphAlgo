from graph_tool.all import *
from gi.repository import Gtk, GObject, Gdk
import cairo

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

# last
White = [1, 1, 1, 1]           # White color
Black = [0, 0, 0, 1]           # Black color
Grey = [0.5, 0.5, 0.5, 1]    # Grey color (will not actually be drawn)
Midnight_Blue = [.098, .098, .4392, 1]
Orange_Red = [1, .2705, 0, 1]
Dark_Orchid = [.6, .196, .8, 1]
Dark_Red = [.545, 0, 0]
Indian_Red = [0.6902, 0.0902, 0.1216, 1, ]
Golden = [1, 0.8431, 0, 1, ]
Yellow = [1, 1, 0, 1]
Forest_Green = [0.1333, 0.5451, 0.1333, 1]
Saddle_Brown = [0.5451, 0.2706, 0.0745, 1]
Green_Parrot = [0.6039, 0.8039, 0.1961, 1]


# Here is the trick
# All internal properties are listed here: https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.graph_draw
# To use it, first create a variable which you can identify as the property e.g. v_fill_color or vHalocolor.
# These variable aren't internal but user made. Now how does graph knows v_fill_color is for Vertex Colors or
# vHaloColor is for Halo Color?  wait...for next trick 2


# The color property of the graph in graph tool is of vector<double> type,
# see all types of variable here
# https://graph-tool.skewed.de/static/doc/graph_tool.html#graph_tool.PropertyMap
v_shape = g.new_vertex_property("int")
v_color = g.new_vertex_property("vector<double>")
v_fill_color = g.new_vertex_property("vector<double>")
v_size = g.new_vertex_property("double")
v_aspect = g.new_vertex_property("double")
v_rotation = g.new_vertex_property("double")
v_anchor = g.new_vertex_property("double")
v_pen_width = g.new_vertex_property("double")
v_halo = g.new_vertex_property("bool")
v_halo_color = g.new_vertex_property("vector<double>")
v_halo_size = g.new_vertex_property("double")
v_text = g.new_vertex_property("string")
v_text_color = g.new_vertex_property("vector<double>")
v_text_position = g.new_vertex_property("double")
v_text_rotation = g.new_vertex_property("double")
v_text_offset = g.new_vertex_property("vector<double>")
v_font_family = g.new_vertex_property("string")
v_font_slant = g.new_vertex_property("int")
v_font_weight = g.new_vertex_property("int")
v_font_size = g.new_vertex_property("float")
v_surface = g.new_vertex_property("object")
v_pie_fractions = g.new_vertex_property("vector<double>")
v_pie_colors = g.new_vertex_property("vector<double>")


# for v in g.vertices():
v_fill_color[0] = Golden
v_fill_color[1] = Midnight_Blue
v_fill_color[2] = Indian_Red
v_fill_color[3] = Dark_Orchid


for v in g.vertices():
    v_halo_color[v] = Saddle_Brown
    v_size[v] = 80
    v_halo[v] = True
    v_halo_size[v] = 1.3
    v_font_size[v] = 25
    v_font_family[v] = "Consolas"


e_color =g.new_edge_property( "vector<double>")
e_pen_width =g.new_edge_property( "double")
e_start_marker =g.new_edge_property( "int")
e_mid_marker =g.new_edge_property( "int")
e_end_marker =g.new_edge_property( "string")
e_marker_size =g.new_edge_property( "double")
e_mid_marker_pos =g.new_edge_property( "double")
e_control_points =g.new_edge_property( "vector<double>")
e_gradient =g.new_edge_property( "vector<double>")
e_dash_style =g.new_edge_property( "vector<double>")
e_text =g.new_edge_property( "string")
e_text_color =g.new_edge_property( "vector<double>")
e_text_distance =g.new_edge_property( "double")
e_text_parallel =g.new_edge_property( "bool")
e_font_family =g.new_edge_property( "string")
e_font_slant =g.new_edge_property( "int")
e_font_weight =g.new_edge_property( "int")
e_font_size =g.new_edge_property( "double")
e_sloppy =g.new_edge_property( "bool")
e_seamless =g.new_edge_property( "bool")

for e in g.edges():
    e_color[e] = Indian_Red
    e_dash_style[e] = []
    e_pen_width[e] = 5
    e_end_marker[e] = "arrow"
    e_marker_size[e] = 30
    e_text[e] = "edge text"
    e_font_size[e] = 20
    e_font_family[e] = "Consolas"




# vHaloColor = g.new_vertex_property("string")  # format number 2 string
# for v in g.vertices():
#     vHaloColor[v] = "black"

# This is some automatic layout. Will see details later.
pos = sfdp_layout(g)


# trick no 2
# Here is answer to last question:
# Make sure you know names of all internal properties from https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.graph_draw
# Those names include "shape" "color" "fill_color" "size" "aspect"
# "rotation"... "halo" "halo_color"

# Now to say the vHaloColor is "halo_color". You define this mapping in the function below:
# append "vertex_" with "halo_color" and assign it equal to vHaloColor.
# Its done.


# see all default styles here: https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/cairo_draw.html

graph_window = GraphWindow(g, pos,
                       # The size of the vertex, in the default units of
                       # the output format (normally either pixels or
                           # points).
                       vertex_size=v_size,
                       # vertex_pen_width = 10,
                       vertex_halo=v_halo,  # to enalbe halos
                       # here 1.3 means, 1.3 times of single line, as I've
                       # observed using trials
                       vertex_halo_size=v_halo_size,
                       vertex_halo_color=v_halo_color,

                       vertex_fill_color=v_fill_color,

                       vertex_text=g.vertex_index,
                       vertex_font_size=v_font_size,
                       vertex_font_family=v_font_family,

                       edge_color=e_color,
                       edge_pen_width=e_pen_width,

                       # Edge markers. Can be one of "none", "arrow",
                       # "circle", "square", "diamond", or "bar".
                       # Optionally, this might take a numeric value
                       # corresponding to position in the list above.
                       edge_end_marker=e_end_marker,
                       edge_marker_size = e_marker_size,

                       edge_dash_style =e_dash_style,

                       edge_text = e_text,
                       edge_font_size = e_font_size,
                       edge_font_family = e_font_family,
                       # vertex_halo_size = 0.0,  # this is temporary method to
                       # remove halos, which are formed when a node is mouse
                       # hovered
                       geometry=(400, 400))


"""
Parameters for above functionq        
 |      ----------
 |      g : :class:`~graph_tool.Graph`
 |          Graph to be drawn.
 |      pos : :class:`~graph_tool.PropertyMap`
 |          Vector-valued vertex property map containing the x and y coordinates of
 |          the vertices.
 |      geometry : tuple
 |          Widget geometry.
 |      vprops : dict (optional, default: ``None``)
 |          Dictionary with the vertex properties. Individual properties may also be
 |          given via the ``vertex_<prop-name>`` parameters, where ``<prop-name>`` is
 |          the name of the property.
 |      eprops : dict (optional, default: ``None``)
 |          Dictionary with the edge properties. Individual properties may also be
 |          given via the ``edge_<prop-name>`` parameters, where ``<prop-name>`` is
 |          the name of the property.
 |      vorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
 |          If provided, defines the relative order in which the vertices are drawn.
 |      eorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
 |          If provided, defines the relative order in which the edges are drawn.
 |      nodesfirst : bool (optional, default: ``False``)
 |          If ``True``, the vertices are drawn first, otherwise the edges are.
 |      update_layout : bool (optional, default: ``True``)
 |          If ``True``, the layout will be updated dynamically.
 |      **kwargs
 |          Any extra parameters are passed to :class:`~graph_tool.draw.GraphWidget` and
 |          :func:`~graph_tool.draw.cairo_draw`.

"""

def button_press_event_function(widget, event):
    global g, v_fill_color, graph_window, sender
    # this when clicked with mouse left butten, returns |vertex| object to
    # |src|
    src = widget.picked
    # import ipdb; ipdb.set_trace()
    # for v in g.vertices():
    # widget.disconnect_by_func(button_press_event_function)

    if src is not None and src is not False:        

        for v in g.vertices():
            v_fill_color[v] = White
            v_text_color[v] = Black 

        v_fill_color[src] = [0.807, 0.360, 0.0, 1]
        
        for out_edge in src.out_edges():
             e_dash_style[out_edge] = [.02,.02,.02,.02,.02,.02,.02]
             v_halo_color[out_edge.target()] = Green_Parrot


    widget.picked = None
    widget.selected.fa = False



    # see definition here https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html
    graph_window.graph.regenerate_surface(complete = True, reset = True)
    graph_window.graph.queue_draw()
    cr= cairo.Context(widget.base)
    graph_window.graph.draw(None,cr)
    cr.paint()

    
    # Gtk.main_iteration()
    # Gtk.main_iteration_do(False)

    # Gtk.cairo_should_draw_window(cr, graph_window)
    # widget.emit("button-release-event", GdkEvent)
    # widget.draw()
    raw_input("Press Enter to Continue ")

    update_state()
    
    if src is not None and src is not False:
        v_fill_color[src] = Dark_Red
        
        for out_edge in src.out_edges():
             e_dash_style[out_edge] = []
             v_halo_color[out_edge.target()] = Saddle_Brown


    graph_window.graph.regenerate_surface()
    graph_window.graph.queue_draw()

    # raw_input("Press Enter Exit ")
    # Gtk.main_quit()


def motion_event_function(widget, event):
    global graph_window
    """This function is to handle any mouse movement over graph widget"""

    """ for now, I am doing this to disable default mouse hover action,
    that is--all closest edges are highlighted and the focused vertex is
    highlighted with blue halo color   """    
    widget.selected.fa = False
    
    

def button_release_event_function(widget, event):
    """This function is to handle any mouse movement over graph widget"""

    """ for now, I am doing this to disable default mouse hover action,
    that is--all closest edges are highlighted and the focused vertex is
    highlighted with blue halo color   """
    print "in button release case"
    return
        


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
    if window_destroyer.destroy_count == 1:
        print 'Exiting Program'
        Gtk.main_quit()


def update_state():
    global graph_window
    graph_window.graph.regenerate_surface()
    graph_window.graph.queue_draw()
    print "m",



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

sender = Sender()
receiver = Receiver(sender)
sender.connect("z_signal", user_callback)

# function are really objects. window_destroyer.destroy_count here acts as
# static variable
window_destroyer.destroy_count = 0


""" Bind the function above as a montion notify handler, see all events
here https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html"""
graph_window.graph.connect("button-press-event", button_press_event_function)


graph_window.graph.connect("motion-notify-event", motion_event_function)
graph_window.graph.connect("button-release-event", button_release_event_function)




# We will give the user the ability to stop the program by closing the window.
graph_window.connect("delete_event", window_destroyer)


# let us set the graph_window as per logger window requirement
# this function sets the size of window
# graph_window.resize(graph_window.get_screen().width() * .7,
#                     graph_window.get_screen().height())

# setting window position
# graph_window.set_pointer(0,0) --does not work
graph_window.move(0, 0)

cid = GObject.timeout_add(1000,update_state)

graph_window.show_all()
Gtk.main()