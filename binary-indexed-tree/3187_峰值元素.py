# 这类题的特点是，区间之和可以累加，比如f[ll,rr]=f[ll,mid1]+f[mid1,mid2]+f[mid2,rr]
# 类似于峰值之类的东西，可以区间累加，也可以用树状数组维护区间和

from typing import List
class Fenwick:
    def __init__(self,arr):
        n=len(arr)
        self.tree=[0 for _ in range(n+1)]
        for i in range(1,n+1):
            self.tree[i]+=arr[i-1]
            j=i+self._lowbit(i)
            if j<=n:
                self.tree[j]+=self.tree[i]               

    @staticmethod
    def _lowbit(x):
        return x&(~x+1)
    def update(self,index,delta):
        i=1+index# 序号，要加一
        while i<len(self.tree):
            self.tree[i]+=delta
            i+=self._lowbit(i)
    def prefix_sum(self,target):# 比他小的前缀和
        s=0
        while target>0:
            s+=self.tree[target]
            target-=self._lowbit(target)
        return s
    def range_sum(self,left,right):
        return self.prefix_sum(right+1)-self.prefix_sum(left)
class Solution:
    @staticmethod
    def isPeakSafe(arr:List,idx:int):# 适合将bug限定在最小域~~
        if idx-1>=0 and idx+1<len(arr) and arr[idx-1]<arr[idx]and arr[idx]>arr[idx+1]:
            return True# 是峰值而且合法
        else:
            return False
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n=len(nums)
        bit=Fenwick([0]*n)
        for i in range(1,n-1):
            if self.isPeakSafe(nums,i):# 可以区间累加的,小心python的大坑残留域！！！！
                bit.update(i,1)
        ans=[]
        # python的大坑是残留域名
        for qu in queries:
            if qu[0]==1:## 求区间峰值
                ll,rr=qu[1],qu[2]# rr是
                if rr-ll<=1:
                    ans.append(0)
                else:
                    peak_count=bit.range_sum(ll+1,rr-1)# 注意在这里限制左右端点
                    ans.append(peak_count)
            else:
                idx,val=qu[1],qu[2]
                for j in range(idx-1,idx+1+1):# 相邻区间都会受影响
                    if self.isPeakSafe(nums,j):# 安全判断
                        bit.update(j,-1)#削去峰值
                nums[idx]=val# 新值
                for j in range(idx-1,idx+1+1):# 遍历相邻，是否是峰值
                    if self.isPeakSafe(nums,j):
                        bit.update(j,1)# 遍历相邻，如果是峰值就加一
        return ans
        

                    
