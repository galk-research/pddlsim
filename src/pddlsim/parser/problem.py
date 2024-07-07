from parsy import forward_declaration, seq, string

from pddlsim.parser.common import (
    braced,
    not_parser,
    s_expression,
    or_parser,
    and_parser,
    lexeme,
    Name,
    end_parser,
)


class ProblemObject:
    parser = Name.parser.map(lambda name: ProblemObject(name))

    def __init__(self, name: Name):
        self.name = name


class GroundPredicate:
    parser = s_expression(Name.parser, ProblemObject.parser).combine(
        lambda name, grounding: GroundPredicate(name, grounding)
    )

    def __init__(self, predicate_name: Name, grounding: list[ProblemObject]):
        self.predicate_name = predicate_name
        self.grounding = grounding


goal_parser = forward_declaration()


class NotGoal:
    parser = braced(not_parser >> goal_parser).combine(lambda goal: NotGoal(goal))

    def __init__(self, goal: "Goal"):
        self.goal = goal


class OrGoal:
    parser = s_expression(or_parser, goal_parser, ignore_header=True).map(
        lambda goals: OrGoal(goals)
    )

    def __init__(self, goals: list["Goal"]):
        self.goals = goals


class AndGoal:
    parser = s_expression(and_parser, goal_parser, ignore_header=True).map(
        lambda goals: AndGoal(goals)
    )

    def __init__(self, goals: list["Goal"]):
        self.goals = goals


Goal = GroundPredicate | NotGoal | OrGoal | AndGoal
goal_parser.become(
    NotGoal.parser | OrGoal.parser | AndGoal.parser | GroundPredicate.parser
)


class Problem:
    _problem_body = seq(
        braced(lexeme(string("problem")) >> Name.parser),
        braced(lexeme(string(":domain")) >> Name.parser),
        s_expression(
            lexeme(string(":objects")), ProblemObject.parser, ignore_header=True
        ),
        s_expression(
            lexeme(string(":init")), GroundPredicate.parser, ignore_header=True
        ),
        braced(lexeme(string(":goal")) >> goal_parser),
    ).combine(
        lambda name, domain_name, problem_objects, initialization, goal: Problem(
            name, domain_name, problem_objects, initialization, goal
        )
    )

    parser = braced(lexeme(string("define")) >> _problem_body) << end_parser

    def __init__(
        self,
        name: Name,
        domain_name: Name,
        problem_objects: list[ProblemObject],
        initialization: list[GroundPredicate],
        goal: Goal,
    ):
        self.name = name
        self.domain_name = domain_name
        self.problem_objects = problem_objects
        self.initialization = initialization
        self.goal = goal


print(
    Problem.parser.parse(
        """
(define (problem strips-gripper2)
    (:domain gripper-strips)
    (:objects rooma roomb ball1 ball2 left right)
    (:init (room rooma)
           (room roomb)
           (ball ball1)
           (ball ball2)
           (gripper left)
           (gripper right)
           (at-robby rooma)
           (free left)
           (free right)
           (at ball1 rooma)
           (at ball2 rooma))
    (:goal (at ball1 roomb)))
"""
    )
)
