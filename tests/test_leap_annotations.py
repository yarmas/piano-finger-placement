from ..src.annotate.notes import collect_margin_notes
from ..src.pfai.config import DEFAULT_CONFIG
from ..src.features.patterns import is_large_leap
from ..src.pfai.types import Event


def test_is_large_leap_detection():
    cfg = DEFAULT_CONFIG
    assert not is_large_leap(60, 71, cfg)  # less than octave
    assert is_large_leap(60, 75, cfg)  # greater than octave


def test_collect_margin_notes_for_leap():
    cfg = DEFAULT_CONFIG
    events = [
        Event(idx=0, pitch=60, time=0.0, tied=False, slur=False, staccato=False, staff=1, is_chord=False),
        Event(idx=1, pitch=76, time=1.0, tied=False, slur=False, staccato=False, staff=1, is_chord=False),
    ]
    fingering = {0: [1], 1: [3]}
    notes = collect_margin_notes(events, fingering, cfg, "RH")
    assert (0.0, "Move early (RH)") in notes
    assert (1.0, "Aim 3 (RH)") in notes
