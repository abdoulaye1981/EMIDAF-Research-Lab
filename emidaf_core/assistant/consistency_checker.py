from __future__ import annotations

import json
import re
from typing import Any


class ConsistencyChecker:
    """
    Garde-fou de fidélité pour les textes générés par l'IA.

    Il ne constitue pas une validation scientifique complète.

    Il vérifie principalement :
    - l'apparition de valeurs numériques absentes du contexte ;
    - certaines extrapolations qualitatives potentiellement
      non soutenues ;
    - certaines recommandations non présentes dans la source.

    Seules les représentations numériques strictement
    équivalentes sont considérées comme cohérentes
    (virgule/point, séparateurs de milliers,
    zéros décimaux non significatifs).

    Les conversions décimal <-> pourcentage,
    les arrondis et les approximations sont interdites.
    """

    NUMBER_PATTERN = re.compile(
        r"(?<![A-Za-z])"
        r"-?"
        r"(?:"
        r"\d{1,3}(?:[ \u00A0\u202F]\d{3})+"
        r"|"
        r"\d+"
        r")"
        r"(?:[.,]\d+)?"
        r"(?:[eE][+-]?\d+)?"
        r"(?:\s*%)?"
    )

    QUALITATIVE_PATTERNS = (
        (
            "qualification_performance",
            re.compile(
                r"\bperformance\s+(?:globale\s+)?"
                r"(?:bonne|mauvaise|faible|élevée|"
                r"modérée|acceptable|satisfaisante|"
                r"excellente|insuffisante|robuste|"
                r"raisonnable|prometteuse)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "sous_detection",
            re.compile(
                r"\b(?:sous[- ]?détect\w*|"
                r"sous[- ]?détection)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "sur_detection",
            re.compile(
                r"\b(?:sur[- ]?détect\w*|"
                r"sur[- ]?détection)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "recommendation_seuil",
            re.compile(
                r"\b(?:modifier|ajuster|changer)"
                r".{0,30}\bseuil\b",
                re.IGNORECASE,
            ),
        ),
        (
            "recommendation_variables",
            re.compile(
                r"\b(?:ajouter|supprimer|retirer)"
                r".{0,30}\bvariables?\b",
                re.IGNORECASE,
            ),
        ),
        (
            "recommendation_modele",
            re.compile(
                r"\b(?:changer|remplacer|réentraîner)"
                r".{0,30}\bmodèle\b",
                re.IGNORECASE,
            ),
        ),
        (
            "utilisabilite_operationnelle",
            re.compile(
                r"\b(?:prêt[e]?\s+pour\s+(?:le\s+)?déploiement|"
                r"prêt[e]?\s+pour\s+(?:la\s+)?production|"
                r"déployer\s+le\s+modèle|"
                r"utilisable\s+en\s+production)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "qualification_effet",
            re.compile(
                r"\b(?:effet|taille\s+d['’]effet|effets?)"
                r".{0,40}\b(?:faible|faibles|modeste|modestes|"
                r"modéré|modérée|modérés|modérées|fort|forte|"
                r"forts|fortes|élevé|élevée|élevés|élevées)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "qualification_silhouette",
            re.compile(
                r"\b(?:silhouette|indice\s+de\s+silhouette)"
                r".{0,50}\b(?:faible|très\s+faible|élevé|élevée|"
                r"bon|bonne|mauvais|mauvaise|robuste)\b"
                r"|"
                r"\b(?:faible|très\s+faible|élevé|élevée)"
                r".{0,40}\b(?:silhouette|indice\s+de\s+silhouette)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "qualification_normalite",
            re.compile(
                r"\b(?:proche|proximité|approximativement)"
                r".{0,20}\b(?:normal|normale|normalité)\b"
                r"|"
                r"\b(?:normalité\s+approximative)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "qualification_intermediaire",
            re.compile(
                r"\b(?:valeur|valeurs|métrique|métriques|performance|"
                r"performances)"
                r".{0,40}\b(?:intermédiaire|intermédiaires)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "dataset_complet",
            re.compile(
                r"\b(?:jeu\s+de\s+données|données|dataset)"
                r".{0,30}\b(?:complet|complète|complets|complètes)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "structure_substantielle",
            re.compile(
                r"\b(?:structure|structures|cluster|clusters|groupes?)"
                r".{0,50}\b(?:substantiel|substantielle|"
                r"substantiels|substantielles|distinct|distincte|"
                r"distincts|distinctes)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "importance_influence",
            re.compile(
                r"\b(?:importance|importance\s+de\s+permutation)"
                r".{0,50}\b(?:influence|influencent|influent|"
                r"facteur\s+influent|facteurs\s+influents)\b"
                r"|"
                r"\b(?:variable|variables)"
                r".{0,40}\b(?:plus\s+influente|plus\s+influentes|"
                r"influente|influentes)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "qualification_dataset_quality",
            re.compile(
                r"\b(?:données|jeu\s+de\s+données|dataset)"
                r".{0,35}\b(?:bonne\s+qualité|"
                r"très\s+bonne\s+qualité|"
                r"qualité\s+satisfaisante|"
                r"qualité\s+élevée)\b"
                r"|"
                r"\b(?:bonne|très\s+bonne)"
                r"\s+qualité\s+(?:des\s+)?données\b",
                re.IGNORECASE,
            ),
        ),
        (
            "dataset_ready_for_use",
            re.compile(
                r"\b(?:données|jeu\s+de\s+données|dataset)"
                r".{0,40}\b(?:prêt|prête|prêts|prêtes)"
                r"\s+(?:à|a)\s+(?:être\s+)?"
                r"(?:utilisé|utilisée|utilisés|utilisées|analysé|analysée|"
                r"analysés|analysées)\b"
                r"|"
                r"\b(?:prêt|prête|prêts|prêtes)"
                r"\s+pour\s+(?:l['’])?analyse\b",
                re.IGNORECASE,
            ),
        ),

    )

    HARD_UNSUPPORTED_PATTERNS = (
        (
            "invented_elae_expansion",
            re.compile(
                r"\banalyse\s+exploratoire\s+linéaire\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_ekde_method",
            re.compile(
                r"\bdensité\s+kernel\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_asymmetry",
            re.compile(
                r"\basymétrie\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_kurtosis",
            re.compile(
                r"\bkurtosis\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_random_baseline",
            re.compile(
                r"\b(?:supérieur|supérieure|supérieurs|supérieures)"
                r"\s+au\s+hasard\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_elae_expansion_statistique",
            re.compile(
                r"\banalyse\s+exploratoire\s+et\s+statistique\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_ekde_expansion_structure",
            re.compile(
                r"\banalyse\s+de\s+structure\s+et\s+de\s+dépendance\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_edse_expansion_threshold",
            re.compile(
                r"\bévaluation\s+de\s+la\s+décision\s+et\s+du\s+seuil\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_eaie_expansion_engine",
            re.compile(
                r"\bmoteur\s+d['’]intelligence\s+artificielle\s+EMIDAF\b",
                re.IGNORECASE,
            ),
        ),
        (
            "invented_exaie_expansion",
            re.compile(
                r"\bexplicabilité\s+de\s+l['’]IA\s+EMIDAF\b",
                re.IGNORECASE,
            ),
        ),
    )


    NEGATION_MARKERS = (
        "aucun",
        "aucune",
        "sans",
        "impossible",
        "ne peut pas",
        "ne permet pas",
        "n'est pas",
        "n’est pas",
        "empêche",
        "manque de",
        "absence de",
        "non disponible",
    )

    @classmethod
    def check(
        cls,
        generated_text: str,
        source_context: dict[str, Any],
    ) -> dict[str, Any]:

        source_text = json.dumps(
            source_context,
            ensure_ascii=False,
            default=str,
        )

        generated_for_numbers = cls._clean_text_for_numbers(
            generated_text
        )

        # --------------------------------------------------
        # Ignorer uniquement les numéros structurels
        # des titres Markdown :
        #   ## 2.1 Préparation
        #   ### 3.2 Résultats
        #
        # Une valeur "2.1" utilisée dans une phrase
        # scientifique reste contrôlée normalement.
        # --------------------------------------------------
        generated_for_numbers = re.sub(
            r"(?m)^(\s{0,3}#{1,6}\s+)"
            r"\d+(?:[.,]\d+)+"
            r"(?:[.)])?"
            r"(?=\s)",
            r"\1",
            generated_for_numbers,
        )

        source_for_numbers = cls._clean_text_for_numbers(
            source_text
        )

        generated_numbers = {
            cls._normalize_number(value)
            for value in cls.NUMBER_PATTERN.findall(
                generated_for_numbers
            )
        }

        source_numbers = {
            cls._normalize_number(value)
            for value in cls.NUMBER_PATTERN.findall(
                source_for_numbers
            )
        }

        generated_numbers.discard("")
        source_numbers.discard("")

        suspicious_numbers: list[str] = []

        for value in sorted(generated_numbers):

            if cls._number_supported(
                value,
                source_numbers,
            ):
                continue

            suspicious_numbers.append(value)

        unsupported_claims: list[str] = []

        for name, pattern in cls.QUALITATIVE_PATTERNS:

            for match in pattern.finditer(
                generated_text
            ):

                if cls._is_negated_context(
                    generated_text,
                    match.start(),
                    match.end(),
                ):
                    continue

                if pattern.search(source_text):
                    continue

                unsupported_claims.append(name)
                break

        # Contrôles sémantiques stricts :
        # aucune tolérance par contexte de négation.
        for name, pattern in cls.HARD_UNSUPPORTED_PATTERNS:

            if not pattern.search(generated_text):
                continue

            # Autorisé uniquement si le même élément
            # figure explicitement dans la source.
            if pattern.search(source_text):
                continue

            if name not in unsupported_claims:
                unsupported_claims.append(name)

        valid = (
            not suspicious_numbers
            and not unsupported_claims
        )

        return {
            "valid": valid,
            "suspicious_numbers": suspicious_numbers,
            "unsupported_claims": unsupported_claims,
            "generated_numbers_count": len(
                generated_numbers
            ),
            "source_numbers_count": len(
                source_numbers
            ),
        }

    @classmethod
    def _number_supported(
        cls,
        generated_value: str,
        source_numbers: set[str],
    ) -> bool:
        """
        Vérifie qu'une valeur numérique générée est
        réellement présente dans le contexte source.

        Sont tolérées uniquement les différences
        de représentation d'une même valeur :
        - virgule / point ;
        - séparateurs de milliers ;
        - zéros décimaux non significatifs.

        Les conversions décimal <-> pourcentage
        sont interdites.
        """

        if generated_value in source_numbers:
            return True

        generated_is_percent = (
            generated_value.endswith("%")
        )

        try:
            generated_float = float(
                generated_value.replace("%", "")
            )
        except ValueError:
            return False

        for source_value in source_numbers:

            source_is_percent = (
                source_value.endswith("%")
            )

            # Une valeur en % ne peut correspondre
            # qu'à une valeur source également en %.
            if (
                generated_is_percent
                != source_is_percent
            ):
                continue

            try:
                source_float = float(
                    source_value.replace("%", "")
                )
            except ValueError:
                continue

            # Même valeur numérique,
            # même nature (% ou non-%).
            if abs(
                generated_float - source_float
            ) < 1e-12:
                return True

        return False

    @staticmethod
    def _normalize_number(
        value: str,
    ) -> str:

        return (
            str(value)
            .strip()
            .replace("\u202f", "")
            .replace("\xa0", "")
            .replace(" ", "")
            .replace("\t", "")
            .replace("\n", "")
            .replace(",", ".")
        )

    @staticmethod
    def _clean_text_for_numbers(
        text: str,
    ) -> str:
        """
        Supprime la numérotation structurelle Markdown
        sans supprimer les vraies valeurs scientifiques.
        """

        text = str(text)

        # **1. Observations**
        text = re.sub(
            r"(?m)^\s*\*{0,2}"
            r"\d{1,2}\\?[.)]"
            r"\*{0,2}\s+",
            "",
            text,
        )

        # ## 1. Observations
        text = re.sub(
            r"(?m)^\s*#{1,6}\s*"
            r"\d{1,2}\\?[.)]\s+",
            "",
            text,
        )

        # 1. Élément
        text = re.sub(
            r"(?m)^\s*"
            r"\d{1,2}\\?[.)]\s+",
            "",
            text,
        )

        return text

    @classmethod
    def _is_negated_context(
        cls,
        text: str,
        start: int,
        end: int,
    ) -> bool:
        """
        Évite les faux positifs lorsque le texte indique
        précisément qu'une conclusion ne peut pas être établie.
        """

        left = max(
            0,
            start - 120,
        )

        right = min(
            len(text),
            end + 80,
        )

        window = (
            text[left:right]
            .lower()
        )

        return any(
            marker in window
            for marker in cls.NEGATION_MARKERS
        )
