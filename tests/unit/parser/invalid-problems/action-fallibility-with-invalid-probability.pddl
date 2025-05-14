; action fallibility for `move` (6:27) is with impossible probability 1.2
(define (problem action-fallibility-with-invalid-probability)
        (:domain invalid-problems-domain)
        (:requirements :fallible-actions)
        (:objects bob - person)
        (:fails (:action (move bob) :on 1.2 (and)))
        (:goal (and)))