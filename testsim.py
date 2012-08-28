import networkx
import simutil
import random

g = networkx.navigable_small_world_graph(1000, 4, 2, 1, 1).to_undirected()
simutil.graphinit(g)
attackers = list()
simutil.pickmalnodes(g, attackers, 4)
simutil.sandbergsolution(g, attackers, .037)
