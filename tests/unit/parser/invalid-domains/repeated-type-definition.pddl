; type with name `a` (4:31) is defined multiple times in types section (4:10)
(define (domain repeated-type-definition)
        (:requirements :typing)
        (:types a b - a c - b a - c))