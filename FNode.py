from DataStore import DataStore
class FNode:
    ds = None
    recentlyrequested = list()
    
    def __init__(self, datastoresize):
        ds = DataStore(datastoresize)
        
    #We can use this for processing the request at each node
    def procReq(self, Request):
	print 'dicks'
