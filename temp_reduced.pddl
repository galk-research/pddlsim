
(define (problem simple_maze)
(:domain maze)
(:objects
	person1
	goal_tile
	start_tile
	)
(:init
	(empty goal_tile)
	(empty start_tile)
	(west goal_tile start_tile)
	(east start_tile goal_tile)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
