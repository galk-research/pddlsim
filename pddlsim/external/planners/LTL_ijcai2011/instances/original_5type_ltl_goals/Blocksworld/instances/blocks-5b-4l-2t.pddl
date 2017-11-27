

(define (problem BW-rand-5-4-2)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5  - block)
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
	)
	(:goal
		[]<>((on b2 b5) && (on b5 b1)) && 
		[]<>((on b2 b4) && (on b2 b4) && (on b3 b1) && (ontable b4) && (on b5 b2)) && 
		[]<>((on b2 b1) && (ontable b4)) && 
		[]<>((ontable b2) && (ontable b2) && (on b3 b2))
	)
)
