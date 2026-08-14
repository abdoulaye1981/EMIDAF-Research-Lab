from emidaf_core.core.analyzer_result import AnalyzerResult


def test_creation():

    result = AnalyzerResult("StructureAnalyzer")

    assert result.analyzer == "StructureAnalyzer"


def test_statistics():

    result = AnalyzerResult("MissingAnalyzer")

    result.set_statistic("missing", 12)

    assert result.statistic("missing") == 12


def test_finalize():

    result = AnalyzerResult("Test")

    result.add_warning("warning")

    result.finalize()

    assert result.status == "WARNING"

    result.add_error("error")

    result.finalize()

    assert result.status == "FAILED"