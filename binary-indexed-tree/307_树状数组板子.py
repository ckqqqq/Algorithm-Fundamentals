from typing import List
class NumArray:
    def __init__(self, nums: List[int]):
        self.prefix=[0 for i in range(len(nums)+1)]
        n=len(nums)
        for i in range(1,n+1):
            self.prefix[i]=self.prefix[i]+nums[i]
            j=i+self.lowbit(i)
            if i<n+1:
                self.prefix[j]=nums[i]
    @staticmethod
    def _lowbit(x:int):
        return x&(~x+1)
    def update(self, index: int, val: int) -> None:
        while index<len(self.prefix):
            self.prefx[index]+=val
            index+=self.lowbit(index)
    def prefix_sum(self,index:int):##开区间，严格比index 小的数据之和
        s=0
        while index>0:
            s+=self.prefix[index]
            index-=self._lowbit(index)
        return s

    def sumRange(self, left: int, right: int) -> int:
        s=self.prefix_sum(right+1)-self.prefix_sum(left)
        return s        
    

# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(index,val)
# param_2 = obj.sumRange(left,right)