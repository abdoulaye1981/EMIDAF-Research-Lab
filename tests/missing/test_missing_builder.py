from emidaf_core.missing.builder.missing_builder import MissingBuilder
from emidaf_core.missing.models.missing_result import MissingResult


def build_sample_report():
    return {
        "rows": 200,
        "columns": 5,
        "cells": 1000,
        "total_missing": 80,
        "missing_rate": 8.0,
        "quality_score": 92.0,
        "execution_time": 0.125,

        "summary": {
            "complete_columns": 1,
            "partial_columns": 4,
            "empty_columns": 0,
            "completeness_score": 92.0,
            "quality_level": "Very Good",
            "pattern_count": 3,
        },

        "row_statistics": {
            "complete_rows": 140,
            "rows_with_missing": 60,
            "empty_rows": 0,
            "complete_percentage": 70.0,
        },

        "patterns": [
            {
                "pattern": [0, 1, 0, 0, 0],
                "count": 30,
                "percentage": 15.0,
            },
            {
                "pattern": [0, 0, 1, 0, 0],
                "count": 20,
                "percentage": 10.0,
            },
        ],

        "imputation_candidates": [
            {
                "column": "Age",
                "dtype": "float64",
                "missing_percentage": 5.0,
                "recommended_strategy": "MEAN",
            },
            {
                "column": "Note",
                "dtype": "float64",
                "missing_percentage": 15.0,
                "recommended_strategy": "KNN",
            },
        ],

        "missing_mechanism": {
            "status": "Not evaluated",
            "candidate": "Unknown",
            "tests": {
                "mcar": {
                    "name": "Little MCAR Test",
                    "available": True,
                    "executed": False,
                },
                "mar": {
                    "name": "MAR Statistical Analysis",
                    "available": True,
                    "executed": False,
                },
                "mnar": {
                    "name": "MNAR Expert Assessment",
                    "available": True,
                    "executed": False,
                },
            },
        },

        "recommendations": [
            "Identifier le mécanisme des valeurs manquantes (MCAR, MAR ou MNAR).",
            "Choisir une méthode d'imputation adaptée avant toute modélisation.",
        ],

        "warnings": [
            "Certaines variables présentent des valeurs manquantes."
        ],

        "errors": [],
    }


def test_missing_builder_creation():
    builder = MissingBuilder()

    assert builder is not None


def test_missing_builder_build():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert isinstance(result, MissingResult)


def test_missing_builder_summary():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert result.summary.rows == 200
    assert result.summary.columns == 5
    assert result.summary.total_missing == 80
    assert result.summary.missing_rate == 8.0


def test_missing_builder_statistics():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert result.statistics.complete_rows == 140
    assert result.statistics.rows_with_missing == 60
    assert result.statistics.empty_rows == 0
    assert result.statistics.pattern_count == 3


def test_missing_builder_mechanism():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert result.mechanism.name == "Unknown"
    assert result.mechanism.detected is False


def test_missing_builder_strategy():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert result.strategy.strategy == "KNN"
    assert result.strategy.applicable is True


def test_missing_builder_patterns():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert len(result.patterns) == 2
    assert result.patterns[0].pattern == [0, 1, 0, 0, 0]
    assert result.patterns[0].count == 30


def test_missing_builder_recommendations():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert len(result.recommendations) == 2

    assert (
        result.recommendations[0].severity
        == "high"
    )

    assert (
        result.recommendations[0].priority
        == 1
    )


def test_missing_builder_warnings_errors():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert len(result.warnings) == 1
    assert result.errors == []


def test_missing_builder_execution_and_score():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert result.execution_time == 0.125
    assert result.score == 92.0


def test_missing_builder_finalize():
    builder = MissingBuilder()

    result = builder.build(
        build_sample_report()
    )

    assert builder.finalize() is result
