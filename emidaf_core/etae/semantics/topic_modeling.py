"""
=========================================================
EMIDAF Framework v1.0
ETAE - Topic Modeling
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import numpy as np
import pandas as pd

from sklearn.decomposition import NMF

from ..preprocessing import (
    TextPreprocessingConfig,
)
from ..vectorization import (
    ETAETfidfVectorizer,
)


@dataclass(frozen=True)
class TopicSummary:
    topic: int
    top_terms: list[str]
    document_count: int
    percentage: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TopicModelingResult:
    text_column: str
    method: str
    n_documents: int
    n_topics: int
    topics: list[TopicSummary]
    dominant_topics: list[int]
    indices: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "text_column": self.text_column,
            "method": self.method,
            "n_documents": self.n_documents,
            "n_topics": self.n_topics,
            "topics": [
                topic.to_dict()
                for topic in self.topics
            ],
            "dominant_topics": (
                self.dominant_topics
            ),
            "indices": self.indices,
        }


class TopicModeler:
    """
    Découverte de thèmes latents par NMF
    sur représentation TF-IDF.
    """

    def __init__(self) -> None:
        self._tfidf = ETAETfidfVectorizer()

    def analyze(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        *,
        n_topics: int = 3,
        top_terms: int = 10,
        max_features: int | None = 5000,
        min_df: int | float = 1,
        max_df: int | float = 1.0,
        ngram_range: tuple[int, int] = (1, 2),
        random_state: int = 42,
        config: TextPreprocessingConfig | None = None,
    ) -> TopicModelingResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe doit être un DataFrame pandas."
            )

        if n_topics < 2:
            raise ValueError(
                "n_topics doit être supérieur "
                "ou égal à 2."
            )

        if top_terms < 1:
            raise ValueError(
                "top_terms doit être supérieur "
                "ou égal à 1."
            )

        (
            matrix,
            vectorizer,
            valid_indices,
        ) = self._tfidf.transform(
            dataframe=dataframe,
            text_column=text_column,
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            ngram_range=ngram_range,
            config=config,
        )

        if matrix is None:
            return TopicModelingResult(
                text_column=text_column,
                method="NMF",
                n_documents=0,
                n_topics=0,
                topics=[],
                dominant_topics=[],
                indices=[],
            )

        n_documents = int(
            matrix.shape[0]
        )

        if n_topics >= n_documents:
            raise ValueError(
                "n_topics doit être strictement "
                "inférieur au nombre de documents."
            )

        model = NMF(
            n_components=n_topics,
            init="nndsvda",
            random_state=random_state,
            max_iter=500,
        )

        document_topic = model.fit_transform(
            matrix
        )

        components = model.components_

        feature_names = np.array(
            vectorizer.get_feature_names_out()
        )

        dominant_topics = (
            document_topic.argmax(axis=1)
        )

        summaries: list[
            TopicSummary
        ] = []

        for topic_id in range(
            n_topics
        ):
            component = components[
                topic_id
            ]

            ranked_indices = (
                component.argsort()[::-1]
            )[:top_terms]

            terms = [
                str(
                    feature_names[index]
                )
                for index in ranked_indices
                if component[index] > 0
            ]

            document_count = int(
                (
                    dominant_topics
                    == topic_id
                ).sum()
            )

            percentage = float(
                (
                    document_count
                    / n_documents
                )
                * 100.0
            )

            summaries.append(
                TopicSummary(
                    topic=int(
                        topic_id
                    ),
                    top_terms=terms,
                    document_count=(
                        document_count
                    ),
                    percentage=percentage,
                )
            )

        return TopicModelingResult(
            text_column=text_column,
            method="NMF",
            n_documents=n_documents,
            n_topics=n_topics,
            topics=summaries,
            dominant_topics=[
                int(topic)
                for topic
                in dominant_topics
            ],
            indices=list(
                valid_indices
            ),
        )
