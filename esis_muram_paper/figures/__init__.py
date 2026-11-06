"""
The figures of this article, each a factory function returning an
:class:`aastex.Figure`.
"""

from ._event import event
from ._overview import overview
from ._widths import widths

__all__ = [
    "event",
    "overview",
    "widths",
]
