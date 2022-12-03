#
# @lc app=leetcode id=22 lang=python3
#
# [22] Generate Parentheses
#

# @lc code=start
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        sta=""
        ans=[]
        def dfs(index:int,sta):
            if index>=2*n:
                ans.append(sta)
                return 
            if sta=="" or sta[-1]=="(":
                dfs(sta.join("("))
            if sta[-1]=="(":
                dfs(sta.join(")"))
        return ans
if __name__=="__main__":
    solution=Solution()
    print(solution.generateParenthesis(3))
                
        
# @lc code=end

