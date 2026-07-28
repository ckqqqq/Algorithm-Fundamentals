# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
# ─── How to run ───
# uv run min_cost_max_flow.py

from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class FlowResult:
    flow: int
    cost: int


@dataclass(frozen=True, slots=True)
class InvalidCapacityError(ValueError):
    capacity: int

    def __str__(self) -> str:
        return f"capacity must be non-negative, got {self.capacity}"


@dataclass(frozen=True, slots=True)
class InvalidVertexError(ValueError):
    vertex: int
    vertex_count: int

    def __str__(self) -> str:
        return f"vertex {self.vertex} is outside [0, {self.vertex_count})"


@dataclass(frozen=True, slots=True)
class InvalidFlowLimitError(ValueError):
    flow_limit: int

    def __str__(self) -> str:
        return f"flow_limit must be non-negative, got {self.flow_limit}"


@dataclass(slots=True)
class _Edge:
    """A mutable residual edge whose capacity changes during augmentation."""

    destination: int
    reverse_index: int
    capacity: int
    cost: int


@dataclass(frozen=True, slots=True)
class _ShortestPath:
    distance: int
    previous_vertex: tuple[int, ...]
    previous_edge: tuple[int, ...]


class MinCostMaxFlow:
    """A directed residual network for minimum-cost maximum-flow queries."""

    def __init__(self, vertex_count: int) -> None:
        if vertex_count <= 0:
            raise InvalidVertexError(vertex=vertex_count, vertex_count=vertex_count)
        self._vertex_count: Final = vertex_count
        self._graph: list[list[_Edge]] = [[] for _ in range(vertex_count)]

    def add_edge(self, source: int, destination: int, capacity: int, cost: int) -> None:
        self._ensure_vertex(source)
        self._ensure_vertex(destination)
        if capacity < 0:
            raise InvalidCapacityError(capacity=capacity)

        forward = _Edge(
            destination=destination,
            reverse_index=len(self._graph[destination]),
            capacity=capacity,
            cost=cost,
        )
        reverse = _Edge(
            destination=source,
            reverse_index=len(self._graph[source]),
            capacity=0,
            cost=-cost,
        )
        self._graph[source].append(forward)
        self._graph[destination].append(reverse)

    def solve(
        self, source: int, sink: int, flow_limit: int | None = None
    ) -> FlowResult:
        self._ensure_vertex(source)
        self._ensure_vertex(sink)
        if flow_limit is not None and flow_limit < 0:
            raise InvalidFlowLimitError(flow_limit=flow_limit)
        if source == sink:
            return FlowResult(flow=0, cost=0)

        remaining = (
            flow_limit
            if flow_limit is not None
            else sum(edge.capacity for edge in self._graph[source])
        )
        total_flow = 0
        total_cost = 0

        while remaining > 0:
            path = self._find_shortest_path(source=source, sink=sink)
            if path is None:
                break

            added_flow = remaining
            vertex = sink
            while vertex != source:
                previous_vertex = path.previous_vertex[vertex]
                edge = self._graph[previous_vertex][path.previous_edge[vertex]]
                added_flow = min(added_flow, edge.capacity)
                vertex = previous_vertex

            vertex = sink
            while vertex != source:
                previous_vertex = path.previous_vertex[vertex]
                edge_index = path.previous_edge[vertex]
                edge = self._graph[previous_vertex][edge_index]
                edge.capacity -= added_flow
                self._graph[vertex][edge.reverse_index].capacity += added_flow
                vertex = previous_vertex

            total_flow += added_flow
            total_cost += added_flow * path.distance
            remaining -= added_flow

        return FlowResult(flow=total_flow, cost=total_cost)

    def _find_shortest_path(self, source: int, sink: int) -> _ShortestPath | None:
        distances: list[int | None] = [None] * self._vertex_count
        previous_vertex = [-1] * self._vertex_count
        previous_edge = [-1] * self._vertex_count
        queued = [False] * self._vertex_count
        queue = deque([source])
        distances[source] = 0
        queued[source] = True

        while queue:
            vertex = queue.popleft()
            queued[vertex] = False
            vertex_distance = distances[vertex]
            if vertex_distance is None:
                continue

            for edge_index, edge in enumerate(self._graph[vertex]):
                candidate = vertex_distance + edge.cost
                destination_distance = distances[edge.destination]
                if edge.capacity <= 0 or (
                    destination_distance is not None
                    and candidate >= destination_distance
                ):
                    continue
                distances[edge.destination] = candidate
                previous_vertex[edge.destination] = vertex
                previous_edge[edge.destination] = edge_index
                if not queued[edge.destination]:
                    queue.append(edge.destination)
                    queued[edge.destination] = True

        sink_distance = distances[sink]
        if sink_distance is None:
            return None
        return _ShortestPath(
            distance=sink_distance,
            previous_vertex=tuple(previous_vertex),
            previous_edge=tuple(previous_edge),
        )

    def _ensure_vertex(self, vertex: int) -> None:
        if vertex < 0 or vertex >= self._vertex_count:
            raise InvalidVertexError(vertex=vertex, vertex_count=self._vertex_count)


def _example() -> FlowResult:
    graph = MinCostMaxFlow(vertex_count=4)
    graph.add_edge(0, 1, capacity=2, cost=1)
    graph.add_edge(0, 2, capacity=1, cost=2)
    graph.add_edge(1, 2, capacity=1, cost=0)
    graph.add_edge(1, 3, capacity=1, cost=3)
    graph.add_edge(2, 3, capacity=2, cost=1)
    return graph.solve(source=0, sink=3)


def main() -> None:
    result = _example()
    print(json.dumps({"flow": result.flow, "cost": result.cost}))


if __name__ == "__main__":
    main()
