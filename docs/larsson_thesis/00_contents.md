Contents
1Introduction 1
1.1 Theaimofthisstudy..............................1
1.2 Rationale ....................................2
1.2.1 Whydialogue management?......................2
1.2.2 Whyexploretheissue-based approach?................2
1.3 Outlineofthisthesis..............................4
1.4 The IBi Sfamilyofsystems ..........................5
1.5 Trindi Kit ...................................6
1.6 Summary ....................................13
2Basicissue-based dialoguemanagement 15
2.1 Introduction...................................15
2.1.1 Asampledialogue ...........................15
2.1.2 Information exchangeandinquiry-orienteddialogue .........16
2.2 Sharedandprivateinformation indialogue ..................18
2.2.1 The BDImodel.............................18
iii

2.2.2 Stalnakerand Lewis..........................19
2.2.3 Ginzburg's Dialogue Gameboard...................19
2.3 Overviewof IBi S1...............................20
2.3.1 IBi S1 architecture ...........................20
2.3.2 Simplifying assumptions ........................22
2.3.3 IBi S1Datatypes............................23
2.4 Semanticsin IBi S1...............................24
2.4.1 Formalsemanticrepresentations....................24
2.4.2 Propositions...............................25
2.4.3 Questions ................................26
2.4.4 Shortanswers..............................27
2.4.5 Semanticsortalrestrictions ......................28
2.4.6 Relations betweenquestions andanswers...............28
2.4.7 Combining Questions and Answerstoform Propositions ......30
2.5 Dialogue movesin IBi S1............................32
2.6 Represen tingdialogue plansin IBi S1.....................33
2.6.1 Domain plansanddialogue plans...................33
2.6.2 Asyntaxforproceduralplans.....................34
2.7 Total Information Statein IBi S1.......................35
2.7.1 Information statein IBi S1.......................36
2.7.2 Initializing theinformation state....................38
2.7.3 Resource interfaces ...........................38
iv

2.7.4 Moduleinterfacevariables .......................39
2.8IBi S1 updatemodule..............................40
2.8.1 Updateruleforgettingthelatestutterance .............40
2.8.2 Raisingissues:theaskmove......................41
2.8.3 Resolving issues.............................45
2.8.4 Downdating QUD............................47
2.8.5 Integrating greetandquitmoves....................48
2.8.6 Managing theplan...........................49
2.8.7 Updatealgorithm for IBi S1......................51
2.9IBi S1 selection module.............................51
2.9.1 Selecting anactionfromtheplan...................51
2.9.2 Selecting theaskmove.........................52
2.9.3 Selecting torespondtoaquestion ...................53
2.9.4 Selecting theanswermove.......................54
2.10 Adapting IBi S1 tothetravelinformation domain ..............55
2.10.1 Thedomainresource ..........................55
2.10.2 Lexiconresource ............................57
2.10.3 Database resource ............................58
2.11 Sampledialogue with IBi S1..........................58
2.12 Discussion ....................................62
2.12.1 Single-issue systems...........................62
2.12.2\Howcan Ihelpyou?".........................62
v

2.12.3 Reraising issuesandsharinginformation ...............64
2.12.4 Database search,relevance,anddialogue ...............68
2.12.5 Additional planconstructs .......................70
2.12.6 Questions andanswersvs.slotsandfillers..............71
2.12.7 Questions vs.knowledgepreconditions ................72
2.13 Summary ....................................73
3Grounding issues 75
3.1 Introduction...................................75
3.1.1 Dialogue examples ...........................76
3.2 Background ...................................78
3.2.1 Clark:Addingtothecommon ground ................78
3.2.2 Ginzburg: QUD-based utterance processingprotocols........80
3.2.3 Allwood:Interactive Communication Managemen t.........83
3.3 Preliminary discussion .............................84
3.3.1 Levelsofactionindialogue ......................84
3.3.2 Reaction levelfeedback.........................85
3.3.3 Levelsofunderstanding ........................87
3.3.4 Somecommentson Ginzburg's protocol................88
3.4 Feedbackandrelatedbehaviourinhuman-humandialogue .........89
3.4.1 Classifying explicitfeedback......................90
3.4.2 Positive,negative,andneutralfeedback................91
vi

3.4.3 Eliciting andnon-eliciting feedback..................92
3.4.4 Formoffeedback............................92
3.4.5 Meta-levelandobject-levelfeedback..................93
3.4.6 Fragmentfeedback/clarification ellipsis...............93
3.4.7 Own Communication Managemen t..................94
3.4.8 Repairandrequestforrepair.....................94
3.4.9 Request forfeedback..........................95
3.5 Updatestrategies forgrounding ........................95
3.5.1 Optimistic andpessimistic strategies .................95
3.5.2 Grounding updatesandactionlevels.................96
3.5.3 Thecautious strategy ..........................97
3.6 Feedbackandgrounding strategies for IBi S.................98
3.6.1 Grounding strategies fordialogue systems ..............99
3.6.2\Implicit" and\explicit" verification indialogue systems ......100
3.6.3 Issue-based grounding in IBi S.....................100
3.6.4 Enhancing theinformation statetohandlefeedback.........103
3.6.5 Feedbackandsequencing dialogue moves...............105
3.6.6 Grounding ofuserutterances in IBi S2................109
3.6.7 Grounding ofsystemutterances in IBi S2...............130
3.6.8 Evidence requirementsandimplicitgrounding ............138
3.6.9 Sequencing ICM:reraising issuesandloadingplans.........142
3.7 Furtherimplementationissues.........................145
vii

3.7.1 Updatemodule.............................146
3.7.2 Selection module............................146
3.8 Discussion ....................................148
3.8.1 Somegrounding-related phenomena nothandled by IBi S2.....148
3.8.2 Towardsanissue-based accountofgrounding andactionlevels...149
3.8.3 Comparison to Traum'scomputational theoryofgrounding .....149
3.9 Summary ....................................151
4Addressing unraisedissues 153
4.1 Introduction...................................153
4.2 Somelimitations of IBi S2...........................154
4.3 Thenature(s) of QUD.............................155
4.3.1 Ginzburg's definition of QUD.....................155
4.3.2 Openquestions notavailableforellipsisresolution ..........157
4.3.3 Openbutnotexplicitly raisedquestions ...............157
4.3.4 Globalandlocal QUD.........................158
4.3.5 Someothernotionsofwhata QUDmightbe.............159
4.4 Question Accommo dation...........................160
4.4.1 Background: Accommo dation.....................160
4.4.2 Accommo dation,interpretation, andtacitmoves...........161
4.4.3 Extending thenotionofaccommodation...............161
4.5 Formalizing question accommodation.....................162
viii

4.5.1 Information statein IBi S3.......................162
4.6 Varietiesofquestion accommodationandreaccommodation.........164
4.6.1 Issueaccommodation:fromdialogue planto ISSUES ........165
4.6.2 Localquestion accommodation:from ISSUES to QUD.......168
4.6.3 Issueclarification ............................169
4.6.4 Dependentissueaccommodation:fromdomainresource to ISSUES 171
4.6.5 Dependentissueclarification ......................176
4.6.6 Question reaccommodation ......................178
4.6.7 Openingupimplicitgrounding issues.................182
4.7 Furtherimplementationissues.........................191
4.7.1 Dialogue moves.............................191
4.7.2 IBi S3 updatemodule..........................191
4.7.3 Selection module............................197
4.8 Discussion ....................................197
4.8.1 Phrasespottingandsyntaxinflexibledialogue ............197
4.8.2 Relaxing constrain tsusingdenialanddependentreaccommodation 199
4.8.3\Smart" interpretation .........................200
4.8.4 Separating understanding, acceptance, andintegration .......201
4.8.5 Accommo dationandthespeaker'sownutterances ..........201
4.8.6 Accommo dationvs.normalintegration ................202
4.8.7 Dependentissueaccommodationin Voice XML? ...........203
4.9 Summary ....................................203
ix

5Action-orientedandnegotiativedialogue 205
5.1 Introduction...................................205
5.2 Issuesandactionsinaction-orienteddialogue ................206
5.3 Extending IBi Stohandleactionorienteddialogue ..............206
5.3.1 Enhancing theinformation state....................206
5.3.2 Dialogue moves.............................208
5.4 Interacting withmenu-baseddevices .....................209
5.4.1 Connecting devicesto IBi S......................209
5.4.2 Frommenutodialogue plan......................212
5.4.3 Extending theresolvesrelationformenu-based AOD........212
5.5 Implemen tationofthe VCRcontroldomain .................213
5.6 Updaterulesanddialogue examples ......................215
5.6.1 Integrating andrejecting requests ...................215
5.6.2 Executing deviceactions........................216
5.6.3 Selecting andintegrating confirm-moves................217
5.6.4 Dialogue example: menutraversalandmultiplethreads.......218
5.6.5 Actionaccommodationandclarification ...............220
5.6.6 Dialogue examples: actionaccommodationandclarification .....222
5.7 Issuesundernegotiation innegotiativedialogue ...............223
5.7.1 Sidner's theoryofnegotiativedialogue ................223
5.7.2 Negotiation asdiscussing alternatives.................226
5.7.3 Issues Under Negotiation (IUN)....................228
x

5.7.4 Anexample ...............................230
5.8 Discussion ....................................230
5.8.1 Negotiation ininquiry-orienteddialogue ...............230
5.8.2 Rejection, negotiation anddownshifting ................232
5.9 Summary ....................................233
6Conclusions andfutureresearch 235
6.1 Introduction...................................235
6.2 Summary ....................................235
6.3 Dialogue typology................................236
6.3.1 Relation to Dahlböack'sdialogue taxonomy..............238
6.3.2 Relation to Allenet.al.'sdialogue classification ...........239
6.4 Dialogue structure ...............................241
6.5 Futureresearchareas..............................243
6.5.1 Developingtheissue-based approachtogrounding ..........243
6.5.2 Otherdialogue andactivitytypes...................245
6.5.3 Semantics................................246
6.5.4 Generalinference ............................247
6.5.5 Naturallanguage inputandoutput..................247
6.5.6 Applications andevaluation ......................248
6.6 Conclusion ....................................249
