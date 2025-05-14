; `(at bob lobby)` is defined multiple times in initialization section
(define (problem repeated-initialization)
        (:domain invalid-problems-domain)
        (:objects bob - person)
        (:init (at bob lobby)
               (at bob lobby))
        (:goal (and)))