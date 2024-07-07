from parsy import string, seq, forward_declaration

from pddlsim.parser.common import (
    lexeme,
    s_expression,
    braced,
    not_parser,
    or_parser,
    and_parser,
    Name,
    end_parser,
)


class Variable:
    parser = (lexeme(string("?")) >> Name.parser).map(lambda name: Variable(name))

    def __init__(self, name: str):
        self.name = name


class PredicateDefinition:
    parser = s_expression(Name.parser, Variable.parser).combine(
        lambda name, parameters: PredicateDefinition(name, parameters)
    )

    def __init__(self, name: Name, parameters: list[Variable]):
        self.name = name
        self.parameters = parameters


class EqualityFormulaAtom:
    parser = braced(
        seq(lexeme(string("=")) >> Variable.parser, Variable.parser)
    ).combine(lambda a, b: EqualityFormulaAtom(a, b))

    def __init__(self, left_hand_side: Variable, right_hand_side: Variable):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side


class PredicateFormulaAtom:
    parser = s_expression(Name.parser, Variable.parser).combine(
        lambda name, grounding: PredicateFormulaAtom(name, grounding)
    )

    def __init__(self, name: Name, grounding: list[Variable]):
        self.name = name
        self.grounding = grounding


FormulaAtom = EqualityFormulaAtom | PredicateFormulaAtom
formula_atom_parser = EqualityFormulaAtom.parser | PredicateFormulaAtom.parser


precondition_parser = forward_declaration()


class NotPrecondition:
    parser = braced(not_parser >> precondition_parser).combine(
        lambda precondition: NotPrecondition(precondition)
    )

    def __init__(self, precondition: "Precondition"):
        self.precondition = precondition


class OrPrecondition:
    parser = s_expression(or_parser, precondition_parser, ignore_header=True).map(
        lambda preconditions: OrPrecondition(preconditions)
    )

    def __init__(self, preconditions: list["Precondition"]):
        self.preconditions = preconditions


class AndPrecondition:
    parser = s_expression(and_parser, precondition_parser, ignore_header=True).map(
        lambda preconditions: AndPrecondition(preconditions)
    )

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
    parser = braced(not_parser >> PredicateFormulaAtom.parser).map(
        lambda predicate_atom: NotLiteral(predicate_atom)
    )

    def __init__(self, predicate_atom: PredicateFormulaAtom):
        self.predicate_atom = predicate_atom


Literal = NotLiteral | PredicateFormulaAtom
literal_parser = NotLiteral.parser | PredicateFormulaAtom.parser


class AndEffect:
    parser = s_expression(and_parser, literal_parser, ignore_header=True).map(
        lambda literals: AndEffect(literals)
    )

    def __init__(self, literals: list[Literal]):
        self.literals = literals


Effect = AndEffect
effect_parser = AndEffect.parser


class Action:
    parser = braced(
        seq(
            lexeme(string(":action")) >> Name.parser,
            lexeme(string(":parameters")),
            braced(Variable.parser.many()),
            lexeme(string(":precondition")) >> precondition_parser,
            lexeme(string(":effect")) >> effect_parser,
        ).combine(
            lambda name, parameters, precondition, effect: Action(
                name, parameters, precondition, effect
            )
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


predicate_definitions_parser = braced(
    lexeme(string(":predicates")) >> PredicateDefinition.parser.many()
)


class Domain:
    _domain_body_parser = seq(
        braced(lexeme(string("domain")) >> Name.parser),
        predicate_definitions_parser,
        Action.parser.many(),
    )
    parser = (
        braced(lexeme(string("define")) >> _domain_body_parser) << end_parser
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
