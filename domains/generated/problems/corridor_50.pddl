
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
	t20
	t21
	t22
	t23
	t24
	t25
	t26
	t27
	t28
	t29
	t30
	t31
	t32
	t33
	t34
	t35
	t36
	t37
	t38
	t39
	t40
	t41
	t42
	t43
	t44
	t45
	t46
	t47
	t48
	t49
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
	(empty t20)
	(empty t21)
	(empty t22)
	(empty t23)
	(empty t24)
	(empty t25)
	(empty t26)
	(empty t27)
	(empty t28)
	(empty t29)
	(empty t30)
	(empty t31)
	(empty t32)
	(empty t33)
	(empty t34)
	(empty t35)
	(empty t36)
	(empty t37)
	(empty t38)
	(empty t39)
	(empty t40)
	(empty t41)
	(empty t42)
	(empty t43)
	(empty t44)
	(empty t45)
	(empty t46)
	(empty t47)
	(empty t48)
	(empty t49)
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
	(east t19 t20)
	(west t20 t19)
	(east t20 t21)
	(west t21 t20)
	(east t21 t22)
	(west t22 t21)
	(east t22 t23)
	(west t23 t22)
	(east t23 t24)
	(west t24 t23)
	(east t24 t25)
	(west t25 t24)
	(east t25 t26)
	(west t26 t25)
	(east t26 t27)
	(west t27 t26)
	(east t27 t28)
	(west t28 t27)
	(east t28 t29)
	(west t29 t28)
	(east t29 t30)
	(west t30 t29)
	(east t30 t31)
	(west t31 t30)
	(east t31 t32)
	(west t32 t31)
	(east t32 t33)
	(west t33 t32)
	(east t33 t34)
	(west t34 t33)
	(east t34 t35)
	(west t35 t34)
	(east t35 t36)
	(west t36 t35)
	(east t36 t37)
	(west t37 t36)
	(east t37 t38)
	(west t38 t37)
	(east t38 t39)
	(west t39 t38)
	(east t39 t40)
	(west t40 t39)
	(east t40 t41)
	(west t41 t40)
	(east t41 t42)
	(west t42 t41)
	(east t42 t43)
	(west t43 t42)
	(east t43 t44)
	(west t44 t43)
	(east t44 t45)
	(west t45 t44)
	(east t45 t46)
	(west t46 t45)
	(east t46 t47)
	(west t47 t46)
	(east t47 t48)
	(west t48 t47)
	(east t48 t49)
	(west t49 t48)
	(east t49 goal_tile)
	(west goal_tile t49)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
