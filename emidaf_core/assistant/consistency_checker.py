from __future__ import annotations

import json
import re
from typing import Any


class ConsistencyChecker:

    NUMBER_PATTERN = re.compile(
        r"(?<![A-Za-z])"
        r"-?\d+(?:[.,]\d+)?"
        r"(?:[eE][+-]?\d+)?"
        r"%?"
    )

    @classmethod
    def check(
        cls,
        generated_text: str,
        source_context: dict[str, Any],
    ) -> dict[str, Any]:

        source_text = json.dumps(
            source_context,
            ensure_ascii=False,
            default=str,
        )

        generated_numbers = set(
            cls.NUMBER_PATTERN.findall(
                generated_text
            )
        )

        source_numbers = set(
            cls.NUMBER_PATTERN.findall(
                source_text
            )
        )

        suspicious = sorted(
            number
            for number in generated_numbers
            if (
                number not in source_numbers
                and cls._is_material_number(number)
            )
        )

        return {
            "valid": not suspicious,
            "suspicious_numbers": suspicious,
            "generated_numbers_count": len(
                generated_numbers
            ),
            "source_numbers_count": len(
                source_numbers
            ),
        }

    @staticmethod
    def _is_material_number(
        value: str,
    ) -> bool:

        clean = (
            value
            .replace("%", "")
            .replace(",", ".")
        )

        try:
            number = float(clean)
        except ValueError:
            return False

        if (
            number.is_integer()
            and 0 <= number <= 30
        ):
            return False

        return True
