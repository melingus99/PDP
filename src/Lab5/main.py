import threading
from src.Lab5.Config import *
import datetime
import sys
import math
import concurrent.futures
class Lab5:
    def __init__(self,array1,array2):
        self.array1=array1
        self.array2=array2
        if len(array1)!=len(array2):
            self.padding()
        self.prod=[0]*(len(self.array1)+len(self.array2)-1)
        self.lock=threading.Lock()


    def prodLinear(self):
        for i in range(len(self.array1)):
            for j in range(len(self.array2)):
                self.prod[i+j]=self.prod[i+j]+self.array1[i]*self.array2[j]


    def prodSome(self,start1,finish1):
        for i in range(start1,finish1):
            for j in range(len(self.array2)):
                self.lock.acquire()
                self.prod[i+j]=self.prod[i+j]+self.array1[i]*self.array2[j]
                self.lock.release()

    def prodParallel(self,nrThreads):
        threads=[]
        ratio1=len(self.array1)//nrThreads
        for i in range(nrThreads-1):
            start1=ratio1*i
            final1=ratio1*(i+1)
            threads.append(threading.Thread(target=self.prodSome,args=(start1,final1)))

        start1=ratio1*(nrThreads-1)
        final1=len(self.array1)

        threads.append(threading.Thread(target=self.prodSome,args=(start1,final1)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def karatsubaPoly(self,ar1,ar2):
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

            productLow=self.karatsubaPoly(ar1Low,ar2Low)
            productHigh=self.karatsubaPoly(ar1High,ar2High)
            productLowHigh=self.karatsubaPoly(ar1LowHigh,ar2LowHigh)

            productMiddle=[0]*len(ar1)

            for i in range(len(ar1)-1):
                productMiddle[i]=productLowHigh[i]-productLow[i]-productHigh[i]

            for i in range(len(ar1)-1):
                product[i]+=productLow[i]
                product[i+len(ar1)]+=productHigh[i]
                product[i+halfSize]+=productMiddle[i]

            return product

    def karatsubaPolyParallel(self,ar1,ar2,depth,max_depth):
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

            executor=concurrent.futures.ThreadPoolExecutor(max_workers=3)
            futureLow = executor.submit(self.karatsubaPolyParallel, ar1Low,ar2Low,depth+1,max_depth)
            productLow = futureLow.result()
            futureHigh = executor.submit(self.karatsubaPolyParallel, ar1High,ar2High,depth+1,max_depth)
            productHigh = futureHigh.result()
            futureLowHigh = executor.submit(self.karatsubaPolyParallel, ar1LowHigh,ar2LowHigh,depth+1,max_depth)
            productLowHigh = futureLowHigh.result()
            
            executor.shutdown(wait=True)
            productMiddle=[0]*len(ar1)

            for i in range(len(ar1)-1):
                productMiddle[i]=productLowHigh[i]-productLow[i]-productHigh[i]

            for i in range(len(ar1)-1):
                product[i]+=productLow[i]
                product[i+len(ar1)]+=productHigh[i]
                product[i+halfSize]+=productMiddle[i]

            return product


    def reset(self):
        self.prod=[0]*(len(self.array1)+len(self.array2)-1)

    def padding(self):
        while len(self.array1)<len(self.array2):
            self.array1.append(0)

        while len(self.array2)<len(self.array1):
            self.array2.append(0)

                
def test():
    f=open("C:\\Users\\Bubu\\PycharmProjects\\labPPD\\src\\Lab5\\doc.txt",'a+')
    lab5=Lab5(ar1,ar2)
    start=datetime.datetime.now()
    lab5.prodLinear()
    finish=datetime.datetime.now()
    prodLinearTime=finish.timestamp()-start.timestamp()
    lab5.reset()

    start=datetime.datetime.now()
    lab5.prodParallel(nrThreads)
    finish=datetime.datetime.now()
    prodParallelTime=finish.timestamp()-start.timestamp()
    lab5.reset()

    start=datetime.datetime.now()
    lab5.karatsubaPoly(lab5.array1,lab5.array2)
    finish=datetime.datetime.now()
    prodKaratsubaLinearTime=finish.timestamp()-start.timestamp()

    start=datetime.datetime.now()
    lab5.karatsubaPolyParallel(lab5.array1,lab5.array2,0,math.ceil(math.log(nrThreads,3)))
    finish=datetime.datetime.now()
    prodKaratsubaParallelTime=finish.timestamp()-start.timestamp()

    f.write("Size of array1: {} \n" \
            "Size of array2: {} \n" \
            "Number of threads: {} \n"\
            "Regular Linear Time: {} \n" \
            "Regular Parallel Time: {} \n" \
            "Karatsuba Linear Time: {} \n" \
            "Karatsuba Parallel Time: {} \n" \
            "\n"
            .format(len(ar1),len(ar2),nrThreads,prodLinearTime,prodParallelTime,prodKaratsubaLinearTime,prodKaratsubaParallelTime)
    )

print(ar1)
print(ar2)
mult=Lab5(ar1,ar2)
print(mult.array2)
mult.prodLinear()
print(mult.prod)
mult.reset()
mult.prodParallel(nrThreads)
print(mult.prod)
mult.reset()
print(mult.karatsubaPoly(mult.array1,mult.array2))
print(mult.karatsubaPolyParallel(mult.array1,mult.array2,0,math.ceil(math.log(nrThreads, 3))))
#test()
