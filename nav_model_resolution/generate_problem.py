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

def generate_corridor(length):
    tiles = ['start_tile'] + list(map(lambda x: 't'+str(x), range(length))) + ['goal_tile']
    last_tile = 't'+str(length-1)
    predicates = ['(empty {})'.format(t) for t in tiles]        
    
    for current_tile,next_tile in zip(tiles,tiles[1:]):
        predicates.append('(east {} {})'.format(current_tile,next_tile))
        predicates.append('(west {1} {0})'.format(current_tile,next_tile)) 
    path = 'nav_model_resolution/corridor_{}.pddl'.format(length)
    create_pddl(tiles,predicates,path)
    return path    

if __name__ == '__main__':
    length = 1000
    generate_corridor(length)
    


