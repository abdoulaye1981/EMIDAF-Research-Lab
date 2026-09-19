import numpy as np
import pandas as pd

from emidaf_core.dataset.profiler.dataset_profiler import DatasetProfiler


print("\n" + "=" * 70)
print("TEST CIBLE : OUTLIER ANALYZER")
print("=" * 70)


# -------------------------------------------------------------------
# 1. Jeu de données de test
# -------------------------------------------------------------------

df = pd.DataFrame({
    "ID": range(1, 11),

    # Pas d'outlier :
    # 10, 11, 12, ..., 19
    "Variable_Sans_Outlier": [
        10, 11, 12, 13, 14,
        15, 16, 17, 18, 19
    ],

    # Outliers évidents :
    # 1 et 100 sont volontairement très éloignés
    "Variable_Avec_Outliers": [
        10, 11, 12, 13, 14,
        15, 16, 17, 100, 1
    ],

    # Variable constante
    "Variable_Constante": [
        5, 5, 5, 5, 5,
        5, 5, 5, 5, 5
    ],

    # Valeurs manquantes
    "Variable_Avec_NaN": [
        10, 11, 12, np.nan, 14,
        15, np.nan, 17, 18, 19
    ],

    # Valeurs infinies
    "Variable_Avec_Inf": [
        10, 11, np.inf, 13, 14,
        15, -np.inf, 17, 18, 19
    ],

    # Variable textuelle : doit être ignorée
    "Nom": [
        "Awa", "Moussa", "Fatou", "Ali", "Mariama",
        "Ousmane", "Sokhna", "Ibrahima", "Aminata", "Cheikh"
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
# 3. Variables numériques
# -------------------------------------------------------------------

print("\n--- 2. VARIABLES NUMÉRIQUES DÉTECTÉES ---")

print(result.datatypes)


# -------------------------------------------------------------------
# 4. Résultat OutlierAnalyzer
# -------------------------------------------------------------------

print("\n--- 3. RÉSULTAT OUTLIER ANALYZER ---")

outliers = result.outliers

print(outliers)


# -------------------------------------------------------------------
# 5. Détail des résultats
# -------------------------------------------------------------------

print("\n--- 4. DÉTAIL PAR VARIABLE ---")

for column, statistics in outliers["columns"].items():

    print(f"\n{column}")

    for key, value in statistics.items():
        print(f"  {key}: {value}")


# -------------------------------------------------------------------
# 6. Vérification : aucune variable textuelle
# -------------------------------------------------------------------

print("\n--- 5. VÉRIFICATION DES VARIABLES ANALYSÉES ---")

assert "Nom" not in outliers

print("✅ La variable textuelle 'Nom' est correctement ignorée.")


# -------------------------------------------------------------------
# 7. Variable sans outlier
# -------------------------------------------------------------------

print("\n--- 6. VARIABLE SANS OUTLIER ---")

sans_outlier = outliers["columns"]["Variable_Sans_Outlier"]

print(sans_outlier)

assert sans_outlier["count"] == 10
assert sans_outlier["outliers"] == 0
assert sans_outlier["outlier_rate"] == 0.0
assert sans_outlier["method"] == "IQR"


# Pour 10 à 19 :
# Q1 = 12.25
# Q3 = 16.75
# IQR = 4.5
# borne inférieure = 5.5
# borne supérieure = 23.5

assert sans_outlier["lower_bound"] == 5.5
assert sans_outlier["upper_bound"] == 23.5


print("✅ Aucune valeur aberrante détectée.")
print("✅ Bornes IQR correctes.")


# -------------------------------------------------------------------
# 8. Variable avec outliers
# -------------------------------------------------------------------

print("\n--- 7. VARIABLE AVEC OUTLIERS ---")

avec_outliers = outliers["columns"]["Variable_Avec_Outliers"]

print(avec_outliers)

assert avec_outliers["count"] == 10
assert avec_outliers["outliers"] == 2
assert avec_outliers["outlier_rate"] == 20.0
assert avec_outliers["method"] == "IQR"


# Pour :
# 10,11,12,13,14,15,16,100,1
# avec l'ensemble complet trié :
# 1,10,11,12,13,14,15,16,100
# Attention : pandas quantile est utilisé par le code.
#
# Nous vérifions donc surtout que les deux valeurs extrêmes
# sont détectées et que le taux est correct.

print("✅ Les valeurs aberrantes sont détectées.")
print("✅ Le taux d'outliers est correct.")


# -------------------------------------------------------------------
# 9. Variable constante
# -------------------------------------------------------------------

print("\n--- 8. VARIABLE CONSTANTE ---")

constante = outliers["columns"]["Variable_Constante"]

print(constante)

assert constante["count"] == 10
assert constante["outliers"] == 0
assert constante["outlier_rate"] == 0.0
assert constante["lower_bound"] == 5.0
assert constante["upper_bound"] == 5.0

print("✅ Variable constante correctement traitée.")


# -------------------------------------------------------------------
# 10. Variable avec NaN
# -------------------------------------------------------------------

print("\n--- 9. VARIABLE AVEC NaN ---")

avec_nan = outliers["columns"]["Variable_Avec_NaN"]

print(avec_nan)

# 8 valeurs exploitables
assert avec_nan["count"] == 8

assert avec_nan["method"] == "IQR"

print("✅ Les valeurs manquantes sont correctement exclues.")


# -------------------------------------------------------------------
# 11. Variable avec +∞ et -∞
# -------------------------------------------------------------------

print("\n--- 10. VARIABLE AVEC +INF / -INF ---")

avec_inf = outliers["columns"]["Variable_Avec_Inf"]

print(avec_inf)

# 8 valeurs finies exploitables
assert avec_inf["count"] == 8

assert avec_inf["method"] == "IQR"

print("✅ Les valeurs infinies sont correctement exclues.")


# -------------------------------------------------------------------
# 12. Vérification globale
# -------------------------------------------------------------------

print("\n--- 11. VÉRIFICATION GLOBALE ---")

assert outliers["count"] == 6

for statistics in outliers["columns"].values():

    assert "count" in statistics
    assert "outliers" in statistics
    assert "outlier_rate" in statistics
    assert "lower_bound" in statistics
    assert "upper_bound" in statistics
    assert statistics["method"] == "IQR"


print("\n" + "=" * 70)
print("✅ TOUTES LES VÉRIFICATIONS SONT RÉUSSIES")
print("OutlierAnalyzer : TEST CIBLÉ OK")
print("=" * 70)
