from DataStore import *

store = DataStore(1234)

store.insert(.5674, 1232)

print "Is bogus key in store?"
print store.keyReq(.4321)
print "Is legit key in store?"
print store.keyReq(.5674)
print "Inserting item of size 3. Old item should go."

store.insert(.8899, 3)

print "Is .5674 still in the store?"
print store.keyReq(.5674)
print "Is .8899 in the store?"
print store.keyReq(.8899)

store = DataStore(6)

print "Created new data store."

store.insert(.1, 1)
print "1"
#print str(store.usedspace())
store.insert(.2, 1)
print "2"
store.insert(.3, 1)
print "3"
#print str(store.usedspace())
#print str(store.storagelimit - store.usedspace())
store.insert(.4, 1)
print "4"
store.insert(.5, 2)

print "Inserted five items"
store.spaceclear()
print "cleared space"
print "Used space: " + str(store.usedspace())
store.keyReq(.1)
store.insert(.22, 3)

print "Keys available after insert:"
for k in store.datastore.keys():
	print str(k)
print "Data deleted: " + str(store.deleteddata)

