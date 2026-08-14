"""
EMIDAF Research Lab
Configuration Manager
Version : 1.0
"""

from pathlib import Path
import json


class ConfigurationManager:
    """
    Gestionnaire central de la configuration d'EMIDAF.

    Responsabilités
    ----------------
    - Charger la configuration.
    - Recharger la configuration.
    - Sauvegarder les modifications.
    - Fournir les paramètres aux autres composants.
    """

    def __init__(self):

        self._config = {}

        self._config_file = (
            Path(__file__).parent.parent.parent
            / "config"
            / "settings.json"
        )

        self.initialize()

    # =====================================================
    # INITIALISATION
    # =====================================================

    def initialize(self):
        """
        Initialise le gestionnaire.
        """

        self.load()

    # =====================================================
    # CHARGEMENT
    # =====================================================

    def load(self):
        """
        Charge le fichier settings.json.
        """

        if not self._config_file.exists():

            raise FileNotFoundError(
                f"Configuration introuvable : {self._config_file}"
            )

        with open(
            self._config_file,
            "r",
            encoding="utf-8"
        ) as file:

            self._config = json.load(file)

    # =====================================================
    # RECHARGEMENT
    # =====================================================

    def reload(self):
        """
        Recharge complètement la configuration.
        """

        self.load()

    # =====================================================
    # ACCES GENERIQUE
    # =====================================================

    def get(self, key, default=None):
        """
        Retourne la valeur associée à une clé.
        """

        return self._config.get(key, default)

    def has(self, key):
        """
        Vérifie si une clé existe.
        """

        return key in self._config

    def keys(self):
        """
        Retourne toutes les clés.
        """

        return list(self._config.keys())

    def values(self):
        """
        Retourne toutes les valeurs.
        """

        return list(self._config.values())

    def items(self):
        """
        Retourne toutes les paires (clé, valeur).
        """

        return list(self._config.items())

    def count(self):
        """
        Retourne le nombre de paramètres.
        """

        return len(self._config)

    # =====================================================
    # MODIFICATION
    # =====================================================

    def set(self, key, value):
        """
        Ajoute ou modifie un paramètre.
        """

        self._config[key] = value

    def remove(self, key):
        """
        Supprime une clé.
        """

        if key in self._config:
            del self._config[key]

    def clear(self):
        """
        Vide complètement la configuration.
        """

        self._config.clear()

    # =====================================================
    # SAUVEGARDE
    # =====================================================

    def save(self):
        """
        Sauvegarde la configuration sur disque.
        """

        with open(
            self._config_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self._config,
                file,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # PROPRIETES
    # =====================================================

    @property
    def application(self):
        return self.get("application")

    @property
    def version(self):
        return self.get("version")

    @property
    def theme(self):
        return self.get("theme")

    @property
    def language(self):
        return self.get("language")

    @property
    def workspace(self):
        return self.get("workspace")

    @property
    def database(self):
        return self.get("database")

    @property
    def debug(self):
        return self.get("debug")

    @property
    def autosave(self):
        return self.get("autosave")

    @property
    def log_level(self):
        return self.get("log_level")