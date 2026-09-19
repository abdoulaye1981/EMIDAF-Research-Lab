from emidaf_core.dataset.profiler.profile_builder import ProfileBuilder
from emidaf_core.dataset.profiler.profile_metadata import ProfileMetadata
from emidaf_core.dataset.profiler.profile_summary import ProfileSummary
from emidaf_core.dataset.profiler.analyzers.analyzer_result import AnalyzerResult


def create_test_data():
    metadata = ProfileMetadata(
        dataset_id=1,
        project_id=2,
        workspace_id=3,
        profile_name="Profil test",
        dataset_name="dataset_test",
        author="EMIDAF"
    )

    summary = ProfileSummary(
        rows=100,
        columns=5,
        cells=500,
        memory_usage=4096
    )

    analyzers = [
        AnalyzerResult(
            name="StructureAnalyzer",
            result={
                "rows": 100,
                "columns": 5
            }
        ),
        AnalyzerResult(
            name="DatatypeAnalyzer",
            result={
                "count": {
                    "numeric": 2,
                    "categorical": 2,
                    "boolean": 1,
                    "datetime": 0,
                    "text": 0
                }
            }
        ),
        AnalyzerResult(
            name="MissingAnalyzer",
            result={
                "total_missing": 10,
                "missing_rate": 2.0
            }
        ),
        AnalyzerResult(
            name="DuplicateAnalyzer",
            result={
                "duplicate_rows": 5,
                "duplicate_rate": 5.0
            }
        ),
        AnalyzerResult(
            name="QualityAnalyzer",
            result={
                "quality_score": 90.0
            },
            score=90.0
        ),
        AnalyzerResult(
            name="StructureAnalyzerExtra",
            result={
                "custom": True
            },
            warnings=["Avertissement structure"],
            errors=["Erreur structure"],
            recommendations=["Vérifier la structure"]
        )
    ]

    return analyzers, metadata, summary


def test_profile_builder_creation():
    builder = ProfileBuilder()

    assert builder is not None
    assert str(builder) == "ProfileBuilder"


def test_profile_builder_build():
    analyzers, metadata, summary = create_test_data()

    builder = ProfileBuilder()
    profile = builder.build(
        analyzers,
        metadata,
        summary
    )

    assert profile is not None

    assert profile.metadata is metadata
    assert profile.summary is summary

    assert profile.structure == {
        "rows": 100,
        "columns": 5
    }

    assert profile.datatypes["count"]["numeric"] == 2
    assert profile.datatypes["count"]["categorical"] == 2

    assert profile.missing["total_missing"] == 10
    assert profile.missing["missing_rate"] == 2.0

    assert profile.duplicates["duplicate_rows"] == 5
    assert profile.duplicates["duplicate_rate"] == 5.0


def test_profile_builder_warnings_errors_recommendations():
    analyzers, metadata, summary = create_test_data()

    builder = ProfileBuilder()
    profile = builder.build(
        analyzers,
        metadata,
        summary
    )

    assert "Avertissement structure" in profile.warnings

    assert any(
        "StructureAnalyzerExtra" in error
        for error in profile.errors
    )

    assert len(profile.recommendations) == 1

    recommendation = profile.recommendations[0]

    assert recommendation["analyzer"] == "StructureAnalyzerExtra"
    assert recommendation["message"] == "Vérifier la structure"
    assert recommendation["priority"] == "MEDIUM"


def test_profile_builder_scores():
    analyzers, metadata, summary = create_test_data()

    builder = ProfileBuilder()
    profile = builder.build(
        analyzers,
        metadata,
        summary
    )

    assert profile.scores["QualityAnalyzer"] == 90.0

    assert profile.scores["quality"] == 90.0
    assert profile.scores["completeness"] == 98.0
    assert profile.scores["uniqueness"] == 95.0
    assert profile.scores["consistency"] == 90.0
    assert profile.scores["validity"] == 90.0

    assert profile.scores["overall"] == 92.6


def test_profile_builder_summary():
    analyzers, metadata, summary = create_test_data()

    builder = ProfileBuilder()
    profile = builder.build(
        analyzers,
        metadata,
        summary
    )

    assert profile.summary.numeric_columns == 2
    assert profile.summary.categorical_columns == 2
    assert profile.summary.boolean_columns == 1

    assert profile.summary.missing_values == 10
    assert profile.summary.missing_percentage == 2.0

    assert profile.summary.duplicate_rows == 5
    assert profile.summary.duplicate_percentage == 5.0

    assert profile.summary.quality_score == 90.0
    assert profile.summary.completeness_score == 98.0
    assert profile.summary.uniqueness_score == 95.0
    assert profile.summary.consistency_score == 90.0
    assert profile.summary.validity_score == 90.0
    assert profile.summary.overall_score == 92.6


def test_profile_builder_metadata():
    analyzers, metadata, summary = create_test_data()

    builder = ProfileBuilder()
    profile = builder.build(
        analyzers,
        metadata,
        summary
    )

    assert profile.metadata.warning_count == 1
    assert profile.metadata.error_count == 1
    assert profile.metadata.analyzed_rows == 100
    assert profile.metadata.analyzed_columns == 5
    assert profile.metadata.analyzed_cells == 500
    assert profile.metadata.memory_usage == 4096


def test_profile_builder_to_profile():
    analyzers, metadata, summary = create_test_data()

    builder = ProfileBuilder()

    profile = builder.build(
        analyzers,
        metadata,
        summary
    )

    assert builder.to_profile() is profile


def test_profile_builder_clear():
    analyzers, metadata, summary = create_test_data()

    builder = ProfileBuilder()

    profile = builder.build(
        analyzers,
        metadata,
        summary
    )

    assert profile.structure
    assert profile.warnings
    assert profile.recommendations

    builder.clear()

    cleared_profile = builder.to_profile()

    assert cleared_profile is not profile
    assert cleared_profile.structure == {}
    assert cleared_profile.warnings == []
    assert cleared_profile.errors == []
    assert cleared_profile.recommendations == []
    assert cleared_profile.scores == {}


def test_profile_builder_attribute_mapping():
    builder = ProfileBuilder()

    assert builder._attribute_name(
        "StructureAnalyzer"
    ) == "structure"

    assert builder._attribute_name(
        "DatatypeAnalyzer"
    ) == "datatypes"

    assert builder._attribute_name(
        "MissingAnalyzer"
    ) == "missing"

    assert builder._attribute_name(
        "OutlierAnalyzer"
    ) == "outliers"

    assert builder._attribute_name(
        "CorrelationAnalyzer"
    ) == "correlations"

    assert builder._attribute_name(
        "MulticollinearityAnalyzer"
    ) == "multicollinearity"


def test_profile_builder_extras():
    analyzer = AnalyzerResult(
        name="CustomAnalyzer",
        result={
            "value": 123
        }
    )

    builder = ProfileBuilder()

    profile = builder.build(
        [analyzer],
        ProfileMetadata(),
        ProfileSummary()
    )

    assert profile.extras["custom"] == {
        "value": 123
    }
