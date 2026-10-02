"""Unfiltered broadcast communication baseline."""
from typing import Optional
from src.common import Message, SENTINEL
from src.comms.interface import BaseProtocol, EnvState

class BroadcastProtocol(BaseProtocol):
    def send(self, agent_id: str, state: EnvState) -> Message:
        # Faithful to the final team experiment: communicating protocols
        # use the environment-provided true_hider_pos (oracle-style signal),
        # not the visibility-limited obs[2:4]. See docs/IMPLEMENTATION_LIMITATION.md.
        x, y = state.true_hider_pos
        return Message(agent_id, x, y, state.step)

    def receive(self, messages: list[Optional[Message]]) -> dict[str, tuple[float, float]]:
        buffer = {}
        for msg in messages:
            if msg is None:
                continue
            x = msg.believed_hider_x if msg.believed_hider_x is not None else SENTINEL
            y = msg.believed_hider_y if msg.believed_hider_y is not None else SENTINEL
            buffer[msg.sender_id] = (float(x), float(y))
        return buffer
