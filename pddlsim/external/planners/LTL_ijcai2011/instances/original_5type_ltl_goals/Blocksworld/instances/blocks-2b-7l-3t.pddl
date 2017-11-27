

(define (problem BW-rand-2-7-3)

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
		(((((((
			((ontable b2)) U ((ontable b2))) U 
			((ontable b2))) U 
			((on b2 b1) && (on b2 b1))) U 
			((on b2 b1) && (on b2 b1))) U 
			((on b2 b1) && (on b2 b1))) U 
			((on b2 b1) && (on b2 b1))) U 
			((on b2 b1) && (on b2 b1)))

	)
)
