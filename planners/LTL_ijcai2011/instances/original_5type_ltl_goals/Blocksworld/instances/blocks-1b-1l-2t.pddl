

(define (problem BW-rand-1-1-2)

	(:domain blocks)
	(:objects b1  - block)
	(:init
		(handempty)
		(ontable b1)
		(clear b1)
	)
	(:goal
		[]<>((ontable b2))
	)
)
