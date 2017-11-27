

(define (problem BW-rand-4-2-4)

	(:domain blocks)
	(:objects b1 b2 b3 b4  - block)
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
	)
	(:goal
		([]<>(on b4 b1)) && ([]<>(on b4 b1)->[]<>(on b2 b2)) && 
		([]<>(ontable b3)->[]<>(on b1 b2)) && 
		([]<>(on b4 b1)->[]<>(on b1 b1)) && 
		([]<>(on b1 b2)->[]<>(on b4 b3))
	)
)
