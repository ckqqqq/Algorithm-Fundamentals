# RL 强化学习策略

## From PPO to GRPO

![image-20250219170636672](https://ckqqqq-qiker-image-service.oss-cn-beijing.aliyuncs.com/typora-image/image-20250219170636672.png)

### PPO有什么问题

* Actor Critic 算法中使用值函数来估计奖励，能够降低偏差但是方差较大，相比AC，PPO使用GAE 来平衡采样过程中方差和偏差的影响

	#### PPO的公式

	$$
	\mathcal{J}_{P P O}(\theta)=\mathbb{E}\left[q \sim P(Q), o \sim \pi_{\theta_{o l d}}(O \mid q)\right] \frac{1}{|o|} \sum_{t=1}^{|o|} \min \left[\frac{\pi_\theta\left(o_t \mid q, o_{<t}\right)}{\pi_{\theta_{o l d}}\left(o_t \mid q, o<t\right)} A_t, \operatorname{clip}\left(\frac{\pi_\theta\left(o_t \mid q, o_{<t}\right)}{\pi_{\theta_{o l d}}\left(o_t \mid q, o_{<t}\right)}, 1-\varepsilon, 1+\varepsilon\right) A_t\right],
	$$

	

	*  $\pi_\theta$ and $\pi_{\theta_{o l d}}$ are the current and old policy models, and $q, o$ are questions and outputs sampled from the question dataset and the old policy $\pi_{\theta_{\text {old }}}$, respectively. $\varepsilon$ is a **clipping-related hyper-parameter introduced in PPO** for **stabilizing training.** $A_t$ is the advantage, which is computed by **applying Generalized Advantage Estimation (GAE)** (Schulman et al., 2015), based on on the **rewards $\left\{r_{\geq t}\right\}$** and a learned value function $V_\psi$. Thus, in PPO, a value function needs to be trained alongside the policy model and to mitigate over-optimization of the reward model, the standard approach is to **add a per-token KL penalty from a reference model in the reward at each toke**n (Ouyang et al., 2022), i.e.,

	#### PPO 的奖励

	* $$
		r_t=r_{\varphi}\left(q, o_{\leq t}\right)-\beta \log \frac{\pi_\theta\left(o_t \mid q, o_{<t}\right)}{\pi_{r e f}\left(o_t \mid q, o_{<t}\right)},
		$$

	* where $r_{\varphi}$ is the **reward modeL**, $\pi_{r e f}$ is the reference mode**l, which is usually the **initial SFT model,** and $\beta$ is the coefficient of the KL penalty.

* #### ppo的问题

* 缺点一（额外的模型和额外的开销）：As the value function employed in PPO is typically another model of comparable size as the **policy model,** **it brings a substantial memory and computational burden**. 

* ,缺点二 （reward 在token粒度上分配不均）： the **value functio**n is treated as a baseline in the calculation of the advantage for variance reduction. While in the LLM context, usually only the **last token** is assigned a **reward score** by the **reward model,** which may complicate the training of a value function that is accurate at each token.

### GRPO

*  We propos**e Group Relative Policy Optimization (GRPO),** which obviates the need for additional value function approximation as in PPO, and **instead uses the average reward of multiple sampled outputs**, produced in response to the same question, as the baseline. More specifically, for each question $q$, GRPO **samples a group of outputs** $\left\{o_1, o_2, \cdots, o_G\right\}$ from the **old policy** $\pi_{\theta_{o l d}}$ and then optimizes the policy model by maximizing the following objective:

![1740660712222](image/强化学习GRPO_PPO_Critic_Actor/1740660712222.png)

$$
J_{GRPO}(\theta)=E[q\sim P(Q),\{o\}^{G}_{i=1} \sim \pi_{\theta old}(O|q)]\\

\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{i=1}^{\langle0|}\sum_{i=1}^{\langle0|}\left\{\operatorname*{min}\left[\frac{\pi_{\theta}(o_{i}|q)}{\pi_{\theta_{old}(o_{i}|q)}}\hat{A}_{i},\text{clip}\left(\frac{\pi_{\theta}(o_{i}|q)}{\pi_{\theta_{old}}(o_{i}|q)},1-\varepsilon,1+\varepsilon\right)\hat{A}_{i}\right]-\beta\mathbf{D}_{KL}\left[\pi_{\theta}||\pi_{e,e j}\right]\right\}
$$

$$
|\mathrm{D}_{K L}\left(\pi_{\theta}||\pi_{r e f}\right)=\frac{\pi_{r e f}(o_{i}|q)}{\pi_{\theta}(o_{i}|q)}-\log\frac{\pi_{r e f}(o_{i}|q)}{\pi_{\theta}(o_{i}|q)}-1
$$

$$

* 公式解析$$J_{grpo}$$ 这是优化目标
* For each **question $q$,** GRPO samples a group of outputs $\left\{o_1, o_2, \cdots, o_G\right\}$ from the old policy $\pi_{\theta_{o l d}}$ and then optimizes the policy model by maximizing the following objective: 
* 

#### reward设计的独到之处

* ![image-20250227205334990](C:/Users/qiker%20chen/AppData/Roaming/Typora/typora-user-images/image-20250227205334990.png)
	*  

## Refer

* DeepseekMath [2402.03300](https://arxiv.org/pdf/2402.03300)
* [论文笔记 General Advantage Estimation（GAE）-CSDN博客](https://blog.csdn.net/weixin_39891381/article/details/105153867)
