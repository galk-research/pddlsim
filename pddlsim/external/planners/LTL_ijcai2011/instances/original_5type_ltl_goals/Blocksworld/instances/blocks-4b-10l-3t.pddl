

(define (problem BW-rand-4-10-3)

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
		((((((((((
			((ontable b2)) U ((ontable b2) && (ontable b2) && (on b3 b4) && (ontable b4))) U 
			((on b2 b4) && (on b2 b4) && (ontable b3))) U 
			((ontable b2) && (on b3 b1))) U 
			((ontable b2) && (ontable b2) && (on b3 b1))) U 
			((ontable b2))) U 
			((ontable b2) && (ontable b2) && (ontable b3))) U 
			((ontable b2))) U 
			((ontable b2) && (ontable b2))) U 
			((on b2 b4) && (on b2 b4) && (on b3 b2))) U 
			((on b2 b3) && (ontable b3) && (on b4 b1)))

	)
)
