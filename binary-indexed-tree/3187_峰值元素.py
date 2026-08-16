# 这类题的特点是，区间之和可以累加，比如f[ll,rr]=f[ll,mid1]+f[mid1,mid2]+f[mid2,rr]
# 类似于峰值之类的东西，可以区间累加，也可以用树状数组维护区间和
class Fenwick:
    def __init__(self,arr):
        n=len(arr)
        self.tree=[0 for _ in range(n+1)]
        