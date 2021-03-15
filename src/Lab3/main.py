import threading
from concurrent.futures import ThreadPoolExecutor
from src.Lab3.Configs import *
import datetime


class Lab3():
    def __init__(self,matrix1,matrix2,nrThreads):
        self.matrix1=matrix1
        self.matrix2=matrix2
        self.nrThreads=nrThreads
        self.threads=[]
        self.finalMatrix=[[0]*len(self.matrix2[0])]*len(self.matrix1)
        self.executor=ThreadPoolExecutor(self.nrThreads)

    def calculateElement(self,row,col):
        for i in range(len(self.matrix2)):
            self.finalMatrix[row][col]+=self.matrix1[row][i]*self.matrix2[i][col]

    def calculateElements(self,start,final):
        m=len(self.matrix2[0])
        for i in range(start,final):
            self.calculateElement(i//m,i%m)

    def calculateMatrixThread(self):
        n=len(self.matrix1)
        m=len(self.matrix2[0])
        ratio=n*m//self.nrThreads
        for i in range(nrThreads-1):
            start=ratio*i
            final=ratio*(i+1)
            self.threads.append(threading.Thread(target=self.calculateElements,args=(start,final)))

        start=ratio*(nrThreads-1)
        final=n*m

        self.threads.append(threading.Thread(target=self.calculateElements,args=(start,final)))

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()


    def calculateMatrixPool(self):
        n=len(self.matrix1)
        m=len(self.matrix2[0])
        for i in range(0,n*m,3):
            for j in range(self.nrThreads):
                if (i+j)//m<n:
                    self.executor.submit(self.calculateElement((i+j)//m,(i+j)%m))

    def reset(self):
        self.finalMatrix=[[0]*len(self.matrix2[0])]*len(self.matrix1)

    def calculateMatrixLinear(self):
        for i in range(len(self.matrix1)):
            for j in range(len(self.matrix2[0])):
                for k in range(len(self.matrix2)):
                    self.finalMatrix[i][j]+=self.matrix1[i][k]*self.matrix2[k][j]


def test():
    f=open("C:\\Users\\Bubu\\PycharmProjects\\labPPD\\src\\Lab3\\Results.txt",'a+')
    lab3=Lab3(matrix1,matrix2,nrThreads)

    start=datetime.datetime.now()
    lab3.calculateMatrixLinear()
    finish=datetime.datetime.now()
    linearTime=finish.timestamp()-start.timestamp()

    start=datetime.datetime.now()
    lab3.calculateMatrixThread()
    finish=datetime.datetime.now()
    threadTime=finish.timestamp()-start.timestamp()

    start=datetime.datetime.now()
    lab3.calculateMatrixPool()
    finish=datetime.datetime.now()
    poolTime=finish.timestamp()-start.timestamp()

    f.write("Size of matrix: {} \n" \
            "Number of threads: {} \n"\
            "Linear Time: {} \n" \
            "Thread Time: {} \n" \
            "Pool Time: {} \n" \
            "\n"
            .format((n,m),nrThreads,linearTime,threadTime,poolTime)
    )

#test()

print("Matrix1: "+str(matrix1))
print("Matrix2: "+str(matrix2))
lab3=Lab3(matrix1,matrix2,nrThreads)
lab3.calculateMatrixLinear()
print("Linear Matrix: "+str(lab3.finalMatrix))
lab3.calculateMatrixThread()
print("Thread Matrix: "+str(lab3.finalMatrix))
lab3.calculateMatrixPool()
print("Pool Matrix: "+str(lab3.finalMatrix))
