# import pddl.parser
# from first_parser import FirstParser
from fd_parser import FDParser
from nav_model_resolution.generate_problem import create_pddl
import copy
DIST = 'distance'

directions = {'north':'south','south':'north','east':'west','west':'east'}

def generate_graph(state):
    graph = {key:dict() for key in map(lambda x:x[0][0], state['empty'])}
    for direction in directions:
        for s in state[direction]:            
            graph[s[0][0]][direction] = (s[1][0],1)
    return graph

def reduce_problem(domain_path, problem_path, new_problem_path):
    # pddlParser = pddl.parser.Parser(domain_path)
    # domain = pddlParser.parse_domain()
    # pddlParser.set_prob_file(problem_path)
    # problem = pddlParser.parse_problem(domain)
    parser = FDParser(domain_path,problem_path)
    state = parser.build_first_state()
    graph = generate_graph(state)
    original_graph = copy.deepcopy(graph)
            # graph[s[0][0]][DIST] = 1
    # print (graph)
    # print()
    start = 'start_tile'
    goal = 'goal_tile'
    
    for t, neighbors in list(graph.items()):        
        if len(neighbors) == 2 and t != start and t != goal:
            got_one = False
            for n in neighbors:
                if directions[n] in neighbors:
                    got_one = True
                    break            
            if got_one:
                # print (n, t, neighbors)    
                oppisite = directions[n]
                tile_in_n, distance_to_n = graph[t][n]
                tile_oppisite_n, distance_to_oppisite = graph[t][oppisite]
                
                total_distance = distance_to_n + distance_to_oppisite
                # print(t, n, tile_in_n, oppisite, tile_oppisite_n)
                graph[tile_in_n][oppisite] = (tile_oppisite_n,total_distance)
                graph[tile_oppisite_n][n] = (tile_in_n,total_distance)
                del graph[t]

    # print(graph)
    generate_pddl_from_graph(graph,new_problem_path)
    return graph, original_graph

def generate_pddl_from_graph(graph,path):
    tiles = graph.keys()
    predicates = ["(empty {})".format(t) for t in tiles]
    for t, neighbors in graph.items():
        for direction, (tile,distance) in neighbors.items():
            predicates.append("({} {} {})".format(direction,t,tile))
        
    create_pddl(tiles,predicates,path)