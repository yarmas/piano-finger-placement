import numpy as np
from typing import Dict, List
from ..pfai.constants import INF_COST, FINGERS
from ..pfai.types import Event
from ..pfai.config import HandProfile, ModelConfig
from ..rules.costs import (
    start_cost,
    transition_cost_first_order,
    apply_rollover_adjustments,
)

def decode_monophonic_second_order(
    events: List[Event],
    profile: HandProfile,
    cfg: ModelConfig,
    hand_staff: int
) -> Dict[int, List[int]]:
    """
    Second-order DP (state carries last two fingers) with rollover support.
    Returns a mapping from event.idx to [finger].
    """
    seq = [e for e in events if e.staff == hand_staff and not e.is_chord]
    if not seq:
        return {}

    N = len(seq)
    dp = np.full((N, 6, 6), INF_COST)  # dp[i][f_{i-1}][f_i]
    back: List[List[List[tuple[int, int] | None]]] = [[[None for _ in range(6)] for _ in range(6)] for _ in range(N)]

    # Seed for i=0 (no previous fingers; model as (0, f0))
    m0 = seq[0].pitch
    for f0 in FINGERS:
        dp[0, 0, f0] = start_cost(f0, m0, cfg)

    # Handle i=1 (transition from (0, f0) to (f0, f1))
    if N == 1:
        # choose best f0 from seed row
        best_f0 = int(np.argmin(dp[0, 0, 1:])) + 1
        return {seq[0].idx: [best_f0]}

    m1 = seq[1].pitch
    for f0 in FINGERS:
        for f1 in FINGERS:
            under_slur = seq[1].slur or seq[0].slur
            local = transition_cost_first_order(f0, m0, f1, m1, under_slur, seq[1].staccato, profile, cfg)
            cand = dp[0, 0, f0] + local
            if cand < dp[1, f0, f1]:
                dp[1, f0, f1] = cand
                back[1][f0][f1] = (0, f0)

    # Main DP
    for i in range(2, N):
        m_prev2, m_prev1, m_cur = seq[i-2].pitch, seq[i-1].pitch, seq[i].pitch
        under_slur = seq[i].slur or seq[i-1].slur
        for f2 in FINGERS:
            for f1 in FINGERS:
                base_prev = dp[i-1, f2, f1]
                if base_prev >= INF_COST:
                    continue
                for f0 in FINGERS:
                    local = transition_cost_first_order(f1, m_prev1, f0, m_cur, under_slur, seq[i].staccato, profile, cfg)
                    local = apply_rollover_adjustments(m_prev2, m_prev1, m_cur, f2, f1, f0, profile, cfg, local)
                    cand = base_prev + local
                    if cand < dp[i, f1, f0]:
                        dp[i, f1, f0] = cand
                        back[i][f1][f0] = (f2, f1)

    # Backtrack best tail (f_{N-2}, f_{N-1})
    tail = np.unravel_index(np.argmin(dp[N-1, :, :]), dp[N-1, :, :].shape)  # (f_{N-2}, f_{N-1})
    f_prev, f_cur = int(tail[0]), int(tail[1])
    fingers = [f_prev, f_cur]
    for i in range(N-1, 1, -1):
        f2, f1 = back[i][f_prev][f_cur]
        fingers.append(f2)
        f_prev, f_cur = f2, f1
    fingers = list(reversed(fingers))[1:]  # drop the leading 0 seed

    assign: Dict[int, List[int]] = {}
    for e, f in zip(seq, fingers):
        assign[e.idx] = [int(f)]
    return assign
