from emidaf_studio.pages.emix.callbacks import (
    _normalize_tokens,
)


def test_normalize_tokens_handles_french_apostrophes():
    assert _normalize_tokens(
        "d’apprendre"
    ) == {"apprendre"}

    assert _normalize_tokens(
        "l’intérêt"
    ) == {"interet"}

    assert _normalize_tokens(
        "l’engagement"
    ) == {"engagement"}


def test_normalize_tokens_handles_ascii_apostrophes():
    assert _normalize_tokens(
        "d'apprendre"
    ) == {"apprendre"}

    assert _normalize_tokens(
        "l'intérêt"
    ) == {"interet"}
