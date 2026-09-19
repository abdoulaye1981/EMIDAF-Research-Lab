from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from emidaf_core.missing import (
    MissingPipeline,
    MissingReporter,
)


def build_result():

    n = 100

    df = pd.DataFrame(
        {
            "age": np.linspace(
                20,
                60,
                n,
            ),
            "income": np.linspace(
                200,
                1000,
                n,
            ),
            "score": np.linspace(
                0,
                100,
                n,
            ),
        }
    )

    df.loc[
        [
            0,
            1,
            2,
        ],
        "age",
    ] = np.nan

    df.loc[
        list(
            range(
                10
            )
        ),
        "income",
    ] = np.nan

    return (
        MissingPipeline()
        .run(
            dataframe=df
        )
    )


def test_invalid_result():

    with pytest.raises(
        TypeError
    ):
        MissingReporter(
            result={}
        )


def test_dataframe():

    reporter = MissingReporter(
        build_result()
    )

    table = (
        reporter.dataframe()
    )

    assert isinstance(
        table,
        pd.DataFrame,
    )

    assert (
        "strategy"
        in table.columns
    )

    assert (
        "missing_rate"
        in table.columns
    )


def test_summary():

    reporter = MissingReporter(
        build_result()
    )

    summary = (
        reporter.summary()
    )

    assert isinstance(
        summary,
        dict,
    )

    assert (
        summary[
            "initial_missing_values"
        ]
        == 13
    )


def test_csv_export(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = reporter.to_csv(
        tmp_path
        / "missing_report.csv"
    )

    assert isinstance(
        output,
        Path,
    )

    assert output.exists()

    table = pd.read_csv(
        output
    )

    assert (
        "column"
        in table.columns
    )


def test_excel_export(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        reporter.to_excel(
            tmp_path
            / "missing_report.xlsx"
        )
    )

    assert output.exists()

    workbook = pd.ExcelFile(
        output
    )

    assert (
        "Summary"
        in workbook.sheet_names
    )

    assert (
        "Variables"
        in workbook.sheet_names
    )


def test_markdown():

    reporter = MissingReporter(
        build_result()
    )

    markdown = (
        reporter.to_markdown()
    )

    assert isinstance(
        markdown,
        str,
    )

    assert (
        "# EMIDAF Missing Data Report"
        in markdown
    )

    assert (
        "MEAN"
        in markdown
    )

    assert (
        "KNN"
        in markdown
    )


def test_markdown_export(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        tmp_path
        / "report.md"
    )

    reporter.to_markdown(
        output
    )

    assert output.exists()


def test_html():

    reporter = MissingReporter(
        build_result()
    )

    html = (
        reporter.to_html()
    )

    assert isinstance(
        html,
        str,
    )

    assert (
        "<html"
        in html
    )

    assert (
        "EMIDAF Missing Data Report"
        in html
    )


def test_html_export(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        tmp_path
        / "report.html"
    )

    reporter.to_html(
        output
    )

    assert output.exists()


def test_extension_is_added():

    reporter = MissingReporter(
        build_result()
    )

    path = (
        reporter._prepare_path(
            path="report",
            expected_suffix=".csv",
        )
    )

    assert (
        path.suffix
        == ".csv"
    )

def test_scientific_markdown():

    reporter = MissingReporter(
        build_result()
    )

    markdown = (
        reporter
        .to_scientific_markdown()
    )

    assert isinstance(
        markdown,
        str,
    )

    assert (
        "# EMIDAF Scientific Missing-Data Report"
        in markdown
    )

    assert (
        "## 1. Executive summary"
        in markdown
    )

    assert (
        "## 3. Missingness mechanism assessment"
        in markdown
    )

    assert (
        "## 6. Methodological cautions"
        in markdown
    )


def test_scientific_markdown_export(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        tmp_path
        / "scientific_report.md"
    )

    reporter.to_scientific_markdown(
        output
    )

    assert output.exists()

    content = output.read_text(
        encoding="utf-8"
    )

    assert (
        "EMIDAF Scientific Missing-Data Report"
        in content
    )


def test_scientific_html():

    reporter = MissingReporter(
        build_result()
    )

    html = (
        reporter
        .to_scientific_html()
    )

    assert isinstance(
        html,
        str,
    )

    assert (
        "<html"
        in html
    )

    assert (
        "Scientific Missing-Data Report"
        in html
    )

    assert (
        "Methodological cautions"
        in html
    )


def test_scientific_html_export(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        tmp_path
        / "scientific_report.html"
    )

    reporter.to_scientific_html(
        output
    )

    assert output.exists()


def test_methodological_notes_include_knn():

    reporter = MissingReporter(
        build_result()
    )

    table = (
        reporter.dataframe()
    )

    notes = (
        reporter
        ._methodological_notes(
            table
        )
    )

    assert any(
        "KNN"
        in note
        for note in notes
    )


def test_mechanism_text_is_cautious():

    text = (
        MissingReporter
        ._scientific_mechanism_text(
            {}
        )
    )

    assert (
        "No conclusion"
        in text
        or
        "No explicit"
        in text
    )

def test_mechanism_summary():

    reporter = MissingReporter(
        build_result()
    )

    summary = (
        reporter
        .mechanism_summary()
    )

    assert isinstance(
        summary,
        dict,
    )

    assert (
        "overall"
        in summary
    )

    assert (
        "mcar"
        in summary
    )

    assert (
        "mar"
        in summary
    )

    assert (
        "mnar"
        in summary
    )


def test_mechanism_dataframe():

    reporter = MissingReporter(
        build_result()
    )

    table = (
        reporter
        .mechanism_dataframe()
    )

    assert isinstance(
        table,
        pd.DataFrame,
    )

    assert list(
        table[
            "mechanism"
        ]
    ) == [
        "MCAR",
        "MAR",
        "MNAR",
    ]


def test_mechanism_dataframe_mar_evidence():

    reporter = MissingReporter(
        build_result()
    )

    table = (
        reporter
        .mechanism_dataframe()
    )

    mar = (
        table[
            table[
                "mechanism"
            ]
            == "MAR"
        ]
        .iloc[
            0
        ]
    )

    assert (
        "MAR"
        in mar[
            "conclusion"
        ]
    )


def test_mechanism_dataframe_mnar_is_cautious():

    reporter = MissingReporter(
        build_result()
    )

    table = (
        reporter
        .mechanism_dataframe()
    )

    mnar = (
        table[
            table[
                "mechanism"
            ]
            == "MNAR"
        ]
        .iloc[
            0
        ]
    )

    assert (
        "cannot generally be confirmed"
        in mnar[
            "conclusion"
        ]
    )


def test_format_pvalue():

    assert (
        MissingReporter
        ._format_pvalue(
            0.0
        )
        == "< 0.001"
    )

    assert (
        MissingReporter
        ._format_pvalue(
            0.03456
        )
        == "0.0346"
    )

    assert (
        MissingReporter
        ._format_pvalue(
            None
        )
        == "N/A"
    )


def test_scientific_report_no_raw_mechanism_dictionary():

    reporter = MissingReporter(
        build_result()
    )

    markdown = (
        reporter
        .to_scientific_markdown()
    )

    assert (
        "### Overall assessment"
        in markdown
    )

    assert (
        "### MCAR / MAR / MNAR assessment"
        in markdown
    )

    assert (
        "'tests': {'mcar'"
        not in markdown
    )


def test_review_dataframe():

    reporter = MissingReporter(
        build_result()
    )

    table = (
        reporter
        ._review_dataframe()
    )

    assert isinstance(
        table,
        pd.DataFrame,
    )

    assert (
        "review_required"
        in table.columns
    )


def test_methodological_notes_dataframe():

    reporter = MissingReporter(
        build_result()
    )

    table = (
        reporter
        ._methodological_notes_dataframe()
    )

    assert isinstance(
        table,
        pd.DataFrame,
    )

    assert (
        "note_id"
        in table.columns
    )

    assert (
        "methodological_note"
        in table.columns
    )

    assert len(
        table
    ) >= 3


def test_scientific_excel_export(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        reporter
        .to_scientific_excel(
            tmp_path
            / "scientific_missing_report.xlsx"
        )
    )

    assert output.exists()

    workbook = pd.ExcelFile(
        output
    )

    assert set(
        workbook.sheet_names
    ) == {
        "Summary",
        "Mechanisms",
        "Variables",
        "Review",
        "Methodological Notes",
    }


def test_scientific_excel_mechanisms_sheet(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        reporter
        .to_scientific_excel(
            tmp_path
            / "report.xlsx"
        )
    )

    mechanisms = pd.read_excel(
        output,
        sheet_name="Mechanisms",
    )

    assert list(
        mechanisms[
            "mechanism"
        ]
    ) == [
        "MCAR",
        "MAR",
        "MNAR",
    ]


def test_scientific_excel_variables_sheet(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        reporter
        .to_scientific_excel(
            tmp_path
            / "report.xlsx"
        )
    )

    variables = pd.read_excel(
        output,
        sheet_name="Variables",
    )

    assert (
        "strategy"
        in variables.columns
    )

    assert (
        "missing_rate"
        in variables.columns
    )

    assert (
        "predictors"
        in variables.columns
    )


def test_scientific_excel_notes_sheet(
    tmp_path,
):

    reporter = MissingReporter(
        build_result()
    )

    output = (
        reporter
        .to_scientific_excel(
            tmp_path
            / "report.xlsx"
        )
    )

    notes = pd.read_excel(
        output,
        sheet_name="Methodological Notes",
    )

    assert (
        "methodological_note"
        in notes.columns
    )

    assert len(
        notes
    ) >= 3
