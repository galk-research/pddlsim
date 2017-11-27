

(define (problem BW-rand-4-2-1)

	(:domain blocks)
	(:objects b1 b2 b3 b4  - block)
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
	)
	(:goal
		<>(((on b2 b4)) && 
		X<>(((ontable b2) && (ontable b2) && (on b3 b2) && (on b4 b3))))

	)
)
