# Registry

**Framework :** EMIDAF v1.0

**Version :** 1.0.0

**Statut :** Stable

---

# Description

Le `Registry` est le registre central du Framework EMIDAF.

Il permet d'enregistrer et de retrouver les composants du Framework à partir d'un identifiant unique.

Le Registry ne contient aucune logique métier.

Il constitue uniquement un conteneur de références.

---

# Responsabilités

Le Registry est responsable des opérations suivantes :

- enregistrer un composant ;
- récupérer un composant ;
- vérifier son existence ;
- supprimer un composant ;
- vider complètement le registre ;
- lister les composants enregistrés ;
- compter les composants.

Il n'a aucune autre responsabilité.

---

# API Publique

## Constructor

```python
Registry()
```

Crée un registre vide.

---

## register

```python
register(name: str, component: object)
```

Ajoute un composant.

Conditions :

- nom obligatoire
- composant obligatoire
- nom unique

---

## get

```python
get(name: str)
```

Retourne le composant.

Retourne `None` si le composant n'existe pas.

---

## exists

```python
exists(name: str)
```

Retourne :

```python
True
```

ou

```python
False
```

---

## unregister

```python
unregister(name: str)
```

Supprime un composant.

Aucune erreur si le composant n'existe pas.

---

## clear

```python
clear()
```

Vide complètement le registre.

---

## list

```python
list()
```

Retourne les noms des composants triés par ordre alphabétique.

---

## count

```python
count()
```

Retourne le nombre de composants enregistrés.

---

# Exemple

```python
registry = Registry()

registry.register("database", DatabaseManager())

registry.register("logger", LoggerManager())

db = registry.get("database")

if registry.exists("logger"):
    print("Logger disponible")
```

---

# Dépendances

Le Registry ne dépend d'aucun composant du Framework.

Il utilise uniquement la bibliothèque standard Python.

---

# Complexité

| Méthode | Complexité |
|----------|------------|
| register | O(1) |
| get | O(1) |
| exists | O(1) |
| unregister | O(1) |
| clear | O(1) |
| count | O(1) |
| list | O(n log n) |

---

# Contraintes

- un nom est unique ;
- un composant est stocké par référence ;
- aucune logique métier ;
- aucune dépendance vers les Managers ;
- aucune dépendance vers le Kernel ;
- aucune dépendance vers Bootstrap.

---

# Cycle de vie

```text
Création

↓

Enregistrement

↓

Consultation

↓

Suppression

↓

Destruction
```

---

# Historique

## Version 1.0.0

- Première implémentation.
- API figée.
- Tests unitaires complets.