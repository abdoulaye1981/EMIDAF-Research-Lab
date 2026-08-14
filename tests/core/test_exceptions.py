import pytest

from emidaf_core.core.exceptions import ValidationError


def test_exception():

    with pytest.raises(ValidationError):

        raise ValidationError("Invalid dataframe")