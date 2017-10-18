import graph_tool.all as gt
from math import sqrt
import numpy as np

# g = gt.price_network(1500)
g = gt.Graph()
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()
e1 = g.add_edge(v1, v2)
e2 = g.add_edge(v2, v3)
e3 = g.add_edge(v3, v1)
e4 = g.add_edge(v3, v4)


pos = gt.sfdp_layout(g)

deg = g.degree_property_map("in")
deg.a = 2 * (np.sqrt(deg.a) * 0.5 + 0.4)
ebet = gt.betweenness(g)[1]

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
    v_size[v] = 2
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

 
gt.graphviz_draw(g, pos, vsize = v_size, vcolor=deg, vorder=deg, elen=5,
                 ecolor=ebet, eorder=ebet)

raw_input("Press Enter to Continue")

# # v_fill = g.degree_property_map("in")
# # v_fill = [0.6, 0.6, 0.6, 1]

deg.a = 2 * (np.sqrt(deg.a) * 0.8 + 0.4)

gt.graphviz_draw(g, pos, vsize = v_size, vcolor=deg, vorder=deg, elen=5,
                 ecolor=ebet, eorder=ebet)