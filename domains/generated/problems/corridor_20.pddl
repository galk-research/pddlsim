
(define (problem simple_maze)
(:domain maze)
(:objects
	person1
	start_tile
	t0
	t1
	t2
	t3
	t4
	t5
	t6
	t7
	t8
	t9
	t10
	t11
	t12
	t13
	t14
	t15
	t16
	t17
	t18
	t19
	goal_tile
	)
(:init
	(empty start_tile)
	(empty t0)
	(empty t1)
	(empty t2)
	(empty t3)
	(empty t4)
	(empty t5)
	(empty t6)
	(empty t7)
	(empty t8)
	(empty t9)
	(empty t10)
	(empty t11)
	(empty t12)
	(empty t13)
	(empty t14)
	(empty t15)
	(empty t16)
	(empty t17)
	(empty t18)
	(empty t19)
	(empty goal_tile)
	(east start_tile t0)
	(west t0 start_tile)
	(east t0 t1)
	(west t1 t0)
	(east t1 t2)
	(west t2 t1)
	(east t2 t3)
	(west t3 t2)
	(east t3 t4)
	(west t4 t3)
	(east t4 t5)
	(west t5 t4)
	(east t5 t6)
	(west t6 t5)
	(east t6 t7)
	(west t7 t6)
	(east t7 t8)
	(west t8 t7)
	(east t8 t9)
	(west t9 t8)
	(east t9 t10)
	(west t10 t9)
	(east t10 t11)
	(west t11 t10)
	(east t11 t12)
	(west t12 t11)
	(east t12 t13)
	(west t13 t12)
	(east t13 t14)
	(west t14 t13)
	(east t14 t15)
	(west t15 t14)
	(east t15 t16)
	(west t16 t15)
	(east t16 t17)
	(west t17 t16)
	(east t17 t18)
	(west t18 t17)
	(east t18 t19)
	(west t19 t18)
	(east t19 goal_tile)
	(west goal_tile t19)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
