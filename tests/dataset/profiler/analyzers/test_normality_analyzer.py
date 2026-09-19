import numpy as np
import pandas as pd

from emidaf_core.dataset.profiler.dataset_profiler import DatasetProfiler


print("\n" + "=" * 70)
print("TEST CIBLE : NORMALITY ANALYZER")
print("=" * 70)


# -------------------------------------------------------------------
# 1. Jeu de données
# -------------------------------------------------------------------

df = pd.DataFrame({
    "ID": range(1, 21),

    # Distribution approximativement normale
    "Variable_Normale": [
        49.2, 51.1, 48.7, 50.5, 52.0,
        47.9, 50.1, 49.8, 51.5, 48.9,
        50.7, 52.2, 47.5, 49.6, 51.0,
        48.4, 50.3, 49.1, 51.8, 50.0
    ],

    # Distribution clairement non normale
    "Variable_Non_Normale": [
        1, 1, 1, 2, 2,
        2, 3, 3, 3, 4,
        10, 20, 30, 50, 80,
        100, 150, 200, 300, 500
    ],

    # Variable constante
    "Variable_Constante": [
        5, 5, 5, 5, 5,
        5, 5, 5, 5, 5,
        5, 5, 5, 5, 5,
        5, 5, 5, 5, 5
    ],

    # Variable avec valeurs manquantes et infinies
    "Variable_Problematique": [
        10, 12, 11, np.nan, 13,
        14, np.inf, 15, 16, -np.inf,
        17, 18, np.nan, 19, 20,
        21, 22, 23, np.nan, 24
    ],

    # Variable avec trop peu d'observations exploitables
    "Variable_Peu_Observations": [
        10, 12, np.nan, np.nan, np.nan,
        np.nan, np.nan, np.nan, np.nan, np.nan,
        np.nan, np.nan, np.nan, np.nan, np.nan,
        np.nan, np.nan, np.nan, np.nan, np.nan
    ],

    # Variable textuelle : doit être ignorée
    "Nom": [
        "Awa", "Moussa", "Fatou", "Ali", "Mariama",
        "Ousmane", "Sokhna", "Ibrahima", "Aminata", "Cheikh",
        "Mamadou", "Astou", "Abdou", "Khady", "Pape",
        "Ndeye", "Modou", "Rama", "Lamine", "Coumba"
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
# 3. Vérification des types
# -------------------------------------------------------------------

print("\n--- 2. VARIABLES NUMÉRIQUES DÉTECTÉES ---")

print(result.datatypes)


# -------------------------------------------------------------------
# 4. Résultat du test de normalité
# -------------------------------------------------------------------

print("\n--- 3. RÉSULTAT NORMALITY ANALYZER ---")

normality = result.normality

print(normality)


# -------------------------------------------------------------------
# 5. Nombre de variables analysées
# -------------------------------------------------------------------

print("\n--- 4. NOMBRE DE VARIABLES ANALYSÉES ---")

print("count =", normality["count"])


# -------------------------------------------------------------------
# 6. Détail par variable
# -------------------------------------------------------------------

print("\n--- 5. DÉTAIL DES TESTS ---")

for column, statistics in normality["columns"].items():

    print(f"\n{column}")

    for key, value in statistics.items():
        print(f"  {key}: {value}")


# -------------------------------------------------------------------
# 7. Vérifications structurelles
# -------------------------------------------------------------------

print("\n--- 6. VÉRIFICATIONS STRUCTURELLES ---")

assert "Variable_Normale" in normality["columns"]
assert "Variable_Non_Normale" in normality["columns"]
assert "Variable_Constante" in normality["columns"]
assert "Variable_Problematique" in normality["columns"]
assert "Variable_Peu_Observations" in normality["columns"]

# La variable textuelle ne doit pas être analysée
assert "Nom" not in normality["columns"]


# -------------------------------------------------------------------
# 8. Vérification Variable_Normale
# -------------------------------------------------------------------

normale = normality["columns"]["Variable_Normale"]

assert normale["n"] == 20
assert normale["statistic"] is not None
assert normale["p_value"] is not None
assert normale["normal"] is True
assert normale["p_value"] > 0.05


# -------------------------------------------------------------------
# 9. Vérification Variable_Non_Normale
# -------------------------------------------------------------------

non_normale = normality["columns"]["Variable_Non_Normale"]

assert non_normale["n"] == 20
assert non_normale["statistic"] is not None
assert non_normale["p_value"] is not None
assert non_normale["normal"] is False
assert non_normale["p_value"] <= 0.05


# -------------------------------------------------------------------
# 10. Vérification Variable_Constante
# -------------------------------------------------------------------

constante = normality["columns"]["Variable_Constante"]

assert constante["n"] == 20
assert constante["statistic"] is None
assert constante["p_value"] is None
assert constante["normal"] is None
assert "constante" in constante["interpretation"].lower()


# -------------------------------------------------------------------
# 11. Vérification Variable_Problematique
# -------------------------------------------------------------------

problematique = normality["columns"]["Variable_Problematique"]

# 24 valeurs au total :
# 3 NaN + 2 infinis = 19 valeurs exploitables
assert problematique["n"] == 15

assert problematique["statistic"] is not None
assert problematique["p_value"] is not None
assert problematique["normal"] in [True, False]


# -------------------------------------------------------------------
# 12. Vérification Variable_Peu_Observations
# -------------------------------------------------------------------

peu = normality["columns"]["Variable_Peu_Observations"]

assert peu["n"] == 2
assert peu["statistic"] is None
assert peu["p_value"] is None
assert peu["normal"] is None

assert "au moins 3" in peu["interpretation"].lower()


# -------------------------------------------------------------------
# 13. Vérification du test
# -------------------------------------------------------------------

assert normality["test"] == "Shapiro-Wilk"
assert normality["alpha"] == 0.05


print("\n" + "=" * 70)
print("✅ TOUTES LES VÉRIFICATIONS SONT RÉUSSIES")
print("NormalityAnalyzer : TEST CIBLÉ OK")
print("=" * 70)
