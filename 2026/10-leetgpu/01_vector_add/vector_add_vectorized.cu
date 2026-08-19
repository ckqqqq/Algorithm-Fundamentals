// vector_add_vectorized.cu —— LeetGPU "Vector Addition" 优化版
//
// 优化点(按收益排序):
//   1. float4 向量化:每个线程一次读写 4 个 float(128-bit 内存事务),
//      指令数和事务数都降到 1/4,内存系统更容易打满带宽。
//   2. grid-stride loop:一个线程循环处理多个 float4 块,
//      步长 = 总线程数,任意 N 都能处理,grid 规模可显式控制。
//   3. __restrict__:告知编译器三个指针互不重叠,解锁指令重排优化。
//   4. 尾部处理:当 N 不是 4 的倍数时,剩余的 0~3 个元素用标量核单独算。
//
// 性能预期(N = 25,000,000, Tesla T4):
//   内存流量 = 3 × 100MB = 300MB,带宽 ~300GB/s,理论下限 ~1.0ms。
//   本版本可达带宽峰值 90%+,约 1.1ms;基线标量版约 60-75%。

#include <cuda_runtime.h>

// ---------------------------------------------------------------------------
// 主核函数:每个线程用 float4 一次处理 4 个元素(只负责 4 的倍数部分)。
//
// 参数:
//   input_a                第一个输入向量,按 float4 视角(设备指针)
//   input_b                第二个输入向量,按 float4 视角(设备指针)
//   output_c               输出向量,按 float4 视角(设备指针)
//   num_four_element_chunks float4 块数 = N / 4
// ---------------------------------------------------------------------------
__global__ void vector_add_vectorized_kernel(
    const float4* __restrict__ input_a,
    const float4* __restrict__ input_b,
    float4* __restrict__ output_c,
    int num_four_element_chunks) {
    // grid-stride loop:
    //   - 起始位置:本线程的全局下标
    //   - 每次迭代后步进 total_threads(整个网格的线程总数)
    //   效果:一个线程连续处理多个间隔为 total_threads 的块,
    //   相邻线程仍然访问相邻地址,内存合并不受影响。
    const int total_threads = gridDim.x * blockDim.x;

    for (int chunk_index = blockIdx.x * blockDim.x + threadIdx.x;
         chunk_index < num_four_element_chunks;
         chunk_index += total_threads) {
        // 一次 128-bit 向量化加载:编译器生成 LDG.E.128 指令,
        // 单条指令搬 16 字节(4 个 float)。
        const float4 a_values = input_a[chunk_index];
        const float4 b_values = input_b[chunk_index];

        // 逐分量相加,写回时同样是一条 STG.E.128。
        float4 sum;
        sum.x = a_values.x + b_values.x;
        sum.y = a_values.y + b_values.y;
        sum.z = a_values.z + b_values.z;
        sum.w = a_values.w + b_values.w;
        output_c[chunk_index] = sum;
    }
}

// ---------------------------------------------------------------------------
// 尾部核函数:处理 N 不是 4 的倍数时剩下的 0~3 个元素。
// 与基线版相同:每线程 1 元素 + 边界检查。
// 也可以用一个小的 grid-stride 循环核,这里用最直白的写法。
// ---------------------------------------------------------------------------
__global__ void vector_add_tail_kernel(const float* __restrict__ input_a,
                                       const float* __restrict__ input_b,
                                       float* __restrict__ output_c,
                                       int num_tail_elements) {
    const int tail_index = blockIdx.x * blockDim.x + threadIdx.x;
    if (tail_index < num_tail_elements) {
        output_c[tail_index] = input_a[tail_index] + input_b[tail_index];
    }
}

// ---------------------------------------------------------------------------
// solve:平台要求的入口,签名不能改。
// A、B、C 是设备指针(指向 GPU 显存),N 是元素个数。
// ---------------------------------------------------------------------------
extern "C" void solve(const float* A, const float* B, float* C, int N) {
    constexpr int kThreadsPerBlock = 256;
    constexpr int kElementsPerVector = 4;  // float4 承载 4 个 float

    // 把 N 拆成两部分:
    //   main_count  = N / 4  —— 完整 float4 块的个数(主核负责)
    //   tail_count  = N % 4  —— 剩下的 0~3 个元素(尾部核负责)
    //   tail_offset = N - tail_count —— 尾部段的起始下标(必为 4 的倍数,
    //   保证 A + tail_offset 的字节偏移仍是 16 的倍数,float4 对齐成立)
    const int main_chunk_count = N / kElementsPerVector;
    const int tail_element_count = N % kElementsPerVector;
    const int tail_start_index = N - tail_element_count;

    // ---- 主循环:float4 向量化 ----
    if (main_chunk_count > 0) {
        const int blocks_for_main =
            (main_chunk_count + kThreadsPerBlock - 1) / kThreadsPerBlock;

        // 把 float* 强转为 float4*:
        //   - 合法前提:cudaMalloc 返回的显存按 256B 对齐,基址满足 16B 对齐;
        //   - 主核处理的 chunk 数是整数,不会跨出分配范围。
        vector_add_vectorized_kernel<<<blocks_for_main, kThreadsPerBlock>>>(
            reinterpret_cast<const float4*>(A),
            reinterpret_cast<const float4*>(B),
            reinterpret_cast<float4*>(C),
            main_chunk_count);
    }

    // ---- 尾部:标量处理剩余 0~3 个元素 ----
    if (tail_element_count > 0) {
        const int blocks_for_tail =
            (tail_element_count + kThreadsPerBlock - 1) / kThreadsPerBlock;
        vector_add_tail_kernel<<<blocks_for_tail, kThreadsPerBlock>>>(
            A + tail_start_index, B + tail_start_index, C + tail_start_index,
            tail_element_count);
    }

    cudaDeviceSynchronize();
}
