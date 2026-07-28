# Problem 3: Prefix Cache (RadixAttention)

## Background

LLM 推理服务（如 SGLang 的 RadixAttention）将历史请求的 KV cache 组织成一棵**前缀树（Trie）**：当新请求到来时，若其 prompt 与缓存共享某个前缀，则共享部分的 KV 无需重新计算，可以直接复用。缓存容量有限；当缓存满时，按照 **LRU**（最近最少使用）策略驱逐节点——被驱逐的节点必须是叶子节点（若某节点被驱逐，其整棵子树必须已经不在缓存中）。

给定缓存容量和依次到达的请求序列，求所有请求的总命中次数。

## Problem Description

缓存是一棵 Trie，每个节点对应一个 token，根节点为空。缓存最多容纳 $C$ 个节点（根节点不计入容量）。

按顺序处理 $Q$ 个请求，每个请求是一个 token 序列。对每个请求：

1. 在 Trie 中找出该序列与当前缓存的**最长公共前缀**，匹配到的节点数即为该请求的命中次数；
2. 将该请求序列中尚未缓存的节点逐个插入 Trie。每次插入之前，若缓存已满，必须反复执行驱逐直到有足够空间：
   - 驱逐规则：在当前缓存的**叶子节点**中，删除**最近最少被访问**的那个叶子（访问 = 某次请求的最长前缀匹配经过了该节点，或该节点是最近某个请求新插入的；每个请求会更新其匹配路径上所有节点以及所有新插入节点的访问时间；越晚的访问时间戳越大；时间戳相同时按节点编号较小者优先）。
   - 被删除节点的 KV 被释放，其父节点可能成为新的叶子。
3. 每个请求的序列长度不超过缓存容量 $C$，因此插入总能保证完成。

输出所有请求的命中次数之和。

## Input Format

第一行包含两个整数 $C, Q$（$1 \le C \le 10^5$，$1 \le Q \le 10^5$）。

接下来 $Q$ 行，每行以一个整数 $L$（$1 \le L \le C$）开头，后跟 $L$ 个整数 $a_1, a_2, \ldots, a_L$（$1 \le a_i \le 10^9$），表示一个请求的 token 序列。

保证所有请求的序列长度之和不超过 $2 \times 10^5$。

## Output Format

一个整数：所有请求的命中次数之和。

## Sample Input

```
4 4
3 1 2 3
3 1 2 4
2 1 5
3 1 2 3
```

## Sample Output

```
5
```

## Sample Explanation

缓存容量 $C = 4$。

- **请求 1** `[1,2,3]`：Trie 为空，命中 0 次。插入节点 1、2、3（占用 3 个槽位）。
- **请求 2** `[1,2,4]`：最长公共前缀为 `[1,2]`，命中 2 次。插入节点 4（4 个槽位全部被占用：1、2、3、4）。
- **请求 3** `[1,5]`：最长公共前缀为 `[1]`，命中 1 次。需要插入节点 5，但缓存已满。当前叶子为 3 和 4：节点 3 最后访问于请求 1，节点 4 最后访问于请求 2，因此驱逐 3。插入 5（节点：1、2、4、5）。
- **请求 4** `[1,2,3]`：最长公共前缀为 `[1,2]`（节点 3 已被驱逐），命中 2 次。插入 3：缓存已满；当前叶子为 4 和 5，节点 4 最后访问于请求 2，节点 5 最后访问于请求 3，因此驱逐 4，插入 3。

总命中次数：$0 + 2 + 1 + 2 = 5$。

## Solution

**数据结构**：Trie + LRU。关键点：

1. 每个 Trie 节点存储：子节点映射（`unordered_map`，或离散化后用数组）、父指针、最后访问时间戳、节点编号。
2. **维护 LRU**：经典做法是用一个 `std::set` 按 (时间戳, 节点编号) 排序维护所有**叶子**节点。每个请求结束后，更新匹配路径与新插入路径上各节点的时间戳；叶子集合随插入/删除而变化：
   - 插入新节点：新节点是叶子，加入集合；若其父节点原本是叶子，则从集合中移除。
   - 驱逐：取出集合中最小元素并删除，然后检查其父节点是否变成叶子。
3. 更新节点时间戳不会影响其在集合中的位置——**只有叶子在集合中**，路径上的内部节点不在，因此只需处理两类事件：“因插入而不再是叶子”和“因删除而成为叶子”，每次操作复杂度 $O(\log C)$。

**复杂度**：设序列总长度为 $S \le 2 \times 10^5$，总复杂度为 $O(S \log C)$。

**常见坑点**：

- 只有叶子可以被驱逐；内部节点绝不能删除（否则其后代的 KV 会悬空）——这正是 RadixAttention 与朴素 LRU 的关键区别。
- 时间戳相同时（同一请求内插入的多个节点），按节点编号或插入顺序作为平局裁决，与题面保持一致。
- 单个请求可能触发多次驱逐。

**进一步思考**：真实系统中，驱逐的粒度是“前缀子树”，且需要处理并发请求共享缓存的问题；本题还可以扩展为带权驱逐（不同的 KV 大小，例如 GQA 中不同的 head 数），这就变成树上的带权缓存问题。

## Reference Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
    unordered_map<int, int> ch;
    int fa = -1;  // 父节点
    int up = -1;  // 父节点指向该节点的边上的 token
    int ts = 0;   // 最后访问时间戳
};

int main() {
    int C, Q;
    scanf("%d %d", &C, &Q);
    vector<Node> tr(1);          // 节点 0 是根
    int used = 0;                // 已缓存的节点数（不含根）
    long long hit = 0;
    int timer = 0;
    set<pair<int,int>> leaves;   // 叶子集合：(时间戳, 节点编号)

    auto isLeaf = [&](int u) { return u != 0 && tr[u].ch.empty(); };

    for (int qi = 0; qi < Q; qi++) {
        int L;
        scanf("%d", &L);
        vector<int> a(L);
        for (auto &x : a) scanf("%d", &x);

        // 1. 沿 Trie 匹配最长前缀
        int cur = 0;
        vector<int> path;        // 本请求经过的节点
        for (int k = 0; k < L; k++) {
            auto it = tr[cur].ch.find(a[k]);
            if (it == tr[cur].ch.end()) break;
            cur = it->second;
            path.push_back(cur);
        }
        hit += (int)path.size();

        // 2. 插入未匹配的后缀
        for (int k = (int)path.size(); k < L; k++) {
            int parent = path.empty() ? 0 : path.back();
            // 空间不足时驱逐 LRU 叶子
            while (used >= C) {
                auto it = leaves.begin();
                int u = it->second;
                leaves.erase(it);
                int p = tr[u].fa;
                tr[p].ch.erase(tr[u].up);
                used--;
                if (isLeaf(p)) leaves.insert({tr[p].ts, p});
            }
            int u = (int)tr.size();
            tr.push_back(Node());
            tr[u].fa = parent;
            tr[u].up = a[k];
            if (parent != 0 && tr[parent].ch.empty())
                leaves.erase({tr[parent].ts, parent}); // 父节点不再是叶子
            tr[parent].ch[a[k]] = u;
            leaves.insert({tr[u].ts, u});              // 新叶子；时间戳稍后统一更新
            used++;
            path.push_back(u);
        }

        // 3. 更新本请求经过的所有节点的时间戳
        for (int u : path) {
            if (isLeaf(u)) leaves.erase({tr[u].ts, u});
            tr[u].ts = ++timer;
            if (isLeaf(u)) leaves.insert({tr[u].ts, u});
        }
    }
    printf("%lld\n", hit);
    return 0;
}
```
