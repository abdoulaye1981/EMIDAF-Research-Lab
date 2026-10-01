import pytest

from emidaf_core.emix import EMIXEngine


def test_eaie_adapter():

    engine = EMIXEngine()

    source = engine.adapt_source(
        engine="eaie",
        payload={
            "model_name": "Ridge",
            "task_type": "regression",
        },
        source_id="eaie-1",
    )

    assert source.engine == "eaie"
    assert source.family == "quantitative"
    assert source.result_type == "regression"


def test_eqae_adapter():

    engine = EMIXEngine()

    source = engine.adapt_source(
        engine="eqae",
        payload={
            "summary": {
                "global": {
                    "n_themes": 2,
                }
            }
        },
        source_id="eqae-1",
    )

    assert source.engine == "eqae"
    assert source.family == "qualitative"

    assert "2" in source.description


def test_etae_adapter():

    engine = EMIXEngine()

    source = engine.adapt_source(
        engine="etae",
        payload={
            "corpus": {},
            "themes": {},
            "sentiment": {},
        },
        source_id="etae-1",
    )

    assert source.family == "textual"
    assert source.engine == "etae"


def test_unknown_adapter_rejected():

    engine = EMIXEngine()

    with pytest.raises(ValueError):

        engine.adapt_source(
            engine="unknown",
            payload={},
            source_id="x",
        )


def test_default_adapter_registry():

    engine = EMIXEngine()

    registry = (
        engine.create_adapter_registry()
    )

    assert set(
        registry.engines()
    ) == {
        "eaie",
        "elae",
        "etae",
        "eqae",
        "ekde",
        "edse",
    }
