'''
class SecondaryNode:
    def __init__(self,childs):
        self.childs=childs
        self.sum=sum(self.childs.number)

    def addParent(self,parent):
        self.parent=parent



class PrimaryNode:
    def __init__(self,number,parent=''):
        self.number=number
        self.parent=parent
'''
class Node:
    def __init__(self,sum):
        self.sum=sum

    def addParent(self,node):
        self.parent=node
