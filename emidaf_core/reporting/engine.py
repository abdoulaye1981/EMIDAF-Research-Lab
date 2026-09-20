"""
=========================================================
EMIDAF Framework
Global Reporting Engine
=========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .builder import ReportBuilder
from .exporter import ReportExporter


class ReportEngine:
    """
    Orchestrateur du rapport global EMIDAF.

    Le moteur consolide les résultats produits
    par les différents modules sans les recalculer.
    """

    STAGES = {
        "project": "Projet et jeu de données",
        "inspection": "Inspection des données",
        "preprocessing": "Prétraitement des données",
        "elae": "Analyse exploratoire",
        "ekde": "Découverte de connaissances",
        "eaie": "Modélisation prédictive",
        "exaie": "Explicabilité des modèles",
        "edse": "Aide à la décision",
        "limitations": "Limites méthodologiques générales",
        "conclusion": "Conclusion",
    }

    def __init__(
        self,
        *,
        title: str = "Rapport d'analyse EMIDAF",
        subtitle: str = "",
        summary: str = "",
        author: str = "Abdoulaye Wakhab DIOP",
        organization: str = "",
    ):

        self.builder = ReportBuilder(
            title=title,
            subtitle=subtitle,
            summary=summary,
            author=author,
            organization=organization,
        )

    def add_stage(
        self,
        stage: str,
        results: Any = None,
        *,
        interpretation: str = "",
        limitations: list[str] | None = None,
    ) -> "ReportEngine":

        if stage not in self.STAGES:
            raise ValueError(
                f"Étape inconnue : {stage}"
            )

        category = (
            "decision_support"
            if stage == "edse"
            else "analysis"
        )

        self.builder.add_section(
            self.STAGES[stage],
            results,
            interpretation=interpretation,
            limitations=limitations,
            category=category,
        )

        return self

    def build(self):
        return self.builder.build()

    def export(
        self,
        output_directory: str | Path,
        *,
        formats: tuple[str, ...] = (
            "markdown",
            "html",
            "json",
        ),
    ):

        report = self.build()

        return ReportExporter.export(
            report,
            output_directory,
            formats=formats,
        )
