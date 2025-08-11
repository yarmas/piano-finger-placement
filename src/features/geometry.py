from ..pfai.constants import BLACK_CHROMA, WHITE_CHROMA, MIDI_MIN

def is_black(midi: int) -> bool:
    """True if MIDI pitch is a black key."""
    return (midi % 12) in BLACK_CHROMA

def white_key_distance(m1: int, m2: int) -> int:
    """
    Approximate white-key steps between two MIDI notes.
    Counts white keys from A0 up to the note and takes the absolute difference.
    """
    def whites_up_to(m: int) -> int:
        count = 0
        for x in range(MIDI_MIN, m + 1):
            if (x % 12) in WHITE_CHROMA:
                count += 1
        return count
    return abs(whites_up_to(m1) - whites_up_to(m2))
