import pytest

import esis_muram_paper


def test_url_default(monkeypatch: pytest.MonkeyPatch):
    """A local build links to the article built from main."""
    monkeypatch.delenv("ESIS_MURAM_PAPER_URL", raising=False)
    result = esis_muram_paper.url("movie.mp4")
    assert result == "https://esis-mission.github.io/esis-muram-paper/movie.mp4"


@pytest.mark.parametrize(
    argnames="base",
    argvalues=[
        "https://esis-mission.github.io/esis-muram-paper/pr/7/",
        "https://esis-mission.github.io/esis-muram-paper/pr/7",
    ],
)
def test_url_pull_request(monkeypatch: pytest.MonkeyPatch, base: str):
    """A pull request links to its own preview, with or without a slash."""
    monkeypatch.setenv("ESIS_MURAM_PAPER_URL", base)
    result = esis_muram_paper.url("movie.mp4")
    assert result == "https://esis-mission.github.io/esis-muram-paper/pr/7/movie.mp4"
