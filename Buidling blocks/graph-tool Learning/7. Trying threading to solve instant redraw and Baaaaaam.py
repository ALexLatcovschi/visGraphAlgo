from graph_tool.all import *
from gi.repository import Gtk, GObject, GLib
import sys
import time
import threading



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
    start_vertex = None

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
        global graph_window, logger_window
        print("Hello")
        # self.log_buffer.insert(self.log_buffer.get_end_iter(), "> first log\n")
        Log_Window.t1 = threading.Thread(target=g.show_BFS,args=(graph_window,logger_window, Log_Window.start_vertex,))
        Log_Window.daemon = True
        Log_Window.t1.start()
        # g.show_BFS(graph_window,logger_window, Log_Window.start_vertex)

    def on_button_reset_graph_clicked(self, widget):
        print("Goodbye")

    def on_button_clear_log_clicked(self, widget):
        print("Goodbye")
        self.log_buffer.delete(self.log_buffer.get_start_iter(), self.log_buffer.get_end_iter())



class GraphL(Graph):
    """
    Graph object, which posses all properties of a graph. Here, is how to create a graph.  


    >>> mygraph = GraphL(g=None, directed=True, prune=False, vorder=None)
    
    @Parameter Details: -----------------------------------------------------------------
    
    g       : If --g-- is specified, the graph (and its internal properties) will be 
              copied.
    
    directed: This class encapsulates either a directed multigraph (default or if
              --directed--=True) or an undirected multigraph (if --directed=False--),
              with optional internal edge, vertex or graph properties.
              prune:
      
    Prune   : If --prune-- is set to --True--, and --g-- is specified, only the filtered
              graph will be copied, and the new graph object will not be
              filtered. Optionally, a tuple of three booleans can be passed as value to
              --prune--, to specify a different behavior to vertex, edge, and reversal
              filters, respectively. 
      
    Vorder  : If --vorder-- is specified, it should correspond to a vertex
              :class:`~graph_tool.PropertyMap` specifying the ordering of the vertices in
              the copied graph.       
    --------------------------------------------------------------------------------------
    
    To make a sample graph use this:
    >>> mygraph.make_Sample()
    
    --------------------------------------------------------------------------------------
    
    Color variables are available with this object as class Attributes.
    Colors ={
    'White' : [1, 1, 1, 1],          # White color
    'Black' : [0, 0, 0, 1],          # Black color
    'Grey ' : [0.5, 0.5, 0.5, 1],    # Grey color 
    'Midnight_Blue' : [.098, .098, .4392, 1],
    'Orange_Red' : [1, .2705, 0, 1],
    'Dark_Orchid' : [.6, .196, .8, 1],
    'Dark_Red' : [.545, 0, 0],
    'Indian_Red' : [0.6902, 0.0902, 0.1216, 1, ],
    'Golden' : [1, 0.8431, 0, 1, ],
    'Yellow' : [1, 1, 0, 1],
    'Forest_Green' : [0.1333, 0.5451, 0.1333, 1],
    'Saddle_Brown' : [0.5451, 0.2706, 0.0745, 1],
    'Green_Parrot' : [0.6039, 0.8039, 0.1961, 1],
    }

    """
    

    Colors ={
    'White' : [1., 1., 1., 1.],           # White color
    'Black' : [0., 0., 0., 1.],           # Black color
    'Grey' : [0.5, 0.5, 0.5, 1],    # Grey color 
    'Midnight_Blue' : [.098, .098, .4392, 1],
    'Orange_Red' : [1, .2705, 0, 1],
    'Dark_Orchid' : [.6, .196, .8, 1],
    'Dark_Red' : [.545, 0, 0],
    'Indian_Red' : [0.6902, 0.0902, 0.1216, 1, ],
    'Golden' : [1, 0.8431, 0, 1, ],
    'Yellow' : [1, 1, 0, 1],
    'Forest_Green' : [0.1333, 0.5451, 0.1333, 1],
    'Saddle_Brown' : [0.5451, 0.2706, 0.0745, 1],
    'Green_Parrot' : [0.6039, 0.8039, 0.1961, 1],
     'Dark_Green' : [ 0, 0.3922, 0, 1],
     'Light_Steel_Blue': [ 0.6902, 0.7686, 0.0863, 1],
     'Silver': [ 0.7529, 0.7529, 0.0745, 1]
    }

    def __init__(self,g=None, directed=True, prune=False, vorder=None):
        Graph.__init__(self,g,directed, prune, vorder)
        # How to change graph's coloring, size, type, text and so on? Read below 

        # All internal properties are listed here: https://graph-tool.skewed.de/static/doc/draw.html
        # To use these properties, first create a variable which you can identify as the property e.g. v_color (color of vertex ) or vHalocolor (color of halo of a vertex).
        # These variable aren't internal but user made. Now how does graph knows v_color is for Vertex's Colors or
        # vHaloColor is for Halo Color?  wait...for trick #1. For, now keep reading


        # The color property of the graph in graph-tool is of vector<double> type,
        # see all types of variable here
        # https://graph-tool.skewed.de/static/doc/graph_tool.html#graph_tool.PropertyMap
        # see all default styles and internal property types here: https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/cairo_draw.html    

        self.v_shape = self.new_vertex_property("int")
        self.v_color = self.new_vertex_property("vector<double>")
        self.v_fill_color = self.new_vertex_property("vector<double>")
        self.v_size = self.new_vertex_property("double")
        self.v_aspect = self.new_vertex_property("double")
        self.v_rotation = self.new_vertex_property("double")
        self.v_anchor = self.new_vertex_property("double")
        self.v_pen_width = self.new_vertex_property("double")
        self.v_halo = self.new_vertex_property("bool")
        self.v_halo_color = self.new_vertex_property("vector<double>")
        self.v_halo_size = self.new_vertex_property("double")
        self.v_text = self.new_vertex_property("string")
        self.v_text_color = self.new_vertex_property("vector<double>")
        self.v_text_position = self.new_vertex_property("double")
        self.v_text_rotation = self.new_vertex_property("double")
        self.v_text_offset = self.new_vertex_property("vector<double>")
        self.v_font_family = self.new_vertex_property("string")
        self.v_font_slant = self.new_vertex_property("int")
        self.v_font_weight = self.new_vertex_property("int")
        self.v_font_size = self.new_vertex_property("float")
        self.v_surface = self.new_vertex_property("object")
        self.v_pie_fractions = self.new_vertex_property("vector<double>")
        self.v_pie_colors = self.new_vertex_property("vector<double>")
        

        self.e_color =self.new_edge_property( "vector<double>")
        self.e_pen_width =self.new_edge_property( "double")
        self.e_start_marker =self.new_edge_property( "int")
        self.e_mid_marker =self.new_edge_property( "int")
        self.e_end_marker =self.new_edge_property( "string")
        self.e_marker_size =self.new_edge_property( "double")
        self.e_mid_marker_pos =self.new_edge_property( "double")
        self.e_control_points =self.new_edge_property( "vector<double>")
        self.e_gradient =self.new_edge_property( "vector<double>")
        self.e_dash_style =self.new_edge_property( "vector<double>")
        self.e_text =self.new_edge_property( "string")
        self.e_text_color =self.new_edge_property( "vector<double>")
        self.e_text_distance =self.new_edge_property( "double")
        self.e_text_parallel =self.new_edge_property( "bool")
        self.e_font_family =self.new_edge_property( "string")
        self.e_font_slant =self.new_edge_property( "int")
        self.e_font_weight =self.new_edge_property( "int")
        self.e_font_size =self.new_edge_property( "double")
        self.e_sloppy =self.new_edge_property( "bool")
        self.e_seamless =self.new_edge_property( "bool")       



    def make_Sample(self):

        # Following code creates a graph of 4 vertex and 4 edges 
        v1 = self.add_vertex()
        v2 = self.add_vertex()
        v3 = self.add_vertex()
        v4 = self.add_vertex()
        e1 = self.add_edge(v1, v2)
        e2 = self.add_edge(v2, v3)
        e3 = self.add_edge(v3, v1)
        e4 = self.add_edge(v3, v4)

        # Here are some sample style setting for the graph 
        
        self.v_fill_color[0] = GraphL.Colors['Golden']
        self.v_fill_color[1] = GraphL.Colors['Midnight_Blue']
        self.v_fill_color[2] = GraphL.Colors['Indian_Red']
        self.v_fill_color[3] = GraphL.Colors['Dark_Orchid']


        for v in self.vertices():
            self.v_halo_color[v] = GraphL.Colors['Saddle_Brown']
            self.v_size[v] = 80
            self.v_text_color[v] = GraphL.Colors['Black'] 
            self.v_halo[v] = True
            self.v_halo_size[v] = 1.3
            self.v_font_size[v] = 25
            self.v_font_family[v] = "Consolas"

        for e in self.edges():
            self.e_color[e] = GraphL.Colors['Grey']
            self.e_dash_style[e] = []
            self.e_pen_width[e] = 5
            self.e_end_marker[e] = "arrow"
            self.e_marker_size[e] = 30
            self.e_text[e] = "edge text"
            self.e_font_size[e] = 20
            self.e_font_family[e] = "Consolas"

    def make_Sample_2(self):

        # Following code creates a graph of 6 vertex and more then 6 edges 
        v1 = self.add_vertex()
        v2 = self.add_vertex()
        v3 = self.add_vertex()
        v4 = self.add_vertex()
        v5 = self.add_vertex()
        v6 = self.add_vertex()

        e1 = self.add_edge(v1, v2)
        e2 = self.add_edge(v1, v4)
        e3 = self.add_edge(v1, v3)

        e4 = self.add_edge(v4, v5)
        e5 = self.add_edge(v4, v6)
        e6 = self.add_edge(v4, v3)

        e7 = self.add_edge(v5, v1)
        e8 = self.add_edge(v5, v3)

        for v in self.vertices():
            self.v_fill_color[v] = GraphL.Colors['White']
            self.v_halo_color[v] = GraphL.Colors['Saddle_Brown']
            self.v_size[v] = 80
            self.v_text_color[v] = GraphL.Colors['Black'] 
            self.v_halo[v] = True
            self.v_halo_size[v] = 1.3
            self.v_font_size[v] = 25
            self.v_font_family[v] = "Consolas"

        for e in self.edges():
            self.e_color[e] = GraphL.Colors['Grey']
            self.e_dash_style[e] = []
            self.e_pen_width[e] = 5
            self.e_end_marker[e] = "arrow"
            self.e_marker_size[e] = 30
            self.e_text[e] = "edge text"
            self.e_font_size[e] = 20
            self.e_font_family[e] = "Consolas"
    
    def repaint_Graph(self,graph_window, logger_window,log_text = '', seconds=1):
        GLib.idle_add( self.render_wait_log, graph_window, logger_window, log_text,2)
        time.sleep(seconds)

    def render_wait_log(self,graph_window, logger_window,log_text = '', seconds=1):
               

        graph_window.graph.regenerate_surface()
        graph_window.graph.queue_draw()
        
        logger_window.log_buffer.insert(logger_window.log_buffer.get_end_iter(), "> "+log_text+"\n")
        # print log_text
        # time.sleep(seconds) 
        



    def show_BFS(self, graph_window, logger_window, root_vertex = 0):
        
        if root_vertex is None or root_vertex < 0 or root_vertex > (self.num_vertices()-1): 
            return None

        state =[]
        arrive = []
        counter = 0
        BFT_Queue = []
        parent = []
        
        self.repaint_Graph(graph_window, logger_window, 'Setting Initial Styles and States...',2)        

        for v in self.vertices():
            self.v_fill_color[v] = GraphL.Colors['White']
            self.v_text_color[v] = GraphL.Colors['Black']
            self.v_halo[v] = False
            state.append('white')
            arrive.append(0)
            parent.append(-1)

        for e in self.edges():
            self.e_text[e] = ""

        self.repaint_Graph(graph_window, logger_window, 'Done',1)
        


        BFTree = GraphL()
        # BFT_v = BFTree.add_vertex()

        def loop(pv):

            print 'loop begin '+str(pv)
            self.repaint_Graph(graph_window, logger_window, 'Loop Begin with Vertex : ['+str(pv) +']',1)            
            

            self.v_fill_color[pv] = GraphL.Colors['Golden']
            arrive[int(pv)] = counter +1
            
            
            self.repaint_Graph(graph_window, logger_window, 'Adjacent Searching...for : ['+str(pv) +']',1)
            


            # if not pv.out_edges():
                # GLib.idle_add( self.render_wait_log, graph_window, logger_window, 'for ['+str(pv)+'] there are no out edges',2)
            

            self.repaint_Graph(graph_window, logger_window, 'here are out edges' + str([int(adj_v) for adj_v in pv.out_neighbours()]),2)
            



            for adj_e in pv.out_edges():
                self.repaint_Graph(graph_window, logger_window, 'inside for loop',2)                
                

                adj_v = adj_e.target()
                if state[int(adj_v)] == 'white': # to be considered for next interation
                    self.v_fill_color[adj_v] = GraphL.Colors['Grey']
                    self.v_halo[adj_v] = True
                    self.v_halo_color[adj_v] = GraphL.Colors['Golden']
                    self.e_dash_style[adj_e] = [.02,.02,.02,.02,.02,.02,.02]
                    self.e_color[adj_e] = GraphL.Colors['Dark_Green']
                    BFT_Queue.append(adj_v)

                    self.repaint_Graph(graph_window, logger_window, 'Got ['+str(adj_v)+']',2)
                    


                    self.v_halo[adj_v] = False 
                    self.e_dash_style[adj_e] = []
                    self.e_color[adj_e] = GraphL.Colors['Grey']
                    state[int(adj_v)] = 'grey'
                    parent[int(adj_v)] = pv
                    # BFTree.add_vertex()
                    # BFTree.add_edge(pv, adj_v)
                
                else:

                    self.v_fill_color[adj_v] = GraphL.Colors['Indian_Red']                    
                    self.e_dash_style[adj_e] = [.02,.02,.02,.02,.02,.02,.02]
                    self.e_color[adj_e] = GraphL.Colors['Indian_Red']
                    

                    if state[int(adj_v)] == 'grey':
                        self.repaint_Graph(graph_window, logger_window, 'The vertex ['+str(adj_v)+'] is already In Queue. => It is a side edge ',2)
                        

                        self.e_text[adj_e] = "Side Edge"
                        self.v_fill_color[adj_v] = GraphL.Colors['Grey']
                    else:
                        self.repaint_Graph(graph_window, logger_window, 'The vertex ['+str(adj_v)+'] is already in BFT Tree. => It is a Back edge. It also forms a cycle',2)
                        

                        self.e_text[adj_e] = "Back Edge"
                        self.v_fill_color[adj_v] = GraphL.Colors['Black']

                     
                    self.e_dash_style[adj_e] = [.02,.02,.02,.02,.02,.02,.02]
                    self.e_color[adj_e] = GraphL.Colors['Silver']
                    self.e_pen_width[adj_e] = 5-3;
                    self.repaint_Graph(graph_window, logger_window, 'Skipping this',1)
                    


            # if not pv.out_edges():
                # GLib.idle_add( self.render_wait_log, graph_window, logger_window, 'Adj loop is skipped',0)
            



            self.v_fill_color[pv] = GraphL.Colors['Black']
            self.v_text_color[pv] = GraphL.Colors['White']
            state[int(pv)] = 'black'

            self.repaint_Graph(graph_window, logger_window, 'Done with ['+str(pv)+'] vertex',2)
            


            if BFT_Queue: # checking for empty list
                
                v_next = BFT_Queue.pop()
                e_next = self.edge(parent[int(v_next)],v_next)
                
                self.e_color[e_next] = GraphL.Colors['Black']
                self.e_pen_width[e_next] = 5+2
                self.repaint_Graph(graph_window, logger_window, 'Black Coloring ['+str(e_next)+'] edge',2)
                

                loop(v_next)

        loop(root_vertex)

        print "Exiting BFT algo"
        return BFTree


# this is the input graph
g = GraphL()
g.make_Sample_2()

# If you have followed code until here, we have created vertices and edges and styles variables.
# To render the graph in a windows with defined properties, 
# 1. we require a layout (a method of arrenging the vertices ans edges)
# 2. and we will have to pass all these variables to graph window   

# both of the above requirements are covered in next two lines of code

# This is some automatic layout. Will see details later.
gLayout = sfdp_layout(g) 

# trick #1
# Here is the answer to last question:
# Make sure you know names of all internal properties from https://graph-tool.skewed.de/static/doc/draw.html
# Those names include "shape" "color" "fill_color" "size" "aspect"
# "rotation"... "halo" "halo_color"

# Now to say the vHaloColor is "halo_color". You define this mapping in the function below:
# append "vertex_" with "halo_color" and assign it equal to vHaloColor.
# Its done.

graph_window = GraphWindow(g, gLayout,
                       # The size of the vertex, in the default units of
                       # the output format (normally either pixels or
                           # points).
                       vertex_size=g.v_size,
                       # vertex_pen_width = 10,
                       vertex_halo=g.v_halo,  # to enable halos
                       # here 1.3 means, 1.3 times of single line, as I've
                       # observed using trials
                       vertex_halo_size=g.v_halo_size,
                       vertex_halo_color=g.v_halo_color,

                       vertex_fill_color=g.v_fill_color,

                       vertex_text=g.vertex_index,
                       vertex_text_color = g.v_text_color,

                       vertex_font_size=g.v_font_size,
                       vertex_font_family=g.v_font_family,

                       edge_color=g.e_color,
                       edge_pen_width=g.e_pen_width,

                       # Edge markers. Can be one of "none", "arrow",
                       # "circle", "square", "diamond", or "bar".
                       # Optionally, this might take a numeric value
                       # corresponding to position in the list above.
                       edge_end_marker=g.e_end_marker,
                       edge_marker_size = g.e_marker_size,

                       edge_dash_style =g.e_dash_style,

                       edge_text = g.e_text,
                       edge_font_size = g.e_font_size,
                       edge_font_family = g.e_font_family,
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
    global g
    # this when clicked with mouse left butten, returns |vertex| object to
    # |src|
    src = widget.picked
    
    # condition 1 & 2: No vertex is picked
    # Condition 3: same vertex is clicked/selected again 
    if src is not None and src is not False and src != button_press_event_function.last_picked:

        # I am keeping a pointer to last picked vertex
        # Here--last picked vertex color is changed to show that last selected vertex is not longer valid to start any algorithm  
        if button_press_event_function.last_picked :
            g.v_color[button_press_event_function.last_picked] = [0.6, 0.6, 0.6, 1]  

        # showing Yellow color for picked vertex
        g.v_color[src] = [0.807843137254902, 0.3607843137254902, 0.0, 1.0]
        
        # updating log
        logger_window.log_buffer.insert(logger_window.log_buffer.get_end_iter(), "> You've picked "+str(src)+" vertex\n")
        Log_Window.start_vertex = src

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
try:
    logger_window.show_all()
    graph_window.show_all()
    Gtk.main()
finally:
    Log_Window.t1.join()


