

(define (problem BW-rand-9-3-2)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9  - block)
	(:init
		(handempty)
		(ontable b1)
		(clear b1)
		(ontable b2)
		(clear b2)
		(ontable b3)
		(clear b3)
		(ontable b4)
		(clear b4)
		(ontable b5)
		(clear b5)
		(ontable b6)
		(clear b6)
		(ontable b7)
		(clear b7)
		(ontable b8)
		(clear b8)
		(ontable b9)
		(clear b9)
	)
	(:goal
		[]<>((on b2 b4) && (ontable b5) && (on b6 b5) && (on b7 b3) && (ontable b8) && (on b9 b8)) && 
		[]<>((ontable b2) && (ontable b4) && (ontable b6) && (on b7 b4)) && 
		[]<>((on b2 b8) && (on b4 b2) && (ontable b5))
	)
)
