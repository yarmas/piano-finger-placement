import argparse
from ..io.musicxml import load_score, extract_monophonic_events, write_fingerings_and_notes
from ..decoding.second_order_dp import decode_monophonic_second_order
from ..annotate.notes import collect_margin_notes
from ..pfai.config import (
    DEFAULT_CONFIG,
    PROFILE_S, PROFILE_M, PROFILE_L, PROFILE_XL,
    HandProfile, ModelConfig
)

def _profile_from_name(name: str) -> HandProfile:
    name = name.upper()
    profiles: dict[str, HandProfile] = {
        "S": PROFILE_S, "M": PROFILE_M, "L": PROFILE_L, "XL": PROFILE_XL
    }
    return profiles.get(name, PROFILE_M)
    # The get method in _profile_from_name returns PROFILE_M if the name is not found.
    # This ensures the return type is always HandProfile.
def app():
    parser = argparse.ArgumentParser(description="Piano Fingering auto-annotator (monophonic, rollover-aware).")
    parser.add_argument("--infile", required=True, help="Input MusicXML file")
    parser.add_argument("--outfile", required=True, help="Output MusicXML file")
    parser.add_argument("--hand-profile", default="M", choices=["S","M","L","XL"], help="Hand size profile")
    parser.add_argument("--staff", default="both", choices=["RH","LH","both"], help="Which staff to process")
    # Optional overrides for key weights (so you can tune without editing code)
    parser.add_argument("--rollover121", type=float, help="Reward for 1-2-1 rollover (negative is better)")
    parser.add_argument("--rollover131", type=float, help="Reward for 1-3-1 rollover (negative is better)")
    parser.add_argument("--jump14", type=float, help="Reward for 1↔4 jumps (negative is better)")
    args = parser.parse_args()

    score = load_score(args.infile)
    events = extract_monophonic_events(score)

    profile = _profile_from_name(args.hand_profile)
    cfg = DEFAULT_CONFIG

    # Allow quick CLI tuning
    if args.rollover121 is not None:
        profile.rollover_bonus_121 = args.rollover121
    if args.rollover131 is not None:
        profile.rollover_bonus_131 = args.rollover131
    if args.jump14 is not None:
        profile.jump_bonus_1_to_4 = args.jump14
        profile.jump_bonus_4_to_1 = args.jump14

    fing_all = {}

    if args.staff in ("RH", "both"):
        fing_RH = decode_monophonic_second_order(events, profile, cfg, hand_staff=1)
        fing_all.update(fing_RH)
    if args.staff in ("LH", "both"):
        fing_LH = decode_monophonic_second_order(events, profile, cfg, hand_staff=2)
        fing_all.update(fing_LH)

    notes = []
    if args.staff in ("RH", "both"):
        notes += collect_margin_notes(events, {k:v for k,v in fing_all.items() if any(e.idx==k and e.staff==1 for e in events)}, cfg, "RH")
    if args.staff in ("LH", "both"):
        notes += collect_margin_notes(events, {k:v for k,v in fing_all.items() if any(e.idx==k and e.staff==2 for e in events)}, cfg, "LH")

    write_fingerings_and_notes(args.infile, args.outfile, fing_all, notes)

if __name__ == "__main__":
    app()
