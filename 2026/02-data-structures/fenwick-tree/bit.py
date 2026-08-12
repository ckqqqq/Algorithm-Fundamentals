class Fenwick():## Fenwick 存的是差分数组
    def __init__(self,n):
        self.n=n
        self.tree=[0]*(n+1)
    @staticmethod
    def __lowbit(n):
        return n& (~n+1)

    def add(self,index,delta):# index ==1000
        while index<=self.n:
            self.tree[index]+=delta
            index+=self.__lowbit(index)#1000+1=1001

    def prefix_query
    
