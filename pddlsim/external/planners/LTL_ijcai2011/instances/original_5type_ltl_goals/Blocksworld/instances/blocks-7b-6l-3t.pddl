

(define (problem BW-rand-7-6-3)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5 b6 b7  - block)
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
		(ontable b7)
		(clear b7)
	)
	(:goal
		((((((
			((on b2 b1) && (ontable b5) && (on b6 b5) && (on b7 b6)) U ((on b2 b1) && (on b2 b1) && (on b3 b7) && (on b6 b5))) U 
			((on b2 b4) && (on b2 b4) && (ontable b3))) U 
			((on b2 b1) && (on b2 b1) && (on b3 b7))) U 
			((on b2 b1) && (on b2 b1) && (on b5 b3) && (on b6 b5))) U 
			((ontable b2) && (on b3 b6) && (on b4 b7) && (ontable b6))) U 
			((on b2 b5) && (ontable b7)))

	)
)
