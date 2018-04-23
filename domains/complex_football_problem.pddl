
(define (problem simple_football)
(:domain complex-football)
(:objects
	ball1 ball2 ball3
	left right
	start_tile
	goal_tile
	c0
	c1
	c2
	c3
	g0
	g1
	g2
	g3
	d0
	d1
	d2
	d3
)
(:init
    (left-foot left)
    (right-foot right)
	(ball ball1)
	(ball ball2)
	(ball ball3)
	(connected start_tile c0)
	(connected c0 start_tile)
	(connected c3 goal_tile)
	(connected goal_tile c3)

	(connected c0 c1)
	(connected c1 c0)
	(connected c1 c2)
	(connected c2 c1)
	(connected c2 c3)
	(connected c3 c2)

	(connected g0 g1)
	(connected g1 g0)
	(connected g1 g2)
	(connected g2 g1)
	(connected g2 g3)
	(connected g3 g2)

	(connected d0 d1)
	(connected d1 d0)
	(connected d1 d2)
	(connected d2 d1)
	(connected d2 d3)
	(connected d3 d2)

	(connected g0 c0)
	(connected c0 g0)
	(connected d0 c0)
	(connected c0 d0)
	(connected g1 c1)
	(connected c1 g1)
	(connected d1 c1)
	(connected c1 d1)
	(connected g2 c2)
	(connected c2 g2)
	(connected d2 c2)
	(connected c2 d2)
	(connected g3 c3)
	(connected c3 g3)
	(connected d3 c3)
	(connected c3 d3)

  (at-ball ball1 d1)
  (at-robby start_tile)
)
(:goal
    (and (at-ball ball1 goal_tile)))	
)
