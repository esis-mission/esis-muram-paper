"""
The explosive events of the simulation, found from the radiance of its fast
plasma in O V.
"""

import dataclasses
import functools

import astropy.units as u
import named_arrays as na
import numpy as np
import scipy.ndimage

import esis_muram_paper

__all__ = [
    "Event",
    "Lobes",
    "events",
    "fraction_fast",
    "fraction_lobe",
    "lobes",
    "num_events",
    "percentile_fast",
    "size_box",
    "size_window",
]

percentile_fast = 99.5
"""
The percentile, over the box, of the radiance of the fast plasma which a pixel
must reach to belong to an event.
"""

fraction_fast = 0.1
"""
The least fraction of the radiance of a pixel which must come from fast
plasma for the pixel to belong to an event.
"""

num_events = 5
"""How many events are named, in order of the radiance of their fast plasma."""

size_window = 20 * u.Mm
"""The width of the square around an event within which its lobes are found."""

fraction_lobe = 0.3
"""
The least fraction of the radiance of a pixel which must come from fast
plasma moving one way for the pixel to belong to the lobe of that direction.
"""

size_box = 3 * u.Mm
"""
The width of the square centered between the lobes of an event, about two
resolution elements of ESIS, which holds both.
"""


def _label(mask: na.AbstractScalar) -> tuple[na.ScalarArray, int]:
    """
    Number the connected regions of `mask`, taking pixels which touch at an
    edge or a corner as connected, and return the number of each pixel's
    region, 0 outside of every region, and how many regions there are.
    """
    mask = mask.explicit
    labels, num = scipy.ndimage.label(
        mask.ndarray,
        structure=np.ones((3, 3), dtype=bool),
    )
    return na.ScalarArray(labels, axes=mask.axes), num


def _sums(
    a: na.AbstractScalar,
    labels: na.ScalarArray,
    num: int,
) -> np.ndarray:
    """The sum of `a` over each of the `num` regions numbered in `labels`."""
    a = a.explicit.broadcast_to(labels.shape)
    return scipy.ndimage.sum(
        a.ndarray.value,
        labels=labels.ndarray,
        index=np.arange(1, num + 1),
    )


@dataclasses.dataclass(frozen=True, eq=False)
class Event:
    """An explosive event of the simulation."""

    name: str
    """The name of the event."""

    mask: na.ScalarArray
    """Which pixels of the simulation belong to the event."""

    @property
    def radiance_fast(self) -> u.Quantity:
        """The radiance of the fast plasma of the event, summed over its pixels."""
        line = esis_muram_paper.O_V
        fast = esis_muram_paper.radiance_blue(line) + esis_muram_paper.radiance_red(
            line
        )
        return (fast * self.mask).sum().ndarray

    @property
    def position(self) -> na.Cartesian2dVectorArray:
        """The center of the event, weighted by the radiance of its fast plasma."""
        line = esis_muram_paper.O_V
        fast = esis_muram_paper.radiance_blue(line) + esis_muram_paper.radiance_red(
            line
        )
        weight = fast * self.mask
        position = esis_muram_paper.simulation().position
        return (position * weight).sum() / weight.sum()

    @property
    def area(self) -> u.Quantity:
        """The area of the pixels of the event."""
        pitch = esis_muram_paper.simulation().pitch
        return self.mask.sum().ndarray * pitch**2


@functools.cache
def events() -> tuple[Event, ...]:
    """
    The :data:`num_events` brightest explosive events of the simulation.

    An event is a connected region of pixels whose fast plasma, moving at
    :data:`esis_muram_paper.speed_fast` or faster either way, is brighter in
    O V than :data:`percentile_fast` of the box and makes up at least
    :data:`fraction_fast` of the radiance of the pixel. The events are named
    M1, M2, and so on, in order of the radiance of their fast plasma.
    """
    line = esis_muram_paper.O_V
    total = esis_muram_paper.radiance(line)
    fast = esis_muram_paper.radiance_blue(line) + esis_muram_paper.radiance_red(line)
    threshold = np.percentile(fast, percentile_fast)
    labels, num = _label((fast >= threshold) & (fast >= fraction_fast * total))
    order = np.argsort(_sums(fast, labels, num))[::-1]
    return tuple(
        Event(name=f"M{k + 1}", mask=labels == (i + 1))
        for k, i in enumerate(order[:num_events])
    )


@dataclasses.dataclass(frozen=True, eq=False)
class Lobes:
    """The lobes of plasma moving toward and away from the observer in an event."""

    event: Event
    """The event the lobes belong to."""

    window: dict[str, slice]
    """
    The square of width :data:`size_window` around the event, as slices
    along the horizontal axes of the simulation.
    """

    blue: na.ScalarArray
    """Which pixels of the simulation belong to the lobe moving toward the observer."""

    red: na.ScalarArray
    """Which pixels of the simulation belong to the lobe moving away from the observer."""

    box: dict[str, slice]
    """
    The square of width :data:`size_box` centered between the lobes, as
    slices along the horizontal axes of the simulation.
    """


def _square(center: na.Cartesian2dVectorArray, size: u.Quantity) -> dict[str, slice]:
    """The pixels of the square of width `size` centered on `center`."""
    simulation = esis_muram_paper.simulation()
    num = int(np.round((size / simulation.pitch).to(u.dimensionless_unscaled)))
    result = {}
    for axis, c, x in [
        (simulation.axis_x, center.x, simulation.position.x),
        (simulation.axis_y, center.y, simulation.position.y),
    ]:
        middle = int(np.argmin(np.abs(x - c), axis=axis)[axis].ndarray)
        start = min(max(middle - num // 2, 0), x.shape[axis] - num)
        result[axis] = slice(start, start + num)
    return result


@functools.cache
def lobes(event: Event) -> Lobes:
    """
    The lobes of `event`.

    Within :data:`size_window` of the event, the lobe of each direction is
    the connected region of pixels whose plasma moving that way at
    :data:`esis_muram_paper.speed_fast` or faster is brighter in O V than the
    threshold of :func:`events` and makes up at least :data:`fraction_lobe`
    of the radiance of the pixel, the brightest such region if there are
    several.

    Parameters
    ----------
    event
        One of the :func:`events`.
    """
    line = esis_muram_paper.O_V
    total = esis_muram_paper.radiance(line)
    blue = esis_muram_paper.radiance_blue(line)
    red = esis_muram_paper.radiance_red(line)
    threshold = np.percentile(blue + red, percentile_fast)
    window = _square(event.position, size_window)

    def lobe(fast: na.AbstractScalar) -> na.ScalarArray:
        """The brightest region of the window bright enough in `fast`."""
        inside = na.ScalarArray(
            np.zeros(tuple(total.shape.values()), dtype=bool),
            axes=tuple(total.shape),
        )
        inside[window] = True
        mask = inside & (fast >= threshold) & (fast >= fraction_lobe * total)
        labels, num = _label(mask)
        if num == 0:
            raise ValueError(f"event {event.name} has no lobe")
        return labels == (int(np.argmax(_sums(fast, labels, num))) + 1)

    blue = lobe(blue)
    red = lobe(red)
    position = esis_muram_paper.simulation().position
    middle = (
        (position * blue).sum() / blue.sum() + (position * red).sum() / red.sum()
    ) / 2
    return Lobes(
        event=event,
        window=window,
        blue=blue,
        red=red,
        box=_square(middle, size_box),
    )
