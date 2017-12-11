from . import conditions

def parse_multiple_goals(alist):
    assert alist[0] == 'all'
    return [conditions.parse_condition(goal) for goal in alist[1:]]
        