from __future__ import annotations

from typing import Any

from emidaf_core.common.results.report_result import (
    ReportResult,
)

from .context_builder import ContextBuilder


class ReportContextBuilder:

    @classmethod
    def build(
        cls,
        report: ReportResult,
        analyses: dict[str, Any],
    ) -> dict[str, Any]:

        if not isinstance(report, ReportResult):
            raise TypeError(
                "report doit être un ReportResult."
            )

        structured_sections = report.metadata.get(
            "structured_sections",
            [],
        )

        safe_analyses = ContextBuilder.build(
            analyses
        )

        safe_analyses = cls._compact_analyses(
            safe_analyses
        )

        return {
            "report": {
                "title": report.title,
                "subtitle": report.subtitle,
                "summary": report.summary,
                "author": report.author,
                "organization": report.organization,
                "language": report.language,
                "sections": ContextBuilder._sanitize(
                    structured_sections
                ),
                "statistics": ContextBuilder._sanitize(
                    report.statistics
                ),
            },
            "analyses": safe_analyses,
        }

    @classmethod
    def _compact_analyses(
        cls,
        analyses: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Réduit le contexte externe du ReportWriter.

        Le stockage scientifique interne EMIDAF n'est pas
        modifié. Cette méthode agit uniquement sur la copie
        destinée au fournisseur génératif.

        Principes :
        - EAIE reste la référence pour la cible et les
          prédicteurs du modèle ;
        - les sorties observationnelles individuelles sont
          exclues ;
        - EDSE conserve uniquement les résultats agrégés ;
        - les résultats scientifiques agrégés des autres
          modules restent disponibles.
        """

        if not isinstance(analyses, dict):
            return {}

        compact = {
            key: value
            for key, value in analyses.items()
        }

        # --------------------------------------------------
        # EIDPP
        # --------------------------------------------------
        # predictor_columns décrit les colonnes disponibles
        # après préparation et ne doit pas être interprété
        # comme la liste des prédicteurs du modèle.
        #
        # La liste de référence pour le modèle est
        # exclusivement EAIE.features.
        eidpp = compact.get("eidpp")

        if isinstance(eidpp, dict):
            eidpp = dict(eidpp)

            eidpp.pop(
                "predictor_columns",
                None,
            )

            compact["eidpp"] = eidpp

        # --------------------------------------------------
        # EXAIE
        # --------------------------------------------------
        # Les explications locales sont liées à une
        # observation particulière et peuvent contenir une
        # prédiction individuelle. Elles restent disponibles
        # dans EMIDAF mais ne sont pas envoyées au LLM.
        exaie = compact.get("exaie")

        if isinstance(exaie, dict):
            exaie = dict(exaie)

            exaie.pop(
                "local_explanation",
                None,
            )

            compact["exaie"] = exaie

        # --------------------------------------------------
        # EDSE
        # --------------------------------------------------
        # Conserver uniquement les éléments agrégés du
        # scénario. Les tables et profils observationnels ne
        # doivent pas quitter EMIDAF.
        edse = compact.get("edse")

        if isinstance(edse, dict):
            edse = dict(edse)

            edse.pop(
                "profiles",
                None,
            )

            scenario = edse.get(
                "scenario"
            )

            if isinstance(scenario, dict):
                scenario = dict(scenario)

                scenario.pop(
                    "table",
                    None,
                )

                scenario.pop(
                    "rows",
                    None,
                )

                scenario.pop(
                    "records",
                    None,
                )

                scenario.pop(
                    "predictions",
                    None,
                )

                scenario.pop(
                    "probabilities",
                    None,
                )

                scenario.pop(
                    "observation_ids",
                    None,
                )

                scenario.pop(
                    "student_ids",
                    None,
                )

                edse[
                    "scenario"
                ] = scenario

            compact["edse"] = edse

        return compact
