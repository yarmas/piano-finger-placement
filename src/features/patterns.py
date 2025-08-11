from ..pfai.config import ModelConfig

def is_neighbor_turn(m_prev2: int, m_prev1: int, m_cur: int, cfg: ModelConfig) -> bool:
    """
    True for A–B–A shapes where the middle is within a small interval of the flank.
    """
    return (m_prev2 == m_cur) and (abs(m_prev1 - m_cur) <= cfg.neighbor_turn_max_interval)

def is_repeat_reartic(m_prev2: int, m_prev1: int, m_cur: int, cfg: ModelConfig) -> bool:
    """
    True for A–A–A rearticulations or A–A–(near) where substitution aids evenness.
    """
    return (m_prev2 == m_prev1 == m_cur) or (m_prev2 == m_prev1 and abs(m_cur - m_prev1) <= cfg.repeat_near_max_interval)

def is_consecutive_walkthrough(f2: int, f1: int, f0: int) -> bool:
    """
    Three consecutive, strictly monotone fingers (e.g., 1-2-3 or 3-2-1).
    Penalized across A–B–A to preserve hand frame.
    """
    return (abs(f2 - f1) == 1) and (abs(f1 - f0) == 1) and ((f2 < f1 < f0) or (f2 > f1 > f0))

def is_large_leap(m_prev: int, m_cur: int, cfg: ModelConfig) -> bool:
    """
    True when the interval between two notes exceeds the configured leap size.
    Used to trigger preparatory technique annotations for big jumps.
    """
    return abs(m_cur - m_prev) > cfg.large_leap_semitones
