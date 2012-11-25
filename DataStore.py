class DataStore:
    storedkeys = dict()
    accesshistory = list()
    storagelimit = 0 #Units are Bytes
    storageused = 0
    deletedata = 0

    def __init__(self, limit):
        self.storagelimit = limit    

    #Inserts a key into the data store.
    #Content is removed on an LRU basis.
    #True on Success, False on Failure(file is bigger than data store)
    def insert(self, key, size):
        if self.storagelimit - self.storageused >= size:
            self.storageused += size
            self.storedkeys[str(key)] = size
            return True
        elif size > self.storagelimit:
            return False
        else:
            freedspace = 0
            while freedspace < size:
                #If no one has requested anything, remove the smallest file
                if len(self.accesshistory) == 0:
                    minsize = min(self.storedkeys.values())
                    for n in self.storedkeys.items():
                        if n[1] == minsize:
                            removeditem = n[0]
                else:
                    removeditem = self.accesshistory.pop(0)
                freedspace += self.storedkeys[str(removeditem)] #Get the size of least recently used key
                self.storedkeys.pop(str(removeditem))
                self.storedkeys[str(key)] = size
                self.storageused -= (freedspace - size)
                return True

    #Is the key in our store?
    def keyReq(self, key):
        try:
            size = self.storedkeys[str(key)]
            for k in self.accesshistory:
                if k == key:
                    self.accesshistory.pop(self.accesshistory.index(key))
            self.accesshistory.append(key)
            return True
        except KeyError:
            return False  

#    def initialdatainsert(self, ):
        
