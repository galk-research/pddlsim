

(define (problem BW-rand-6-2-2)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5 b6  - block)
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
	)
	(:goal
		[]<>((ontable b2) && (on b5 b6) && (ontable b6)) && 
		[]<>((on b2 b3) && (on b2 b3) && (on b3 b4) && (on b4 b6))
	)
)