from datetime import datetime

from emidaf_core.builders.dataset_builder import DatasetBuilder
from emidaf_core.dto.dataset_dto import DatasetDTO


def test_dataset_builder_creation():
    builder = DatasetBuilder()

    assert builder is not None


def test_dataset_builder_build():
    builder = DatasetBuilder()

    result = builder.build(
        project_id=1,
        name="Dataset Test",
        original_filename="test.csv",
        stored_filename="test_2026.csv",
        extension=".csv",
        separator=",",
        encoding="utf-8",
        rows=100,
        columns=5,
        size=2048,
    )

    assert isinstance(result, DatasetDTO)


def test_dataset_builder_values():
    builder = DatasetBuilder()

    result = builder.build(
        project_id=10,
        name="Etudiants",
        original_filename="students.csv",
        stored_filename="students_2026.csv",
        extension=".csv",
        separator=";",
        encoding="utf-8",
        rows=1000,
        columns=12,
        size=85000,
    )

    assert result.project_id == 10
    assert result.name == "Etudiants"
    assert result.original_filename == "students.csv"
    assert result.stored_filename == "students_2026.csv"
    assert result.extension == ".csv"
    assert result.separator == ";"
    assert result.encoding == "utf-8"
    assert result.rows == 1000
    assert result.columns == 12
    assert result.size == 85000


def test_dataset_builder_defaults():
    builder = DatasetBuilder()

    result = builder.build(
        project_id=1,
        name="Dataset",
        original_filename="data.csv",
        stored_filename="data.csv",
        extension=".csv",
    )

    assert result.separator == ","
    assert result.encoding == "utf-8"
    assert result.rows == 0
    assert result.columns == 0
    assert result.size == 0
    assert result.created_at is None
    assert result.updated_at is None


def test_dataset_builder_dates():
    builder = DatasetBuilder()

    created_at = datetime(2026, 1, 1, 10, 0, 0)
    updated_at = datetime(2026, 1, 2, 10, 0, 0)

    result = builder.build(
        project_id=1,
        name="Dataset",
        original_filename="data.csv",
        stored_filename="data.csv",
        extension=".csv",
        created_at=created_at,
        updated_at=updated_at,
    )

    assert result.created_at == created_at
    assert result.updated_at == updated_at
