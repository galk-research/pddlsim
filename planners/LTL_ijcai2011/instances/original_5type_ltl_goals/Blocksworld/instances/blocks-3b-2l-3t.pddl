

(define (problem BW-rand-3-2-3)

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
		((
			((ontable b2)) U ((ontable b2) && (ontable b3))) U 
			((ontable b2) && (ontable b2) && (on b3 b2)))

	)
)