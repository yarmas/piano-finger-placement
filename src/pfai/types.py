from dataclasses import dataclass
from typing import List

@dataclass
class Event:
    """
    A single monophonic note event for one hand.
    """
    idx: int            # running index across parsed events
    pitch: int          # MIDI number
    time: float         # quarterLength offset in score
    tied: bool
    slur: bool
    staccato: bool
    staff: int          # 1 = treble (RH), 2 = bass (LH)
    is_chord: bool      # kept for completeness; decoder skips if True