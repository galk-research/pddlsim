
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
	c299
	c300
	c301
	c302
	c303
	c304
	c305
	c306
	c307
	c308
	c309
	c310
	c311
	c312
	c313
	c314
	c315
	c316
	c317
	c318
	c319
	c320
	c321
	c322
	c323
	c324
	c325
	c326
	c327
	c328
	c329
	c330
	c331
	c332
	c333
	c334
	c335
	c336
	c337
	c338
	c339
	c340
	c341
	c342
	c343
	c344
	c345
	c346
	c347
	c348
	c349
	c350
	c351
	c352
	c353
	c354
	c355
	c356
	c357
	c358
	c359
	c360
	c361
	c362
	c363
	c364
	c365
	c366
	c367
	c368
	c369
	c370
	c371
	c372
	c373
	c374
	c375
	c376
	c377
	c378
	c379
	c380
	c381
	c382
	c383
	c384
	c385
	c386
	c387
	c388
	c389
	c390
	c391
	c392
	c393
	c394
	c395
	c396
	c397
	c398
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
	g99
	g100
	g101
	g102
	g103
	g104
	g105
	g106
	g107
	g108
	g109
	g110
	g111
	g112
	g113
	g114
	g115
	g116
	g117
	g118
	g119
	g120
	g121
	g122
	g123
	g124
	g125
	g126
	g127
	g128
	g129
	g130
	g131
	g132
	g133
	g134
	g135
	g136
	g137
	g138
	g139
	g140
	g141
	g142
	g143
	g144
	g145
	g146
	g147
	g148
	g149
	g150
	g151
	g152
	g153
	g154
	g155
	g156
	g157
	g158
	g159
	g160
	g161
	g162
	g163
	g164
	g165
	g166
	g167
	g168
	g169
	g170
	g171
	g172
	g173
	g174
	g175
	g176
	g177
	g178
	g179
	g180
	g181
	g182
	g183
	g184
	g185
	g186
	g187
	g188
	g189
	g190
	g191
	g192
	g193
	g194
	g195
	g196
	g197
	g198
	g199
	g200
	g201
	g202
	g203
	g204
	g205
	g206
	g207
	g208
	g209
	g210
	g211
	g212
	g213
	g214
	g215
	g216
	g217
	g218
	g219
	g220
	g221
	g222
	g223
	g224
	g225
	g226
	g227
	g228
	g229
	g230
	g231
	g232
	g233
	g234
	g235
	g236
	g237
	g238
	g239
	g240
	g241
	g242
	g243
	g244
	g245
	g246
	g247
	g248
	g249
	g250
	g251
	g252
	g253
	g254
	g255
	g256
	g257
	g258
	g259
	g260
	g261
	g262
	g263
	g264
	g265
	g266
	g267
	g268
	g269
	g270
	g271
	g272
	g273
	g274
	g275
	g276
	g277
	g278
	g279
	g280
	g281
	g282
	g283
	g284
	g285
	g286
	g287
	g288
	g289
	g290
	g291
	g292
	g293
	g294
	g295
	g296
	g297
	g298
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
	d100
	d101
	d102
	d103
	d104
	d105
	d106
	d107
	d108
	d109
	d110
	d111
	d112
	d113
	d114
	d115
	d116
	d117
	d118
	d119
	d120
	d121
	d122
	d123
	d124
	d125
	d126
	d127
	d128
	d129
	d130
	d131
	d132
	d133
	d134
	d135
	d136
	d137
	d138
	d139
	d140
	d141
	d142
	d143
	d144
	d145
	d146
	d147
	d148
	d149
	d150
	d151
	d152
	d153
	d154
	d155
	d156
	d157
	d158
	d159
	d160
	d161
	d162
	d163
	d164
	d165
	d166
	d167
	d168
	d169
	d170
	d171
	d172
	d173
	d174
	d175
	d176
	d177
	d178
	d179
	d180
	d181
	d182
	d183
	d184
	d185
	d186
	d187
	d188
	d189
	d190
	d191
	d192
	d193
	d194
	d195
	d196
	d197
	d198
	d199
	d200
	d201
	d202
	d203
	d204
	d205
	d206
	d207
	d208
	d209
	d210
	d211
	d212
	d213
	d214
	d215
	d216
	d217
	d218
	d219
	d220
	d221
	d222
	d223
	d224
	d225
	d226
	d227
	d228
	d229
	d230
	d231
	d232
	d233
	d234
	d235
	d236
	d237
	d238
	d239
	d240
	d241
	d242
	d243
	d244
	d245
	d246
	d247
	d248
	d249
	d250
	d251
	d252
	d253
	d254
	d255
	d256
	d257
	d258
	d259
	d260
	d261
	d262
	d263
	d264
	d265
	d266
	d267
	d268
	d269
	d270
	d271
	d272
	d273
	d274
	d275
	d276
	d277
	d278
	d279
	d280
	d281
	d282
	d283
	d284
	d285
	d286
	d287
	d288
	d289
	d290
	d291
	d292
	d293
	d294
	d295
	d296
	d297
	d298
	d299
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
	(empty c299)
	(empty c300)
	(empty c301)
	(empty c302)
	(empty c303)
	(empty c304)
	(empty c305)
	(empty c306)
	(empty c307)
	(empty c308)
	(empty c309)
	(empty c310)
	(empty c311)
	(empty c312)
	(empty c313)
	(empty c314)
	(empty c315)
	(empty c316)
	(empty c317)
	(empty c318)
	(empty c319)
	(empty c320)
	(empty c321)
	(empty c322)
	(empty c323)
	(empty c324)
	(empty c325)
	(empty c326)
	(empty c327)
	(empty c328)
	(empty c329)
	(empty c330)
	(empty c331)
	(empty c332)
	(empty c333)
	(empty c334)
	(empty c335)
	(empty c336)
	(empty c337)
	(empty c338)
	(empty c339)
	(empty c340)
	(empty c341)
	(empty c342)
	(empty c343)
	(empty c344)
	(empty c345)
	(empty c346)
	(empty c347)
	(empty c348)
	(empty c349)
	(empty c350)
	(empty c351)
	(empty c352)
	(empty c353)
	(empty c354)
	(empty c355)
	(empty c356)
	(empty c357)
	(empty c358)
	(empty c359)
	(empty c360)
	(empty c361)
	(empty c362)
	(empty c363)
	(empty c364)
	(empty c365)
	(empty c366)
	(empty c367)
	(empty c368)
	(empty c369)
	(empty c370)
	(empty c371)
	(empty c372)
	(empty c373)
	(empty c374)
	(empty c375)
	(empty c376)
	(empty c377)
	(empty c378)
	(empty c379)
	(empty c380)
	(empty c381)
	(empty c382)
	(empty c383)
	(empty c384)
	(empty c385)
	(empty c386)
	(empty c387)
	(empty c388)
	(empty c389)
	(empty c390)
	(empty c391)
	(empty c392)
	(empty c393)
	(empty c394)
	(empty c395)
	(empty c396)
	(empty c397)
	(empty c398)
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
	(empty g99)
	(empty g100)
	(empty g101)
	(empty g102)
	(empty g103)
	(empty g104)
	(empty g105)
	(empty g106)
	(empty g107)
	(empty g108)
	(empty g109)
	(empty g110)
	(empty g111)
	(empty g112)
	(empty g113)
	(empty g114)
	(empty g115)
	(empty g116)
	(empty g117)
	(empty g118)
	(empty g119)
	(empty g120)
	(empty g121)
	(empty g122)
	(empty g123)
	(empty g124)
	(empty g125)
	(empty g126)
	(empty g127)
	(empty g128)
	(empty g129)
	(empty g130)
	(empty g131)
	(empty g132)
	(empty g133)
	(empty g134)
	(empty g135)
	(empty g136)
	(empty g137)
	(empty g138)
	(empty g139)
	(empty g140)
	(empty g141)
	(empty g142)
	(empty g143)
	(empty g144)
	(empty g145)
	(empty g146)
	(empty g147)
	(empty g148)
	(empty g149)
	(empty g150)
	(empty g151)
	(empty g152)
	(empty g153)
	(empty g154)
	(empty g155)
	(empty g156)
	(empty g157)
	(empty g158)
	(empty g159)
	(empty g160)
	(empty g161)
	(empty g162)
	(empty g163)
	(empty g164)
	(empty g165)
	(empty g166)
	(empty g167)
	(empty g168)
	(empty g169)
	(empty g170)
	(empty g171)
	(empty g172)
	(empty g173)
	(empty g174)
	(empty g175)
	(empty g176)
	(empty g177)
	(empty g178)
	(empty g179)
	(empty g180)
	(empty g181)
	(empty g182)
	(empty g183)
	(empty g184)
	(empty g185)
	(empty g186)
	(empty g187)
	(empty g188)
	(empty g189)
	(empty g190)
	(empty g191)
	(empty g192)
	(empty g193)
	(empty g194)
	(empty g195)
	(empty g196)
	(empty g197)
	(empty g198)
	(empty g199)
	(empty g200)
	(empty g201)
	(empty g202)
	(empty g203)
	(empty g204)
	(empty g205)
	(empty g206)
	(empty g207)
	(empty g208)
	(empty g209)
	(empty g210)
	(empty g211)
	(empty g212)
	(empty g213)
	(empty g214)
	(empty g215)
	(empty g216)
	(empty g217)
	(empty g218)
	(empty g219)
	(empty g220)
	(empty g221)
	(empty g222)
	(empty g223)
	(empty g224)
	(empty g225)
	(empty g226)
	(empty g227)
	(empty g228)
	(empty g229)
	(empty g230)
	(empty g231)
	(empty g232)
	(empty g233)
	(empty g234)
	(empty g235)
	(empty g236)
	(empty g237)
	(empty g238)
	(empty g239)
	(empty g240)
	(empty g241)
	(empty g242)
	(empty g243)
	(empty g244)
	(empty g245)
	(empty g246)
	(empty g247)
	(empty g248)
	(empty g249)
	(empty g250)
	(empty g251)
	(empty g252)
	(empty g253)
	(empty g254)
	(empty g255)
	(empty g256)
	(empty g257)
	(empty g258)
	(empty g259)
	(empty g260)
	(empty g261)
	(empty g262)
	(empty g263)
	(empty g264)
	(empty g265)
	(empty g266)
	(empty g267)
	(empty g268)
	(empty g269)
	(empty g270)
	(empty g271)
	(empty g272)
	(empty g273)
	(empty g274)
	(empty g275)
	(empty g276)
	(empty g277)
	(empty g278)
	(empty g279)
	(empty g280)
	(empty g281)
	(empty g282)
	(empty g283)
	(empty g284)
	(empty g285)
	(empty g286)
	(empty g287)
	(empty g288)
	(empty g289)
	(empty g290)
	(empty g291)
	(empty g292)
	(empty g293)
	(empty g294)
	(empty g295)
	(empty g296)
	(empty g297)
	(empty g298)
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
	(empty d100)
	(empty d101)
	(empty d102)
	(empty d103)
	(empty d104)
	(empty d105)
	(empty d106)
	(empty d107)
	(empty d108)
	(empty d109)
	(empty d110)
	(empty d111)
	(empty d112)
	(empty d113)
	(empty d114)
	(empty d115)
	(empty d116)
	(empty d117)
	(empty d118)
	(empty d119)
	(empty d120)
	(empty d121)
	(empty d122)
	(empty d123)
	(empty d124)
	(empty d125)
	(empty d126)
	(empty d127)
	(empty d128)
	(empty d129)
	(empty d130)
	(empty d131)
	(empty d132)
	(empty d133)
	(empty d134)
	(empty d135)
	(empty d136)
	(empty d137)
	(empty d138)
	(empty d139)
	(empty d140)
	(empty d141)
	(empty d142)
	(empty d143)
	(empty d144)
	(empty d145)
	(empty d146)
	(empty d147)
	(empty d148)
	(empty d149)
	(empty d150)
	(empty d151)
	(empty d152)
	(empty d153)
	(empty d154)
	(empty d155)
	(empty d156)
	(empty d157)
	(empty d158)
	(empty d159)
	(empty d160)
	(empty d161)
	(empty d162)
	(empty d163)
	(empty d164)
	(empty d165)
	(empty d166)
	(empty d167)
	(empty d168)
	(empty d169)
	(empty d170)
	(empty d171)
	(empty d172)
	(empty d173)
	(empty d174)
	(empty d175)
	(empty d176)
	(empty d177)
	(empty d178)
	(empty d179)
	(empty d180)
	(empty d181)
	(empty d182)
	(empty d183)
	(empty d184)
	(empty d185)
	(empty d186)
	(empty d187)
	(empty d188)
	(empty d189)
	(empty d190)
	(empty d191)
	(empty d192)
	(empty d193)
	(empty d194)
	(empty d195)
	(empty d196)
	(empty d197)
	(empty d198)
	(empty d199)
	(empty d200)
	(empty d201)
	(empty d202)
	(empty d203)
	(empty d204)
	(empty d205)
	(empty d206)
	(empty d207)
	(empty d208)
	(empty d209)
	(empty d210)
	(empty d211)
	(empty d212)
	(empty d213)
	(empty d214)
	(empty d215)
	(empty d216)
	(empty d217)
	(empty d218)
	(empty d219)
	(empty d220)
	(empty d221)
	(empty d222)
	(empty d223)
	(empty d224)
	(empty d225)
	(empty d226)
	(empty d227)
	(empty d228)
	(empty d229)
	(empty d230)
	(empty d231)
	(empty d232)
	(empty d233)
	(empty d234)
	(empty d235)
	(empty d236)
	(empty d237)
	(empty d238)
	(empty d239)
	(empty d240)
	(empty d241)
	(empty d242)
	(empty d243)
	(empty d244)
	(empty d245)
	(empty d246)
	(empty d247)
	(empty d248)
	(empty d249)
	(empty d250)
	(empty d251)
	(empty d252)
	(empty d253)
	(empty d254)
	(empty d255)
	(empty d256)
	(empty d257)
	(empty d258)
	(empty d259)
	(empty d260)
	(empty d261)
	(empty d262)
	(empty d263)
	(empty d264)
	(empty d265)
	(empty d266)
	(empty d267)
	(empty d268)
	(empty d269)
	(empty d270)
	(empty d271)
	(empty d272)
	(empty d273)
	(empty d274)
	(empty d275)
	(empty d276)
	(empty d277)
	(empty d278)
	(empty d279)
	(empty d280)
	(empty d281)
	(empty d282)
	(empty d283)
	(empty d284)
	(empty d285)
	(empty d286)
	(empty d287)
	(empty d288)
	(empty d289)
	(empty d290)
	(empty d291)
	(empty d292)
	(empty d293)
	(empty d294)
	(empty d295)
	(empty d296)
	(empty d297)
	(empty d298)
	(empty d299)
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
	(east c298 c299)
	(west c299 c298)
	(east c299 c300)
	(west c300 c299)
	(east c300 c301)
	(west c301 c300)
	(east c301 c302)
	(west c302 c301)
	(east c302 c303)
	(west c303 c302)
	(east c303 c304)
	(west c304 c303)
	(east c304 c305)
	(west c305 c304)
	(east c305 c306)
	(west c306 c305)
	(east c306 c307)
	(west c307 c306)
	(east c307 c308)
	(west c308 c307)
	(east c308 c309)
	(west c309 c308)
	(east c309 c310)
	(west c310 c309)
	(east c310 c311)
	(west c311 c310)
	(east c311 c312)
	(west c312 c311)
	(east c312 c313)
	(west c313 c312)
	(east c313 c314)
	(west c314 c313)
	(east c314 c315)
	(west c315 c314)
	(east c315 c316)
	(west c316 c315)
	(east c316 c317)
	(west c317 c316)
	(east c317 c318)
	(west c318 c317)
	(east c318 c319)
	(west c319 c318)
	(east c319 c320)
	(west c320 c319)
	(east c320 c321)
	(west c321 c320)
	(east c321 c322)
	(west c322 c321)
	(east c322 c323)
	(west c323 c322)
	(east c323 c324)
	(west c324 c323)
	(east c324 c325)
	(west c325 c324)
	(east c325 c326)
	(west c326 c325)
	(east c326 c327)
	(west c327 c326)
	(east c327 c328)
	(west c328 c327)
	(east c328 c329)
	(west c329 c328)
	(east c329 c330)
	(west c330 c329)
	(east c330 c331)
	(west c331 c330)
	(east c331 c332)
	(west c332 c331)
	(east c332 c333)
	(west c333 c332)
	(east c333 c334)
	(west c334 c333)
	(east c334 c335)
	(west c335 c334)
	(east c335 c336)
	(west c336 c335)
	(east c336 c337)
	(west c337 c336)
	(east c337 c338)
	(west c338 c337)
	(east c338 c339)
	(west c339 c338)
	(east c339 c340)
	(west c340 c339)
	(east c340 c341)
	(west c341 c340)
	(east c341 c342)
	(west c342 c341)
	(east c342 c343)
	(west c343 c342)
	(east c343 c344)
	(west c344 c343)
	(east c344 c345)
	(west c345 c344)
	(east c345 c346)
	(west c346 c345)
	(east c346 c347)
	(west c347 c346)
	(east c347 c348)
	(west c348 c347)
	(east c348 c349)
	(west c349 c348)
	(east c349 c350)
	(west c350 c349)
	(east c350 c351)
	(west c351 c350)
	(east c351 c352)
	(west c352 c351)
	(east c352 c353)
	(west c353 c352)
	(east c353 c354)
	(west c354 c353)
	(east c354 c355)
	(west c355 c354)
	(east c355 c356)
	(west c356 c355)
	(east c356 c357)
	(west c357 c356)
	(east c357 c358)
	(west c358 c357)
	(east c358 c359)
	(west c359 c358)
	(east c359 c360)
	(west c360 c359)
	(east c360 c361)
	(west c361 c360)
	(east c361 c362)
	(west c362 c361)
	(east c362 c363)
	(west c363 c362)
	(east c363 c364)
	(west c364 c363)
	(east c364 c365)
	(west c365 c364)
	(east c365 c366)
	(west c366 c365)
	(east c366 c367)
	(west c367 c366)
	(east c367 c368)
	(west c368 c367)
	(east c368 c369)
	(west c369 c368)
	(east c369 c370)
	(west c370 c369)
	(east c370 c371)
	(west c371 c370)
	(east c371 c372)
	(west c372 c371)
	(east c372 c373)
	(west c373 c372)
	(east c373 c374)
	(west c374 c373)
	(east c374 c375)
	(west c375 c374)
	(east c375 c376)
	(west c376 c375)
	(east c376 c377)
	(west c377 c376)
	(east c377 c378)
	(west c378 c377)
	(east c378 c379)
	(west c379 c378)
	(east c379 c380)
	(west c380 c379)
	(east c380 c381)
	(west c381 c380)
	(east c381 c382)
	(west c382 c381)
	(east c382 c383)
	(west c383 c382)
	(east c383 c384)
	(west c384 c383)
	(east c384 c385)
	(west c385 c384)
	(east c385 c386)
	(west c386 c385)
	(east c386 c387)
	(west c387 c386)
	(east c387 c388)
	(west c388 c387)
	(east c388 c389)
	(west c389 c388)
	(east c389 c390)
	(west c390 c389)
	(east c390 c391)
	(west c391 c390)
	(east c391 c392)
	(west c392 c391)
	(east c392 c393)
	(west c393 c392)
	(east c393 c394)
	(west c394 c393)
	(east c394 c395)
	(west c395 c394)
	(east c395 c396)
	(west c396 c395)
	(east c396 c397)
	(west c397 c396)
	(east c397 c398)
	(west c398 c397)
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
	(north g98 g99)
	(south g99 g98)
	(north g99 g100)
	(south g100 g99)
	(north g100 g101)
	(south g101 g100)
	(north g101 g102)
	(south g102 g101)
	(north g102 g103)
	(south g103 g102)
	(north g103 g104)
	(south g104 g103)
	(north g104 g105)
	(south g105 g104)
	(north g105 g106)
	(south g106 g105)
	(north g106 g107)
	(south g107 g106)
	(north g107 g108)
	(south g108 g107)
	(north g108 g109)
	(south g109 g108)
	(north g109 g110)
	(south g110 g109)
	(north g110 g111)
	(south g111 g110)
	(north g111 g112)
	(south g112 g111)
	(north g112 g113)
	(south g113 g112)
	(north g113 g114)
	(south g114 g113)
	(north g114 g115)
	(south g115 g114)
	(north g115 g116)
	(south g116 g115)
	(north g116 g117)
	(south g117 g116)
	(north g117 g118)
	(south g118 g117)
	(north g118 g119)
	(south g119 g118)
	(north g119 g120)
	(south g120 g119)
	(north g120 g121)
	(south g121 g120)
	(north g121 g122)
	(south g122 g121)
	(north g122 g123)
	(south g123 g122)
	(north g123 g124)
	(south g124 g123)
	(north g124 g125)
	(south g125 g124)
	(north g125 g126)
	(south g126 g125)
	(north g126 g127)
	(south g127 g126)
	(north g127 g128)
	(south g128 g127)
	(north g128 g129)
	(south g129 g128)
	(north g129 g130)
	(south g130 g129)
	(north g130 g131)
	(south g131 g130)
	(north g131 g132)
	(south g132 g131)
	(north g132 g133)
	(south g133 g132)
	(north g133 g134)
	(south g134 g133)
	(north g134 g135)
	(south g135 g134)
	(north g135 g136)
	(south g136 g135)
	(north g136 g137)
	(south g137 g136)
	(north g137 g138)
	(south g138 g137)
	(north g138 g139)
	(south g139 g138)
	(north g139 g140)
	(south g140 g139)
	(north g140 g141)
	(south g141 g140)
	(north g141 g142)
	(south g142 g141)
	(north g142 g143)
	(south g143 g142)
	(north g143 g144)
	(south g144 g143)
	(north g144 g145)
	(south g145 g144)
	(north g145 g146)
	(south g146 g145)
	(north g146 g147)
	(south g147 g146)
	(north g147 g148)
	(south g148 g147)
	(north g148 g149)
	(south g149 g148)
	(north g149 g150)
	(south g150 g149)
	(north g150 g151)
	(south g151 g150)
	(north g151 g152)
	(south g152 g151)
	(north g152 g153)
	(south g153 g152)
	(north g153 g154)
	(south g154 g153)
	(north g154 g155)
	(south g155 g154)
	(north g155 g156)
	(south g156 g155)
	(north g156 g157)
	(south g157 g156)
	(north g157 g158)
	(south g158 g157)
	(north g158 g159)
	(south g159 g158)
	(north g159 g160)
	(south g160 g159)
	(north g160 g161)
	(south g161 g160)
	(north g161 g162)
	(south g162 g161)
	(north g162 g163)
	(south g163 g162)
	(north g163 g164)
	(south g164 g163)
	(north g164 g165)
	(south g165 g164)
	(north g165 g166)
	(south g166 g165)
	(north g166 g167)
	(south g167 g166)
	(north g167 g168)
	(south g168 g167)
	(north g168 g169)
	(south g169 g168)
	(north g169 g170)
	(south g170 g169)
	(north g170 g171)
	(south g171 g170)
	(north g171 g172)
	(south g172 g171)
	(north g172 g173)
	(south g173 g172)
	(north g173 g174)
	(south g174 g173)
	(north g174 g175)
	(south g175 g174)
	(north g175 g176)
	(south g176 g175)
	(north g176 g177)
	(south g177 g176)
	(north g177 g178)
	(south g178 g177)
	(north g178 g179)
	(south g179 g178)
	(north g179 g180)
	(south g180 g179)
	(north g180 g181)
	(south g181 g180)
	(north g181 g182)
	(south g182 g181)
	(north g182 g183)
	(south g183 g182)
	(north g183 g184)
	(south g184 g183)
	(north g184 g185)
	(south g185 g184)
	(north g185 g186)
	(south g186 g185)
	(north g186 g187)
	(south g187 g186)
	(north g187 g188)
	(south g188 g187)
	(north g188 g189)
	(south g189 g188)
	(north g189 g190)
	(south g190 g189)
	(north g190 g191)
	(south g191 g190)
	(north g191 g192)
	(south g192 g191)
	(north g192 g193)
	(south g193 g192)
	(north g193 g194)
	(south g194 g193)
	(north g194 g195)
	(south g195 g194)
	(north g195 g196)
	(south g196 g195)
	(north g196 g197)
	(south g197 g196)
	(north g197 g198)
	(south g198 g197)
	(north g198 g199)
	(south g199 g198)
	(north g199 g200)
	(south g200 g199)
	(north g200 g201)
	(south g201 g200)
	(north g201 g202)
	(south g202 g201)
	(north g202 g203)
	(south g203 g202)
	(north g203 g204)
	(south g204 g203)
	(north g204 g205)
	(south g205 g204)
	(north g205 g206)
	(south g206 g205)
	(north g206 g207)
	(south g207 g206)
	(north g207 g208)
	(south g208 g207)
	(north g208 g209)
	(south g209 g208)
	(north g209 g210)
	(south g210 g209)
	(north g210 g211)
	(south g211 g210)
	(north g211 g212)
	(south g212 g211)
	(north g212 g213)
	(south g213 g212)
	(north g213 g214)
	(south g214 g213)
	(north g214 g215)
	(south g215 g214)
	(north g215 g216)
	(south g216 g215)
	(north g216 g217)
	(south g217 g216)
	(north g217 g218)
	(south g218 g217)
	(north g218 g219)
	(south g219 g218)
	(north g219 g220)
	(south g220 g219)
	(north g220 g221)
	(south g221 g220)
	(north g221 g222)
	(south g222 g221)
	(north g222 g223)
	(south g223 g222)
	(north g223 g224)
	(south g224 g223)
	(north g224 g225)
	(south g225 g224)
	(north g225 g226)
	(south g226 g225)
	(north g226 g227)
	(south g227 g226)
	(north g227 g228)
	(south g228 g227)
	(north g228 g229)
	(south g229 g228)
	(north g229 g230)
	(south g230 g229)
	(north g230 g231)
	(south g231 g230)
	(north g231 g232)
	(south g232 g231)
	(north g232 g233)
	(south g233 g232)
	(north g233 g234)
	(south g234 g233)
	(north g234 g235)
	(south g235 g234)
	(north g235 g236)
	(south g236 g235)
	(north g236 g237)
	(south g237 g236)
	(north g237 g238)
	(south g238 g237)
	(north g238 g239)
	(south g239 g238)
	(north g239 g240)
	(south g240 g239)
	(north g240 g241)
	(south g241 g240)
	(north g241 g242)
	(south g242 g241)
	(north g242 g243)
	(south g243 g242)
	(north g243 g244)
	(south g244 g243)
	(north g244 g245)
	(south g245 g244)
	(north g245 g246)
	(south g246 g245)
	(north g246 g247)
	(south g247 g246)
	(north g247 g248)
	(south g248 g247)
	(north g248 g249)
	(south g249 g248)
	(north g249 g250)
	(south g250 g249)
	(north g250 g251)
	(south g251 g250)
	(north g251 g252)
	(south g252 g251)
	(north g252 g253)
	(south g253 g252)
	(north g253 g254)
	(south g254 g253)
	(north g254 g255)
	(south g255 g254)
	(north g255 g256)
	(south g256 g255)
	(north g256 g257)
	(south g257 g256)
	(north g257 g258)
	(south g258 g257)
	(north g258 g259)
	(south g259 g258)
	(north g259 g260)
	(south g260 g259)
	(north g260 g261)
	(south g261 g260)
	(north g261 g262)
	(south g262 g261)
	(north g262 g263)
	(south g263 g262)
	(north g263 g264)
	(south g264 g263)
	(north g264 g265)
	(south g265 g264)
	(north g265 g266)
	(south g266 g265)
	(north g266 g267)
	(south g267 g266)
	(north g267 g268)
	(south g268 g267)
	(north g268 g269)
	(south g269 g268)
	(north g269 g270)
	(south g270 g269)
	(north g270 g271)
	(south g271 g270)
	(north g271 g272)
	(south g272 g271)
	(north g272 g273)
	(south g273 g272)
	(north g273 g274)
	(south g274 g273)
	(north g274 g275)
	(south g275 g274)
	(north g275 g276)
	(south g276 g275)
	(north g276 g277)
	(south g277 g276)
	(north g277 g278)
	(south g278 g277)
	(north g278 g279)
	(south g279 g278)
	(north g279 g280)
	(south g280 g279)
	(north g280 g281)
	(south g281 g280)
	(north g281 g282)
	(south g282 g281)
	(north g282 g283)
	(south g283 g282)
	(north g283 g284)
	(south g284 g283)
	(north g284 g285)
	(south g285 g284)
	(north g285 g286)
	(south g286 g285)
	(north g286 g287)
	(south g287 g286)
	(north g287 g288)
	(south g288 g287)
	(north g288 g289)
	(south g289 g288)
	(north g289 g290)
	(south g290 g289)
	(north g290 g291)
	(south g291 g290)
	(north g291 g292)
	(south g292 g291)
	(north g292 g293)
	(south g293 g292)
	(north g293 g294)
	(south g294 g293)
	(north g294 g295)
	(south g295 g294)
	(north g295 g296)
	(south g296 g295)
	(north g296 g297)
	(south g297 g296)
	(north g297 g298)
	(south g298 g297)
	(north g298 goal_tile)
	(south goal_tile g298)
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
	(south c98 c99)
	(north c99 c98)
	(south c99 c100)
	(north c100 c99)
	(south c100 c101)
	(north c101 c100)
	(south c101 c102)
	(north c102 c101)
	(south c102 c103)
	(north c103 c102)
	(south c103 c104)
	(north c104 c103)
	(south c104 c105)
	(north c105 c104)
	(south c105 c106)
	(north c106 c105)
	(south c106 c107)
	(north c107 c106)
	(south c107 c108)
	(north c108 c107)
	(south c108 c109)
	(north c109 c108)
	(south c109 c110)
	(north c110 c109)
	(south c110 c111)
	(north c111 c110)
	(south c111 c112)
	(north c112 c111)
	(south c112 c113)
	(north c113 c112)
	(south c113 c114)
	(north c114 c113)
	(south c114 c115)
	(north c115 c114)
	(south c115 c116)
	(north c116 c115)
	(south c116 c117)
	(north c117 c116)
	(south c117 c118)
	(north c118 c117)
	(south c118 c119)
	(north c119 c118)
	(south c119 c120)
	(north c120 c119)
	(south c120 c121)
	(north c121 c120)
	(south c121 c122)
	(north c122 c121)
	(south c122 c123)
	(north c123 c122)
	(south c123 c124)
	(north c124 c123)
	(south c124 c125)
	(north c125 c124)
	(south c125 c126)
	(north c126 c125)
	(south c126 c127)
	(north c127 c126)
	(south c127 c128)
	(north c128 c127)
	(south c128 c129)
	(north c129 c128)
	(south c129 c130)
	(north c130 c129)
	(south c130 c131)
	(north c131 c130)
	(south c131 c132)
	(north c132 c131)
	(south c132 c133)
	(north c133 c132)
	(south c133 c134)
	(north c134 c133)
	(south c134 c135)
	(north c135 c134)
	(south c135 c136)
	(north c136 c135)
	(south c136 c137)
	(north c137 c136)
	(south c137 c138)
	(north c138 c137)
	(south c138 c139)
	(north c139 c138)
	(south c139 c140)
	(north c140 c139)
	(south c140 c141)
	(north c141 c140)
	(south c141 c142)
	(north c142 c141)
	(south c142 c143)
	(north c143 c142)
	(south c143 c144)
	(north c144 c143)
	(south c144 c145)
	(north c145 c144)
	(south c145 c146)
	(north c146 c145)
	(south c146 c147)
	(north c147 c146)
	(south c147 c148)
	(north c148 c147)
	(south c148 c149)
	(north c149 c148)
	(south c149 c150)
	(north c150 c149)
	(south c150 c151)
	(north c151 c150)
	(south c151 c152)
	(north c152 c151)
	(south c152 c153)
	(north c153 c152)
	(south c153 c154)
	(north c154 c153)
	(south c154 c155)
	(north c155 c154)
	(south c155 c156)
	(north c156 c155)
	(south c156 c157)
	(north c157 c156)
	(south c157 c158)
	(north c158 c157)
	(south c158 c159)
	(north c159 c158)
	(south c159 c160)
	(north c160 c159)
	(south c160 c161)
	(north c161 c160)
	(south c161 c162)
	(north c162 c161)
	(south c162 c163)
	(north c163 c162)
	(south c163 c164)
	(north c164 c163)
	(south c164 c165)
	(north c165 c164)
	(south c165 c166)
	(north c166 c165)
	(south c166 c167)
	(north c167 c166)
	(south c167 c168)
	(north c168 c167)
	(south c168 c169)
	(north c169 c168)
	(south c169 c170)
	(north c170 c169)
	(south c170 c171)
	(north c171 c170)
	(south c171 c172)
	(north c172 c171)
	(south c172 c173)
	(north c173 c172)
	(south c173 c174)
	(north c174 c173)
	(south c174 c175)
	(north c175 c174)
	(south c175 c176)
	(north c176 c175)
	(south c176 c177)
	(north c177 c176)
	(south c177 c178)
	(north c178 c177)
	(south c178 c179)
	(north c179 c178)
	(south c179 c180)
	(north c180 c179)
	(south c180 c181)
	(north c181 c180)
	(south c181 c182)
	(north c182 c181)
	(south c182 c183)
	(north c183 c182)
	(south c183 c184)
	(north c184 c183)
	(south c184 c185)
	(north c185 c184)
	(south c185 c186)
	(north c186 c185)
	(south c186 c187)
	(north c187 c186)
	(south c187 c188)
	(north c188 c187)
	(south c188 c189)
	(north c189 c188)
	(south c189 c190)
	(north c190 c189)
	(south c190 c191)
	(north c191 c190)
	(south c191 c192)
	(north c192 c191)
	(south c192 c193)
	(north c193 c192)
	(south c193 c194)
	(north c194 c193)
	(south c194 c195)
	(north c195 c194)
	(south c195 c196)
	(north c196 c195)
	(south c196 c197)
	(north c197 c196)
	(south c197 c198)
	(north c198 c197)
	(south c198 c199)
	(north c199 c198)
	(south c199 c200)
	(north c200 c199)
	(south c200 c201)
	(north c201 c200)
	(south c201 c202)
	(north c202 c201)
	(south c202 c203)
	(north c203 c202)
	(south c203 c204)
	(north c204 c203)
	(south c204 c205)
	(north c205 c204)
	(south c205 c206)
	(north c206 c205)
	(south c206 c207)
	(north c207 c206)
	(south c207 c208)
	(north c208 c207)
	(south c208 c209)
	(north c209 c208)
	(south c209 c210)
	(north c210 c209)
	(south c210 c211)
	(north c211 c210)
	(south c211 c212)
	(north c212 c211)
	(south c212 c213)
	(north c213 c212)
	(south c213 c214)
	(north c214 c213)
	(south c214 c215)
	(north c215 c214)
	(south c215 c216)
	(north c216 c215)
	(south c216 c217)
	(north c217 c216)
	(south c217 c218)
	(north c218 c217)
	(south c218 c219)
	(north c219 c218)
	(south c219 c220)
	(north c220 c219)
	(south c220 c221)
	(north c221 c220)
	(south c221 c222)
	(north c222 c221)
	(south c222 c223)
	(north c223 c222)
	(south c223 c224)
	(north c224 c223)
	(south c224 c225)
	(north c225 c224)
	(south c225 c226)
	(north c226 c225)
	(south c226 c227)
	(north c227 c226)
	(south c227 c228)
	(north c228 c227)
	(south c228 c229)
	(north c229 c228)
	(south c229 c230)
	(north c230 c229)
	(south c230 c231)
	(north c231 c230)
	(south c231 c232)
	(north c232 c231)
	(south c232 c233)
	(north c233 c232)
	(south c233 c234)
	(north c234 c233)
	(south c234 c235)
	(north c235 c234)
	(south c235 c236)
	(north c236 c235)
	(south c236 c237)
	(north c237 c236)
	(south c237 c238)
	(north c238 c237)
	(south c238 c239)
	(north c239 c238)
	(south c239 c240)
	(north c240 c239)
	(south c240 c241)
	(north c241 c240)
	(south c241 c242)
	(north c242 c241)
	(south c242 c243)
	(north c243 c242)
	(south c243 c244)
	(north c244 c243)
	(south c244 c245)
	(north c245 c244)
	(south c245 c246)
	(north c246 c245)
	(south c246 c247)
	(north c247 c246)
	(south c247 c248)
	(north c248 c247)
	(south c248 c249)
	(north c249 c248)
	(south c249 c250)
	(north c250 c249)
	(south c250 c251)
	(north c251 c250)
	(south c251 c252)
	(north c252 c251)
	(south c252 c253)
	(north c253 c252)
	(south c253 c254)
	(north c254 c253)
	(south c254 c255)
	(north c255 c254)
	(south c255 c256)
	(north c256 c255)
	(south c256 c257)
	(north c257 c256)
	(south c257 c258)
	(north c258 c257)
	(south c258 c259)
	(north c259 c258)
	(south c259 c260)
	(north c260 c259)
	(south c260 c261)
	(north c261 c260)
	(south c261 c262)
	(north c262 c261)
	(south c262 c263)
	(north c263 c262)
	(south c263 c264)
	(north c264 c263)
	(south c264 c265)
	(north c265 c264)
	(south c265 c266)
	(north c266 c265)
	(south c266 c267)
	(north c267 c266)
	(south c267 c268)
	(north c268 c267)
	(south c268 c269)
	(north c269 c268)
	(south c269 c270)
	(north c270 c269)
	(south c270 c271)
	(north c271 c270)
	(south c271 c272)
	(north c272 c271)
	(south c272 c273)
	(north c273 c272)
	(south c273 c274)
	(north c274 c273)
	(south c274 c275)
	(north c275 c274)
	(south c275 c276)
	(north c276 c275)
	(south c276 c277)
	(north c277 c276)
	(south c277 c278)
	(north c278 c277)
	(south c278 c279)
	(north c279 c278)
	(south c279 c280)
	(north c280 c279)
	(south c280 c281)
	(north c281 c280)
	(south c281 c282)
	(north c282 c281)
	(south c282 c283)
	(north c283 c282)
	(south c283 c284)
	(north c284 c283)
	(south c284 c285)
	(north c285 c284)
	(south c285 c286)
	(north c286 c285)
	(south c286 c287)
	(north c287 c286)
	(south c287 c288)
	(north c288 c287)
	(south c288 c289)
	(north c289 c288)
	(south c289 c290)
	(north c290 c289)
	(south c290 c291)
	(north c291 c290)
	(south c291 c292)
	(north c292 c291)
	(south c292 c293)
	(north c293 c292)
	(south c293 c294)
	(north c294 c293)
	(south c294 c295)
	(north c295 c294)
	(south c295 c296)
	(north c296 c295)
	(south c296 c297)
	(north c297 c296)
	(south c297 c298)
	(north c298 c297)
	(south c298 c299)
	(north c299 c298)
	(south c299 c300)
	(north c300 c299)
	(south c300 c301)
	(north c301 c300)
	(south c301 c302)
	(north c302 c301)
	(south c302 c303)
	(north c303 c302)
	(south c303 c304)
	(north c304 c303)
	(south c304 c305)
	(north c305 c304)
	(south c305 c306)
	(north c306 c305)
	(south c306 c307)
	(north c307 c306)
	(south c307 c308)
	(north c308 c307)
	(south c308 c309)
	(north c309 c308)
	(south c309 c310)
	(north c310 c309)
	(south c310 c311)
	(north c311 c310)
	(south c311 c312)
	(north c312 c311)
	(south c312 c313)
	(north c313 c312)
	(south c313 c314)
	(north c314 c313)
	(south c314 c315)
	(north c315 c314)
	(south c315 c316)
	(north c316 c315)
	(south c316 c317)
	(north c317 c316)
	(south c317 c318)
	(north c318 c317)
	(south c318 c319)
	(north c319 c318)
	(south c319 c320)
	(north c320 c319)
	(south c320 c321)
	(north c321 c320)
	(south c321 c322)
	(north c322 c321)
	(south c322 c323)
	(north c323 c322)
	(south c323 c324)
	(north c324 c323)
	(south c324 c325)
	(north c325 c324)
	(south c325 c326)
	(north c326 c325)
	(south c326 c327)
	(north c327 c326)
	(south c327 c328)
	(north c328 c327)
	(south c328 c329)
	(north c329 c328)
	(south c329 c330)
	(north c330 c329)
	(south c330 c331)
	(north c331 c330)
	(south c331 c332)
	(north c332 c331)
	(south c332 c333)
	(north c333 c332)
	(south c333 c334)
	(north c334 c333)
	(south c334 c335)
	(north c335 c334)
	(south c335 c336)
	(north c336 c335)
	(south c336 c337)
	(north c337 c336)
	(south c337 c338)
	(north c338 c337)
	(south c338 c339)
	(north c339 c338)
	(south c339 c340)
	(north c340 c339)
	(south c340 c341)
	(north c341 c340)
	(south c341 c342)
	(north c342 c341)
	(south c342 c343)
	(north c343 c342)
	(south c343 c344)
	(north c344 c343)
	(south c344 c345)
	(north c345 c344)
	(south c345 c346)
	(north c346 c345)
	(south c346 c347)
	(north c347 c346)
	(south c347 c348)
	(north c348 c347)
	(south c348 c349)
	(north c349 c348)
	(south c349 c350)
	(north c350 c349)
	(south c350 c351)
	(north c351 c350)
	(south c351 c352)
	(north c352 c351)
	(south c352 c353)
	(north c353 c352)
	(south c353 c354)
	(north c354 c353)
	(south c354 c355)
	(north c355 c354)
	(south c355 c356)
	(north c356 c355)
	(south c356 c357)
	(north c357 c356)
	(south c357 c358)
	(north c358 c357)
	(south c358 c359)
	(north c359 c358)
	(south c359 c360)
	(north c360 c359)
	(south c360 c361)
	(north c361 c360)
	(south c361 c362)
	(north c362 c361)
	(south c362 c363)
	(north c363 c362)
	(south c363 c364)
	(north c364 c363)
	(south c364 c365)
	(north c365 c364)
	(south c365 c366)
	(north c366 c365)
	(south c366 c367)
	(north c367 c366)
	(south c367 c368)
	(north c368 c367)
	(south c368 c369)
	(north c369 c368)
	(south c369 c370)
	(north c370 c369)
	(south c370 c371)
	(north c371 c370)
	(south c371 c372)
	(north c372 c371)
	(south c372 c373)
	(north c373 c372)
	(south c373 c374)
	(north c374 c373)
	(south c374 c375)
	(north c375 c374)
	(south c375 c376)
	(north c376 c375)
	(south c376 c377)
	(north c377 c376)
	(south c377 c378)
	(north c378 c377)
	(south c378 c379)
	(north c379 c378)
	(south c379 c380)
	(north c380 c379)
	(south c380 c381)
	(north c381 c380)
	(south c381 c382)
	(north c382 c381)
	(south c382 c383)
	(north c383 c382)
	(south c383 c384)
	(north c384 c383)
	(south c384 c385)
	(north c385 c384)
	(south c385 c386)
	(north c386 c385)
	(south c386 c387)
	(north c387 c386)
	(south c387 c388)
	(north c388 c387)
	(south c388 c389)
	(north c389 c388)
	(south c389 c390)
	(north c390 c389)
	(south c390 c391)
	(north c391 c390)
	(south c391 c392)
	(north c392 c391)
	(south c392 c393)
	(north c393 c392)
	(south c393 c394)
	(north c394 c393)
	(south c394 c395)
	(north c395 c394)
	(south c395 c396)
	(north c396 c395)
	(south c396 c397)
	(north c397 c396)
	(south c397 c398)
	(north c398 c397)
	(north c398 g0)
	(south g0 c398)
	(south c398 d0)
	(north d0 c398)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
