from ..pfai.constants import FINGERS
from ..features.geometry import white_key_distance, is_black
from ..features.patterns import (
    is_neighbor_turn,
    is_repeat_reartic,
    is_consecutive_walkthrough,
)
from ..pfai.config import HandProfile, ModelConfig

def start_cost(f: int, m: int, cfg: ModelConfig) -> float:
    """
    Initial cost at sequence start.
    Slight penalty for starting with thumb on a black key.
    """
    return cfg.start_thumb_on_black_penalty if (f == 1 and is_black(m)) else 0.0

def transition_cost_first_order(
    f_prev: int, m_prev: int, f_cur: int, m_cur: int,
    under_slur: bool, staccato: bool,
    profile: HandProfile, cfg: ModelConfig
) -> float:
    """
    Base first-order movement cost between two notes/fingers.
    """
    cost = 0.0

    # Geometry distances
    semi = abs(m_cur - m_prev)
    wdist = white_key_distance(m_cur, m_prev)
    cost += cfg.weight_white_key_distance * wdist
    cost += cfg.weight_semitone_distance * semi

    # Smooth finger motion
    cost += cfg.weight_finger_delta * abs(f_cur - f_prev)

    # Prefer 1 <-> 4 jumps (user priority)
    if f_prev == 1 and f_cur == 4:
        cost += profile.jump_bonus_1_to_4
    if f_prev == 4 and f_cur == 1:
        cost += profile.jump_bonus_4_to_1

    # Discourage consecutive steps unless legato context invites it
    if abs(f_cur - f_prev) == 1 and not under_slur:
        cost += cfg.consecutive_step_penalty

    # Finger repeats
    if f_prev == f_cur:
        cost += cfg.repeat_penalty_non_staccato if not staccato else cfg.repeat_penalty_staccato

    # Thumb on black (soft)
    if f_cur == 1 and is_black(m_cur):
        cost += profile.thumb_on_black_penalty

    # Gentle thumb-under prep during ascending slurs (kept small)
    if under_slur and m_cur > m_prev and f_cur <= f_prev:
        cost += profile.thumb_under_prep_bonus

    return cost

def apply_rollover_adjustments(
    m_prev2: int, m_prev1: int, m_cur: int,
    f2: int, f1: int, f0: int,
    profile: HandProfile, cfg: ModelConfig,
    base_cost: float
) -> float:
    """
    Adds rollover bonuses and anti-walkthrough penalties on top of a local transition cost.
    """
    adjusted = base_cost

    if is_neighbor_turn(m_prev2, m_prev1, m_cur, cfg) or is_repeat_reartic(m_prev2, m_prev1, m_cur, cfg):
        if (f2, f1, f0) == (1, 2, 1):
            adjusted += profile.rollover_bonus_121
        if (f2, f1, f0) == (1, 3, 1):
            adjusted += profile.rollover_bonus_131

        if is_consecutive_walkthrough(f2, f1, f0):
            adjusted += profile.walkthrough_penalty

    return adjusted
