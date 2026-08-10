# Tree Dp
#
class Fenwick():
    def __init__(self,n):# TreeArrary
        self.cells=[0]* (n+1)

    def add(self, index:int, delta:int):# 给为止index的值加上deta 0不计算，注意
        """给位置 index 的值加上delta nlogn"""
        position= index +1# 转为 1-based
        while position<len(self.cells):
            self.cells[position]+=delta
            position+=self._lowbit(position)
        
    def prefix_sum(self, index:int)-> int:
        """返回[0,index] 封闭区间的元素之和,nlogn"""
        position =index+1
        total=0
        while position>0:
            total+=self.cells[position]
            position-= self._lowbit(position)
        return total

    def range_sum(self,left:int,right:int):
        """返回[left,right]封闭区间的元素之和"""
        if left ==0:
            return self.prefix_sum(right)
        return self.prefix_sum(right)-self.prefix_sum(left-1)

    @staticmethod
    def _lowbit(value:int) ->int:
        return value & (~value+1)
tree= Fenwick(10)
tree.add(3,5)
tree.add(5,2)
assert tree.prefix_sum(3)==5
assert tree.prefix_sum(5)==7
assert tree.range_sum(4,9)==2
print(tree.range_sum(3,9))