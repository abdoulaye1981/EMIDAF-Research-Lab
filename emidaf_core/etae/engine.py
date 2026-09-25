"""
=========================================================
EMIDAF Framework v1.0
ETAE - Text Analysis Engine
=========================================================
"""

from __future__ import annotations

import pandas as pd

from .descriptive.corpus_profiler import (
    CorpusProfiler,
)
from .descriptive.frequency_analyzer import (
    FrequencyAnalyzer,
)
from .result import CorpusProfileResult
from .preprocessing import (
    ProcessedText,
    TextPreprocessingConfig,
    TextPreprocessor,
)
from .vectorization import (
    ETAETfidfVectorizer,
)
from .semantics import (
    TextClusterer,
    TopicModeler,
)
from .association import (
    TopicTargetAnalyzer,
)
from .text_column_detector import (
    TextColumnCandidate,
    TextColumnDetector,
)


class ETAEEngine:
    """
    Point d'entrée principal du moteur ETAE.

    ETAE analyse les variables textuelles d'un jeu
    de données sans modifier le dataset source.
    """

    def __init__(self) -> None:
        self._corpus_profiler = (
            CorpusProfiler()
        )
        self._frequency_analyzer = (
            FrequencyAnalyzer()
        )
        self._text_column_detector = (
            TextColumnDetector()
        )
        self._tfidf_vectorizer = (
            ETAETfidfVectorizer()
        )
        self._text_clusterer = (
            TextClusterer()
        )
        self._topic_modeler = (
            TopicModeler()
        )
        self._topic_target_analyzer = (
            TopicTargetAnalyzer()
        )

    def detect_text_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> list[str]:
        """
        Retourne les colonnes détectées comme
        texte libre.
        """

        return (
            self._text_column_detector
            .text_columns(
                dataframe
            )
        )

    def inspect_text_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> list[TextColumnCandidate]:
        """
        Retourne le diagnostic détaillé des
        colonnes textuelles candidates.
        """

        return (
            self._text_column_detector
            .detect(
                dataframe
            )
        )

    def preprocess_text_column(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        *,
        config: TextPreprocessingConfig | None = None,
    ) -> list[ProcessedText]:
        """
        Prétraite une colonne textuelle sans modifier
        le DataFrame source.
        """

        if text_column not in dataframe.columns:
            raise ValueError(
                f"Colonne textuelle introuvable : "
                f"{text_column}"
            )

        preprocessor = TextPreprocessor(
            config=config
        )

        return preprocessor.process_series(
            dataframe[text_column]
        )

    def analyze_frequencies(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        *,
        ngram_size: int = 1,
        top_n: int | None = 20,
        config: TextPreprocessingConfig | None = None,
    ):
        """
        Analyse les fréquences lexicales ou n-grams.
        """

        return self._frequency_analyzer.analyze(
            dataframe=dataframe,
            text_column=text_column,
            ngram_size=ngram_size,
            top_n=top_n,
            config=config,
        )

    def analyze_tfidf(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        **kwargs,
    ):
        """
        Produit la représentation descriptive TF-IDF.
        """

        return self._tfidf_vectorizer.analyze(
            dataframe=dataframe,
            text_column=text_column,
            **kwargs,
        )

    def transform_tfidf(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        **kwargs,
    ):
        """
        Produit la matrice TF-IDF pour les analyses
        sémantiques et prédictives.
        """

        return self._tfidf_vectorizer.transform(
            dataframe=dataframe,
            text_column=text_column,
            **kwargs,
        )

    def cluster_texts(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        **kwargs,
    ):
        """
        Regroupe les textes à partir de TF-IDF.
        """

        return self._text_clusterer.analyze(
            dataframe=dataframe,
            text_column=text_column,
            **kwargs,
        )

    def analyze_topics(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        **kwargs,
    ):
        """
        Découvre les thèmes latents du corpus.
        """

        return self._topic_modeler.analyze(
            dataframe=dataframe,
            text_column=text_column,
            **kwargs,
        )

    def analyze_topic_target(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        target_column: str,
        *,
        n_topics: int = 3,
        **kwargs,
    ):
        """
        Analyse l'association entre thèmes textuels
        et variable quantitative.
        """

        return (
            self._topic_target_analyzer
            .analyze(
                dataframe=dataframe,
                text_column=text_column,
                target_column=target_column,
                n_topics=n_topics,
                **kwargs,
            )
        )

    def profile_corpus(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
    ) -> CorpusProfileResult:
        """
        Produit le profil descriptif du corpus.
        """

        return self._corpus_profiler.profile(
            dataframe=dataframe,
            text_column=text_column,
        )
