

(define (problem BW-rand-8-10-0)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5 b6 b7 b8  - block)
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
	)
	(:goal
		<>((on b2 b7) && (ontable b5) && (ontable b6) && (on b7 b5) && (on b8 b3)) && 
		<>((on b2 b8) && (on b2 b8) && (on b5 b4) && (on b7 b3) && (on b8 b1)) && 
		<>((on b2 b6) && (ontable b6) && (on b7 b5)) && 
		<>((ontable b2) && (on b5 b3) && (on b8 b6)) && 
		<>((ontable b2) && (ontable b2) && (on b5 b7) && (ontable b6) && (on b8 b4)) && 
		<>((on b2 b6) && (on b8 b7)) && 
		<>((ontable b2) && (ontable b3) && (ontable b6) && (ontable b8)) && 
		<>((on b2 b5) && (on b5 b7) && (ontable b6) && (on b7 b8) && (ontable b8)) && 
		<>((on b2 b3) && (on b2 b3) && (ontable b3) && (on b4 b1) && (ontable b6) && (ontable b7)) && 
		<>((on b2 b8) && (on b2 b8) && (on b6 b3) && (on b7 b6))

	)
)
