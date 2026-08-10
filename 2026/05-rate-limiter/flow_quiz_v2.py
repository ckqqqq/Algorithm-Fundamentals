from collections import deque
import time
class CircleRateLimiter:
    def __init__(self,max_requests,max_tokens):
        self.max_req=max_requests
        self.max_tok=max_tokens
        self.window=60 ## 窗口有多少秒，可能为两分钟 比如120
        self.n_buckets=60 ## 窗口有多少块
        self.bucket_size=self.window//self.n_buckets # 每一块多少秒
        self.ring=[[0,0,0] for _ in range(self.n_buckets)]
        self.win_req=0
        self.win_tok=0
    
    def allow(self, cost=1):## 这个请求有可能在同一秒内放进来，也可能在下一秒甚至数秒内放进来
        """返回True就值得放行并计入，否则就拒绝"""
        now=int(time.time())
        bucket_ts= (now// self.bucket_size)*self.bucket_size  #时间戳（timestamp）# 当前桶的时间戳
        bucket=self.ring[(now//self.bucket_size)%self.n_buckets]##当前时间戳对应的桶
        #核心代码
        ## 每个元素为[时间戳，请求数，token数]

        if bucket[0]!=bucket_ts:# 槽位里面的数据是旧的
            if bucket_ts-bucket[0]>self.window:# 闲置超过一个窗口，所有的桶都过期了，窗口全部清空
                self.win_req=0
                self.win_tok =0
                # self.ring=[[0,0,0] for _ range(self.n_buckets)]
                for b in self.ring:
                    b[0]=b[1]=b[2]=0
            else:
                self.win_req-= bucket[1]# 这个槽不计入窗口
                self.win_tok-= bucket[2]# 这个槽里面的旧内容不计入窗口
            # 加上新的值
            bucket[0]=bucket_ts
            bucket[1]=0 #请求数 
            bucket[2]=0 # token数
        # 请求非法
        if self.win_req>=self.max_req or self.win_tok>=self.max_tok:
            return False
        else:
            #   请求合法，更新当前桶和窗口的计数
            bucket[1]+=1
            bucket[2]+=cost
            self.win_req+=1
            self.win_tok+=cost
            return True

            

        




