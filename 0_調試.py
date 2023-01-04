
from typing import List
from typing import Optional
from queue import Queue
from collections import deque
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res=[]
        def dfs(ans:str,stack:int):
            if stack<0 or len(ans)>2*n:
                return 
            if len(ans)==2*n and stack==0:
                res.append(ans)
                return 
            dfs(ans+"(",stack+1)
            dfs(ans+")",stack-1)
        dfs("",0)
        return res
        
                    
solution=Solution()
print(solution.generateParenthesis(1))
        