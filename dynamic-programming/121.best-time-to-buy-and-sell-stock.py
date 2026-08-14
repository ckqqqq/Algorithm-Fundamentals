#
# @lc app=leetcode id=121 lang=python3
#
# [121] Best Time to Buy and Sell Stock
#

# @lc code=start
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices)<=1:
            return 0
        minPrice=prices[0]#可以用正无穷float('inf')
        ans=0
        for price in prices:
            if price<minPrice:#事实上减少if判断直接用min和max会更快
                minPrice=price
            elif price>minPrice:
                ans=max(ans,price-minPrice)
        return ans
                
        
# @lc code=end

