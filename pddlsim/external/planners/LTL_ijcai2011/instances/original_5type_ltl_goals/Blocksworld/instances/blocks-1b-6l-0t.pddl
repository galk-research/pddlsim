

(define (problem BW-rand-1-6-0)

	(:domain blocks)
	(:objects b1  - block)
	(:init
		(handempty)
		(ontable b1)
		(clear b1)
	)
	(:goal
		<>((ontable b2)) && 
		<>((ontable b2)) && 
		<>((ontable b2)) && 
		<>((ontable b2)) && 
		<>((ontable b2)) && 
		<>((ontable b2))

	)
)