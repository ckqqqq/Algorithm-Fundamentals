#
# @lc app=leetcode id=169 lang=python3
#
# [169] Majority Element
#

# @lc code=start
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        dic={}
        numMax=0
        ans=0
        for i in nums:
            dic[i]=dic.get(i,0)+1
            if numMax<dic[i]:
                numMax=dic[i]
                ans=i
        return ans
        
# @lc code=end

