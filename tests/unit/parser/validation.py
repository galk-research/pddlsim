from typing import NewType

import pytest

from pddlsim.parser import parse_domain, parse_problem
from tests import preprocess_files
from tests.unit.parser import _RESOURCES

PDDLText = NewType("PDDLText", str)
ExpectedErrorText = NewType("ExpectedErrorText", str)


def _preprocess_invalid_pddl(
    text: str,
) -> tuple[PDDLText, ExpectedErrorText]:
    if not text.startswith(";"):
        raise ValueError("invalid pddl file must start with comment")

    newline_index = text.index("\n")
    expected_error_text = text[1:newline_index].strip()
    domain_text = text[newline_index:]

    return PDDLText(domain_text), ExpectedErrorText(expected_error_text)


_INVALID_DOMAINS = preprocess_files(
    _RESOURCES.joinpath("invalid-domains"), _preprocess_invalid_pddl
)


_INVALID_PROBLEMS = preprocess_files(
    _RESOURCES.joinpath("invalid-problems"), _preprocess_invalid_pddl
)
_INVALID_PROBLEMS_DOMAIN = parse_domain(
    _RESOURCES.joinpath("invalid-problems-domain.pddl").read_text()
)


@pytest.mark.parametrize(
    ["text", "expected_error_text"],
    _INVALID_DOMAINS.values(),
    ids=_INVALID_DOMAINS.keys(),
)
def test_domain_validation(
    text: PDDLText, expected_error_text: ExpectedErrorText
) -> None:
    with pytest.raises(ValueError) as exception_info:
        parse_domain(text)

    assert expected_error_text == str(exception_info.value)


@pytest.mark.parametrize(
    ["text", "expected_error_text"],
    _INVALID_PROBLEMS.values(),
    ids=_INVALID_PROBLEMS.keys(),
)
def test_problem_validation(
    text: PDDLText, expected_error_text: ExpectedErrorText
) -> None:
    with pytest.raises(ValueError) as exception_info:
        parse_problem(text, _INVALID_PROBLEMS_DOMAIN)

    assert expected_error_text == str(exception_info.value)
