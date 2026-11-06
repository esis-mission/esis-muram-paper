import named_arrays as na
import numpy as np

import esis_muram_paper


def test_events():
    """The events are named in order of the radiance of their fast plasma."""
    events = esis_muram_paper.events()
    assert len(events) == esis_muram_paper._events.num_events
    assert [e.name for e in events] == [f"M{i + 1}" for i in range(len(events))]
    radiance = [e.radiance_fast for e in events]
    assert radiance == sorted(radiance, reverse=True)
    for event in events:
        assert event.mask.sum() > 0


def test_lobes():
    """The lobes of M1 move the ways their names say, and lie inside its window."""
    line = esis_muram_paper.O_V
    lobes = esis_muram_paper.lobes(esis_muram_paper.events()[0])
    blue = esis_muram_paper.radiance_blue(line)
    red = esis_muram_paper.radiance_red(line)
    assert (blue * lobes.blue).sum() > (red * lobes.blue).sum()
    assert (red * lobes.red).sum() > (blue * lobes.red).sum()
    shape = lobes.blue.shape
    outside = na.ScalarArray(
        np.ones(tuple(shape.values()), dtype=bool), axes=tuple(shape)
    )
    outside[lobes.window] = False
    assert not np.any(lobes.blue & outside)
    assert not np.any(lobes.red & outside)
