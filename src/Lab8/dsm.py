from mpi4py import MPI

class DSM:
    def __init__(self):
        self.vars={}
        self.vars['a']=[[],1]
        self.vars['b']=[[],2]
        self.vars['c']=[[],'mere']

    def subscribe(self,var,subscriber):
        self.vars[var][0].append(subscriber)
        comm=MPI.COMM_WORLD
        for i in range(0,comm.Get_size()):
            if i!=comm.Get_rank():
                comm.send([var,subscriber,'update subscribers'],dest=i)

    def updateSubscribers(self,var,subscriber):
        self.vars[var][0].append(subscriber)



    def setVar(self,var,value):
        self.vars[var][1]=value
        comm=MPI.COMM_WORLD
        for subscriber in self.vars[var][0]:
            if subscriber!=comm.Get_rank():
                comm.send([var,value,'variable {} has been changed to {} by {}'.format(var,value,comm.Get_rank())],dest=subscriber,tag=2)

    def updateVar(self,var,value):
        self.vars[var][1]=value

    def close(self):
        comm=MPI.COMM_WORLD
        for subscriber in range(comm.Get_size()):
            comm.send([0,0,0],dest=subscriber,tag=3)

    def seekAndDestroy(self,var,newValue):
        comm=MPI.COMM_WORLD
        if self.vars[var][1]!=newValue:
            self.setVar(var,newValue)
        else:
            comm.send([var,newValue,'variable {} had already value {}'.format(var,newValue)],dest=comm.rank,tag=4)


