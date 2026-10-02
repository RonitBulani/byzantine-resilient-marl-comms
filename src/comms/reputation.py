"""Reputation-based resilient aggregation."""
from typing import Optional
import numpy as np
from src.common import Message, SENTINEL
from src.comms.interface import BaseProtocol, EnvState

class ReputationProtocol(BaseProtocol):
    def __init__(
        self,
        min_trust: float = 0.3,
        deviation_threshold: float = 0.1,
        trust_increment: float = 0.1,
        trust_decrement: float = 0.1,
    ) -> None:
        if not 0.0 < min_trust <= 1.0:
            raise ValueError("min_trust must be in (0, 1]")
        if deviation_threshold < 0:
            raise ValueError("deviation_threshold must be >= 0")
        self._min_trust = min_trust
        self._threshold = deviation_threshold
        self._inc = trust_increment
        self._dec = trust_decrement
        self._scores: dict[str, float] = {}

    @property
    def trust_scores(self) -> dict[str, float]:
        return dict(self._scores)

    def reset(self) -> None:
        self._scores = {k: 1.0 for k in self._scores}

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

        for m in valid:
            self._scores.setdefault(m.sender_id, 1.0)

        trusted = [m for m in valid if self._scores[m.sender_id] >= self._min_trust]
        pool = trusted if trusted else valid
        cx, cy = self._mean_position(pool)

        for m in valid:
            x = m.believed_hider_x if m.believed_hider_x is not None else SENTINEL
            y = m.believed_hider_y if m.believed_hider_y is not None else SENTINEL
            if cx == SENTINEL or cy == SENTINEL:
                deviation = 0.0
            elif x == SENTINEL or y == SENTINEL:
                deviation = float("inf")
            else:
                deviation = float(np.hypot(x - cx, y - cy))

            if deviation > self._threshold:
                self._scores[m.sender_id] = max(0.0, self._scores[m.sender_id] - self._dec)
            else:
                self._scores[m.sender_id] = min(1.0, self._scores[m.sender_id] + self._inc)

        active = trusted if trusted else valid
        return {m.sender_id: (cx, cy) for m in active}

    @staticmethod
    def _mean_position(messages: list[Message]) -> tuple[float, float]:
        xs = [m.believed_hider_x for m in messages if m.believed_hider_x is not None]
        ys = [m.believed_hider_y for m in messages if m.believed_hider_y is not None]
        return (
            float(np.mean(xs)) if xs else float(SENTINEL),
            float(np.mean(ys)) if ys else float(SENTINEL),
        )
