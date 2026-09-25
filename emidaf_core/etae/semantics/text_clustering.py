"""
=========================================================
EMIDAF Framework v1.0
ETAE - Text Clustering
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)

from ..preprocessing import (
    TextPreprocessingConfig,
)
from ..vectorization import (
    ETAETfidfVectorizer,
)


@dataclass(frozen=True)
class TextClusterSummary:
    cluster: int
    size: int
    percentage: float
    top_terms: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TextClusteringResult:
    text_column: str
    n_documents: int
    n_clusters: int
    silhouette_score: float | None
    davies_bouldin_score: float | None
    calinski_harabasz_score: float | None
    clusters: list[TextClusterSummary]
    labels: list[int]
    indices: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "text_column": self.text_column,
            "n_documents": self.n_documents,
            "n_clusters": self.n_clusters,
            "silhouette_score": (
                self.silhouette_score
            ),
            "davies_bouldin_score": (
                self.davies_bouldin_score
            ),
            "calinski_harabasz_score": (
                self.calinski_harabasz_score
            ),
            "clusters": [
                cluster.to_dict()
                for cluster in self.clusters
            ],
            "labels": self.labels,
            "indices": self.indices,
        }


class TextClusterer:
    """
    Regroupe les documents textuels à partir
    d'une représentation TF-IDF.
    """

    def __init__(self) -> None:
        self._tfidf = ETAETfidfVectorizer()

    def analyze(
        self,
        dataframe: pd.DataFrame,
        text_column: str,
        *,
        n_clusters: int = 3,
        max_features: int | None = 5000,
        min_df: int | float = 1,
        max_df: int | float = 1.0,
        ngram_range: tuple[int, int] = (1, 2),
        top_terms: int = 10,
        random_state: int = 42,
        config: TextPreprocessingConfig | None = None,
    ) -> TextClusteringResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "dataframe doit être un DataFrame pandas."
            )

        if n_clusters < 2:
            raise ValueError(
                "n_clusters doit être supérieur "
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
            return TextClusteringResult(
                text_column=text_column,
                n_documents=0,
                n_clusters=0,
                silhouette_score=None,
                davies_bouldin_score=None,
                calinski_harabasz_score=None,
                clusters=[],
                labels=[],
                indices=[],
            )

        n_documents = int(
            matrix.shape[0]
        )

        if n_clusters >= n_documents:
            raise ValueError(
                "n_clusters doit être strictement "
                "inférieur au nombre de documents."
            )

        model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=10,
        )

        labels = model.fit_predict(
            matrix
        )

        dense_matrix = (
            matrix.toarray()
        )

        silhouette = float(
            silhouette_score(
                matrix,
                labels,
            )
        )

        davies_bouldin = float(
            davies_bouldin_score(
                dense_matrix,
                labels,
            )
        )

        calinski_harabasz = float(
            calinski_harabasz_score(
                dense_matrix,
                labels,
            )
        )

        feature_names = np.array(
            vectorizer.get_feature_names_out()
        )

        summaries: list[
            TextClusterSummary
        ] = []

        for cluster_id in range(
            n_clusters
        ):
            mask = labels == cluster_id

            size = int(
                mask.sum()
            )

            percentage = float(
                (
                    size
                    / n_documents
                )
                * 100.0
            )

            centroid = (
                model.cluster_centers_[
                    cluster_id
                ]
            )

            ranked_indices = (
                centroid.argsort()[::-1]
            )[:top_terms]

            terms = [
                str(
                    feature_names[index]
                )
                for index in ranked_indices
                if centroid[index] > 0
            ]

            summaries.append(
                TextClusterSummary(
                    cluster=int(
                        cluster_id
                    ),
                    size=size,
                    percentage=percentage,
                    top_terms=terms,
                )
            )

        return TextClusteringResult(
            text_column=text_column,
            n_documents=n_documents,
            n_clusters=n_clusters,
            silhouette_score=silhouette,
            davies_bouldin_score=(
                davies_bouldin
            ),
            calinski_harabasz_score=(
                calinski_harabasz
            ),
            clusters=summaries,
            labels=[
                int(label)
                for label in labels
            ],
            indices=list(
                valid_indices
            ),
        )
