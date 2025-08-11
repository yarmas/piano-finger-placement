from typing import List
from music21 import converter, note, chord, expressions, articulations, stream
from ..types import Event

def load_score(path: str):
    """
    Loads a MusicXML (or other music21-supported) score.
    """
    return converter.parse(path)

def extract_monophonic_events(score) -> List[Event]:
    """
    Flatten notes and transform into :class:`Event` objects.

    Chords are skipped explicitly while rests are inherently excluded by
    ``score.recurse().notes``.
    """
    evts: List[Event] = []
    idx = 0
    for n in score.recurse().notes:
        staff = getattr(n, 'staffNumber', 1)
        if isinstance(n, chord.Chord):
            # per user request, skip chords for now
            continue
        if isinstance(n, note.Note):
            tied = n.tie is not None
            # music21 encodes slurs as Span objects; editions vary, so we also accept Tenuto as legato-ish
            has_slur = any(isinstance(x, expressions.Slur) for x in n.expressions)
            is_stacc = any(isinstance(a, articulations.Staccato) for a in n.articulations)
            evts.append(Event(
                idx=idx,
                pitch=n.pitch.midi,
                time=float(n.offset),
                tied=tied,
                slur=has_slur,
                staccato=is_stacc,
                staff=staff,
                is_chord=False
            ))
            idx += 1
    return evts

def write_fingerings_and_notes(src_path: str,
                               out_path: str,
                               fingering_map: dict[int, list[int]],
                               margin_notes: list[tuple[float, str]]) -> None:
    """
    Writes finger numbers and margin notes back to a MusicXML file.
    """
    s = converter.parse(src_path)

    # Attach fingerings in appearance order.
    k = 0
    for n in s.recurse().notes:
        if isinstance(n, chord.Chord):
            continue
        if k in fingering_map:
            n.expressions.append(expressions.Fingering(fingering_map[k][0]))
        k += 1

    # Write margin notes as text expressions near their time.
    for t, text in margin_notes:
        try:
            meas_num = max(1, int(t) + 1)
            te = expressions.TextExpression(text)
            te.placement = "above"
            s.parts[0].measure(meas_num).insert(t, te)
        except Exception:
            # layout can fail on some imported editions; ignore rather than crash
            pass

    s.write('musicxml', out_path)
    
