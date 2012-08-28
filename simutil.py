import random
import math
import networkx        
from DataStore import DataStore
from FNode import FNode

def sandbergsolution(graph, attackers, distance):
    i = 0
    while i < 2000:
        newattackers = list() 
        for a in attackers:
            newattackers.append(pbswap(graph, a, attackers))
        defensiveswapiteration(graph, attackers, distance)
        attackers = newattackers
        i += 1

def initialdatainsert(graph):
    for n in graph.nodes(data=True):
        i = 0
        approxloc = round(n[0][0], 6)
        while i < 250:
            approxloc += .000000000001
            n[1]['ds'].insert(approxloc, 100)
            i += 1

def attacksimulation(graph, attackers):
    i = 0
    while i < 2000:
        newattackers = list() 
        for a in attackers:
            newattackers.append(pbswap(graph, a, attackers))
        swapiteration(graph)
        attackers = newattackers
        i += 1   

#Newloc must be in tuple format
def changenodeloc(graph, nodeid, newloc):
    node = getbyID(graph, nodeid)
    neighbors = graph.neighbors(node[0])
    graph.add_node(newloc, id=node[1]['id'], ds=node[1]['ds'])
    for n in neighbors:
        graph.add_edge(newloc, n)
    graph.remove_node(node[0])

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

#def DFS(graph, node, nodelist):
#    nodelist.append(node)
#    for n in set(graph.neighbors(node)).differences(set(nodelist)):

#Startnode and key MUST be passed as tuples.
def getRequest(graph, startnode, key):
    htl = int(round(math.pow(math.log(1000, 10), 2)))
    visited = list()
    currentnode = getbyLoc(graph, startnode)
    visited.append(currentnode[0])
    previous = None
    #visited.append(None)
    mindistance = distance(currentnode[0], key)
    while htl > 0:
        if currentnode[1]['ds'].keyReq(key[0]) > 0:
            htl = 0
        else:
            nextnode = cn(graph, currentnode[0], key, visited)
            currentnode = getbyLoc(graph, nextnode)
            print "Next node: " + str(nextnode)
            if distance(currentnode[0], key) < mindistance:
                print "Node switched. Current node: " + str(currentnode)
                mindistance = distance(currentnode[0], key)
                htl = int(round(math.pow(math.log(1000, 10), 2)))
            else:
                htl -= 1
        visited.append(currentnode[0])
    return visited


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

def pickmalnode(graph):
    node = random.choice(graph.nodes(data=True))
    bias = round(node[0][0], 2)
    return (node[1]['id'], bias)

def pbswap(graph, maltuple, attackers):
    bias = round(float(maltuple[1]) + .0000000001, 10)
    malid = maltuple[0]
    changenodeloc(graph, malid, (bias,))
    neighbor = random.choice(graph.neighbors(getbyID(graph, malid)[0]))
    for a in attackers:
        while a[0] == neighbor:
            neighbor = random.choice(graph.neighbors(getbyID(graph, malid)[0]))
    locationswap(graph, getbyID(graph, malid)[0], neighbor)
    return (malid, bias)

def getbyID(graph, nodeid):
    node = None
    for n in graph.nodes(data=True):
        if n[1]['id'] == nodeid:
            node = n
    return node

#Pass this function the node's locaiton in tuple format
def getbyLoc(graph, location):
    node = None
    for n in graph.nodes(data=True):
        if n[0] == location:
            node = n
    return node

#Assigns random locations to the NetworkX Graph and Adds FNodes as attributes
#Each node has a default data store size of 10000 bytes
def graphinit(graph):
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

#Randomly pick nodes as attackers with their location and 3 other evenly spaced
#Locations as their biases
def pickmalnodes(graph, attackers, numattackers):
	i = 0
	while i < numattackers:
        	maltuple = pickmalnode(graph)
        	attackers.append((maltuple[0], maltuple[1]))
        	attackers.append((maltuple[0], round((maltuple[1] + .5) % 1, 3)))
        	attackers.append((maltuple[0], round((maltuple[1] + .25) % 1, 3)))
        	attackers.append((maltuple[0], round((maltuple[1] + .75) % 1, 3)))
		i += 1

def greedysearch(graph, node1, node2):
    currentnode = node1
    visited = list()
    visited.append(node1)
    while currentnode != node2:
        currentnode = cn(graph, currentnode, node2, visited)
        visited.append(currentnode)
    return visited


def defensiveswapiteration(g, attackers, distance):
    for n in g.nodes(data=True):
        node1 = n
        node2 = random.choice(g.neighbors(n[0]))
        newloc = defensiveswapcalc(g, n[0], attackers, distance)
        if newloc == None:
            print "Didn't need to change. Doing Swap Calc."
            swap_calc(g, node1[0], node2)
        else:
            if n in attackers:
                print "Attack node will not defensively swap." 
            else:
                changenodeloc(g, node1[1]['id'], newloc)
                print "Replaced " + str(n) + " with " + str(newloc)

def swapiteration(g):
    for n in g.nodes():
        node1 = n
        node2 = random.choice(g.neighbors(n))
        swap_calc(g, node1, node2)
    print "Swap iteration complete."

def defensiveswapcalc(graph, node, attackers, dist):
    if node not in attackers:
        randomloc = float(random.randint(0, 999999999))/1000000000
        randnode = (randomloc, )
        closestnode = closestnodequery(graph, node, randnode, attackers)
        print "Randomly chosen location: " + str(randnode)
        print "Closest found node: " + str(closestnode)
        if distance(randnode, closestnode) >= dist:
            return randnode
        else:
            return None

def cn(graph, currentnode, endnode, visited):
    neighbors = graph.neighbors(currentnode) 
    mindistance = distance(random.choice(list(neighbors)), endnode)
    closest = None
    for n in neighbors:
        if distance(n, endnode) <= mindistance:
            mindistance = distance(n, endnode)
            closest = n
    return closest

def closestnodequery(graph, startnode, desired, attackers):
    HTL = int(math.ceil(math.pow(math.log(len(graph.nodes()), 10), 2)))
    visitednodes = list()
    currentnode = startnode
    previousnode = None
    attacknodes = set()
    visitednodes.append(currentnode)
    for a in attackers:
        attacknodes.add(getbyLoc(graph, a[0]))
    while HTL > 0:
        currentnode = cn(graph, currentnode, desired, visitednodes)
        if currentnode in attackers:
            currentnode = desired
            HTL = 0
        else:
            HTL -= 1
        visitednodes.append(currentnode)
    mindistance = distance(visitednodes[0], desired)
    closestnode = None
    for n in visitednodes:
        if distance(n, desired) <= mindistance:
            mindistance = distance(n, desired)
            closestnode = n
    return closestnode

def distance(node1, node2):
    return abs(node1[0] - node2[0])
