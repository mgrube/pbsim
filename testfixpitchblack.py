#!/usr/bin/env python

"""Testing the fix to the pitch black attack following Oskar Sandberg's fix.

Taken from thesnarks solution: https://emu.freenetproject.org/pipermail/devl/2013-January/036774.html
"""

import pynetsim
from pynetsim import *
from networkx import *
from pylab import *
from DataStore import DataStore

networksize = 400

#: mean plus two sigma probability of the distance to a random node when routing through a random network with 5 peers per node
m2s = .037
#: rough mean plus two sigma deviation for two tries (via bruteforcemindist.py)
m2s2 = .022
#: rough median plus twosigma deviation for two tries (via bruteforcemindist.py)
medtwosigma2 = 0.02
#: rough median plus twosigma deviation for four tries (via bruteforcemindist.py)
medtwosigma4 = 0.0125

small_world_network = navigable_small_world_graph(networksize, 4, 2, 1, 1).to_undirected()

# change the locations to be [0..1).
g = small_world_network
for n in g.nodes()[:]:
    newnode = (float(n[0]) / networksize,)
    neighbors = g.neighbors(n)
    g.add_node(newnode, id=n[0], ds=DataStore(100000))
    for neighbor in neighbors:
        g.add_edge(newnode, neighbor)
    g.remove_node(n)

random_network = navigable_small_world_graph(networksize, 4, 2, 1, 1).to_undirected()

randomize(random_network)

clean_swap_network = random_network.copy()
attacked_network = random_network.copy()
sandberg_solution_network = random_network.copy()
sandberg_solution_network_minus = random_network.copy()
sandberg_solution_network_mean2 = random_network.copy()
sandberg_solution_network_median = random_network.copy()
sandberg_solution_network_median2 = random_network.copy()
sandberg_solution_network_median4 = random_network.copy()


f, axes = subplots(3, 2, sharex=True, sharey=True)
# link lengths
axes[2, 0].set_xlabel('max link length of the node')
axes[2, 1].set_xlabel('max link length of the node')
# axes[0, 0].set_ylabel('number of nodes with this link length or less')
axes[1, 0].set_ylabel('number of nodes with this link length or less')
# axes[2, 0].set_ylabel('number of nodes with this link length or less')

def showlinklength(net, ax):
    linklengths = [max([abs((e[0][0] - e[1][0])) for e in net.edges(n)]) for n in net.nodes()]
    ll_smallworld = [max([abs(e[0][0] - e[1][0]) for e in small_world_network.edges(n)]) for n in small_world_network.nodes()]
    ll_random = [max([abs(e[0][0] - e[1][0]) for e in random_network.edges(n)]) for n in random_network.nodes()]
    ax.plot(sorted(linklengths), range(len(linklengths)), label="simulated")
    ax.plot(sorted(ll_smallworld), range(len(ll_smallworld)), label="kleinberg")
    ax.plot(sorted(ll_random), range(len(ll_random)), label="randomized")
    # ax.set_yscale('log')
    ax.set_xscale('log')
    ax.legend(loc='upper left')

ax = axes[0, 0]
ax.set_title("Clean Swapping Simulation")
for i in range(pynetsim.number_of_swapping_tries):
    swapiteration(clean_swap_network)
showlinklength(clean_swap_network, ax=ax)

attackers = list()
pickmalnodes(attacked_network, attackers, 2)  # We're picking 2 malicious nodes because that is the number chosen by the writers of the Pitch Black paper.


ax = axes[0, 1]
ax.set_title("Attacked Network")
attacksimulation(attacked_network, attackers) # We're using 2 nodes, each with 4 malicious locations.
showlinklength(attacked_network, ax)

ax = axes[1, 0]
ax.set_title("Sandberg abs(route) - mean")
sandbergsolution(sandberg_solution_network_minus, attackers, m2s, swapcalcfun=defensiveswapcalcabsminusmean)
showlinklength(sandberg_solution_network_minus, ax)

ax = axes[1, 1]
ax.set_title("Attacked, sandberg abs(route) - median")
sandbergsolution(sandberg_solution_network_median, attackers, m2s, swapcalcfun=defensiveswapcalcmedian)
showlinklength(sandberg_solution_network_median, ax)

ax = axes[2, 0]
ax.set_title("Attacked, sandberg abs(route) - mean2")
sandbergsolution(sandberg_solution_network_mean2, attackers, m2s2, swapcalcfun=defensiveswapcalcabsminusmean2)
showlinklength(sandberg_solution_network_mean2, ax)

ax = axes[2, 1]
ax.set_title("Attacked, sandberg abs(route) - median2")
sandbergsolution(sandberg_solution_network_median2, attackers, medtwosigma2, swapcalcfun=defensiveswapcalcmedian2)
showlinklength(sandberg_solution_network_median2, ax)


savefig("fix-pitch-black-{}-mean-median-median2-peerdist.png".format(networksize), dpi=300, bbox_inches='tight', transparent=True)

# histograms
f, axes = subplots(2, 2, sharex=True, sharey=True)
axes[0, 0].set_ylabel('nodes in the bin')
axes[1, 0].set_ylabel('nodes in the bin')
axes[1, 0].set_xlabel('node positions')
axes[1, 1].set_xlabel('node positions')


# ax = axes[0, 0]
# ax.set_title("Clean swapping network")
# ax.hist([n[0] for n in clean_swap_network.nodes()], 100)

ax = axes[0, 0]
ax.set_title("attacked vs. mean fix")
ax.hist([n[0] for n in sandberg_solution_network_minus.nodes()], 100, label="mean")
ax.hist([n[0] for n in attacked_network.nodes()], 100, label="attacked")
ax.legend()

ax = axes[1, 1]
ax.set_title("defensive median2 swapping")
ax.hist([n[0] for n in sandberg_solution_network_median2.nodes()], 100)

ax = axes[0, 1]
ax.set_title("defensive median swapping")
ax.hist([n[0] for n in sandberg_solution_network_median.nodes()], 100)

ax = axes[1, 0]
ax.set_title("defensive mean2 swapping")
ax.hist([n[0] for n in sandberg_solution_network_mean2.nodes()], 100)

savefig("fix-pitch-black-{}-mean-median-median2-lochist.png".format(networksize), dpi=300, bbox_inches='tight', transparent=True)
