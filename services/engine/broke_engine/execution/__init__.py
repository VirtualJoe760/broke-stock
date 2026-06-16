"""Execution: stable adapter interface + simulated (paper) matcher."""

from .adapter import ExecutionAdapter, Fill, Order, SimulatedMatcher

__all__ = ["ExecutionAdapter", "Order", "Fill", "SimulatedMatcher"]
