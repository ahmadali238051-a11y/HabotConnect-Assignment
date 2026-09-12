"""Deterministic Controlled Yes/No (DCYN) normalization library."""

from typing import Final

TRUE_VALUES: Final[frozenset[object]] = frozenset({True, 1, "1", "yes", "true"})
FALSE_VALUES: Final[frozenset[object]] = frozenset({False, 0, "0", "no", "false"})


class DCYNValidationError(ValueError):
    """Raised when input cannot be deterministically converted to Yes or No."""


def normalize_dcyn(value: object) -> bool:
    """Convert an approved binary value to bool and reject every ambiguous value."""
    normalized = value.strip().lower() if isinstance(value, str) else value

    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False

    raise DCYNValidationError(
        "Accepted binary values are Yes, No, True, False, 1, or 0 only."
    )
