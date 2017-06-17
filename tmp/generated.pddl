
    (define (problem simple_maze)
    (:domain  maze)
    (:objects
        person1
	goal_tile
	t4
	t2
	t3
	t0
	start_tile
	person1
	t1)
(:init
	(west t2 t1)
	(west t4 t3)
	(west t3 t2)
	(west t0 start_tile)
	(west goal_tile t4)
	(west t1 t0)
	(person person1)
	(at person1 start_tile)
	(east t1 t2)
	(east start_tile t0)
	(east t2 t3)
	(east t0 t1)
	(east t3 t4)
	(east t4 goal_tile)
	(empty t1)
	(empty goal_tile)
	(empty t0)
	(empty t4)
	(empty t2)
	(empty start_tile)
	(empty t3)        
            )
    (:goal 
        (and (at person1 goal_tile))
        )
    )
    