; parameter `?z` (6:38) of predicate definition `cool` (6:23) is of undefined type `beans` (6:43)
(define (domain predicate-definition-with-undefined-type)
        (:requirements :typing)
        (:types cool)
        (:predicates (wow ?x - cool)
                     (cool ?y - cool ?z - beans)))