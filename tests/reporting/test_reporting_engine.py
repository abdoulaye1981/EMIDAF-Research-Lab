from pathlib import Path

from emidaf_core.reporting import ReportEngine


def test_build_global_report():

    engine = ReportEngine(
        title="Rapport EMIDAF Test",
        summary="Synthèse scientifique.",
    )

    engine.add_stage(
        "inspection",
        {
            "rows": 100,
            "columns": 5,
        },
        interpretation=(
            "Le jeu de données contient "
            "100 observations."
        ),
    )

    report = engine.build()

    assert report.title == (
        "Rapport EMIDAF Test"
    )

    assert len(report.sections) == 1

    assert (
        report.statistics[
            "sections_count"
        ]
        == 1
    )


def test_methodological_limitations():

    engine = ReportEngine()

    engine.add_stage(
        "eaie",
        {
            "model": "svr",
            "cv_mean": -0.11,
            "test_score": -0.03,
        },
        interpretation=(
            "La capacité prédictive "
            "n'est pas convaincante."
        ),
        limitations=[
            (
                "Les scores négatifs imposent "
                "une interprétation prudente."
            )
        ],
    )

    report = engine.build()

    section = report.metadata[
        "structured_sections"
    ][0]

    assert section["limitations"]


def test_export_report(tmp_path: Path):

    engine = ReportEngine(
        title="Rapport export"
    )

    engine.add_stage(
        "inspection",
        {"rows": 20},
    )

    report = engine.export(
        tmp_path,
    )

    assert Path(
        report.markdown_file
    ).exists()

    assert Path(
        report.html_file
    ).exists()

    assert Path(
        report.json_file
    ).exists()


def test_edse_is_decision_support():

    engine = ReportEngine()

    engine.add_stage(
        "edse",
        {
            "threshold": 100,
            "selected": 4,
        },
        interpretation=(
            "Le seuil représente un "
            "scénario défini par l'utilisateur."
        ),
    )

    report = engine.build()

    section = report.metadata[
        "structured_sections"
    ][0]

    assert (
        section["category"]
        == "decision_support"
    )
