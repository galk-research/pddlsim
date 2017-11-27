

(define (problem BW-rand-10-2-1)

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
		<>(((on b2 b6) && (ontable b5) && (on b6 b9) && (on b7 b4) && (on b8 b1) && (on b9 b8)) && 
		X<>(((on b2 b6) && (ontable b3) && (on b5 b8) && (on b6 b1))))

	)
)
