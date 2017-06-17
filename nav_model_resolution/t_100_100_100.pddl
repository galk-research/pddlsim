
(define (problem simple_maze)
(:domain maze)
(:objects
	person1
	start_tile
	c0
	c1
	c2
	c3
	c4
	c5
	c6
	c7
	c8
	c9
	c10
	c11
	c12
	c13
	c14
	c15
	c16
	c17
	c18
	c19
	c20
	c21
	c22
	c23
	c24
	c25
	c26
	c27
	c28
	c29
	c30
	c31
	c32
	c33
	c34
	c35
	c36
	c37
	c38
	c39
	c40
	c41
	c42
	c43
	c44
	c45
	c46
	c47
	c48
	c49
	c50
	c51
	c52
	c53
	c54
	c55
	c56
	c57
	c58
	c59
	c60
	c61
	c62
	c63
	c64
	c65
	c66
	c67
	c68
	c69
	c70
	c71
	c72
	c73
	c74
	c75
	c76
	c77
	c78
	c79
	c80
	c81
	c82
	c83
	c84
	c85
	c86
	c87
	c88
	c89
	c90
	c91
	c92
	c93
	c94
	c95
	c96
	c97
	c98
	g0
	g1
	g2
	g3
	g4
	g5
	g6
	g7
	g8
	g9
	g10
	g11
	g12
	g13
	g14
	g15
	g16
	g17
	g18
	g19
	g20
	g21
	g22
	g23
	g24
	g25
	g26
	g27
	g28
	g29
	g30
	g31
	g32
	g33
	g34
	g35
	g36
	g37
	g38
	g39
	g40
	g41
	g42
	g43
	g44
	g45
	g46
	g47
	g48
	g49
	g50
	g51
	g52
	g53
	g54
	g55
	g56
	g57
	g58
	g59
	g60
	g61
	g62
	g63
	g64
	g65
	g66
	g67
	g68
	g69
	g70
	g71
	g72
	g73
	g74
	g75
	g76
	g77
	g78
	g79
	g80
	g81
	g82
	g83
	g84
	g85
	g86
	g87
	g88
	g89
	g90
	g91
	g92
	g93
	g94
	g95
	g96
	g97
	g98
	goal_tile
	d0
	d1
	d2
	d3
	d4
	d5
	d6
	d7
	d8
	d9
	d10
	d11
	d12
	d13
	d14
	d15
	d16
	d17
	d18
	d19
	d20
	d21
	d22
	d23
	d24
	d25
	d26
	d27
	d28
	d29
	d30
	d31
	d32
	d33
	d34
	d35
	d36
	d37
	d38
	d39
	d40
	d41
	d42
	d43
	d44
	d45
	d46
	d47
	d48
	d49
	d50
	d51
	d52
	d53
	d54
	d55
	d56
	d57
	d58
	d59
	d60
	d61
	d62
	d63
	d64
	d65
	d66
	d67
	d68
	d69
	d70
	d71
	d72
	d73
	d74
	d75
	d76
	d77
	d78
	d79
	d80
	d81
	d82
	d83
	d84
	d85
	d86
	d87
	d88
	d89
	d90
	d91
	d92
	d93
	d94
	d95
	d96
	d97
	d98
	d99
	)
(:init
	(empty start_tile)
	(empty c0)
	(empty c1)
	(empty c2)
	(empty c3)
	(empty c4)
	(empty c5)
	(empty c6)
	(empty c7)
	(empty c8)
	(empty c9)
	(empty c10)
	(empty c11)
	(empty c12)
	(empty c13)
	(empty c14)
	(empty c15)
	(empty c16)
	(empty c17)
	(empty c18)
	(empty c19)
	(empty c20)
	(empty c21)
	(empty c22)
	(empty c23)
	(empty c24)
	(empty c25)
	(empty c26)
	(empty c27)
	(empty c28)
	(empty c29)
	(empty c30)
	(empty c31)
	(empty c32)
	(empty c33)
	(empty c34)
	(empty c35)
	(empty c36)
	(empty c37)
	(empty c38)
	(empty c39)
	(empty c40)
	(empty c41)
	(empty c42)
	(empty c43)
	(empty c44)
	(empty c45)
	(empty c46)
	(empty c47)
	(empty c48)
	(empty c49)
	(empty c50)
	(empty c51)
	(empty c52)
	(empty c53)
	(empty c54)
	(empty c55)
	(empty c56)
	(empty c57)
	(empty c58)
	(empty c59)
	(empty c60)
	(empty c61)
	(empty c62)
	(empty c63)
	(empty c64)
	(empty c65)
	(empty c66)
	(empty c67)
	(empty c68)
	(empty c69)
	(empty c70)
	(empty c71)
	(empty c72)
	(empty c73)
	(empty c74)
	(empty c75)
	(empty c76)
	(empty c77)
	(empty c78)
	(empty c79)
	(empty c80)
	(empty c81)
	(empty c82)
	(empty c83)
	(empty c84)
	(empty c85)
	(empty c86)
	(empty c87)
	(empty c88)
	(empty c89)
	(empty c90)
	(empty c91)
	(empty c92)
	(empty c93)
	(empty c94)
	(empty c95)
	(empty c96)
	(empty c97)
	(empty c98)
	(empty g0)
	(empty g1)
	(empty g2)
	(empty g3)
	(empty g4)
	(empty g5)
	(empty g6)
	(empty g7)
	(empty g8)
	(empty g9)
	(empty g10)
	(empty g11)
	(empty g12)
	(empty g13)
	(empty g14)
	(empty g15)
	(empty g16)
	(empty g17)
	(empty g18)
	(empty g19)
	(empty g20)
	(empty g21)
	(empty g22)
	(empty g23)
	(empty g24)
	(empty g25)
	(empty g26)
	(empty g27)
	(empty g28)
	(empty g29)
	(empty g30)
	(empty g31)
	(empty g32)
	(empty g33)
	(empty g34)
	(empty g35)
	(empty g36)
	(empty g37)
	(empty g38)
	(empty g39)
	(empty g40)
	(empty g41)
	(empty g42)
	(empty g43)
	(empty g44)
	(empty g45)
	(empty g46)
	(empty g47)
	(empty g48)
	(empty g49)
	(empty g50)
	(empty g51)
	(empty g52)
	(empty g53)
	(empty g54)
	(empty g55)
	(empty g56)
	(empty g57)
	(empty g58)
	(empty g59)
	(empty g60)
	(empty g61)
	(empty g62)
	(empty g63)
	(empty g64)
	(empty g65)
	(empty g66)
	(empty g67)
	(empty g68)
	(empty g69)
	(empty g70)
	(empty g71)
	(empty g72)
	(empty g73)
	(empty g74)
	(empty g75)
	(empty g76)
	(empty g77)
	(empty g78)
	(empty g79)
	(empty g80)
	(empty g81)
	(empty g82)
	(empty g83)
	(empty g84)
	(empty g85)
	(empty g86)
	(empty g87)
	(empty g88)
	(empty g89)
	(empty g90)
	(empty g91)
	(empty g92)
	(empty g93)
	(empty g94)
	(empty g95)
	(empty g96)
	(empty g97)
	(empty g98)
	(empty goal_tile)
	(empty d0)
	(empty d1)
	(empty d2)
	(empty d3)
	(empty d4)
	(empty d5)
	(empty d6)
	(empty d7)
	(empty d8)
	(empty d9)
	(empty d10)
	(empty d11)
	(empty d12)
	(empty d13)
	(empty d14)
	(empty d15)
	(empty d16)
	(empty d17)
	(empty d18)
	(empty d19)
	(empty d20)
	(empty d21)
	(empty d22)
	(empty d23)
	(empty d24)
	(empty d25)
	(empty d26)
	(empty d27)
	(empty d28)
	(empty d29)
	(empty d30)
	(empty d31)
	(empty d32)
	(empty d33)
	(empty d34)
	(empty d35)
	(empty d36)
	(empty d37)
	(empty d38)
	(empty d39)
	(empty d40)
	(empty d41)
	(empty d42)
	(empty d43)
	(empty d44)
	(empty d45)
	(empty d46)
	(empty d47)
	(empty d48)
	(empty d49)
	(empty d50)
	(empty d51)
	(empty d52)
	(empty d53)
	(empty d54)
	(empty d55)
	(empty d56)
	(empty d57)
	(empty d58)
	(empty d59)
	(empty d60)
	(empty d61)
	(empty d62)
	(empty d63)
	(empty d64)
	(empty d65)
	(empty d66)
	(empty d67)
	(empty d68)
	(empty d69)
	(empty d70)
	(empty d71)
	(empty d72)
	(empty d73)
	(empty d74)
	(empty d75)
	(empty d76)
	(empty d77)
	(empty d78)
	(empty d79)
	(empty d80)
	(empty d81)
	(empty d82)
	(empty d83)
	(empty d84)
	(empty d85)
	(empty d86)
	(empty d87)
	(empty d88)
	(empty d89)
	(empty d90)
	(empty d91)
	(empty d92)
	(empty d93)
	(empty d94)
	(empty d95)
	(empty d96)
	(empty d97)
	(empty d98)
	(empty d99)
	(east start_tile c0)
	(west c0 start_tile)
	(east c0 c1)
	(west c1 c0)
	(east c1 c2)
	(west c2 c1)
	(east c2 c3)
	(west c3 c2)
	(east c3 c4)
	(west c4 c3)
	(east c4 c5)
	(west c5 c4)
	(east c5 c6)
	(west c6 c5)
	(east c6 c7)
	(west c7 c6)
	(east c7 c8)
	(west c8 c7)
	(east c8 c9)
	(west c9 c8)
	(east c9 c10)
	(west c10 c9)
	(east c10 c11)
	(west c11 c10)
	(east c11 c12)
	(west c12 c11)
	(east c12 c13)
	(west c13 c12)
	(east c13 c14)
	(west c14 c13)
	(east c14 c15)
	(west c15 c14)
	(east c15 c16)
	(west c16 c15)
	(east c16 c17)
	(west c17 c16)
	(east c17 c18)
	(west c18 c17)
	(east c18 c19)
	(west c19 c18)
	(east c19 c20)
	(west c20 c19)
	(east c20 c21)
	(west c21 c20)
	(east c21 c22)
	(west c22 c21)
	(east c22 c23)
	(west c23 c22)
	(east c23 c24)
	(west c24 c23)
	(east c24 c25)
	(west c25 c24)
	(east c25 c26)
	(west c26 c25)
	(east c26 c27)
	(west c27 c26)
	(east c27 c28)
	(west c28 c27)
	(east c28 c29)
	(west c29 c28)
	(east c29 c30)
	(west c30 c29)
	(east c30 c31)
	(west c31 c30)
	(east c31 c32)
	(west c32 c31)
	(east c32 c33)
	(west c33 c32)
	(east c33 c34)
	(west c34 c33)
	(east c34 c35)
	(west c35 c34)
	(east c35 c36)
	(west c36 c35)
	(east c36 c37)
	(west c37 c36)
	(east c37 c38)
	(west c38 c37)
	(east c38 c39)
	(west c39 c38)
	(east c39 c40)
	(west c40 c39)
	(east c40 c41)
	(west c41 c40)
	(east c41 c42)
	(west c42 c41)
	(east c42 c43)
	(west c43 c42)
	(east c43 c44)
	(west c44 c43)
	(east c44 c45)
	(west c45 c44)
	(east c45 c46)
	(west c46 c45)
	(east c46 c47)
	(west c47 c46)
	(east c47 c48)
	(west c48 c47)
	(east c48 c49)
	(west c49 c48)
	(east c49 c50)
	(west c50 c49)
	(east c50 c51)
	(west c51 c50)
	(east c51 c52)
	(west c52 c51)
	(east c52 c53)
	(west c53 c52)
	(east c53 c54)
	(west c54 c53)
	(east c54 c55)
	(west c55 c54)
	(east c55 c56)
	(west c56 c55)
	(east c56 c57)
	(west c57 c56)
	(east c57 c58)
	(west c58 c57)
	(east c58 c59)
	(west c59 c58)
	(east c59 c60)
	(west c60 c59)
	(east c60 c61)
	(west c61 c60)
	(east c61 c62)
	(west c62 c61)
	(east c62 c63)
	(west c63 c62)
	(east c63 c64)
	(west c64 c63)
	(east c64 c65)
	(west c65 c64)
	(east c65 c66)
	(west c66 c65)
	(east c66 c67)
	(west c67 c66)
	(east c67 c68)
	(west c68 c67)
	(east c68 c69)
	(west c69 c68)
	(east c69 c70)
	(west c70 c69)
	(east c70 c71)
	(west c71 c70)
	(east c71 c72)
	(west c72 c71)
	(east c72 c73)
	(west c73 c72)
	(east c73 c74)
	(west c74 c73)
	(east c74 c75)
	(west c75 c74)
	(east c75 c76)
	(west c76 c75)
	(east c76 c77)
	(west c77 c76)
	(east c77 c78)
	(west c78 c77)
	(east c78 c79)
	(west c79 c78)
	(east c79 c80)
	(west c80 c79)
	(east c80 c81)
	(west c81 c80)
	(east c81 c82)
	(west c82 c81)
	(east c82 c83)
	(west c83 c82)
	(east c83 c84)
	(west c84 c83)
	(east c84 c85)
	(west c85 c84)
	(east c85 c86)
	(west c86 c85)
	(east c86 c87)
	(west c87 c86)
	(east c87 c88)
	(west c88 c87)
	(east c88 c89)
	(west c89 c88)
	(east c89 c90)
	(west c90 c89)
	(east c90 c91)
	(west c91 c90)
	(east c91 c92)
	(west c92 c91)
	(east c92 c93)
	(west c93 c92)
	(east c93 c94)
	(west c94 c93)
	(east c94 c95)
	(west c95 c94)
	(east c95 c96)
	(west c96 c95)
	(east c96 c97)
	(west c97 c96)
	(east c97 c98)
	(west c98 c97)
	(north g0 g1)
	(south g1 g0)
	(north g1 g2)
	(south g2 g1)
	(north g2 g3)
	(south g3 g2)
	(north g3 g4)
	(south g4 g3)
	(north g4 g5)
	(south g5 g4)
	(north g5 g6)
	(south g6 g5)
	(north g6 g7)
	(south g7 g6)
	(north g7 g8)
	(south g8 g7)
	(north g8 g9)
	(south g9 g8)
	(north g9 g10)
	(south g10 g9)
	(north g10 g11)
	(south g11 g10)
	(north g11 g12)
	(south g12 g11)
	(north g12 g13)
	(south g13 g12)
	(north g13 g14)
	(south g14 g13)
	(north g14 g15)
	(south g15 g14)
	(north g15 g16)
	(south g16 g15)
	(north g16 g17)
	(south g17 g16)
	(north g17 g18)
	(south g18 g17)
	(north g18 g19)
	(south g19 g18)
	(north g19 g20)
	(south g20 g19)
	(north g20 g21)
	(south g21 g20)
	(north g21 g22)
	(south g22 g21)
	(north g22 g23)
	(south g23 g22)
	(north g23 g24)
	(south g24 g23)
	(north g24 g25)
	(south g25 g24)
	(north g25 g26)
	(south g26 g25)
	(north g26 g27)
	(south g27 g26)
	(north g27 g28)
	(south g28 g27)
	(north g28 g29)
	(south g29 g28)
	(north g29 g30)
	(south g30 g29)
	(north g30 g31)
	(south g31 g30)
	(north g31 g32)
	(south g32 g31)
	(north g32 g33)
	(south g33 g32)
	(north g33 g34)
	(south g34 g33)
	(north g34 g35)
	(south g35 g34)
	(north g35 g36)
	(south g36 g35)
	(north g36 g37)
	(south g37 g36)
	(north g37 g38)
	(south g38 g37)
	(north g38 g39)
	(south g39 g38)
	(north g39 g40)
	(south g40 g39)
	(north g40 g41)
	(south g41 g40)
	(north g41 g42)
	(south g42 g41)
	(north g42 g43)
	(south g43 g42)
	(north g43 g44)
	(south g44 g43)
	(north g44 g45)
	(south g45 g44)
	(north g45 g46)
	(south g46 g45)
	(north g46 g47)
	(south g47 g46)
	(north g47 g48)
	(south g48 g47)
	(north g48 g49)
	(south g49 g48)
	(north g49 g50)
	(south g50 g49)
	(north g50 g51)
	(south g51 g50)
	(north g51 g52)
	(south g52 g51)
	(north g52 g53)
	(south g53 g52)
	(north g53 g54)
	(south g54 g53)
	(north g54 g55)
	(south g55 g54)
	(north g55 g56)
	(south g56 g55)
	(north g56 g57)
	(south g57 g56)
	(north g57 g58)
	(south g58 g57)
	(north g58 g59)
	(south g59 g58)
	(north g59 g60)
	(south g60 g59)
	(north g60 g61)
	(south g61 g60)
	(north g61 g62)
	(south g62 g61)
	(north g62 g63)
	(south g63 g62)
	(north g63 g64)
	(south g64 g63)
	(north g64 g65)
	(south g65 g64)
	(north g65 g66)
	(south g66 g65)
	(north g66 g67)
	(south g67 g66)
	(north g67 g68)
	(south g68 g67)
	(north g68 g69)
	(south g69 g68)
	(north g69 g70)
	(south g70 g69)
	(north g70 g71)
	(south g71 g70)
	(north g71 g72)
	(south g72 g71)
	(north g72 g73)
	(south g73 g72)
	(north g73 g74)
	(south g74 g73)
	(north g74 g75)
	(south g75 g74)
	(north g75 g76)
	(south g76 g75)
	(north g76 g77)
	(south g77 g76)
	(north g77 g78)
	(south g78 g77)
	(north g78 g79)
	(south g79 g78)
	(north g79 g80)
	(south g80 g79)
	(north g80 g81)
	(south g81 g80)
	(north g81 g82)
	(south g82 g81)
	(north g82 g83)
	(south g83 g82)
	(north g83 g84)
	(south g84 g83)
	(north g84 g85)
	(south g85 g84)
	(north g85 g86)
	(south g86 g85)
	(north g86 g87)
	(south g87 g86)
	(north g87 g88)
	(south g88 g87)
	(north g88 g89)
	(south g89 g88)
	(north g89 g90)
	(south g90 g89)
	(north g90 g91)
	(south g91 g90)
	(north g91 g92)
	(south g92 g91)
	(north g92 g93)
	(south g93 g92)
	(north g93 g94)
	(south g94 g93)
	(north g94 g95)
	(south g95 g94)
	(north g95 g96)
	(south g96 g95)
	(north g96 g97)
	(south g97 g96)
	(north g97 g98)
	(south g98 g97)
	(north g98 goal_tile)
	(south goal_tile g98)
	(south start_tile c0)
	(north c0 start_tile)
	(south c0 c1)
	(north c1 c0)
	(south c1 c2)
	(north c2 c1)
	(south c2 c3)
	(north c3 c2)
	(south c3 c4)
	(north c4 c3)
	(south c4 c5)
	(north c5 c4)
	(south c5 c6)
	(north c6 c5)
	(south c6 c7)
	(north c7 c6)
	(south c7 c8)
	(north c8 c7)
	(south c8 c9)
	(north c9 c8)
	(south c9 c10)
	(north c10 c9)
	(south c10 c11)
	(north c11 c10)
	(south c11 c12)
	(north c12 c11)
	(south c12 c13)
	(north c13 c12)
	(south c13 c14)
	(north c14 c13)
	(south c14 c15)
	(north c15 c14)
	(south c15 c16)
	(north c16 c15)
	(south c16 c17)
	(north c17 c16)
	(south c17 c18)
	(north c18 c17)
	(south c18 c19)
	(north c19 c18)
	(south c19 c20)
	(north c20 c19)
	(south c20 c21)
	(north c21 c20)
	(south c21 c22)
	(north c22 c21)
	(south c22 c23)
	(north c23 c22)
	(south c23 c24)
	(north c24 c23)
	(south c24 c25)
	(north c25 c24)
	(south c25 c26)
	(north c26 c25)
	(south c26 c27)
	(north c27 c26)
	(south c27 c28)
	(north c28 c27)
	(south c28 c29)
	(north c29 c28)
	(south c29 c30)
	(north c30 c29)
	(south c30 c31)
	(north c31 c30)
	(south c31 c32)
	(north c32 c31)
	(south c32 c33)
	(north c33 c32)
	(south c33 c34)
	(north c34 c33)
	(south c34 c35)
	(north c35 c34)
	(south c35 c36)
	(north c36 c35)
	(south c36 c37)
	(north c37 c36)
	(south c37 c38)
	(north c38 c37)
	(south c38 c39)
	(north c39 c38)
	(south c39 c40)
	(north c40 c39)
	(south c40 c41)
	(north c41 c40)
	(south c41 c42)
	(north c42 c41)
	(south c42 c43)
	(north c43 c42)
	(south c43 c44)
	(north c44 c43)
	(south c44 c45)
	(north c45 c44)
	(south c45 c46)
	(north c46 c45)
	(south c46 c47)
	(north c47 c46)
	(south c47 c48)
	(north c48 c47)
	(south c48 c49)
	(north c49 c48)
	(south c49 c50)
	(north c50 c49)
	(south c50 c51)
	(north c51 c50)
	(south c51 c52)
	(north c52 c51)
	(south c52 c53)
	(north c53 c52)
	(south c53 c54)
	(north c54 c53)
	(south c54 c55)
	(north c55 c54)
	(south c55 c56)
	(north c56 c55)
	(south c56 c57)
	(north c57 c56)
	(south c57 c58)
	(north c58 c57)
	(south c58 c59)
	(north c59 c58)
	(south c59 c60)
	(north c60 c59)
	(south c60 c61)
	(north c61 c60)
	(south c61 c62)
	(north c62 c61)
	(south c62 c63)
	(north c63 c62)
	(south c63 c64)
	(north c64 c63)
	(south c64 c65)
	(north c65 c64)
	(south c65 c66)
	(north c66 c65)
	(south c66 c67)
	(north c67 c66)
	(south c67 c68)
	(north c68 c67)
	(south c68 c69)
	(north c69 c68)
	(south c69 c70)
	(north c70 c69)
	(south c70 c71)
	(north c71 c70)
	(south c71 c72)
	(north c72 c71)
	(south c72 c73)
	(north c73 c72)
	(south c73 c74)
	(north c74 c73)
	(south c74 c75)
	(north c75 c74)
	(south c75 c76)
	(north c76 c75)
	(south c76 c77)
	(north c77 c76)
	(south c77 c78)
	(north c78 c77)
	(south c78 c79)
	(north c79 c78)
	(south c79 c80)
	(north c80 c79)
	(south c80 c81)
	(north c81 c80)
	(south c81 c82)
	(north c82 c81)
	(south c82 c83)
	(north c83 c82)
	(south c83 c84)
	(north c84 c83)
	(south c84 c85)
	(north c85 c84)
	(south c85 c86)
	(north c86 c85)
	(south c86 c87)
	(north c87 c86)
	(south c87 c88)
	(north c88 c87)
	(south c88 c89)
	(north c89 c88)
	(south c89 c90)
	(north c90 c89)
	(south c90 c91)
	(north c91 c90)
	(south c91 c92)
	(north c92 c91)
	(south c92 c93)
	(north c93 c92)
	(south c93 c94)
	(north c94 c93)
	(south c94 c95)
	(north c95 c94)
	(south c95 c96)
	(north c96 c95)
	(south c96 c97)
	(north c97 c96)
	(south c97 c98)
	(north c98 c97)
	(north c98 g0)
	(south g0 c98)
	(south c98 d0)
	(north d0 c98)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
