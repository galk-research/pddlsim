(define (problem simple_maze)
(:domain maze)
(:objects
	person1
	start_tile
    goal_tile
	)
(:init
    (person person1)
    (at person1 start_tile)
    (east start_tile goal_tile)
    (west goal_tile start_tile)
    (empty start_tile)
    (empty goal_tile)
)
(:goal 
    (and (at person1 goal_tile))
	)

)
