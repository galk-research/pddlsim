; parameter with name `?from` (6:36) is defined multiple times in parameters of `move` (5:18)
(define (domain action-definition-with-repeated-parameter)
        (:requirements :typing)
        (:types cool beans)
        (:action move
         :parameters (?from - cool ?from - beans)))