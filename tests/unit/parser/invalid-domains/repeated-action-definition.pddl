; action with name `move` (5:18) is defined multiple times in actions section
(define (domain repeated-action-definition)
        (:action move
         :parameters (?from ?to))
        (:action move
         :parameters (?person ?from ?to)))