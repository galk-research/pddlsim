


(define (problem gripper-18)
(:domain gripper-typed)
(:objects  roomA roomB - room Ball1 Ball2 Ball3 Ball4 Ball5 Ball6 Ball7 Ball8 Ball9 Ball10 Ball11 Ball12 Ball13 Ball14 Ball15 Ball16 Ball17 Ball18  - ball )
(:init
(at-robby roomA)
(free left)
(free right)
(at Ball1 roomA)
(at Ball2 roomA)
(at Ball3 roomA)
(at Ball4 roomA)
(at Ball5 roomA)
(at Ball6 roomA)
(at Ball7 roomA)
(at Ball8 roomA)
(at Ball9 roomA)
(at Ball10 roomA)
(at Ball11 roomA)
(at Ball12 roomA)
(at Ball13 roomA)
(at Ball14 roomA)
(at Ball15 roomA)
(at Ball16 roomA)
(at Ball17 roomA)
(at Ball18 roomA)
)
(:goal 
 <>( (at Ball1 roomB)
 && X<>(  (at Ball2 roomB)
 && X<>(  (at Ball3 roomB)
 && X<>(  (at Ball4 roomB)
 && X<>(  (at Ball5 roomB)
 && X<>  (at Ball6 roomB) ) ) ) ) )
)



)