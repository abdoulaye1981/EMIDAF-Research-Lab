# EMIDAF Research Lab

**EMIDAF — Educational Multimodal Intelligent Data Analysis Framework**  
Version de référence : **v1.1.0**

EMIDAF Research Lab est un framework scientifique modulaire dédié à l’analyse de données éducatives, à la détection et au diagnostic des difficultés d’apprentissage, à l’explicabilité des modèles, à l’aide à la décision et à la validation humaine.

Le framework est conçu pour séparer clairement :

- la production des résultats scientifiques ;
- leur interprétation ;
- leur explicabilité ;
- l’aide à la décision ;
- la validation par l’enseignant ;
- la restitution et l’assistance rédactionnelle.

---

## 1. Objectif scientifique

EMIDAF vise à fournir un environnement intégré permettant d’exploiter des données éducatives structurées, qualitatives et textuelles pour soutenir l’analyse des difficultés d’apprentissage.

Le principe méthodologique central est le suivant :

> **EMIDAF produit les résultats scientifiques ; les couches d’assistance les expliquent et les rédigent sans les recalculer, les modifier ni les inventer.**

Le framework privilégie :

- la traçabilité ;
- la reproductibilité ;
- l’explicabilité ;
- la validation humaine ;
- la distinction entre association, prédiction et causalité ;
- la séparation entre décision algorithmique et jugement pédagogique.

---

## 2. Pipeline principal

```text
Inspection
   ↓
EIDPP
   ↓
ELAE
   ↓
EKDE
   ↓
EAIE
   ↓
EXAIE
   ↓
EDSE
   ↓
EMIX
   ↓
Reporting
```

Des modules complémentaires peuvent intervenir selon les données disponibles :

```text
ETAE → analyse textuelle
EQAE → analyse qualitative
```

---

## 3. Architecture fonctionnelle

### Inspection
Analyse initiale du jeu de données :

- dimensions ;
- types de variables ;
- valeurs manquantes ;
- doublons ;
- distributions ;
- anomalies de structure.

### EIDPP
Préparation et prétraitement des données.

### ELAE — EMIDAF Learning Analytics Engine
Analyses descriptives, exploratoires et statistiques :

- statistiques descriptives ;
- distributions ;
- comparaisons ;
- tests statistiques ;
- tailles d’effet ;
- relations entre variables.

### EKDE — EMIDAF Knowledge Discovery Engine
Découverte de structures et de profils :

- clustering ;
- segmentation ;
- sélection de caractéristiques ;
- profils de groupes ;
- mesures de qualité des partitions.

### EAIE — EMIDAF Artificial Intelligence Engine
Modélisation supervisée :

- régression ;
- classification ;
- Random Forest ;
- Gradient Boosting ;
- XGBoost ;
- SVM ;
- KNN ;
- modèles multiniveaux selon le contexte.

### EXAIE — EMIDAF Explainable Artificial Intelligence Engine
Explicabilité des modèles :

- importance des variables ;
- contributions locales ;
- permutation importance ;
- SHAP lorsque disponible ;
- analyse des erreurs de classification ;
- traçabilité des observations expliquées.

### EDSE — EMIDAF Decision Support Engine
Aide à la décision éducative :

- scénarios ;
- profils ;
- détection ;
- éléments de diagnostic éducatif ;
- seuils de décision ;
- traçabilité EAIE → EDSE ;
- validation enseignant ;
- mesure de l’accord humain–machine.

### EMIX — EMIDAF Multi-Intelligence eXchange
Intégration des résultats :

- rapprochement de sources analytiques ;
- convergence ;
- complémentarité ;
- divergence ;
- joint displays ;
- méta-inférences validées par le chercheur.

### ETAE — EMIDAF Text Analysis Engine
Analyse textuelle computationnelle lorsque des variables textuelles sont disponibles.

### EQAE — EMIDAF Qualitative Analysis Engine
Analyse qualitative assistée :

- corpus ;
- codebook ;
- codage ;
- thèmes ;
- verbatims ;
- cooccurrences ;
- mémos ;
- validation du chercheur.

---

## 4. Validation enseignant

EMIDAF v1.1.0 intègre une couche de validation humaine indépendante.

La validation enseignant permet notamment de conserver :

- l’identifiant de l’observation ;
- l’identifiant de l’élève lorsque disponible ;
- la prédiction algorithmique ;
- la probabilité prédite ;
- le jugement indépendant de l’enseignant ;
- la validation de la détection ;
- la validation du diagnostic ;
- le niveau de difficulté ;
- les facteurs relevés par l’enseignant ;
- les commentaires pédagogiques.

Le jugement humain n’écrase jamais le résultat algorithmique.

L’accord humain–machine peut être étudié à travers :

- taux d’accord ;
- matrice de confusion ;
- coefficient κ de Cohen lorsque les conditions sont réunies.

> Le κ de Cohen est utilisé pour mesurer l’accord sur la détection binaire. Il ne constitue ni une preuve de causalité ni une validation automatique du diagnostic éducatif.

---

## 5. Assistant contextuel EMIDAF

La version v1.1.0 introduit un assistant contextuel basé sur un provider IA externe configurable.

Son rôle est de :

- décrire les résultats ;
- fournir des observations ;
- expliquer les métriques ;
- interpréter les résultats ;
- synthétiser plusieurs modules ;
- produire des conclusions prudentes ;
- expliciter les limites ;
- adapter le niveau d’explication à l’utilisateur.

Trois niveaux d’explication sont prévus :

- débutant ;
- intermédiaire ;
- expert.

### Règles scientifiques de l’assistant

L’assistant :

- ne recalcule aucune statistique ;
- ne produit aucune nouvelle métrique ;
- n’invente aucune valeur ;
- ne modifie aucune prédiction ;
- ne modifie aucun seuil ;
- ne remplace pas la validation enseignant ;
- ne transforme pas une association en causalité ;
- ne transforme pas une importance prédictive en cause ;
- ne transforme pas une prédiction en certitude ;
- reste strictement dans le contexte EMIDAF fourni.

Si une information n’est pas disponible, il doit le signaler explicitement.

---

## 6. Report Writer enrichi

EMIDAF conserve deux niveaux de reporting.

### Rapport scientifique EMIDAF
Produit à partir des résultats persistés dans le pipeline.

Il constitue la **source scientifique de référence**.

### Rapport enrichi assisté
Produit à partir du rapport EMIDAF déjà généré et des résultats structurés disponibles.

Il peut développer :

- observations ;
- interprétations ;
- transitions ;
- synthèses ;
- conclusions ;
- limites méthodologiques ;
- recommandations prudentes ;
- implications pédagogiques.

Le rapport enrichi :

- ne remplace jamais le rapport scientifique ;
- ne recalcule pas les résultats ;
- ne doit pas créer de résultats absents ;
- conserve les valeurs scientifiques d’origine.

Les modes de restitution prévus sont :

- scientifique ;
- pédagogique ;
- technique ;
- exécutif ;
- complet.

---

## 7. Intégration Gemini

L’intégration Gemini repose sur le SDK `google-genai`.

La clé API doit être fournie par variable d’environnement :

```bash
export GEMINI_API_KEY="VOTRE_CLE"
```

Le modèle peut également être configuré par variable d’environnement :

```bash
export GEMINI_MODEL="MODELE_GEMINI"
```

L’absence de clé ou l’indisponibilité du service externe ne doit pas empêcher EMIDAF de fonctionner.

Les composants principaux sont :

```text
emidaf_core/assistant/
├── provider.py
├── gemini_provider.py
├── fake_provider.py
├── context_builder.py
├── report_context_builder.py
├── assistant_service.py
├── report_writer.py
├── consistency_checker.py
└── prompts.py
```

Le `FakeProvider` permet de tester l’architecture sans appel réseau.

---

## 8. Confidentialité et contrôle du contexte

Le `ContextBuilder` filtre les objets qui ne doivent pas être transmis au provider externe, notamment :

- estimateurs ;
- pipelines ;
- matrices d’entraînement et de test ;
- jeux de données bruts ;
- prédictions individuelles volumineuses ;
- identifiants d’observations ;
- identifiants d’élèves ;
- verbatims et contenus qualitatifs sensibles lorsque filtrés.

L’objectif est de transmettre uniquement le contexte nécessaire à l’explication des résultats.

---

## 9. Structure du projet

```text
EMIDAF_Research_Lab/
├── database/
│   └── models/
├── emidaf_core/
│   ├── assistant/
│   ├── controllers/
│   ├── edse/
│   ├── managers/
│   ├── repositories/
│   ├── services/
│   └── ...
├── emidaf_studio/
│   ├── pages/
│   │   ├── eaie/
│   │   ├── exaie/
│   │   ├── edse/
│   │   └── reports/
│   └── ...
├── tests/
├── workspace/
└── main.py
```

---

## 10. Environnement de développement

La version actuelle a été développée et testée principalement avec :

- macOS ;
- Python 3.12 ;
- environnement Anaconda ;
- pandas ;
- NumPy ;
- scikit-learn ;
- SciPy ;
- statsmodels ;
- XGBoost ;
- SHAP ;
- Dash ;
- Plotly ;
- `google-genai`.

---

## 11. Lancement

Depuis la racine du projet :

```bash
python main.py
```

ou selon la configuration de Studio :

```bash
python -m emidaf_studio.app
```

La commande exacte peut dépendre de la configuration locale du projet.

---

## 12. Tests

La version v1.1.0 a été validée avec :

```text
1849 passed
306 warnings
```

Exécution :

```bash
pytest -q
```

Contrôle de propreté Git :

```bash
git diff --check
```

Les warnings restants sont principalement issus de bibliothèques scientifiques et de cas limites connus. Ils ne bloquent pas la validation actuelle de la suite de tests.

---

## 13. Versioning

### v1.0.0
Premier jalon stable EMIDAF avec les modules scientifiques principaux, authentification, ownership et sécurité de production.

### v1.1.0
Ajouts principaux :

- validation enseignant ;
- traçabilité renforcée ;
- mesure de l’accord humain–machine ;
- Assistant contextuel EMIDAF ;
- intégration Gemini configurable ;
- Report Writer enrichi ;
- séparation stricte entre rapport scientifique et rapport assisté ;
- filtres de contexte pour les appels IA externes.

---

## 14. Principes scientifiques

EMIDAF applique les principes suivants :

1. aucun résultat scientifique ne doit être inventé ;
2. les calculs sont produits par les moteurs scientifiques ;
3. l’explicabilité est séparée de la prédiction ;
4. l’aide à la décision est séparée de la validation humaine ;
5. une association ne constitue pas une causalité ;
6. une importance prédictive ne constitue pas une cause ;
7. une prédiction ne constitue pas une certitude ;
8. le diagnostic EMIDAF est un diagnostic éducatif et non médical ou clinique ;
9. le chercheur ou l’enseignant reste responsable de l’interprétation finale ;
10. la traçabilité doit permettre de relier chaque restitution aux résultats sources.

---

## 15. Positionnement de la version v1.1.0

EMIDAF v1.1.0 est considéré comme un **feature freeze fonctionnel**.

Les travaux suivants doivent prioritairement porter sur :

- stabilisation ;
- documentation ;
- packaging ;
- démonstration ;
- validation scientifique ;
- tests sur plusieurs jeux de données ;
- amélioration de l’ergonomie ;
- préparation des publications scientifiques ;
- reproductibilité des expériences.

Les nouvelles fonctionnalités majeures devront être planifiées pour une version ultérieure.

---

## 16. Dépôt

GitHub :

```text
https://github.com/abdoulaye1981/EMIDAF-Research-Lab
```

Version de référence :

```text
v1.1.0
```

---

## 17. Auteur

**Abdoulaye Wakhab DIOP**  
Enseignant-chercheur  
Sciences des données, intelligence artificielle, statistiques et mathématiques appliquées

---

## Citation

Une référence bibliographique formelle pourra être ajoutée après la stabilisation de la publication scientifique associée au framework.
