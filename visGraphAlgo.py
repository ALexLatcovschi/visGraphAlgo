"""Most Important Links

Gtk All Classes
    All Classes : http://lazka.github.io/pgi-docs/Gtk-3.0/classes.html
    Gtk.Window  : http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Window.html
    Gtk.Widget  : http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Widget.html

Graph-Tools

    GraphWindow : https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.GraphWindow
                  Path is  graph_tool.draw.GraphWindow

    Graph Class : https://graph-tool.skewed.de/static/doc/graph_tool.html#graph_tool.Graph
                  https://graph-tool.skewed.de/static/doc/_modules/graph_tool.html#Graph
                  Path is graph_tool.Graph

    Gtk Window Events : https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html

    Quick Guide       : https://graph-tool.skewed.de/static/doc/quickstart.html

    graph's Internal Properties : https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.graph_draw
                                  Look for [Notes] section right after parameter and return details  

Threading
    https://wiki.gnome.org/Projects/PyGObject/Threading

Documentation style    : http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html 

"""

from graph_tool.all import *
from gi.repository import Gtk, GLib
import time
import threading


class GraphWindowL(GraphWindow):
    r"""

    GraphWindowL is child class of GraphWindow object from graph-tool 
            (https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.GraphWindow). 
    The leading --L--, in the class name, stand for Learners.
    It includes custom event trigger functions for GraphWindow suitalble for Learner's observation. 

    Interactive GTK+ window containing a :class:`~graph_tool.draw.GraphWidget`.

        Parameters
        ----------
        g : :class:`~graph_tool.Graph`
            Graph to be drawn.
        pos : :class:`~graph_tool.PropertyMap`
            Vector-valued vertex property map containing the x and y coordinates of
            the vertices.
        geometry : tuple
            Widget geometry.
        vprops : dict (optional, default: ``None``)
            Dictionary with the vertex properties. Individual properties may also be
            given via the ``vertex_<prop-name>`` parameters, where ``<prop-name>`` is
            the name of the property.
        eprops : dict (optional, default: ``None``)
            Dictionary with the edge properties. Individual properties may also be
            given via the ``edge_<prop-name>`` parameters, where ``<prop-name>`` is
            the name of the property.
        vorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
            If provided, defines the relative order in which the vertices are drawn.
        eorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
            If provided, defines the relative order in which the edges are drawn.
        nodesfirst : bool (optional, default: ``False``)
            If ``True``, the vertices are drawn first, otherwise the edges are.
        update_layout : bool (optional, default: ``True``)
            If ``True``, the layout will be updated dynamically.
        **kwargs
            Any extra parameters are passed to :class:`~graph_tool.draw.GraphWidget` and
            :func:`~graph_tool.draw.cairo_draw`.


    All Parameters are exactly as here: 
        https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.GraphWindow


    """

    def __init__(self, g, pos, geometry, vprops=None, eprops=None, vorder=None,
                 eorder=None, nodesfirst=False, update_layout=False, **kwargs):
        GraphWindow.__init__(self, g, pos, geometry, vprops, eprops, vorder,
                             eorder, nodesfirst, update_layout, **kwargs)

        self.graphL = g
            # the graph object inside this window can be accessed using this
            # variable

        self.graph.connect("motion-notify-event", self.motion_event_function)
        self.graph.connect("button-press-event",
                           self.button_press_event_function)
            # Handle Mouse Movement and Mouse/Keyboard button press Events
            #  see all events here
            #                https://graph-tool.skewed.de/static/doc/_modules/graph_tool/draw/gtk_draw.html

        self.graph.set_hexpand(True)
        self.graph.set_vexpand(True)
            # Allow windows to expand avialable vertical/horizonal screen space

        self.connect("delete_event", self.window_closer)
            # Allow closing the window.

        self.last_picked_vertex = None
            # last_picked_vertex {int} This keeps track of last picked vertex from Graph Window
            # This variable is used only in button_press_event_function

    def set_Position_and_Dimension(self, position_x=0, position_y=0, width=1, height=1):
        """Sets the position and dimension of the Graph Window

        The default size and positon of windows created by Gtk is often undersirable. 
        This function can also be used to set initial position and dimension

        Arguments:
            position_x {float} -- x cordinate of system's screen as a fraction of system screen width, 
                                    where the top-left corner of the graph windows is to be placed
            position_y {float} -- y cordinate of system's screen as a fraction of system screen height, 
                                    where the top-left corner of the graph windows is to be placed
            width      {float} -- fraction of the system's screen width to be occupied 
            height     {float} -- fraction of the system's screen height to be occupied 


        Example:  
            >>> Graph_WindowL_instance.set_Position_and_Dimension( .5, 0, .3, 1)

                 # Assuming Scree size = 800x200 (WidthxHeight).  
                 # This will set the window to the right half of the whole screen.
                 # The windows will have width = ScreenWidth * 0.3 and heigth = ScreenHeight*1 (full height)

        """

        self.move(self.get_screen().width() * position_x,
                  self.get_screen().height() * position_y)
            # Sets window position (This works by --moving-- the created window to required position)
            # graph_window.set_pointer(0,0) --this function does not work

        self.resize(self.get_screen().width()
                    * width, self.get_screen().height() * height)
            # Sets the Grapgh Window's dimension as per width and height

    def motion_event_function(self, widget, event):
        """This function is to handle any mouse movement over graph widget"""

        widget.selected.fa = False
            # for now, I am doing this to disable default mouse hover action,
            # that is--all closest edges are highlighted and the focused vertex is
            # highlighted with blue halo color   """

    def button_press_event_function(self, widget, event):
        """
        This function handles Keyboard Keys and Mouse buttons clicks on Graph Window.

        Parameters: 

        widget: It is the canvas on which the graph is drawn and 
                the button (Keyboard or Mouse) is pressed
        event:  event object

        this function is attached to Graph Window as an event triggered function. 
        (graph_window.graph.connect("button-press-event", button_press_event_function))   

        """

        src = widget.picked
            # widget.picked returns the |vertex| object which was clicked using
            # mouse

        if src is not None and src is not False and src != self.last_picked_vertex:
            # condition 1 & 2: No vertex is picked
            # Condition 3: same vertex is clicked/selected again

            if self.last_picked_vertex:
                self.graphL.v_color[self.last_picked_vertex] = [
                    0.6, 0.6, 0.6, 1]
                # I am keeping a pointer to last picked vertex (self.last_picked_vertex)
                # Here--last picked vertex color is changed to show that last selected
                #   vertex is longer valid to start any algorithm

            self.graphL.v_color[src] = [
                0.807843137254902, 0.3607843137254902, 0.0, 1.0]
                # showing Yellow color for picked vertex

            self.graphL.log.log_buffer.insert(self.graphL.log.log_buffer.get_end_iter(
            ), "> You've picked " + str(src) + " vertex\n")
                # updating log

            Log_Window.algorithm_start_vertex = src
                # Since log window spawns the algorithm procedure, it needs to know
                # the alorithm start vertex

            self.last_picked_vertex = src
                # setting current selection as last picked for next loop

            widget.picked = None
            widget.selected.fa = False
                # following is a workaround to, prevent default coloring of vertexes upon mouse clicks
                # Presently, I don't understand the ".fa" thing (see 2nd line
                # below), will see later

            widget.regenerate_surface()
            widget.queue_draw()
                # Changing colors requires the above 2 lines of code to come in
                # effect

    def window_closer(self, widget, event):
        """It is custom fuction called when used clicks on X mark on Graph Window.
           It is event handler function.widget

        This function deletes the windows to close it.
        This function is called by graph and logger windows
        using
          graph_window.connect("delete_event", window_closer)
          logger_window.connect("delete_event", window_closer)

        Arguments:
            widget {Gtk.Widget} -- The Widget/Window to be closed
            event {Gdk.Event} -- Close button click event
        """
        print('In the destroyer function')
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

    """

    algorithm_start_vertex = None

    def __init__(self, graph):

        Gtk.Window.__init__(self, title="Log Window")

        self.graph = graph
            # The connected graph can be access using self.graph

        self.connect("delete-event", Gtk.main_quit)
            # delete window handler

        self.set_size_request(self.get_screen().width()
                              * .1, self.get_screen().height() * .2)
            # Sets minimum size for Log Window

        self.set_Position_and_Dimension(.705, 0, .297, 1)
            # Setting size and position of window, see definition for syntax

        #--------------------BUIDLING BUTTONS, LOG AREA, ALGORITHM SECTIONS----

        #----Buttons-----#

        self.button_start_algo = Gtk.Button(label="Start Algo")
        self.button_start_algo.connect(
            "clicked", self.on_button_start_algo_clicked)

        self.button_reset_graph = Gtk.Button(label="Reset Graph")
        self.button_reset_graph.connect(
            "clicked", self.on_button_reset_graph_clicked)

        self.button_clear_log = Gtk.Button(label="Clear Log")
        self.button_clear_log.connect(
            "clicked", self.on_button_clear_log_clicked)

        #-----Log And Algorithm Tabs----#

        self.notebook = Gtk.Notebook()
            # Log Area and List of Algorithm is shown in tabs using Notebook class

        #------  Log Tab Text ----------#

        self.log_buffer = Gtk.TextBuffer()
        self.log_pad = Gtk.TextView(buffer=self.log_buffer)
            # text is a seperate buffer class

        self.log_pad.set_wrap_mode(Gtk.WrapMode.WORD)
            # wrap the text, if needed, breaking lines in between words
        self.log_pad.set_editable(False)
            # Log is only readable
        self.log_pad.set_cursor_visible(False)
            # Hiding cursor for read-only area

        #---Prepare Scrolling Functionality-------#

        self.scrolled_window = Gtk.ScrolledWindow()
            # a scrollbar for the child widget (that is going to be the textview)

        self.scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            # we scroll only if needed

        self.scrolled_window.connect("size-allocate", self.autoscroll_log_area)
            # Auto scroll to new text at the bottom

        self.scrolled_window.add(self.log_pad)
            # log pad is added inside scroller

        #------  Adding Tabs------------#

        self.notebook.append_page(self.scrolled_window, Gtk.Label('Log'))
            # First tab of Notebook

        self.page2 = Gtk.Box()
            # Adding second tab in Notebook

        info_label = Gtk.Label(
            'Implementation Pending. Switch to log tab to see what you can do for now.')
        self.page2.add(info_label)
        info_label.set_line_wrap(True)

        self.notebook.append_page(self.page2, Gtk.Label('Algorithms'))

        #------- Setting Notebook Parameters-----#

        self.notebook.set_vexpand(True)
        self.notebook.set_hexpand(True)
        # This is required so that the Notebook element streaches to occupy the remaning area
        # in the Log_window. Without the above code, the Notebooks will be shown in default size
        # only. If you did not understand this, try commenting these and
        # observe

        #----------------------BUTTONS AND NOTEBOOK ARE READY------------------

        #--- Its time for laying out the elements using Grid Layout
        # read more about layouts
        # http://python-gtk-3-tutorial.readthedocs.io/en/latest/layout.html

        grid = Gtk.Grid()

        grid.add(self.button_start_algo)
        grid.attach(self.button_reset_graph, 1, 0, 1, 1)
        grid.attach(self.button_clear_log, 2, 0, 1, 1)
        grid.attach_next_to(
            self.notebook, self.button_start_algo, Gtk.PositionType.BOTTOM, 10, 100)

        self.add(grid)
            # [attach] and [attach_next_to] functions have following syntax:

            # attach(child, col #, row #, width--col span, height--row span)
            # attach_next_to(child, sibling, side, width--col span, height--row
            #
            # The above functions adds the given object to Window as per grid
            # layout

        self.write("Welcome to Graph Learning Tool\n\n"
                   "Pick a vertex from the graph shown in the left, and press [Start Algo] button to run Breadth First Tree (BFT) Algorithm with choosen vertex as root vertex.")
            # Writing Intial text on log area

    def autoscroll_log_area(self, *args):
        """Autoscroll to botton of log area up to the last line 

        By default, the scroll does not move to show the newly added log in the log window.
        This function, as an event handler, autscroll to show up latest log text.


        Arguments:
            *args {list} -- All argument in one list. (For now there is no need to provide arguments,
                            hence this fucntion can be called without any parameter
        """
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_button_start_algo_clicked(self, widget):
        """It is called upon click of Start Algo Button in Log Window. 

        This function create a new thread for algorithm procedure. 
        The main process is Gtk.main loop (Google it for more) and the algorithm runs in different thread.

        Arguments:
            widget {Gtk.Widget} -- The widget on which the user clicked or interacted 
        """
        GraphL.algorithm_thread = threading.Thread(target=self.graph.show_BFT, args=(
            Log_Window.algorithm_start_vertex,))
            # Created a new thread and assigned the function (self.graph.show_BFT) which will run as a thread.
            # the args=(...) contains all the parameter required for the assigned
            # function.
        GraphL.algorithm_thread.daemon = True
            # This is recommended form of using thread along with gtk loop.
            # Read more here https://wiki.gnome.org/Projects/PyGObject/Threading
        GraphL.algorithm_thread.start()
            # Begin the algo. The assinged function thread runs starting from here.

    def on_button_reset_graph_clicked(self, widget):
        """This resets the graph to intial settings

        The implementation is still pending. 

        Arguments:
            widget {Gtk.Widget} -- The widget on which the user clicked or interacted 
        """
        self.write(
            "This functionality is yet to be implemented. Please close this logger windows and re-run the program to restart algorithm.")

    def on_button_clear_log_clicked(self, widget):
        """This is an event handler function. It clears the log text upon click on clear log
          button in the Log Window.

        Removes existing text in the log area of the Log Window. 

        Arguments:
            widget {Gtk.Widget} -- The widget on which the user clicked or interacted 
        """

        self.log_buffer.delete(
            self.log_buffer.get_start_iter(), self.log_buffer.get_end_iter())
            # this is thw way to modify, append and clear the log text, which is
            # stored in log_buffer object.

    def set_Position_and_Dimension(self, position_x=0, position_y=0, width=1, height=1):
        """Sets the position and dimension of the Log Window.

        The default size and positon of windows created by Gtk is often undersirable. 
        This function can also be used to set initial postion and dimension.

        Arguments:
            position_x {float} -- x cordinate of system's screen as a fraction of system screen width 
                                    where the top-left corner of the log windows is to be placed
            position_y {float} -- y cordinate of system's screen as a fraction of system screen height 
                                    where the top-left corner of the log windows is to be placed
            width {float} -- fraction of the system's screen width to be occupied 
            height {float} -- fraction of the system's screen height to be occupied 


        >>> Log_Window_instance.set_Position_and_Dimension( .5, 0, .3, 1)

                 # Assuming Scree size = 800x200 (WidthxHeight).  
                 # This will set the window to the right half of the whole screen.
                 # The windows will have width = ScreenWidth * 0.3 and heigth = ScreenHeight*1 (full height)
        """

        self.resize(self.get_screen().width()
                    * width, self.get_screen().height() * height)
            # Sets the Graph Window's dimension as per width and height
            # We can also use following function as well to resize.
            #   self.resize_to_geometry(self.get_screen().width()* width, self.get_screen().height() * height)
        time.sleep(.1)
            # Sometime the resize and move are not able to execute properly and in time.
            # the sleep delay fixes the issue if occurs.

        self.move(self.get_screen().width() * position_x,
                  self.get_screen().height() * position_y)
            # Sets window position (This works by --moving-- the created window to required position)
            # graph_window.set_pointer(0,0) --this function does not work

    def write(self, log_text):
        """for logging custom text to the Log Window

        This function can be used to write log text in log window.
        The log_text is written with "> " prefix

        Arguments:
            log_text {string} -- the text to be logged
        """
        self.log_buffer.insert(
            self.log_buffer.get_end_iter(), "> " + log_text + "\n")
            # log_buffer is the object which keeps the log text


class Color:
    """
    Color variables are available with this object as class Attributes.

    In each color attribute, the value are based on RGB code. Format is [Red, Green, Blue, Trasparancy]

    Normally, RGB color value ranges from 0-255, but here, specially for graph-tools, the values are 
    specified as fraction of 255. For example, an RGB value of <168,146,146> corresponds to gray color. 
    Now, for color variable here values will be [168/255 , 146/255, 146/255, 1  ]. 
    The last '1' is for color with NO TRANSPARENCY. A value '.5' will corresponds to 50% TRASNPARENCY 
    and so on.

    To use any color, just type--
    >>>Color.White
    >>>some_variable = Color.Black

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
    Graph object, which possesses all properties of a graph (Computer Science graph).
    This is class derived from graph_tool.Graph class (Links are at the very top) 

    To create a graph use following syntax.  

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
    >>> mygraph.add_sample_vertices_n_edges()

    Read more about graph (by graph-tools) https://graph-tool.skewed.de/static/doc/quickstart.html
    """

    def __init__(self, g=None, directed=True, prune=False, vorder=None):
        Graph.__init__(self, g, directed, prune, vorder)

        #---------- How to change graph's coloring, size, type, text and so on?

        # All internal properties are listed here:
        # https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.graph_draw

        # To use these properties, first create a variable which you can identify as the property
        # e.g. v_color (color of vertex ) or vHalocolor (color of halo of a vertex).
        # These variable aren't internal but user made. You can use any
        # variable name as you wish.

        # Now, How does graph-tools knows v_color is for Vertex's Colors or
        # vHaloColor is for Halo Color? OR How do these user made variable are going
        # to come in effect on graph?

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

    def set_default_essentials(self):
        """This function can be called to set
        1. default coloring/size/text font/halo color/vertices
             and Edges type and so on.
        2. default graph layout and configuration (Geometry, Order)
             As set by
             https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.GraphWindow
        3. attach log window, which shows all activities of
             graph operations

        This function should be called essentially to set
        default characterstics for a graph.
        """

        # Job No 1.
        # Setting vertex and edges style
        for v in self.vertices():
            self.v_fill_color[v] = Color.White
            self.v_halo_color[v] = Color.Saddle_Brown
            self.v_size[v] = 80
            self.v_text_color[v] = Color.Black
            self.v_halo[v] = True
            self.v_halo_size[v] = 1.3
            self.v_font_size[v] = 25
            self.v_font_family[v] = "Inconsolata-Regular"

        for e in self.edges():
            self.e_color[e] = Color.Gray
            self.e_dash_style[e] = []
            self.e_pen_width[e] = 5
            self.e_end_marker[e] = "arrow"
            self.e_marker_size[e] = 30
            # self.e_text[e] = "edge text"
            self.e_font_size[e] = 20
            self.e_font_family[e] = "Inconsolata-Regular"

        # Job No 2
        # Follow function definition to see how layout is created and added
        self.attach_Window_and_Canvas(
            
            vertex_size=self.v_size,
                # The size of the vertex, in the default units of 
                # the output format (normally either pixels or points).
            # vertex_pen_width = 10,
            vertex_halo=self.v_halo,  # to enable halos
                # here 1.3 (V_halo) means, 1.3 times of single line, as I've
                # observed using trials
            vertex_halo_size=self.v_halo_size,
            vertex_halo_color=self.v_halo_color,

            vertex_fill_color=self.v_fill_color,

            vertex_text=self.vertex_index,
            vertex_text_color=self.v_text_color,

            vertex_font_size=self.v_font_size,
            vertex_font_family=self.v_font_family,

            edge_color=self.e_color,
            edge_pen_width=self.e_pen_width,

            
            edge_end_marker=self.e_end_marker,
            edge_marker_size=self.e_marker_size,
                # Edge markers. Can be one of "none", "arrow",
                # "circle", "square", "diamond", or "bar".
                # Optionally, this might take a numeric value
                # corresponding to position in the list above.

            edge_dash_style=self.e_dash_style,

            edge_text=self.e_text,
            edge_font_size=self.e_font_size,
            edge_font_family=self.e_font_family,
                # vertex_halo_size = 0.0,  # this is temporary method to
                # remove halos, which are formed when a node is mouse
                # hovered
            geometry=(1000, 800))

        # Job No 3
        self.attach_log()

    def attach_Window_and_Canvas(self, geometry, layout=None, vprops=None, eprops=None, vorder=None,
                                 eorder=None, nodesfirst=False, update_layout=False, **kwargs):
        """This function attaches Window and Canvas to a graph. A Graph is drawn on a canvas
         which is placed inside a Window. The window and canavas are accessible through graph_instance.window
         and graph_instance.canvas attributes.

        graph_instance.window is equivalent to class graph_tool.draw.GraphWindow
        graph_instance.canvas is equivalent to  class graph_tool.draw.GraphWindow.graph
                    which is also equivalent to class graph_tool.draw.GraphWidget 
                    (I belive canvas is better word for the equivalent class)

        To know more see the class structure of graph-tools.                  

        Parameters
        ----------

        layout : :class:`~graph_tool.PropertyMap`
            Vector-valued vertex property map containing the x and y coordinates of
            the vertices.
        geometry : tuple
            Widget geometry.
        vprops : dict (optional, default: ``None``)
            Dictionary with the vertex properties. Individual properties may also be
            given via the ``vertex_<prop-name>`` parameters, where ``<prop-name>`` is
            the name of the property.
        eprops : dict (optional, default: ``None``)
            Dictionary with the edge properties. Individual properties may also be
            given via the ``edge_<prop-name>`` parameters, where ``<prop-name>`` is
            the name of the property.
        vorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
            If provided, defines the relative order in which the vertices are drawn.
        eorder : :class:`~graph_tool.PropertyMap` (optional, default: ``None``)
            If provided, defines the relative order in which the edges are drawn.
        nodesfirst : bool (optional, default: ``False``)
            If ``True``, the vertices are drawn first, otherwise the edges are.
        update_layout : bool (optional, default: ``True``)
            If ``True``, the layout will be updated dynamically.
        **kwargs
            Any extra parameters are passed to :class:`~graph_tool.draw.GraphWidget`
             and :func:`~graph_tool.draw.cairo_draw`.

        Returns:
            None
        """

        if not layout:
            layout = sfdp_layout(self)
            # This is some automatic layout. Read link below for more details
            # https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.sfdp_layout

        self.window = GraphWindowL(self, layout, geometry, vprops, eprops, vorder,
                                   eorder, nodesfirst, update_layout, **kwargs)
            # GraphWindowL function sets all configuration for a given graph
            # this is equivalent to GraphWindow class of graph-tool
            # (see links at the very top )

        self.window.set_Position_and_Dimension(0, 0, .7, 1)
        self.canvas = self.window.graph
            # serves better naming for RHS variable

    def attach_log(self):
        """Attaches a log window to provided graph object.

        Every graph have a log window where are activities are logged.
        Log Window is also responsible for controlling graph actions
        using some button availabe on it.
        """

        self.log = Log_Window(self)
            # Creating and connecting log window

    def make_Sample(self):
        """Creats a smple graph of 4 vertices and 4 edges.

        Use this function to create sample graph to quickly get started.
        """
        
        v1 = self.add_vertex()
        v2 = self.add_vertex()
        v3 = self.add_vertex()
        v4 = self.add_vertex()
        e1 = self.add_edge(v1, v2)
        e2 = self.add_edge(v2, v3)
        e3 = self.add_edge(v3, v1)
        e4 = self.add_edge(v3, v4)
            # the above lines of code creates a graph of 4 vertex and 4 edges

        # self.v_fill_color[0] = Color.Golden
        # self.v_fill_color[1] = Color.Midnight_Blue
        # self.v_fill_color[2] = Color.Indian_Red
        # self.v_fill_color[3] = Color.Dark_Orchid
            # Here are some sample style setting for the graph

    def add_sample_vertices_n_edges(self):
        """Creats a smple graph of 6 vertices and 6 edges.

        Use this function to create sample graph to quickly get started.
        """
        v1 = self.add_vertex()
        v2 = self.add_vertex()
        v3 = self.add_vertex()
        v4 = self.add_vertex()
        v5 = self.add_vertex()
        v6 = self.add_vertex()

        self.add_edge(v1, v2)
        self.add_edge(v1, v4)
        self.add_edge(v1, v3)

        self.add_edge(v4, v5)
        self.add_edge(v4, v6)
        self.add_edge(v4, v3)

        self.add_edge(v5, v1)
        self.add_edge(v5, v3)
            # above lines of code creates
            # a graph of 6 vertex and more then 6 edges

    def show_this(self, newWindow):
        newWindow.show_all()

    def repaint_Graph_and_Log(self, log_text='', seconds=1):
        GLib.idle_add(self.render_wait_log, log_text, 2)
        time.sleep(.1)
        # time.sleep(seconds)

    def render_wait_log(self, log_text='', seconds=1):

        self.canvas.regenerate_surface()
        self.canvas.queue_draw()

        self.log.write(log_text)

    def render_resize_wait_log(self, log_text='', seconds=1):

        self.canvas.fit_to_window(ink=True)
        self.canvas.queue_resize()

        self.canvas.regenerate_surface()
        self.canvas.queue_draw()

        self.log.write(log_text)
        # print log_text
        # time.sleep(seconds)

    def show_BFT(self, root_vertex=0):
        """Starts Breadth First Search Algorithm from given root_vertex index.

        This fucntion also shows steps of BFT algorithm as it progresses. The
        progress steps and other information are printed on log window.

        Keyword Arguments:
            root_vertex {number} -- source vertex index for BFT (default: {0})

        Returns:
            None
        """

        if root_vertex is None or \
           root_vertex < 0 or \
           root_vertex > (self.num_vertices() - 1):
            return None
                # Checking all valid requirement for root vertex

        state = []
        arrive = []
        counter = 0
        BFT_Queue = []
        parent = []
        v_Is_in_BFT = self.new_vertex_property("bool")
        e_Is_in_BFT = self.new_edge_property("bool")
            # Setting up initial variable essential for BFT

        self.log.write('Setting Initial Styles and States...')
            # simple logging message

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

        ##### the above lines of code sets initial state and 
            # parent values Including setting node's and edges'
            # visual style 
        
        self.repaint_Graph_and_Log('Done', 1)
            # renders the graph with intial setting 

        def loop(pv):
            """Main recursive loop for BFT algorithm. pv is current
            vertex getting processed.

            After intial processing of nodes and edges this loop is 
            the beginning of BFT main code.

            Arguments:
                pv {Vertex} -- a vertex object (class graph_tool.Vertex)
                               poitning to root vertex of BFT algorithm.


            """

            # print('loop begin ' + str(pv))
            self.log.write('Loop Begin with Vertex : ['+ str(pv) + ']')

            self.v_fill_color[pv] = Color.Golden
            arrive[int(pv)] = counter + 1
                # setting up color and arrive number for pivot vertex
                # the vertex of current consideration

            self.log.write('Adjacent Searching...for : [' + str(pv) + ']')

            # if not pv.out_edges():
            # GLib.idle_add( self.render_wait_log, self.window, self.log, 'for ['+str(pv)+'] there are no out edges',2)

            # self.repaint_Graph_and_Log('here are out edges' + str([int(adj_v) for adj_v in pv.out_neighbours()]),2)

            for adj_e in pv.out_edges():

                adj_v = adj_e.target()
                if state[int(adj_v)] == 'white':  # to be considered for next interaction
                    self.v_fill_color[adj_v] = Color.Gray
                        
                    self.v_halo[adj_v] = True
                    self.v_halo_color[adj_v] = Color.Golden
                    self.e_dash_style[
                        adj_e] = [.02, .02, .02, .02, .02, .02, .02]
                    self.e_color[adj_e] = Color.Golden
                        # above lines of code highlights the neighbor
                        # which is just discovered
                    BFT_Queue.append(adj_v)

                    self.repaint_Graph_and_Log('Got [' + str(adj_v) + ']', 2)
                        # render the discovered neighbor node    
                    self.v_halo[adj_v] = False
                    self.e_dash_style[adj_e] = []
                    self.e_color[adj_e] = Color.Gray
                        # above lines of code renders the neighbor
                        # node and edge based on tree or non tree
                        # edge

                    state[int(adj_v)] = 'gray'
                    parent[int(adj_v)] = pv
                        # state Gray for considered not processed yet
                        # parent is set to remember the BFT tree

                else:  # the target node is already visited

                    self.v_halo_color[adj_v] = Color.Indian_Red
                    self.e_dash_style[
                        adj_e] = [.02, .02, .02, .02, .02, .02, .02]
                    self.e_color[adj_e] = Color.Indian_Red
                        # Color setting for Non Tree edge and node

                    if state[int(adj_v)] == 'gray':
                        # condition for un-processed but under-consideration
                        # node i.e. the node is in the queue but BFT is not 
                        # done with that yet 
                        self.repaint_Graph_and_Log('The vertex [' + str(
                            adj_v) + '] is already In Queue. => not a BFT Edge ', 2)
                            # render the graph for non tree edge and node
                            # setting

                    else:  # condition for processed nodes                        
                        self.repaint_Graph_and_Log('The vertex [' + str(
                            adj_v) + '] is already in BFT Tree. => not a BFT Edge.', 2)
                        


                    self.e_text[adj_e] = "Non BFT"
                    self.e_color[adj_e] = Color.Gray
                    self.e_pen_width[adj_e] = 5 - 3
                    self.e_end_marker[adj_e] = "none"
                    self.v_halo[adj_v] = False
                    self.repaint_Graph_and_Log('Skipping this', 1)

                    e_Is_in_BFT[adj_e] = False

            # if not pv.out_edges():
                # GLib.idle_add( self.render_wait_log, self.window, self.log, 'Adj loop is skipped',0)

            self.v_fill_color[pv] = Color.Black
            self.v_text_color[pv] = Color.White
            state[int(pv)] = 'black'

            self.repaint_Graph_and_Log('Done with [' + str(pv) + '] vertex', 2)

            if BFT_Queue:  # checking for empty list

                v_next = BFT_Queue.pop()
                e_next = self.edge(parent[int(v_next)], v_next)

                self.e_color[e_next] = Color.Black
                self.e_pen_width[e_next] = 5 + 2
                self.repaint_Graph_and_Log(
                    'Black Coloring [' + str(e_next) + '] edge', 2)

                loop(v_next)

        loop(root_vertex)

        print("Exiting BFT algo")
        BFTree = GraphView(self, vfilt=v_Is_in_BFT, efilt=e_Is_in_BFT)

        # Tree layout --root at center---
        # https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.radial_tree_layout
        tree_layout = radial_tree_layout(BFTree, root_vertex)

        BFT_Tree_Window = GraphWindowL(BFTree, tree_layout,

                                       vertex_size=self.v_size,
                                       # The size of the vertex, in the
                                       # default units of the output format
                                       # (normally either pixels or points).
                                       # vertex_pen_width = 10,
                                       vertex_halo=self.v_halo,
                                       # to enable halos
                                       vertex_halo_size=self.v_halo_size,
                                       # here 1.3 means, 1.3 times of single
                                       # line, as I've observed using trials
                                       vertex_halo_color=self.v_halo_color,

                                       vertex_fill_color=self.v_fill_color,

                                       vertex_text=self.vertex_index,
                                       vertex_text_color=self.v_text_color,

                                       vertex_font_size=self.v_font_size,
                                       vertex_font_family=self.v_font_family,

                                       edge_color=self.e_color,
                                       edge_pen_width=self.e_pen_width,

                                       # Edge markers. Can be one of "none",
                                       # "arrow", "circle", "square",
                                       # "diamond", or "bar".
                                       # Optionally, this might take a
                                       # numeric value corresponding to
                                       # position in the list above.
                                       edge_end_marker=self.e_end_marker,
                                       edge_marker_size=self.e_marker_size,

                                       edge_dash_style=self.e_dash_style,

                                       edge_text=self.e_text,
                                       edge_font_size=self.e_font_size,
                                       edge_font_family=self.e_font_family,
                                       # vertex_halo_size = 0.0,
                                            # this is temporary method to
                                            # remove halos, which are formed
                                            # when a node is mouse hovered
                                       geometry=(1000, 800))

        BFT_Tree_Window.set_Position_and_Dimension(.5, 0, .5, 1)
        self.log.button_start_algo.disconnect_by_func(
            self.log.on_button_start_algo_clicked)
        self.window.graph.disconnect_by_func(
            self.window.button_press_event_function)
        self.window.set_Position_and_Dimension(0, 0, .5, .7)
        BFT_Tree_Window.graph.disconnect_by_func(
            BFT_Tree_Window.button_press_event_function)
        # self.window.hide()

        self.repaint_Graph_and_Log('Resizing Window', 2)

        GLib.idle_add(self.render_resize_wait_log, "Resizing Graph", 2)
        time.sleep(1)

        GLib.idle_add(self.show_this, BFT_Tree_Window)
        time.sleep(1)

        self.log.set_Position_and_Dimension(
            position_x=0, position_y=.8, width=.5, height=.2)

        self.log.write(
            "The algorithm is complete now.\n\n"

            "The above ^ graph is the same window you have been"
            " observing till now.\n"
            "The graph at > right side show the Breasth First Tree in"
            " Radial Tree layout (Google it to know more).\n\n"
            "You are free to explore (zoom in, zoom out, move, "
            "drag graphs) in both of the windows.\n"
            "Close this log window to exit the program. (and also if"
            " you want to run the algorithm with a new vertex)\n"

        )

        return BFTree

    def show(self):
        self.window.show_all()
        self.log.show_all()


# this is the input graph
g = GraphL()

g.add_sample_vertices_n_edges()
g.set_default_essentials()

# Time to show the windows, and start the GTK main loop.
try:
    g.show()
    Gtk.main()
finally:
    pass
    # GraphL.algorithm_thread.join()
