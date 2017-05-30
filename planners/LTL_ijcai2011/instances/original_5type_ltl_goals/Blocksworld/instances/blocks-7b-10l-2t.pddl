

(define (problem BW-rand-7-10-2)

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
		[]<>((on b2 b5) && (on b5 b1) && (on b6 b7) && (on b7 b4)) && 
		[]<>((ontable b2) && (ontable b2) && (on b3 b5) && (ontable b6)) && 
		[]<>((on b2 b7) && (on b2 b7) && (on b3 b4)) && 
		[]<>((ontable b2) && (ontable b2) && (on b3 b7)) && 
		[]<>((on b2 b5) && (on b2 b5) && (ontable b5) && (ontable b6)) && 
		[]<>((on b2 b6) && (on b3 b5) && (ontable b4) && (ontable b6)) && 
		[]<>((on b2 b5) && (on b7 b3)) && 
		[]<>((ontable b2) && (ontable b3) && (ontable b6)) && 
		[]<>((on b2 b1) && (on b2 b1) && (on b6 b2) && (ontable b7)) && 
		[]<>((on b2 b6) && (on b2 b6) && (ontable b3) && (on b4 b5) && (on b5 b7) && (ontable b6))
	)
)
