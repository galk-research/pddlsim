; equality predicate (5:25) used in condition, but `:equality` is not in requirements section
(define (domain precondition-with-type-mismatch)
        (:action move
         :parameters (?x ?y)
         :precondition (= ?x ?y)))