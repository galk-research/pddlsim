(define (problem BLOCKS-18-0)
(:domain BLOCKS)
(:objects C P D E A I N J F M L O H R G Q B K - block)
(:INIT (CLEAR K) (CLEAR B) (CLEAR Q) (ONTABLE G) (ONTABLE R) (ONTABLE H)
 (ON K O) (ON O G) (ON B L) (ON L M) (ON M F) (ON F J) (ON J N) (ON N I)
 (ON I A) (ON A E) (ON E D) (ON D R) (ON Q P) (ON P C) (ON C H) (HANDEMPTY))
(:goal <>(  (ON H J) && (ON J N) && (ON N R) && (ON R F) && (ON F K) && (ON K L) && (ON L I) && (ON I B) && (ON B M) && (ON M C) && (ON C D) && (ON D A) && (ON A O) && (ON O Q) && (ON Q P) && (ON P G) && (ON G E))))