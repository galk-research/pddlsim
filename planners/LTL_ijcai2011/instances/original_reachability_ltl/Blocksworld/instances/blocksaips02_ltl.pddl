(define (problem BLOCKS-4-1)
(:domain BLOCKS)
(:objects A C D B - block)
(:INIT (CLEAR B) (ONTABLE D) (ON B C) (ON C A) (ON A D) (HANDEMPTY))
(:goal <>(  (ON D C) && (ON C A) && (ON A B))))