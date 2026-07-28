# Gradient Checkpointing

## Background

训练 LLM 时，反向传播需要前向传播中每一层的激活值。但当模型过大时，显存无法容纳所有激活值。**梯度检查点**（gradient checkpointing）技术只保存部分层的激活值；其余层在反向传播需要时通过重新执行前向传播来重算。

给定一个 $n$ 层的网络（链式结构；第 $1$ 层的输入已被免费保存），第 $i$ 层的激活值占用 $m_i$ 内存，重算第 $i$ 层需要 $t_i$ 时间。内存容量为 $M$。当反向传播经过每一层时，必须能够从某个已保存的检查点开始重算到该层。求最小总重算时间。

## Description

网络是一条链 $1 \to 2 \to \cdots \to n$。位置 $0$ 处的激活值（即输入）被免费保存，不占用内存。你可以选择若干层作为检查点来保存其激活值；所有检查点占用的内存之和不得超过 $M$。

当反向传播到达第 $i$ 层时，如果第 $i$ 层本身是检查点，其激活值已被保存，代价为 $0$；否则，找到它之前最近的检查点 $j$（$j < i$；位置 $0$ 也算作检查点），则必须重算第 $j+1, j+2, \ldots, i$ 层，代价为 $t_{j+1} + t_{j+2} + \cdots + t_i$。总代价为所有 $n$ 层代价之和。求最小总代价。

## Input Format

第一行包含两个整数 $n, M$（$1 \le n \le 2000$，$1 \le M \le 10^9$）。

接下来 $n$ 行，每行包含两个整数 $m_i, t_i$（$1 \le m_i \le M$，$1 \le t_i \le 10^4$），分别表示第 $i$ 层的内存占用和重算时间。

## Output Format

输出一个整数：最小总重算时间。

## Sample Input

```
4 10
3 5
4 2
3 8
4 1
```



## Sample Output

```
1
```



## Sample Explanation

规则：如果第 $i$ 层本身是检查点，那么当反向传播到达它时其激活值已被保存，因此重算代价为 $0$。

最优方案：选择第 1、2、3 层作为检查点（内存 $3+4+3=10 \le 10$）。

- 第 1、2、3 层：它们本身是检查点，所以代价均为 $0$
- 第 4 层：从最近的检查点 3 开始重算，代价为 $t_4 = 1$

总代价为 $1$。无法更优：保存全部 4 层需要内存 $14 > 10$，所以第 4 层代价为 $0$ 至多只能在一种情况下成立（它自身是检查点），但此时第 1、2 层中至少有一层需要重算（内存不足以同时保存第 1、2、4 层），代价至少为 $\min(t_1, t_2) = 2 > 1$。因此最小总代价为 $1$。

## Solution

**建模**：经典的"分段 DP"问题。

设 $dp[i]$ 表示处理完前 $i$ 层、且第 $i$ 层被选为检查点时的最小总代价。转移时枚举前一个检查点 $j$：

$$dp[i] = \min_{j < i, \text{feasible}} \left dp[j] + \text{cost}(j, i) \right$$

其中 $\text{cost}(j, i)$ 表示在"区间 $(j, i)$ 内没有检查点且 $i$ 是检查点"时，第 $j+1, \ldots, i-1$ 层的重算代价之和（第 $i$ 层是检查点，代价为 $0$）。令 $T_i = \sum_{k=1}^{i} t_k$ 为前缀和；当反向传播到达第 $p$ 层（$j < p < i$）时，代价为 $T_p - T_j$，所以：

$$\text{cost}(j, i) = \sum_{p=j+1}^{i-1} (T_p - T_j)$$

最后一个检查点 $i$ 之后的层也必须计费：$\text{tail}(i) = \sum_{p=i+1}^{n} (T_p - T_i)$，答案为 $\min_i  dp[i] + \text{tail}(i) $（包括 $i = 0$，即完全不设检查点的情况）。

**处理内存约束**：$M$ 太大，不能直接作为背包维度。注意到 $n \le 2000$，因此可以按"检查点个数"离散化，或直接按内存离散化：检查点至多有 $n$ 个；用 $dp[i][k]$ 表示前 $i$ 层选了 $k$ 个检查点，再利用下界 $k \cdot m$ 或直接在每个状态中记录最小内存占用。一个更简洁的做法：由于每层的内存满足 $m_i \le M$，当不同内存取值的数量较小时，可以用 `unordered_map` 做稀疏 DP；对于典型的竞赛数据范围，$O(n^2)$ 的转移枚举加上内存维度的可行性剪枝就足够了。

**复杂度**：状态转移为 $O(n^2)$；对内存维度稀疏化后，整体复杂度为 $O(n^2)$。

**进一步思考**：真实的梯度检查点（例如陈天奇的 *Training Deep Nets with Sublinear Memory Cost*）将任意计算图（DAG）上的检查点选择建模为**最小割**问题——这是本题从链到一般图的推广。

## Reference Code (C++, chain + sparse memory)

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll INF = 4e18;

int main() {
    int n; ll M;
    scanf("%d %lld", &n, &M);
    vector<ll> m(n + 1), t(n + 1), T(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        scanf("%lld %lld", &m[i], &t[i]);
        T[i] = T[i - 1] + t[i];
    }
    // 预处理：seg[j][i] = sum_{p=j+1..i} (T[p]-T[j])（包含第 i 层），O(n^2)
    vector<vector<ll>> seg(n + 1, vector<ll>(n + 1, 0));
    for (int j = 0; j <= n; j++)
        for (int i = j + 1; i <= n; i++)
            seg[j][i] = seg[j][i - 1] + T[i] - T[j];
    // 状态：对每个位置 i（作为检查点），维护一个 (内存 -> 最小代价) 的 Pareto 前沿
    vector<map<ll, ll>> pareto(n + 1);
    pareto[0][0] = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            for (auto &[mem, cost] : pareto[j]) {
                ll nm = mem + m[i];
                if (nm > M) continue;
                // 第 j+1..i-1 层从检查点 j 重算；第 i 层是检查点，代价为 0
                ll nc = cost + seg[j][i - 1];
                // 插入并维护 Pareto 前沿
                auto it = pareto[i].lower_bound(nm);
                if (it != pareto[i].begin() && prev(it)->second <= nc) continue;
                if (it != pareto[i].end() && it->first == nm && it->second <= nc) continue;
                pareto[i][nm] = nc;
                // 删除被支配的条目
                it = pareto[i].find(nm);
                auto nit = next(it);
                while (nit != pareto[i].end() && nit->second >= nc) {
                    nit = pareto[i].erase(nit);
                }
            }
        }
    }
    // 答案：最后一个检查点 i（包括 i=0，即不设检查点）加上其后各层的重算代价
    ll ans = INF;
    for (int i = 0; i <= n; i++)
        for (auto &[mem, cost] : pareto[i])
            ans = min(ans, cost + seg[i][n]);
    printf("%lld\n", ans);
    return 0;
}
```
