from collections import deque
import time
class SlidingWindowLimiter:
    def __init__(self,max_requests,max_tokens:1000,windows=60):
        self.max_req= max_requests
        self.max_tok=max_tokens
        self.window=window#60
        self.history=deque()# 每个元素：
        # (时间，Token数)可惜队列里面装不了太多

    def allow(self,token_cost=1):
        now=time.time()
        while self.history and self.history[0][0] < now -self.window:
            self.history.popleft()
            ## 过期则弹出
        total_req=len(self.history)
        total_tok=sum(c for _, c in self.history)#n(o)
        if total_req >= self.max_req or total_tok + token_cost>self.max_tok:
            return False
        self.history.append((now,token_cost))
        return True


