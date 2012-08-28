class DataStore:

    def __init__(self, limit):
        self.storagelimit = limit
        self.datastore = {}
        self.deleteddata = 0
        self.accesshistory = []    

    def usedspace(self):
        used = 0
        for v in self.datastore.values():
            used += v
        return used

    #Inserts a key into the data store.
    #Content is removed on an LRU basis.
    #True on Success, False on Failure(file is bigger than data store)
    def insert(self, key, size):
        while self.storagelimit - self.usedspace() < size:
            self.spaceclear()
        self.datastore[str(key)] = size

    #This function will remove either:
    #The least recently used item, if one exists
    #The item taking the most space
    def spaceclear(self):
        if len(self.accesshistory) > 0:
            key = self.accesshistory.pop(0)
            size = self.datastore.pop(str(key))
            self.deleteddata += size
            return True
        elif len(self.datastore) > 0:
            maxval = max(self.datastore.values())
            size = self.datastore.pop(self.datastore.keys()[self.datastore.values().index(maxval)])
            self.deleteddata += size

    #Is the key in our store?
    #If so, add key to accesshistory
    def keyReq(self, key):
        try:
            size = self.datastore[str(key)]
            while key in self.accesshistory:
                 self.accesshistory.remove(key)
            self.accesshistory.append(key)
            return size
        except KeyError:
            return -1
