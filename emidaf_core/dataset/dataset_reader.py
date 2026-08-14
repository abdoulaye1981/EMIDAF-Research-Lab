"""
=========================================================
EMIDAF Framework v1.0
Dataset Reader
---------------------------------------------------------
Lecture des jeux de données.
=========================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class DatasetReader:
    """
    Lecture des datasets.

    Retourne toujours un DataFrame.
    """

    def read(
        self,
        file: Path,
        **kwargs
    ) -> pd.DataFrame:

        extension = file.suffix.lower()

        if extension == ".csv":
            return self._read_csv(file, **kwargs)

        elif extension in [".xlsx", ".xls"]:
            return self._read_excel(file, **kwargs)

        elif extension == ".json":
            return self._read_json(file)

        elif extension == ".parquet":
            return self._read_parquet(file)

        elif extension == ".feather":
            return self._read_feather(file)

        elif extension == ".pickle":
            return self._read_pickle(file)

        elif extension == ".xml":
            return self._read_xml(file)

        elif extension == ".txt":
            return self._read_txt(file, **kwargs)

        else:

            raise ValueError(
                f"Unsupported format : {extension}"
            )

    # =====================================================
    # CSV
    # =====================================================

    def _read_csv(self, file, **kwargs):

        return pd.read_csv(file, **kwargs)

    # =====================================================
    # EXCEL
    # =====================================================

    def _read_excel(self, file, **kwargs):

        return pd.read_excel(file, **kwargs)

    # =====================================================
    # JSON
    # =====================================================

    def _read_json(self, file):

        return pd.read_json(file)

    # =====================================================
    # PARQUET
    # =====================================================

    def _read_parquet(self, file):

        return pd.read_parquet(file)

    # =====================================================
    # FEATHER
    # =====================================================

    def _read_feather(self, file):

        return pd.read_feather(file)

    # =====================================================
    # PICKLE
    # =====================================================

    def _read_pickle(self, file):

        return pd.read_pickle(file)

    # =====================================================
    # XML
    # =====================================================

    def _read_xml(self, file):

        return pd.read_xml(file)

    # =====================================================
    # TXT
    # =====================================================

    def _read_txt(self, file, **kwargs):

        return pd.read_csv(file, **kwargs)