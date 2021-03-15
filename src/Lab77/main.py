from mpi4py import MPI
import threading
import datetime
import sys
import math
import concurrent.futures



def prodLinear(array1,array2):
    prod=[0]*(2*len(array2)-1)
    for i in range(len(array1)):
        for j in range(len(array2)):
            prod[i+j]=prod[i+j]+array1[i]*array2[j]

    return prod

def prodSome(start,finish,array1,array2):
    prod=[0]*(2*len(array2)-1)
    for i in range(start,finish):
        for j in range(len(array2)):
            prod[i+j]=prod[i+j]+array1[i-start]*array2[j]

    return prod


def prodParallel(test):
    if rank == 0:

        ar1=[i for i in range(0,8)]
        ar2=[i for i in range(0,8)]
        ar1=padding(ar1,ar2)
        ar2=padding(ar2,ar1)

        ParallelTime=datetime.datetime.now()
        ratio=len(ar1)//comm.Get_size()

        for i in range(comm.Get_size()-1):
            start=ratio*i
            finish=ratio*(i+1)
            ar=[ar1[i] for i in range(start,finish)]
            comm.send(ar, dest=i+1, tag=11)
            comm.send([start,finish],dest=i+1,tag=12)

        for i in range(comm.Get_size()-1):
            comm.send(ar2, dest=i+1, tag=13)

        start=ratio*(comm.Get_size()-1)
        finish=len(ar1)
        ar=[ar1[i] for i in range(start,finish)]
        prod=prodSome(start,finish,ar,ar2)

        for i in range(comm.Get_size()-1):
            data=comm.recv(source=i+1,tag=14)
            for i in range(len(data)):
                prod[i]+=data[i]

        ParallelTime=datetime.datetime.now().timestamp()-ParallelTime.timestamp()
        if test==False:
            print(prod)
        else:
            f=open("C:\\Users\\Bubu\\PycharmProjects\\labPPD\\src\\Lab77\\doc.txt","a")
            f.write("Regular Parallel Time: {} \n"
            .format(ParallelTime)
            )

    else:
        ar=comm.recv(source=0,tag=11)
        start_finish=comm.recv(source=0,tag=12)
        start=start_finish[0]
        finish=start_finish[1]
        ar2=comm.recv(source=0,tag=13)
        prod=prodSome(start,finish,ar,ar2)
        comm.send(prod,dest=0,tag=14)


def karatsubaPoly(ar1,ar2):
    product=[0]*(len(ar1)+len(ar2)-1)
    if len(ar1)==1:
        product[0]=ar1[0]*ar2[0]
        return product
    else:
        halfSize=len(ar1)//2
        ar1Low=[0]*halfSize
        ar1High=[0]*halfSize
        ar2Low=[0]*halfSize
        ar2High=[0]*halfSize
        ar1LowHigh=[0]*halfSize
        ar2LowHigh=[0]*halfSize

        for i in range(halfSize):
            ar1Low[i]=ar1[i]
            ar1High[i]=ar1[halfSize+i]
            ar1LowHigh[i]=ar1Low[i]+ar1High[i]
            ar2Low[i]=ar2[i]
            ar2High[i]=ar2[halfSize+i]
            ar2LowHigh[i]=ar2Low[i]+ar2High[i]

        productLow=karatsubaPoly(ar1Low,ar2Low)
        productHigh=karatsubaPoly(ar1High,ar2High)
        productLowHigh=karatsubaPoly(ar1LowHigh,ar2LowHigh)

        productMiddle=[0]*len(ar1)

        for i in range(len(ar1)-1):
            productMiddle[i]=productLowHigh[i]-productLow[i]-productHigh[i]

        for i in range(len(ar1)-1):
            product[i]+=productLow[i]
            product[i+len(ar1)]+=productHigh[i]
            product[i+halfSize]+=productMiddle[i]

        return product

def karatsubaPolyParallel(ar1,ar2,depth,max_depth):
    product=[0]*(len(ar1)+len(ar2)-1)
    if depth==max_depth:
        for i in range(len(ar1)):
            for j in range(len(ar2)):
                product[i+j]+=(ar1[i]*ar2[j])
        return product
    else:
        halfSize=len(ar1)//2
        ar1Low=[0]*halfSize
        ar1High=[0]*halfSize
        ar2Low=[0]*halfSize
        ar2High=[0]*halfSize
        ar1LowHigh=[0]*halfSize
        ar2LowHigh=[0]*halfSize

        for i in range(halfSize):
            ar1Low[i]=ar1[i]
            ar1High[i]=ar1[halfSize+i]
            ar1LowHigh[i]=ar1Low[i]+ar1High[i]
            ar2Low[i]=ar2[i]
            ar2High[i]=ar2[halfSize+i]
            ar2LowHigh[i]=ar2Low[i]+ar2High[i]


        comm.send([ar1Low,ar2Low,depth+1,max_depth],dest=1,tag=1)
        comm.send([ar1High,ar2High,depth+1,max_depth],dest=2,tag=1)
        comm.send([ar1LowHigh,ar2LowHigh,depth+1,max_depth],dest=3,tag=1)
        productLow = comm.recv(source=1,tag=1)
        productHigh = comm.recv(source=2,tag=1)
        productLowHigh = comm.recv(source=3,tag=1)

        productMiddle=[0]*len(ar1)

        for i in range(len(ar1)-1):
            productMiddle[i]=productLowHigh[i]-productLow[i]-productHigh[i]

        for i in range(len(ar1)-1):
            product[i]+=productLow[i]
            product[i+len(ar1)]+=productHigh[i]
            product[i+halfSize]+=productMiddle[i]

        return product


def karaParallel(test):
    if rank==0:
        ar1=[i for i in range(0,8)]
        ar2=[i for i in range(0,8)]
        padding(ar1,ar2)
        padding(ar2,ar1)

        karaParallelTime=datetime.datetime.now()
        prod=karatsubaPolyParallel(ar1,ar2,0,1)
        karaParallelTime=datetime.datetime.now().timestamp()-karaParallelTime.timestamp()
        if test==False:
            print(prod)
        else:
            f=open("C:\\Users\\Bubu\\PycharmProjects\\labPPD\\src\\Lab77\\doc.txt","a")
            f.write("Karatsuba Parallel Time: {} \n \n".format(karaParallelTime))

    else:
        data=comm.recv(source=0,tag=1)
        ar1=data[0]
        ar2=data[1]
        depth=data[2]
        max_depth=data[3]
        prod=karatsubaPolyParallel(ar1,ar2,depth,max_depth)
        comm.send(prod,dest=0,tag=1)


def padding(array1,array2):
    while len(array1)<len(array2):
        array1.append(0)

    return array1



comm=MPI.COMM_WORLD
rank = comm.Get_rank()
test=False
if rank==0:
    ar1=[i for i in range(0,8)]
    ar2=[i for i in range(0,8)]
    ar1=padding(ar1,ar2)
    ar2=padding(ar2,ar1)
    print(ar1)
    print(ar2)
    linearTime=datetime.datetime.now()
    prod_linear=prodLinear(ar1,ar2)
    linearTime=datetime.datetime.now().timestamp()-linearTime.timestamp()
    karaTime=datetime.datetime.now()
    prod_kara=karatsubaPoly(ar1,ar2)
    karaTime=datetime.datetime.now().timestamp()-karaTime.timestamp()
    if test==False:
        print(prod_linear)
        print(prod_kara)
    else:
        f=open("C:\\Users\\Bubu\\PycharmProjects\\labPPD\\src\\Lab77\\doc.txt","a")
        f.write("Size of array1: {} \n" \
            "Size of array2: {} \n" \
            "Number of processes: {} \n"\
            "Regular Linear Time: {} \n" \
            "Karatsuba Linear Time: {} \n"
            .format(len(ar1),len(ar2),comm.Get_size(),linearTime,karaTime)
        )
        f.close()


prodParallel(test)
karaParallel(test)


