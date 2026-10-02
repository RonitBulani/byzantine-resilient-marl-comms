import numpy as np
import pytest

from src.common import Message
from src.byzantine.subtypes import (
    RandomNoiseByzantine, MisdirectionByzantine,
    SpoofingByzantine, SilentByzantine,
)
from src.comms.broadcast import BroadcastProtocol
from src.comms.interface import EnvState
from src.comms.gossip import GossipProtocol
from src.comms.trimmed_mean import TrimmedMeanProtocol
from src.comms.reputation import ReputationProtocol

def msgs():
    return [
        Message("s0", 0.5, 0.5, 0),
        Message("s1", 0.5, 0.5, 0),
        Message("s2", 0.5, 0.5, 0),
        Message("s3", 0.0, 0.0, 0),
    ]

def test_silence_suppresses_message():
    assert SilentByzantine("s0").corrupt_message(msgs()[0]) is None

def test_random_noise_stays_in_unit_square():
    out = RandomNoiseByzantine("s0", grid_size=16, seed=1).corrupt_message(msgs()[0])
    assert 0 <= out.believed_hider_x <= 1
    assert 0 <= out.believed_hider_y <= 1

def test_spoofing_changes_identity():
    out = SpoofingByzantine("s0", ["s0", "s1"], seed=1).corrupt_message(msgs()[0])
    assert out.sender_id == "s1"

def test_misdirection_reflects_and_clamps():
    atk = MisdirectionByzantine(
        "s0", 16,
        get_true_hider_pos=lambda: (10, 10),
        get_agent_pos=lambda: (5, 5),
    )
    out = atk.corrupt_message(msgs()[0])
    assert out.believed_hider_x == pytest.approx(0.0)
    assert out.believed_hider_y == pytest.approx(0.0)

def test_trimmed_mean_rejects_extreme_report():
    out = TrimmedMeanProtocol(trim_fraction=0.25).receive(msgs())
    assert out["s0"] == pytest.approx((0.5, 0.5))

def test_gossip_respects_fanout():
    out = GossipProtocol(fanout=2, seed=0).receive(msgs())
    assert len(out) == 2

def test_reputation_penalises_outlier():
    proto = ReputationProtocol(min_trust=0.3, deviation_threshold=0.2, trust_decrement=0.1)
    for _ in range(5):
        proto.receive(msgs())
    assert proto.trust_scores["s3"] < proto.trust_scores["s0"]

def test_broadcast_skips_silent_entries():
    out = BroadcastProtocol().receive([msgs()[0], None])
    assert list(out) == ["s0"]


def test_broadcast_preserves_oracle_signal_used_by_team_experiment():
    # Local observation says the hider is unseen, while true_hider_pos contains
    # the environment-provided position. The final team experiment transmitted
    # the latter; this test intentionally locks that documented behaviour.
    state = EnvState(
        obs=np.array([0.1, 0.1, -1.0, -1.0], dtype=float),
        step=3,
        grid_size=16,
        true_hider_pos=(0.8, 0.6),
    )
    msg = BroadcastProtocol().send("s0", state)
    assert msg.believed_hider_x == pytest.approx(0.8)
    assert msg.believed_hider_y == pytest.approx(0.6)
