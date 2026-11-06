# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`esis-muram-paper` is a **reproducible scientific article**, not a conventional
software library. The `esis_muram_paper` Python package programmatically
generates a complete AAS-journal LaTeX article (text, figures, tables, and
numeric values) comparing the explosive events of a MURaM simulation of the
quiet Sun with those observed by the EUV Snapshot Imaging Spectrograph (ESIS)
during its 2019 September 30 flight.
Calling `esis_muram_paper.pdf()` produces the final `esis-muram.pdf`.

This is one package within the larger Kankelborg-Group workspace (see the parent
`../CLAUDE.md`). Its sibling article `esis-jet-paper` follows the same layout
and is the template it was made from.

## The analysis

- **The simulation**: the velocity differential emission measure (VDEM) of
  one snapshot of a MURaM quiet-Sun run, sent by Matthias Rempel as
  `vdem_MURaM_QS_x_120000.zarr.tar.gz`. It is not published yet, so it is kept
  by hand in `~/.esis_muram_paper/` (`_muram.py`), and CI cannot build the
  article until it is. Never commit it.
- **Synthesis**: contribution functions and spectra from `utu`
  (`utu.spectrum.contribution_function`, `utu.spectrum.synthesize`), in
  `_lines.py` and `_spectra.py`.
- **Events**: found by the O V radiance of their fast plasma, in `_events.py`.
  They are named M1, M2, ... so as not to be confused with the events A-E of
  Parker et al. (2022). The same criteria are to be applied to the MART
  inversions of the flight data.
- **Synthetic ESIS observations and the flight data**: the instrument model
  and the Level-4 MART inversions live in `esis`, the inversion in `ctis`.

## Rules

- **Push reusable functionality down the stack**: if a figure or quantity needs a
  capability the libraries lack, add it there (with tests) rather than writing
  bespoke code here, but ask before adding a new public API to a library.
  This repo should contain only prose, `aastex` document assembly, and thin
  glue that calls library functions.
- **Every number in the prose is an `aastex.Variable`** defined in `_variables.py`.
  A number the analysis cannot supply yet is declared with `_pending()`, which
  renders as a bold `XX`, so the draft shows plainly what is still owed.
- Sections not yet written are drafted as an `outline` environment (defined in
  `_preamble.py`), which renders as a gray bulleted list, so the plan cannot be
  mistaken for the article.
- The emission measure is several gigabytes in single precision. Keep the
  products along the way in single precision and reduce the temperature axis
  to the bins of the line (`esis_muram_paper.bins`) before multiplying.

## Commands

Run from this package directory:

```bash
pip install -e .[test]          # install for development
pytest                          # run tests; test_pdf compiles the LaTeX → PDF
black esis_muram_paper          # format (CI enforces --check)
ruff check                      # lint (CI enforces)
```

Building the PDF requires a **LaTeX installation** with `latexmk` (TeX Live:
`texlive-publishers texlive-science cm-super latexmk`). Without `latexmk`,
`pylatex` falls back to a single `pdflatex` pass and the bibliography is
silently missing; `test_pdf` checks for this.

## Architecture

The whole article is assembled in `_document.py`: `document()` builds an
`aastex.Document`, appending acronyms, variables, title, authors, abstract,
keywords, each section, the acknowledgments, and finally the bibliography
(`sources.bib`). `pdf()` renders it.

- **`sections/`**: each module returns an `aastex.Section` (or `aastex.Abstract`).
  Prose lives here as raw LaTeX strings (with `\cite`, `\ref`, equations) and
  embeds figures/tables by calling the corresponding factory.
- **`figures/`**: each module builds a matplotlib figure and wraps it in an
  `aastex.Figure`/`FigureStar` with a caption. Maps are drawn with
  `figures._images.image`, which embeds the pixels of the simulation unresampled.
- **`tables/`**: factories returning `aastex.Table` objects.
- **`_variables.py`**: `aastex.Variable` LaTeX macros for every numeric value
  cited in the prose.
- **`_acronyms.py`**: `aastex.Acronym` definitions; prose uses `\ACRONYM` macros.
- **`_preamble.py`**: custom commands, including a colored comment macro per
  author (`\roy`, `\matthias`, `\jake`, `\charles`).

## Conventions

- Every module declares an explicit `__all__` and exposes functionality through small
  factory functions, re-exported up the package via `__init__.py`. To add a new
  figure/table/section: create `_name.py`, then add it to the subpackage `__init__.py`.
- Modules import the top-level package as `import esis_muram_paper` and reach back
  into it (`esis_muram_paper.figures.x()`) rather than deep relative imports.
- Cite only entries in `sources.bib`, and add new ones from the publisher's
  record (e.g. `curl -LH "Accept: application/x-bibtex" https://doi.org/<doi>`)
  rather than typing them by hand.
- Generated LaTeX/PDF output and caches are gitignored; never commit build artifacts.
- Stage explicit files with `git add`; never `git add` whole directories.
