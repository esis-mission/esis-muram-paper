import aastex

__all__ = [
    "authors",
]


def authors() -> list[aastex.Author]:
    """
    A list of the authors of this article and their affiliations.
    """

    msu = aastex.Affiliation(
        "Montana State University, "
        "Department of Physics, "
        "P.O. Box 173840, "
        "Bozeman, MT 59717, USA"
    )

    hao = aastex.Affiliation(
        "NSF National Center for Atmospheric Research, "
        "High Altitude Observatory, "
        "P.O. Box 3000, "
        "Boulder, CO 80307, USA"
    )

    return [
        aastex.Author(
            name="Roy T. Smart",
            affiliation=msu,
            orcid="0000-0002-9997-5515",
            email="roytsmart@gmail.com",
            corresponding=True,
        ),
        aastex.Author(
            name="Matthias Rempel",
            affiliation=hao,
            orcid="0000-0001-5850-3119",
        ),
        aastex.Author(
            name="Jacob D. Parker",
            affiliation=msu,
            orcid="0000-0001-8732-8284",
        ),
        aastex.Author(
            name="Charles C. Kankelborg",
            affiliation=msu,
            orcid="0000-0002-1992-7469",
        ),
    ]
