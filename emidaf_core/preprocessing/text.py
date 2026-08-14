"""
=========================================================
EMIDAF Framework
Text Processing Engine
=========================================================

Auteur : Abdoulaye Wakhab DIOP
Version : 1.0.0

Traitement automatique des données textuelles.

=========================================================
"""

from __future__ import annotations

from abc import ABC

import re
import string
import unicodedata

import pandas as pd

from .base import BasePreprocessor

# ==========================================================
# BASE
# ==========================================================

class BaseTextProcessor(

    BasePreprocessor

):

    """
    Classe mère.
    """

    name = "Base Text Processor"

# ==========================================================
# UNICODE
# ==========================================================

class UnicodeNormalizer(

    BaseTextProcessor

):

    name = "Unicode"

    def fit(self, X, y=None):

        self.fitted = True

        return self

    def transform(self, X):

        X = X.copy()

        for column in X.columns:

            X[column] = X[column].astype(str).apply(

                lambda text:

                unicodedata.normalize(

                    "NFKC",

                    text

                )

            )

        return X

# ==========================================================
# LOWER
# ==========================================================

class LowerCase(

    BaseTextProcessor

):

    name = "Lower"

    def fit(self, X, y=None):

        self.fitted=True

        return self

    def transform(self,X):

        X=X.copy()

        for column in X.columns:

            X[column]=(

                X[column]

                .astype(str)

                .str.lower()

            )

        return X

# ==========================================================
# PUNCTUATION
# ==========================================================

class RemovePunctuation(

    BaseTextProcessor

):

    name="Punctuation"

    def fit(self,X,y=None):

        self.fitted=True

        return self

    def transform(self,X):

        X=X.copy()

        table=str.maketrans(

            "",

            "",

            string.punctuation

        )

        for column in X.columns:

            X[column]=X[column].apply(

                lambda x:

                str(x).translate(table)

            )

        return X

# ==========================================================
# NUMBERS
# ==========================================================

class RemoveNumbers(

    BaseTextProcessor

):

    name="Numbers"

    def fit(self,X,y=None):

        self.fitted=True

        return self

    def transform(self,X):

        X=X.copy()

        for column in X.columns:

            X[column]=X[column].replace(

                r"\d+",

                "",

                regex=True

            )

        return X

# ==========================================================
# MULTIPLE SPACES
# ==========================================================

class RemoveExtraSpaces(

    BaseTextProcessor

):

    name="Spaces"

    def fit(self,X,y=None):

        self.fitted=True

        return self

    def transform(self,X):

        X=X.copy()

        for column in X.columns:

            X[column]=X[column].replace(

                r"\s+",

                " ",

                regex=True

            ).str.strip()

        return X

# ==========================================================
# TOKENIZER
# ==========================================================

class Tokenizer(

    BaseTextProcessor

):

    name="Tokenizer"

    def fit(self,X,y=None):

        self.fitted=True

        return self

    def transform(self,X):

        X=X.copy()

        for column in X.columns:

            X[column]=(

                X[column]

                .str.split()

            )

        return X

# ==========================================================
# TEXT LENGTH
# ==========================================================

class TextLength(

    BaseTextProcessor

):

    name="Length"

    def fit(self,X,y=None):

        self.fitted=True

        return self

    def transform(self,X):

        result=pd.DataFrame(index=X.index)

        for column in X.columns:

            result[column+"_characters"]=X[column].str.len()

            result[column+"_words"]=X[column].str.split().str.len()

        return result
    
# ==========================================================
# CLEAN TEXT
# ==========================================================

class CleanText(

    BaseTextProcessor

):

    """
    Pipeline automatique.
    """

    def fit(self,X,y=None):

        self.fitted=True

        return self

    def transform(self,X):

        pipeline=[

            UnicodeNormalizer(),

            LowerCase(),

            RemovePunctuation(),

            RemoveNumbers(),

            RemoveExtraSpaces()

        ]

        data=X.copy()

        for step in pipeline:

            data=step.fit_transform(data)

        return data
    
# ==========================================================
# LANGUAGE
# ==========================================================

class LanguageDetector(

    BaseTextProcessor

):

    """
    Version 2.0
    """

    name="Language"

    def fit(self,X,y=None):

        raise NotImplementedError(

            "Disponible dans EMIDAF NLP."

        )

# ==========================================================
# LEMMATIZATION
# ==========================================================

class Lemmatizer(

    BaseTextProcessor

):

    """
    Wrapper spaCy.

    Version future.
    """

    name="Lemma"

    def fit(self,X,y=None):

        raise NotImplementedError()

# ==========================================================
# STEMMING
# ==========================================================

class Stemmer(

    BaseTextProcessor

):

    name="Stemmer"

    def fit(self,X,y=None):

        raise NotImplementedError()

# ==========================================================
# TF IDF
# ==========================================================

from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFVectorizer(

    BaseTextProcessor

):

    name="TF-IDF"

    def __init__(

        self,

        max_features=5000

    ):

        self.model=TfidfVectorizer(

            max_features=max_features

        )

    def fit(self,X,y=None):

        self.model.fit(

            X.iloc[:,0]

        )

        self.fitted=True

        return self

    def transform(self,X):

        matrix=self.model.transform(

            X.iloc[:,0]

        )

        return pd.DataFrame(

            matrix.toarray(),

            columns=self.model.get_feature_names_out()

        )

# ==========================================================
# SERVICE
# ==========================================================

class Text:

    registry={

        "unicode":UnicodeNormalizer,

        "lower":LowerCase,

        "punctuation":RemovePunctuation,

        "numbers":RemoveNumbers,

        "spaces":RemoveExtraSpaces,

        "tokenizer":Tokenizer,

        "length":TextLength,

        "clean":CleanText,

        "language":LanguageDetector,

        "lemma":Lemmatizer,

        "stem":Stemmer,

        "tfidf":TFIDFVectorizer

    }

    @classmethod
    def get(

        cls,

        method,

        **kwargs

    ):

        return cls.registry[method](

            **kwargs

        )