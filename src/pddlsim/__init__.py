from unified_planning import environment

# Removes credits from planner invocations
environment.get_environment().credits_stream = None
