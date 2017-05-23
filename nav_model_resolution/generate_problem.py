BEGINNING = '''
(define (problem simple_maze)
(:domain maze)
(:objects
	person1
	start_tile
    goal_tile
    '''

MIDDLE = '''
	)
(:init
'''

END = '''

    (person person1)
    (at person1 start_tile)    
    (empty start_tile)
    (empty goal_tile)
)
(:goal 
    (and (at person1 goal_tile))
	)
)
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


if __name__ == '__main__':
    length = 5
    with open('corridor_'+str(length)+'.pddl','w') as f:
        f.write(BEGINNING)
        f.write('\n\t'.join(map(lambda x: 't'+str(x), range(length))))     
        f.write(MIDDLE)
        
        last_tile = 't'+str(length-1)
        f.write( '''
    (east start_tile t0)
    (west t0 start_tile)
    (east '''+last_tile +''' goal_tile)
    (west goal_tile ''' + last_tile + ")\n")

        for i in range(length-1):
            current_tile = 't'+str(i)
            next_tile = 't'+str(i+1)
            f.write("\t(east " + current_tile + " " + next_tile + ")\n"+\
            "\t(west " + next_tile + " " + current_tile + ")\n")
        
        f.write('\n\t'.join(map(lambda x: '(empty t'+str(x) + ' )', range(length))))     
        f.write(END)
        

    
