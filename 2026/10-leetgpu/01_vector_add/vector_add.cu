// vector_add.cu —— LeetGPU "Vector Addition" 基线解法(正确性优先)
//
// 思路:每个线程处理一个输出元素 (one thread per element)。
// 这是最简单、最容易验证正确的 CUDA 形态,也是理解后面所有优化的起点。
//
// 关键概念:
//   - Grid(网格)= 若干 Block(线程块);Block = 若干 Thread(线程)
//   - 一个线程的"全局下标" = blockIdx.x * blockDim.x + threadIdx.x
//   - 相邻线程访问相邻地址 => 内存合并(memory coalescing),一次事务搬 128B

#include <cuda_runtime.h>

// ---------------------------------------------------------------------------
// 核函数:每个线程负责计算一个输出元素
//
// 参数:
//   input_a      第一个输入向量(设备指针)
//   input_b      第二个输入向量(设备指针)
//   output_c     输出向量(设备指针),存放逐元素之和
//   num_elements 向量长度 N
// ---------------------------------------------------------------------------
__global__ void vector_add_kernel(const float* input_a,
                                  const float* input_b,
                                  float* output_c,
                                  int num_elements) {
    // 当前线程在整个网格中的全局下标:
    //   blockIdx.x : 本线程所在 block 的编号
    //   blockDim.x : 每个 block 的线程数
    //   threadIdx.x: 本线程在 block 内的编号
    int global_index = blockIdx.x * blockDim.x + threadIdx.x;

    // 边界检查:最后一个 block 可能超出 N,越界的线程直接退出。
    // (N 恰好被整除时,这个分支恒真,编译器能把它优化掉。)
    if (global_index < num_elements) {
        output_c[global_index] = input_a[global_index] + input_b[global_index];
    }
}

// ---------------------------------------------------------------------------
// solve:平台要求的入口,签名不能改。
// A、B、C 是设备指针(指向 GPU 显存),N 是元素个数。
// ---------------------------------------------------------------------------
extern "C" void solve(const float* A, const float* B, float* C, int N) {
    // 每个 block 放 256 个线程(经验值;128/256/512 对 element-wise 都合理)
    const int threads_per_block = 256;

    // block 数量 = 向上取整(N / 256),保证每个元素至少被一个线程覆盖。
    // 例如 N = 1000 -> (1000 + 255) / 256 = 4 个 block,共 1024 个线程,
    // 多出的 24 个线程被边界检查拦住。
    const int blocks_per_grid = (N + threads_per_block - 1) / threads_per_block;

    // 启动核函数:<<<grid 规模, block 规模>>>
    vector_add_kernel<<<blocks_per_grid, threads_per_block>>>(A, B, C, N);

    // 同步等待核函数执行完毕。
    // LeetGPU 的计时以"核函数完整执行"为准,显式同步避免异步启动造成计时偏差。
    cudaDeviceSynchronize();
}
