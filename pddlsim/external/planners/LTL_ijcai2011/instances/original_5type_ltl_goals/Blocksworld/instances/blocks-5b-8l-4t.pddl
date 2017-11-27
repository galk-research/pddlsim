

(define (problem BW-rand-5-8-4)

	(:domain blocks)
	(:objects b1 b2 b3 b4 b5  - block)
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
	)
	(:goal
		([]<>(on b3 b4)) && ([]<>(on b3 b4)->[]<>(on b4 b3)) && 
		([]<>(on b1 b2)->[]<>(on b5 b3)) && 
		([]<>(on b4 b4)->[]<>(ontable b1)) && 
		([]<>(on b3 b2)->[]<>(on b3 b3)) && 
		([]<>(on b3 b4)->[]<>(on b1 b2))
	)
)
