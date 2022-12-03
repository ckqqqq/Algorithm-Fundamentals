#
# @lc app=leetcode id=235 lang=python3
#
# [235] Lowest Common Ancestor of a Binary Search Tree
#

# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        def BSTLCA(root: TreeNode,p:TreeNode,q:TreeNode):
            if root==None:
                return None
            if q.val<root.val and p.val<root.val:
                return BSTLCA(root.left,p,q)
            if q.val>root.val and q.val>root.val:
                return BSTLCA(root.right,p,q)
            return root 
            
# @lc code=end

