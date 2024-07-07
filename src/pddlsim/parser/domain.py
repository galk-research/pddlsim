from typing import Callable

from parsy import regex, string, seq, Parser, forward_declaration

_whitespace = regex(r"\s*")

_lexeme: Callable[[Parser], Parser] = lambda parser: _whitespace >> parser

_left_brace = _lexeme(string("("))
_right_brace = _lexeme(string(")"))


def _s_expression(
    header_parser: Parser,
    item_parser: Parser,
    items: int | None = None,
    ignore_header=False,
):
    header_section_parser = _left_brace >> header_parser
    items_parser = item_parser.many() if items is None else item_parser.times(items)
    items_section_parser = items_parser << _right_brace

    if ignore_header:
        return header_section_parser >> items_section_parser
    else:
        return seq(header_section_parser, items_section_parser)


class Name:
    parser = _lexeme(regex(r"[a-zA-Z][a-zA-Z0-9_\-]*").map(lambda name: Name(name)))

    def __init__(self, value: str):
        self.value = value


class Variable:
    parser = (_lexeme(string("?")) >> Name.parser).map(lambda name: Variable(name))

    def __init__(self, name: str):
        self.name = name


class PredicateDefinition:
    parser = _s_expression(Name.parser, Variable.parser).combine(
        lambda name, parameters: PredicateDefinition(name, parameters)
    )

    def __init__(self, name: Name, parameters: list[Variable]):
        self.name = name
        self.parameters = parameters


class EqualityFormulaAtom:
    parser = _s_expression(
        _lexeme(string("=")), Variable.parser, items=2, ignore_header=True
    ).combine(lambda a, b: EqualityFormulaAtom(a, b))

    def __init__(self, left_hand_side: Variable, right_hand_side: Variable):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side


class PredicateFormulaAtom:
    parser = _s_expression(Name.parser, Variable.parser).combine(
        lambda name, grounding: PredicateFormulaAtom(name, grounding)
    )

    def __init__(self, name: Name, grounding: list[Variable]):
        self.name = name
        self.grounding = grounding


FormulaAtom = EqualityFormulaAtom | PredicateFormulaAtom
formula_atom_parser = EqualityFormulaAtom.parser | PredicateFormulaAtom.parser


precondition_parser = forward_declaration()


class NotPrecondition:
    parser = _s_expression(
        _lexeme(string("not")), precondition_parser, items=1, ignore_header=True
    ).combine(lambda precondition: NotPrecondition(precondition))

    def __init__(self, precondition: "Precondition"):
        self.precondition = precondition


class OrPrecondition:
    parser = _s_expression(
        _lexeme(string("or")), precondition_parser, ignore_header=True
    ).map(lambda preconditions: OrPrecondition(preconditions))

    def __init__(self, preconditions: list["Precondition"]):
        self.preconditions = preconditions


class AndPrecondition:
    parser = _s_expression(
        _lexeme(string("and")), precondition_parser, ignore_header=True
    ).map(lambda preconditions: AndPrecondition(preconditions))

    def __init__(self, preconditions: list["Precondition"]):
        self.preconditions = preconditions


Precondition = FormulaAtom | NotPrecondition | OrPrecondition | AndPrecondition
precondition_parser.become(
    NotPrecondition.parser
    | OrPrecondition.parser
    | AndPrecondition.parser
    | formula_atom_parser
)


class NotLiteral:
    parser = _s_expression(
        _lexeme(string("not")), PredicateFormulaAtom.parser, items=1, ignore_header=True
    ).combine(lambda predicate_atom: NotLiteral(predicate_atom))

    def __init__(self, predicate_atom: PredicateFormulaAtom):
        self.predicate_atom = predicate_atom


Literal = NotLiteral | PredicateFormulaAtom
literal_parser = NotLiteral.parser | PredicateFormulaAtom.parser


class AndEffect:
    parser = _s_expression(
        _lexeme(string("and")), literal_parser, ignore_header=True
    ).map(lambda literals: AndEffect(literals))

    def __init__(self, literals: list[Literal]):
        self.literals = literals


Effect = AndEffect
effect_parser = AndEffect.parser


class Action:
    parser = seq(
        _left_brace >> _lexeme(string(":action")) >> Name.parser,
        _lexeme(string(":parameters"))
        >> _left_brace
        >> Variable.parser.many()
        << _right_brace,
        _lexeme(string(":precondition")) >> precondition_parser,
        _lexeme(string(":effect")) >> effect_parser << _right_brace,
    ).combine(
        lambda name, parameters, precondition, effect: Action(
            name, parameters, precondition, effect
        )
    )

    def __init__(
        self,
        name: Name,
        parameters: list[Variable],
        precondition: Precondition,
        effect: Effect,
    ):
        self.name = name
        self.parameters = parameters
        self.precondition = precondition
        self.effect = effect


predicate_definitions_parser = (
    _left_brace
    >> _lexeme(string(":predicates"))
    >> PredicateDefinition.parser.many()
    << _right_brace
)

domain_name_parser = (
    _left_brace >> _lexeme(string("domain")) >> Name.parser << _right_brace
)

domain_body_parser = seq(
    domain_name_parser,
    predicate_definitions_parser,
    Action.parser.many(),
)


class Domain:
    parser = (
        _left_brace
        >> _lexeme(string("define"))
        >> domain_body_parser
        << _right_brace
        << _whitespace
    ).combine(
        lambda name, predicate_definitions, actions: Domain(
            name, predicate_definitions, actions
        )
    )

    def __init__(
        self,
        name: Name,
        predicate_definitions: list[PredicateDefinition],
        actions: list[Action],
    ):
        self.name = name
        self.predicate_definitions = predicate_definitions
        self.actions = actions
