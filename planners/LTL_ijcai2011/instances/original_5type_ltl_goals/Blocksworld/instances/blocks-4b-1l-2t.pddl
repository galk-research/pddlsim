

(define (problem BW-rand-4-1-2)

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
		[]<>((ontable b2))
	)
)
