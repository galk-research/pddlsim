(define (problem TPP)
(:domain TPP-Propositional)
(:objects
	 goods  - goods
	truck1 truck2 - truck
	market1 market2 market3 - market
	 depot - depot
	level0 level1 level2 level3 - level)

(:init
	(next level1 level0)
	(next level2 level1)
	(next level3 level2)

	(ready-to-load goods market1 level0)
	(ready-to-load goods market2 level0)
	(ready-to-load goods market3 level0)

	(stored goods level0)


	(loaded goods truck1 level0)
	(loaded goods truck2 level0)

	
	(connected market1 market3)
	(connected market2 market3)
	(connected market3 market1)
	(connected market3 market2)
	(connected depot market2)
	(connected market2 depot)



	(on-sale goods market1 level1)
	
	(on-sale goods market2 level1)
	
	(on-sale goods market3 level1)
	
	(at truck1 depot)

	(at truck2 depot))

(:goal <>( (stored goods level3))))