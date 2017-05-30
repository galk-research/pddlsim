

(define (problem BW-rand-10-4-1)

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
		<>(((ontable b2) && (on b5 b1) && (on b6 b9) && (on b7 b8) && (on b8 b6) && (on b9 b4)) && 
		X<>(((on b2 b6) && (on b3 b10) && (ontable b5) && (on b6 b8)) && 
		X<>(((ontable b2) && (ontable b2) && (on b3 b10) && (on b8 b6)) && 
		X<>(((on b2 b4) && (on b2 b4) && (on b3 b8) && (ontable b6) && (on b7 b5) && (on b9 b3))))))

	)
)
