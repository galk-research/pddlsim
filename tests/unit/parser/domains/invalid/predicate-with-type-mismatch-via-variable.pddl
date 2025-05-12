; argument `?b` (8:29) in `wow` (8:25) is of type `beans` (7:28), but is supposed to be of type `cool` (5:32)
(define (domain predicate-with-type-mismatch)
        (:requirements :typing)
        (:types cool beans)
        (:predicates (wow ?x - cool))
        (:action move
         :parameters (?b - beans)
         :precondition (wow ?b)))