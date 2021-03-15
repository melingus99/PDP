from mpi4py import MPI
from time import sleep
from dsm import DSM
from random import randint
import threading

def listen():
    while True:
        f=open("process {}.txt".format(comm.rank),'a')
        data=comm.recv(source=MPI.ANY_SOURCE)
        if data[2]==0:
            f.write('dsm closing \n')
            break
        elif data[2]=='update subscribers':
            dsm.updateSubscribers(data[0],data[1])
            f.write('dsm updated \n')
        else:
            dsm.updateVar(data[0],data[1])
            f.write(data[2]+'\n')

comm=MPI.COMM_WORLD
rank = comm.Get_rank()
dsm=DSM()
listener=threading.Thread(target=listen,args=())
listener.start()

if rank==0:
    dsm.subscribe('a',rank)
    dsm.subscribe('b',rank)
    dsm.subscribe('c',rank)

elif rank==1:
    dsm.subscribe('c',rank)
elif rank==2:
    dsm.subscribe('b',rank)
    dsm.subscribe('c',rank)




while True:
    i=randint(0,2000)
    if i==20:
        dsm.close()
        print('STOP!')
        break
    if rank==0:
        i=randint(0,2)
        if i==0:
            i=randint(0,5)
            dsm.seekAndDestroy('c',i)
        if i==1:
            i=randint(0,5)
            dsm.setVar('c',i)
    elif rank==1:
        i=randint(0,2)
        if i==0:
            i=randint(6,10)
            dsm.seekAndDestroy('c',i)
        if i==1:
            i=randint(6,10)
            dsm.setVar('c',i)
    elif rank==2:
        i=randint(0,2)
        if i==0:
            i=randint(11,15)
            dsm.seekAndDestroy('b',i)
        if i==1:
            i=randint(11,15)
            dsm.setVar('b',i)
# if rank==0:
#     print(rank,'da')
#     i=randint(0,5)
#     dsm.setVar('c',i)
# elif rank==1:
#     print(rank,'da')
#     i=randint(6,10)
#     dsm.setVar('c',i)
# elif rank==2:
#     print(rank,'da')
#     i=randint(11,15)
#     dsm.setVar('b',i)
