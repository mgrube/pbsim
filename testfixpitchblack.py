#!/usr/bin/env python

"""Testing the fix to the pitch black attack following Oskar Sandberg's fix.

Taken from thesnarks solution: https://emu.freenetproject.org/pipermail/devl/2013-January/036774.html
"""

from pynetsim import *
from networkx import *
from pylab import *
random_network = navigable_small_world_graph(1000, 4, 2, 1, 1).to_undirected()

randomize(random_network)

clean_swap_network = random_network.copy()
attacked_network = random_network.copy()
sandberg_solution_network = random_network.copy()

for i in range(2000):
    swapiteration(clean_swap_network)

def showlinklength(net):
    linklengths = list()
    for e in net.edges():
        linklengths.append(abs(e[0][0] - e[1][0]))
    hist(linklengths, 100)
    show()

showlinklength(clean_swap_network)

attackers = list()
pickmalnodes(attacked_network, attackers, 2)  # We're picking 2 malicious nodes because that is the number chosen by the writers of the Pitch Black paper.
attacksimulation(attacked_network, attackers) # We're using 2 nodes, each with 4 malicious locations.

showlinklength(attacked_network)

sandbergsolution(sandberg_solution_network, attackers, .037)

showlinklength(sandberg_solution_network)
