; constant `y` (6:21) is of undefined type `beans` (6:25)
(define (domain constant-definition-with-undefined-type)
        (:requirements :typing)
        (:types cool)
        (:constants x - cool
                    y - beans))