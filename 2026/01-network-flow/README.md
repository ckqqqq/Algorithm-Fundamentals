# 最小费用最大流

`min_cost_max_flow.py` 使用残量网络和 SPFA 最短增广路实现最小费用最大流，支持负费用边（图中不应包含可达的负费用环）。

运行示例：

```bash
uv run min_cost_max_flow.py
```

输出：

```json
{"flow": 3, "cost": 9}
```

作为模块使用：

```python
from min_cost_max_flow import MinCostMaxFlow

graph = MinCostMaxFlow(vertex_count=3)
graph.add_edge(0, 1, capacity=2, cost=1)
graph.add_edge(1, 2, capacity=2, cost=3)
result = graph.solve(source=0, sink=2)
print(result.flow, result.cost)
```

设每轮增广前 SPFA 的复杂度为 `O(VE)`，最多执行 `A` 轮增广，总时间复杂度为 `O(AVE)`，空间复杂度为 `O(V + E)`。
