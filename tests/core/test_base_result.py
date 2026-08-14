from emidaf_core.core.base_result import BaseResult


def test_result_creation():

    result = BaseResult()

    assert result.success is True

    assert result.score == 0


def test_warning():

    result = BaseResult()

    result.add_warning("Attention")

    assert result.warning_count == 1


def test_error():

    result = BaseResult()

    result.add_error("Erreur")

    assert result.success is False

    assert result.error_count == 1


def test_recommendation():

    result = BaseResult()

    result.add_recommendation("Nettoyer")

    assert result.recommendation_count == 1


def test_data():

    result = BaseResult()

    result.put("rows", 150)

    assert result.get("rows") == 150