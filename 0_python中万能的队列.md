一、队列（Queue）
Python的Queue模块中提供了同步的、线程安全的队列类，包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列PriorityQueue。这些队列都实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步。

常用方法：

Queue.qsize() 返回队列的大小
Queue.empty() 如果队列为空，返回True,反之False
Queue.full() 如果队列满了，返回True,反之False，Queue.full 与 maxsize 大小对应
Queue.get([block[, timeout]])获取队列，timeout等待时间
Queue.get_nowait() 相当于Queue.get(False)，非阻塞方法
Queue.put(item) 写入队列，timeout等待时间
Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号。每个get()调用得到一个任务，接下来task_done()调用告诉队列该任务已经处理完毕。
Queue.join() 实际上意味着等到队列为空，再执行别的操作
示例代码如下：

```python
from Queue import Queue,LifoQueue,PriorityQueue
#先进先出队列
q=Queue(maxsize=5)
#后进先出队列 可以做stack用
lq=LifoQueue(maxsize=6)
#优先级队列 就是堆
pq=PriorityQueue(maxsize=5)

for i in range(5):
    q.put(i)
    lq.put(i)
    pq.put(i)

print "先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" %(q.queue,q.empty(),q.qsize(),q.full())
print "后进先出队列：%s;是否为空：%s;多大,%s;是否满,%s" %(lq.queue,lq.empty(),lq.qsize(),lq.full())
print "优先级队列：%s;是否为空：%s,多大,%s;是否满,%s" %(pq.queue,pq.empty(),pq.qsize(),pq.full())

print q.get(),lq.get(),pq.get()

print "先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" %(q.queue,q.empty(),q.qsize(),q.full())
print "后进先出队列：%s;是否为空：%s;多大,%s;是否满,%s" %(lq.queue,lq.empty(),lq.qsize(),lq.full())
print "优先级队列：%s;是否为空：%s,多大,%s;是否满,%s" %(pq.queue,pq.empty(),pq.qsize(),pq.full())
```

先进先出队列：deque([0, 1, 2, 3, 4]);是否为空：False；多大,5;是否满,True
后进先出队列：[0, 1, 2, 3, 4];是否为空：False;多大,5;是否满,False
优先级队列：[0, 1, 2, 3, 4];是否为空：False,多大,5;是否满,True
0 4 0
先进先出队列：deque([1, 2, 3, 4]);是否为空：False；多大,4;是否满,False
后进先出队列：[0, 1, 2, 3];是否为空：False;多大,4;是否满,False
优先级队列：[1, 3, 2, 4];是否为空：False,多大,4;是否满,False
 还有一种队列是双边队列，示例代码如下：

```python
from Queue import deque
dq=deque(['a','b'])
dq.append('c')
print dq
print dq.pop()
print dq
print dq.popleft()
print dq
dq.appendleft('d')
print dq
print len(dq)
deque(['a', 'b', 'c'])
c
deque(['a', 'b'])
a
deque(['b'])
deque(['d', 'b'])
2
```



 二、生产者消费者模式
生产者消费者模式并不是GOF提出的众多模式之一，但它依然是开发同学编程过程中最常用的一种模式

生产者模块儿负责产生数据，放入缓冲区，这些数据由另一个消费者模块儿来从缓冲区取出并进行消费者相应的处理。该模式的优点在于：

解耦：缓冲区的存在可以让生产者和消费者降低互相之间的依赖性，一个模块儿代码变化，不会直接影响另一个模块儿
并发：由于缓冲区，生产者和消费者不是直接调用，而是两个独立的并发主体，生产者产生数据之后把它放入缓冲区，就继续生产数据，不依赖消费者的处理速度
三、采用生产者消费者模式开发的Python多线程
在Python中，队列是最常用的线程间的通信方法，因为它是线程安全的，自带锁。而Condition等需要额外加锁的代码操作，在编程对死锁现象要很小心，Queue就不用担心这个问题。

Queue多线程代码示例如下：

```
from Queue import Queue
import time,threading
q=Queue(maxsize=0)

def product(name):
    count=1
    while True:
        q.put('气球兵{}'.format(count))
        print ('{}训练气球兵{}只'.format(name,count))
        count+=1
        time.sleep(5)
def consume(name):
    while True:
        print ('{}使用了{}'.format(name,q.get()))
        time.sleep(1)
        q.task_done()
t1=threading.Thread(target=product,args=('wpp',))
t2=threading.Thread(target=consume,args=('ypp',))
t3=threading.Thread(target=consume,args=('others',))

t1.start()
t2.start()
t3.start()
```


网上还有很多非常好的生产者消费者模式的Queue代码例子，开发同学需要根据具体的实际需求去设计实际模式
————————————————
版权声明：本文为CSDN博主「Survivior_Y」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_43533825/article/details/89155648
