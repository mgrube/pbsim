import networkx
import netsimtest

a = networkx.navigable_small_world_graph(1000, 4, 2, 1, 1).to_undirected()
netsimtest.randomize(a)
b = a.copy()
c = a.copy()

numattackers = 2
attackers = list()

netsimtest.pickmalnodes(a, attackers, 2)
netsimtest.attacksimulation(a, attackers)

for m in attackers:
	print m

locations = list()
for n in a.nodes():
	locations.append(n[0])

hist(locations, 100)
