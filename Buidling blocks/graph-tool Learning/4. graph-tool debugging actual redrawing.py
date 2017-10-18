from graph_tool.all import *
from gi.repository import Gtk
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



for v in g.vertices():
    # v_halo_color[v] = Saddle_Brown
    v_size[v] = 80
    v_halo[v] = True
    v_halo_size[v] = 1.3
    v_font_size[v] = 25
    v_font_family[v] = "Consolas"
    v_fill_color[v] = White
    v_text_color[v] = Black


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
    # e_text[e] = "edge text"
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
                       geometry=(1000, 800))


def button_press_event_function(widget, event):
    global g, v_fill_color, graph_window
    # this when clicked with mouse left butten, returns |vertex| object to
    # |src|
    src = widget.picked
    
    if src is not None and src is not False:
        if int(src) == 0:
           for v in g.vertices():
                v_fill_color[v] = White
                v_halo_color[v] = []
        else:
            
            v_fill_color[src] = [0.807, 0.360, 0.0, 1]
        
            for out_edge in src.out_edges():
                 e_dash_style[out_edge] = [.02,.02,.02,.02,.02,.02,.02]
                 v_halo_color[out_edge.target()] = Green_Parrot

    widget.picked = None
    widget.selected.fa = False

    widget.regenerate_surface()
    widget.queue_draw()
    # cr = cairo.Context(widget.base)

    # widget.draw(None, cr)
    # cr.paint()


    # Gtk.main_iteration()




    raw_input("Press Enter to Continue ")
    # del g._Graph__known_properties[id(self)]

    # graph_window.graph.connect("button-press-event", button_press_event_function)



""" Bind the function above as a montion notify handler, see all events
here https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html"""
graph_window.graph.connect("button-press-event", button_press_event_function)


# graph_window.graph.connect("motion-notify-event", motion_event_function)


# We will give the user the ability to stop the program by closing the window.
graph_window.connect("delete_event", Gtk.main_quit)


# let us set the graph_window as per logger window requirement
# this function sets the size of window
graph_window.resize(graph_window.get_screen().width() * .5,
                    graph_window.get_screen().height())

# setting window position
# graph_window.set_pointer(0,0) --does not work
graph_window.move(0, 0)

graph_window.show_all()
Gtk.main()
