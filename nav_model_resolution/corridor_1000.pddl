
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
	t400
	t401
	t402
	t403
	t404
	t405
	t406
	t407
	t408
	t409
	t410
	t411
	t412
	t413
	t414
	t415
	t416
	t417
	t418
	t419
	t420
	t421
	t422
	t423
	t424
	t425
	t426
	t427
	t428
	t429
	t430
	t431
	t432
	t433
	t434
	t435
	t436
	t437
	t438
	t439
	t440
	t441
	t442
	t443
	t444
	t445
	t446
	t447
	t448
	t449
	t450
	t451
	t452
	t453
	t454
	t455
	t456
	t457
	t458
	t459
	t460
	t461
	t462
	t463
	t464
	t465
	t466
	t467
	t468
	t469
	t470
	t471
	t472
	t473
	t474
	t475
	t476
	t477
	t478
	t479
	t480
	t481
	t482
	t483
	t484
	t485
	t486
	t487
	t488
	t489
	t490
	t491
	t492
	t493
	t494
	t495
	t496
	t497
	t498
	t499
	t500
	t501
	t502
	t503
	t504
	t505
	t506
	t507
	t508
	t509
	t510
	t511
	t512
	t513
	t514
	t515
	t516
	t517
	t518
	t519
	t520
	t521
	t522
	t523
	t524
	t525
	t526
	t527
	t528
	t529
	t530
	t531
	t532
	t533
	t534
	t535
	t536
	t537
	t538
	t539
	t540
	t541
	t542
	t543
	t544
	t545
	t546
	t547
	t548
	t549
	t550
	t551
	t552
	t553
	t554
	t555
	t556
	t557
	t558
	t559
	t560
	t561
	t562
	t563
	t564
	t565
	t566
	t567
	t568
	t569
	t570
	t571
	t572
	t573
	t574
	t575
	t576
	t577
	t578
	t579
	t580
	t581
	t582
	t583
	t584
	t585
	t586
	t587
	t588
	t589
	t590
	t591
	t592
	t593
	t594
	t595
	t596
	t597
	t598
	t599
	t600
	t601
	t602
	t603
	t604
	t605
	t606
	t607
	t608
	t609
	t610
	t611
	t612
	t613
	t614
	t615
	t616
	t617
	t618
	t619
	t620
	t621
	t622
	t623
	t624
	t625
	t626
	t627
	t628
	t629
	t630
	t631
	t632
	t633
	t634
	t635
	t636
	t637
	t638
	t639
	t640
	t641
	t642
	t643
	t644
	t645
	t646
	t647
	t648
	t649
	t650
	t651
	t652
	t653
	t654
	t655
	t656
	t657
	t658
	t659
	t660
	t661
	t662
	t663
	t664
	t665
	t666
	t667
	t668
	t669
	t670
	t671
	t672
	t673
	t674
	t675
	t676
	t677
	t678
	t679
	t680
	t681
	t682
	t683
	t684
	t685
	t686
	t687
	t688
	t689
	t690
	t691
	t692
	t693
	t694
	t695
	t696
	t697
	t698
	t699
	t700
	t701
	t702
	t703
	t704
	t705
	t706
	t707
	t708
	t709
	t710
	t711
	t712
	t713
	t714
	t715
	t716
	t717
	t718
	t719
	t720
	t721
	t722
	t723
	t724
	t725
	t726
	t727
	t728
	t729
	t730
	t731
	t732
	t733
	t734
	t735
	t736
	t737
	t738
	t739
	t740
	t741
	t742
	t743
	t744
	t745
	t746
	t747
	t748
	t749
	t750
	t751
	t752
	t753
	t754
	t755
	t756
	t757
	t758
	t759
	t760
	t761
	t762
	t763
	t764
	t765
	t766
	t767
	t768
	t769
	t770
	t771
	t772
	t773
	t774
	t775
	t776
	t777
	t778
	t779
	t780
	t781
	t782
	t783
	t784
	t785
	t786
	t787
	t788
	t789
	t790
	t791
	t792
	t793
	t794
	t795
	t796
	t797
	t798
	t799
	t800
	t801
	t802
	t803
	t804
	t805
	t806
	t807
	t808
	t809
	t810
	t811
	t812
	t813
	t814
	t815
	t816
	t817
	t818
	t819
	t820
	t821
	t822
	t823
	t824
	t825
	t826
	t827
	t828
	t829
	t830
	t831
	t832
	t833
	t834
	t835
	t836
	t837
	t838
	t839
	t840
	t841
	t842
	t843
	t844
	t845
	t846
	t847
	t848
	t849
	t850
	t851
	t852
	t853
	t854
	t855
	t856
	t857
	t858
	t859
	t860
	t861
	t862
	t863
	t864
	t865
	t866
	t867
	t868
	t869
	t870
	t871
	t872
	t873
	t874
	t875
	t876
	t877
	t878
	t879
	t880
	t881
	t882
	t883
	t884
	t885
	t886
	t887
	t888
	t889
	t890
	t891
	t892
	t893
	t894
	t895
	t896
	t897
	t898
	t899
	t900
	t901
	t902
	t903
	t904
	t905
	t906
	t907
	t908
	t909
	t910
	t911
	t912
	t913
	t914
	t915
	t916
	t917
	t918
	t919
	t920
	t921
	t922
	t923
	t924
	t925
	t926
	t927
	t928
	t929
	t930
	t931
	t932
	t933
	t934
	t935
	t936
	t937
	t938
	t939
	t940
	t941
	t942
	t943
	t944
	t945
	t946
	t947
	t948
	t949
	t950
	t951
	t952
	t953
	t954
	t955
	t956
	t957
	t958
	t959
	t960
	t961
	t962
	t963
	t964
	t965
	t966
	t967
	t968
	t969
	t970
	t971
	t972
	t973
	t974
	t975
	t976
	t977
	t978
	t979
	t980
	t981
	t982
	t983
	t984
	t985
	t986
	t987
	t988
	t989
	t990
	t991
	t992
	t993
	t994
	t995
	t996
	t997
	t998
	t999
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
	(empty t400)
	(empty t401)
	(empty t402)
	(empty t403)
	(empty t404)
	(empty t405)
	(empty t406)
	(empty t407)
	(empty t408)
	(empty t409)
	(empty t410)
	(empty t411)
	(empty t412)
	(empty t413)
	(empty t414)
	(empty t415)
	(empty t416)
	(empty t417)
	(empty t418)
	(empty t419)
	(empty t420)
	(empty t421)
	(empty t422)
	(empty t423)
	(empty t424)
	(empty t425)
	(empty t426)
	(empty t427)
	(empty t428)
	(empty t429)
	(empty t430)
	(empty t431)
	(empty t432)
	(empty t433)
	(empty t434)
	(empty t435)
	(empty t436)
	(empty t437)
	(empty t438)
	(empty t439)
	(empty t440)
	(empty t441)
	(empty t442)
	(empty t443)
	(empty t444)
	(empty t445)
	(empty t446)
	(empty t447)
	(empty t448)
	(empty t449)
	(empty t450)
	(empty t451)
	(empty t452)
	(empty t453)
	(empty t454)
	(empty t455)
	(empty t456)
	(empty t457)
	(empty t458)
	(empty t459)
	(empty t460)
	(empty t461)
	(empty t462)
	(empty t463)
	(empty t464)
	(empty t465)
	(empty t466)
	(empty t467)
	(empty t468)
	(empty t469)
	(empty t470)
	(empty t471)
	(empty t472)
	(empty t473)
	(empty t474)
	(empty t475)
	(empty t476)
	(empty t477)
	(empty t478)
	(empty t479)
	(empty t480)
	(empty t481)
	(empty t482)
	(empty t483)
	(empty t484)
	(empty t485)
	(empty t486)
	(empty t487)
	(empty t488)
	(empty t489)
	(empty t490)
	(empty t491)
	(empty t492)
	(empty t493)
	(empty t494)
	(empty t495)
	(empty t496)
	(empty t497)
	(empty t498)
	(empty t499)
	(empty t500)
	(empty t501)
	(empty t502)
	(empty t503)
	(empty t504)
	(empty t505)
	(empty t506)
	(empty t507)
	(empty t508)
	(empty t509)
	(empty t510)
	(empty t511)
	(empty t512)
	(empty t513)
	(empty t514)
	(empty t515)
	(empty t516)
	(empty t517)
	(empty t518)
	(empty t519)
	(empty t520)
	(empty t521)
	(empty t522)
	(empty t523)
	(empty t524)
	(empty t525)
	(empty t526)
	(empty t527)
	(empty t528)
	(empty t529)
	(empty t530)
	(empty t531)
	(empty t532)
	(empty t533)
	(empty t534)
	(empty t535)
	(empty t536)
	(empty t537)
	(empty t538)
	(empty t539)
	(empty t540)
	(empty t541)
	(empty t542)
	(empty t543)
	(empty t544)
	(empty t545)
	(empty t546)
	(empty t547)
	(empty t548)
	(empty t549)
	(empty t550)
	(empty t551)
	(empty t552)
	(empty t553)
	(empty t554)
	(empty t555)
	(empty t556)
	(empty t557)
	(empty t558)
	(empty t559)
	(empty t560)
	(empty t561)
	(empty t562)
	(empty t563)
	(empty t564)
	(empty t565)
	(empty t566)
	(empty t567)
	(empty t568)
	(empty t569)
	(empty t570)
	(empty t571)
	(empty t572)
	(empty t573)
	(empty t574)
	(empty t575)
	(empty t576)
	(empty t577)
	(empty t578)
	(empty t579)
	(empty t580)
	(empty t581)
	(empty t582)
	(empty t583)
	(empty t584)
	(empty t585)
	(empty t586)
	(empty t587)
	(empty t588)
	(empty t589)
	(empty t590)
	(empty t591)
	(empty t592)
	(empty t593)
	(empty t594)
	(empty t595)
	(empty t596)
	(empty t597)
	(empty t598)
	(empty t599)
	(empty t600)
	(empty t601)
	(empty t602)
	(empty t603)
	(empty t604)
	(empty t605)
	(empty t606)
	(empty t607)
	(empty t608)
	(empty t609)
	(empty t610)
	(empty t611)
	(empty t612)
	(empty t613)
	(empty t614)
	(empty t615)
	(empty t616)
	(empty t617)
	(empty t618)
	(empty t619)
	(empty t620)
	(empty t621)
	(empty t622)
	(empty t623)
	(empty t624)
	(empty t625)
	(empty t626)
	(empty t627)
	(empty t628)
	(empty t629)
	(empty t630)
	(empty t631)
	(empty t632)
	(empty t633)
	(empty t634)
	(empty t635)
	(empty t636)
	(empty t637)
	(empty t638)
	(empty t639)
	(empty t640)
	(empty t641)
	(empty t642)
	(empty t643)
	(empty t644)
	(empty t645)
	(empty t646)
	(empty t647)
	(empty t648)
	(empty t649)
	(empty t650)
	(empty t651)
	(empty t652)
	(empty t653)
	(empty t654)
	(empty t655)
	(empty t656)
	(empty t657)
	(empty t658)
	(empty t659)
	(empty t660)
	(empty t661)
	(empty t662)
	(empty t663)
	(empty t664)
	(empty t665)
	(empty t666)
	(empty t667)
	(empty t668)
	(empty t669)
	(empty t670)
	(empty t671)
	(empty t672)
	(empty t673)
	(empty t674)
	(empty t675)
	(empty t676)
	(empty t677)
	(empty t678)
	(empty t679)
	(empty t680)
	(empty t681)
	(empty t682)
	(empty t683)
	(empty t684)
	(empty t685)
	(empty t686)
	(empty t687)
	(empty t688)
	(empty t689)
	(empty t690)
	(empty t691)
	(empty t692)
	(empty t693)
	(empty t694)
	(empty t695)
	(empty t696)
	(empty t697)
	(empty t698)
	(empty t699)
	(empty t700)
	(empty t701)
	(empty t702)
	(empty t703)
	(empty t704)
	(empty t705)
	(empty t706)
	(empty t707)
	(empty t708)
	(empty t709)
	(empty t710)
	(empty t711)
	(empty t712)
	(empty t713)
	(empty t714)
	(empty t715)
	(empty t716)
	(empty t717)
	(empty t718)
	(empty t719)
	(empty t720)
	(empty t721)
	(empty t722)
	(empty t723)
	(empty t724)
	(empty t725)
	(empty t726)
	(empty t727)
	(empty t728)
	(empty t729)
	(empty t730)
	(empty t731)
	(empty t732)
	(empty t733)
	(empty t734)
	(empty t735)
	(empty t736)
	(empty t737)
	(empty t738)
	(empty t739)
	(empty t740)
	(empty t741)
	(empty t742)
	(empty t743)
	(empty t744)
	(empty t745)
	(empty t746)
	(empty t747)
	(empty t748)
	(empty t749)
	(empty t750)
	(empty t751)
	(empty t752)
	(empty t753)
	(empty t754)
	(empty t755)
	(empty t756)
	(empty t757)
	(empty t758)
	(empty t759)
	(empty t760)
	(empty t761)
	(empty t762)
	(empty t763)
	(empty t764)
	(empty t765)
	(empty t766)
	(empty t767)
	(empty t768)
	(empty t769)
	(empty t770)
	(empty t771)
	(empty t772)
	(empty t773)
	(empty t774)
	(empty t775)
	(empty t776)
	(empty t777)
	(empty t778)
	(empty t779)
	(empty t780)
	(empty t781)
	(empty t782)
	(empty t783)
	(empty t784)
	(empty t785)
	(empty t786)
	(empty t787)
	(empty t788)
	(empty t789)
	(empty t790)
	(empty t791)
	(empty t792)
	(empty t793)
	(empty t794)
	(empty t795)
	(empty t796)
	(empty t797)
	(empty t798)
	(empty t799)
	(empty t800)
	(empty t801)
	(empty t802)
	(empty t803)
	(empty t804)
	(empty t805)
	(empty t806)
	(empty t807)
	(empty t808)
	(empty t809)
	(empty t810)
	(empty t811)
	(empty t812)
	(empty t813)
	(empty t814)
	(empty t815)
	(empty t816)
	(empty t817)
	(empty t818)
	(empty t819)
	(empty t820)
	(empty t821)
	(empty t822)
	(empty t823)
	(empty t824)
	(empty t825)
	(empty t826)
	(empty t827)
	(empty t828)
	(empty t829)
	(empty t830)
	(empty t831)
	(empty t832)
	(empty t833)
	(empty t834)
	(empty t835)
	(empty t836)
	(empty t837)
	(empty t838)
	(empty t839)
	(empty t840)
	(empty t841)
	(empty t842)
	(empty t843)
	(empty t844)
	(empty t845)
	(empty t846)
	(empty t847)
	(empty t848)
	(empty t849)
	(empty t850)
	(empty t851)
	(empty t852)
	(empty t853)
	(empty t854)
	(empty t855)
	(empty t856)
	(empty t857)
	(empty t858)
	(empty t859)
	(empty t860)
	(empty t861)
	(empty t862)
	(empty t863)
	(empty t864)
	(empty t865)
	(empty t866)
	(empty t867)
	(empty t868)
	(empty t869)
	(empty t870)
	(empty t871)
	(empty t872)
	(empty t873)
	(empty t874)
	(empty t875)
	(empty t876)
	(empty t877)
	(empty t878)
	(empty t879)
	(empty t880)
	(empty t881)
	(empty t882)
	(empty t883)
	(empty t884)
	(empty t885)
	(empty t886)
	(empty t887)
	(empty t888)
	(empty t889)
	(empty t890)
	(empty t891)
	(empty t892)
	(empty t893)
	(empty t894)
	(empty t895)
	(empty t896)
	(empty t897)
	(empty t898)
	(empty t899)
	(empty t900)
	(empty t901)
	(empty t902)
	(empty t903)
	(empty t904)
	(empty t905)
	(empty t906)
	(empty t907)
	(empty t908)
	(empty t909)
	(empty t910)
	(empty t911)
	(empty t912)
	(empty t913)
	(empty t914)
	(empty t915)
	(empty t916)
	(empty t917)
	(empty t918)
	(empty t919)
	(empty t920)
	(empty t921)
	(empty t922)
	(empty t923)
	(empty t924)
	(empty t925)
	(empty t926)
	(empty t927)
	(empty t928)
	(empty t929)
	(empty t930)
	(empty t931)
	(empty t932)
	(empty t933)
	(empty t934)
	(empty t935)
	(empty t936)
	(empty t937)
	(empty t938)
	(empty t939)
	(empty t940)
	(empty t941)
	(empty t942)
	(empty t943)
	(empty t944)
	(empty t945)
	(empty t946)
	(empty t947)
	(empty t948)
	(empty t949)
	(empty t950)
	(empty t951)
	(empty t952)
	(empty t953)
	(empty t954)
	(empty t955)
	(empty t956)
	(empty t957)
	(empty t958)
	(empty t959)
	(empty t960)
	(empty t961)
	(empty t962)
	(empty t963)
	(empty t964)
	(empty t965)
	(empty t966)
	(empty t967)
	(empty t968)
	(empty t969)
	(empty t970)
	(empty t971)
	(empty t972)
	(empty t973)
	(empty t974)
	(empty t975)
	(empty t976)
	(empty t977)
	(empty t978)
	(empty t979)
	(empty t980)
	(empty t981)
	(empty t982)
	(empty t983)
	(empty t984)
	(empty t985)
	(empty t986)
	(empty t987)
	(empty t988)
	(empty t989)
	(empty t990)
	(empty t991)
	(empty t992)
	(empty t993)
	(empty t994)
	(empty t995)
	(empty t996)
	(empty t997)
	(empty t998)
	(empty t999)
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
	(east t399 t400)
	(west t400 t399)
	(east t400 t401)
	(west t401 t400)
	(east t401 t402)
	(west t402 t401)
	(east t402 t403)
	(west t403 t402)
	(east t403 t404)
	(west t404 t403)
	(east t404 t405)
	(west t405 t404)
	(east t405 t406)
	(west t406 t405)
	(east t406 t407)
	(west t407 t406)
	(east t407 t408)
	(west t408 t407)
	(east t408 t409)
	(west t409 t408)
	(east t409 t410)
	(west t410 t409)
	(east t410 t411)
	(west t411 t410)
	(east t411 t412)
	(west t412 t411)
	(east t412 t413)
	(west t413 t412)
	(east t413 t414)
	(west t414 t413)
	(east t414 t415)
	(west t415 t414)
	(east t415 t416)
	(west t416 t415)
	(east t416 t417)
	(west t417 t416)
	(east t417 t418)
	(west t418 t417)
	(east t418 t419)
	(west t419 t418)
	(east t419 t420)
	(west t420 t419)
	(east t420 t421)
	(west t421 t420)
	(east t421 t422)
	(west t422 t421)
	(east t422 t423)
	(west t423 t422)
	(east t423 t424)
	(west t424 t423)
	(east t424 t425)
	(west t425 t424)
	(east t425 t426)
	(west t426 t425)
	(east t426 t427)
	(west t427 t426)
	(east t427 t428)
	(west t428 t427)
	(east t428 t429)
	(west t429 t428)
	(east t429 t430)
	(west t430 t429)
	(east t430 t431)
	(west t431 t430)
	(east t431 t432)
	(west t432 t431)
	(east t432 t433)
	(west t433 t432)
	(east t433 t434)
	(west t434 t433)
	(east t434 t435)
	(west t435 t434)
	(east t435 t436)
	(west t436 t435)
	(east t436 t437)
	(west t437 t436)
	(east t437 t438)
	(west t438 t437)
	(east t438 t439)
	(west t439 t438)
	(east t439 t440)
	(west t440 t439)
	(east t440 t441)
	(west t441 t440)
	(east t441 t442)
	(west t442 t441)
	(east t442 t443)
	(west t443 t442)
	(east t443 t444)
	(west t444 t443)
	(east t444 t445)
	(west t445 t444)
	(east t445 t446)
	(west t446 t445)
	(east t446 t447)
	(west t447 t446)
	(east t447 t448)
	(west t448 t447)
	(east t448 t449)
	(west t449 t448)
	(east t449 t450)
	(west t450 t449)
	(east t450 t451)
	(west t451 t450)
	(east t451 t452)
	(west t452 t451)
	(east t452 t453)
	(west t453 t452)
	(east t453 t454)
	(west t454 t453)
	(east t454 t455)
	(west t455 t454)
	(east t455 t456)
	(west t456 t455)
	(east t456 t457)
	(west t457 t456)
	(east t457 t458)
	(west t458 t457)
	(east t458 t459)
	(west t459 t458)
	(east t459 t460)
	(west t460 t459)
	(east t460 t461)
	(west t461 t460)
	(east t461 t462)
	(west t462 t461)
	(east t462 t463)
	(west t463 t462)
	(east t463 t464)
	(west t464 t463)
	(east t464 t465)
	(west t465 t464)
	(east t465 t466)
	(west t466 t465)
	(east t466 t467)
	(west t467 t466)
	(east t467 t468)
	(west t468 t467)
	(east t468 t469)
	(west t469 t468)
	(east t469 t470)
	(west t470 t469)
	(east t470 t471)
	(west t471 t470)
	(east t471 t472)
	(west t472 t471)
	(east t472 t473)
	(west t473 t472)
	(east t473 t474)
	(west t474 t473)
	(east t474 t475)
	(west t475 t474)
	(east t475 t476)
	(west t476 t475)
	(east t476 t477)
	(west t477 t476)
	(east t477 t478)
	(west t478 t477)
	(east t478 t479)
	(west t479 t478)
	(east t479 t480)
	(west t480 t479)
	(east t480 t481)
	(west t481 t480)
	(east t481 t482)
	(west t482 t481)
	(east t482 t483)
	(west t483 t482)
	(east t483 t484)
	(west t484 t483)
	(east t484 t485)
	(west t485 t484)
	(east t485 t486)
	(west t486 t485)
	(east t486 t487)
	(west t487 t486)
	(east t487 t488)
	(west t488 t487)
	(east t488 t489)
	(west t489 t488)
	(east t489 t490)
	(west t490 t489)
	(east t490 t491)
	(west t491 t490)
	(east t491 t492)
	(west t492 t491)
	(east t492 t493)
	(west t493 t492)
	(east t493 t494)
	(west t494 t493)
	(east t494 t495)
	(west t495 t494)
	(east t495 t496)
	(west t496 t495)
	(east t496 t497)
	(west t497 t496)
	(east t497 t498)
	(west t498 t497)
	(east t498 t499)
	(west t499 t498)
	(east t499 t500)
	(west t500 t499)
	(east t500 t501)
	(west t501 t500)
	(east t501 t502)
	(west t502 t501)
	(east t502 t503)
	(west t503 t502)
	(east t503 t504)
	(west t504 t503)
	(east t504 t505)
	(west t505 t504)
	(east t505 t506)
	(west t506 t505)
	(east t506 t507)
	(west t507 t506)
	(east t507 t508)
	(west t508 t507)
	(east t508 t509)
	(west t509 t508)
	(east t509 t510)
	(west t510 t509)
	(east t510 t511)
	(west t511 t510)
	(east t511 t512)
	(west t512 t511)
	(east t512 t513)
	(west t513 t512)
	(east t513 t514)
	(west t514 t513)
	(east t514 t515)
	(west t515 t514)
	(east t515 t516)
	(west t516 t515)
	(east t516 t517)
	(west t517 t516)
	(east t517 t518)
	(west t518 t517)
	(east t518 t519)
	(west t519 t518)
	(east t519 t520)
	(west t520 t519)
	(east t520 t521)
	(west t521 t520)
	(east t521 t522)
	(west t522 t521)
	(east t522 t523)
	(west t523 t522)
	(east t523 t524)
	(west t524 t523)
	(east t524 t525)
	(west t525 t524)
	(east t525 t526)
	(west t526 t525)
	(east t526 t527)
	(west t527 t526)
	(east t527 t528)
	(west t528 t527)
	(east t528 t529)
	(west t529 t528)
	(east t529 t530)
	(west t530 t529)
	(east t530 t531)
	(west t531 t530)
	(east t531 t532)
	(west t532 t531)
	(east t532 t533)
	(west t533 t532)
	(east t533 t534)
	(west t534 t533)
	(east t534 t535)
	(west t535 t534)
	(east t535 t536)
	(west t536 t535)
	(east t536 t537)
	(west t537 t536)
	(east t537 t538)
	(west t538 t537)
	(east t538 t539)
	(west t539 t538)
	(east t539 t540)
	(west t540 t539)
	(east t540 t541)
	(west t541 t540)
	(east t541 t542)
	(west t542 t541)
	(east t542 t543)
	(west t543 t542)
	(east t543 t544)
	(west t544 t543)
	(east t544 t545)
	(west t545 t544)
	(east t545 t546)
	(west t546 t545)
	(east t546 t547)
	(west t547 t546)
	(east t547 t548)
	(west t548 t547)
	(east t548 t549)
	(west t549 t548)
	(east t549 t550)
	(west t550 t549)
	(east t550 t551)
	(west t551 t550)
	(east t551 t552)
	(west t552 t551)
	(east t552 t553)
	(west t553 t552)
	(east t553 t554)
	(west t554 t553)
	(east t554 t555)
	(west t555 t554)
	(east t555 t556)
	(west t556 t555)
	(east t556 t557)
	(west t557 t556)
	(east t557 t558)
	(west t558 t557)
	(east t558 t559)
	(west t559 t558)
	(east t559 t560)
	(west t560 t559)
	(east t560 t561)
	(west t561 t560)
	(east t561 t562)
	(west t562 t561)
	(east t562 t563)
	(west t563 t562)
	(east t563 t564)
	(west t564 t563)
	(east t564 t565)
	(west t565 t564)
	(east t565 t566)
	(west t566 t565)
	(east t566 t567)
	(west t567 t566)
	(east t567 t568)
	(west t568 t567)
	(east t568 t569)
	(west t569 t568)
	(east t569 t570)
	(west t570 t569)
	(east t570 t571)
	(west t571 t570)
	(east t571 t572)
	(west t572 t571)
	(east t572 t573)
	(west t573 t572)
	(east t573 t574)
	(west t574 t573)
	(east t574 t575)
	(west t575 t574)
	(east t575 t576)
	(west t576 t575)
	(east t576 t577)
	(west t577 t576)
	(east t577 t578)
	(west t578 t577)
	(east t578 t579)
	(west t579 t578)
	(east t579 t580)
	(west t580 t579)
	(east t580 t581)
	(west t581 t580)
	(east t581 t582)
	(west t582 t581)
	(east t582 t583)
	(west t583 t582)
	(east t583 t584)
	(west t584 t583)
	(east t584 t585)
	(west t585 t584)
	(east t585 t586)
	(west t586 t585)
	(east t586 t587)
	(west t587 t586)
	(east t587 t588)
	(west t588 t587)
	(east t588 t589)
	(west t589 t588)
	(east t589 t590)
	(west t590 t589)
	(east t590 t591)
	(west t591 t590)
	(east t591 t592)
	(west t592 t591)
	(east t592 t593)
	(west t593 t592)
	(east t593 t594)
	(west t594 t593)
	(east t594 t595)
	(west t595 t594)
	(east t595 t596)
	(west t596 t595)
	(east t596 t597)
	(west t597 t596)
	(east t597 t598)
	(west t598 t597)
	(east t598 t599)
	(west t599 t598)
	(east t599 t600)
	(west t600 t599)
	(east t600 t601)
	(west t601 t600)
	(east t601 t602)
	(west t602 t601)
	(east t602 t603)
	(west t603 t602)
	(east t603 t604)
	(west t604 t603)
	(east t604 t605)
	(west t605 t604)
	(east t605 t606)
	(west t606 t605)
	(east t606 t607)
	(west t607 t606)
	(east t607 t608)
	(west t608 t607)
	(east t608 t609)
	(west t609 t608)
	(east t609 t610)
	(west t610 t609)
	(east t610 t611)
	(west t611 t610)
	(east t611 t612)
	(west t612 t611)
	(east t612 t613)
	(west t613 t612)
	(east t613 t614)
	(west t614 t613)
	(east t614 t615)
	(west t615 t614)
	(east t615 t616)
	(west t616 t615)
	(east t616 t617)
	(west t617 t616)
	(east t617 t618)
	(west t618 t617)
	(east t618 t619)
	(west t619 t618)
	(east t619 t620)
	(west t620 t619)
	(east t620 t621)
	(west t621 t620)
	(east t621 t622)
	(west t622 t621)
	(east t622 t623)
	(west t623 t622)
	(east t623 t624)
	(west t624 t623)
	(east t624 t625)
	(west t625 t624)
	(east t625 t626)
	(west t626 t625)
	(east t626 t627)
	(west t627 t626)
	(east t627 t628)
	(west t628 t627)
	(east t628 t629)
	(west t629 t628)
	(east t629 t630)
	(west t630 t629)
	(east t630 t631)
	(west t631 t630)
	(east t631 t632)
	(west t632 t631)
	(east t632 t633)
	(west t633 t632)
	(east t633 t634)
	(west t634 t633)
	(east t634 t635)
	(west t635 t634)
	(east t635 t636)
	(west t636 t635)
	(east t636 t637)
	(west t637 t636)
	(east t637 t638)
	(west t638 t637)
	(east t638 t639)
	(west t639 t638)
	(east t639 t640)
	(west t640 t639)
	(east t640 t641)
	(west t641 t640)
	(east t641 t642)
	(west t642 t641)
	(east t642 t643)
	(west t643 t642)
	(east t643 t644)
	(west t644 t643)
	(east t644 t645)
	(west t645 t644)
	(east t645 t646)
	(west t646 t645)
	(east t646 t647)
	(west t647 t646)
	(east t647 t648)
	(west t648 t647)
	(east t648 t649)
	(west t649 t648)
	(east t649 t650)
	(west t650 t649)
	(east t650 t651)
	(west t651 t650)
	(east t651 t652)
	(west t652 t651)
	(east t652 t653)
	(west t653 t652)
	(east t653 t654)
	(west t654 t653)
	(east t654 t655)
	(west t655 t654)
	(east t655 t656)
	(west t656 t655)
	(east t656 t657)
	(west t657 t656)
	(east t657 t658)
	(west t658 t657)
	(east t658 t659)
	(west t659 t658)
	(east t659 t660)
	(west t660 t659)
	(east t660 t661)
	(west t661 t660)
	(east t661 t662)
	(west t662 t661)
	(east t662 t663)
	(west t663 t662)
	(east t663 t664)
	(west t664 t663)
	(east t664 t665)
	(west t665 t664)
	(east t665 t666)
	(west t666 t665)
	(east t666 t667)
	(west t667 t666)
	(east t667 t668)
	(west t668 t667)
	(east t668 t669)
	(west t669 t668)
	(east t669 t670)
	(west t670 t669)
	(east t670 t671)
	(west t671 t670)
	(east t671 t672)
	(west t672 t671)
	(east t672 t673)
	(west t673 t672)
	(east t673 t674)
	(west t674 t673)
	(east t674 t675)
	(west t675 t674)
	(east t675 t676)
	(west t676 t675)
	(east t676 t677)
	(west t677 t676)
	(east t677 t678)
	(west t678 t677)
	(east t678 t679)
	(west t679 t678)
	(east t679 t680)
	(west t680 t679)
	(east t680 t681)
	(west t681 t680)
	(east t681 t682)
	(west t682 t681)
	(east t682 t683)
	(west t683 t682)
	(east t683 t684)
	(west t684 t683)
	(east t684 t685)
	(west t685 t684)
	(east t685 t686)
	(west t686 t685)
	(east t686 t687)
	(west t687 t686)
	(east t687 t688)
	(west t688 t687)
	(east t688 t689)
	(west t689 t688)
	(east t689 t690)
	(west t690 t689)
	(east t690 t691)
	(west t691 t690)
	(east t691 t692)
	(west t692 t691)
	(east t692 t693)
	(west t693 t692)
	(east t693 t694)
	(west t694 t693)
	(east t694 t695)
	(west t695 t694)
	(east t695 t696)
	(west t696 t695)
	(east t696 t697)
	(west t697 t696)
	(east t697 t698)
	(west t698 t697)
	(east t698 t699)
	(west t699 t698)
	(east t699 t700)
	(west t700 t699)
	(east t700 t701)
	(west t701 t700)
	(east t701 t702)
	(west t702 t701)
	(east t702 t703)
	(west t703 t702)
	(east t703 t704)
	(west t704 t703)
	(east t704 t705)
	(west t705 t704)
	(east t705 t706)
	(west t706 t705)
	(east t706 t707)
	(west t707 t706)
	(east t707 t708)
	(west t708 t707)
	(east t708 t709)
	(west t709 t708)
	(east t709 t710)
	(west t710 t709)
	(east t710 t711)
	(west t711 t710)
	(east t711 t712)
	(west t712 t711)
	(east t712 t713)
	(west t713 t712)
	(east t713 t714)
	(west t714 t713)
	(east t714 t715)
	(west t715 t714)
	(east t715 t716)
	(west t716 t715)
	(east t716 t717)
	(west t717 t716)
	(east t717 t718)
	(west t718 t717)
	(east t718 t719)
	(west t719 t718)
	(east t719 t720)
	(west t720 t719)
	(east t720 t721)
	(west t721 t720)
	(east t721 t722)
	(west t722 t721)
	(east t722 t723)
	(west t723 t722)
	(east t723 t724)
	(west t724 t723)
	(east t724 t725)
	(west t725 t724)
	(east t725 t726)
	(west t726 t725)
	(east t726 t727)
	(west t727 t726)
	(east t727 t728)
	(west t728 t727)
	(east t728 t729)
	(west t729 t728)
	(east t729 t730)
	(west t730 t729)
	(east t730 t731)
	(west t731 t730)
	(east t731 t732)
	(west t732 t731)
	(east t732 t733)
	(west t733 t732)
	(east t733 t734)
	(west t734 t733)
	(east t734 t735)
	(west t735 t734)
	(east t735 t736)
	(west t736 t735)
	(east t736 t737)
	(west t737 t736)
	(east t737 t738)
	(west t738 t737)
	(east t738 t739)
	(west t739 t738)
	(east t739 t740)
	(west t740 t739)
	(east t740 t741)
	(west t741 t740)
	(east t741 t742)
	(west t742 t741)
	(east t742 t743)
	(west t743 t742)
	(east t743 t744)
	(west t744 t743)
	(east t744 t745)
	(west t745 t744)
	(east t745 t746)
	(west t746 t745)
	(east t746 t747)
	(west t747 t746)
	(east t747 t748)
	(west t748 t747)
	(east t748 t749)
	(west t749 t748)
	(east t749 t750)
	(west t750 t749)
	(east t750 t751)
	(west t751 t750)
	(east t751 t752)
	(west t752 t751)
	(east t752 t753)
	(west t753 t752)
	(east t753 t754)
	(west t754 t753)
	(east t754 t755)
	(west t755 t754)
	(east t755 t756)
	(west t756 t755)
	(east t756 t757)
	(west t757 t756)
	(east t757 t758)
	(west t758 t757)
	(east t758 t759)
	(west t759 t758)
	(east t759 t760)
	(west t760 t759)
	(east t760 t761)
	(west t761 t760)
	(east t761 t762)
	(west t762 t761)
	(east t762 t763)
	(west t763 t762)
	(east t763 t764)
	(west t764 t763)
	(east t764 t765)
	(west t765 t764)
	(east t765 t766)
	(west t766 t765)
	(east t766 t767)
	(west t767 t766)
	(east t767 t768)
	(west t768 t767)
	(east t768 t769)
	(west t769 t768)
	(east t769 t770)
	(west t770 t769)
	(east t770 t771)
	(west t771 t770)
	(east t771 t772)
	(west t772 t771)
	(east t772 t773)
	(west t773 t772)
	(east t773 t774)
	(west t774 t773)
	(east t774 t775)
	(west t775 t774)
	(east t775 t776)
	(west t776 t775)
	(east t776 t777)
	(west t777 t776)
	(east t777 t778)
	(west t778 t777)
	(east t778 t779)
	(west t779 t778)
	(east t779 t780)
	(west t780 t779)
	(east t780 t781)
	(west t781 t780)
	(east t781 t782)
	(west t782 t781)
	(east t782 t783)
	(west t783 t782)
	(east t783 t784)
	(west t784 t783)
	(east t784 t785)
	(west t785 t784)
	(east t785 t786)
	(west t786 t785)
	(east t786 t787)
	(west t787 t786)
	(east t787 t788)
	(west t788 t787)
	(east t788 t789)
	(west t789 t788)
	(east t789 t790)
	(west t790 t789)
	(east t790 t791)
	(west t791 t790)
	(east t791 t792)
	(west t792 t791)
	(east t792 t793)
	(west t793 t792)
	(east t793 t794)
	(west t794 t793)
	(east t794 t795)
	(west t795 t794)
	(east t795 t796)
	(west t796 t795)
	(east t796 t797)
	(west t797 t796)
	(east t797 t798)
	(west t798 t797)
	(east t798 t799)
	(west t799 t798)
	(east t799 t800)
	(west t800 t799)
	(east t800 t801)
	(west t801 t800)
	(east t801 t802)
	(west t802 t801)
	(east t802 t803)
	(west t803 t802)
	(east t803 t804)
	(west t804 t803)
	(east t804 t805)
	(west t805 t804)
	(east t805 t806)
	(west t806 t805)
	(east t806 t807)
	(west t807 t806)
	(east t807 t808)
	(west t808 t807)
	(east t808 t809)
	(west t809 t808)
	(east t809 t810)
	(west t810 t809)
	(east t810 t811)
	(west t811 t810)
	(east t811 t812)
	(west t812 t811)
	(east t812 t813)
	(west t813 t812)
	(east t813 t814)
	(west t814 t813)
	(east t814 t815)
	(west t815 t814)
	(east t815 t816)
	(west t816 t815)
	(east t816 t817)
	(west t817 t816)
	(east t817 t818)
	(west t818 t817)
	(east t818 t819)
	(west t819 t818)
	(east t819 t820)
	(west t820 t819)
	(east t820 t821)
	(west t821 t820)
	(east t821 t822)
	(west t822 t821)
	(east t822 t823)
	(west t823 t822)
	(east t823 t824)
	(west t824 t823)
	(east t824 t825)
	(west t825 t824)
	(east t825 t826)
	(west t826 t825)
	(east t826 t827)
	(west t827 t826)
	(east t827 t828)
	(west t828 t827)
	(east t828 t829)
	(west t829 t828)
	(east t829 t830)
	(west t830 t829)
	(east t830 t831)
	(west t831 t830)
	(east t831 t832)
	(west t832 t831)
	(east t832 t833)
	(west t833 t832)
	(east t833 t834)
	(west t834 t833)
	(east t834 t835)
	(west t835 t834)
	(east t835 t836)
	(west t836 t835)
	(east t836 t837)
	(west t837 t836)
	(east t837 t838)
	(west t838 t837)
	(east t838 t839)
	(west t839 t838)
	(east t839 t840)
	(west t840 t839)
	(east t840 t841)
	(west t841 t840)
	(east t841 t842)
	(west t842 t841)
	(east t842 t843)
	(west t843 t842)
	(east t843 t844)
	(west t844 t843)
	(east t844 t845)
	(west t845 t844)
	(east t845 t846)
	(west t846 t845)
	(east t846 t847)
	(west t847 t846)
	(east t847 t848)
	(west t848 t847)
	(east t848 t849)
	(west t849 t848)
	(east t849 t850)
	(west t850 t849)
	(east t850 t851)
	(west t851 t850)
	(east t851 t852)
	(west t852 t851)
	(east t852 t853)
	(west t853 t852)
	(east t853 t854)
	(west t854 t853)
	(east t854 t855)
	(west t855 t854)
	(east t855 t856)
	(west t856 t855)
	(east t856 t857)
	(west t857 t856)
	(east t857 t858)
	(west t858 t857)
	(east t858 t859)
	(west t859 t858)
	(east t859 t860)
	(west t860 t859)
	(east t860 t861)
	(west t861 t860)
	(east t861 t862)
	(west t862 t861)
	(east t862 t863)
	(west t863 t862)
	(east t863 t864)
	(west t864 t863)
	(east t864 t865)
	(west t865 t864)
	(east t865 t866)
	(west t866 t865)
	(east t866 t867)
	(west t867 t866)
	(east t867 t868)
	(west t868 t867)
	(east t868 t869)
	(west t869 t868)
	(east t869 t870)
	(west t870 t869)
	(east t870 t871)
	(west t871 t870)
	(east t871 t872)
	(west t872 t871)
	(east t872 t873)
	(west t873 t872)
	(east t873 t874)
	(west t874 t873)
	(east t874 t875)
	(west t875 t874)
	(east t875 t876)
	(west t876 t875)
	(east t876 t877)
	(west t877 t876)
	(east t877 t878)
	(west t878 t877)
	(east t878 t879)
	(west t879 t878)
	(east t879 t880)
	(west t880 t879)
	(east t880 t881)
	(west t881 t880)
	(east t881 t882)
	(west t882 t881)
	(east t882 t883)
	(west t883 t882)
	(east t883 t884)
	(west t884 t883)
	(east t884 t885)
	(west t885 t884)
	(east t885 t886)
	(west t886 t885)
	(east t886 t887)
	(west t887 t886)
	(east t887 t888)
	(west t888 t887)
	(east t888 t889)
	(west t889 t888)
	(east t889 t890)
	(west t890 t889)
	(east t890 t891)
	(west t891 t890)
	(east t891 t892)
	(west t892 t891)
	(east t892 t893)
	(west t893 t892)
	(east t893 t894)
	(west t894 t893)
	(east t894 t895)
	(west t895 t894)
	(east t895 t896)
	(west t896 t895)
	(east t896 t897)
	(west t897 t896)
	(east t897 t898)
	(west t898 t897)
	(east t898 t899)
	(west t899 t898)
	(east t899 t900)
	(west t900 t899)
	(east t900 t901)
	(west t901 t900)
	(east t901 t902)
	(west t902 t901)
	(east t902 t903)
	(west t903 t902)
	(east t903 t904)
	(west t904 t903)
	(east t904 t905)
	(west t905 t904)
	(east t905 t906)
	(west t906 t905)
	(east t906 t907)
	(west t907 t906)
	(east t907 t908)
	(west t908 t907)
	(east t908 t909)
	(west t909 t908)
	(east t909 t910)
	(west t910 t909)
	(east t910 t911)
	(west t911 t910)
	(east t911 t912)
	(west t912 t911)
	(east t912 t913)
	(west t913 t912)
	(east t913 t914)
	(west t914 t913)
	(east t914 t915)
	(west t915 t914)
	(east t915 t916)
	(west t916 t915)
	(east t916 t917)
	(west t917 t916)
	(east t917 t918)
	(west t918 t917)
	(east t918 t919)
	(west t919 t918)
	(east t919 t920)
	(west t920 t919)
	(east t920 t921)
	(west t921 t920)
	(east t921 t922)
	(west t922 t921)
	(east t922 t923)
	(west t923 t922)
	(east t923 t924)
	(west t924 t923)
	(east t924 t925)
	(west t925 t924)
	(east t925 t926)
	(west t926 t925)
	(east t926 t927)
	(west t927 t926)
	(east t927 t928)
	(west t928 t927)
	(east t928 t929)
	(west t929 t928)
	(east t929 t930)
	(west t930 t929)
	(east t930 t931)
	(west t931 t930)
	(east t931 t932)
	(west t932 t931)
	(east t932 t933)
	(west t933 t932)
	(east t933 t934)
	(west t934 t933)
	(east t934 t935)
	(west t935 t934)
	(east t935 t936)
	(west t936 t935)
	(east t936 t937)
	(west t937 t936)
	(east t937 t938)
	(west t938 t937)
	(east t938 t939)
	(west t939 t938)
	(east t939 t940)
	(west t940 t939)
	(east t940 t941)
	(west t941 t940)
	(east t941 t942)
	(west t942 t941)
	(east t942 t943)
	(west t943 t942)
	(east t943 t944)
	(west t944 t943)
	(east t944 t945)
	(west t945 t944)
	(east t945 t946)
	(west t946 t945)
	(east t946 t947)
	(west t947 t946)
	(east t947 t948)
	(west t948 t947)
	(east t948 t949)
	(west t949 t948)
	(east t949 t950)
	(west t950 t949)
	(east t950 t951)
	(west t951 t950)
	(east t951 t952)
	(west t952 t951)
	(east t952 t953)
	(west t953 t952)
	(east t953 t954)
	(west t954 t953)
	(east t954 t955)
	(west t955 t954)
	(east t955 t956)
	(west t956 t955)
	(east t956 t957)
	(west t957 t956)
	(east t957 t958)
	(west t958 t957)
	(east t958 t959)
	(west t959 t958)
	(east t959 t960)
	(west t960 t959)
	(east t960 t961)
	(west t961 t960)
	(east t961 t962)
	(west t962 t961)
	(east t962 t963)
	(west t963 t962)
	(east t963 t964)
	(west t964 t963)
	(east t964 t965)
	(west t965 t964)
	(east t965 t966)
	(west t966 t965)
	(east t966 t967)
	(west t967 t966)
	(east t967 t968)
	(west t968 t967)
	(east t968 t969)
	(west t969 t968)
	(east t969 t970)
	(west t970 t969)
	(east t970 t971)
	(west t971 t970)
	(east t971 t972)
	(west t972 t971)
	(east t972 t973)
	(west t973 t972)
	(east t973 t974)
	(west t974 t973)
	(east t974 t975)
	(west t975 t974)
	(east t975 t976)
	(west t976 t975)
	(east t976 t977)
	(west t977 t976)
	(east t977 t978)
	(west t978 t977)
	(east t978 t979)
	(west t979 t978)
	(east t979 t980)
	(west t980 t979)
	(east t980 t981)
	(west t981 t980)
	(east t981 t982)
	(west t982 t981)
	(east t982 t983)
	(west t983 t982)
	(east t983 t984)
	(west t984 t983)
	(east t984 t985)
	(west t985 t984)
	(east t985 t986)
	(west t986 t985)
	(east t986 t987)
	(west t987 t986)
	(east t987 t988)
	(west t988 t987)
	(east t988 t989)
	(west t989 t988)
	(east t989 t990)
	(west t990 t989)
	(east t990 t991)
	(west t991 t990)
	(east t991 t992)
	(west t992 t991)
	(east t992 t993)
	(west t993 t992)
	(east t993 t994)
	(west t994 t993)
	(east t994 t995)
	(west t995 t994)
	(east t995 t996)
	(west t996 t995)
	(east t996 t997)
	(west t997 t996)
	(east t997 t998)
	(west t998 t997)
	(east t998 t999)
	(west t999 t998)
	(east t999 goal_tile)
	(west goal_tile t999)
    (person person1)
    (at person1 start_tile)   
        )
(:goal 
    (and (at person1 goal_tile))
	)
)
