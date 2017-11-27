

(define (problem BW-rand-9-6-3)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9  - block)
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
		(ontable b8)
		(clear b8)
		(ontable b9)
		(clear b9)
	)
	(:goal
		((((((
			((on b2 b9) && (ontable b5) && (on b6 b7) && (on b7 b1) && (ontable b8) && (on b9 b8)) U ((on b2 b9) && (ontable b4) && (on b6 b7) && (on b7 b1))) U 
			((ontable b2) && (on b4 b9) && (on b5 b3))) U 
			((ontable b2) && (ontable b2) && (ontable b5) && (ontable b6) && (on b9 b8))) U 
			((on b2 b7) && (on b2 b7) && (on b4 b3))) U 
			((ontable b2) && (on b3 b5) && (on b5 b4) && (on b8 b2))) U 
			((ontable b2) && (ontable b2) && (on b6 b7) && (on b7 b2) && (on b8 b9) && (ontable b9)))

	)
)
