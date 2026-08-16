from typing import List
def bisect_left(nums:List,x):#第一个>=x的下标, 注意这里不一定是x
    ll,rr=0,len(nums)-1
    while ll<=rr:
        mid=ll+(rr-ll)//2
        if nums[mid]<x:# 小于目标值，mid->
            ll=mid+1
        else:#nums[mid]>=x
            rr=mid-1# 返回
    return ll
print(bisect_left([1,2,2,4],2))
## 1(2)24
print(bisect_left([1,2,2,4],1))
## (1)224
print(bisect_left([1,2,2,4],3))
## 122(4)
def bisect_right(nums:List,x):## 返回>x的值的下标
    ll,rr=0,len(nums)-1
    while ll<=rr:
        mid=ll+(rr-ll)//2
        if nums[mid]<=x:# 小等于目标值，mid->
            ll=mid+1
        else:
            rr=mid-1
    # 笑死，缩进别写错了
    #
    return ll
print(bisect_right([1,2,2,4],2))
## 12(2)4
print(bisect_right([1,2,2,4],1))
## (1）224
print(bisect_right([1,2,2,4],3))
## 1224