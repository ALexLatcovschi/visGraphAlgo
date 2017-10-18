from graph_tool.all import *
from gi.repository import Gtk, GObject, GLib, Gdk
import sys
import time
import threading

#-----------------------------------------------------------------------------------

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
    if window_destroyer.destroy_count == 1:
        print 'Exiting Program'
        Gtk.main_quit()

# function are really objects. window_destroyer.destroy_count here acts as
# static variable
window_destroyer.destroy_count = 0

#----------------------------------------------------------------------------------------


class GraphWindowL(GraphWindow):
    """

    GraphWindowL is child class of GraphWindow object from graph-tool (https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.GraphWindow). The leading --L-- stand for Learners.
    It includes custom event trigger functions for GraphWindow suitalble for Learner's observation. 

    ---- Parameters-------------------------

     Exactly as here: https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.GraphWindow

    """
    last_picked_vertex = None
    def __init__(self, g, pos, geometry, vprops=None, eprops=None, vorder=None,
                 eorder=None, nodesfirst=False, update_layout=False, **kwargs):
        GraphWindow.__init__(self, g, pos, geometry, vprops, eprops, vorder,
                             eorder, nodesfirst, update_layout, **kwargs)
        # global window_destroyer
        self.graphL = g

        # just creating a better name for the Graph Widget placed inside this Graph Window
        # self.graph is used to deal with every kind of changes in the graph that it contains.
        # The changes include  vertex and edge coloring, resizing, zooming, moving , draging and so on.  
        self.grah_canvas = self.graph 

        # Binder for graph_window
        self.graph.connect("motion-notify-event", self.motion_event_function)
        
        """ Bind the function above as a motion notify handler, see all events
        here https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html
        """
        self.graph.connect("button-press-event", self.button_press_event_function)
        # again a static variable for button_press_event_function

        self.graph.set_hexpand(True)
        self.graph.set_vexpand(True)
        

        # We will give the user the ability to stop the program by closing the window.
        self.connect("delete_event", self.window_closer)

    def set_Position_and_Dimension(self, position_x=0, position_y=0, width=1 , height=1):
        """Sets the position and dimension of the Graph Window
        
        The default size and positon of windows created by Gtk is often undersirable. This function can also be used to set initial postion and dimension
        
        Arguments:
            position_x {float} -- x cordinate of system's screen as a fraction of system screen width where the top-left corner of the graph windows is to be placed
            position_y {float} -- y cordinate of system's screen as a fraction of system screen height where the top-left corner of the graph windows is to be placed
            width {float} -- fraction of the system's screen width to be occupied 
            height {float} -- fraction of the system's screen height to be occupied 

        
        Example:  
            >>> Graph_WindowL_instance.set_Position_and_Dimension( 400, 0, 0.5, 1)
                 # Assuming Scree size = (800 width,200 heigth).  This will set the window
                 to the right half of the whole screen.
        """

        # setting window position (This works by --moving-- the created window to required position)
        # graph_window.set_pointer(0,0) --does not work
        self.move(self.get_screen().width()*position_x,  self.get_screen().height()*position_y)

        # let us set the Grapg Window's dimension to as per width and height
        self.resize(self.get_screen().width()
                            * width, self.get_screen().height() * height)

    def motion_event_function(self, widget, event):
        """This function is to handle any mouse movement over graph widget"""

        """ for now, I am doing this to disable default mouse hover action,
        that is--all closest edges are highlighted and the focused vertex is
        highlighted with blue halo color   """
        widget.selected.fa = False

    def button_press_event_function(self, widget, event):
        """
        This function handles Keyboard Keys and Mouse buttons clicks in Graph Window.

        Parameters: 

        widget: the window's pointer on which a button (Keyboard or Mouse) is pressed
        event: event object

        It was attached to Graph Window as an event triggered function. 
        (graph_window.graph.connect("button-press-event", button_press_event_function))   

        """

        # this when clicked with mouse left butten, returns |vertex| object to
        # |src|
        src = widget.picked

        # condition 1 & 2: No vertex is picked
        # Condition 3: same vertex is clicked/selected again
        if src is not None and src is not False and src != GraphWindowL.last_picked_vertex:

            # I am keeping a pointer to last picked vertex
            # Here--last picked vertex color is changed to show that last selected
            # vertex is not longer valid to start any algorithm
            if GraphWindowL.last_picked_vertex:
                self.graphL.v_color[GraphWindowL.last_picked_vertex] = [
                    0.6, 0.6, 0.6, 1]

            # showing Yellow color for picked vertex
            self.graphL.v_color[src] = [0.807843137254902, 0.3607843137254902, 0.0, 1.0]

            # updating log
            logger_window.log_buffer.insert(logger_window.log_buffer.get_end_iter(
            ), "> You've picked " + str(src) + " vertex\n")
            Log_Window.algorithm_start_vertex = src

            # setting current selection as last picked for next loop
            GraphWindowL.last_picked_vertex = src

            # following is a workaround to, prevent default coloring of vertexes upon mouse clicks
            # Presently, I don't understand the ".fa" thing (see 2nd line below),
            # will see later
            widget.picked = None
            widget.selected.fa = False

            # Changing colors requires following 2 lines of code to come in effect
            widget.regenerate_surface()
            widget.queue_draw()

    def window_closer(self, widget, event):
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
        del self

       


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
    algorithm_start_vertex = None
    other_windows_for_reset = []
    main_graph_window= None
    def __init__(self):

        Gtk.Window.__init__(self, title="Log Window")
        self.connect("delete-event", window_destroyer)

        #----------------BASIC INFOMATION PRINTING ABOUT THE WINDOW------------

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

        #---------------------SETTING SIZE AND POSITION OF WINDOW--------------

        # Set width = 30% of Horizontal Length and Full Height
        # this function sets the size of window
        self.resize(self.get_screen().width() * .298,
                    self.get_screen().height())

        # setting window's position
        # self.set_pointer(0,0) --does not work
        self.move(self.get_screen().width() * .708, 0)

        #------------------------Buidling buttons, log area, algorithm sections

        #------------------------Buttons---------------------------------------
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

        #-----------------------Log and Algorithm lists------------------------

        # Log Area and List of Algorithm is shown in tabs using Notebook class
        self.notebook = Gtk.Notebook()

        # a scrollbar for the child widget (that is going to be the textview)
        self.scrolled_window = Gtk.ScrolledWindow()

        # we scroll only if needed
        self.scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.connect("size-allocate", self.autoscroll_log_area)

        self.log_buffer = Gtk.TextBuffer()
        self.log_pad = Gtk.TextView(buffer=self.log_buffer)

        # wrap the text, if needed, breaking lines in between words
        self.log_pad.set_wrap_mode(Gtk.WrapMode.WORD)
        self.log_pad.set_editable(False)  # Log is only readable
        # Hiding cursor for read-only area
        self.log_pad.set_cursor_visible(False)

        # textview is scrolled
        self.scrolled_window.add(self.log_pad)

        # First tab of Notebook
        self.notebook.append_page(self.scrolled_window, Gtk.Label('Log'))

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

        #----------------------Buttons and Notebook is ready-------------------
        #---------------------- Its time for laying out the elements using Grid

        grid = Gtk.Grid()

        # [attach] and [attach_next_to] functions have following syntax:

        # attach(child, col #, row #, width--col span, height--row span)
        # attach_next_to(child, sibling, side, width--col span, height--row
        # span)

        grid.add(self.button_start_algo)
        grid.attach(self.button_reset_graph, 1, 0, 1, 1)
        grid.attach(self.button_clear_log, 2, 0, 1, 1)
        grid.attach_next_to(
            self.notebook, self.button_start_algo, Gtk.PositionType.BOTTOM, 10, 100)

        self.add(grid)

    def autoscroll_log_area(self, *args):
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_button_start_algo_clicked(self, widget):
        global graph_window
        print("Hello")
        Log_Window.algorithm_thread = threading.Thread(target=g.show_BFS, args=(
            graph_window, self, Log_Window.algorithm_start_vertex,))
        Log_Window.daemon = True
        Log_Window.algorithm_thread.start()

    def on_button_reset_graph_clicked(self, widget):
        print("Goodbye")
        self.write("This functionality is yet to be implemented. Please close this logger windows and re-run the program to restart algorithm.")

    def on_button_clear_log_clicked(self, widget):
        print("Goodbye")
        self.log_buffer.delete(
            self.log_buffer.get_start_iter(), self.log_buffer.get_end_iter())

    def set_Position_and_Dimension(self, position_x=0, position_y=0, width=1 , height=1):
        """Sets the position and dimension of the Graph Window
        
        The default size and positon of windows created by Gtk is often undersirable. This function can also be used to set initial postion and dimension
        
        Arguments:
            position_x {float} -- x cordinate of system's screen as a fraction of system screen width where the top-left corner of the graph windows is to be placed
            position_y {float} -- y cordinate of system's screen as a fraction of system screen height where the top-left corner of the graph windows is to be placed
            width {float} -- fraction of the system's screen width to be occupied 
            height {float} -- fraction of the system's screen height to be occupied 

        
        Example:  
            >>> Graph_WindowL_instance.set_Position_and_Dimension( 400, 0, 0.5, 1)
                 # Assuming Scree size = (800 width,200 heigth).  This will set the window
                 to the right half of the whole screen.
        """

        # setting window position (This works by --moving-- the created window to required position)
        # graph_window.set_pointer(0,0) --does not work
        # self.set_gravity(Gdk.Gravity.SOUTH)
        # self.set_decorated(False)

        # self.set_vexpand(False)
        # self.set_hexpand(False)
        # let us set the Grapg Window's dimension to as per width and height
        self.resize(self.get_screen().width()
                            * width, self.get_screen().height() * height)
        time.sleep(.1)
        self.move(self.get_screen().width()*position_x, self.get_screen().height()* position_y)

    def write(self,log_text):
        """for logging custome text to the Log Window
        
        This function can be used to write log text in log window. The log_text is written with "> " prefix.self
        
        Arguments:
            log_text {string} -- the text to be logged
        """ 
        self.log_buffer.insert(
            self.log_buffer.get_end_iter(), "> " + log_text + "\n")

    def reset_algorithm_thread(self):

        for the_window in Log_Window.other_windows_for_reset:
            del the_window

        # main_graph_window.set_Position_and_Dimension()
        

        


class Color:
    """
    Color variables are available with this object as class Attributes.

    In each color value are based on RGB values. Format is [Red, Green, Blue, Trasparancy]

    Normally, RGB color value ranges from 0-255, but here values are specified as fraction of 255.
    For example, an RGB value of <168,146,146> corresponds to gray color. Now, for color variable here

    values will be [168/255 , 146/255, 146/255, 1  ]. The last '1' is for color with NO TRANSPARENCY. A value '.5' will corresponds to 50% TRASNPARENCY and so on.
    """
    White = [1., 1., 1., 1.]           # White color
    Black = [0., 0., 0., 1.]           # Black color
    Gray = [0.5, 0.5, 0.5, 1]    # Gray color
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
    Dark_Green = [0, 0.3922, 0, 1]
    Light_Steel_Blue = [0.6902, 0.7686, 0.0863, 1]
    Silver = [0.7529, 0.7529, 0.0745, 1]


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
    OR
    >>> mygraph.make_Sample_2()

    """

    def __init__(self, g=None, directed=True, prune=False, vorder=None):
        Graph.__init__(self, g, directed, prune, vorder)
        # How to change graph's coloring, size, type, text and so on? Read
        # below

        # All internal properties are listed here: https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.graph_draw
        # To use these properties, first create a variable which you can identify as the property e.g. v_color (color of vertex ) or vHalocolor (color of halo of a vertex).
        # These variable aren't internal but user made. Now how does graph knows v_color is for Vertex's Colors or
        # vHaloColor is for Halo Color?  wait...for trick #1. For, now keep
        # reading

        # The color property of the graph in graph-tool is of vector<double> type,
        # see all types of variable here
        # https://graph-tool.skewed.de/static/doc/graph_tool.html#graph_tool.PropertyMap
        # see all default styles and internal property types here:
        # https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/cairo_draw.html

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

        self.e_color = self.new_edge_property("vector<double>")
        self.e_pen_width = self.new_edge_property("double")
        self.e_start_marker = self.new_edge_property("int")
        self.e_mid_marker = self.new_edge_property("int")
        self.e_end_marker = self.new_edge_property("string")
        self.e_marker_size = self.new_edge_property("double")
        self.e_mid_marker_pos = self.new_edge_property("double")
        self.e_control_points = self.new_edge_property("vector<double>")
        self.e_gradient = self.new_edge_property("vector<double>")
        self.e_dash_style = self.new_edge_property("vector<double>")
        self.e_text = self.new_edge_property("string")
        self.e_text_color = self.new_edge_property("vector<double>")
        self.e_text_distance = self.new_edge_property("double")
        self.e_text_parallel = self.new_edge_property("bool")
        self.e_font_family = self.new_edge_property("string")
        self.e_font_slant = self.new_edge_property("int")
        self.e_font_weight = self.new_edge_property("int")
        self.e_font_size = self.new_edge_property("double")
        self.e_sloppy = self.new_edge_property("bool")
        self.e_seamless = self.new_edge_property("bool")

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

        self.v_fill_color[0] = Color.Golden
        self.v_fill_color[1] = Color.Midnight_Blue
        self.v_fill_color[2] = Color.Indian_Red
        self.v_fill_color[3] = Color.Dark_Orchid

        for v in self.vertices():
            self.v_halo_color[v] = Color.Saddle_Brown
            self.v_size[v] = 80
            self.v_text_color[v] = Color.Black
            self.v_halo[v] = True
            self.v_halo_size[v] = 1.3
            self.v_font_size[v] = 25
            self.v_font_family[v] = "Consolas"

        for e in self.edges():
            self.e_color[e] = Color.Gray
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

        # Setting vertex and edges style
        for v in self.vertices():
            self.v_fill_color[v] = Color.White
            self.v_halo_color[v] = Color.Saddle_Brown
            self.v_size[v] = 80
            self.v_text_color[v] = Color.Black
            self.v_halo[v] = True
            self.v_halo_size[v] = 1.3
            self.v_font_size[v] = 25
            self.v_font_family[v] = "Consolas"

        for e in self.edges():
            self.e_color[e] = Color.Gray
            self.e_dash_style[e] = []
            self.e_pen_width[e] = 5
            self.e_end_marker[e] = "arrow"
            self.e_marker_size[e] = 30
            self.e_text[e] = "edge text"
            self.e_font_size[e] = 20
            self.e_font_family[e] = "Consolas"

    def show_this(self,newWindow):
        newWindow.show_all()


    def repaint_Graph(self, graph_window, logger_window, log_text='', seconds=1):
        GLib.idle_add(self.render_wait_log, graph_window,
                      logger_window, log_text, 2)
        time.sleep(.02)
        # time.sleep(seconds)
        time.sleep(0)

    def render_wait_log(self, graph_window, logger_window, log_text='', seconds=1):
        graph_window.graph.regenerate_surface()
        graph_window.graph.queue_draw()      
        

        logger_window.write(log_text)

    def render_resize_wait_log(self, graph_window, logger_window, log_text='', seconds=1):
        graph_window.graph.fit_to_window(ink=True)
        graph_window.graph.queue_resize()
        graph_window.graph.regenerate_surface()
        graph_window.graph.queue_draw()     
        

        logger_window.write(log_text)
        # print log_text
        # time.sleep(seconds)

    def show_BFS(self, graph_window, logger_window, root_vertex=0):

        if root_vertex is None or root_vertex < 0 or root_vertex > (self.num_vertices() - 1):
            return None

        state = []
        arrive = []
        counter = 0
        BFT_Queue = []
        parent = []
        v_Is_in_BFT = self.new_vertex_property("bool")         
        e_Is_in_BFT = self.new_edge_property("bool")  

        self.repaint_Graph(graph_window, logger_window,
                           'Setting Initial Styles and States...', 2)

        for v in self.vertices():
            self.v_fill_color[v] = Color.White
            self.v_text_color[v] = Color.Black
            v_Is_in_BFT[v] = True

            self.v_halo[v] = False
            state.append('white')
            arrive.append(0)
            parent.append(-1)

        for e in self.edges():
            self.e_text[e] = ""
            self.e_dash_style[e] = []
            self.e_pen_width[e] = 5
            self.e_color[e] = Color.Gray
            e_Is_in_BFT[e] = True 

        self.repaint_Graph(graph_window, logger_window, 'Done', 1)

        def loop(pv):

            print 'loop begin ' + str(pv)
            self.repaint_Graph(graph_window, logger_window,
                               'Loop Begin with Vertex : [' + str(pv) + ']', 1)

            self.v_fill_color[pv] = Color.Golden
            arrive[int(pv)] = counter + 1

            self.repaint_Graph(graph_window, logger_window,
                               'Adjacent Searching...for : [' + str(pv) + ']', 1)

            # if not pv.out_edges():
            # GLib.idle_add( self.render_wait_log, graph_window, logger_window, 'for ['+str(pv)+'] there are no out edges',2)

            # self.repaint_Graph(graph_window, logger_window, 'here are out edges' + str([int(adj_v) for adj_v in pv.out_neighbours()]),2)

            for adj_e in pv.out_edges():
                # self.repaint_Graph(graph_window, logger_window, 'inside for loop',2)
                adj_v = adj_e.target()
                if state[int(adj_v)] == 'white':  # to be considered for next interation
                    self.v_fill_color[adj_v] = Color.Gray
                    self.v_halo[adj_v] = True
                    self.v_halo_color[adj_v] = Color.Golden
                    self.e_dash_style[
                        adj_e] = [.02, .02, .02, .02, .02, .02, .02]
                    self.e_color[adj_e] = Color.Golden
                    BFT_Queue.append(adj_v)

                    self.repaint_Graph(
                        graph_window, logger_window, 'Got [' + str(adj_v) + ']', 2)
                    self.v_halo[adj_v] = False
                    self.e_dash_style[adj_e] = []
                    self.e_color[adj_e] = Color.Gray
                    state[int(adj_v)] = 'gray'
                    parent[int(adj_v)] = pv
                    

                else:

                    self.v_halo_color[adj_v] = Color.Indian_Red
                    self.e_dash_style[
                        adj_e] = [.02, .02, .02, .02, .02, .02, .02]
                    self.e_color[adj_e] = Color.Indian_Red

                    if state[int(adj_v)] == 'gray':
                        self.repaint_Graph(graph_window, logger_window, 'The vertex [' + str(
                            adj_v) + '] is already In Queue. => not a BFT Edge ', 2)
                        self.v_fill_color[adj_v] = Color.Gray
                    else:
                        self.repaint_Graph(graph_window, logger_window, 'The vertex [' + str(
                            adj_v) + '] is already in BFT Tree. => not a BFT Edge.', 2)
                        self.v_fill_color[adj_v] = Color.Black

                    self.e_text[adj_e] = "Non BFT"
                    self.e_color[adj_e] = Color.Gray
                    self.e_pen_width[adj_e] = 5 - 3
                    self.e_end_marker[adj_e] = "none"
                    self.v_halo[adj_v] = False
                    self.repaint_Graph(
                        graph_window, logger_window, 'Skipping this', 1)

                    e_Is_in_BFT[adj_e] = False

            # if not pv.out_edges():
                # GLib.idle_add( self.render_wait_log, graph_window, logger_window, 'Adj loop is skipped',0)

            self.v_fill_color[pv] = Color.Black
            self.v_text_color[pv] = Color.White
            state[int(pv)] = 'black'

            self.repaint_Graph(graph_window, logger_window,
                               'Done with [' + str(pv) + '] vertex', 2)

            if BFT_Queue:  # checking for empty list

                v_next = BFT_Queue.pop()
                e_next = self.edge(parent[int(v_next)], v_next)

                self.e_color[e_next] = Color.Black
                self.e_pen_width[e_next] = 5 + 2
                self.repaint_Graph(graph_window, logger_window,
                                   'Black Coloring [' + str(e_next) + '] edge', 2)

                loop(v_next)

        loop(root_vertex)

        print "Exiting BFT algo"
        BFTree = GraphView(self, vfilt=v_Is_in_BFT, efilt = e_Is_in_BFT)

        # Tree layout --root at center--- https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.radial_tree_layout
        tree_layout = radial_tree_layout(BFTree, root_vertex)


        BFT_Tree_Window = GraphWindowL(BFTree, tree_layout,
                            # The size of the vertex, in the default units of
                            # the output format (normally either pixels or
                            # points).
                            vertex_size=self.v_size,
                            # # vertex_pen_width = 10,
                            vertex_halo=self.v_halo,  # to enable halos
                            # # here 1.3 means, 1.3 times of single line, as I've
                            # # observed using trials
                            vertex_halo_size=self.v_halo_size,
                            vertex_halo_color=self.v_halo_color,

                            vertex_fill_color=self.v_fill_color,

                            vertex_text=self.vertex_index,
                            vertex_text_color=self.v_text_color,

                            vertex_font_size=self.v_font_size,
                            vertex_font_family=self.v_font_family,

                            edge_color=self.e_color,
                            edge_pen_width=self.e_pen_width,

                            # # Edge markers. Can be one of "none", "arrow",
                            # # "circle", "square", "diamond", or "bar".
                            # # Optionally, this might take a numeric value
                            # # corresponding to position in the list above.
                            edge_end_marker=self.e_end_marker,
                            edge_marker_size=self.e_marker_size,

                            edge_dash_style=self.e_dash_style,

                            edge_text=self.e_text,
                            edge_font_size=self.e_font_size,
                            edge_font_family=self.e_font_family,
                            # vertex_halo_size = 0.0,  # this is temporary method to
                            # remove halos, which are formed when a node is mouse
                            # hovered
                            geometry=(1000, 800))

        
        BFT_Tree_Window.set_Position_and_Dimension(.5,0,.5,1)
        logger_window.button_start_algo.disconnect_by_func(logger_window.on_button_start_algo_clicked)
        graph_window.graph.disconnect_by_func(graph_window.button_press_event_function)      
        graph_window.set_Position_and_Dimension(0,0,.5,.7)
        BFT_Tree_Window.graph.disconnect_by_func(BFT_Tree_Window.button_press_event_function)         
        # graph_window.hide()

        self.repaint_Graph(graph_window, logger_window,
                               'Resizing Window', 2)

        GLib.idle_add(self.render_resize_wait_log, graph_window,
                      logger_window, "Resizing Graph", 2)
        time.sleep(1)


        GLib.idle_add(self.show_this, BFT_Tree_Window)
        time.sleep(1)

        
        logger_window.set_Position_and_Dimension(position_x=0, position_y=.8, width =.5, height =.2)


        logger_window.write(
                            """The algorithm is complete now.
                            The above ^ graph is the same window you have been observing till now.
                            The graph at > right side show the Breasth First Tree in Radial Tree layout (Google it to know more).

                            You are free to explore (zoom in, zoom out, move, drag graphs) in both of the windows.

                            Close this log window to exit the program.
                            Click on Reset Algo button to restart the the algorithm with new vertex."""
                            )
        
        logger_window.other_windows_for_reset.append(BFT_Tree_Window)
        logger_window.graph_window_for_reset = graph_window
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

graph_window = GraphWindowL(g, gLayout,
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
                            vertex_text_color=g.v_text_color,

                            vertex_font_size=g.v_font_size,
                            vertex_font_family=g.v_font_family,

                            edge_color=g.e_color,
                            edge_pen_width=g.e_pen_width,

                            # Edge markers. Can be one of "none", "arrow",
                            # "circle", "square", "diamond", or "bar".
                            # Optionally, this might take a numeric value
                            # corresponding to position in the list above.
                            edge_end_marker=g.e_end_marker,
                            edge_marker_size=g.e_marker_size,

                            edge_dash_style=g.e_dash_style,

                            edge_text=g.e_text,
                            edge_font_size=g.e_font_size,
                            edge_font_family=g.e_font_family,
                            # vertex_halo_size = 0.0,  # this is temporary method to
                            # remove halos, which are formed when a node is mouse
                            # hovered
                            
                            geometry=(400, 400))


graph_window.set_Position_and_Dimension(0,0,.7,1)
logger_window = Log_Window()
# logger_window.connect("delete-event", window_destroyer)


# Time to show the windows, and start the GTK main loop.
try:
    logger_window.show_all()
    graph_window.show_all()
    Gtk.main()
finally:
    Log_Window.algorithm_thread.join()
