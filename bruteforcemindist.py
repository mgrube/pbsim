#!/usr/bin/env python

"""Brute force calculation of the minimum distance to assume being attacked using only the number of peers and the HTL.

This currently ignores that in a real network there will only be a fixed number of locations equal to the size of the network.
"""

import random
import pylab as pl
import math

def dist(loc1, loc2):
    dist1 = abs(loc1 - loc2)
    dist2 = (loc1 + loc2)%1
    return min(dist1, dist2)

def random_dist(npeers, target):
  return min([dist(random.random(), target) for i in range(npeers)])

def oneroute(npeers, target, HTL=10):
    best = random_dist(npeers, target)
    maybebetter = random_dist(npeers, target)
    for i in range(HTL-1):
        if maybebetter > best:
           break
        best = maybebetter
        maybebetter = random_dist(npeers, target)
    return best

def trial(npeers, ntries):
  target = random.random()
  best = oneroute(npeers, target)
  maybebetter = oneroute(npeers, target)
  for i in range(ntries):
    maybebetter = oneroute(npeers, target)
    if maybebetter < best:
      best = maybebetter
  return best

npeers = 5
samples_per_try = 100
maxtries = 10000
tries = []
best_by_tries = []
for ntries in range(int(math.log(maxtries, 2))):
    for i in range(samples_per_try):
        tries.append(2**ntries)
        best_by_tries.append(trial(npeers, int(2**ntries)))
pl.plot(tries, best_by_tries, "+")
pl.xscale('log')
pl.show()
