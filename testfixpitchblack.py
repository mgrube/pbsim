#!/usr/bin/env python

"""Testing the fix to the pitch black attack following Oskar Sandberg's fix.

Taken from thesnarks solution: https://emu.freenetproject.org/pipermail/devl/2013-January/036774.html
"""

from pynetsim import *
from networkx import *
from pylab import *
from DataStore import DataStore

networksize = 1000

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
sandberg_solution_network_median = random_network.copy()


f, axes = subplots(3, 2, sharex=True, sharey=True)
axes[2, 0].set_xlabel('max link length of the node')
axes[2, 1].set_xlabel('max link length of the node')
axes[0, 0].set_ylabel('number of nodes with this link length or less')
axes[1, 0].set_ylabel('number of nodes with this link length or less')
axes[2, 0].set_ylabel('number of nodes with this link length or less')


def showlinklength(net, ax):
    linklengths = [max([abs((e[0][0] - e[1][0])) for e in net.edges(n)]) for n in net.nodes()]
    ll_smallworld = [max([abs(e[0][0] - e[1][0]) for e in small_world_network.edges(n)]) for n in small_world_network.nodes()]
    ll_random = [max([abs(e[0][0] - e[1][0]) for e in random_network.edges(n)]) for n in random_network.nodes()]
    # hist([abs(e[0][0] - e[1][0]) for e in net.edges()], 100)
    ax.plot(sorted(linklengths), range(len(linklengths)), label="simulated")
    ax.plot(sorted(ll_smallworld), range(len(ll_smallworld)), label="kleinberg")
    ax.plot(sorted(ll_random), range(len(ll_random)), label="randomized")
    # ax.set_yscale('log')
    ax.set_xscale('log')
    ax.legend()
    # show()

ax = axes[0, 0]
ax.set_title("Clean Swapping Simulation")
for i in range(2000):
    swapiteration(clean_swap_network)
showlinklength(clean_swap_network, ax=ax)

attackers = list()
pickmalnodes(attacked_network, attackers, 2)  # We're picking 2 malicious nodes because that is the number chosen by the writers of the Pitch Black paper.


ax = axes[1, 0]
ax.set_title("Attacked Network")
attacksimulation(attacked_network, attackers) # We're using 2 nodes, each with 4 malicious locations.
showlinklength(attacked_network, ax)

ax = axes[0, 1]
ax.set_title("Attacked Network, defensive sandberg abs(route - mean)")
sandbergsolution(sandberg_solution_network, attackers, .037)
showlinklength(sandberg_solution_network, ax)

ax = axes[1, 1]
ax.set_title("Attacked Network, defensive sandberg abs(route) - mean")
sandbergsolution(sandberg_solution_network_minus, attackers, .037, swapcalcfun=defensiveswapcalcabsminusmean)
showlinklength(sandberg_solution_network_minus, ax)

ax = axes[2, 1]
ax.set_title("Attacked Network, defensive sandberg median")
sandbergsolution(sandberg_solution_network_median, attackers, .037, swapcalcfun=defensiveswapcalcmedian)
showlinklength(sandberg_solution_network_median, ax)

show()
