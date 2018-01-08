
(define (problem simple_maze)
(:domain maze)
(:objects
	person1
	s
	g
	)
(:init
	(empty s)
	(empty g)
	(east s t)
	(west g t)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
