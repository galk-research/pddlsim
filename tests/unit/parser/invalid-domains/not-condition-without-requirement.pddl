; negation (5:25) used in condition, but `:negative-preconditions` is not in requirements section
(define (domain precondition-with-type-mismatch)
        (:action move
         :parameters ()
         :precondition (not (and))))