# TODO — 2026 Roadmap

## Goal 1: Learn Harness & Track Frontier Research
- [ ] Expand `08-research-notes/draft.md` (currently only 3 lines: harness as a progressive, systematic research process; harness agents in the pre-training / post-training / infra loop)
- [ ] Keep updating `mid-training-task-synthesis/后训练-任务合成-前沿工作跟踪.md` with new frontier work (RL expert domains, partial rollout, reasoning-effort budgeting, GRM, MOPD, MXFP4 QAT, EAGLE-3)
- [ ] Deep-dive into Harness team requirements from `09-career-targets/target.md` and map skill gaps

## Goal 2: Solidify Algorithm Fundamentals
- [ ] Finish `02-data-structures/fenwick-tree/bit.py` (`prefix_query` incomplete)
- [ ] Fill in the empty notes: Fenwick tree summary, segment-tree printing utility
- [ ] Fix `05-rate-limiter/flow_quiz.py` syntax errors, or remove it and keep `flow_quiz_v2.py` as the canonical version
- [ ] Complete `03-cow-reverse/cow_reverse_question_v2.rs` (self-rewrite exercise)
- [ ] Re-derive the three ML-system problems in `06-ml-system-problems/` from scratch without looking at the solutions (DP / probability-on-trees / Trie+LRU)
- [ ] Practice with `04-cp-templates/cp.py` stress-testing workflow on new problems

## Goal 3: IQ & Probability Puzzles
- [ ] Solve Jane Street problem 1 (Blotto castle variant with overspend penalty) — currently open
- [ ] Solve Jane Street problem 2 (four 50-sided dice pairing + auction bidding) — currently open
- [ ] Write up clean solutions in `07-janestreet-puzzles/js_20260720_answer.md`

## Goal 4: Learn Rust
- [ ] Continue rust-by-example chapters beyond ch.8 (flow of control): functions, modules, crates, error handling, ownership/borrowing deep dive
- [ ] Consolidate `rust_learning/rust_note` notes
- [ ] Rewrite one Python algorithm (e.g. `min_cost_max_flow.py`) in Rust as a capstone exercise

## Housekeeping
- [ ] Decide whether `2026/` should be tracked by git in Algorithm-Fundamentals (or added to `.gitignore`)
- [ ] Clean up leftover build artifacts in the old `deepseek/` directory (Cargo `target/`, empty files, compiled binaries)
- [ ] Optionally rename remaining Chinese file names to English for consistency

---

# TODO — 2026 路线

## 目标一：学习 Harness 知识，跟踪前沿工作
- [ ] 扩写 `08-research-notes/draft.md`（目前仅 3 行：harness 是渐进式、系统性的研究过程，harness agent 参与预训练/后训练/Infra 的 loop）
- [ ] 持续更新 `mid-training-task-synthesis/后训练-任务合成-前沿工作跟踪.md`，跟踪前沿工作（RL 专家域、partial rollout、reasoning-effort 预算、GRM、MOPD、MXFP4 QAT、EAGLE-3）
- [ ] 对照 `09-career-targets/target.md` 中 Harness 团队 JD，梳理自己的能力差距

## 目标二：夯实算法基础
- [ ] 补完 `02-data-structures/fenwick-tree/bit.py`（`prefix_query` 未写完）
- [ ] 补全空笔记：树状数组总结、线段树打印工具
- [ ] 修复 `05-rate-limiter/flow_quiz.py` 的语法错误，或删掉它以 v2 为准
- [ ] 完成 `03-cow-reverse/cow_reverse_question_v2.rs`（自己重写的练习）
- [ ] 不看题解，独立重做 `06-ml-system-problems/` 三道题（DP / 树上概率 / Trie+LRU）
- [ ] 用 `04-cp-templates/cp.py` 的对拍流程练习新题

## 目标三：准备基础的智力和概率题
- [ ] 解出 Jane Street 题 1（带超额扣分的 Blotto 城堡博弈变体）——目前无答案
- [ ] 解出 Jane Street 题 2（四颗 50 面骰子配对 + 拍卖出价）——目前无答案
- [ ] 把完整解答写进 `07-janestreet-puzzles/js_20260720_answer.md`

## 目标四：了解 Rust
- [ ] 继续 rust-by-example 第 8 章之后的内容：函数、模块、crate、错误处理，深入所有权/借用
- [ ] 整理 `rust_learning/rust_note` 笔记
- [ ] 收官练习：把一个 Python 算法（如 `min_cost_max_flow.py`）用 Rust 重写

## 杂项
- [ ] 决定 `2026/` 是否纳入 Algorithm-Fundamentals 的 git 管理（或加入 `.gitignore`）
- [ ] 清理旧 `deepseek/` 目录的残留构建产物（Cargo `target/`、空文件、编译出的二进制）
- [ ] 可选：把剩余中文文件名统一改成英文
