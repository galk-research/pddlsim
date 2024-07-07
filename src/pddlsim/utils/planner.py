import json
import sys
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
    print(problem)
    with OneshotPlanner(problem_kind=problem.kind) as planner:
        result: SequentialPlan = planner.solve(problem).plan
        return [
            f"({action.action.value} {' '.join(map(str, action.actual_parameters))})"
            for action in result.actions
        ]


if __name__ == "__main__":
    use_local = True

    if use_local:
        make_plan = local
    else:
        make_plan = online

    plan = make_plan(sys.argv[1], sys.argv[2])
    with open(sys.argv[3], "w") as f:
        f.write("\n".join(plan))
