

(define (problem BW-rand-1-10-1)

	(:domain blocks)
	(:objects b1  - block)
	(:init
		(handempty)
		(ontable b1)
		(clear b1)
	)
	(:goal
		<>(((ontable b2)) && 
		X<>(((ontable b2)) && 
		X<>(((ontable b2)) && 
		X<>(((ontable b2)) && 
		X<>(((ontable b2)) && 
		X<>(((ontable b2)) && 
		X<>(((ontable b2)) && 
		X<>(((ontable b2)) && 
		X<>(((ontable b2)) && 
		X<>(((ontable b2))))))))))))

	)
)