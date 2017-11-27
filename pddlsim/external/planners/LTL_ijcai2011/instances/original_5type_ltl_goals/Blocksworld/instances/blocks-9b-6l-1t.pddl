

(define (problem BW-rand-9-6-1)

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
		<>(((ontable b2) && (on b5 b6) && (on b6 b7) && (ontable b7) && (on b8 b2) && (on b9 b1)) && 
		X<>(((on b2 b1) && (ontable b4) && (on b6 b4) && (on b7 b6)) && 
		X<>(((on b2 b1) && (on b4 b9) && (ontable b5)) && 
		X<>(((ontable b2) && (ontable b2) && (on b5 b7) && (on b6 b9) && (on b9 b3)) && 
		X<>(((on b2 b7) && (on b2 b7) && (on b4 b9)) && 
		X<>(((on b2 b3) && (ontable b3) && (on b5 b9) && (on b8 b7))))))))

	)
)
