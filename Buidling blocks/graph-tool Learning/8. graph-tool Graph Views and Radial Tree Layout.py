from graph_tool.all import *
# We need some Gtk functions
from gi.repository import Gtk, Gdk
import sys
import time


# this is the input graph
g = Graph()

# Following code creates a graph of 6 vertex and more then 6 edges 
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()
v5 = g.add_vertex()
v6 = g.add_vertex()

e1 = g.add_edge(v1, v2)
e2 = g.add_edge(v1, v4)
e3 = g.add_edge(v1, v3)

e4 = g.add_edge(v4, v5)
e5 = g.add_edge(v4, v6)
e6 = g.add_edge(v4, v3)

e7 = g.add_edge(v5, v1)
e8 = g.add_edge(v5, v3)

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
v_text = g.new_vertex_property("string")


v_Is_in_BFT = g.new_vertex_property("bool")         
e_Is_in_BFT = g.new_edge_property("bool")      






for v in g.vertices():
    vcolor[v] = [0.6, 0.6, 0.6, 1]
    v_Is_in_BFT[v] = True
    v_text[v] = g.vertex_index[v] + 1

for e in g.edges():
    e_Is_in_BFT[e] =  True

# v_Is_in_BFT[0] = False
e_Is_in_BFT[e8] = False
e_Is_in_BFT[e7] = False
e_Is_in_BFT[e6] = False


""" graph filtering https://graph-tool.skewed.de/static/doc/quickstart.html#graph-filtering

   HOW TO FILTER A GRAPH
      1. Create a vertex and edge propeties (v_Is_in_BFT and e_Is_in_BFT here) of type bool
        
             v_Is_in_BFT = g.new_vertex_property("bool")         
             e_Is_in_BFT = g.new_edge_property("bool") 
      
      2. First set True values for each of above variables 
            
            for v in g.vertices():
                v_Is_in_BFT[v] = True
                
            for e in g.edges():
                e_Is_in_BFT[e] =  True


      3. Set False values for individual vertex or edges for thes ones that you want to hide   

            v_Is_in_BFT[0] = False  # Note that this will also remove/hide linked edges 
            e_Is_in_BFT[e8] = False

      4. Create a GraphView object with parameters as orginal graph and the two filter variable created above 
            
            g2 = GraphView(g, vfilt=v_Is_in_BFT, efilt = e_Is_in_BFT)

      5.Just use g2 with GraphWindow function to show it. Note that , vertex properties and edges properties passed here can be of original graph.
        The removed vertex property entry will not be applied.  In other words, as you can see I did not create new vertex or edge property variables for 
        the new GraphView object considering that some of the vertices/edges of orginal graph are absent here.
        
      READ MORE: https://graph-tool.skewed.de/static/doc/quickstart.html#graph-filtering  
"""
g2 = GraphView(g, vfilt=v_Is_in_BFT, efilt = e_Is_in_BFT)


node_wght = g.new_vertex_property("float")

node_wght[v1] = 0
node_wght[v2] = 3
node_wght[v3] = 3
node_wght[v4] = 3
node_wght[v5] = 20
node_wght[v6] = 20



# Tree layout --root at center--- https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.radial_tree_layout
tree_layout = radial_tree_layout(g2, 0, weighted=False,node_weight = node_wght, r =1)






# tree_layout = arf_layout(g2, weight=None, d=0.1, a=50, dt=0.01, epsilon=2e-10, max_iter=1000, pos=radial_tree_layout(g2, 5), dim=2)
# tree_layout = fruchterman_reingold_layout(g2, weight=None, a=None, r=0.25, scale=None, circular=True, grid=True, t_range=None, n_iter=100, pos=None)

# tree_layout =sfdp_layout(g2, vweight=None, eweight=None, pin=None, groups=None, C=0.2, K=None, p=2.0, theta=0.6, max_level=15, gamma=1.0, mu=0.0, mu_p=1.0, init_step=None, cooling_step=0.95, adaptive_cooling=True, epsilon=0.01, max_iter=0, pos=None, multilevel=None, coarse_method='hybrid', mivs_thres=0.9, ec_thres=0.75, coarse_stack=None, weighted_coarse=False, verbose=False)

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
                  vertex_text=v_text,
                  vertex_font_size=18,
                   # vertex_halo_size = 0.0,  # this is temporary method to
                   # remove halos, which are formed when a node is mouse
                   # hovered
                    geometry=(1000, 800))


win2 = GraphWindow(g2, tree_layout,
                  vertex_halo=False,
                  vertex_fill_color=vcolor,
                  vertex_text=v_text,
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
win.graph.connect("motion-notify-event", motion_event_function)

# We will give the user the ability to stop the program by closing the window.
win.connect("delete_event", Gtk.main_quit)
win2.connect("delete_event", Gtk.main_quit)


# let us set the win windows as per logger window requirement
# this function sets the size of window
win.resize(win.get_screen().width() * .5,win.get_screen().height())

# setting window position
# win.set_pointer(0,0) --does not work
win.move(0,0)


# let us set the win windows as per logger window requirement
# this function sets the size of window
win2.resize(win.get_screen().width() * .5,win.get_screen().height())

# setting window position
# win.set_pointer(0,0) --does not work
win2.move(win.get_screen().width() *.5,0)


# Actually show the window, and start the main loop.
win.show_all()
win2.show_all()
Gtk.main()
