import pytest

from emidaf_core.emix import (
    MixedMethodSource,
    SourceRegistry,
)


def make_source(
    source_id="s1",
    family="quantitative",
):
    return MixedMethodSource(
        source_id=source_id,
        engine="eaie",
        family=family,
        label="Source test",
        result_type="test",
    )


def test_add_get_remove():

    registry = SourceRegistry()

    source = make_source()

    registry.add(source)

    assert (
        registry.get("s1")
        == source
    )

    removed = registry.remove(
        "s1"
    )

    assert removed == source
    assert registry.all() == []


def test_duplicate_source_rejected():

    registry = SourceRegistry()

    source = make_source()

    registry.add(source)

    with pytest.raises(ValueError):
        registry.add(source)


def test_family_filter():

    registry = SourceRegistry()

    registry.add(
        make_source(
            "q1",
            "quantitative",
        )
    )

    registry.add(
        MixedMethodSource(
            source_id="ql1",
            engine="eqae",
            family="qualitative",
            label="Qualitatif",
            result_type="theme",
        )
    )

    result = registry.by_family(
        "qualitative"
    )

    assert len(result) == 1
    assert result[0].source_id == "ql1"
