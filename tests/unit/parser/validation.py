from typing import NewType

import pytest

from pddlsim.parser import parse_domain
from tests import preprocess_files
from tests.unit.parser import _RESOURCES

DomainText = NewType("DomainText", str)
ExpectedErrorText = NewType("ExpectedErrorText", str)


def _preprocess_invalid_domain(
    text: str,
) -> tuple[DomainText, ExpectedErrorText]:
    if not text.startswith(";"):
        raise ValueError("invalid domain file must start with comment")

    newline_index = text.index("\n")
    expected_error_text = text[1:newline_index].strip()
    domain_text = text[newline_index:]

    return DomainText(domain_text), ExpectedErrorText(expected_error_text)


_INVALID_DOMAINS = preprocess_files(
    _RESOURCES.joinpath("domains", "invalid"), _preprocess_invalid_domain
)


@pytest.mark.parametrize(
    ["text", "expected_error_text"],
    _INVALID_DOMAINS.values(),
    ids=_INVALID_DOMAINS.keys(),
)
def test_domain_validation(
    text: DomainText, expected_error_text: ExpectedErrorText
) -> None:
    with pytest.raises(ValueError) as exception_info:
        parse_domain(text)

    assert expected_error_text == str(exception_info.value)
