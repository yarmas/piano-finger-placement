from typing import Dict, List, Tuple
from ..pfai.types import Event
from ..features.patterns import is_neighbor_turn, is_repeat_reartic, is_consecutive_walkthrough
from ..pfai.config import ModelConfig as mc

def collect_margin_notes(
    events: List[Event],
    fingering: Dict[int, List[int]],
    cfg: mc,
    hand_label: str
) -> List[Tuple[float, str]]:
    """
    Emits short pedagogical notes whenever a rollover fired or a walkthrough was avoided.
    """
    notes: List[Tuple[float, str]] = []
    seq = [e for e in events if e.idx in fingering]
    seq.sort(key=lambda e: e.time)

    for i in range(2, len(seq)):
        e2, e1, e0 = seq[i-2], seq[i-1], seq[i]
        f2, f1, f0 = fingering[e2.idx][0], fingering[e1.idx][0], fingering[e0.idx][0]

        if is_neighbor_turn(e2.pitch, e1.pitch, e0.pitch, cfg) or is_repeat_reartic(e2.pitch, e1.pitch, e0.pitch, cfg):
            if (f2, f1, f0) == (1, 2, 1):
                notes.append((e0.time, f"Rollover 1–2–1 ({hand_label})"))
            elif (f2, f1, f0) == (1, 3, 1):
                notes.append((e0.time, f"Rollover 1–3–1 ({hand_label})"))
            elif is_consecutive_walkthrough(f2, f1, f0):
                notes.append((e0.time, f"Avoided walk‑through ({hand_label})"))
    return notes
