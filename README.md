<!-- Copyright 2017 Mohit Kumar Jangid. All rights reserved.
     Use of this source code is governed by a GPL-style license that can be found in the LICENSE file.
-->

Visualize Graph Algorithms
==========================

It is a python platform for visualizing all steps of a given graph algorithm operations. It's intended for graph algorithm learners.

The goal of this project is to provide the user an ability to configure (timing, layout, and styles of the graph etc) the visualization experience for a given graph and chosen graph algorithm. 


Prerequisite:
------------
The current version of the project uses python3. Main development is done on Linux OS based on Debian. So, install following python3 libraries in Linux-

1. [Graph-tool](https://graph-tool.skewed.de/)  --  This is the main library of for this project. See [Installation instructions](https://git.skewed.de/count0/graph-tool/wikis/installation-instructions).   
2. [Matplotlib](https://matplotlib.org/) -- See [installation instructions](https://matplotlib.org/users/installing.html).


Demo
----

![Run of a Breadth First Search Algorithm](https://github.com/mohitWrangler/visGraphAlgo/blob/master/Demo/Breadth%20First%20Search.gif)

Execution
------------------

The default run of the code shows the steps of Breadth-First Traversal of a sample graph.

	python3.5 visGraphAlgo.py  


Other Notes
-----------
- I have used Inconsolata-Regular fonts (source https://github.com/google/fonts/tree/master/ofl/inconsolata). I have included the fonts files in the project.
- Building blocks folder contains small programs. I learned individual component of the project using these program modules. To add a new feature, I usually test my code with these small modules and then I integrate the new code into the main code.    
