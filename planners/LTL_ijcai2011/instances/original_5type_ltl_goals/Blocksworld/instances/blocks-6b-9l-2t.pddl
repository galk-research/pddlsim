

(define (problem BW-rand-6-9-2)

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
		[]<>((on b2 b3) && (on b5 b4) && (on b6 b1)) && 
		[]<>((on b2 b5) && (on b2 b5) && (ontable b3) && (on b4 b2)) && 
		[]<>((ontable b2) && (ontable b2) && (on b4 b6) && (on b5 b4)) && 
		[]<>((ontable b2) && (on b5 b1) && (on b6 b5)) && 
		[]<>((ontable b2) && (on b6 b3)) && 
		[]<>((ontable b2) && (on b4 b5) && (ontable b5)) && 
		[]<>((on b2 b3) && (on b3 b5) && (on b4 b2) && (on b6 b1)) && 
		[]<>((on b2 b1)) && 
		[]<>((on b2 b5) && (on b3 b4) && (ontable b5))
	)
)
