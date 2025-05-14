; argument `my-bean` (9:29) in `wow` (9:25) is of type `beans` (5:31), but is supposed to be of type `cool` (6:32)
(define (domain predicate-with-type-mismatch-via-constant)
        (:requirements :typing)
        (:types cool beans)
        (:constants my-bean - beans)
        (:predicates (wow ?x - cool))
        (:action move
         :parameters ()
         :precondition (wow my-bean)))