
(define (problem simple_maze)
(:domain maze)
(:objects
	person1
	start_tile
	goal_tile
	)
(:init
	(empty start_tile)
	(empty goal_tile)
	(east start_tile goal_tile)
	(west goal_tile start_tile)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
