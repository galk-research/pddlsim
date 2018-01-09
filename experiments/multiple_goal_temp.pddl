
    (define (problem simple_maze)
    (:domain  maze)
    (:objects
        
	g3
	g2
	g1
	g0
	goal_tile
	start_tile
	d4
	person1
	c3
	c2
	c1
	c0
	d2
	d3
	d0
	d1)
(:init
	(south d1 d2)
	(south c3 d0)
	(south g1 g0)
	(south g3 g2)
	(south g0 c3)
	(south d2 d3)
	(south g2 g1)
	(south d0 d1)
	(south goal_tile g3)
	(south d3 d4)
	(north g2 g3)
	(north g3 goal_tile)
	(north c3 g0)
	(north d4 d3)
	(north d2 d1)
	(north d3 d2)
	(north d1 d0)
	(north g0 g1)
	(north d0 c3)
	(north g1 g2)
	(west c2 c1)
	(west c3 c2)
	(west c1 c0)
	(west c0 start_tile)
	(person person1)
	(at person1 start_tile)
	(east c0 c1)
	(east c2 c3)
	(east c1 c2)
	(east start_tile c0)
	(empty c1)
	(empty c0)
	(empty d2)
	(empty d4)
	(empty d3)
	(empty d0)
	(empty goal_tile)
	(empty g3)
	(empty d1)
	(empty g2)
	(empty g1)
	(empty g0)
	(empty start_tile)
	(empty c3)
	(empty c2)
            )
    (:goal
        (and (at person1 goal_tile))
        )
    )
    