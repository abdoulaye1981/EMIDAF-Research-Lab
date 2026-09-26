import pytest

from emidaf_core.eqae import (
    QualitativeTheme,
)


def test_create_theme():
    theme = QualitativeTheme.create(
        name="Expérience scolaire",
        description="Thème principal",
    )

    assert theme.theme_id
    assert (
        theme.name
        == "Expérience scolaire"
    )
    assert (
        theme.description
        == "Thème principal"
    )


def test_theme_requires_name():
    with pytest.raises(ValueError):
        QualitativeTheme.create(
            name="   "
        )


def test_theme_serialization():
    theme = QualitativeTheme.create(
        name="Motivation"
    )

    result = theme.to_dict()

    assert result["theme_id"]
    assert result["name"] == "Motivation"
