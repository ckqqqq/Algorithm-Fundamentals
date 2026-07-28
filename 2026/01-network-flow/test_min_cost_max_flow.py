from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import min_cost_max_flow as mcmf


def test_finds_maximum_flow_with_minimum_cost() -> None:
    # Given
    graph = mcmf.MinCostMaxFlow(vertex_count=4)
    graph.add_edge(0, 1, capacity=2, cost=1)
    graph.add_edge(0, 2, capacity=1, cost=2)
    graph.add_edge(1, 2, capacity=1, cost=0)
    graph.add_edge(1, 3, capacity=1, cost=3)
    graph.add_edge(2, 3, capacity=2, cost=1)

    # When
    result = graph.solve(source=0, sink=3)

    # Then
    assert result == mcmf.FlowResult(flow=3, cost=9)


def test_supports_negative_edge_costs_without_negative_cycles() -> None:
    # Given
    graph = mcmf.MinCostMaxFlow(vertex_count=3)
    graph.add_edge(0, 1, capacity=1, cost=-2)
    graph.add_edge(1, 2, capacity=1, cost=1)
    graph.add_edge(0, 2, capacity=1, cost=4)

    # When
    result = graph.solve(source=0, sink=2)

    # Then
    assert result == mcmf.FlowResult(flow=2, cost=3)


def test_respects_requested_flow_limit() -> None:
    # Given
    graph = mcmf.MinCostMaxFlow(vertex_count=2)
    graph.add_edge(0, 1, capacity=5, cost=3)

    # When
    result = graph.solve(source=0, sink=1, flow_limit=2)

    # Then
    assert result == mcmf.FlowResult(flow=2, cost=6)


def test_rejects_negative_capacity() -> None:
    # Given
    graph = mcmf.MinCostMaxFlow(vertex_count=2)

    # When / Then
    with pytest.raises(mcmf.InvalidCapacityError):
        graph.add_edge(0, 1, capacity=-1, cost=0)


def test_cli_prints_example_result_as_json() -> None:
    # Given
    script = Path(__file__).with_name("min_cost_max_flow.py")

    # When
    completed = subprocess.run(
        [sys.executable, str(script)],
        check=False,
        capture_output=True,
        text=True,
    )

    # Then
    assert completed.returncode == 0
    assert json.loads(completed.stdout) == {"flow": 3, "cost": 9}
