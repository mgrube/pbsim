#This is our request class. It can also act as a probe. 

class NodeMessage:
    type = ""
    visitednodes = list()
    HTL = 0
    key = float()
    value = float()
    payload = int()

    def __init__(self, rtype, HTL):
        self.HTL = HTL
        

    def setKey(self, keyval):
        self.key = keyval

    def setPayload(self, payloadsize):
        self.payload = payloadsize

    def 
