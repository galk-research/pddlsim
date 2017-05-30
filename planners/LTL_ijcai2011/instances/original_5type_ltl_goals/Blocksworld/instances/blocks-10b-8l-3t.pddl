

(define (problem BW-rand-10-8-3)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10  - block)
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
		(ontable b10)
		(clear b10)
	)
	(:goal
		((((((((
			((on b2 b7) && (ontable b5) && (ontable b6) && (on b7 b9) && (on b8 b10) && (ontable b9)) U ((on b2 b7) && (on b3 b6) && (ontable b5) && (ontable b6))) U 
			((on b2 b4) && (on b2 b4) && (ontable b3) && (on b8 b1))) U 
			((on b2 b8) && (on b2 b8) && (on b3 b4) && (ontable b6) && (on b7 b3) && (ontable b9))) U 
			((on b2 b7) && (on b7 b4) && (on b9 b1))) U 
			((on b2 b9) && (on b3 b2) && (on b5 b3) && (on b9 b8) && (on b10 b4))) U 
			((ontable b2) && (ontable b2) && (on b3 b10) && (on b4 b5) && (ontable b5) && (on b6 b4) && (ontable b8) && (on b9 b7))) U 
			((ontable b2) && (ontable b2) && (on b6 b8) && (on b7 b5) && (ontable b9))) U 
			((on b2 b10) && (ontable b5) && (on b7 b5)))

	)
)
