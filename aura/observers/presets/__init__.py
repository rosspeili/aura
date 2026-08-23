"""Packaged observer presets (monitor, break, …)."""

from aura.observers.presets.break_observer import BreakObserver, create_break_observer
from aura.observers.presets.monitor import MonitorObserver, create_monitor_observer

__all__ = [
    "BreakObserver",
    "MonitorObserver",
    "create_break_observer",
    "create_monitor_observer",
]
