

(define (problem BW-rand-1-9-4)

	(:domain blocks)
	(:objects b1  - block)
	(:init
		(handempty)
		(ontable b1)
		(clear b1)
	)
	(:goal
		([]<>(ontable b1)) && ([]<>(ontable b1)->[]<>(ontable b1))
	)
)
