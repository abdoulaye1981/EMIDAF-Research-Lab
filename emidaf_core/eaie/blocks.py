"""
=========================================================
EMIDAF Framework
EAIE - Scientific Feature Blocks
=========================================================

Gestion générique des blocs scientifiques de variables
pour les comparaisons prédictives incrémentales.

Un bloc représente une famille conceptuelle de variables.

Exemple :

A : variables individuelles
B : variables familiales
C : variables pédagogiques
D : variables institutionnelles

Les comparaisons cumulatives deviennent alors :

A
A + B
A + B + C
A + B + C + D
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Mapping
from typing import Sequence


@dataclass(slots=True)
class FeatureBlockResult:
    """
    Résultat de la résolution des blocs scientifiques.
    """

    blocks: dict[str, list[str]] = field(
        default_factory=dict
    )

    cumulative: dict[str, list[str]] = field(
        default_factory=dict
    )

    predictors: list[str] = field(
        default_factory=list
    )

    assigned: list[str] = field(
        default_factory=list
    )

    unassigned: list[str] = field(
        default_factory=list
    )

    protected: list[str] = field(
        default_factory=list
    )

    target: str | None = None

    valid: bool = True

    conflicts: list[str] = field(
        default_factory=list
    )

    def to_dict(self) -> dict:
        """
        Sérialisation simple pour Dash / reporting.
        """

        return {
            "blocks": {
                name: list(values)
                for name, values
                in self.blocks.items()
            },
            "cumulative": {
                name: list(values)
                for name, values
                in self.cumulative.items()
            },
            "predictors": list(
                self.predictors
            ),
            "assigned": list(
                self.assigned
            ),
            "unassigned": list(
                self.unassigned
            ),
            "protected": list(
                self.protected
            ),
            "target": self.target,
            "valid": self.valid,
            "conflicts": list(
                self.conflicts
            ),
        }


class FeatureBlocks:
    """
    Résolution et validation des blocs scientifiques.

    Cette classe est volontairement générique :
    aucune variable liée à une étude particulière
    n'est codée dans le moteur EAIE.
    """

    @staticmethod
    def resolve(
        *,
        predictors: Sequence[str],
        blocks: Mapping[
            str,
            Sequence[str],
        ],
        target: str | None = None,
        protected: Sequence[str] | None = None,
        require_all: bool = False,
    ) -> FeatureBlockResult:
        """
        Valide et construit les blocs scientifiques.

        Parameters
        ----------
        predictors
            Variables admissibles issues, par exemple,
            de FeatureRoles.

        blocks
            Dictionnaire ordonné :
            nom_bloc -> variables du bloc.

        target
            Variable cible éventuelle.

        protected
            Variables explicitement protégées.

        require_all
            Si True, toute variable admissible doit
            appartenir à exactement un bloc.
        """

        predictor_list = list(
            dict.fromkeys(
                predictors
            )
        )

        predictor_set = set(
            predictor_list
        )

        protected_list = list(
            dict.fromkeys(
                protected or []
            )
        )

        protected_set = set(
            protected_list
        )

        conflicts: list[str] = []

        normalized_blocks: dict[
            str,
            list[str],
        ] = {}

        seen_variables: dict[
            str,
            str,
        ] = {}

        if not blocks:
            conflicts.append(
                "Aucun bloc scientifique n'est défini."
            )

        for raw_name, raw_variables in (
            blocks.items()
        ):

            name = str(
                raw_name
            ).strip()

            if not name:
                conflicts.append(
                    "Un bloc possède un nom vide."
                )
                continue

            if name in normalized_blocks:
                conflicts.append(
                    f"Le bloc '{name}' est défini "
                    "plusieurs fois."
                )
                continue

            variables = list(
                dict.fromkeys(
                    raw_variables or []
                )
            )

            normalized_blocks[
                name
            ] = variables

            if not variables:
                conflicts.append(
                    f"Le bloc '{name}' ne contient "
                    "aucune variable."
                )

            for variable in variables:

                if variable == target:
                    conflicts.append(
                        f"La cible '{variable}' ne peut "
                        "pas appartenir à un bloc "
                        "prédictif."
                    )

                if variable in protected_set:
                    conflicts.append(
                        f"La variable protégée "
                        f"'{variable}' ne peut pas "
                        "appartenir à un bloc."
                    )

                if variable not in predictor_set:
                    conflicts.append(
                        f"La variable '{variable}' du "
                        f"bloc '{name}' n'est pas un "
                        "prédicteur admissible."
                    )

                previous_block = (
                    seen_variables.get(
                        variable
                    )
                )

                if (
                    previous_block is not None
                    and previous_block != name
                ):
                    conflicts.append(
                        f"La variable '{variable}' "
                        "appartient à plusieurs blocs : "
                        f"'{previous_block}' et '{name}'."
                    )
                else:
                    seen_variables[
                        variable
                    ] = name

        assigned = [
            variable
            for variable
            in predictor_list
            if variable in seen_variables
        ]

        unassigned = [
            variable
            for variable
            in predictor_list
            if variable not in seen_variables
        ]

        if (
            require_all
            and unassigned
        ):
            conflicts.append(
                "Certaines variables admissibles ne "
                "sont affectées à aucun bloc : "
                + ", ".join(
                    unassigned
                )
            )

        cumulative: dict[
            str,
            list[str],
        ] = {}

        running: list[str] = []

        for name, variables in (
            normalized_blocks.items()
        ):

            for variable in variables:

                if (
                    variable in predictor_set
                    and variable not in running
                    and variable != target
                    and variable
                    not in protected_set
                ):
                    running.append(
                        variable
                    )

            cumulative[
                name
            ] = list(
                running
            )

        return FeatureBlockResult(
            blocks=normalized_blocks,
            cumulative=cumulative,
            predictors=predictor_list,
            assigned=assigned,
            unassigned=unassigned,
            protected=protected_list,
            target=target,
            valid=not conflicts,
            conflicts=conflicts,
        )


def resolve_feature_blocks(
    *,
    predictors: Sequence[str],
    blocks: Mapping[
        str,
        Sequence[str],
    ],
    target: str | None = None,
    protected: Sequence[str] | None = None,
    require_all: bool = False,
) -> FeatureBlockResult:
    """
    Façade fonctionnelle.
    """

    return FeatureBlocks.resolve(
        predictors=predictors,
        blocks=blocks,
        target=target,
        protected=protected,
        require_all=require_all,
    )
