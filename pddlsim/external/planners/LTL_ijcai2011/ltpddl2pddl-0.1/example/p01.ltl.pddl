(define (problem automat-01)
	(:domain automat)
	(:objects c11 c12 c13 c21 c22 c23 c31 c32 c33 - cells)
	(:init 
		(connected c11 c21)
		(connected c21 c11)
		
		(connected c21 c31)
		(connected c31 c21)
		
		(connected c21 c22)
		(connected c22 c21)
		
		(connected c22 c32)
		(connected c32 c22)
		
		(connected c32 c33)
		(connected c33 c32)
		
		(connected c33 c23)
		(connected c23 c33)
		
		(connected c23 c13)
		(connected c13 c23)
		
		(connected c13 c12)
		(connected c12 c13)
		
		;special cells
		(food-station c23)
		(drink-station c23)
		(drink-station c33)
		(drink-station c11)
		(bedroom c11)
		
		(next l0 l1)
		(next l1 l2)
		(next l2 l3)
		(next l3 l4)
		(next l4 l5)
		(next l5 l6)
		(next l6 l7)
		(next l7 l8)
		(next l8 l9)
		(next l9 l10)
		(next l10 l11)
		(next l11 l12)
		(next l12 l13)
		(next l13 l14)
				
		(at robot c11)
		(hunger l0)
		(thirst l0)
		(power l5)
		(handempty)
	)
	
	(:goal 
		[](<> (at robot c12) && <>(at robot c11))
	)
)
