import numpy as np
import pandas as pd

from emidaf_core.dataset.profiler.dataset_profiler import DatasetProfiler


print("\n" + "=" * 70)
print("TEST CIBLE : MULTICOLLINEARITY ANALYZER")
print("=" * 70)


# ============================================================
# 1. DONNÉES DE TEST
# ============================================================

df = pd.DataFrame({
    # Identifiant
    "ID": range(1, 11),

    # Variable de référence
    "X1": [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10
    ],

    # Très fortement corrélée à X1
    "X2": [
        2.1, 3.9, 6.2, 7.8, 10.1,
        12.2, 13.8, 16.1, 18.2, 19.9
    ],

    # Combinaison linéaire parfaite de X1
    "X3": [
        3, 6, 9, 12, 15,
        18, 21, 24, 27, 30
    ],

    # Variable avec NaN
    "X4": [
        5, 7, np.nan, 11, 13,
        15, np.nan, 19, 21, 23
    ],

    # Variable avec +INF / -INF
    "X5": [
        10, 12, np.inf, 16, 18,
        20, -np.inf, 24, 26, 28
    ],

    # Variable constante
    "Constante": [
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

print("\n--- 2. RÉSULTAT MULTICOLLINEARITY ANALYZER ---")

result = profile.multicollinearity

print(result)


# ============================================================
# 4. VARIABLES ANALYSÉES
# ============================================================

print("\n--- 3. VARIABLES ANALYSÉES ---")

print(result["columns"])

assert "Nom" not in result["columns"]

print("✓ Variable textuelle 'Nom' ignorée.")


# ============================================================
# 5. MATRICE DE CORRÉLATION
# ============================================================

print("\n--- 4. MATRICE DE CORRÉLATION ---")

print(result["correlation_matrix"])

matrix = result["correlation_matrix"]


# X1 / X3 : corrélation parfaite
assert matrix["X1"]["X3"] == 1.0

print("✓ X1 / X3 : corrélation parfaite détectée.")


# X1 / X2 : forte corrélation
assert abs(matrix["X1"]["X2"]) >= 0.8

print("✓ X1 / X2 : forte corrélation détectée.")


# ============================================================
# 6. FORTES CORRÉLATIONS
# ============================================================

print("\n--- 5. FORTES CORRÉLATIONS ---")

high_correlations = result["high_correlations"]

for pair in high_correlations:
    print(pair)


assert len(high_correlations) > 0

print("✓ Des fortes corrélations sont détectées.")


# Vérification de la structure
for pair in high_correlations:

    assert "variable_1" in pair
    assert "variable_2" in pair
    assert "correlation" in pair

    assert abs(pair["correlation"]) >= 0.8

print("✓ Structure des fortes corrélations correcte.")


# ============================================================
# 7. VIF
# ============================================================

print("\n--- 6. VIF ---")

vif = result["vif"]

for column, value in vif.items():
    print(f"{column} : {value}")


# X1 et X3 sont dans une relation
# de dépendance linéaire parfaite.
assert np.isinf(vif["X1"])

assert np.isinf(vif["X3"])

print("✓ VIF infini correctement détecté pour X1 et X3.")


# ============================================================
# 8. INTERPRÉTATION DU VIF
# ============================================================

print("\n--- 7. INTERPRÉTATION DU VIF ---")

interpretation = result["vif_interpretation"]

for column, value in interpretation.items():
    print(f"{column} : {value}")


assert (
    interpretation["X1"]
    == "Multicolinéarité parfaite"
)

assert (
    interpretation["X3"]
    == "Multicolinéarité parfaite"
)

print("✓ Interprétation du VIF correcte.")


# ============================================================
# 9. DÉTECTION GLOBALE
# ============================================================

print("\n--- 8. DÉTECTION GLOBALE ---")

print(
    "Multicolinéarité détectée :",
    result["multicollinearity_detected"]
)

assert result["multicollinearity_detected"] is True

print("✓ Multicolinéarité correctement détectée.")


# ============================================================
# 10. WARNINGS
# ============================================================

print("\n--- 9. WARNINGS ---")

for warning in result["warnings"]:
    print("⚠", warning)


assert len(result["warnings"]) > 0

print("✓ Warnings générés.")


# ============================================================
# 11. RECOMMANDATIONS
# ============================================================

print("\n--- 10. RECOMMANDATIONS ---")

for recommendation in result["recommendations"]:
    print("→", recommendation)


assert len(result["recommendations"]) > 0

print("✓ Recommandations générées.")


# ============================================================
# 12. NaN ET INF
# ============================================================

print("\n--- 11. GESTION NaN / INF ---")

assert "X4" in result["columns"]
assert "X5" in result["columns"]

print("✓ Variables contenant NaN et INF analysées.")


# Vérification : aucune corrélation infinie
for column_1, values in matrix.items():

    for column_2, value in values.items():

        if value is not None:
            assert not np.isinf(value)

print("✓ Aucun INF ne contamine la matrice.")


# ============================================================
# 13. VARIABLE CONSTANTE
# ============================================================

print("\n--- 12. VARIABLE CONSTANTE ---")

assert "Constante" in result["columns"]

print("✓ Variable constante présente dans l'analyse.")


# ============================================================
# 14. STATUS
# ============================================================

print("\n--- 13. STATUS ---")

print("Status :", result["status"])

assert result["status"] == "success"

print("✓ Status correct.")


# ============================================================
# 15. RESULTAT FINAL
# ============================================================

print("\n" + "=" * 70)
print("✅ TOUTES LES VÉRIFICATIONS SONT RÉUSSIES")
print("MulticollinearityAnalyzer : TEST CIBLÉ OK")
print("=" * 70)
