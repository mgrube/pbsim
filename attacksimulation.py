import networkx
import pynetsim

a = networkx.navigable_small_world_graph(1000, 4, 2, 1, 1).to_undirected()
pynetsim.randomize(a)
b = a.copy()
c = a.copy()

numattackers = 2
attackers = list()

pynetsim.pickmalnodes(a, attackers, 2)
pynetsim.attacksimulation(a, attackers)

for m in attackers:
	print m

locations = list()
for n in a.nodes():
	locations.append(n[0])

hist(locations, 100)
