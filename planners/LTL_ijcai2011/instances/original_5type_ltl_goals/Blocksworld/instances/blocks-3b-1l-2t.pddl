

(define (problem BW-rand-3-1-2)

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
		[]<>((ontable b2))
	)
)
