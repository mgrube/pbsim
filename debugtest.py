import networkx
import pynetsim

a = networkx.navigable_small_world_graph(1000, 4, 2, 1, 1).to_undirected()
pynetsim.randomize(a)

attackers = list()
pynetsim.pickmalnodes(a, attackers, 10)

pynetsim.attacksimulation(a, attackers)

