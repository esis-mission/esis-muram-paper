import aastex

__all__ = [
    "acronyms",
]


def acronyms() -> list[aastex.Acronym]:
    """
    A list of acronyms that are used in the body of the article.
    """
    return [
        aastex.Acronym("ESIS", "the EUV Snapshot Imaging Spectrograph"),
        aastex.Acronym(
            "MURaM",
            "the Max Planck Institute for Solar System Research/University of Chicago "
            "Radiative MHD code",
        ),
        aastex.Acronym("MUSE", "the Multi-slit Solar Explorer"),
        aastex.Acronym(
            "SUMER",
            "the Solar Ultraviolet Measurements of Emitted Radiation spectrometer",
        ),
        aastex.Acronym("IRIS", "the Interface Region Imaging Spectrograph"),
        aastex.Acronym("EUV", "extreme ultraviolet"),
        aastex.Acronym("TR", "transition region"),
        aastex.Acronym("EE", "explosive event", plural=True),
        aastex.Acronym("MHD", "magnetohydrodynamics"),
        aastex.Acronym("CTIS", "computed tomography imaging spectrograph", plural=True),
        aastex.Acronym("MART", "multiplicative algebraic reconstruction technique"),
        aastex.Acronym("DEM", "differential emission measure", plural=True),
        aastex.Acronym("VDEM", "velocity differential emission measure", plural=True),
        aastex.Acronym("FWHM", "full width at half maximum"),
        aastex.Acronym("LOS", "line of sight", short=True),
    ]
