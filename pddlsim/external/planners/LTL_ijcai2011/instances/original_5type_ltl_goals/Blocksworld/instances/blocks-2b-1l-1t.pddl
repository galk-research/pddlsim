

(define (problem BW-rand-2-1-1)

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
		<>(((ontable b2)))

	)
)
