

(define (problem BW-rand-1-8-3)

	(:domain blocks)
	(:objects b1  - block)
	(:init
		(handempty)
		(ontable b1)
		(clear b1)
	)
	(:goal
		((((((((
			((ontable b2)) U ((ontable b2))) U 
			((ontable b2))) U 
			((ontable b2))) U 
			((ontable b2))) U 
			((ontable b2))) U 
			((ontable b2))) U 
			((ontable b2))) U 
			((ontable b2)))

	)
)