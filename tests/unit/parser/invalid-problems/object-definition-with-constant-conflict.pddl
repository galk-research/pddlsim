; object `lobby` (4:19) shares name with a constant in domain
(define (problem object-definition-with-constant-conflict)
        (:domain invalid-problems-domain)
        (:objects lobby - person)
        (:goal (and)))