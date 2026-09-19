import numpy as np
import pandas as pd

from emidaf_core.dataset.profiler.dataset_profiler import DatasetProfiler


print("\n" + "=" * 70)
print("TEST CIBLE : DISTRIBUTION ANALYZER")
print("=" * 70)


# -------------------------------------------------------------------
# 1. Jeu de données de test
# -------------------------------------------------------------------

df = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5, 6, 7, 8],

    "Age": [
        20, 21, 22, np.nan,
        24, 25, np.inf, -np.inf
    ],

    "Note": [
        10, 12, 14, 16,
        18, 20, 22, 24
    ],

    "Salaire": [
        100000, 120000, 110000, np.nan,
        130000, 125000, 140000, 150000
    ],

    "Constante": [
        5, 5, 5, 5,
        5, 5, 5, 5
    ],

    "Nom": [
        "Awa", "Moussa", "Fatou", "Ali",
        "Mariama", "Ousmane", "Sokhna", "Ibrahima"
    ]
})


print("\n--- 1. DONNÉES ---")
print(df)


# -------------------------------------------------------------------
# 2. Profilage
# -------------------------------------------------------------------

profiler = DatasetProfiler()

result = profiler.profile(df)


# -------------------------------------------------------------------
# 3. Vérification de DatatypeAnalyzer
# -------------------------------------------------------------------

print("\n--- 2. VARIABLES NUMÉRIQUES DÉTECTÉES ---")

datatype = result.datatypes

print(datatype)


# -------------------------------------------------------------------
# 4. Résultat DistributionAnalyzer
# -------------------------------------------------------------------

print("\n--- 3. RÉSULTAT DISTRIBUTION ---")

distribution = result.distributions

print(distribution)


# -------------------------------------------------------------------
# 5. Nombre de variables analysées
# -------------------------------------------------------------------

print("\n--- 4. NOMBRE DE VARIABLES ---")

print(
    "count =",
    distribution.get("count")
)


# -------------------------------------------------------------------
# 6. Détail de chaque variable
# -------------------------------------------------------------------

print("\n--- 5. DÉTAIL DES DISTRIBUTIONS ---")

for column, statistics in distribution["columns"].items():

    print(f"\n{column}")

    for key, value in statistics.items():
        print(f"  {key}: {value}")


# -------------------------------------------------------------------
# 7. Vérifications automatiques
# -------------------------------------------------------------------

print("\n--- 6. VÉRIFICATIONS ---")

assert "ID" in distribution["columns"]
assert "Age" in distribution["columns"]
assert "Note" in distribution["columns"]
assert "Salaire" in distribution["columns"]
assert "Constante" in distribution["columns"]

# Nom ne doit pas être analysée comme variable numérique
assert "Nom" not in distribution["columns"]

# Age : NaN + inf + -inf
age = distribution["columns"]["Age"]

assert age["count"] == 5

# Les statistiques doivent être calculées uniquement
# sur les valeurs finies : 20, 21, 22, 24, 25
assert age["minimum"] == 20.0
assert age["maximum"] == 25.0

# Note : toutes les valeurs sont exploitables
note = distribution["columns"]["Note"]

assert note["count"] == 8
assert note["minimum"] == 10.0
assert note["maximum"] == 24.0
assert note["median"] == 17.0

# Constante
constante = distribution["columns"]["Constante"]

assert constante["mean"] == 5.0
assert constante["median"] == 5.0
assert constante["variance"] == 0.0
assert constante["iqr"] == 0.0

print("\n" + "=" * 70)
print("✅ TOUTES LES VÉRIFICATIONS SONT RÉUSSIES")
print("DistributionAnalyzer : TEST CIBLÉ OK")
print("=" * 70)
