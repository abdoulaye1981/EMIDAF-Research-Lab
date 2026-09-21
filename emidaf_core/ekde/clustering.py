"""
=========================================================
EMIDAF Framework
EKDE - Exploratory Clustering
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Clustering exploratoire non supervisé.

La standardisation des données n'est pas réalisée
silencieusement par ce module. Les données doivent être
préparées explicitement avant l'appel au moteur.
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.cluster import (
    KMeans,
    DBSCAN,
)
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)

from emidaf_core.common.results.model_result import (
    ModelResult,
)


class KMeansClustering:
    """
    Clustering exploratoire par K-Means.
    """

    name = "K-Means"
    task = "clustering"
    scaling_sensitive = True

    @classmethod
    def fit(
        cls,
        dataframe: pd.DataFrame,
        n_clusters: int = 3,
        random_state: int = 42,
    ) -> ModelResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "KMeansClustering attend un "
                "pandas.DataFrame."
            )

        if dataframe.empty:
            raise ValueError(
                "Le dataframe est vide."
            )

        non_numeric = [
            column
            for column in dataframe.columns
            if not pd.api.types.is_numeric_dtype(
                dataframe[column]
            )
        ]

        if non_numeric:
            raise ValueError(
                "Toutes les variables doivent être "
                "numériques avant K-Means. "
                f"Variables non numériques : "
                f"{non_numeric}"
            )

        if dataframe.isna().any().any():
            raise ValueError(
                "K-Means ne peut pas être exécuté "
                "avec des valeurs manquantes."
            )

        n_observations = len(
            dataframe
        )

        try:
            n_clusters = int(
                n_clusters
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "n_clusters doit être un entier."
            ) from exc

        if n_clusters < 2:
            raise ValueError(
                "K-Means nécessite au moins "
                "2 clusters."
            )

        if n_clusters >= n_observations:
            raise ValueError(
                "n_clusters doit être strictement "
                "inférieur au nombre "
                "d'observations."
            )

        model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init="auto",
        )

        labels = model.fit_predict(
            dataframe
        )

        unique_labels = np.unique(
            labels
        )

        if len(unique_labels) < 2:
            silhouette = None
            davies_bouldin = None
            calinski_harabasz = None
        else:
            silhouette = float(
                silhouette_score(
                    dataframe,
                    labels,
                )
            )

            davies_bouldin = float(
                davies_bouldin_score(
                    dataframe,
                    labels,
                )
            )

            calinski_harabasz = float(
                calinski_harabasz_score(
                    dataframe,
                    labels,
                )
            )

        return ModelResult(
            model_name=cls.name,
            algorithm="KMeans",
            model_type="unsupervised",
            task="clustering",
            library="scikit-learn",
            fitted=True,
            train_size=n_observations,
            test_size=0,
            features=list(
                dataframe.columns
            ),
            estimator=model,
            parameters={
                "n_clusters": n_clusters,
                "random_state": random_state,
                "n_init": "auto",
                "scaling_sensitive": True,
            },
            predictions=(
                labels
                .astype(int)
                .tolist()
            ),
            silhouette_score=silhouette,
            davies_bouldin_score=(
                davies_bouldin
            ),
            calinski_harabasz_score=(
                calinski_harabasz
            ),
            inertia=float(
                model.inertia_
            ),
            cluster_centers=(
                model.cluster_centers_
                .tolist()
            ),
        )

    fit_predict = fit


class DBSCANClustering:
    """
    Clustering exploratoire par DBSCAN.

    Les observations étiquetées -1 sont considérées
    comme du bruit et ne sont pas supprimées.

    Les métriques de partitionnement sont calculées
    uniquement sur les observations appartenant à
    des clusters lorsque cela est mathématiquement
    possible.
    """

    name = "DBSCAN"
    task = "clustering"
    scaling_sensitive = True

    @classmethod
    def fit(
        cls,
        dataframe: pd.DataFrame,
        eps: float = 0.5,
        min_samples: int = 5,
    ) -> ModelResult:

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                "DBSCANClustering attend un "
                "pandas.DataFrame."
            )

        if dataframe.empty:
            raise ValueError(
                "Le dataframe est vide."
            )

        non_numeric = [
            column
            for column in dataframe.columns
            if not pd.api.types.is_numeric_dtype(
                dataframe[column]
            )
        ]

        if non_numeric:
            raise ValueError(
                "Toutes les variables doivent être "
                "numériques avant DBSCAN. "
                f"Variables non numériques : "
                f"{non_numeric}"
            )

        if dataframe.isna().any().any():
            raise ValueError(
                "DBSCAN ne peut pas être exécuté "
                "avec des valeurs manquantes."
            )

        try:
            eps = float(eps)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "eps doit être une valeur numérique."
            ) from exc

        try:
            min_samples = int(
                min_samples
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "min_samples doit être un entier."
            ) from exc

        if eps <= 0:
            raise ValueError(
                "eps doit être strictement positif."
            )

        if min_samples < 2:
            raise ValueError(
                "min_samples doit être au moins égal à 2."
            )

        n_observations = len(
            dataframe
        )

        if min_samples > n_observations:
            raise ValueError(
                "min_samples ne peut pas dépasser "
                "le nombre d'observations."
            )

        model = DBSCAN(
            eps=eps,
            min_samples=min_samples,
        )

        labels = model.fit_predict(
            dataframe
        )

        cluster_labels = sorted(
            int(label)
            for label in np.unique(labels)
            if label != -1
        )

        n_clusters = len(
            cluster_labels
        )

        noise_mask = (
            labels == -1
        )

        noise_count = int(
            noise_mask.sum()
        )

        noise_percentage = (
            100.0
            * noise_count
            / n_observations
        )

        clustered_mask = (
            labels != -1
        )

        clustered_data = dataframe.loc[
            clustered_mask
        ]

        clustered_labels = labels[
            clustered_mask
        ]

        unique_clustered_labels = np.unique(
            clustered_labels
        )

        silhouette = None
        davies_bouldin = None
        calinski_harabasz = None

        if (
            len(clustered_data) >= 2
            and len(unique_clustered_labels) >= 2
            and len(unique_clustered_labels)
            < len(clustered_data)
        ):
            silhouette = float(
                silhouette_score(
                    clustered_data,
                    clustered_labels,
                )
            )

            davies_bouldin = float(
                davies_bouldin_score(
                    clustered_data,
                    clustered_labels,
                )
            )

            calinski_harabasz = float(
                calinski_harabasz_score(
                    clustered_data,
                    clustered_labels,
                )
            )

        return ModelResult(
            model_name=cls.name,
            algorithm="DBSCAN",
            model_type="unsupervised",
            task="clustering",
            library="scikit-learn",
            fitted=True,
            train_size=n_observations,
            test_size=0,
            features=list(
                dataframe.columns
            ),
            estimator=model,
            parameters={
                "eps": eps,
                "min_samples": min_samples,
                "scaling_sensitive": True,
                "n_clusters": n_clusters,
                "noise_count": noise_count,
                "noise_percentage": (
                    noise_percentage
                ),
            },
            predictions=(
                labels
                .astype(int)
                .tolist()
            ),
            silhouette_score=silhouette,
            davies_bouldin_score=(
                davies_bouldin
            ),
            calinski_harabasz_score=(
                calinski_harabasz
            ),
        )

    fit_predict = fit
