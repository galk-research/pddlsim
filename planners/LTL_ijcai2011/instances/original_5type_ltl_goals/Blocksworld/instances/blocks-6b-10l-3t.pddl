

(define (problem BW-rand-6-10-3)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5 b6  - block)
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
		(ontable b5)
		(clear b5)
		(ontable b6)
		(clear b6)
	)
	(:goal
		((((((((((
			((ontable b2) && (on b5 b4) && (on b6 b1)) U ((ontable b2) && (ontable b2) && (on b3 b5) && (on b4 b2))) U 
			((ontable b2) && (ontable b2) && (ontable b4) && (on b5 b6))) U 
			((ontable b2) && (on b5 b3) && (on b6 b5))) U 
			((on b2 b6) && (on b6 b5))) U 
			((on b2 b3) && (ontable b4) && (on b5 b4))) U 
			((on b2 b4) && (on b3 b1) && (ontable b4) && (on b6 b5))) U 
			((ontable b2))) U 
			((on b2 b6) && (on b3 b4) && (on b5 b1))) U 
			((on b2 b6) && (ontable b3) && (ontable b5))) U 
			((ontable b2) && (on b4 b3) && (ontable b5) && (on b6 b5)))

	)
)