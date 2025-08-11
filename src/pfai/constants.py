# Musical / piano constants and shared “no more magic numbers”

# White-key chroma set: C D E F G A B
WHITE_CHROMA = {0, 2, 4, 5, 7, 9, 11}

# Black-key chroma set: C#/Db D#/Eb F#/Gb G#/Ab A#/Bb
BLACK_CHROMA = {1, 3, 6, 8, 10}

# Keyboard MIDI range: A0 (21) .. C8 (108)
MIDI_MIN = 21
MIDI_MAX = 108

# Default finger set for a hand
FINGERS = [1, 2, 3, 4, 5]

# Rollover triples we prioritize
ROLLOVER_TRIPLES = [(1, 2, 1), (1, 3, 1)]

# DP sentinel
INF_COST = 1e12
