from typing import Callable

from parsy import regex, string, seq, Parser

whitespace = regex(r"\s*")
lexeme: Callable[[Parser], Parser] = lambda parser: whitespace >> parser

end_parser = whitespace

or_parser = lexeme(string("or"))
and_parser = lexeme(string("and"))
not_parser = lexeme(string("not"))
left_brace = lexeme(string("("))
right_brace = lexeme(string(")"))


def braced(parser: Parser) -> Parser:
    return left_brace >> parser << right_brace


def s_expression(
    header_parser: Parser,
    item_parser: Parser,
    ignore_header=False,
):
    multiple_item_parser = item_parser.many()
    parser = (
        header_parser >> multiple_item_parser
        if ignore_header
        else seq(header_parser, multiple_item_parser)
    )

    return braced(parser)


class Name:
    parser = lexeme(regex(r"[a-zA-Z][a-zA-Z0-9_\-]*").map(lambda name: Name(name)))

    def __init__(self, value: str):
        self.value = value
