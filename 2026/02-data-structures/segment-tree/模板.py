"""
最简单的线段树模板（递归版）
功能：单点修改 + 区间求和，都是 O(log n)

节点下标规则：根节点是 1，节点 node 的左孩子是 node*2，右孩子是 node*2+1。
树用数组存，开 4*n 保证不会越界。
"""


class SegmentTree:
    def __init__(self, data):
        self.n = len(data)                # 数组长度
        self.tree = [0] * (4 * self.n)    # 线段树数组
        # 四倍数据 长度
        self._build(1, 0, self.n - 1, data)# 0~n-1遍历建树
        ## node 本身

    def _build(self, node, start, end, data):
        """递归建树：把区间 [start, end] 的和存到 tree[node]"""
        if start == end:                  # 叶子节点：区间只有一个数
            self.tree[node] = data[start]# 把区间Start end 的和存到tree[node]
            return# 很聪明的方法，将数组打散
        mid = (start + end) // 2          # 把区间一分为二
        self._build(node * 2, start, mid, data)          # 左半边 如果发生收敛，旧# 
        # 数组打散的关键在于node
        self._build(node * 2 + 1, mid + 1, end, data)    # 右半边
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]  # 父节点 = 左右之和
        #这个非常重要

    def update(self, index, value):
        """把下标 index 的值改成 value"""
        self._update(1, 0, self.n - 1, index, value)

    def _update(self, node, start, end, index, value):
        """单点修改：一路下探到叶子，改完再一路回溯更新父节点"""
        if start == end:                  # 找到目标叶子
            self.tree[node] = value
            return
        mid = (start + end) // 2
        if index <= mid:
            self._update(node * 2, start, mid, index, value)      # 目标在左半边
        else:
            self._update(node * 2 + 1, mid + 1, end, index, value)  # 目标在右半边
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]  # 回溯更新

    def range_sum(self, left, right):
        """求区间 [left, right] 的和（闭区间）"""
        return self._range_sum(1, 0, self.n - 1, left, right)

    def _range_sum(self, node, start, end, left, right):# 出界
        """区间查询：目标区间和当前节点区间的关系分三种情况"""
        if right < start or end < left:
            return 0                       # 情况1：完全不相交 → 返回 0
        if left <= start and end <= right:
            return self.tree[node]         # 情况2：完全被覆盖 → 直接返回节点值
        # 情况3：部分相交 → 拆到左右孩子继续查
        mid = (start + end) // 2
        return (
            self._range_sum(node * 2, start, mid, left, right)
            + self._range_sum(node * 2 + 1, mid + 1, end, left, right)
        )


# ============ 用法示例 ============
if __name__ == "__main__":
    # 快速读入所有数字
    import sys
    data = list(map(int, sys.stdin.buffer.read().split()))

    n = data[0]                     # 数组长度
    arr = data[1:1 + n]             # 初始数组
    segment_tree = SegmentTree(arr)

    # 示例：单点修改 + 区间查询
    segment_tree.update(0, 100)     # 把下标 0 改成 100
    print(segment_tree.range_sum(0, n - 1))   # 求整个数组的和

    # 注意：这里区间是闭区间 [left, right]
    # 如果要改成"区间最大值"，只需要把所有的 "+" 换成 max，并把"不相交返回 0"改成返回极小值
