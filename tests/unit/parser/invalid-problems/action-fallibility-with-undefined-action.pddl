; action with name `woah` (5:27) is undefined
(define (problem action-fallibility-with-undefined-action)
        (:domain invalid-problems-domain)
        (:requirements :fallible-actions)
        (:fails (:action (woah ?x ?y) :on 0.5 (and)))
        (:goal (and)))