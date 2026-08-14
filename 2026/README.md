# 2026 学习路线与题目汇总

本文件夹记录目前需要做的事情，围绕四个目标展开：

1. **学习 Harness 知识，跟踪前沿工作** → `08-research-notes/`、`09-career-targets/`
2. **夯实算法基础** → `01-network-flow/`、`02-data-structures/`、`03-cow-reverse/`、`04-cp-templates/`、`05-rate-limiter/`、`06-ml-system-problems/`
3. **准备基础的智力和概率题** → `07-janestreet-puzzles/`
4. **了解 Rust** → `rust_learning/`

题目材料从 `deepseek/`、`janestreet/`、`Kimi/`、`paper/` 四个目录整理而来。

---

## 目标一：Harness 知识与前沿跟踪

### 08-research-notes
- `mid-training-task-synthesis/后训练-任务合成-前沿工作跟踪.md` — Kimi K3 后训练综述（RL 三域九专家、partial rollout、reasoning-effort 预算控制、GRM、MOPD 多教师蒸馏、MXFP4 QAT、EAGLE-3 草稿模型等）
- `draft.md` — harness 研究观点论文草稿（极早期片段）

### 09-career-targets
- `target.md` — DeepSeek Harness 团队 JD + 个人批注

## 目标二：算法基础

### 01-network-flow
- `min_cost_max_flow.py` — 最小费用最大流完整实现（残量网络 + SPFA，支持负费用边）
- `test_min_cost_max_flow.py` — pytest 测试
- `README.md` — 使用说明

### 02-data-structures
- `fenwick-tree/`
  - `TreeDP.py` / `TreeDP.rs` — Fenwick 树状数组手写实现（Python / Rust，文件名 TreeDP 是历史遗留，内容不是树上 DP）
  - `bit.py` — 未完成草稿（prefix_query 未写完）
  - `前缀和与差分.py` — 树状数组区间管辖原理笔记
- `segment-tree/`
  - `线段树.md` — 模板文档（zkw 迭代版 + 递归懒标记版）
  - `模板.py` — Python 模板

### 03-cow-reverse
开关翻转问题（Flip Game / POJ 1753 变体）：枚举首行 + 逐行逼迫。
- `cow_reverse_question.rs` — 题面 + 完整解答一体
- `main.rs` — cargo 工程版正解（模拟翻转法）
- `cow_reverse_question_v2.rs` — 未完成的重写草稿
- `tests/` — 测试数据（1.in/1.ans、2.in/2.ans）

### 04-cp-templates
- `cp.py` — ICPC 刷题脚手架 CLI（new/test/stress/time，正解 vs 暴力对拍）
- `templates/` — 配套 sol/brute/gen 模板

### 05-rate-limiter
Token 计数限流器（每用户每分钟 N 请求 / M token）。
- `kimi.md` — 英文原题题干
- `flow.md` — 设计推导笔记（deque 基线 → 环形数组分桶 → O(1) 窗口累计）
- `flow_quiz.py` — 第一版作答（有 bug，草稿）
- `flow_quiz_v2.py` — 第二版作答（60 桶环形数组，完整可运行）

### 06-ml-system-problems
Kimi 风格：ML 系统场景改编的算法题，均含完整题解 + C++ 参考代码。
- `problem1_gradient_checkpointing.md` — 梯度检查点：链式网络选检查点最小化重算时间（分段 DP + Pareto 前沿）
- `problem2_tree_speculative_decoding.md` — 树形投机解码：期望接受 token 数（路径概率 + 期望线性性）
- `problem3_radix_attention_cache.md` — RadixAttention 前缀缓存模拟（Trie + 叶子 LRU）

## 目标三：智力与概率题

### 07-janestreet-puzzles
- `js_20260720.md` — 三道面试题：Blotto 城堡博弈变体、50 面骰子配对拍卖、硬币偶数正面概率
- `js_20260720_answer.md` — 整理版（⚠️ 仅题 3 有思路，题 1/2 为开放问题，无答案）

## 目标四：Rust

### rust_learning
Rust 学习练习（rust-by-example 风格，按章节编号）：
- `2_1primitives.rs` — 基本类型
- `3_1struct.rs` — 结构体
- `4_2Mutability.rs`、`4_3Scope_and_shadowing.rs` — 可变性与作用域/遮蔽
- `5_1Casting.rs`、`5_2FromInto.rs`、`5_3Inference.rs` — 类型转换与推断
- `6_1From_to.rs` — From/Into 转换
- `8_2Flow_of_control.rs`、`8_4Flow_and_Range.rs`、`8_5Fizz.rs`、`8_5_1_Grauds.rs`、`8_5_2_Binding.rs` — 流程控制
- `rust_note` — 学习笔记

---

## 待办 / 开放项
- [ ] Jane Street 题 1（Blotto 变体）、题 2（骰子拍卖）无答案
- [ ] `bit.py` 树状数组草稿未写完
- [ ] `flow_quiz.py` 有语法错误，以 v2 为准
- [ ] `08-research-notes/draft.md` 仅 3 行，待扩写
