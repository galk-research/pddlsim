(define (problem action-fallibility-with-impossible-probability)
        (:domain invalid-problems-domain)
        (:requirements :fallible-actions)
        (:objects bob - person)
        (:fails (:action (move bob) :on 1.2 (and)))
        (:goal (and)))