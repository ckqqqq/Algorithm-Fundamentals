# vector_add_jax.py —— LeetGPU "Vector Addition" JAX 版
#
# JAX 的契约与其他框架不同:不传输出张量 C,而是直接 return 结果张量。
# @jax.jit 会把 Python 函数编译成 XLA 设备内核(自动向量化、自动合并内存访问),
# 一行 `A + B` 即可,平台内部会把它放到 GPU 上执行。
#
# 注意:本文件的意义主要是"理解契约差异"——JAX 版不写显式循环,
# 正确性由 XLA 保证,无法(也不需要)手动调优。

import jax
import jax.numpy as jnp


# A、B 是设备上的张量,N 是元素个数(长度由张量形状决定,这里只做一致性校验用)
@jax.jit
def solve(A: jax.Array, B: jax.Array, N: int) -> jax.Array:
    # return output tensor directly
    # XLA 会把逐元素加法编译为 element-wise 设备内核,并保证广播语义
    return A + B
