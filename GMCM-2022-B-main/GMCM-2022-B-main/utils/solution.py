
class solution:
    def __init__(self,M,data)-> None:
        self.bestfiness=len(M)
        self.bestlist =self.get_list(data)
        self.bins=M
    def get_list(self,data):
        List=[]
        for i in range(len(data)):
            item=data[i]
            List.append(item.idx)
        return List

