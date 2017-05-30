

(define (problem BW-rand-8-9-1)

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
		<>(((on b2 b6) && (on b5 b3) && (on b6 b5) && (on b7 b8) && (on b8 b1)) && 
		X<>(((on b2 b5) && (on b2 b5) && (ontable b5) && (on b7 b6) && (ontable b8)) && 
		X<>(((on b2 b5) && (ontable b6) && (on b7 b4)) && 
		X<>(((on b2 b5) && (on b5 b7) && (on b8 b6)) && 
		X<>(((on b2 b1) && (on b2 b1) && (ontable b5) && (on b6 b3) && (on b8 b6)) && 
		X<>(((on b2 b4) && (ontable b8)) && 
		X<>(((on b2 b1) && (ontable b3) && (on b6 b5) && (on b8 b3)) && 
		X<>(((on b2 b7) && (on b5 b6) && (ontable b6) && (on b7 b3) && (ontable b8)) && 
		X<>(((on b2 b6) && (on b2 b6) && (ontable b3) && (on b4 b5) && (ontable b6) && (ontable b7)))))))))))

	)
)
