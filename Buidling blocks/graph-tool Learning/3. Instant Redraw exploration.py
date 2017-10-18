import graph_tool.all as gt
from math import sqrt
import numpy as np

g = gt.price_network(1500)
deg = g.degree_property_map("in")
deg.a = 4 * (np.sqrt(deg.a) * 0.5 + 0.4)
ebet = gt.betweenness(g)[1]
ebet.a /= ebet.a.max() / 10.
eorder = ebet.copy()
eorder.a *= -1
pos = gt.sfdp_layout(g)
control = g.new_edge_property("vector<double>")
for e in g.edges():
    d = sqrt(sum((pos[e.source()].a - pos[e.target()].a) ** 2)) / 5
    control[e] = [0.3, d, 0.7, d]

gt.graph_draw(g, pos=pos, vertex_size=deg, vertex_fill_color=deg, vorder=deg,
              edge_color=ebet, eorder=eorder, edge_pen_width=ebet,
              edge_control_points=control # some curvy edges
              )



raw_input("Press Enter to Continue")

v_fill = [0.6, 0.6, 0.6, 1]
gt.graph_draw(g, pos=pos, vertex_size=deg, vertex_fill_color=v_fill, vorder=deg,
              edge_color=ebet, eorder=eorder, edge_pen_width=ebet,
              edge_control_points=control # some curvy edges
              )