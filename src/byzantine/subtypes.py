"""Four communication-only Byzantine attack models."""
from typing import Callable
import numpy as np
from src.common import Message
from src.comms.interface import ByzantineAgent

class RandomNoiseByzantine(ByzantineAgent):
    def __init__(self, agent_id: str, grid_size: int, seed: int | None = None):
        self.agent_id = agent_id
        self.grid_size = grid_size
        self.rng = np.random.default_rng(seed)

    def corrupt_message(self, honest_message: Message) -> Message:
        norm = float(self.grid_size - 1)
        x = float(self.rng.integers(0, self.grid_size)) / norm
        y = float(self.rng.integers(0, self.grid_size)) / norm
        return Message(honest_message.sender_id, x, y, honest_message.step)

class MisdirectionByzantine(ByzantineAgent):
    """Worst-case omniscient attacker that reflects the true hider position."""
    def __init__(
        self,
        agent_id: str,
        grid_size: int,
        get_true_hider_pos: Callable[[], tuple[int, int]],
        get_agent_pos: Callable[[], tuple[int, int]],
    ):
        self.agent_id = agent_id
        self.grid_size = grid_size
        self._get_true_hider_pos = get_true_hider_pos
        self._get_agent_pos = get_agent_pos

    def corrupt_message(self, honest_message: Message) -> Message:
        ax, ay = self._get_agent_pos()
        hx, hy = self._get_true_hider_pos()
        rx = int(np.clip(2 * ax - hx, 0, self.grid_size - 1))
        ry = int(np.clip(2 * ay - hy, 0, self.grid_size - 1))
        norm = float(self.grid_size - 1)
        return Message(honest_message.sender_id, rx / norm, ry / norm, honest_message.step)

class SpoofingByzantine(ByzantineAgent):
    def __init__(self, agent_id: str, all_seeker_ids: list[str], seed: int | None = None):
        self.agent_id = agent_id
        self._other_ids = [x for x in all_seeker_ids if x != agent_id]
        self.rng = np.random.default_rng(seed)

    def corrupt_message(self, honest_message: Message) -> Message:
        if not self._other_ids:
            return honest_message
        fake = self._other_ids[int(self.rng.integers(0, len(self._other_ids)))]
        return Message(fake, honest_message.believed_hider_x, honest_message.believed_hider_y, honest_message.step)

class SilentByzantine(ByzantineAgent):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def corrupt_message(self, honest_message: Message) -> None:
        return None
