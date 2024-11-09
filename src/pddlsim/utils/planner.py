import json
from urllib import request

from unified_planning.io import PDDLReader
from unified_planning.plans import SequentialPlan
from unified_planning.shortcuts import OneshotPlanner


def online(domain_path, problem_path):
    data = {
        "domain": open(domain_path, "r").read(),
        "problem": open(problem_path, "r").read(),
    }

    req = request.Request("http://solver.planning.domains/solve")
    req.add_header("Content-Type", "application/json")
    resp = json.loads(
        request.urlopen(req, json.dumps(data).encode("utf-8")).read().decode("utf-8")
    )

    return [act["name"] for act in resp["result"]["plan"]]


def local(domain_path, problem_path):
    print(domain_path, problem_path)
    reader = PDDLReader()
    problem = reader.parse_problem(domain_path, problem_path)

    with OneshotPlanner(problem_kind=problem.kind) as planner:
        result: SequentialPlan = planner.solve(problem).plan
        return [
            f"({action.action.name} {' '.join(map(str, action.actual_parameters))})"
            for action in result.actions
        ]
