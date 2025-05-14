; revealable is with impossible probability 1.2
(define (problem revealable-with-impossible-probability)
        (:domain invalid-problems-domain)
        (:requirements :revealables)
        (:reveals (when 1.2 (and) (and)))
        (:goal (and)))