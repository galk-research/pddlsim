

(define (problem BW-rand-10-7-0)

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
		<>((ontable b2) && (on b5 b3) && (on b6 b10) && (on b7 b5) && (ontable b8) && (on b9 b2)) && 
		<>((on b2 b5) && (on b3 b10) && (on b5 b8) && (ontable b6)) && 
		<>((ontable b2) && (ontable b2) && (on b3 b6) && (on b8 b2)) && 
		<>((on b2 b10) && (on b2 b10) && (on b3 b6) && (on b6 b7) && (ontable b7) && (ontable b9)) && 
		<>((on b2 b6) && (on b7 b3) && (ontable b9)) && 
		<>((ontable b2) && (on b3 b7) && (on b5 b3) && (on b9 b1) && (on b10 b6)) && 
		<>((on b2 b9) && (on b2 b9) && (on b3 b5) && (on b4 b10) && (on b5 b7) && (ontable b6) && (on b8 b3) && (on b9 b8))

	)
)
