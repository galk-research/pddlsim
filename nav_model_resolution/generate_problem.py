MIDDLE = '''
	)
(:init
'''

def create_pddl(tiles, predicates, out_file):
    with open(out_file,'w') as f:
        f.write('''
(define (problem simple_maze)
(:domain maze)
(:objects
	person1''')
        for t in tiles:
            f.write('\n\t'+t)
        f.write(MIDDLE)        
        f.write('\t'+'\n\t'.join(predicates))
        f.write('''
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
''')
def get_tiles(prefix,length):
    return list(map(lambda x: prefix + str(x), range(length)))

def connect_tiles(tiles,direction,reverse_direction):
    predicates = []    
    for current_tile,next_tile in zip(tiles,tiles[1:]):
        predicates.append('({} {} {})'.format(direction,current_tile,next_tile))
        predicates.append('({0} {2} {1})'.format(reverse_direction,current_tile,next_tile)) 
    return predicates

def generate_corridor(length):
    tiles = ['start_tile'] + get_tiles('t',length) + ['goal_tile']
    last_tile = 't'+str(length-1)
    predicates = ['(empty {})'.format(t) for t in tiles]        
    
    predicates += connect_tiles(tiles,'east','west')
    path = 'nav_model_resolution/corridor_{}.pddl'.format(length)
    create_pddl(tiles,predicates,path)
    return path    

def generate_T(corridor_length,goal_length, deadend_length):
    '''
    structured in the following way:
    there are `corridor_length` tiles until the fork, 
    at the fork:
     `goal_length` cells north to the goal
     `deadend_length` cells south to a deadend
    '''
    corridor_tiles = ['start_tile'] + get_tiles('c',corridor_length - 1)
    goal_tiles = get_tiles('g',goal_length-1) + ['goal_tile']
    deadend_tiles = get_tiles('d',deadend_length)
    tiles = corridor_tiles + goal_tiles + deadend_tiles
    predicates = ['(empty {})'.format(t) for t in tiles] + \
        connect_tiles(corridor_tiles,'east','west') + \
        connect_tiles(goal_tiles,'north','south') + \
        connect_tiles(deadend_tiles,'south','north')                        
    
    fork = corridor_tiles[-1]
    predicates.append('(north {} {})'.format(fork,goal_tiles[0]))
    predicates.append('(south {1} {0})'.format(fork,goal_tiles[0]))

    predicates.append('(south {} {})'.format(fork,deadend_tiles[0]))
    predicates.append('(north {1} {0})'.format(fork,deadend_tiles[0]))
 
    path = 'nav_model_resolution/t_{}_{}_{}.pddl'.format(corridor_length,goal_length,deadend_length)
    create_pddl(tiles,predicates,path)
    return path    

if __name__ == '__main__':
    # length = 1000
    # generate_corridor(length)
    generate_T(5,5,5)

    


