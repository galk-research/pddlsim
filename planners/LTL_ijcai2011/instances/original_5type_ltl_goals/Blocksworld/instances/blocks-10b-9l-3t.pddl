

(define (problem BW-rand-10-9-3)

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
		(((((((((
			((ontable b2) && (on b5 b9) && (on b6 b5) && (on b7 b1) && (on b8 b4) && (on b9 b2)) U ((ontable b2) && (on b3 b10) && (on b5 b9) && (on b6 b5))) U 
			((on b2 b4) && (on b2 b4) && (on b3 b7) && (on b8 b5))) U 
			((on b2 b8) && (on b2 b8) && (on b3 b6) && (on b6 b2) && (on b7 b1) && (on b9 b5))) U 
			((on b2 b7) && (on b7 b4) && (ontable b9))) U 
			((on b2 b6) && (ontable b3) && (ontable b5) && (ontable b9) && (on b10 b8))) U 
			((on b2 b8) && (on b2 b8) && (ontable b3) && (on b4 b7) && (on b5 b4) && (on b6 b1) && (ontable b8) && (ontable b9))) U 
			((on b2 b8) && (on b2 b8) && (on b6 b7) && (ontable b7) && (on b9 b3))) U 
			((ontable b2) && (on b5 b6) && (on b7 b9))) U 
			((on b2 b6) && (on b2 b6) && (ontable b8) && (on b10 b3)))

	)
)
