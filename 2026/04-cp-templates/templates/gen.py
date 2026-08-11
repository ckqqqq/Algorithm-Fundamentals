"""数据生成器模板：向 stdout 打印一组随机测试数据。

要点：
- 范围先调小（n <= 10），出错时反例才好看；对拍通过后再放大
- 覆盖边界：最小值、最大值、全相同、有序、逆序
"""
import random


def main():
    n = random.randint(1, 10)
    print(n)
    print(' '.join(str(random.randint(1, 100)) for _ in range(n)))


main()
