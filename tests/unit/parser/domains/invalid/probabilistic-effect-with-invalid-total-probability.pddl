; total probability of probabilistic effect (6:19) mustn't be greater than 1, is 1.2
(define (domain probabilistic-effect-without-requirement)
        (:requirements :probabilistic-effects)
        (:action move
         :parameters ()
         :effect (probabilistic 0.6 (and) 0.6 (and))))