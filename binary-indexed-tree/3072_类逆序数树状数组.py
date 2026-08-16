from typing import List
class Fenwick:
    def __init__(self,arr):
        n=len(arr)
        self.tree=[0]*(n+1)
        for i in range(1,n+1):
            self.tree[i]+=arr[i-1]
            j=i+self._lowbit(i)
            if j<n+1:
                self.tree[j]+=self.tree[i]
    @staticmethod
    def _lowbit(x):
        return x&(~x+1)
    def update(self,index,delta):#数组下标要+1
        i=index+1
        while i<len(self.tree):
            self.tree[i]+=delta
            i+=self._lowbit(i)
        
    def prefix_sum(self,count):# count代表个数,很简单，count=0的时候要返回0
        s=0
        i=count
        while i>0:
            s+=self.tree[i]
            i-=self._lowbit(i)
        return s
    def range_sum(self,right,left):# 
        return self.prefix_sum(right+1)-self.prefix_sum(left)

class Solution:
    # @staticmethod
    def resultArray(self, nums: List[int]) -> List[int]:
        n=len(nums)
        arr1=[nums[0]]
        arr2=[nums[1]]
        s_nums=sorted(nums)
        # 0,1,2,3# 4-0,4-3,4-3,4-1
        # 4,3,2,1
        # 9,8,3,1
        ## 离散化
        ranks={v:n-i for i,v in enumerate(s_nums)}# 通过值找排名
        # 4,3,2,1
        bit1=Fenwick([0]*n)
        bit2=Fenwick([0]*n)
        bit1.update(ranks[arr1[0]],1)# R1
        bit2.update(ranks[arr2[0]],1)# R2
        for i in range(2,n):
            rank=ranks[nums[i]]# 按照大小序号
            count1=bit1.prefix_sum(rank)# 开区间，严格比x小的数
            count2=bit2.prefix_sum(rank)# 开区间，严格比x小的数
            x=nums[i]
            if count1>count2 or (count1==count2 and len(arr1)<=len(arr2)):
                arr1.append(x)
                bit1.update(ranks[x],1)
            else: #count2<count1:# 可优化
                arr2.append(x)
                bit2.update(ranks[x],1)
        return arr1+arr2

            



