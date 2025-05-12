; probabilistic effect (5:19) used in action, but `:probabilistic-effects` does not appear in requirements section
(define (domain probabilistic-effect-without-requirement)
        (:action move
         :parameters ()
         :effect (probabilistic)))