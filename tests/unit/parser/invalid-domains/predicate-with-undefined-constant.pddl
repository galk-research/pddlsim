; object `x` (6:27) in `a` (6:25) is undefined
(define (domain predicate-with-type-mismatch)
        (:predicates (a ?x))
        (:action move
         :parameters ()
         :precondition (a x)))