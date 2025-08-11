from piano_fingering.pfai.types import Event
from piano_fingering.decoding.second_order_dp import decode_monophonic_second_order
from piano_fingering.pfai.config import PROFILE_M, DEFAULT_CONFIG


def test_decode_monophonic_second_order_returns_fingers_for_events():
    events = [
        Event(idx=0, pitch=60, time=0.0, tied=False, slur=False, staccato=False, staff=1, is_chord=False),
        Event(idx=1, pitch=62, time=1.0, tied=False, slur=False, staccato=False, staff=1, is_chord=False),
    ]

    mapping = decode_monophonic_second_order(events, PROFILE_M, DEFAULT_CONFIG, hand_staff=1)

    assert set(mapping.keys()) == {0, 1}
    for fingers in mapping.values():
        assert all(f in {1, 2, 3, 4, 5} for f in fingers)
