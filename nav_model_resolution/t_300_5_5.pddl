
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
	c99
	c100
	c101
	c102
	c103
	c104
	c105
	c106
	c107
	c108
	c109
	c110
	c111
	c112
	c113
	c114
	c115
	c116
	c117
	c118
	c119
	c120
	c121
	c122
	c123
	c124
	c125
	c126
	c127
	c128
	c129
	c130
	c131
	c132
	c133
	c134
	c135
	c136
	c137
	c138
	c139
	c140
	c141
	c142
	c143
	c144
	c145
	c146
	c147
	c148
	c149
	c150
	c151
	c152
	c153
	c154
	c155
	c156
	c157
	c158
	c159
	c160
	c161
	c162
	c163
	c164
	c165
	c166
	c167
	c168
	c169
	c170
	c171
	c172
	c173
	c174
	c175
	c176
	c177
	c178
	c179
	c180
	c181
	c182
	c183
	c184
	c185
	c186
	c187
	c188
	c189
	c190
	c191
	c192
	c193
	c194
	c195
	c196
	c197
	c198
	c199
	c200
	c201
	c202
	c203
	c204
	c205
	c206
	c207
	c208
	c209
	c210
	c211
	c212
	c213
	c214
	c215
	c216
	c217
	c218
	c219
	c220
	c221
	c222
	c223
	c224
	c225
	c226
	c227
	c228
	c229
	c230
	c231
	c232
	c233
	c234
	c235
	c236
	c237
	c238
	c239
	c240
	c241
	c242
	c243
	c244
	c245
	c246
	c247
	c248
	c249
	c250
	c251
	c252
	c253
	c254
	c255
	c256
	c257
	c258
	c259
	c260
	c261
	c262
	c263
	c264
	c265
	c266
	c267
	c268
	c269
	c270
	c271
	c272
	c273
	c274
	c275
	c276
	c277
	c278
	c279
	c280
	c281
	c282
	c283
	c284
	c285
	c286
	c287
	c288
	c289
	c290
	c291
	c292
	c293
	c294
	c295
	c296
	c297
	c298
	g0
	g1
	g2
	g3
	goal_tile
	d0
	d1
	d2
	d3
	d4
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
	(empty c99)
	(empty c100)
	(empty c101)
	(empty c102)
	(empty c103)
	(empty c104)
	(empty c105)
	(empty c106)
	(empty c107)
	(empty c108)
	(empty c109)
	(empty c110)
	(empty c111)
	(empty c112)
	(empty c113)
	(empty c114)
	(empty c115)
	(empty c116)
	(empty c117)
	(empty c118)
	(empty c119)
	(empty c120)
	(empty c121)
	(empty c122)
	(empty c123)
	(empty c124)
	(empty c125)
	(empty c126)
	(empty c127)
	(empty c128)
	(empty c129)
	(empty c130)
	(empty c131)
	(empty c132)
	(empty c133)
	(empty c134)
	(empty c135)
	(empty c136)
	(empty c137)
	(empty c138)
	(empty c139)
	(empty c140)
	(empty c141)
	(empty c142)
	(empty c143)
	(empty c144)
	(empty c145)
	(empty c146)
	(empty c147)
	(empty c148)
	(empty c149)
	(empty c150)
	(empty c151)
	(empty c152)
	(empty c153)
	(empty c154)
	(empty c155)
	(empty c156)
	(empty c157)
	(empty c158)
	(empty c159)
	(empty c160)
	(empty c161)
	(empty c162)
	(empty c163)
	(empty c164)
	(empty c165)
	(empty c166)
	(empty c167)
	(empty c168)
	(empty c169)
	(empty c170)
	(empty c171)
	(empty c172)
	(empty c173)
	(empty c174)
	(empty c175)
	(empty c176)
	(empty c177)
	(empty c178)
	(empty c179)
	(empty c180)
	(empty c181)
	(empty c182)
	(empty c183)
	(empty c184)
	(empty c185)
	(empty c186)
	(empty c187)
	(empty c188)
	(empty c189)
	(empty c190)
	(empty c191)
	(empty c192)
	(empty c193)
	(empty c194)
	(empty c195)
	(empty c196)
	(empty c197)
	(empty c198)
	(empty c199)
	(empty c200)
	(empty c201)
	(empty c202)
	(empty c203)
	(empty c204)
	(empty c205)
	(empty c206)
	(empty c207)
	(empty c208)
	(empty c209)
	(empty c210)
	(empty c211)
	(empty c212)
	(empty c213)
	(empty c214)
	(empty c215)
	(empty c216)
	(empty c217)
	(empty c218)
	(empty c219)
	(empty c220)
	(empty c221)
	(empty c222)
	(empty c223)
	(empty c224)
	(empty c225)
	(empty c226)
	(empty c227)
	(empty c228)
	(empty c229)
	(empty c230)
	(empty c231)
	(empty c232)
	(empty c233)
	(empty c234)
	(empty c235)
	(empty c236)
	(empty c237)
	(empty c238)
	(empty c239)
	(empty c240)
	(empty c241)
	(empty c242)
	(empty c243)
	(empty c244)
	(empty c245)
	(empty c246)
	(empty c247)
	(empty c248)
	(empty c249)
	(empty c250)
	(empty c251)
	(empty c252)
	(empty c253)
	(empty c254)
	(empty c255)
	(empty c256)
	(empty c257)
	(empty c258)
	(empty c259)
	(empty c260)
	(empty c261)
	(empty c262)
	(empty c263)
	(empty c264)
	(empty c265)
	(empty c266)
	(empty c267)
	(empty c268)
	(empty c269)
	(empty c270)
	(empty c271)
	(empty c272)
	(empty c273)
	(empty c274)
	(empty c275)
	(empty c276)
	(empty c277)
	(empty c278)
	(empty c279)
	(empty c280)
	(empty c281)
	(empty c282)
	(empty c283)
	(empty c284)
	(empty c285)
	(empty c286)
	(empty c287)
	(empty c288)
	(empty c289)
	(empty c290)
	(empty c291)
	(empty c292)
	(empty c293)
	(empty c294)
	(empty c295)
	(empty c296)
	(empty c297)
	(empty c298)
	(empty g0)
	(empty g1)
	(empty g2)
	(empty g3)
	(empty goal_tile)
	(empty d0)
	(empty d1)
	(empty d2)
	(empty d3)
	(empty d4)
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
	(east c98 c99)
	(west c99 c98)
	(east c99 c100)
	(west c100 c99)
	(east c100 c101)
	(west c101 c100)
	(east c101 c102)
	(west c102 c101)
	(east c102 c103)
	(west c103 c102)
	(east c103 c104)
	(west c104 c103)
	(east c104 c105)
	(west c105 c104)
	(east c105 c106)
	(west c106 c105)
	(east c106 c107)
	(west c107 c106)
	(east c107 c108)
	(west c108 c107)
	(east c108 c109)
	(west c109 c108)
	(east c109 c110)
	(west c110 c109)
	(east c110 c111)
	(west c111 c110)
	(east c111 c112)
	(west c112 c111)
	(east c112 c113)
	(west c113 c112)
	(east c113 c114)
	(west c114 c113)
	(east c114 c115)
	(west c115 c114)
	(east c115 c116)
	(west c116 c115)
	(east c116 c117)
	(west c117 c116)
	(east c117 c118)
	(west c118 c117)
	(east c118 c119)
	(west c119 c118)
	(east c119 c120)
	(west c120 c119)
	(east c120 c121)
	(west c121 c120)
	(east c121 c122)
	(west c122 c121)
	(east c122 c123)
	(west c123 c122)
	(east c123 c124)
	(west c124 c123)
	(east c124 c125)
	(west c125 c124)
	(east c125 c126)
	(west c126 c125)
	(east c126 c127)
	(west c127 c126)
	(east c127 c128)
	(west c128 c127)
	(east c128 c129)
	(west c129 c128)
	(east c129 c130)
	(west c130 c129)
	(east c130 c131)
	(west c131 c130)
	(east c131 c132)
	(west c132 c131)
	(east c132 c133)
	(west c133 c132)
	(east c133 c134)
	(west c134 c133)
	(east c134 c135)
	(west c135 c134)
	(east c135 c136)
	(west c136 c135)
	(east c136 c137)
	(west c137 c136)
	(east c137 c138)
	(west c138 c137)
	(east c138 c139)
	(west c139 c138)
	(east c139 c140)
	(west c140 c139)
	(east c140 c141)
	(west c141 c140)
	(east c141 c142)
	(west c142 c141)
	(east c142 c143)
	(west c143 c142)
	(east c143 c144)
	(west c144 c143)
	(east c144 c145)
	(west c145 c144)
	(east c145 c146)
	(west c146 c145)
	(east c146 c147)
	(west c147 c146)
	(east c147 c148)
	(west c148 c147)
	(east c148 c149)
	(west c149 c148)
	(east c149 c150)
	(west c150 c149)
	(east c150 c151)
	(west c151 c150)
	(east c151 c152)
	(west c152 c151)
	(east c152 c153)
	(west c153 c152)
	(east c153 c154)
	(west c154 c153)
	(east c154 c155)
	(west c155 c154)
	(east c155 c156)
	(west c156 c155)
	(east c156 c157)
	(west c157 c156)
	(east c157 c158)
	(west c158 c157)
	(east c158 c159)
	(west c159 c158)
	(east c159 c160)
	(west c160 c159)
	(east c160 c161)
	(west c161 c160)
	(east c161 c162)
	(west c162 c161)
	(east c162 c163)
	(west c163 c162)
	(east c163 c164)
	(west c164 c163)
	(east c164 c165)
	(west c165 c164)
	(east c165 c166)
	(west c166 c165)
	(east c166 c167)
	(west c167 c166)
	(east c167 c168)
	(west c168 c167)
	(east c168 c169)
	(west c169 c168)
	(east c169 c170)
	(west c170 c169)
	(east c170 c171)
	(west c171 c170)
	(east c171 c172)
	(west c172 c171)
	(east c172 c173)
	(west c173 c172)
	(east c173 c174)
	(west c174 c173)
	(east c174 c175)
	(west c175 c174)
	(east c175 c176)
	(west c176 c175)
	(east c176 c177)
	(west c177 c176)
	(east c177 c178)
	(west c178 c177)
	(east c178 c179)
	(west c179 c178)
	(east c179 c180)
	(west c180 c179)
	(east c180 c181)
	(west c181 c180)
	(east c181 c182)
	(west c182 c181)
	(east c182 c183)
	(west c183 c182)
	(east c183 c184)
	(west c184 c183)
	(east c184 c185)
	(west c185 c184)
	(east c185 c186)
	(west c186 c185)
	(east c186 c187)
	(west c187 c186)
	(east c187 c188)
	(west c188 c187)
	(east c188 c189)
	(west c189 c188)
	(east c189 c190)
	(west c190 c189)
	(east c190 c191)
	(west c191 c190)
	(east c191 c192)
	(west c192 c191)
	(east c192 c193)
	(west c193 c192)
	(east c193 c194)
	(west c194 c193)
	(east c194 c195)
	(west c195 c194)
	(east c195 c196)
	(west c196 c195)
	(east c196 c197)
	(west c197 c196)
	(east c197 c198)
	(west c198 c197)
	(east c198 c199)
	(west c199 c198)
	(east c199 c200)
	(west c200 c199)
	(east c200 c201)
	(west c201 c200)
	(east c201 c202)
	(west c202 c201)
	(east c202 c203)
	(west c203 c202)
	(east c203 c204)
	(west c204 c203)
	(east c204 c205)
	(west c205 c204)
	(east c205 c206)
	(west c206 c205)
	(east c206 c207)
	(west c207 c206)
	(east c207 c208)
	(west c208 c207)
	(east c208 c209)
	(west c209 c208)
	(east c209 c210)
	(west c210 c209)
	(east c210 c211)
	(west c211 c210)
	(east c211 c212)
	(west c212 c211)
	(east c212 c213)
	(west c213 c212)
	(east c213 c214)
	(west c214 c213)
	(east c214 c215)
	(west c215 c214)
	(east c215 c216)
	(west c216 c215)
	(east c216 c217)
	(west c217 c216)
	(east c217 c218)
	(west c218 c217)
	(east c218 c219)
	(west c219 c218)
	(east c219 c220)
	(west c220 c219)
	(east c220 c221)
	(west c221 c220)
	(east c221 c222)
	(west c222 c221)
	(east c222 c223)
	(west c223 c222)
	(east c223 c224)
	(west c224 c223)
	(east c224 c225)
	(west c225 c224)
	(east c225 c226)
	(west c226 c225)
	(east c226 c227)
	(west c227 c226)
	(east c227 c228)
	(west c228 c227)
	(east c228 c229)
	(west c229 c228)
	(east c229 c230)
	(west c230 c229)
	(east c230 c231)
	(west c231 c230)
	(east c231 c232)
	(west c232 c231)
	(east c232 c233)
	(west c233 c232)
	(east c233 c234)
	(west c234 c233)
	(east c234 c235)
	(west c235 c234)
	(east c235 c236)
	(west c236 c235)
	(east c236 c237)
	(west c237 c236)
	(east c237 c238)
	(west c238 c237)
	(east c238 c239)
	(west c239 c238)
	(east c239 c240)
	(west c240 c239)
	(east c240 c241)
	(west c241 c240)
	(east c241 c242)
	(west c242 c241)
	(east c242 c243)
	(west c243 c242)
	(east c243 c244)
	(west c244 c243)
	(east c244 c245)
	(west c245 c244)
	(east c245 c246)
	(west c246 c245)
	(east c246 c247)
	(west c247 c246)
	(east c247 c248)
	(west c248 c247)
	(east c248 c249)
	(west c249 c248)
	(east c249 c250)
	(west c250 c249)
	(east c250 c251)
	(west c251 c250)
	(east c251 c252)
	(west c252 c251)
	(east c252 c253)
	(west c253 c252)
	(east c253 c254)
	(west c254 c253)
	(east c254 c255)
	(west c255 c254)
	(east c255 c256)
	(west c256 c255)
	(east c256 c257)
	(west c257 c256)
	(east c257 c258)
	(west c258 c257)
	(east c258 c259)
	(west c259 c258)
	(east c259 c260)
	(west c260 c259)
	(east c260 c261)
	(west c261 c260)
	(east c261 c262)
	(west c262 c261)
	(east c262 c263)
	(west c263 c262)
	(east c263 c264)
	(west c264 c263)
	(east c264 c265)
	(west c265 c264)
	(east c265 c266)
	(west c266 c265)
	(east c266 c267)
	(west c267 c266)
	(east c267 c268)
	(west c268 c267)
	(east c268 c269)
	(west c269 c268)
	(east c269 c270)
	(west c270 c269)
	(east c270 c271)
	(west c271 c270)
	(east c271 c272)
	(west c272 c271)
	(east c272 c273)
	(west c273 c272)
	(east c273 c274)
	(west c274 c273)
	(east c274 c275)
	(west c275 c274)
	(east c275 c276)
	(west c276 c275)
	(east c276 c277)
	(west c277 c276)
	(east c277 c278)
	(west c278 c277)
	(east c278 c279)
	(west c279 c278)
	(east c279 c280)
	(west c280 c279)
	(east c280 c281)
	(west c281 c280)
	(east c281 c282)
	(west c282 c281)
	(east c282 c283)
	(west c283 c282)
	(east c283 c284)
	(west c284 c283)
	(east c284 c285)
	(west c285 c284)
	(east c285 c286)
	(west c286 c285)
	(east c286 c287)
	(west c287 c286)
	(east c287 c288)
	(west c288 c287)
	(east c288 c289)
	(west c289 c288)
	(east c289 c290)
	(west c290 c289)
	(east c290 c291)
	(west c291 c290)
	(east c291 c292)
	(west c292 c291)
	(east c292 c293)
	(west c293 c292)
	(east c293 c294)
	(west c294 c293)
	(east c294 c295)
	(west c295 c294)
	(east c295 c296)
	(west c296 c295)
	(east c296 c297)
	(west c297 c296)
	(east c297 c298)
	(west c298 c297)
	(north g0 g1)
	(south g1 g0)
	(north g1 g2)
	(south g2 g1)
	(north g2 g3)
	(south g3 g2)
	(north g3 goal_tile)
	(south goal_tile g3)
	(south d0 d1)
	(north d1 d0)
	(south d1 d2)
	(north d2 d1)
	(south d2 d3)
	(north d3 d2)
	(south d3 d4)
	(north d4 d3)
	(north c298 g0)
	(south g0 c298)
	(south c298 d0)
	(north d0 c298)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
