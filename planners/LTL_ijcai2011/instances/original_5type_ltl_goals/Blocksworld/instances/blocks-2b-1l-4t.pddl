

(define (problem BW-rand-2-1-4)

	(:domain blocks)
	(:objects b1 b2  - block)
	(:init
		(handempty)
		(ontable b1)
		(clear b1)
		(ontable b2)
		(clear b2)
	)
	(:goal
		([]<>(on b2 b1)) && ([]<>(on b2 b1)->[]<>(ontable b2)) && 
		([]<>(ontable b1)->[]<>(ontable b1))
	)
)
