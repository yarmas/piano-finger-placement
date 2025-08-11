from dataclasses import dataclass

@dataclass
class HandProfile:
    """
    Hand span/technique preferences. Used both for feasibility (later when chords are added)
    and to bias movement costs now.
    """
    name: str
    easy_span_semitones: int
    max_span_semitones: int
    # Jump preferences
    jump_bonus_1_to_4: float = -0.8   # reward for 1→4 jump (negative cost)
    jump_bonus_4_to_1: float = -0.8   # reward for 4→1 jump
    # Rollover preferences
    rollover_bonus_121: float = -0.75 # reward for 1–2–1
    rollover_bonus_131: float = -0.65 # reward for 1–3–1
    # Anti-patterns
    walkthrough_penalty: float = 0.35 # penalize 1–2–3 or 3–2–1 across A–B–A
    # Micro-technique
    thumb_on_black_penalty: float = 0.10
    thumb_under_prep_bonus: float = -0.05  # encourage during slurred ascents

@dataclass
class ModelConfig:
    """
    Global model coefficients (“weights”) replacing magic numbers.
    Tune these by hand or learn them later.
    """
    # Geometry terms
    weight_white_key_distance: float = 0.15
    weight_semitone_distance: float = 0.05
    # Finger motion smoothness
    weight_finger_delta: float = 0.10
    # Consecutive finger step (discouraged unless under slur)
    consecutive_step_penalty: float = 0.12
    # Finger repeats
    repeat_penalty_non_staccato: float = 0.18
    repeat_penalty_staccato: float = 0.02
    # Start state
    start_thumb_on_black_penalty: float = 0.05
    # Rollover window detection tolerance (in semitones)
    neighbor_turn_max_interval: int = 2  # allows up to whole-step around center
    repeat_near_max_interval: int = 2    # A–A–near
    # Large leap detection threshold (in semitones)
    large_leap_semitones: int = 12       # leaps larger than an octave trigger guidance

# Predefined hand sizes
PROFILE_S  = HandProfile('S',  9, 10)
PROFILE_M  = HandProfile('M', 10, 12)
PROFILE_L  = HandProfile('L', 12, 13)
PROFILE_XL = HandProfile('XL',13, 14)

DEFAULT_CONFIG = ModelConfig()
