"""Coordinate-wise trimmed-mean aggregation."""
import math
from typing import Optional
import numpy as np
from src.common import Message, SENTINEL
from src.comms.interface import BaseProtocol, EnvState

class TrimmedMeanProtocol(BaseProtocol):
    def __init__(self, trim_fraction: float = 0.2) -> None:
        if not 0.0 <= trim_fraction < 0.5:
            raise ValueError("trim_fraction must be in [0.0, 0.5)")
        self._trim_fraction = trim_fraction

    def send(self, agent_id: str, state: EnvState) -> Message:
        # Faithful to the final team experiment: communicating protocols
        # use the environment-provided true_hider_pos (oracle-style signal),
        # not the visibility-limited obs[2:4]. See docs/IMPLEMENTATION_LIMITATION.md.
        x, y = state.true_hider_pos
        return Message(agent_id, x, y, state.step)

    def receive(self, messages: list[Optional[Message]]) -> dict[str, tuple[float, float]]:
        valid = [m for m in messages if m is not None]
        if not valid:
            return {}
        xs = [m.believed_hider_x for m in valid if m.believed_hider_x is not None]
        ys = [m.believed_hider_y for m in valid if m.believed_hider_y is not None]
        cx = self._trimmed_mean(xs)
        cy = self._trimmed_mean(ys)
        return {m.sender_id: (cx, cy) for m in valid}

    def _trimmed_mean(self, values: list[float]) -> float:
        if not values:
            return float(SENTINEL)
        if len(values) < 3:
            return float(np.mean(values))
        k = math.floor(len(values) * self._trim_fraction)
        vals = sorted(values)
        vals = vals[k:len(vals)-k] if k else vals
        return float(np.mean(vals)) if vals else float(SENTINEL)
