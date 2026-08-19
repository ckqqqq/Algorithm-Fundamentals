# vector_add_triton.py —— LeetGPU "Vector Addition" Triton 版
#
# Triton 是 OpenAI 开发的 GPU 编程语言/编译器:用 Python 写核函数,
# 编译器自动完成线程映射、向量化(128-bit 访问)、内存合并等底层优化。
# 相比手写 CUDA,Triton 的代码量小很多,性能通常接近手写最优。
#
# 契约:a、b、c 是 GPU 上的张量,N 是元素个数,结果写入 c。

import torch
import triton
import triton.language as tl


@triton.jit
def vector_add_kernel(
    a_ptr,            # 输入向量 a 的指针
    b_ptr,            # 输入向量 b 的指针
    c_ptr,            # 输出向量 c 的指针
    n_elements,       # 总元素个数 N
    BLOCK_SIZE: tl.constexpr,  # 每个 program(相当于一个 block)处理的元素数
):
    """逐元素相加:a[i] + b[i] -> c[i]。

    Triton 模型:把数组切成若干 program,每个 program 处理 BLOCK_SIZE 个元素。
    program_id 相当于 CUDA 的 blockIdx,BLOCK_SIZE 相当于 blockDim。
    """
    # 当前 program 的编号
    program_id = tl.program_id(axis=0)

    # 本 program 负责的元素下标区间:[program_id * BLOCK_SIZE, (pid+1) * BLOCK_SIZE)
    element_offsets = program_id * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)

    # 边界掩码:最后一个 program 可能越界,越界的元素不读写
    load_mask = element_offsets < n_elements

    # 向量化加载(编译器自动合并/向量化),越界位置返回任意值(不参与存储)
    a_values = tl.load(a_ptr + element_offsets, mask=load_mask)
    b_values = tl.load(b_ptr + element_offsets, mask=load_mask)

    # 逐元素相加
    sum_values = a_values + b_values

    # 带掩码写回,越界位置不写
    tl.store(c_ptr + element_offsets, sum_values, mask=load_mask)


# a、b、c 是 GPU 上的张量
def solve(a: torch.Tensor, b: torch.Tensor, c: torch.Tensor, N: int):
    # 每个 program 处理 1024 个元素(经验值;Triton 内部还会再分块向量化)
    BLOCK_SIZE = 1024

    # grid = program 数量 = 向上取整(N / BLOCK_SIZE)
    grid = (triton.cdiv(N, BLOCK_SIZE),)

    # 启动核函数
    vector_add_kernel[grid](a, b, c, N, BLOCK_SIZE)
