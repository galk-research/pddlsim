; predicate with name `wow` (5:23) is defined multiple times in predicates section
(define (domain repeated-predicate-definition)
        (:predicates (wow ?x ?y)
                     (cool ?y ?z)
                     (wow ?w)))