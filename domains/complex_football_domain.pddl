(define (domain complex-football)
(:predicates
	 (at-robby ?c) (at-ball ?b ?c) (connected ?c1 ?c2) (left-foot ?f) (right-foot ?f) (up ?f) (ball ?b))

(:action move-left-leg
 :parameters (?c1 ?c2 ?f1 ?f2)
 :precondition
	(and (at-robby ?c1)  (connected ?c1 ?c2) (left-foot ?f1) (right-foot ?f2) (up ?f1) (not (up ?f2)))
 :effect
	(and (at-robby ?c2) (not (at-robby ?c1)) (not (up ?f1))))

(:action move-right-leg
 :parameters (?c1 ?c2 ?f1 ?f2)
 :precondition
	(and (at-robby ?c1)  (connected ?c1 ?c2) (right-foot ?f1) (left-foot ?f2) (up ?f1) (not (up ?f2)))
 :effect
	(and (at-robby ?c2) (not (at-robby ?c1)) (not (up ?f1))))


(:action raise-left
    :parameters (?f)
	:precondition
	  (and (left-foot ?f) (not (up ?f)))
	:effect
	  (and (up ?f)))

(:action raise-right
    :parameters (?f)
	:precondition
	  (and (right-foot ?f) (not (up ?f)))
	:effect
	  (and (up ?f)))

(:action lower-left
    :parameters (?f)
	:precondition
	  (and (left-foot ?f) (up ?f))
	:effect
	  (and (not(up ?f))))

(:action lower-right
    :parameters (?f)
	:precondition
	  (and (right-foot ?f) (up ?f))
	:effect
	  (and (not(up ?f))))

(:action kick-left
	:parameters (?b ?c1 ?c2 ?f)
	:precondition
  	(and (ball ?b) (at-ball ?b ?c1) (at-robby ?c1) (connected ?c1 ?c2) (left-foot ?f) (up ?f))
 :effect
	  (and (at-ball ?b ?c2) (not (at-ball ?b ?c1))))

(:action kick-right
			:parameters (?b ?c1 ?c2 ?f)
			:precondition
		  	(and (ball ?b) (at-ball ?b ?c1) (at-robby ?c1) (connected ?c1 ?c2) (right-foot ?f) (up ?f))
		 :effect
			  (and (at-ball ?b ?c2) (not (at-ball ?b ?c1))))

)
