(define (domain grid)
(:requirements :types)
(:types location keys shapes)
(:predicates (conn ?x - location ?y - location)
             (key-shape ?k - keys ?s - shapes )
             (lock-shape ?x - location ?s - shapes)
             (at ?k - keys ?x - location)
	     (at-robot ?x - location)
             (place ?p - location)
             (key ?k - keys)
             (shape ?s - shapes)
             (locked ?x - location)
             (holding ?k - keys)
             (open ?x - location)
             (arm-empty ))



(:action unlock
:parameters (?curpos - location ?lockpos - location ?key - keys ?shape - shapes)
:precondition (and (place ?curpos) (place ?lockpos) (key ?key) (shape ?shape)
          (conn ?curpos ?lockpos) (key-shape ?key ?shape)
                   (lock-shape ?lockpos ?shape) (at-robot ?curpos) 
                   (locked ?lockpos) (holding ?key))
:effect (and  (open ?lockpos) (not (locked ?lockpos))))


(:action move
:parameters (?curpos - location ?nextpos - location)
:precondition (and (place ?curpos) (place ?nextpos)
               (at-robot ?curpos) (conn ?curpos ?nextpos) (open ?nextpos))
:effect (and (at-robot ?nextpos) (not (at-robot ?curpos))))

(:action pickup
:parameters (?curpos - location ?key - keys)
:precondition (and (place ?curpos) (key ?key) 
                  (at-robot ?curpos) (at ?key ?curpos) (arm-empty ))
:effect (and (holding ?key)
   (not (at ?key ?curpos)) (not (arm-empty ))))


(:action pickup-and-loose
:parameters (?curpos - location ?newkey - keys ?oldkey - keys)
:precondition (and (place ?curpos) (key ?newkey) (key ?oldkey)
                  (at-robot ?curpos) (holding ?oldkey) (at ?newkey ?curpos))
:effect (and (holding ?newkey) (at ?oldkey ?curpos)
        (not (holding ?oldkey)) (not (at ?newkey ?curpos))))

(:action putdown
:parameters (?curpos - location ?key - keys)
:precondition (and (place ?curpos) (key ?key) 
                  (at-robot ?curpos) (holding ?key))
:effect (and (arm-empty ) (at ?key ?curpos) (not (holding ?key)))))


	
