# 01. Vector Addition —— 深度拆解

> 题目:两个 float32 向量逐元素相加。
> 约束:`1 ≤ N ≤ 100,000,000`,性能测试 `N = 25,000,000`。
> 契约:`extern "C" void solve(const float* A, const float* B, float* C, int N)`。

## 1. 先判断:这是 memory-bound 还是 compute-bound?

写 GPU 算子的第一步永远是**算账**:

```
每个元素的计算量: 1 次浮点加法 (FLOP = 1)
每个元素的内存流量: 读 A(4B) + 读 B(4B) + 写 C(4B) = 12B
```

- 计算强度 (arithmetic intensity) = 1 FLOP / 12 B ≈ 0.08 FLOP/B
- T4 的 FP32 峰值 ~8.1 TFLOPS,带宽 ~300 GB/s
- 以带宽打满算,每秒能处理 300GB/12B = 25G 元素 → 25M 元素只需 ~1ms
- 以算力打满算,每秒能处理 8.1T 元素 → 快 300 倍以上

**结论:瓶颈 100% 在内存带宽。** 所有优化手段都必须围绕
"让内存系统搬运得更高效"展开,而不是"让计算更快"。

## 2. 优化阶梯(从易到难)

### 阶梯 0:每线程 1 元素(基线)

```cuda
__global__ void vector_add_kernel(const float* input_a, const float* input_b,
                                  float* output_c, int num_elements) {
    int global_index = blockIdx.x * blockDim.x + threadIdx.x;
    if (global_index < num_elements) {
        output_c[global_index] = input_a[global_index] + input_b[global_index];
    }
}
```

- 相邻线程访问相邻地址 → **天然内存合并**,32 线程的 warp 一次事务搬 128B。
- 这是正确性优先的写法,性能大概在带宽峰值的 60-75%。
- 为什么到不了 100%?因为每 4B 一次访问,指令多、事务粒度小,
  还有边界分支的代价。

### 阶梯 1:float4 向量化(128-bit 访问)

```cuda
__global__ void vector_add_vectorized_kernel(const float4* input_a, ...)
```

- 每个线程一次搬 4 个 float(16B),内存指令从 `LDG.E.32` 变成 `LDG.E.128`。
- 指令数 ÷4、事务数 ÷4,内存系统更容易打满。
- 前提:`N` 是 4 的倍数,或把尾部(0~3 个元素)单独用标量核处理。

### 阶梯 2:grid-stride loop

```cuda
for (int chunk_index = blockIdx.x * blockDim.x + threadIdx.x;
     chunk_index < num_chunks;
     chunk_index += gridDim.x * blockDim.x) { ... }
```

- 一个线程处理多个元素,循环步长 = 总线程数。
- 好处:
  1. **任意 N** 都能处理(包括 N 小于总线程数的情况);
  2. grid 大小可以显式控制,不为"恰好覆盖"而生成巨大的 grid;
  3. 后续如果做 stream/多 kernel 融合,循环体可复用。

### 阶梯 3:`__restrict__` 与指针别名

- 核函数参数加 `__restrict__` 告诉编译器 `A/B/C` 互不重叠,
  编译器可以放心地把加载提前、重排指令。
- element-wise 场景收益不大(已经很简单),但 GEMM 这类大算子收益显著,
  养成习惯。

### 阶梯 4(可选):`cudaOccupancyMaxPotentialBlockSize`

- 用 API 查当前设备的最优 block 大小,而不是写死 256。
- 对 vector add 收益微小(线程越多越好,256/512/1024 差别不大),
  但这是"调优心智模型"的一部分。

## 3. 性能账本(估算)

| 版本 | 每次访问宽度 | 预期带宽利用率 | N=25M 预估耗时 |
|---|---|---|---|
| 基线(标量) | 4B | ~60-75% | ~1.3-1.7 ms |
| float4 向量化 | 16B | ~90%+ | ~1.1 ms |
| 理论下限 | — | 100% | ~1.0 ms |

- 带宽利用率上不去,常见原因:边界分支、非合并访问、grid 太小、
  block 太小导致 SM 占不满。
- 用 `ncu --metrics dram__throughput.avg.pct_of_peak_sustained_elapsed`
  实测,接近 100% 就说明"到内存墙了",别再折腾核函数,该想
  **数据复用**(比如把 A+B 的结果直接喂给下游算子,省一次写回)。

## 4. 本目录代码对照

| 文件 | 对应阶梯 | 说明 |
|---|---|---|
| `vector_add.cu` | 阶梯 0 | 每线程 1 元素,带完整注释 |
| `vector_add_vectorized.cu` | 阶梯 1+2+3 | float4 + grid-stride + `__restrict__` + 尾部处理 |
| `vector_add_triton.py` | 自动 | Triton 编译器自动做向量化/合并,写起来最短 |
| `vector_add_jax.py` | 自动 | `A + B` 一行,验证"正确性契约" |

## 5. 通用模板:遇到 element-wise 算子怎么下手

1. 算账:计算强度 = FLOPs / bytes,判断 memory-bound 还是 compute-bound。
2. 正确性优先:写最直白的每线程 1 元素版本,通过功能测试。
3. 向量化:能 float2/float4/float8 就向量化,注意尾部。
4. 测带宽利用率;到 90%+ 就收手,把时间花在算法/数据复用上。
5. 性能测试只跑一次大 N,多次取中位数,避免冷启动噪声。
