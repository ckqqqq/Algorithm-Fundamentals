# LeetGPU 学习笔记

> LeetGPU = "GPU 界的 LeetCode"。在线写 GPU 代码(以 CUDA 为主),跑在真实硬件上,
> 目标是把每个算子写到**最快**。本目录按题目逐步深入,每题附带
> 平台机制讲解、性能分析、多框架实现(CUDA / Triton / JAX)。

参考链接:

- 平台主页: <https://leetgpu.com>
- 官方题库仓库(含 challenge 定义与 starter 模板): <https://github.com/AlphaGPU/leetgpu-challenges>
- 社区解法仓库: <https://github.com/rishisankar/leetgpu>、<https://github.com/dsl-learn/LeetGPU>
- 入门介绍: <https://www.i-programmer.info/news/204-challenges/17945-leetgpu-the-cuda-challenges.html>
- 中文笔记: <https://blog.csdn.net/jnlxx/article/details/149315227>

---

## 1. LeetGPU 是什么

- 由 **AlphaGPU** 公司开发的在线平台,口号是 "democratize access to hardware-accelerated
  languages"——不需要本地装 CUDA 工具链和 GPU,浏览器里写完直接跑。
- 题目按难度分 **easy / medium / hard**,覆盖算子全谱系:
  - easy: vector add、color inversion、relu、leaky relu、matrix transpose……
  - medium: reduction、histogram、2D conv、GEMM、softmax、sparse matvec……
  - hard: sorting、multi-head self-attention、top-k、k-means、rainbow table……
- 支持**多框架**提交,同一道题的 `solve()` 语义一致:
  **CUDA / PyTorch / Triton / JAX / CuTe / Mojo**。
- 免费档可提交并看到是否通过;Pro 档增加 **cycle-accurate GPU 计时** 与
  **性能百分位对比**(能看到自己的解法在全站用户里排多少名)。

## 2. 一道题是怎么被评判的

每道题在官方仓库 `challenges/<difficulty>/<number>_<name>/` 下由 3 部分定义:

1. **challenge.html** —— 题目描述、实现要求、示例、约束(用户看到的就是这个)。
2. **challenge.py** —— 判题逻辑:参考实现(reference_impl, PyTorch 写的)、
   功能测试用例、性能测试用例、`solve()` 签名(ctypes 描述)。
3. **starter/**(每个框架一份)—— 编译能通过但**不实现功能**的模板,保证大家都在同一契约下作答。

判分流程(以 vector add 为例):

| 阶段 | 内容 | 目的 |
|---|---|---|
| 示例测试 | `A=[1,2,3,4]`, `B=[5,6,7,8]` | 人工可读的最小用例 |
| 功能测试 | 约 10 个用例:长度 1~4、2 的幂、非 2 的幂、全零、负数、混合、极小/极大值、随机 | 正确性 |
| 性能测试 | `N = 25,000,000`(Tesla T4, 16GB) | 性能,决定排名 |

- 正确性判定:`atol = 1e-5, rtol = 1e-5`(float32 标准容差),与 PyTorch
  参考实现逐元素对比。
- **性能测试尺寸要能 5 倍放进 16GB 显存**(防止有人靠"多存几份"作弊)。

## 3. solve() 签名契约(各框架对照)

以 Vector Addition 为例(1D、float32、N 个元素):

| 框架 | solve 签名 | 结果放哪 |
|---|---|---|
| CUDA | `extern "C" void solve(const float* A, const float* B, float* C, int N)` | 写入 `C`(设备指针) |
| PyTorch | `def solve(A: Tensor, B: Tensor, C: Tensor, N: int)` | 写入 `C`(GPU 张量) |
| Triton | `def solve(a, b, c, N)` | 写入 `c`(GPU 张量) |
| JAX | `def solve(A, B, N) -> Array` | **直接 return** 结果(张量在设备上) |
| CuTe | `def solve(A, B, C, N)` | 写入 `C` |
| Mojo | `fn solve(A, B, C, N)` | 写入 `C`(设备指针) |

注意几个细节:

- CUDA/Mojo 里 `A, B, C` 是**设备指针**(显存地址),不是主机指针——不能直接解引用,必须进核函数。
- JAX 的契约和别家不一样:不传 `C`,返回新张量。
- 平台用 ctypes 按签名把张量数据指针传给 `solve`,所以签名**一字不能改**。

## 4. 解题必备的 GPU 概念(按重要性排序)

1. **Grid / Block / Thread 三级层次**:核函数启动 `<<<grid, block>>>`,
   每个线程用 `blockIdx.x * blockDim.x + threadIdx.x` 算出全局下标。
2. **内存合并 (memory coalescing)**:同一 warp(32 线程)同时访问**连续**地址,
   GPU 才能用一次内存事务搬完——这是 element-wise 算子性能的第一要素。
3. **内存带宽 vs 计算量**:先判断问题是 memory-bound 还是 compute-bound。
   vector add 是典型的 memory-bound:每元素 1 次加法、12 字节流量。
4. **向量化 (float4 / 128-bit 事务)**:一次搬 4 个 float,指令数减 4,
   事务数减 4,是 element-wise 算子的标准优化。
5. **grid-stride loop**:一个线程处理多个元素,循环步长 = 总线程数。
   优点:任意 N 都能处理、可以控制 grid 大小、减少启动开销。
6. **`__restrict__`**:告诉编译器指针不重叠(alias-free),解锁更激进的优化。
7. **Occupancy**:一个 SM 上同时跑的线程数。element-wise 算子一般
   "线程越多越好",让带宽打满。
8. **`cudaDeviceSynchronize()`**:平台计时通常以核函数完成为准,显式同步更稳。

## 5. 性能分析方法论

```
理论下限 = 总内存流量 / 内存带宽
```

vector add @ N=25,000,000(float32):

```
A: 25M × 4B = 100 MB
B: 25M × 4B = 100 MB
C: 25M × 4B = 100 MB
总计 ≈ 300 MB
T4 带宽 ≈ 300 GB/s (HBM2)

理论下限 ≈ 300 MB / 300 GB/s ≈ 1.0 ms
```

- 基线标量版(每线程 1 元素,4B 访问)一般能到带宽峰值的 ~60-75%。
- float4 向量化版(16B 访问)通常能到 ~90%+。
- 实测手段:NSight Compute / ncu 看 `Memory Throughput %`、`DRAM Throughput`,
  接近 100% 就是"已经到内存墙了,再优化也快不了"。

## 6. 目录结构

```
10-leetgpu/
├── README.md                  ← 本文件(平台机制 + 概念)
└── 01_vector_add/
    ├── notes.md               ← 题目深度拆解(优化阶梯、性能账本)
    ├── vector_add.cu          ← CUDA 基线(每线程 1 元素)
    ├── vector_add_vectorized.cu  ← CUDA float4 + grid-stride 优化版
    ├── vector_add_triton.py   ← Triton 版
    └── vector_add_jax.py      ← JAX 版
```
