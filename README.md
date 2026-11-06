# esis-muram-paper

[![tests](https://github.com/esis-mission/esis-muram-paper/actions/workflows/tests.yml/badge.svg)](https://github.com/esis-mission/esis-muram-paper/actions/workflows/tests.yml)
[![Black](https://github.com/esis-mission/esis-muram-paper/actions/workflows/black.yml/badge.svg)](https://github.com/esis-mission/esis-muram-paper/actions/workflows/black.yml)
[![Ruff](https://github.com/esis-mission/esis-muram-paper/actions/workflows/ruff.yml/badge.svg)](https://github.com/esis-mission/esis-muram-paper/actions/workflows/ruff.yml)

An AAS journal article comparing the explosive events of a MURaM simulation of
the quiet Sun with those observed by the EUV Snapshot Imaging Spectrograph
(ESIS) during its 2019 September 30 sounding rocket flight.

Roy T. Smart, Matthias Rempel, Jacob D. Parker, and Charles C. Kankelborg

📄 **[Read the article (pdf)](https://esis-mission.github.io/esis-muram-paper/esis-muram.pdf)**

## What this is

Explosive events are small, short-lived brightenings of the solar transition
region whose line profiles show fast flows toward and away from the observer,
and are thought to be the outflows of magnetic reconnection. This article asks
whether the explosive events of a radiative MHD simulation look like those
ESIS observed:

- **Synthesis.** The spectra of O V 630 Å and Mg X 625 Å are synthesized from
  the velocity differential emission measure (VDEM) of a snapshot of a MURaM
  simulation of the quiet Sun, with the thermal width of each temperature.
- **Events.** The explosive events of the simulation are found by the
  radiance of their fast plasma.
- **Synthetic observations.** ESIS observations of the simulation are
  simulated with the model of the instrument and inverted with the
  multiplicative algebraic reconstruction technique (MART), as the flight data
  are.
- **Comparison.** The events recovered from the synthetic observations are
  compared with those found the same way in the flight data.

## This repository *is* the article

Every figure, table, and numeric value in the prose is computed at build time
by the `esis_muram_paper` package, so the text cannot drift away from the
analysis. Numbers reach the prose as `aastex.Variable` macros rather than as
literals; a quantity the analysis has not produced yet is rendered as a bold
**XX**. Sections not yet written appear in the PDF as a gray outline.

```python
import esis_muram_paper
esis_muram_paper.pdf()
```

| path | contents |
|---|---|
| `_document.py` | assembles the article and renders the pdf |
| `_muram.py` | reads the VDEM of the simulation |
| `_lines.py`, `_spectra.py` | the contribution functions, maps, and spectra of the lines |
| `_events.py` | finds the explosive events of the simulation and their lobes |
| `sections/` | the prose, as LaTeX strings, one module per section |
| `figures/` | one module per figure, each returning an `aastex.Figure` |
| `tables/` | one module per table |
| `_variables.py` | the `aastex.Variable` macros quoted in the prose |
| `_acronyms.py` | acronym definitions used as `\ACRONYM` macros |
| `_preamble.py` | custom commands, including a comment macro per author |
| `sources.bib` | the bibliography |

The analysis itself belongs in the group's libraries, not here:
[`utu`](https://github.com/sun-data/utu) for the contribution functions and
the spectral synthesis, [`esis`](https://github.com/esis-mission/esis) for the
model of the instrument and the flight data, and
[`ctis`](https://github.com/sun-data/ctis) for the MART inversion.

## The simulation

The VDEM of the simulation, `vdem_MURaM_QS_x_120000.zarr.tar.gz`, is not
published yet, so it has to be put in `~/.esis_muram_paper/` by hand before
the article can be built; `esis_muram_paper.archive()` checks it against its
checksum and unpacks it there. Until it is published, the article cannot be
built by continuous integration.

## Building

Requires Python 3.12 or newer and a LaTeX installation. On Ubuntu:

```bash
sudo apt-get install latexmk texlive-publishers texlive-science cm-super
```

`latexmk` is not optional. Without it `pylatex` falls back to a single
`pdflatex` pass, which silently produces an article with no bibliography.

```bash
pip install -e .[test]
pytest                       # builds and validates the pdf
black esis_muram_paper       # formatting, enforced in CI
ruff check                   # linting, enforced in CI
```

## Continuous integration

Every push runs the test suite, which builds the article and checks that no
citation or cross-reference is left unresolved. Pushes to `main` publish the
article to the link above, and pull requests get their own preview at
`…/pr/<number>/esis-muram.pdf`, linked in a comment on the pull request and
removed when it closes.

The formatted bibliography and the BibTeX file of the article are published
beside it too, as `esis-muram.bbl` and `esis-muram.bib`, for the cumulative
References Cited of the dissertation that includes it.

## Commenting on the draft

Each author has a colored comment macro for notes in the prose:
`\roy{...}`, `\matthias{...}`, `\jake{...}`, and `\charles{...}`.
