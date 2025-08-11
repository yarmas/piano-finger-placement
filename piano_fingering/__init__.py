"""Compatibility layer exposing project modules under the ``piano_fingering``
package.

The source tree stores subpackages like ``cli`` and ``features`` directly under
``src``.  To allow ``import piano_fingering`` without installing the project,
this module adds ``src`` to :mod:`sys.path` and configures the package's
``__path__`` so that submodules are discovered in that location.
"""

import pathlib
import sys

# Ensure the ``src`` directory is on ``sys.path`` so that the real modules can
# be located when this package is imported from a source checkout.  We also make
# this package behave like a namespace package rooted at ``src`` by adjusting
# ``__path__``.
_SRC_PATH = pathlib.Path(__file__).resolve().parent.parent / "src"
if str(_SRC_PATH) not in sys.path:
    sys.path.insert(0, str(_SRC_PATH))

__path__ = [str(_SRC_PATH)]

__all__: list[str] = []

