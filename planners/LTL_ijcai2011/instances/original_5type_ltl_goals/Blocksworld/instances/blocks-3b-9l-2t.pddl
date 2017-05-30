

(define (problem BW-rand-3-9-2)

	(:domain blocks)
	(:objects b1 b2 b3  - block)
	(:init
		(handempty)
		(ontable b1)
		(clear b1)
		(ontable b2)
		(clear b2)
		(ontable b3)
		(clear b3)
	)
	(:goal
		[]<>((on b2 b3)) && 
		[]<>((on b2 b1) && (ontable b3)) && 
		[]<>((on b2 b3) && (on b2 b3) && (ontable b3)) && 
		[]<>((on b2 b1) && (on b2 b1) && (on b3 b2)) && 
		[]<>((ontable b2)) && 
		[]<>((ontable b2) && (ontable b2)) && 
		[]<>((on b2 b3) && (on b2 b3) && (on b3 b1)) && 
		[]<>((ontable b2)) && 
		[]<>((ontable b2))
	)
)
