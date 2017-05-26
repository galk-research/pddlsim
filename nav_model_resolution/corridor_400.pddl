
(define (problem simple_maze)
(:domain maze)
(:objects
	person1
	start_tile
	t0
	t1
	t2
	t3
	t4
	t5
	t6
	t7
	t8
	t9
	t10
	t11
	t12
	t13
	t14
	t15
	t16
	t17
	t18
	t19
	t20
	t21
	t22
	t23
	t24
	t25
	t26
	t27
	t28
	t29
	t30
	t31
	t32
	t33
	t34
	t35
	t36
	t37
	t38
	t39
	t40
	t41
	t42
	t43
	t44
	t45
	t46
	t47
	t48
	t49
	t50
	t51
	t52
	t53
	t54
	t55
	t56
	t57
	t58
	t59
	t60
	t61
	t62
	t63
	t64
	t65
	t66
	t67
	t68
	t69
	t70
	t71
	t72
	t73
	t74
	t75
	t76
	t77
	t78
	t79
	t80
	t81
	t82
	t83
	t84
	t85
	t86
	t87
	t88
	t89
	t90
	t91
	t92
	t93
	t94
	t95
	t96
	t97
	t98
	t99
	t100
	t101
	t102
	t103
	t104
	t105
	t106
	t107
	t108
	t109
	t110
	t111
	t112
	t113
	t114
	t115
	t116
	t117
	t118
	t119
	t120
	t121
	t122
	t123
	t124
	t125
	t126
	t127
	t128
	t129
	t130
	t131
	t132
	t133
	t134
	t135
	t136
	t137
	t138
	t139
	t140
	t141
	t142
	t143
	t144
	t145
	t146
	t147
	t148
	t149
	t150
	t151
	t152
	t153
	t154
	t155
	t156
	t157
	t158
	t159
	t160
	t161
	t162
	t163
	t164
	t165
	t166
	t167
	t168
	t169
	t170
	t171
	t172
	t173
	t174
	t175
	t176
	t177
	t178
	t179
	t180
	t181
	t182
	t183
	t184
	t185
	t186
	t187
	t188
	t189
	t190
	t191
	t192
	t193
	t194
	t195
	t196
	t197
	t198
	t199
	t200
	t201
	t202
	t203
	t204
	t205
	t206
	t207
	t208
	t209
	t210
	t211
	t212
	t213
	t214
	t215
	t216
	t217
	t218
	t219
	t220
	t221
	t222
	t223
	t224
	t225
	t226
	t227
	t228
	t229
	t230
	t231
	t232
	t233
	t234
	t235
	t236
	t237
	t238
	t239
	t240
	t241
	t242
	t243
	t244
	t245
	t246
	t247
	t248
	t249
	t250
	t251
	t252
	t253
	t254
	t255
	t256
	t257
	t258
	t259
	t260
	t261
	t262
	t263
	t264
	t265
	t266
	t267
	t268
	t269
	t270
	t271
	t272
	t273
	t274
	t275
	t276
	t277
	t278
	t279
	t280
	t281
	t282
	t283
	t284
	t285
	t286
	t287
	t288
	t289
	t290
	t291
	t292
	t293
	t294
	t295
	t296
	t297
	t298
	t299
	t300
	t301
	t302
	t303
	t304
	t305
	t306
	t307
	t308
	t309
	t310
	t311
	t312
	t313
	t314
	t315
	t316
	t317
	t318
	t319
	t320
	t321
	t322
	t323
	t324
	t325
	t326
	t327
	t328
	t329
	t330
	t331
	t332
	t333
	t334
	t335
	t336
	t337
	t338
	t339
	t340
	t341
	t342
	t343
	t344
	t345
	t346
	t347
	t348
	t349
	t350
	t351
	t352
	t353
	t354
	t355
	t356
	t357
	t358
	t359
	t360
	t361
	t362
	t363
	t364
	t365
	t366
	t367
	t368
	t369
	t370
	t371
	t372
	t373
	t374
	t375
	t376
	t377
	t378
	t379
	t380
	t381
	t382
	t383
	t384
	t385
	t386
	t387
	t388
	t389
	t390
	t391
	t392
	t393
	t394
	t395
	t396
	t397
	t398
	t399
	goal_tile
	)
(:init
	(empty start_tile)
	(empty t0)
	(empty t1)
	(empty t2)
	(empty t3)
	(empty t4)
	(empty t5)
	(empty t6)
	(empty t7)
	(empty t8)
	(empty t9)
	(empty t10)
	(empty t11)
	(empty t12)
	(empty t13)
	(empty t14)
	(empty t15)
	(empty t16)
	(empty t17)
	(empty t18)
	(empty t19)
	(empty t20)
	(empty t21)
	(empty t22)
	(empty t23)
	(empty t24)
	(empty t25)
	(empty t26)
	(empty t27)
	(empty t28)
	(empty t29)
	(empty t30)
	(empty t31)
	(empty t32)
	(empty t33)
	(empty t34)
	(empty t35)
	(empty t36)
	(empty t37)
	(empty t38)
	(empty t39)
	(empty t40)
	(empty t41)
	(empty t42)
	(empty t43)
	(empty t44)
	(empty t45)
	(empty t46)
	(empty t47)
	(empty t48)
	(empty t49)
	(empty t50)
	(empty t51)
	(empty t52)
	(empty t53)
	(empty t54)
	(empty t55)
	(empty t56)
	(empty t57)
	(empty t58)
	(empty t59)
	(empty t60)
	(empty t61)
	(empty t62)
	(empty t63)
	(empty t64)
	(empty t65)
	(empty t66)
	(empty t67)
	(empty t68)
	(empty t69)
	(empty t70)
	(empty t71)
	(empty t72)
	(empty t73)
	(empty t74)
	(empty t75)
	(empty t76)
	(empty t77)
	(empty t78)
	(empty t79)
	(empty t80)
	(empty t81)
	(empty t82)
	(empty t83)
	(empty t84)
	(empty t85)
	(empty t86)
	(empty t87)
	(empty t88)
	(empty t89)
	(empty t90)
	(empty t91)
	(empty t92)
	(empty t93)
	(empty t94)
	(empty t95)
	(empty t96)
	(empty t97)
	(empty t98)
	(empty t99)
	(empty t100)
	(empty t101)
	(empty t102)
	(empty t103)
	(empty t104)
	(empty t105)
	(empty t106)
	(empty t107)
	(empty t108)
	(empty t109)
	(empty t110)
	(empty t111)
	(empty t112)
	(empty t113)
	(empty t114)
	(empty t115)
	(empty t116)
	(empty t117)
	(empty t118)
	(empty t119)
	(empty t120)
	(empty t121)
	(empty t122)
	(empty t123)
	(empty t124)
	(empty t125)
	(empty t126)
	(empty t127)
	(empty t128)
	(empty t129)
	(empty t130)
	(empty t131)
	(empty t132)
	(empty t133)
	(empty t134)
	(empty t135)
	(empty t136)
	(empty t137)
	(empty t138)
	(empty t139)
	(empty t140)
	(empty t141)
	(empty t142)
	(empty t143)
	(empty t144)
	(empty t145)
	(empty t146)
	(empty t147)
	(empty t148)
	(empty t149)
	(empty t150)
	(empty t151)
	(empty t152)
	(empty t153)
	(empty t154)
	(empty t155)
	(empty t156)
	(empty t157)
	(empty t158)
	(empty t159)
	(empty t160)
	(empty t161)
	(empty t162)
	(empty t163)
	(empty t164)
	(empty t165)
	(empty t166)
	(empty t167)
	(empty t168)
	(empty t169)
	(empty t170)
	(empty t171)
	(empty t172)
	(empty t173)
	(empty t174)
	(empty t175)
	(empty t176)
	(empty t177)
	(empty t178)
	(empty t179)
	(empty t180)
	(empty t181)
	(empty t182)
	(empty t183)
	(empty t184)
	(empty t185)
	(empty t186)
	(empty t187)
	(empty t188)
	(empty t189)
	(empty t190)
	(empty t191)
	(empty t192)
	(empty t193)
	(empty t194)
	(empty t195)
	(empty t196)
	(empty t197)
	(empty t198)
	(empty t199)
	(empty t200)
	(empty t201)
	(empty t202)
	(empty t203)
	(empty t204)
	(empty t205)
	(empty t206)
	(empty t207)
	(empty t208)
	(empty t209)
	(empty t210)
	(empty t211)
	(empty t212)
	(empty t213)
	(empty t214)
	(empty t215)
	(empty t216)
	(empty t217)
	(empty t218)
	(empty t219)
	(empty t220)
	(empty t221)
	(empty t222)
	(empty t223)
	(empty t224)
	(empty t225)
	(empty t226)
	(empty t227)
	(empty t228)
	(empty t229)
	(empty t230)
	(empty t231)
	(empty t232)
	(empty t233)
	(empty t234)
	(empty t235)
	(empty t236)
	(empty t237)
	(empty t238)
	(empty t239)
	(empty t240)
	(empty t241)
	(empty t242)
	(empty t243)
	(empty t244)
	(empty t245)
	(empty t246)
	(empty t247)
	(empty t248)
	(empty t249)
	(empty t250)
	(empty t251)
	(empty t252)
	(empty t253)
	(empty t254)
	(empty t255)
	(empty t256)
	(empty t257)
	(empty t258)
	(empty t259)
	(empty t260)
	(empty t261)
	(empty t262)
	(empty t263)
	(empty t264)
	(empty t265)
	(empty t266)
	(empty t267)
	(empty t268)
	(empty t269)
	(empty t270)
	(empty t271)
	(empty t272)
	(empty t273)
	(empty t274)
	(empty t275)
	(empty t276)
	(empty t277)
	(empty t278)
	(empty t279)
	(empty t280)
	(empty t281)
	(empty t282)
	(empty t283)
	(empty t284)
	(empty t285)
	(empty t286)
	(empty t287)
	(empty t288)
	(empty t289)
	(empty t290)
	(empty t291)
	(empty t292)
	(empty t293)
	(empty t294)
	(empty t295)
	(empty t296)
	(empty t297)
	(empty t298)
	(empty t299)
	(empty t300)
	(empty t301)
	(empty t302)
	(empty t303)
	(empty t304)
	(empty t305)
	(empty t306)
	(empty t307)
	(empty t308)
	(empty t309)
	(empty t310)
	(empty t311)
	(empty t312)
	(empty t313)
	(empty t314)
	(empty t315)
	(empty t316)
	(empty t317)
	(empty t318)
	(empty t319)
	(empty t320)
	(empty t321)
	(empty t322)
	(empty t323)
	(empty t324)
	(empty t325)
	(empty t326)
	(empty t327)
	(empty t328)
	(empty t329)
	(empty t330)
	(empty t331)
	(empty t332)
	(empty t333)
	(empty t334)
	(empty t335)
	(empty t336)
	(empty t337)
	(empty t338)
	(empty t339)
	(empty t340)
	(empty t341)
	(empty t342)
	(empty t343)
	(empty t344)
	(empty t345)
	(empty t346)
	(empty t347)
	(empty t348)
	(empty t349)
	(empty t350)
	(empty t351)
	(empty t352)
	(empty t353)
	(empty t354)
	(empty t355)
	(empty t356)
	(empty t357)
	(empty t358)
	(empty t359)
	(empty t360)
	(empty t361)
	(empty t362)
	(empty t363)
	(empty t364)
	(empty t365)
	(empty t366)
	(empty t367)
	(empty t368)
	(empty t369)
	(empty t370)
	(empty t371)
	(empty t372)
	(empty t373)
	(empty t374)
	(empty t375)
	(empty t376)
	(empty t377)
	(empty t378)
	(empty t379)
	(empty t380)
	(empty t381)
	(empty t382)
	(empty t383)
	(empty t384)
	(empty t385)
	(empty t386)
	(empty t387)
	(empty t388)
	(empty t389)
	(empty t390)
	(empty t391)
	(empty t392)
	(empty t393)
	(empty t394)
	(empty t395)
	(empty t396)
	(empty t397)
	(empty t398)
	(empty t399)
	(empty goal_tile)
	(east start_tile t0)
	(west t0 start_tile)
	(east t0 t1)
	(west t1 t0)
	(east t1 t2)
	(west t2 t1)
	(east t2 t3)
	(west t3 t2)
	(east t3 t4)
	(west t4 t3)
	(east t4 t5)
	(west t5 t4)
	(east t5 t6)
	(west t6 t5)
	(east t6 t7)
	(west t7 t6)
	(east t7 t8)
	(west t8 t7)
	(east t8 t9)
	(west t9 t8)
	(east t9 t10)
	(west t10 t9)
	(east t10 t11)
	(west t11 t10)
	(east t11 t12)
	(west t12 t11)
	(east t12 t13)
	(west t13 t12)
	(east t13 t14)
	(west t14 t13)
	(east t14 t15)
	(west t15 t14)
	(east t15 t16)
	(west t16 t15)
	(east t16 t17)
	(west t17 t16)
	(east t17 t18)
	(west t18 t17)
	(east t18 t19)
	(west t19 t18)
	(east t19 t20)
	(west t20 t19)
	(east t20 t21)
	(west t21 t20)
	(east t21 t22)
	(west t22 t21)
	(east t22 t23)
	(west t23 t22)
	(east t23 t24)
	(west t24 t23)
	(east t24 t25)
	(west t25 t24)
	(east t25 t26)
	(west t26 t25)
	(east t26 t27)
	(west t27 t26)
	(east t27 t28)
	(west t28 t27)
	(east t28 t29)
	(west t29 t28)
	(east t29 t30)
	(west t30 t29)
	(east t30 t31)
	(west t31 t30)
	(east t31 t32)
	(west t32 t31)
	(east t32 t33)
	(west t33 t32)
	(east t33 t34)
	(west t34 t33)
	(east t34 t35)
	(west t35 t34)
	(east t35 t36)
	(west t36 t35)
	(east t36 t37)
	(west t37 t36)
	(east t37 t38)
	(west t38 t37)
	(east t38 t39)
	(west t39 t38)
	(east t39 t40)
	(west t40 t39)
	(east t40 t41)
	(west t41 t40)
	(east t41 t42)
	(west t42 t41)
	(east t42 t43)
	(west t43 t42)
	(east t43 t44)
	(west t44 t43)
	(east t44 t45)
	(west t45 t44)
	(east t45 t46)
	(west t46 t45)
	(east t46 t47)
	(west t47 t46)
	(east t47 t48)
	(west t48 t47)
	(east t48 t49)
	(west t49 t48)
	(east t49 t50)
	(west t50 t49)
	(east t50 t51)
	(west t51 t50)
	(east t51 t52)
	(west t52 t51)
	(east t52 t53)
	(west t53 t52)
	(east t53 t54)
	(west t54 t53)
	(east t54 t55)
	(west t55 t54)
	(east t55 t56)
	(west t56 t55)
	(east t56 t57)
	(west t57 t56)
	(east t57 t58)
	(west t58 t57)
	(east t58 t59)
	(west t59 t58)
	(east t59 t60)
	(west t60 t59)
	(east t60 t61)
	(west t61 t60)
	(east t61 t62)
	(west t62 t61)
	(east t62 t63)
	(west t63 t62)
	(east t63 t64)
	(west t64 t63)
	(east t64 t65)
	(west t65 t64)
	(east t65 t66)
	(west t66 t65)
	(east t66 t67)
	(west t67 t66)
	(east t67 t68)
	(west t68 t67)
	(east t68 t69)
	(west t69 t68)
	(east t69 t70)
	(west t70 t69)
	(east t70 t71)
	(west t71 t70)
	(east t71 t72)
	(west t72 t71)
	(east t72 t73)
	(west t73 t72)
	(east t73 t74)
	(west t74 t73)
	(east t74 t75)
	(west t75 t74)
	(east t75 t76)
	(west t76 t75)
	(east t76 t77)
	(west t77 t76)
	(east t77 t78)
	(west t78 t77)
	(east t78 t79)
	(west t79 t78)
	(east t79 t80)
	(west t80 t79)
	(east t80 t81)
	(west t81 t80)
	(east t81 t82)
	(west t82 t81)
	(east t82 t83)
	(west t83 t82)
	(east t83 t84)
	(west t84 t83)
	(east t84 t85)
	(west t85 t84)
	(east t85 t86)
	(west t86 t85)
	(east t86 t87)
	(west t87 t86)
	(east t87 t88)
	(west t88 t87)
	(east t88 t89)
	(west t89 t88)
	(east t89 t90)
	(west t90 t89)
	(east t90 t91)
	(west t91 t90)
	(east t91 t92)
	(west t92 t91)
	(east t92 t93)
	(west t93 t92)
	(east t93 t94)
	(west t94 t93)
	(east t94 t95)
	(west t95 t94)
	(east t95 t96)
	(west t96 t95)
	(east t96 t97)
	(west t97 t96)
	(east t97 t98)
	(west t98 t97)
	(east t98 t99)
	(west t99 t98)
	(east t99 t100)
	(west t100 t99)
	(east t100 t101)
	(west t101 t100)
	(east t101 t102)
	(west t102 t101)
	(east t102 t103)
	(west t103 t102)
	(east t103 t104)
	(west t104 t103)
	(east t104 t105)
	(west t105 t104)
	(east t105 t106)
	(west t106 t105)
	(east t106 t107)
	(west t107 t106)
	(east t107 t108)
	(west t108 t107)
	(east t108 t109)
	(west t109 t108)
	(east t109 t110)
	(west t110 t109)
	(east t110 t111)
	(west t111 t110)
	(east t111 t112)
	(west t112 t111)
	(east t112 t113)
	(west t113 t112)
	(east t113 t114)
	(west t114 t113)
	(east t114 t115)
	(west t115 t114)
	(east t115 t116)
	(west t116 t115)
	(east t116 t117)
	(west t117 t116)
	(east t117 t118)
	(west t118 t117)
	(east t118 t119)
	(west t119 t118)
	(east t119 t120)
	(west t120 t119)
	(east t120 t121)
	(west t121 t120)
	(east t121 t122)
	(west t122 t121)
	(east t122 t123)
	(west t123 t122)
	(east t123 t124)
	(west t124 t123)
	(east t124 t125)
	(west t125 t124)
	(east t125 t126)
	(west t126 t125)
	(east t126 t127)
	(west t127 t126)
	(east t127 t128)
	(west t128 t127)
	(east t128 t129)
	(west t129 t128)
	(east t129 t130)
	(west t130 t129)
	(east t130 t131)
	(west t131 t130)
	(east t131 t132)
	(west t132 t131)
	(east t132 t133)
	(west t133 t132)
	(east t133 t134)
	(west t134 t133)
	(east t134 t135)
	(west t135 t134)
	(east t135 t136)
	(west t136 t135)
	(east t136 t137)
	(west t137 t136)
	(east t137 t138)
	(west t138 t137)
	(east t138 t139)
	(west t139 t138)
	(east t139 t140)
	(west t140 t139)
	(east t140 t141)
	(west t141 t140)
	(east t141 t142)
	(west t142 t141)
	(east t142 t143)
	(west t143 t142)
	(east t143 t144)
	(west t144 t143)
	(east t144 t145)
	(west t145 t144)
	(east t145 t146)
	(west t146 t145)
	(east t146 t147)
	(west t147 t146)
	(east t147 t148)
	(west t148 t147)
	(east t148 t149)
	(west t149 t148)
	(east t149 t150)
	(west t150 t149)
	(east t150 t151)
	(west t151 t150)
	(east t151 t152)
	(west t152 t151)
	(east t152 t153)
	(west t153 t152)
	(east t153 t154)
	(west t154 t153)
	(east t154 t155)
	(west t155 t154)
	(east t155 t156)
	(west t156 t155)
	(east t156 t157)
	(west t157 t156)
	(east t157 t158)
	(west t158 t157)
	(east t158 t159)
	(west t159 t158)
	(east t159 t160)
	(west t160 t159)
	(east t160 t161)
	(west t161 t160)
	(east t161 t162)
	(west t162 t161)
	(east t162 t163)
	(west t163 t162)
	(east t163 t164)
	(west t164 t163)
	(east t164 t165)
	(west t165 t164)
	(east t165 t166)
	(west t166 t165)
	(east t166 t167)
	(west t167 t166)
	(east t167 t168)
	(west t168 t167)
	(east t168 t169)
	(west t169 t168)
	(east t169 t170)
	(west t170 t169)
	(east t170 t171)
	(west t171 t170)
	(east t171 t172)
	(west t172 t171)
	(east t172 t173)
	(west t173 t172)
	(east t173 t174)
	(west t174 t173)
	(east t174 t175)
	(west t175 t174)
	(east t175 t176)
	(west t176 t175)
	(east t176 t177)
	(west t177 t176)
	(east t177 t178)
	(west t178 t177)
	(east t178 t179)
	(west t179 t178)
	(east t179 t180)
	(west t180 t179)
	(east t180 t181)
	(west t181 t180)
	(east t181 t182)
	(west t182 t181)
	(east t182 t183)
	(west t183 t182)
	(east t183 t184)
	(west t184 t183)
	(east t184 t185)
	(west t185 t184)
	(east t185 t186)
	(west t186 t185)
	(east t186 t187)
	(west t187 t186)
	(east t187 t188)
	(west t188 t187)
	(east t188 t189)
	(west t189 t188)
	(east t189 t190)
	(west t190 t189)
	(east t190 t191)
	(west t191 t190)
	(east t191 t192)
	(west t192 t191)
	(east t192 t193)
	(west t193 t192)
	(east t193 t194)
	(west t194 t193)
	(east t194 t195)
	(west t195 t194)
	(east t195 t196)
	(west t196 t195)
	(east t196 t197)
	(west t197 t196)
	(east t197 t198)
	(west t198 t197)
	(east t198 t199)
	(west t199 t198)
	(east t199 t200)
	(west t200 t199)
	(east t200 t201)
	(west t201 t200)
	(east t201 t202)
	(west t202 t201)
	(east t202 t203)
	(west t203 t202)
	(east t203 t204)
	(west t204 t203)
	(east t204 t205)
	(west t205 t204)
	(east t205 t206)
	(west t206 t205)
	(east t206 t207)
	(west t207 t206)
	(east t207 t208)
	(west t208 t207)
	(east t208 t209)
	(west t209 t208)
	(east t209 t210)
	(west t210 t209)
	(east t210 t211)
	(west t211 t210)
	(east t211 t212)
	(west t212 t211)
	(east t212 t213)
	(west t213 t212)
	(east t213 t214)
	(west t214 t213)
	(east t214 t215)
	(west t215 t214)
	(east t215 t216)
	(west t216 t215)
	(east t216 t217)
	(west t217 t216)
	(east t217 t218)
	(west t218 t217)
	(east t218 t219)
	(west t219 t218)
	(east t219 t220)
	(west t220 t219)
	(east t220 t221)
	(west t221 t220)
	(east t221 t222)
	(west t222 t221)
	(east t222 t223)
	(west t223 t222)
	(east t223 t224)
	(west t224 t223)
	(east t224 t225)
	(west t225 t224)
	(east t225 t226)
	(west t226 t225)
	(east t226 t227)
	(west t227 t226)
	(east t227 t228)
	(west t228 t227)
	(east t228 t229)
	(west t229 t228)
	(east t229 t230)
	(west t230 t229)
	(east t230 t231)
	(west t231 t230)
	(east t231 t232)
	(west t232 t231)
	(east t232 t233)
	(west t233 t232)
	(east t233 t234)
	(west t234 t233)
	(east t234 t235)
	(west t235 t234)
	(east t235 t236)
	(west t236 t235)
	(east t236 t237)
	(west t237 t236)
	(east t237 t238)
	(west t238 t237)
	(east t238 t239)
	(west t239 t238)
	(east t239 t240)
	(west t240 t239)
	(east t240 t241)
	(west t241 t240)
	(east t241 t242)
	(west t242 t241)
	(east t242 t243)
	(west t243 t242)
	(east t243 t244)
	(west t244 t243)
	(east t244 t245)
	(west t245 t244)
	(east t245 t246)
	(west t246 t245)
	(east t246 t247)
	(west t247 t246)
	(east t247 t248)
	(west t248 t247)
	(east t248 t249)
	(west t249 t248)
	(east t249 t250)
	(west t250 t249)
	(east t250 t251)
	(west t251 t250)
	(east t251 t252)
	(west t252 t251)
	(east t252 t253)
	(west t253 t252)
	(east t253 t254)
	(west t254 t253)
	(east t254 t255)
	(west t255 t254)
	(east t255 t256)
	(west t256 t255)
	(east t256 t257)
	(west t257 t256)
	(east t257 t258)
	(west t258 t257)
	(east t258 t259)
	(west t259 t258)
	(east t259 t260)
	(west t260 t259)
	(east t260 t261)
	(west t261 t260)
	(east t261 t262)
	(west t262 t261)
	(east t262 t263)
	(west t263 t262)
	(east t263 t264)
	(west t264 t263)
	(east t264 t265)
	(west t265 t264)
	(east t265 t266)
	(west t266 t265)
	(east t266 t267)
	(west t267 t266)
	(east t267 t268)
	(west t268 t267)
	(east t268 t269)
	(west t269 t268)
	(east t269 t270)
	(west t270 t269)
	(east t270 t271)
	(west t271 t270)
	(east t271 t272)
	(west t272 t271)
	(east t272 t273)
	(west t273 t272)
	(east t273 t274)
	(west t274 t273)
	(east t274 t275)
	(west t275 t274)
	(east t275 t276)
	(west t276 t275)
	(east t276 t277)
	(west t277 t276)
	(east t277 t278)
	(west t278 t277)
	(east t278 t279)
	(west t279 t278)
	(east t279 t280)
	(west t280 t279)
	(east t280 t281)
	(west t281 t280)
	(east t281 t282)
	(west t282 t281)
	(east t282 t283)
	(west t283 t282)
	(east t283 t284)
	(west t284 t283)
	(east t284 t285)
	(west t285 t284)
	(east t285 t286)
	(west t286 t285)
	(east t286 t287)
	(west t287 t286)
	(east t287 t288)
	(west t288 t287)
	(east t288 t289)
	(west t289 t288)
	(east t289 t290)
	(west t290 t289)
	(east t290 t291)
	(west t291 t290)
	(east t291 t292)
	(west t292 t291)
	(east t292 t293)
	(west t293 t292)
	(east t293 t294)
	(west t294 t293)
	(east t294 t295)
	(west t295 t294)
	(east t295 t296)
	(west t296 t295)
	(east t296 t297)
	(west t297 t296)
	(east t297 t298)
	(west t298 t297)
	(east t298 t299)
	(west t299 t298)
	(east t299 t300)
	(west t300 t299)
	(east t300 t301)
	(west t301 t300)
	(east t301 t302)
	(west t302 t301)
	(east t302 t303)
	(west t303 t302)
	(east t303 t304)
	(west t304 t303)
	(east t304 t305)
	(west t305 t304)
	(east t305 t306)
	(west t306 t305)
	(east t306 t307)
	(west t307 t306)
	(east t307 t308)
	(west t308 t307)
	(east t308 t309)
	(west t309 t308)
	(east t309 t310)
	(west t310 t309)
	(east t310 t311)
	(west t311 t310)
	(east t311 t312)
	(west t312 t311)
	(east t312 t313)
	(west t313 t312)
	(east t313 t314)
	(west t314 t313)
	(east t314 t315)
	(west t315 t314)
	(east t315 t316)
	(west t316 t315)
	(east t316 t317)
	(west t317 t316)
	(east t317 t318)
	(west t318 t317)
	(east t318 t319)
	(west t319 t318)
	(east t319 t320)
	(west t320 t319)
	(east t320 t321)
	(west t321 t320)
	(east t321 t322)
	(west t322 t321)
	(east t322 t323)
	(west t323 t322)
	(east t323 t324)
	(west t324 t323)
	(east t324 t325)
	(west t325 t324)
	(east t325 t326)
	(west t326 t325)
	(east t326 t327)
	(west t327 t326)
	(east t327 t328)
	(west t328 t327)
	(east t328 t329)
	(west t329 t328)
	(east t329 t330)
	(west t330 t329)
	(east t330 t331)
	(west t331 t330)
	(east t331 t332)
	(west t332 t331)
	(east t332 t333)
	(west t333 t332)
	(east t333 t334)
	(west t334 t333)
	(east t334 t335)
	(west t335 t334)
	(east t335 t336)
	(west t336 t335)
	(east t336 t337)
	(west t337 t336)
	(east t337 t338)
	(west t338 t337)
	(east t338 t339)
	(west t339 t338)
	(east t339 t340)
	(west t340 t339)
	(east t340 t341)
	(west t341 t340)
	(east t341 t342)
	(west t342 t341)
	(east t342 t343)
	(west t343 t342)
	(east t343 t344)
	(west t344 t343)
	(east t344 t345)
	(west t345 t344)
	(east t345 t346)
	(west t346 t345)
	(east t346 t347)
	(west t347 t346)
	(east t347 t348)
	(west t348 t347)
	(east t348 t349)
	(west t349 t348)
	(east t349 t350)
	(west t350 t349)
	(east t350 t351)
	(west t351 t350)
	(east t351 t352)
	(west t352 t351)
	(east t352 t353)
	(west t353 t352)
	(east t353 t354)
	(west t354 t353)
	(east t354 t355)
	(west t355 t354)
	(east t355 t356)
	(west t356 t355)
	(east t356 t357)
	(west t357 t356)
	(east t357 t358)
	(west t358 t357)
	(east t358 t359)
	(west t359 t358)
	(east t359 t360)
	(west t360 t359)
	(east t360 t361)
	(west t361 t360)
	(east t361 t362)
	(west t362 t361)
	(east t362 t363)
	(west t363 t362)
	(east t363 t364)
	(west t364 t363)
	(east t364 t365)
	(west t365 t364)
	(east t365 t366)
	(west t366 t365)
	(east t366 t367)
	(west t367 t366)
	(east t367 t368)
	(west t368 t367)
	(east t368 t369)
	(west t369 t368)
	(east t369 t370)
	(west t370 t369)
	(east t370 t371)
	(west t371 t370)
	(east t371 t372)
	(west t372 t371)
	(east t372 t373)
	(west t373 t372)
	(east t373 t374)
	(west t374 t373)
	(east t374 t375)
	(west t375 t374)
	(east t375 t376)
	(west t376 t375)
	(east t376 t377)
	(west t377 t376)
	(east t377 t378)
	(west t378 t377)
	(east t378 t379)
	(west t379 t378)
	(east t379 t380)
	(west t380 t379)
	(east t380 t381)
	(west t381 t380)
	(east t381 t382)
	(west t382 t381)
	(east t382 t383)
	(west t383 t382)
	(east t383 t384)
	(west t384 t383)
	(east t384 t385)
	(west t385 t384)
	(east t385 t386)
	(west t386 t385)
	(east t386 t387)
	(west t387 t386)
	(east t387 t388)
	(west t388 t387)
	(east t388 t389)
	(west t389 t388)
	(east t389 t390)
	(west t390 t389)
	(east t390 t391)
	(west t391 t390)
	(east t391 t392)
	(west t392 t391)
	(east t392 t393)
	(west t393 t392)
	(east t393 t394)
	(west t394 t393)
	(east t394 t395)
	(west t395 t394)
	(east t395 t396)
	(west t396 t395)
	(east t396 t397)
	(west t397 t396)
	(east t397 t398)
	(west t398 t397)
	(east t398 t399)
	(west t399 t398)
	(east t399 goal_tile)
	(west goal_tile t399)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
