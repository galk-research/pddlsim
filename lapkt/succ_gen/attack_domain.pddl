(define (domain computer_network)
    (:predicates
        (computer ?c)
        (windows7 ?c)
        (windows10 ?c)
        (mint ?c)
        (ubuntu16 ?c)
        (attacker-at ?c)
        (connected ?a ?b)
        (attacked ?c)
    )

    (:action attack-ubuntu16
     :parameters (?from ?to)
     :precondition
        (and (computer ?from) (computer ?to) (ubuntu16 ?to) (connected ?from ?to) (attacker-at ?from))
     :effect
        (and (attacker-at ?to) (not (attacker-at ?from)) (attacked ?to)))

    (:action attack-mint
     :parameters (?from ?to)
     :precondition
        (and (computer ?from) (computer ?to) (mint ?to) (connected ?from ?to) (attacker-at ?from))
     :effect
        (and (attacker-at ?to) (not (attacker-at ?from)) (attacked ?to)))

    (:action attack-windows10
     :parameters (?from ?to)
     :precondition
        (and (computer ?from) (computer ?to) (windows10 ?to) (connected ?from ?to) (attacked ?from))
     :effect
        (and (attacker-at ?to) (not (attacker-at ?from)) (attacked ?to)))

    (:action attack-windows7
     :parameters (?from ?to)
     :precondition
        (and (computer ?from) (computer ?to) (windows7 ?to) (connected ?from ?to) (attacker-at ?from))
     :effect
        (and (attacker-at ?to) (not (attacker-at ?from)) (attacked ?to)))

)