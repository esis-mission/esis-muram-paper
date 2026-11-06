import aastex

__all__ = [
    "abstract",
]


def abstract() -> aastex.Abstract:
    result = aastex.Abstract()
    result.append(r"""
Explosive events are small, short-lived brightenings of the solar transition region whose line
profiles show flows toward and away from the observer of up to about \SI{150}{\kilo\meter\per\second},
and are thought to be the outflows of magnetic reconnection.
The EUV Snapshot Imaging Spectrograph (ESIS), a slitless computed tomography imaging spectrograph,
recorded several of them in \OV\ \SI{630}{\angstrom} across a wide field of the quiet Sun during its
sounding rocket flight on 2019 September 30.
We ask whether the explosive events of a radiative magnetohydrodynamic simulation of the quiet Sun
look like those that ESIS observed.
We synthesize the spectra of \OV\ and \MgX\ \SI{625}{\angstrom} from the velocity differential
emission measure of a snapshot of a MURaM simulation, and find its explosive events by the
radiance of their fast plasma.
The brightest, M1, has a lobe moving toward the observer at \eventSpeedBlue, with wings reaching
\eventExtentBlue, beside a smaller lobe moving away at \eventSpeedRed.
The synthesized lines of \OV\ are narrower than those observed: in blocks of \widthsBlockLarge\
their median width is \widthsMedianLarge, against \widthsObserved\ in the quiet Sun.
We simulate the ESIS observation of the snapshot, invert it with the multiplicative algebraic
reconstruction technique (MART), and compare the explosive events recovered from it with the
\esisNumEvents\ events found in the same way in the flight data.
\roy{One or two sentences of conclusions, once the comparison is done: \comparisonSummary.}
\acresetall""")
    return result
