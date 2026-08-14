from emidaf_core.core.configuration import Configuration


def test_configuration():

    cfg = Configuration()

    assert cfg.statistics.alpha == 0.05

    assert cfg.cache.enabled

    assert cfg.analysis.random_state == 42