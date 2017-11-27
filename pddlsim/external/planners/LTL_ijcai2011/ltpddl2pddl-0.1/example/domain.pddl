(define (domain automat)
  (:requirements :adl)
  (:types items - objects cells beds levels)
  (:constants l0 l1 l2 l3 l4 l5 l6 l7 l8 l9 l10 l11 l12 l13 l14 - levels robot - objects food drink - items)
  (:predicates 
  			(next ?cur - levels ?nxt - levels)
  			(connected ?c1 - cells ?c2 - cells)
  			(food-station ?c - cells)
  			(drink-station ?c - cells)
  			(bedroom ?c - cells)
  			(hunger ?l - levels)
  			(thirst ?l -levels)
  			(power ?l - levels)
  			(at ?it - objects ?c - cells)
  			(holding ?it - items)
  			(handempty)
  )
  
  (:action move
    :parameters (?from - cells ?to - cells)
    :precondition (and (at robot ?from) (connected ?from ?to) (not (hunger l5)) (not (thirst l5)) (not (power l0)))
    :effect
        (and (not (at robot ?from))
             (at robot ?to)
             
             (forall (?cur ?nxt - levels) 
             	(when 
             		(and (hunger ?cur) (next ?cur ?nxt)) 
             		(and (not (hunger ?cur)) (hunger ?nxt))
         		)
     		)
     		
	        (forall (?cur ?nxt - levels) 
	         	(when 
	         		(and (thirst ?cur) (next ?cur ?nxt)) 
	         		(and (not (thirst ?cur)) (thirst ?nxt))
	     		)
	 		)
	 		
            (forall (?cur ?nxt - levels) 
             	(when 
             		(and (power ?cur) (next ?nxt ?cur)) 
             		(and (not (power ?cur)) (power ?nxt))
         		)
     		)     		
		)
  )
  
  (:action eat
    :precondition (and  (holding food))
    :effect(and 
    	(handempty)
    	(not (holding food))
    	(hunger l0)
    	(forall (?l - levels) 
    		(when 
    			(not (= ?l l0)) 
    			(not (hunger ?l)) 
    		)
		)
    )
  )  
  
  (:action have-drink
    :precondition (and  (holding drink))
    :effect(and 
    	(handempty)
    	(not (holding drink))
    	(thirst l0)
    	(forall (?l - levels) 
    		(when 
    			(not (= ?l l0)) 
    			(not (thirst ?l)) 
    		)
		)
    )
  )  
  
  ; rest
  (:action rest
    :parameters (?c - cells)
    :precondition (and (at robot ?c) (bedroom ?c))
    :effect(and     	
    	(power l14)
    	(forall (?l - levels) 
    		(when 
    			(not (= ?l l14)) 
    			(not (power ?l)) 
    		)
		)
  	)
  )
  
  
  ; get new food (e.g., from store)
  (:action get-food
    :parameters (?c - cells)
    :precondition (and (at robot ?c) (food-station ?c) (handempty))
    :effect(and (not (handempty)) (holding food))
  )
  
  ; get new drink (e.g., from store)
  (:action get-drink
    :parameters (?c - cells)
    :precondition (and (at robot ?c) (drink-station ?c) (handempty))
    :effect(and (not (handempty)) (holding drink))
  )
  
  (:action pick-up
  	:parameters (?it - items ?c - cells)
  	:precondition (and (handempty) (at robot ?c) (at ?it ?c))
  	:effect (and (holding ?it) (not(handempty)) (not (at ?it ?c)))
  )
  
;  (:action drop-down
;  	:parameters (?it - items ?c -cells)
;  	:precondition (and (holding ?it) (at robot ?c))
;  	:effect (and (not(holding ?it)) (handempty) (at ?it ?c))
;  )  
  
)
