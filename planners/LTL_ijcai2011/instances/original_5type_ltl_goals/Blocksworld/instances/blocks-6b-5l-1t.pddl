

(define (problem BW-rand-6-5-1)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5 b6  - block)
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
	)
	(:goal
		<>(((ontable b2) && (ontable b5) && (on b6 b5)) && 
		X<>(((ontable b2) && (ontable b2) && (on b3 b6) && (on b4 b1)) && 
		X<>(((on b2 b5) && (on b2 b5) && (ontable b4) && (on b5 b4)) && 
		X<>(((on b2 b5) && (ontable b5) && (on b6 b4)) && 
		X<>(((ontable b2) && (on b6 b5)))))))

	)
)
