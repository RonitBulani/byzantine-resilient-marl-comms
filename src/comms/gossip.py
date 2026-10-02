"""Random-fanout gossip protocol."""
from typing import Optional
import numpy as np
from src.common import Message, SENTINEL
from src.comms.interface import BaseProtocol, EnvState

class GossipProtocol(BaseProtocol):
    def __init__(self, fanout: int = 2, seed: int = 0) -> None:
        if fanout < 0:
            raise ValueError("fanout must be >= 0")
        self._fanout = fanout
        self._seed = seed
        self._rng = np.random.default_rng(seed)

    def reset(self) -> None:
        self._rng = np.random.default_rng(self._seed)

    def send(self, agent_id: str, state: EnvState) -> Message:
        # Faithful to the final team experiment: communicating protocols
        # use the environment-provided true_hider_pos (oracle-style signal),
        # not the visibility-limited obs[2:4]. See docs/IMPLEMENTATION_LIMITATION.md.
        x, y = state.true_hider_pos
        return Message(agent_id, x, y, state.step)

    def receive(self, messages: list[Optional[Message]]) -> dict[str, tuple[float, float]]:
        valid = [m for m in messages if m is not None]
        n_select = min(self._fanout, len(valid))
        if n_select == 0:
            return {}
        idx = self._rng.choice(len(valid), size=n_select, replace=False)
        selected = [valid[i] for i in sorted(idx)]
        out = {}
        for msg in selected:
            x = msg.believed_hider_x if msg.believed_hider_x is not None else SENTINEL
            y = msg.believed_hider_y if msg.believed_hider_y is not None else SENTINEL
            out[msg.sender_id] = (float(x), float(y))
        return out
