import threading
import concurrent.futures
from src.Lab6.Config import *
import datetime
class Graph:
    def __init__(self,nrVertices,matrix):
        self.graph = matrix
        self.nrVertices = nrVertices
        self.path=[-1] * self.nrVertices

    def hasHamiltonianCycle(self):
        self.path[0] = 0

        if self.Util(0) == False:
            return False

        return True

    def checkFuture(self, v, pos,path):
        if self.graph[ path[pos-1] ][v] == 0:
            return False

        for vertex in path:
            if vertex == v:
                return False

        return True

    def Util(self,pos):
        if pos == self.nrVertices:
            if self.graph[ self.path[pos-1] ][ self.path[0] ] == 1:
                return True
            else:
                return False

        for v in range(0,self.nrVertices):

            if self.checkFuture(v, pos,self.path) == True:

                self.path[pos] = v

                if self.Util(pos+1) == True:
                    return True

                self.path[pos] = -1

        return False

    def hasHamiltonianCylceParallel(self):
        path=[-1] * self.nrVertices
        path[0] = 0

        executor=concurrent.futures.ThreadPoolExecutor(max_workers=nrThreads)
        ratio=self.nrVertices//nrThreads
        lock=threading.Lock()
        results=[]
        futures=[]
        for i in range(nrThreads-1):
            start=i*ratio
            finish=(i+1)*ratio
            future=executor.submit(self.UtilParallel,0,start,finish,lock,path)
            futures.append(future)

        for future in futures:
            results.append(future.result())

        start=(nrThreads-1)*ratio
        finish=self.nrVertices
        future=executor.submit(self.UtilParallel,0,start,finish,lock,path)
        results.append(future.result())

        executor.shutdown(wait=True)

        if any(result==True for result in results):
            return True

        return False

    def UtilParallel(self,pos,start,finish,lock,path):
        if pos == self.nrVertices:
            if self.graph[ path[pos-1] ][ path[0] ] == 1:
                return True
            else:
                return False
        for v in range(start,finish):
            if self.checkFuture(v, pos,path) == True:

                path[pos] = v
                if self.UtilParallel(pos+1,0,self.nrVertices,lock,path) == True:
                    return True

                path[pos] = -1
        return False

    def reset(self):
        self.path=[-1] * self.nrVertices

def test():
    g=Graph(nrVertices,matrix)
    edges=0
    for i in matrix:
        for j in i:
            if j==1:
                edges+=1
    f=open("C:\\Users\\Bubu\\PycharmProjects\\labPPD\\src\\Lab6\\doc.txt",'a+')
    start=datetime.datetime.now()
    g.hasHamiltonianCycle()
    finish=datetime.datetime.now()
    LinearTime=finish.timestamp()-start.timestamp()
    g.reset()

    start=datetime.datetime.now()
    g.hasHamiltonianCylceParallel()
    finish=datetime.datetime.now()
    ParallelTime=finish.timestamp()-start.timestamp()

    f.write("Nr of Vertices: {} \n" \
            "Nr of edges: {} \n" \
            "Number of threads: {} \n"\
            "Linear Time: {} \n" \
            "Parallel Time: {} \n" \
            "\n"
            .format(nrVertices,edges,nrThreads,LinearTime,ParallelTime)
    )
nrVertices=4
matrix=[ [0, 1, 0, 1], [1, 0, 1, 0],
         [0, 1, 0, 1], [1, 0, 1, 0]]

# matrix=[ [0, 1, 0, 0], [1, 0, 1, 0],
#          [0, 1, 0, 1], [0, 0, 1, 0]]
g = Graph(nrVertices,matrix)

print(g.hasHamiltonianCycle())
g.reset()
print(g.hasHamiltonianCylceParallel())
#test()
