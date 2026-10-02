"""Communication interfaces adapted from the original Role C subsystem."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import numpy as np

from src.common import Message, SENTINEL

@dataclass
class EnvState:
    obs: np.ndarray
    step: int
    grid_size: int
    # Environment-provided true position used by the final team communication experiment.
    true_hider_pos: tuple[float, float]

class BaseProtocol(ABC):
    def reset(self) -> None:
        pass

    @abstractmethod
    def send(self, agent_id: str, state: EnvState) -> Message:
        ...

    @abstractmethod
    def receive(self, messages: list[Optional[Message]]) -> dict[str, tuple[float, float]]:
        ...

class ByzantineAgent(ABC):
    @abstractmethod
    def corrupt_message(self, honest_message: Message) -> Optional[Message]:
        ...

class NoneProtocol(BaseProtocol):
    """No-communication baseline."""
    def send(self, agent_id: str, state: EnvState) -> Message:
        x = float(state.obs[2])
        y = float(state.obs[3])
        return Message(
            agent_id,
            None if x == SENTINEL else x,
            None if y == SENTINEL else y,
            state.step,
        )

    def receive(self, messages: list[Optional[Message]]) -> dict[str, tuple[float, float]]:
        return {}
