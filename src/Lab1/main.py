from random import randint
from src.Lab1.Node import *
import threading
from src.Lab1.Config import *
from src.Lab1.Counter import Counter
from time import sleep
import datetime
import logging
import statistics as st


def changePrimary(primary):
    number=randint(-100,100)
    index= randint(0,len(primary)-1)
    updateSecondary(primary[index],primary[index].sum,number)


def updateSecondary(node,oldNumber,newNumber):
    try:
        if node.parent:
            updateSecondary(node.parent,oldNumber,newNumber)
            lock.acquire_write()
            node.sum=node.sum-oldNumber+newNumber
            lock.release()
    except:
        lock.acquire_write()
        node.sum=node.sum-oldNumber+newNumber
        lock.release()

def addParent(nodes,NrOfElementsInTuples):
    if(len(nodes)==1):
        return
    parents=[]
    for i in range(0,len(nodes),NrOfElementsInTuples):
        node=Node(0)
        parents.append(node)
        if i+NrOfElementsInTuples<=len(nodes):
            for j in range(NrOfElementsInTuples):
                nodes[i+j].parent=node
                nodes[i+j].parent.sum+=nodes[i+j].sum
        else:
            for j in range(len(nodes)%NrOfElementsInTuples):
                nodes[i+j].parent=node
                nodes[i+j].parent.sum+=nodes[i+j].sum
    addParent(parents,NrOfElementsInTuples)

def recursivePrint(nodes,depth):
    parents=[]
    for i in nodes:
        print(i.sum,depth)
        try:
            if i.parent not in parents:
                parents.append(i.parent)
        except:
            return
    recursivePrint(parents,depth+1)

def checkSum(nodes,NrOfElementsInTuples,ok):
    if ok==0:
        return ok
    parents=[]
    for i in range(0,len(nodes),NrOfElementsInTuples):
        sum=0
        if i+NrOfElementsInTuples<=len(nodes):
            it=NrOfElementsInTuples
        else:
            it=len(nodes)%NrOfElementsInTuples

        for j in range(it):
            sum+=nodes[i+j].sum
            try:
                if nodes[i+j].parent not in parents:
                    parents.append(nodes[i+j].parent)
            except:
                return ok
        if sum!=nodes[i].parent.sum and ok==1:
            ok=0

    return checkSum(parents,NrOfElementsInTuples,ok)



def startThread(name):
    while c.value<=maxit:
        if c.value%100==0:
            lock.acquire_write()
            print('thread: '+str(name)+' iteration: '+str(c.value))
            print('Check sum: ')
            lock.release()
            ok=checkSum(primaryNodes,NrOfElementsInTuples,1)
            lock.acquire_write()
            if ok==1:
                print('Sum correspond')
            else:
                print('Sum do not correspond')
            print('nodes: ')
            recursivePrint(primaryNodes,0)
            print(' \n')
            lock.release()
        changePrimary(primaryNodes)
        c.increment()
        #sleep(1)

nrok=0
min=100
max=0
times=[]

primaryNodes=[]
c=Counter()
for i in primary:
    primaryNodes.append(Node(i))

addParent(primaryNodes,NrOfElementsInTuples)
threads=[threading.Thread(target=startThread, args=(i,)) for i in range(maxthreads)]
start = datetime.datetime.now()
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

finish = datetime.datetime.now()
time=finish.timestamp()-start.timestamp()
if time>max:
    max=time
if time<min:
    min=time
times.append(time)

ok=checkSum(primaryNodes,NrOfElementsInTuples,1)
if ok==1:
    nrok+=1


'''
avg=st.mean(times)
std=st.stdev(times)
f=open("Documentation.txt","a+")

f.write(" \n" \
    "12.  Number of primary variables:{} \n" \
        "Locks:{} \n" \
        "Number of elements summed to a secondary variable:{} \n" \
        "Number of Threads:{} \n" \
        "Number of times primary variables were changed:{} \n" \
        "Average time:{} \n" \
        "standard dev:{} \n" \
        "Minimum time:{} \n" \
        "Maximum time:{} \n" \
        "correct sums:{}% \n".format(len(primary),'no',NrOfElementsInTuples,maxthreads,maxit,avg,std,min,max,nrok))
'''
