# RL 强化学习策略

## From PPO to GRPO

![image-20250219170636672](https://ckqqqq-qiker-image-service.oss-cn-beijing.aliyuncs.com/typora-image/image-20250219170636672.png)

### PPO有什么问题

* Actor Critic 算法中使用值函数来估计奖励，能够降低偏差但是方差较大，相比AC，PPO使用GAE 来平衡采样过程中方差和偏差的影响



## Refer

* DeepseekMath [2402.03300](https://arxiv.org/pdf/2402.03300)
* [论文笔记 General Advantage Estimation（GAE）-CSDN博客](https://blog.csdn.net/weixin_39891381/article/details/105153867)