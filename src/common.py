"""Minimal compatibility types for the portfolio extract.

The full team project defined these types inside the pursuit environment.
They are recreated here only so the Byzantine/comms subsystem can be imported
and tested independently without copying the rest of the team codebase.
"""
from dataclasses import dataclass
from typing import Optional

SENTINEL = -1.0

@dataclass(frozen=True)
class Message:
    sender_id: str
    believed_hider_x: Optional[float]
    believed_hider_y: Optional[float]
    step: int
