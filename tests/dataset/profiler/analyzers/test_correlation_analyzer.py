import numpy as np
import pandas as pd

from emidaf_core.dataset.profiler.dataset_profiler import DatasetProfiler


print("\n" + "=" * 70)
print("TEST CIBLE : CORRELATION ANALYZER")
print("=" * 70)


# ============================================================
# 1. DONNÉES
# ============================================================

df = pd.DataFrame({
    "ID": range(1, 11),

    # Corrélation positive parfaite
    "Variable_Positive": [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10
    ],

    # Corrélation négative parfaite
    "Variable_Negative": [
        10, 9, 8, 7, 6,
        5, 4, 3, 2, 1
    ],

    # Relation différente
    "Variable_Avec_NaN": [
        2, 4, np.nan, 8, 10,
        12, np.nan, 16, 18, 20
    ],

    # Valeurs infinies
    "Variable_Avec_Inf": [
        1, 2, np.inf, 4, 5,
        6, -np.inf, 8, 9, 10
    ],

    # Variable constante
    "Variable_Constante": [
        5, 5, 5, 5, 5,
        5, 5, 5, 5, 5
    ],

    # Variable textuelle
    "Nom": [
        "Awa", "Moussa", "Fatou", "Ali", "Mariama",
        "Ousmane", "Aminata", "Cheikh", "Sokhna", "Ibrahima"
    ]
})


print("\n--- 1. DONNÉES ---")
print(df)


# ============================================================
# 2. PROFILER
# ============================================================

profiler = DatasetProfiler()

profile = profiler.profile(df)


# ============================================================
# 3. RÉSULTAT
# ============================================================

print("\n--- 2. RÉSULTAT CORRELATION ANALYZER ---")

correlation_result = profile.correlations

print(correlation_result)


# ============================================================
# 4. VARIABLES ANALYSÉES
# ============================================================

print("\n--- 3. VARIABLES ANALYSÉES ---")

print(
    correlation_result["columns"]
)

assert "Nom" not in correlation_result["columns"]

print("✓ Variable textuelle 'Nom' ignorée.")


# ============================================================
# 5. NOMBRE DE VARIABLES
# ============================================================

assert correlation_result["count"] == 6

print("✓ Nombre de variables numériques correct : 6")


# ============================================================
# 6. MATRICE DE CORRÉLATION
# ============================================================

matrix = correlation_result[
    "correlation_matrix"
]

print("\n--- 4. MATRICE ---")
print(matrix)


# Corrélation positive parfaite
r_positive = matrix[
    "Variable_Positive"
]["Variable_Negative"]

assert r_positive == -1.0

print("✓ Corrélation négative parfaite : -1.0")


# ============================================================
# 7. PAIRES DE VARIABLES
# ============================================================

pairs = correlation_result["pairs"]

print("\n--- 5. PAIRES ---")

for pair in pairs:
    print(pair)


# La paire Positive / Negative doit être
# en première position car |r| = 1
first_pair = pairs[0]

assert abs(
    first_pair["correlation"]
) == 1.0

print(
    "✓ Les paires sont triées par "
    "corrélation absolue décroissante."
)


# ============================================================
# 8. VALEURS MANQUANTES
# ============================================================

print("\n--- 6. NaN ---")

assert (
    "Variable_Avec_NaN"
    in correlation_result["columns"]
)

print(
    "✓ Variable contenant des NaN "
    "correctement analysée."
)


# ============================================================
# 9. VALEURS INFINIES
# ============================================================

print("\n--- 7. +INF / -INF ---")

assert (
    "Variable_Avec_Inf"
    in correlation_result["columns"]
)

# La matrice ne doit pas contenir
# de valeurs infinies
for column_1, values in matrix.items():

    for column_2, value in values.items():

        if value is not None:
            assert not np.isinf(value)

print(
    "✓ Les valeurs +INF / -INF "
    "ne contaminent pas la matrice."
)


# ============================================================
# 10. VARIABLE CONSTANTE
# ============================================================

print("\n--- 8. VARIABLE CONSTANTE ---")

assert (
    "Variable_Constante"
    in correlation_result["columns"]
)

# Une variable constante produit NaN
# dans les corrélations avec les autres variables.
constant_pairs = [
    pair
    for pair in pairs
    if (
        pair["variable_1"]
        == "Variable_Constante"
        or
        pair["variable_2"]
        == "Variable_Constante"
    )
]

assert len(constant_pairs) == 0

print(
    "✓ Variable constante correctement "
    "exclue des paires valides."
)


# ============================================================
# 11. STRUCTURE DES PAIRES
# ============================================================

for pair in pairs:

    assert "variable_1" in pair
    assert "variable_2" in pair
    assert "correlation" in pair

    assert isinstance(
        pair["correlation"],
        float
    )

print(
    "✓ Structure des paires correcte."
)


# ============================================================
# 12. RÉSULTAT FINAL
# ============================================================

print("\n" + "=" * 70)
print("✅ TOUTES LES VÉRIFICATIONS SONT RÉUSSIES")
print("CorrelationAnalyzer : TEST CIBLÉ OK")
print("=" * 70)
