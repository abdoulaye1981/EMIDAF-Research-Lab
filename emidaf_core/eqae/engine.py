"""
=========================================================
EMIDAF Framework v1.0
EQAE - Qualitative Analysis Engine
=========================================================
"""

from __future__ import annotations

from .coding import (
    AssistedCodingManager,
    Codebook,
    QualitativeCoder,
)
from .themes import ThematicAnalysis
from .quotations import QuotationManager
from .cooccurrence import CooccurrenceAnalyzer
from .memos import MemoManager
from .summary import QualitativeSummaryBuilder


class EQAEEngine:
    """
    Point d'entrée principal du moteur EQAE.

    EQAE prend en charge l'analyse qualitative :
    codebooks, codage, thèmes, verbatims,
    cooccurrences et mémos analytiques.

    Les résultats assistés restent soumis à la
    validation du chercheur.
    """

    def create_codebook(
        self,
        name: str,
        *,
        description: str = "",
    ) -> Codebook:
        """
        Crée un nouveau codebook qualitatif.
        """

        return Codebook(
            name=name,
            description=description,
        )

    def create_coder(
        self,
        codebook: Codebook,
    ) -> QualitativeCoder:
        """
        Crée un service de codage pour un codebook.
        """

        return QualitativeCoder(
            codebook=codebook
        )

    def create_assisted_coding_manager(
        self,
        *,
        codebook: Codebook,
        coder: QualitativeCoder,
    ) -> AssistedCodingManager:
        """
        Crée le gestionnaire de codage assisté
        avec validation humaine.
        """

        return AssistedCodingManager(
            codebook=codebook,
            coder=coder,
        )

    def create_thematic_analysis(
        self,
        codebook: Codebook,
    ) -> ThematicAnalysis:
        """
        Crée une analyse thématique liée à un codebook.
        """

        return ThematicAnalysis(
            codebook=codebook
        )

    def create_quotation_manager(
        self,
        *,
        coder: QualitativeCoder,
        thematic_analysis: ThematicAnalysis,
    ) -> QuotationManager:
        """
        Crée le gestionnaire de verbatims EQAE.
        """

        return QuotationManager(
            coder=coder,
            thematic_analysis=thematic_analysis,
        )

    def create_cooccurrence_analyzer(
        self,
        coder: QualitativeCoder,
    ) -> CooccurrenceAnalyzer:
        """
        Crée l'analyseur de cooccurrences de codes.
        """

        return CooccurrenceAnalyzer(
            coder=coder
        )

    def create_memo_manager(
        self,
    ) -> MemoManager:
        """
        Crée le gestionnaire de mémos analytiques.
        """

        return MemoManager()

    def create_summary_builder(
        self,
        *,
        coder: QualitativeCoder,
        thematic_analysis: ThematicAnalysis,
        quotation_manager: QuotationManager | None = None,
        assisted_coding: AssistedCodingManager | None = None,
    ) -> QualitativeSummaryBuilder:
        """
        Crée le constructeur de synthèse qualitative.
        """

        return QualitativeSummaryBuilder(
            coder=coder,
            thematic_analysis=thematic_analysis,
            quotation_manager=quotation_manager,
            assisted_coding=assisted_coding,
        )
