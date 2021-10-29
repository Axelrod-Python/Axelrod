# v4.12.0, 2021-05-25

New documentation structure, new strategy and ability to pass a custom match to
the Moran class.

- Move documentation to diataxis framework
  https://github.com/Axelrod-Python/Axelrod/pull/1391
- Add the CAPRI strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1393
- Add custom matches to Moran process
  https://github.com/Axelrod-Python/Axelrod/pull/1397
- Update CITATIONS.md
  https://github.com/Axelrod-Python/Axelrod/pull/1389
- Fix contributor documentation links
  https://github.com/Axelrod-Python/Axelrod/pull/1396

https://github.com/Axelrod-Python/Axelrod/compare/v4.12.0...v4.11.0

# v4.11.0, 2021-05-25

A number of improvements to documentation, a new strategy, removing the cheating
strategies and a number of internal fixes.

- Use black style formatting
  https://github.com/Axelrod-Python/Axelrod/pull/1368
- Move to `dev` as main branch
  https://github.com/Axelrod-Python/Axelrod/pull/1367
- Tests refactor
  https://github.com/Axelrod-Python/Axelrod/pull/1372
  https://github.com/Axelrod-Python/Axelrod/pull/1373
- Improved docstrings
  https://github.com/Axelrod-Python/Axelrod/pull/1377
  https://github.com/Axelrod-Python/Axelrod/pull/1381
- Add publications
  https://github.com/Axelrod-Python/Axelrod/pull/1378
  https://github.com/Axelrod-Python/Axelrod/pull/1384
- Bump pyaml
  https://github.com/Axelrod-Python/Axelrod/pull/1380
- Add new FSM
  https://github.com/Axelrod-Python/Axelrod/pull/1383
- Update some type hinting
  https://github.com/Axelrod-Python/Axelrod/pull/1385
- Remove cheating strategies
  https://github.com/Axelrod-Python/Axelrod/pull/1388

https://github.com/Axelrod-Python/Axelrod/compare/v4.11.0...v4.10.0

# v4.10.0, 2020-08-12

Major rewrite of the random seeding (which fixes a reproducibility bug when
using parallel processing), support for python 3.8 and various
documentation/internal fixes.

- Move CI to github actions
  https://github.com/Axelrod-Python/Axelrod/pull/1309
  https://github.com/Axelrod-Python/Axelrod/pull/1322
  https://github.com/Axelrod-Python/Axelrod/pull/1327
- Sort all import statements using isort
  https://github.com/Axelrod-Python/Axelrod/pull/1351
- Add a test that all strategies have names
  https://github.com/Axelrod-Python/Axelrod/pull/1354
- Add a function to automatically check what information is used by strategies
  https://github.com/Axelrod-Python/Axelrod/pull/1355
  https://github.com/Axelrod-Python/Axelrod/pull/1331
- Minor documentation fixes
  https://github.com/Axelrod-Python/Axelrod/pull/1321
  https://github.com/Axelrod-Python/Axelrod/pull/1329
  https://github.com/Axelrod-Python/Axelrod/pull/1357
  https://github.com/Axelrod-Python/Axelrod/pull/1358
  https://github.com/Axelrod-Python/Axelrod/pull/1363
- Add python 3.8 support
  https://github.com/Axelrod-Python/Axelrod/pull/1366
- Improve tests
  https://github.com/Axelrod-Python/Axelrod/pull/1332
  https://github.com/Axelrod-Python/Axelrod/pull/1333
  https://github.com/Axelrod-Python/Axelrod/pull/1359
- Fix RevisedDowning
  https://github.com/Axelrod-Python/Axelrod/pull/1323

https://github.com/Axelrod-Python/Axelrod/compare/v4.10.0...v4.9.1

# v4.9.1, 2020-04-08

Bug fixes

- Fix install problem:
  https://github.com/Axelrod-Python/Axelrod/pull/1314
- Fix read the docs configuration:
  https://github.com/Axelrod-Python/Axelrod/pull/1313

https://github.com/Axelrod-Python/Axelrod/compare/v4.9.1...v4.9.0

# v4.9.0, 2020-04-07

New strategies, new classifier system and internal improvements/fixes.

- Cleanup the tests:
  https://github.com/Axelrod-Python/Axelrod/pull/1308
- Create function to handle internal file paths:
  https://github.com/Axelrod-Python/Axelrod/pull/1307
- Fix bug in Result set:
  https://github.com/Axelrod-Python/Axelrod/pull/1305
- Improve and expand LR Player's docstring
  https://github.com/Axelrod-Python/Axelrod/pull/1303
- New strategy classifier mechanism:
  https://github.com/Axelrod-Python/Axelrod/pull/1300
- Add new Gradual strategy:
  https://github.com/Axelrod-Python/Axelrod/pull/1299
- Add missing author to docs bibliography:
  https://github.com/Axelrod-Python/Axelrod/pull/1295
- Suppress numpy warnings:
  https://github.com/Axelrod-Python/Axelrod/pull/1292
- Fix documentation:
  https://github.com/Axelrod-Python/Axelrod/pull/1291
- Fix FirstByDowning:
  https://github.com/Axelrod-Python/Axelrod/pull/1285
- Add citations:
  https://github.com/Axelrod-Python/Axelrod/pull/1281

https://github.com/Axelrod-Python/Axelrod/compare/v4.9.0...v4.8.0

# v4.8.0, 2019-12-16

Reimplementation of first tournament strategies, rename of second tournament
strategies and

- Reimplement and rename first tournament strategies and rename second
  tournament strategies:
  https://github.com/Axelrod-Python/Axelrod/pull/1275
- Update citations:
  https://github.com/Axelrod-Python/Axelrod/pull/1276
  https://github.com/Axelrod-Python/Axelrod/pull/1278
- Add Detective strategy:
  https://github.com/Axelrod-Python/Axelrod/pull/1269
- Remove Fool Me Forever (duplicate):
  https://github.com/Axelrod-Python/Axelrod/pull/1274
- Add documentation to a testing script:
  https://github.com/Axelrod-Python/Axelrod/pull/1271
- Fix documentation render:
  https://github.com/Axelrod-Python/Axelrod/pull/1268

https://github.com/Axelrod-Python/Axelrod/compare/v4.8.0...v4.7.0

# v4.7.0, 2019-10-23

New Moran process mechanics, new strategy implementations, drop support for
python 3.5 and various minor fixes.

- Drop support for python 3.5:
  https://github.com/Axelrod-Python/Axelrod/pull/1255
  https://github.com/Axelrod-Python/Axelrod/pull/1254
- New strategies:
  https://github.com/Axelrod-Python/Axelrod/pull/1263
- Bug fix:
  https://github.com/Axelrod-Python/Axelrod/pull/1260
- Documentation fixes:
  https://github.com/Axelrod-Python/Axelrod/pull/1266
  https://github.com/Axelrod-Python/Axelrod/pull/1262
- Implement Evolvable Player for Moran processes:
  https://github.com/Axelrod-Python/Axelrod/pull/1267
  https://github.com/Axelrod-Python/Axelrod/pull/1256
- Update citations: https://github.com/Axelrod-Python/Axelrod/pull/1249

https://github.com/Axelrod-Python/Axelrod/compare/v4.7.0...v4.6.0

# v4.6.0, 2019-05-20

New history class, new strategy from Axelrod's first tournament and a number of
internal fixes/improvements.

- A new history class: https://github.com/Axelrod-Python/Axelrod/pull/1241
- Minor internal fixes: https://github.com/Axelrod-Python/Axelrod/pull/1236
  https://github.com/Axelrod-Python/Axelrod/pull/1237
  https://github.com/Axelrod-Python/Axelrod/pull/1243
- Test speed up and refactor:
  https://github.com/Axelrod-Python/Axelrod/pull/1238
- New strategy (Graaskamp from RA's first tournament):
  https://github.com/Axelrod-Python/Axelrod/pull/1244

https://github.com/Axelrod-Python/Axelrod/compare/v4.6.0...v4.5.0

# v4.5.0, 2019-01-31

Implemented algorithm for memory depth of Finite State Machines, some new
strategies  and some minor internal improvements.

- Algorithm for memory depth of Finite State machines
  https://github.com/Axelrod-Python/Axelrod/pull/1233
- Minor refactoring
  https://github.com/Axelrod-Python/Axelrod/pull/1223
  https://github.com/Axelrod-Python/Axelrod/pull/1227
  https://github.com/Axelrod-Python/Axelrod/pull/1225
  https://github.com/Axelrod-Python/Axelrod/pull/1222
- Speed up of cache
  https://github.com/Axelrod-Python/Axelrod/pull/1229
- New strategies
  https://github.com/Axelrod-Python/Axelrod/pull/1228
  https://github.com/Axelrod-Python/Axelrod/pull/1231

https://github.com/Axelrod-Python/Axelrod/compare/v4.5.0...v4.4.0

# v4.4.0, 2018-10-30

2 new strategies and internal refactoring.

- Clean citations of library
  https://github.com/Axelrod-Python/Axelrod/pull/1221
  https://github.com/Axelrod-Python/Axelrod/pull/1220
- Fix numpy depreciation warnings
  https://github.com/Axelrod-Python/Axelrod/pull/1218
- Code refactoring
  https://github.com/Axelrod-Python/Axelrod/pull/1204
  https://github.com/Axelrod-Python/Axelrod/pull/1205
  https://github.com/Axelrod-Python/Axelrod/pull/1206
  https://github.com/Axelrod-Python/Axelrod/pull/1208
  https://github.com/Axelrod-Python/Axelrod/pull/1210
  https://github.com/Axelrod-Python/Axelrod/pull/1212
  https://github.com/Axelrod-Python/Axelrod/pull/1216
  https://github.com/Axelrod-Python/Axelrod/pull/1219
- Two new strategies
  https://github.com/Axelrod-Python/Axelrod/pull/1215

https://github.com/Axelrod-Python/Axelrod/compare/v4.4.0...v4.3.0

# v4.3.0, 2018-08-30

Big code base cleanup, ability to pass a fitness transform to the Moran process,
minor bug fixes.

- Use black and isort on entire library:
  https://github.com/Axelrod-Python/Axelrod/pull/1203
- Refactor of actions modules:
  https://github.com/Axelrod-Python/Axelrod/pull/1193
- Refactor of deterministic cache, ecosystem and eigen:
  https://github.com/Axelrod-Python/Axelrod/pull/1197
  https://github.com/Axelrod-Python/Axelrod/pull/1195
- Refactor strategy utils module:
  https://github.com/Axelrod-Python/Axelrod/pull/1196
- Order Actions: https://github.com/Axelrod-Python/Axelrod/pull/1199
- Add ability to pass fitness transformation to Moran process:
  https://github.com/Axelrod-Python/Axelrod/pull/1198
- Add a matplotlibrc for testing purposes:
  https://github.com/Axelrod-Python/Axelrod/pull/1194
  https://github.com/Axelrod-Python/Axelrod/pull/1191
- Add a page of citations: https://github.com/Axelrod-Python/Axelrod/pull/1188
- Fix bug in lookerup players:
  https://github.com/Axelrod-Python/Axelrod/pull/1190
- Fix bug in graphs: https://github.com/Axelrod-Python/Axelrod/pull/1189
- Tweak a random test seed: https://github.com/Axelrod-Python/Axelrod/pull/1201

https://github.com/Axelrod-Python/Axelrod/compare/v4.3.0...v4.2.2

# v4.2.2, 2018-07-30

Update of training weights for neural network strategy

- Update training weights
  https://github.com/Axelrod-Python/Axelrod/pull/1182

https://github.com/Axelrod-Python/Axelrod/compare/v4.2.2...v4.2.1

# v4.2.1, 2018-07-09

Minor internal fixes.

- Add an upper bound for a dependency version
  https://github.com/Axelrod-Python/Axelrod/pull/1184
- Add a long markdown description for pypi
  https://github.com/Axelrod-Python/Axelrod/pull/1179

https://github.com/Axelrod-Python/Axelrod/compare/v4.2.1...v4.2.0

# v4.2.0, 2018-05-25

New strategies and minor internal fixes.

- Add implementation of generic memory 2 strategy and 2 new strategies
  https://github.com/Axelrod-Python/Axelrod/pull/1171
- Add Tricky Level Punisher
  https://github.com/Axelrod-Python/Axelrod/pull/1178
- Remove unneeded code
  https://github.com/Axelrod-Python/Axelrod/pull/1173
- Fix type hints to work with mypy 2.1
  https://github.com/Axelrod-Python/Axelrod/pull/1177

https://github.com/Axelrod-Python/Axelrod/compare/v4.2.0...v4.1.0

# v4.1.0, 2018-03-13

New strategy

- Implemented Mikkelson (k66r)
  https://github.com/Axelrod-Python/Axelrod/pull/1167

https://github.com/Axelrod-Python/Axelrod/compare/v4.1.0...v4.0.0

# v4.0.0, 2018-02-07

More efficient tournament result analysis, and 2 new strategies.

- Implemented RichardHufford (k47r)
  https://github.com/Axelrod-Python/Axelrod/pull/1162
- Implemented Yamachi (k64r)
  https://github.com/Axelrod-Python/Axelrod/pull/1163
- Implemented Colbert (k51r)
  https://github.com/Axelrod-Python/Axelrod/pull/1164
- Re write the result set
  https://github.com/Axelrod-Python/Axelrod/pull/1166

https://github.com/Axelrod-Python/Axelrod/compare/v4.0.0...v3.11.0

# v3.11.0, 2018-01-09

A number of strategies from Axelrod's original second tournament, new tests and
minor documentation changes.

- Implemented GraaskampKatzen (k60r)
  https://github.com/Axelrod-Python/Axelrod/pull/1144
- Implemented Weiner (k41r)
  https://github.com/Axelrod-Python/Axelrod/pull/1145
- Implemented Harrington (k75r)
  https://github.com/Axelrod-Python/Axelrod/pull/1146
- Implemented MoreTidemanAndChieruzzi (k84r)
  https://github.com/Axelrod-Python/Axelrod/pull/1147
- Implemented Getzler (k35r) strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1151
- Implemented Leyvraz (k86r) strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1153
- Implemented White (k72r) strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1154
- Implemented Black (k83r) strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1155
- Add a test for memory depth
  https://github.com/Axelrod-Python/Axelrod/pull/1157
- Fix implementation of TidemanAndChieruzzi
  https://github.com/Axelrod-Python/Axelrod/pull/1152
- Modify implementation of strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1143
- Update python version requirements
  https://github.com/Axelrod-Python/Axelrod/pull/1158
- Add citations section to README
  https://github.com/Axelrod-Python/Axelrod/pull/1148
  https://github.com/Axelrod-Python/Axelrod/pull/1150

https://github.com/Axelrod-Python/Axelrod/compare/v3.11.0...v3.10.0

# v3.10.0, 2017-11-27

One new strategy

- Add the WmAdams strategy:
  https://github.com/Axelrod-Python/Axelrod/pull/1142

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.10.0...v3.9.0

# v3.9.0, 2017-11-19

New strategies, a minor bug fix and a small documentation improvement.

- Add the Bush Mosteller strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1002
- Add k42r from Fortran code
  https://github.com/Axelrod-Python/Axelrod/pull/1135
- Add MemoryDecay
  https://github.com/Axelrod-Python/Axelrod/pull/1137
- Add k32r from Fortran code
  https://github.com/Axelrod-Python/Axelrod/pull/1138
- Add Random Tit For Tat
  https://github.com/Axelrod-Python/Axelrod/pull/1136
- Add k42r from Fortran code
  https://github.com/Axelrod-Python/Axelrod/pull/1139
- Add reference to documentation
  https://github.com/Axelrod-Python/Axelrod/pull/1134
- Fix minor bug in the fingerprints
  https://github.com/Axelrod-Python/Axelrod/pull/1140


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.9.0...v3.8.1

# v3.8.1, 2017-10-13

Minor change to behaviour of Champion

- This is more in line with the original description of Champion
  https://github.com/Axelrod-Python/Axelrod/pull/1131

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.8.1...v3.8.0

# v3.8.0, 2017-10-10

A new strategy and some bug fixes due to dependency updates

- New strategy MoreGrofman from Axelrod's second tournament
  https://github.com/Axelrod-Python/Axelrod/pull/1124
- Bug fixes due to dependency updates
  https://github.com/Axelrod-Python/Axelrod/pull/1130

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.8.0...v3.7.0

# v3.7.0, 2017-09-05

A new strategy, contributor documentation and internal fixes.

- New strategy Tranqulizer from Axelrod's second tournament:
  https://github.com/Axelrod-Python/Axelrod/pull/1126
- Improved use of `pass_default_arguments` and documentation:
  https://github.com/Axelrod-Python/Axelrod/pull/1127
  https://github.com/Axelrod-Python/Axelrod/pull/1128

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.7.0...v3.6.0

# v3.6.0, 2017-08-26

A new fingerprint mechanism, internal improvements.

- Transitive fingerprints:
  https://github.com/Axelrod-Python/Axelrod/pull/1125
- Add ability to pass game to Moran process
  https://github.com/Axelrod-Python/Axelrod/pull/1122
- Implement a global reset method
  https://github.com/Axelrod-Python/Axelrod/pull/1123

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.6.0...v3.5.0

# v3.5.0, 2017-08-19

Parallel processing now supported on Windows, a new strategy and some minor
improvements.

- Parallel processing now supported on Windows
  https://github.com/Axelrod-Python/Axelrod/pull/1117
- New strategy TidemanAndChieruzzi:
  https://github.com/Axelrod-Python/Axelrod/pull/1118
- Minor change to some tests
  https://github.com/Axelrod-Python/Axelrod/pull/1120

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.5.0...v3.4.0

# v3.4.0, 2017-08-06

A new strategy, internal improvement relevant for pickling, better testing and
minor fixes.

- Gladstein, a strategy by that named author from Axelrod's second tournament
  has been added
  https://github.com/Axelrod-Python/Axelrod/pull/1113
  https://github.com/Axelrod-Python/Axelrod/pull/1110
- Internal improvement for pickling of all strategy classes
  https://github.com/Axelrod-Python/Axelrod/pull/1092
- Better testing of the reset method
  https://github.com/Axelrod-Python/Axelrod/pull/1098
- Minor tweak to a type hint
  https://github.com/Axelrod-Python/Axelrod/pull/1108
- Minor fix to a strategy to match description
  https://github.com/Axelrod-Python/Axelrod/pull/1111

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.4.0...v3.3.0

# v3.3.0, 2017-07-30

4 new strategies and ability to pass game information at the tournament level.

- 3 new zero determinant strategies
  https://github.com/Axelrod-Python/Axelrod/pull/1097
- A memory 2 zero determinant strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1099
- Add ability for tournament to set known match attributes
  https://github.com/Axelrod-Python/Axelrod/pull/1096

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.2.1...v3.3.0

# v3.2.1, 2017-07-28

Documentation fixes.

- Various minor fixes/updates to documentation
  https://github.com/Axelrod-Python/Axelrod/pull/1088
  https://github.com/Axelrod-Python/Axelrod/pull/1089
  https://github.com/Axelrod-Python/Axelrod/pull/1090

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.2.0...v3.2.1

# v3.2.0, 2017-07-26

Minor internal fixes and a new strategy

- New NTitForMTats strategy
  https://github.com/Axelrod-Python/Axelrod/pull/1084
- Pip installing no longer installs hypothesis and tests
  https://github.com/Axelrod-Python/Axelrod/pull/1086
- Remove some code that checked if matplotlib was installed
  https://github.com/Axelrod-Python/Axelrod/pull/1087

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.1.2...v3.2.0

# v3.1.2, 2017-07-24

Minor documentation fixes

- Fixes
  https://github.com/Axelrod-Python/Axelrod/pull/1082
  https://github.com/Axelrod-Python/Axelrod/pull/1083

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.1.1...v3.1.2

# v3.1.1, 2017-07-23

Improvements to documentation and README.

- Re write of the README
  https://github.com/Axelrod-Python/Axelrod/pull/1072
- Fix typos/errors in docs
  https://github.com/Axelrod-Python/Axelrod/pull/1075
  https://github.com/Axelrod-Python/Axelrod/pull/1077
- Big improvement to past tournament documentation reference
  https://github.com/Axelrod-Python/Axelrod/pull/1081
  https://github.com/Axelrod-Python/Axelrod/pull/1080
  https://github.com/Axelrod-Python/Axelrod/pull/1078

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.1.0...v3.1.1

# v3.1.0, 2017-07-16

New class for actions, Internal improvements, a new strategy class,
reclassification of grudger.

- Actions are now an enum class:
  https://github.com/Axelrod-Python/Axelrod/pull/1052
  https://github.com/Axelrod-Python/Axelrod/pull/1053
  https://github.com/Axelrod-Python/Axelrod/pull/1054
- Add explanation of py version to README:
  https://github.com/Axelrod-Python/Axelrod/pull/1056
- Documentation typo fixes:
  https://github.com/Axelrod-Python/Axelrod/pull/1057
- DBS strategy classified as long run time:
  https://github.com/Axelrod-Python/Axelrod/pull/1058
- Correct classification for Grudger:
  https://github.com/Axelrod-Python/Axelrod/pull/1066
- Add another source and name for ALLCorALLD:
  https://github.com/Axelrod-Python/Axelrod/pull/1067
- Update init parameter for lookerup:
  https://github.com/Axelrod-Python/Axelrod/pull/1068
- Add a reactive strategy:
  https://github.com/Axelrod-Python/Axelrod/pull/1070

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v3.0.0...v3.1.0

# v3.0.0, 2017-06-13

A single class for tournaments and Moran processes, sources for all strategies
included in docstrings and internal refactoring,

- The numerous tournament types (prob end, spatial etc) are all now created from
  the `Tournament` class.:
  https://github.com/Axelrod-Python/Axelrod/pull/1042
- The graphical moran processes are now created using the `MoranProcess` class:
  https://github.com/Axelrod-Python/Axelrod/pull/1043
- Sources for all strategies now included in docstrings:
  https://github.com/Axelrod-Python/Axelrod/pull/1041
- Remove some unneeded tests:
  https://github.com/Axelrod-Python/Axelrod/pull/1039
- Further refactoring:
  https://github.com/Axelrod-Python/Axelrod/pull/1044
  https://github.com/Axelrod-Python/Axelrod/pull/1040
  https://github.com/Axelrod-Python/Axelrod/pull/1037

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.13.0...v3.0.0

# v2.13.0, 2017-06-01

New strategies, refactor of strategy tests and minor documentation fixes.

- New strategy Dynamic Two Tits for Tat:
  https://github.com/Axelrod-Python/Axelrod/pull/1030
- New strategy Eugine Nier
  https://github.com/Axelrod-Python/Axelrod/pull/1016
- New strategies: trained FSMs, TF1, TF2, TF3
  https://github.com/Axelrod-Python/Axelrod/pull/1036
- Small documentation fix:
  https://github.com/Axelrod-Python/Axelrod/pull/1022
- Refactor of strategy tests:
  https://github.com/Axelrod-Python/Axelrod/pull/1016
  https://github.com/Axelrod-Python/Axelrod/pull/1021
  https://github.com/Axelrod-Python/Axelrod/pull/1022
  https://github.com/Axelrod-Python/Axelrod/pull/1023
  https://github.com/Axelrod-Python/Axelrod/pull/1024
  https://github.com/Axelrod-Python/Axelrod/pull/1028
  https://github.com/Axelrod-Python/Axelrod/pull/1029
  https://github.com/Axelrod-Python/Axelrod/pull/1030
  https://github.com/Axelrod-Python/Axelrod/pull/1031
  https://github.com/Axelrod-Python/Axelrod/pull/1032
  https://github.com/Axelrod-Python/Axelrod/pull/1033
  https://github.com/Axelrod-Python/Axelrod/pull/1034
  https://github.com/Axelrod-Python/Axelrod/pull/1035

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.12.0...v2.13.0

# v2.12.0, 2017-05-23

New strategies and internal refactoring/improvements

- New strategy Alexei:
  https://github.com/Axelrod-Python/Axelrod/pull/997
- New strategy Stein And Rapaport:
  https://github.com/Axelrod-Python/Axelrod/pull/1012
- Documentation fixes/improvements:
  https://github.com/Axelrod-Python/Axelrod/pull/1020
  https://github.com/Axelrod-Python/Axelrod/pull/1018
  https://github.com/Axelrod-Python/Axelrod/pull/1013
  https://github.com/Axelrod-Python/Axelrod/pull/1011
  https://github.com/Axelrod-Python/Axelrod/pull/1005
  https://github.com/Axelrod-Python/Axelrod/pull/1004
  https://github.com/Axelrod-Python/Axelrod/pull/1003
- Internal refactoring:
  https://github.com/Axelrod-Python/Axelrod/pull/1017
  https://github.com/Axelrod-Python/Axelrod/pull/1015
  https://github.com/Axelrod-Python/Axelrod/pull/1010


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.11.0...v2.12.0

# v2.11.0, 2017-05-06

A new strategy, improvements to documentation, player equality and some
internal refactoring,

- New strategy DBS:
  https://github.com/Axelrod-Python/Axelrod/pull/976
- Documentation improvements:
  https://github.com/Axelrod-Python/Axelrod/pull/995
  https://github.com/Axelrod-Python/Axelrod/pull/1003
- Internal refactoring:
  https://github.com/Axelrod-Python/Axelrod/pull/943
  https://github.com/Axelrod-Python/Axelrod/pull/980
  https://github.com/Axelrod-Python/Axelrod/pull/981
  https://github.com/Axelrod-Python/Axelrod/pull/982
  https://github.com/Axelrod-Python/Axelrod/pull/983
  https://github.com/Axelrod-Python/Axelrod/pull/993
  https://github.com/Axelrod-Python/Axelrod/pull/996
- Add a development testing tool:
  https://github.com/Axelrod-Python/Axelrod/pull/980
- Implement an equality method on players:
  https://github.com/Axelrod-Python/Axelrod/pull/975


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.10.0...v2.11.0

# v2.10.0, 2017-04-17

Bug fix in strategy transformers, new strategy, internal refactor of strategies,
fix bibtex in citation file.

- Fix a bug: ensure strategy transformers also transform classification
  https://github.com/Axelrod-Python/Axelrod/pull/972
- Add DoubleResurrection strategy
  https://github.com/Axelrod-Python/Axelrod/pull/965
- Refactor of LookerUp and Gambler
  https://github.com/Axelrod-Python/Axelrod/pull/966
- Add regression test for FSM players
  https://github.com/Axelrod-Python/Axelrod/pull/967
- Bibtex fix in CITATION.rst
  https://github.com/Axelrod-Python/Axelrod/pull/968

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.09.0...v2.10.0

# v2.9.0, 2017-04-11

Approximate Moran process, test refactor, tweak to the Human play repr,
documentation and an
internal improvement to some cheating strategies.

- Small fix to the repr for the Human strategy:
  https://github.com/Axelrod-Python/Axelrod/pull/959
- Speedup to Geller, Darwin and MindReader
  https://github.com/Axelrod-Python/Axelrod/pull/950
- Add documentation details for running tests
  https://github.com/Axelrod-Python/Axelrod/pull/954
- Add documentation for commit message guidelines:
  https://github.com/Axelrod-Python/Axelrod/pull/963
- Fragment the Moran process documentation
  https://github.com/Axelrod-Python/Axelrod/pull/962
- Add an approximate Moran process
  https://github.com/Axelrod-Python/Axelrod/pull/955
- Test refactor:
  https://github.com/Axelrod-Python/Axelrod/pull/964
- Refactor of the finite state machines:
  https://github.com/Axelrod-Python/Axelrod/pull/956

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.8.0...v2.9.0

# v2.8.0, 2017-04-02

Source code cleanup, test refactor, new strategies and improved `__repr__` of
strategies

- Improved/refactored source code:
  https://github.com/Axelrod-Python/Axelrod/pull/917
  https://github.com/Axelrod-Python/Axelrod/pull/952
- Internal improvement: remove the `init_args` decorator as superseded by the
  `kward_args`:
  https://github.com/Axelrod-Python/Axelrod/pull/918
- Strategy `__repr__` now automatically includes all parameters of a strategy:
  https://github.com/Axelrod-Python/Axelrod/pull/953
  https://github.com/Axelrod-Python/Axelrod/pull/922
- Type hints:
  https://github.com/Axelrod-Python/Axelrod/pull/883
  https://github.com/Axelrod-Python/Axelrod/pull/935
  https://github.com/Axelrod-Python/Axelrod/pull/949
  https://github.com/Axelrod-Python/Axelrod/pull/951
- Refactor of tests:
  https://github.com/Axelrod-Python/Axelrod/pull/924
  https://github.com/Axelrod-Python/Axelrod/pull/927
  https://github.com/Axelrod-Python/Axelrod/pull/928
  https://github.com/Axelrod-Python/Axelrod/pull/933
  https://github.com/Axelrod-Python/Axelrod/pull/934
  https://github.com/Axelrod-Python/Axelrod/pull/937
- New strategy: `SlowTitForTwoTats2`
  https://github.com/Axelrod-Python/Axelrod/pull/926
- New strategy: `GeneralSoftGrudger`
  https://github.com/Axelrod-Python/Axelrod/pull/936

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.7.0...v2.8.0

# v2.7.0, 2017-03-17

New strategies, increased test coverage, refactor of some tests, documentation
and minor bug fixes.

- New strategy: VeryBad
  https://github.com/Axelrod-Python/Axelrod/pull/869
- New strategy: Resurrection
  https://github.com/Axelrod-Python/Axelrod/pull/865
- Documentation of docstring requirements for contributions
  https://github.com/Axelrod-Python/Axelrod/pull/872
- Refactor tests:
  https://github.com/Axelrod-Python/Axelrod/pull/875
  https://github.com/Axelrod-Python/Axelrod/pull/907
  https://github.com/Axelrod-Python/Axelrod/pull/908
  https://github.com/Axelrod-Python/Axelrod/pull/909
  https://github.com/Axelrod-Python/Axelrod/pull/911
  https://github.com/Axelrod-Python/Axelrod/pull/914
- Improved coverage:
  https://github.com/Axelrod-Python/Axelrod/pull/899
  https://github.com/Axelrod-Python/Axelrod/pull/900
  https://github.com/Axelrod-Python/Axelrod/pull/901
  https://github.com/Axelrod-Python/Axelrod/pull/902
  https://github.com/Axelrod-Python/Axelrod/pull/904
  https://github.com/Axelrod-Python/Axelrod/pull/905
  https://github.com/Axelrod-Python/Axelrod/pull/910
- Bug in plot:
  https://github.com/Axelrod-Python/Axelrod/pull/897
- Bug fix in deterministic cache:
  https://github.com/Axelrod-Python/Axelrod/pull/882
- Bug in average copier:
  https://github.com/Axelrod-Python/Axelrod/pull/912
- Minor function rename:
  https://github.com/Axelrod-Python/Axelrod/pull/906


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.6.0...v2.7.0

# v2.6.0, 2017-02-26

New strategy, state to action analysis and internal improvements

- A number of type hints added to the library
  https://github.com/Axelrod-Python/Axelrod/pull/860
  https://github.com/Axelrod-Python/Axelrod/pull/863
  https://github.com/Axelrod-Python/Axelrod/pull/864
- New strategy: SelfSteem
  https://github.com/Axelrod-Python/Axelrod/pull/866
- Add state to action analysis
  https://github.com/Axelrod-Python/Axelrod/pull/870

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.5.0...v2.6.0

# v2.5.0, 2017-02-11

Internal improvements, type hints, documentation and a new strategy

- New strategy: ShortMem
  https://github.com/Axelrod-Python/Axelrod/pull/857
- A number of type hints added to the library
  https://github.com/Axelrod-Python/Axelrod/pull/828
  https://github.com/Axelrod-Python/Axelrod/pull/831
  https://github.com/Axelrod-Python/Axelrod/pull/832
  https://github.com/Axelrod-Python/Axelrod/pull/833
  https://github.com/Axelrod-Python/Axelrod/pull/834
  https://github.com/Axelrod-Python/Axelrod/pull/835
  https://github.com/Axelrod-Python/Axelrod/pull/836
  https://github.com/Axelrod-Python/Axelrod/pull/840
  https://github.com/Axelrod-Python/Axelrod/pull/846
  https://github.com/Axelrod-Python/Axelrod/pull/847
  https://github.com/Axelrod-Python/Axelrod/pull/849
  https://github.com/Axelrod-Python/Axelrod/pull/850
  https://github.com/Axelrod-Python/Axelrod/pull/851
  https://github.com/Axelrod-Python/Axelrod/pull/853
  https://github.com/Axelrod-Python/Axelrod/pull/854
  https://github.com/Axelrod-Python/Axelrod/pull/856
  https://github.com/Axelrod-Python/Axelrod/pull/858
  https://github.com/Axelrod-Python/Axelrod/pull/824
  https://github.com/Axelrod-Python/Axelrod/pull/821
  https://github.com/Axelrod-Python/Axelrod/pull/815
  https://github.com/Axelrod-Python/Axelrod/pull/814
- internal improvement to how players are cloned
  https://github.com/Axelrod-Python/Axelrod/pull/817
- Refactor/removal of dynamic classes
  https://github.com/Axelrod-Python/Axelrod/pull/852
- Run windows CI for py3.6
  https://github.com/Axelrod-Python/Axelrod/pull/844
- Run mypi on travis
  https://github.com/Axelrod-Python/Axelrod/pull/843
  https://github.com/Axelrod-Python/Axelrod/pull/837
- Small update to the readme
  https://github.com/Axelrod-Python/Axelrod/pull/829
- Docstring fix for random
  https://github.com/Axelrod-Python/Axelrod/pull/826
- Improve efficiency of neural network strategy
  https://github.com/Axelrod-Python/Axelrod/pull/819
- Improve efficiency of cycle detection
  https://github.com/Axelrod-Python/Axelrod/pull/809
- Refactor of a number of tests and test documentation
  https://github.com/Axelrod-Python/Axelrod/pull/820
- Large refactor thanks to dropping of python 2
  https://github.com/Axelrod-Python/Axelrod/pull/818

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.4.0...v2.5.0

# v2.4.0, 2017-01-05

New machine learning strategies and moran processes on graphs.

- Moran processes on graphs
  https://github.com/Axelrod-Python/Axelrod/pull/799
- Machine learning strategies
  https://github.com/Axelrod-Python/Axelrod/pull/803

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.3.0...v2.4.0

# v2.3.0, 2017-01-04

Support for py3.6, new strategies, more tournament result information,  and
internal improvements.

- Helpful list of short run time strategies
  https://github.com/Axelrod-Python/Axelrod/pull/792
- Nice Meta strategy
  https://github.com/Axelrod-Python/Axelrod/pull/794
- New strategies: Mem2, Pun1, Collective Strategy
  https://github.com/Axelrod-Python/Axelrod/pull/795
- New strategies: Mem2, Pun1, Collective Strategy
  https://github.com/Axelrod-Python/Axelrod/pull/795
- Python 3.6 supported
  https://github.com/Axelrod-Python/Axelrod/pull/800
- Keep track of initial play rate in results
  https://github.com/Axelrod-Python/Axelrod/pull/797
- Fix depreciation warning
  https://github.com/Axelrod-Python/Axelrod/pull/793
- Moran processes are always stochastic
  https://github.com/Axelrod-Python/Axelrod/pull/796

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.2.0...v2.3.0

# v2.2.0, 2016-12-20

Minor update: ability to pass axes object to plots and internal documentation
build fix.

- Pass axis object to plots
  https://github.com/Axelrod-Python/Axelrod/pull/791
- Build docs with py3
  https://github.com/Axelrod-Python/Axelrod/pull/788

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v2.1.0...v2.2.0

# v2.0.0, 2016-12-05

Dropping support for python 2, bug fixes, minor tidy of code (thanks to
dropping python 2 support!) and progress bars for fingerprinting.

- Dropping support for python 2
  https://github.com/Axelrod-Python/Axelrod/pull/774
- Fix bug in cache
  https://github.com/Axelrod-Python/Axelrod/pull/782
- Fix bug in stochastic classification of Random player
  https://github.com/Axelrod-Python/Axelrod/pull/783
- Fix docstrings in fingerprint
  https://github.com/Axelrod-Python/Axelrod/pull/784
- Use python 3 function caching
  https://github.com/Axelrod-Python/Axelrod/pull/775
- More progress bars for fingerprinting
  https://github.com/Axelrod-Python/Axelrod/pull/778

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.19.0...v2.0.0

# v1.19.0, 2016-11-30

New strategy using a trained neural network and documentation.

- Implement the EvolvedANN
  https://github.com/Axelrod-Python/Axelrod/pull/773
- More strategy documentation
  https://github.com/Axelrod-Python/Axelrod/pull/772

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.18.1...v1.19.0

# v1.18.1, 2016-11-24

There are no changes between 1.18.1 and 1.18.0. This release is due to an error
during the uploading to pypi.

# v1.18.0, 2016-11-24

There are no changes between 1.18.0 and 1.17.1. This release is due to an error
during the uploading to pypi.

# v1.17.1, 2016-11-23

Minor bug fix and a title option for fingerprints and a small internal
improvement.

- Correct the range for the fingerprint
  https://github.com/Axelrod-Python/Axelrod/pull/766
- Include ability to have a title for fingerprint plot
  https://github.com/Axelrod-Python/Axelrod/pull/769
- Calculate score per turn for Moran process using internal method.
  https://github.com/Axelrod-Python/Axelrod/pull/764

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.17.0...v1.17.1

# v1.17.0, 2016-11-19

Ahslock fingerprinting.

- Add a class for fingerprinting of strategies according to a paper by Ashlock
  et al.
  https://github.com/Axelrod-Python/Axelrod/pull/759

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.16.0...v1.17.0

# v1.16.0, 2016-11-13

Minor internal change, new strategy and new strategy transformers

- Random_choice method does not sample if not necessary
  https://github.com/Axelrod-Python/Axelrod/pull/761
- New strategy: Meta Winner Ensemble
  https://github.com/Axelrod-Python/Axelrod/pull/757
- New strategy transformers: Dual transformer and Joss-Ann transformer
  https://github.com/Axelrod-Python/Axelrod/pull/758

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.15.0...v1.16.0

# v1.15.0, 2016-11-03

Mutation in Moran process, players track state pairs, save all plots method,
new strategies and PEP8.

- Mutation in Moran processes:
  https://github.com/Axelrod-Python/Axelrod/pull/754
- Save all plots to file method:
  https://github.com/Axelrod-Python/Axelrod/pull/753
- Players track state pairs:
  https://github.com/Axelrod-Python/Axelrod/pull/752
- New strategies:
      - StochasticCooperator (re introduced):
        https://github.com/Axelrod-Python/Axelrod/pull/755
      - SpitefulTitForTat
        https://github.com/Axelrod-Python/Axelrod/pull/749
- PEP8:
  https://github.com/Axelrod-Python/Axelrod/pull/750

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.14.0...v1.15.0

# v1.14.0, 2016-10-24

Two new strategies.

- Adding Negative strategy
  https://github.com/Axelrod-Python/Axelrod/pull/748
- Adding Doubler strategy
  https://github.com/Axelrod-Python/Axelrod/pull/747

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.13.0...v1.14.0

# v1.13.0, 2016-10-16

New strategy, state distribution and documentation

- Adding Prober4 strategy
  https://github.com/Axelrod-Python/Axelrod/pull/743
- Adding state distribution to results set
  https://github.com/Axelrod-Python/Axelrod/pull/742
- More references for strategies
  https://github.com/Axelrod-Python/Axelrod/pull/745

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.12.0...v1.13.0

# v1.12.0, 2016-10-13

Human interactive player, new strategy, under the hood improvements and
documentation.

- You can play against an instance of `axelrod.Human`
  https://github.com/Axelrod-Python/Axelrod/pull/732
- Improved efficiency of result set from memory
  https://github.com/Axelrod-Python/Axelrod/pull/737
- Documentation improvements
  https://github.com/Axelrod-Python/Axelrod/pull/741
  https://github.com/Axelrod-Python/Axelrod/pull/736
  https://github.com/Axelrod-Python/Axelrod/pull/735
  https://github.com/Axelrod-Python/Axelrod/pull/727
- New strategy CyclerCCCDCD:
  https://github.com/Axelrod-Python/Axelrod/pull/379

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.11.0...v1.12.0

# v1.12.0, 2016-10-13

Human interactive player, new strategy, under the hood improvements and
documentation.

- You can play against an instance of `axelrod.Human`
  https://github.com/Axelrod-Python/Axelrod/pull/732
- Improved efficiency of result set from memory
  https://github.com/Axelrod-Python/Axelrod/pull/737
- Documentation improvements
  https://github.com/Axelrod-Python/Axelrod/pull/741
  https://github.com/Axelrod-Python/Axelrod/pull/736
  https://github.com/Axelrod-Python/Axelrod/pull/735
  https://github.com/Axelrod-Python/Axelrod/pull/727
- New strategy CyclerCCCDCD:
  https://github.com/Axelrod-Python/Axelrod/pull/379

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.11.0...v1.12.0

# v1.11.0, 2016-09-28

State distribution functions, new strategies and minor test fix.

- Matches have a method to give state distribution:
  https://github.com/Axelrod-Python/Axelrod/pull/717
- Two new strategies: Worse and Worse and Knowledgeable Worse and Worse.
  https://github.com/Axelrod-Python/Axelrod/pull/724
- Minor fix of a test that would sometimes fail due to floating point error.
  https://github.com/Axelrod-Python/Axelrod/pull/725


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.10.0...v1.11.0

# v1.10.0, 2016-09-22

Windows support! Summarise method for results, new strategies, and code of
conduct as well as minor fixes.

- Various fixes to windows bugs (thanks to the PyConUK sprint!):
  https://github.com/Axelrod-Python/Axelrod/pull/711
  https://github.com/Axelrod-Python/Axelrod/pull/714
  https://github.com/Axelrod-Python/Axelrod/pull/721
- The result set has a summary:
  https://github.com/Axelrod-Python/Axelrod/pull/707
- Three new strategies (Gradual killer, easy go, Grudger alternator):
  https://github.com/Axelrod-Python/Axelrod/pull/715
- Code of conduct:
  https://github.com/Axelrod-Python/Axelrod/pull/705
- Fix of some tests:
  https://github.com/Axelrod-Python/Axelrod/pull/716
- Fix of link in docs:
  https://github.com/Axelrod-Python/Axelrod/pull/722


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.9.0...v1.10.0

# v1.9.0, 2016-09-09

Filtering of strategy classes with a filterset dictionary.

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.8.0...v1.9.0

# v1.8.0, 2016-08-28

New strategies:

- Adaptive TitForTat:
  https://github.com/Axelrod-Python/Axelrod/pull/697
- Desperate, Hopeless, Willing:
  https://github.com/Axelrod-Python/Axelrod/pull/686

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.7.0...v1.8.0

# v1.7.0, 2016-08-14

Probabilistic ending spatial tournaments, classifier for long run time, style
improvements, documentation improvements (including a bibliography) and bug fix.

- Probabilistic ending spatial tournaments:
  https://github.com/Axelrod-Python/Axelrod/pull/674
- Classifier for strategies that have a long run time:
  https://github.com/Axelrod-Python/Axelrod/issues/690
- Documentation and style
  cleanup:https://github.com/Axelrod-Python/Axelrod/issues/675,
  https://github.com/Axelrod-Python/Axelrod/pull/687,
  https://github.com/Axelrod-Python/Axelrod/pull/685,
  https://github.com/Axelrod-Python/Axelrod/pull/682
- Fix the noise in spatial tournaments:
  https://github.com/Axelrod-Python/Axelrod/pull/679

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.6.0...v1.7.0

# v1.6.0, 2016-07-31

Renaming of strategies, big performance improvement for result analysis and bug
fixes

- axelrod.strategies is a list of well behaved (non cheating strategies):
  https://github.com/Axelrod-Python/Axelrod/pull/665
- The results set now has much lower memory footprint and is much faster:
  https://github.com/Axelrod-Python/Axelrod/pull/672
- Correct calculation for mean score diffs:
  https://github.com/Axelrod-Python/Axelrod/pull/671
- Error catching for bug with OSX, virtual envs and matplotlib:
  https://github.com/Axelrod-Python/Axelrod/pull/669

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.5.0...v1.6.0

# v1.5.0, 2016-07-19

New tournament type, new strategy, seeding, dev tools, docs + minor/bug fixes

User facing:

- Spatial tournaments: https://github.com/Axelrod-Python/Axelrod/pull/654
- New strategy, slow tit for tat:
  https://github.com/Axelrod-Python/Axelrod/pull/659
- Seed the library: https://github.com/Axelrod-Python/Axelrod/pull/653
- More uniform strategy transformer behaviour:
  https://github.com/Axelrod-Python/Axelrod/pull/657
- Results can be calculated with non default game:
  https://github.com/Axelrod-Python/Axelrod/pull/656

Documentation:

- A community page: https://github.com/Axelrod-Python/Axelrod/pull/656
- An overall results page that replaces the payoff matrix page:
  https://github.com/Axelrod-Python/Axelrod/pull/660

Development:

- A git hook script for commit messages:
  https://github.com/Axelrod-Python/Axelrod/pull/648
- Caching of hypothesis database on travis:
  https://github.com/Axelrod-Python/Axelrod/pull/658

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.4.0...v1.5.0

# v1.4.0, 2016-06-22

New strategy.

- contrite TitForTat: https://github.com/Axelrod-Python/Axelrod/pull/639

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.3.0...v1.4.0

# v1.3.0, 2016-06-21

New strategy, a bug fix and more explicit copyright notice

- Remorseful Prober: https://github.com/Axelrod-Python/Axelrod/pull/633

Bug fix:

- The finite state machines were not reseting state properly.


Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.2.0...v1.3.0

# v1.2.0, 2016-06-13

New strategies and some minor improvements

- Naive Prober: https://github.com/Axelrod-Python/Axelrod/pull/629
- Gradual: https://github.com/Axelrod-Python/Axelrod/pull/627
- Soft grudger and reverse pavlov:
  https://github.com/Axelrod-Python/Axelrod/pull/628

Minor improvements include:

- Progress bar for result set reading of data:
  https://github.com/Axelrod-Python/Axelrod/pull/618
- Prob end tournament players do not know match length (this was in essence a
  bug): https://github.com/Axelrod-Python/Axelrod/pull/611
- Doc fixes

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.1.1...v1.2.0

# v1.1.1, 2016-06-01

Minor changes, bug fixes.

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.1.0...v1.1.1

User facing:

- The matches can tell the players different match attributes than the ones
  actually being played (helpful for prob end tournaments where players cannot
  know the length of the match for example):
  https://github.com/Axelrod-Python/Axelrod/pull/609
- A progress bar for the result set:
  https://github.com/Axelrod-Python/Axelrod/pull/603

Internal:

- Reducing some test sizes: https://github.com/Axelrod-Python/Axelrod/pull/601
- PEP8 improvements: https://github.com/Axelrod-Python/Axelrod/pull/607
- Refactor of the match generator (noise is an attribute):
  https://github.com/Axelrod-Python/Axelrod/pull/608

# v1.1.0, 2016-05-18

New strategies and minor changes to the test suite

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.0.1...v1.1.0

This introduces various new strategies to the library:

- Adaptive
- Handshake
- CyclerDC and CyclerDDC (used in the literature)
- 8 Finite State Machine strategies: Fortress3, Fortress4, Predator,
  Raider, Ripoff, SolutionB1, SolutionB5, Thumper

This version also includes a minor change to the test suite: shortening the size
of the tournaments being run in the integration tests.

Here is the PR that incorporated all of the above:
https://github.com/Axelrod-Python/Axelrod/pull/591

# v1.0.1, 2016-05-15

Bug fix.

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v1.0.0...v1.0.1

During the previous refactor of the Tournament, the ability to create noisy
tournaments was lost. An integration test has been written to catch this in the
future: https://github.com/Axelrod-Python/Axelrod/pull/596

# v1.0.0, 2016-05-14

Internal improvements, progress bar, minor interface change

Here are all the commits for this PR:
https://github.com/Axelrod-Python/Axelrod/compare/v0.0.31...v1.0.0

This release is the first major release stating the stability and maturity of
the library.

There are some user facing improvements:

- A progress bar: https://github.com/Axelrod-Python/Axelrod/pull/578
- Whether or not a tournament is to be run using parallel processing is no
  longer a property of the tournament itself but an argument of the play method:
  https://github.com/Axelrod-Python/Axelrod/pull/582

There were some extensive internal changes:

- The tournament attributes are passed to the players from the matches and not
  the tournament. This should make further things like changing what the players
  know about the tournament more straightforward:
  https://github.com/Axelrod-Python/Axelrod/pull/537
- A huge re write of the actual way the tournament runs. This is the biggest
  such re write to date. The parallel workers now execute repetitions of matches
  which are written to disk as and when they complete. This greatly reduces the
  memory footprint of the tournament. A side effect of the above is a change of
  how the tournament is written to disk: the format is now much clearer (every
  row is a match): https://github.com/Axelrod-Python/Axelrod/pull/572

# v0.0.31, 2016-04-18

Moran processes, better caching architecture and match generator

# v0.0.30, 2016-04-08

Reading and writing tournaments to file, better pickling.

# v0.0.29, 2016-04-04

Bug fix with parallel processing.

# v0.0.28, 2016-03-29

New strategy, enhanced matches and prob end tournaments.

# v0.0.27, 2016-03-06

Minor fixes, rewrite of tournament engine: interactions now available.

# v0.0.26, 2016-02-24

Bug fix and two new strategies based on ThueMorse sequence.

# v0.0.25, 2016-01-26

Minor documentation changes.

# v0.0.24, 2016-01-19

New strategy (FirmButFair) and hypothesis testing

# v0.0.23, 2015-12-14

Mixed strategies (decorator and meta player)

# v0.0.22, 2015-12-07

Including a DOI.

# v0.0.21, 2015-11-29

Match class with sparklines.

# v0.0.20, 2015-11-21

Strategies have 'makes_use_of' attribute, improved docs/doctests,

# v0.0.19, 2015-11-21

Efficiency improvements, new default colour maps

# v0.0.18, 2015-11-04

New strategies

# v0.0.17, 2015-10-30

Strategy transforms and bug fixes

# v0.0.16, 2015-10-25

Tidying strategies, action classes, flip action method and new docs

# v0.0.15, 2015-10-13

Distribution of wins plots, and is_cheater becomes obey_axelrod

# v0.0.14, 2015-09-28

Change to use distutils, mirror strategy and readthedocs bug

# v0.0.13, 2015-09-16

Adding classifier dictionary and dynamic strategy list.

# v0.0.12, 2015-09-02

Further behaviour and more info being passed to players.

# v0.0.11, 2015-08-17

Updating Core team

# v0.0.10, 2015-08-17

Python 3 support and behaviour metrics

# v0.0.9, 2015-06-14

Various improvements including noisy tournaments

# v0.0.8, 2015-04-16

Change default behaviour to maximisation

# v0.0.7, 2015-04-01

Perhaps removes long description

# v0.0.6, 2015-04-01

Removes long description

# v0.0.5, 2015-03-28

Corrects formatting of authors

# v0.0.4, 2015-03-28

Adding all authors

# v0.0.3, 2015-03-27

Minor fix

# v0.0.2, 2015-03-27

Minor fix

# v0.0.1, 2015-03-27

Initial release
