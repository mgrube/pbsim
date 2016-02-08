import random
import math
import networkx
import numpy
from DataStore import DataStore

number_of_swapping_tries = 1000

#This function takes a graph, a set of attackers as tuples and a 
#distance each node should be away from the others. 
def sandbergsolution(graph, attackers, distance, swapcalcfun=None):
    if swapcalcfun is None:
        swapcalcfun = defensiveswapcalc
    i = 0
    while i < number_of_swapping_tries:
        newattackers = list() 
        for a in attackers:
            newattackers.append(pbswap(graph, a, attackers))
        defensiveswapiteration(graph, attackers, distance, swapcalcfun)
        attackers = newattackers
        i += 1

#This inserts one object of size 1000 into each node in the network's 
#datastore. The use for this is to fill the network with data, which
#would amplify the effects of the pitch black attack
def networkdatainsert(g):
	for n in g.nodes(data=True):
		randloc = float(random.randint(2000, 10000))/1000000000
		keyloc = round(n[0][0], 3) + randloc
		n[1]['ds'].insert(keyloc, 1000)

#This function is for inserting a standard, default amount of
#niformation into the datastores on the network.
def initialdatainsert(g):
	for n in g.nodes(data=True):
		approxloc = round(n[0][0], 3)
		i = 0
		while i < 1000:
			approxloc += .00000001
			n[1]['ds'].insert(approxloc, 250)
			i += 1

#This function takes a graph to attack and a list of nodes who are attackers
#and carries out the Pitch Black attack.
def attacksimulation(graph, attackers):
    i = 0
    while i < number_of_swapping_tries:
        newattackers = list() 
        for a in attackers:
            newattackers.append(pbswap(graph, a, attackers))
        swapiteration(graph)
        attackers = newattackers
        i += 1

#Changes a node's location in the graph by the Node ID it is given.
#Newloc must be in tuple format
def changenodeloc(graph, nodeid, newloc):
    node = getbyID(graph, nodeid)
    neighbors = graph.neighbors(node[0])
    graph.add_node(newloc, id=node[1]['id'], ds=node[1]['ds'])
    for n in neighbors:
        graph.add_edge(newloc, n)
    graph.remove_node(node[0])

#Returns the location of a node after htl number of random hops from the originator
def randomwalk(originator, htl, graph):
	path = list()
	htl = 6
	current = originator
	while htl > 0:
		current = random.choice(graph.neighbors(current))
		htl -= 1
	if current == originator:
		return randomwalk(originator, htl, graph)
	else:
		return current

#Takes one node and replaces it with another, while mainatining
#all connections. This does not use node ID, but rather location.
def replacenode(graph, node, newnode):
    nodedict = dict()
    for n in graph.nodes(data=True):
        if n[0] == node:
             nodedict = n[1]
    neighbors = graph.neighbors(node)
    graph.add_node(newnode, id=nodedict['id'], ds=nodedict['ds'])
    #print "Replace - Node added: " + str(newnode)
    for n in neighbors:
        graph.add_edge(newnode, n)
    graph.remove_node(node)
    #print "Replace - Node removed: " + str(node)


#Swaps the location of two nodes based on location.
def locationswap(graph, node1, node2):
    neighbors1 = graph.neighbors(node1)
    neighbors2 = graph.neighbors(node2)
    dict1 = dict()
    dict2 = dict()
    for n in graph.nodes(data=True):
        if n[0] == node1:
            dict1 = n[1]
        elif n[0] == node2:
            dict2 = n[1]
    #Need to clean this segment up later
    graph.remove_node(node1)
    #print "Swap - Node removed: " + str(node1)
    graph.remove_node(node2)
    #print "Swap - Node removed: " + str(node2)
    graph.add_node(node1, id=dict2['id'], ds=dict2['ds'])
    #print "Swap - Node added: " + str(node1)
    graph.add_node(node2, id=dict1['id'], ds=dict1['ds'])
    #print "Swap - Node added: " + str(node2)
    #end segment to be cleaned
    for n in neighbors2:
        if n == node1:
            graph.add_edge(node1, node2)
        else:
            graph.add_edge(node1, n)
    for n in neighbors1:
        if n == node2:
            graph.add_edge(node1, node2)
        else:
            graph.add_edge(node2, n)

#Select some node in the network to be malicious
def pickmalnode(graph):
    node = random.choice(graph.nodes(data=True))
    bias = round(node[0][0], 4)
    return (node[1]['id'], bias)

#This is the malicious swap described by the Pitch Black paper
#The malicious node changes its own location to a set bias
#after swapping with a good node, replacing that good location with
#its own bias to swap during the next iteration. This is what
#causes the location clustering that prevents the network from
#storing a significant portion of the keyspace.
def pbswap(graph, maltuple, attackers):
    bias = round(float(maltuple[1]) + .0000000001, 10)
    print 'Bias: ' + str(bias)
    malid = maltuple[0]
    print 'Malicious Node ID: ' + str(malid)
    print 'Maltuple:' + str(maltuple)
    changenodeloc(graph, malid, (bias,))
    victim = randomwalk(getbyID(graph, malid)[0], 6, graph)
    for a in attackers:
        while a[0] == victim:
            neighbor = randomwalk(getbyID(graph, malid)[0], 6, graph)
    locationswap(graph, getbyID(graph, malid)[0], victim)
    return (malid, bias)

#Returns a node by its NodeID
def getbyID(graph, nodeid):
    node = None
    for n in graph.nodes(data=True):
        if n[1]['id'] == nodeid:
            node = n
    return node

#Returns a node by its location
def getbyLoc(graph, location):
    node = None
    for n in graph.nodes(data=True):
        if n[0] == location:
            node = n
    return node

#Assign random locations throughout the whole graph
def randomize(graph):
    i = 0
    for n in graph.nodes():
        i += 1
        randomloc = float(random.randint(0, 999999999))/1000000000
        newnode = (randomloc,)
        neighbors = graph.neighbors(n)
        graph.add_node(newnode, id=i, ds=DataStore(100000))
        for neighbor in neighbors:
            graph.add_edge(newnode, neighbor)
        graph.remove_node(n)

#This is important. This is Oskar Sandberg's original swapping calculation.
#This needs to be run number_of_swaps * N times to be effective.
def swap_calc(graph, node1, node2):
    d1 = float()
    d2 = float()
    d1 = 0.0
    d2 = 0.0
    node1neighbors  = graph.neighbors(node1)
    node2neighbors = graph.neighbors(node2)
    for n in node1neighbors:
        if n != node2:
            if d1 == 0.0:
                d1 = float(abs(node1[0] - n[0]))/1000
            else:
                d1 *= float(abs(node1[0] - n[0]))/1000

    for n in node2neighbors:
        if n != node1:
            d1 *= float(abs(node2[0] - n[0]))/1000
    #print "d1 value: " + str(d1)
    for n in node1neighbors:
        if n != node2:
            if d2 == 0.0:
                d2 = float(abs(node2[0] - n[0]))/1000
            else:
                d2 *= float(abs(node2[0] - n[0]))/1000
    for n in node2neighbors:
        if n != node1:
            d2 *= float(abs(node1[0] - n[0]))/1000
    #print "d2 value: " + str(d2)
    if d2 <= d1:
        #print "Doing a swap..."
        locationswap(graph, node1, node2)
    else:
        #print "Trying probabilisitc swap..."
        swapprob = d1/d2
        trial = float(random.randint(0, 1000))/1000
        if swapprob > trial:
            #print "Did probabilistic swap."
            locationswap(graph, node1, node2)

#Assign a set of malicious nodes
def pickmalnodes(graph, attackers, numattackers):
	for i in range(numattackers):
        	maltuple = pickmalnode(graph)
        	attackers.append((maltuple[0], maltuple[1]))
        	attackers.append((maltuple[0], round((maltuple[1] + .5) % 1, 5)))
                # only 2 locations per attacker to make this easier to see in small networks
        	# attackers.append((maltuple[0], round((maltuple[1] + .25) % 1, 5)))
        	# attackers.append((maltuple[0], round((maltuple[1] + .75) % 1, 5)))

#Defensively swaps the whole graph
def defensiveswapiteration(g, attackers, distance, swapcalcfun):
    for n in g.nodes(data=True):
        node1 = n
        node2 = randomwalk(n[0], 6, g)
        newloc = swapcalcfun(g, n[0], attackers, distance)
        if newloc is None:
            print "Didn't need to change. Doing Swap Calc."
            swap_calc(g, node1[0], node2)
        else:
            if n in attackers:
                print "Attack node will not defensively swap."
            else:
                changenodeloc(g, node1[1]['id'], newloc)
                print "Replaced " + str(n[0]) + " with " + str(newloc[0])

#Use Sandberg's Swapping algorithm once for the whole graph
def swapiteration(g):
    for n in g.nodes():
        node1 = n
        node2 = randomwalk(n, 6, g)
        swap_calc(g, node1, node2)
    print "Swap iteration complete."

#Use a swapping technique that takes pitch black into account
def defensiveswapcalc(graph, node, attackers, dist):
    if node not in attackers:
        randomloc = float(random.randint(0, 999999999))/1000000000
        randnode = (randomloc, )
        closestnode = closestnodequery(graph, node, randnode)
        print "Randomly chosen location: " + str(randnode)
        print "Closest found node: " + str(closestnode)
        neighbordistances = list()
        for n in graph.neighbors(node):
            neighbordistances.append(distance(node, n))
        _dist = abs(distance(randnode, closestnode) - numpy.mean(neighbordistances))
        # if the difference between the mean distance to my neighbors
        # and the closest found route to a random node is larger than dist,
        # take the random location.
        if _dist >= dist:
            print "Calculated distance relation", _dist, "is larger than dist", dist
            return randnode
        else:
            return None


#Use a swapping technique that takes pitch black into account
def defensiveswapcalcabsminusmean(graph, node, attackers, dist):
    if node not in attackers:
        randomloc = float(random.randint(0, 999999999))/1000000000
        randnode = (randomloc, )
        closestnode = closestnodequery(graph, node, randnode)
        print "Randomly chosen location: " + str(randnode)
        print "Closest found node: " + str(closestnode)
        neighbordistances = list()
        for n in graph.neighbors(node):
            neighbordistances.append(distance(node, n))
        _dist = distance(randnode, closestnode) - numpy.mean(neighbordistances)
        # if the difference between the mean distance to my neighbors
        # and the closest found route to a random node is larger than dist,
        # take the random location.
        if _dist >= dist:
            print "Calculated distance relation", _dist, "is larger than dist", dist
            return randnode
        else:
            return None


# Do two routing tries.
def defensiveswapcalcabsminusmean2(graph, node, attackers, dist):
    if node not in attackers:
        randdistnodes = []
        for i in range(2):
            randomloc = float(random.randint(0, 999999999))/1000000000
            randnode = (randomloc, )
            closestnode = closestnodequery(graph, node, randnode)
            print "Randomly chosen location: " + str(randnode)
            print "Closest found node: " + str(closestnode)
            randdistnodes.append((distance(randnode, closestnode), randnode))
        randdistnodes.sort()
        neighbordistances = list()
        for n in graph.neighbors(node):
            neighbordistances.append(distance(node, n))
        # compare the distance for best random node
        _dist = randdistnodes[0][0] - numpy.mean(neighbordistances)
        # if the difference between the mean distance to my neighbors
        # and the closest found route to a random node is larger than dist,
        # take the random location.
        if _dist >= dist:
            print "Calculated distance relation", _dist, "is larger than dist", dist
            # switch to the worst node to fill the most problematic part in the keyspace
            return randdistnodes[-1][1]
        else:
            return None


#Simpler swapping technique that takes pitch black into account
def defensiveswapcalcmedian(graph, node, attackers, dist):
    if node not in attackers:
        randomloc = float(random.randint(0, 999999999))/1000000000
        randnode = (randomloc, )
        closestnode = closestnodequery(graph, node, randnode)
        print "Randomly chosen location: " + str(randnode)
        print "Closest found node: " + str(closestnode)
        neighbordistances = list()
        for n in graph.neighbors(node):
            neighbordistances.append(distance(node, n))
        _dist = abs(distance(randnode, closestnode)) - numpy.median(neighbordistances)
        # if the difference between the mean distance to my neighbors
        # and the closest found route to a random node is larger than dist,
        # take the random location.
        if _dist >= dist:
            print "Calculated distance relation", _dist, "is larger than dist", dist
            return randnode
        else:
            return None

        
#Double median random test
def defensiveswapcalcmedian2(graph, node, attackers, dist):
    if node not in attackers:
        randdistnodes = []
        for i in range(2):
            randomloc = float(random.randint(0, 999999999))/1000000000
            randnode = (randomloc, )
            closestnode = closestnodequery(graph, node, randnode)
            print "Randomly chosen location: " + str(randnode)
            print "Closest found node: " + str(closestnode)
            randdistnodes.append((distance(randnode, closestnode), randnode))
        randdistnodes.sort()
        neighbordistances = list()
        for n in graph.neighbors(node):
            neighbordistances.append(distance(node, n))
        # compare the distance for best random node
        _dist = randdistnodes[0][0] - numpy.median(neighbordistances)
        # if the difference between the mean distance to my neighbors
        # and the closest found route to a random node is larger than dist,
        # take the random location.
        if _dist >= dist:
            print "Calculated distance relation", _dist, "is larger than dist", dist
            # switch to the worst node to fill the most problematic part in the keyspace
            return randdistnodes[-1][1]
        else:
            return None

        
#Quadruple median random test
def defensiveswapcalcmedian4(graph, node, attackers, dist):
    if node not in attackers:
        randdistnodes = []
        for i in range(4):
            randomloc = float(random.randint(0, 999999999))/1000000000
            randnode = (randomloc, )
            closestnode = closestnodequery(graph, node, randnode)
            print "Randomly chosen location: " + str(randnode)
            print "Closest found node: " + str(closestnode)
            randdistnodes.append((distance(randnode, closestnode), randnode))
        randdistnodes.sort()
        neighbordistances = list()
        for n in graph.neighbors(node):
            neighbordistances.append(distance(node, n))
        # compare the distance for best random node
        _dist = randdistnodes[0][0] - numpy.median(neighbordistances)
        # if the difference between the mean distance to my neighbors
        # and the closest found route to a random node is larger than dist,
        # take the random location.
        if _dist >= dist:
            print "Calculated distance relation", _dist, "is larger than dist", dist
            # switch to the worst node to fill the most problematic part in the keyspace
            return randdistnodes[-1][1]
        else:
            return None

        
#Return the closest node relative to a specific location
def closestnodequery(graph, startnode, desired):
    HTL = int(math.ceil(math.pow(math.log(len(graph.nodes()), 10), 2)))
    visitednodes = list()
    currentnode = startnode
    previousnode = None
    while HTL > 0:
        if len(visitednodes) >= 2:
            previousnode = visitednodes[len(visitednodes) - 2]
        currentnode = closestneighbor(graph, currentnode, desired, previousnode)
        visitednodes.append(currentnode)
        HTL -= 1
    mindistance = distance(visitednodes[0], desired)
    closestnode = None
    for n in visitednodes:
        if distance(n, desired) <= mindistance:
            mindistance = distance(n, desired)
            closestnode = n
    return closestnode

#Return the closest neighbor relative to a certain location.
#The previous node is passed to ensure that a node is not 
#Returned twice when crawling. 
def closestneighbor(graph, currentnode, desired, previous):
    neighbors = graph.neighbors(currentnode)
    distances = list()
    if previous != None:
        neighbors.remove(previous)
    for n in neighbors:
        distances.append(distance(n, desired))
    mindistance = min(distances)
    return neighbors[distances.index(mindistance)]

#Simple distance function
def distance(node1, node2):
    dist1 = abs(node1[0] - node2[0])
    dist2 = (node1[0] + node2[0])%1
    return min(dist1, dist2)
