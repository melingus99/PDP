import threading


class Lab2():
    def __init__(self):
        self.avaible=False
        self.p=0
        self.s=0
        self.first=[i for i in range(3)]
        self.second=[i for i in range(3,6)]

    def consumer(self):
        for i in range(len(self.first)):
            lock.acquire()
            while not self.avaible:
                lock.wait()
            self.s+=self.p
            self.avaible=False
            lock.notifyAll()
            lock.release()

    def producer(self):
        for i in range(len(self.first)):
            lock.acquire()
            while self.avaible:
                lock.wait()
            self.p=self.first[i]*self.second[i]
            self.avaible=True
            lock.notifyAll()
            lock.release()




lab2=Lab2()
threads=[threading.Thread(target=lab2.consumer, args=()),threading.Thread(target=lab2.producer,args=())]
lock=threading.Condition()

for i in threads:
    i.start()

for i in threads:
    i.join()


print(lab2.s)

liniar=[i for i in range(3)]
liniar2=[i for i in range(3,6)]
sum=0
for i in range(3):
    sum+=liniar[i]*liniar2[i]

print(sum)
