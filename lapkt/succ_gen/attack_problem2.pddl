(define (problem network_clique_chain)
    (:domain computer_network)
    (:objects
        windows10_0
        windows10_1
        windows10_2
        windows7_0
        windows7_1
        windows7_2
        ubuntu16_0
        ubuntu16_1
        ubuntu16_2
        mint
        )
    (:init
        (computer windows10_0)
        (computer windows10_1)
        (computer windows10_2)
        (computer windows7_0)
        (computer windows7_1)
        (computer windows7_2)
        (computer ubuntu16_0)
        (computer ubuntu16_1)
        (computer ubuntu16_2)
        (computer mint)

        (windows10 windows10_0)
        (windows10 windows10_1)
        (windows10 windows10_2)
        (windows7 windows7_0)
        (windows7 windows7_1)
        (windows7 windows7_2)
        (ubuntu16 ubuntu16_0)
        (ubuntu16 ubuntu16_1)
        (ubuntu16 ubuntu16_2)
        (mint mint)

        (connected windows10_0 windows10_1)
        (connected windows10_1 windows10_0)
        (connected windows10_0 windows10_2)
        (connected windows10_2 windows10_0)
        (connected windows10_1 windows10_2)
        (connected windows10_2 windows10_1)

        (connected windows7_0 windows7_1)
        (connected windows7_1 windows7_0)
        (connected windows7_0 windows7_2)
        (connected windows7_2 windows7_0)
        (connected windows7_1 windows7_2)
        (connected windows7_2 windows7_1)

        (connected ubuntu16_0 ubuntu16_1)
        (connected ubuntu16_1 ubuntu16_0)
        (connected ubuntu16_0 ubuntu16_2)
        (connected ubuntu16_2 ubuntu16_0)
        (connected ubuntu16_1 ubuntu16_2)
        (connected ubuntu16_2 ubuntu16_1)

        (connected ubuntu16_1 mint)
        (connected mint ubuntu16_1)

        (connected windows10_2 windows7_0)
        (connected windows7_0 windows10_2)

        (connected windows7_2 ubuntu16_2)
        (connected ubuntu16_2 windows7_2)

        (connected windows10_1 ubuntu16_0)
        (connected ubuntu16_0 windows10_1)


        (attacked windows10_0)
        (attacker-at windows10_0)
    )
    (:goal
        (and (or (attacked windows10_0) (attacked windows10_1) (attacked windows10_2))
         (or (attacked windows7_0) (attacked windows7_1) (attacked windows7_2))
         (or (attacked ubuntu16_0) (attacked ubuntu16_1) (attacked ubuntu16_2))
         (attacked mint))
    )
)
