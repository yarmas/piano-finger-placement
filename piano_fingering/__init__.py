"""Minimal package exposing modules under the ``piano_fingering`` namespace."""
from pathlib import Path

# Include the ``src`` directory in the package search path so submodules can be
# imported as ``piano_fingering.<module>`` without installing the project.
__path__.append(str(Path(__file__).resolve().parent.parent / "src"))
