(define (problem logistics-4-4-4-4-5-4)
	(:domain logistics)
	(:objects
		apn1 apn2 apn3 apn4 apn5 - airplane
		apt1 apt2 apt3 apt4 - airport
		pos1 pos2 pos3 pos4 - location
		cit1 cit2 cit3 cit4 - city
		tru1 tru2 tru3 tru4 - truck
		obj1 obj2 obj3 obj4 - package
	)
	(:init
		(at apn1 apt1) (at apn2 apt2) (at apn3 apt3) (at apn4 apt4) (at apn5 apt1) 
		(at tru1 pos1) (at tru2 pos2) (at tru3 pos3) (at tru4 pos4) 
		(at obj1 pos1) (at obj2 pos2) (at obj3 pos3) (at obj4 pos4) 
		(in-city apt1 cit1) (in-city apt2 cit2) (in-city apt3 cit3) (in-city apt4 cit4) 
		(in-city pos1 cit1) (in-city pos2 cit2) (in-city pos3 cit3) (in-city pos4 cit4) 
	)
	(:goal
		<>(at obj2 pos4) && <>(at obj3 pos2) && <>(at obj1 pos3) && <>(at obj3 pos1) && <>(at obj2 pos4)
	)
)
