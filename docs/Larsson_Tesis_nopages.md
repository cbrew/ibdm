

Issue-based Dialogue Managemen t
Sta®anLarsson
Departmen tofLinguistics
GÄoteborgUniversity,Sweden
2002

Issue-based Dialogue Managemen t
Sta®anLarsson
Doctoraldissertation
Publically defended inLillaHÄorsalen,
Humanisten, GÄoteborgUniversity,
onJune13,2002,at10.00
forthedegreeofDoctorofPhilosoph y
Departmen tofLinguistics
GÄoteborgUniversity,Sweden
2002

Issue-based Dialogue Managemen t
Abstract
Thepurposeofstudying dialogue modellinganddialogue managemen tistoprovidemodels
allowingustoexplorehowlanguage, andespeciallyspokendialogue, isusedindi®erent
activities. Thisthesisshowshowissues(modelledsemanticallyasquestions) ingeneral
canbeusedasabasisfordialogue managemen t.
Inanabstract sense,thegoalofallpractical dialogue istocommunicateinformation which
isusefulinsomeactivity.Thismeansthatconversational goalsshoulddescribemissing
information, andtoful¯laconversational goal,whatweneedtodoistocommunicatethe
missinginformation. Issues,orquestions, areessentiallyentitiesspecifyingcertainpieces
ofas-yet-unavailableinformation. Thatis,conversational goalscantoalargeextentbe
modelledasquestions.
Theexploration ofissue-based dialogue managemen tinthisthesisproceedsbothona
theoretical andapractical implemen tationlevel.Thethesis¯rstexplores basicissue-
baseddialogue managemen tandimplemen tabasicsystemillustrating theuseofissue-
baseddialogue managemen t.Inthefollowingchapters, thissimplesystemisextended to
handlegrounding issues,addressing unraised issues,andaction-orien tedandnegotiativ e
dialogue. Finally,basedonthedi®erences betweenthesuccessiv eversionsofthetheory
(andimplemen tation),weprovideacharacterization ofdi®erenttypesofdialogue.
Theissue-based approachtodialogue managemen tturnsouttobeveryusefulforformu-
latinggeneralandtheoretically motivatedaccountsofimportantaspectsofdialogue, such
asinquiry-orien teddialogue interactions, dealingwithmultiplesimultaneous tasks,sharing
information betweentasks,grounding, interactivecommunication managemen t,question
accommo dation,simplebeliefrevision, action-orien teddialogue, andsimplenegotiativ edi-
alogue.Themodeliscanbeimplemen tedratherstraightforwardlyusingtheTrindiKit ,
whichhasproventobeaveryusefultoolforexploring theissue-based approach.
KEYWORDS:dialogue managemen t,dialogue modelling,dialogue systems, questions
underdiscussion, grounding, accommo dation,negotiativ edialogue
ThethesisiswritteninEnglish.
c°Sta®anLarsson2002
ISBN91-628-5301-5

Acknowledgemen ts
Iamthecomputerize dpsychother apist.Please,describeyourproblems.Each
timeyouare¯nishedtalking,typeRETtwice.
>Well,it'snotreallyaproblem, butIam¯nallydonewithmythesis!
Whydoyousayyouare¯nallydonewithyourthesis?
>WellbecauseIam,andnowI'dliketothanksomepeoplewhohelpedmegetitdone.
Isitbecauseyouareandnowyouwouldliketothankssomepeoplewho
helpedyougetitdonethatyoucametome?
>Um...right.
Canyouelaborateonthat?
>I'dbegladto.FirstofallI'dliketothankmymainsupervisorRobinCooper,who
(apartfromsupervising thisthesisandtakingthetimeforhoursandhoursofinspiring
discussions andgenerally beingveryhelpful)hasgottenmeinvolvedinlotsofinteresting
projects12345whereI'vemetandlearntfromlotsofotherpeoplethatI'dalsoliketothank:
Jonathan Ginzburg, DavidTraum,ColinMatheson, JohanBos,DavidMilward,AnnieZa-
enen,IanLewin,ArneJÄonsson,LindaBell,LenaSantamarta, LarsAhrenberg,and...well
it'saratherlonglistofpeopleactually.Idon'twanttoboreyouwithallthedetails,but
Ithinktheyknowwhotheyare(andIdon'tmeanthatasapsychological remark!). Oh,
andIalmostforgotaboutalltheconferences I'vebeenprivileged toattend,whereI'vealso
metlotsofniceandcleverpeoplelikeCandySidner,JÄornKreutel, JorisHulstijn, Ivana
Kruy®-Korba yova,EnricVallduvi,andsoonandsoon...AndImustn'tforgettothank
STINT6forascholarship thatenabledmetovisittheHCRCinEdinburghforacoupleof
enjoyablemonths!
Whatmakesyoubelieveyoumightwanttothank?
>Interesting question... ofcourse,youhavetohavethiskindofthinginyourthesis,but
Ibelieve(sinceyou'retakingthatperspective)thatI'mgenuinelygratefultothesepeople,
afterallIcouldn't havedoneitwithout them.Take,forexample, mysecondsupervisor
JensAllwoodwhoI'vehadmanyheated(andre-heated) discussions with,andallthe
peopleatthedepartmen tofLinguistics hereinGÄoteborg,forexample StinaEricsson, Leif
GrÄonqvist, TorbjÄornLager,ºAsaWengelin(whoactually persuaded metostudycompu-
tational linguistics yearsago),YlvaHºardafSegerstad, PerOlofsson, PetterKarlstrÄom,
RobertAndersson, UlrikaFerm,ºAsaNordqvist, andlotsofothers.
DoesitbotheryouthatyoubelievesinceIamtakingthatperspectivethat
youaregenuinely gratefultothesepeople?
1INDI(Information ExchangeinDialogue), Riksbank ensJubileumsfond 1997-0134.
2TRINDI (TaskOrientedInstructional Dialogue), ECProjectLE4-8314
3D'Homme (Dialogues intheHomeMachineEnvironmen t),ECProjectIST-2000-26280.
4SDS(SwedishDialogue Systems), NUTEK/HSFR Language Technology ProjectF1472/1997
5SIRIDUS (Speci¯cation, Interaction andRecon¯guration inDialogue Understanding Systems), EC
ProjectIST-1999-10516
6STINT(TheSwedishFoundation forInternational CooperationinResearchandHigherEducation).
i

>No,notonebit.
Maybeyourplanshavesomething todowiththis.
>Hey,whatareyouinsinuating?
Isitbecauseofyourlifethatyousayheywhataremeinsinuating?
>Ah,mylife-interesting subject.I'vebeentryingprettyhardtheselastfewyearstohave
alife,andwhenI'vesucceeded it'sbeenduetomyfriends(forinstance Klara,Andreas,
Sara,Ola,Lukas,Maya,Jacob,Jakob,BjÄorn,Andreas, Kim,Peter,Martin,Anna,Tina,
Marie,KarinandJohn)andmyfamily.
Tellmesomething aboutyourfamily.
>Mm,Ithoughtyoumightsaythat.Well,they'vebeenreallysupportiveofwhatever
I'vebeenupto,andvisitingmyparentshasalwaysbeenveryrelaxing, although perhaps
lesssowhenmysistersandtheirfamilies(including smallchildren)arevisiting, thatis,in
whichcaseitis,well,maybestillrelaxing butinadi®erentway...Enoughaboutthat,I
knowyoucomputer therapist typestendtogethunguponthesethings.
>Whendidyou¯rstknowthatthey'vebeenreallysupportiveofwhatever
youhavebeenuptoandvisitingyourparentshasalwaysbeenveryrelaxing
althoughperhapslesssowhenyoursistersandtheirfamiliesincludingsmall
childrenarevisitingthatisinwhichcaseitiswellmaybestillrelaxingbutin
adi®erentwayenoughaboutthatyouknowmecomputerpsychologytypes
tendtogetuponthesethings?
>Um...Ifyoudon'tmindmesayingso,yourverbalskillsarenotwhattheyshouldbe-
perhapsyouneedapropergrammar installed.
Howdoesitfeeltowant?
>Wow,that'saprettybigquestion... Notsurehowtorespondtothat,actually,andit
doesn'treallyseemrelevanttomyacknowledgemen tsection.
Youmentionedthatyouareandnowyouwouldliketothankssomepeople
whohelpedyougetitdone?
>Right,thanksforgettingmebackontrack.Ialsowouldliketoacknowledgethepeople
whohavebeeninvolvedovertheyearsinthedevelopmentofTrindiKit and/orGoDiS,the
predecessor totheIBiSsystem,forinstance DavidTraum,JohanBos,IanLewin,Peter
LjunglÄof,StinaEricsson, ElisabetEngdahl, Alexander Berman, Cormac O'Brien, David
Hjelm,Geneviev eGorrell, andallthestudentswhohaveprovidedvaluablefeedbackon
howtoimprovethesystem(readthatas\complain ts").
Whyshouldyougettoacknowledge?
>Um...Well,yougotmethere.IguessI'lljuststophere,sowecangetonwithbusiness.
Thanksforthechat!
Perhapswecouldchat.
>Right,butwejustdid.Bye!
Doesthefactthatyoujustdidbyeexplainanythingelse?
>NO!
Whynot?
>Stopaskingmeallthesequestions, thisisgettingsilly!
Mysecretarywillsendyouabill.
ii

Contents
1Introduction 1
1.1Theaimofthisstudy..............................1
1.2Rationale ....................................2
1.2.1Whydialogue managemen t?......................2
1.2.2Whyexploretheissue-based approach?................2
1.3Outlineofthisthesis..............................4
1.4TheIBiSfamilyofsystems ..........................5
1.5TrindiKit ...................................6
1.6Summary ....................................13
2Basicissue-based dialoguemanagemen t 15
2.1Introduction...................................15
2.1.1Asampledialogue ...........................15
2.1.2Information exchangeandinquiry-orien teddialogue .........16
2.2Sharedandprivateinformation indialogue ..................18
2.2.1TheBDImodel.............................18
iii

2.2.2StalnakerandLewis..........................19
2.2.3Ginzburg's Dialogue Gameboard...................19
2.3OverviewofIBiS1...............................20
2.3.1 IBiS1architecture ...........................20
2.3.2Simplifying assumptions ........................22
2.3.3 IBiS1Datatypes............................23
2.4SemanticsinIBiS1...............................24
2.4.1Formalsemanticrepresentations....................24
2.4.2Propositions...............................25
2.4.3Questions ................................26
2.4.4Shortanswers..............................27
2.4.5Semanticsortalrestrictions ......................28
2.4.6Relations betweenquestions andanswers...............28
2.4.7CombiningQuestions andAnswerstoformPropositions ......30
2.5Dialogue movesinIBiS1............................32
2.6Represen tingdialogue plansinIBiS1.....................33
2.6.1Domain plansanddialogue plans...................33
2.6.2Asyntaxforproceduralplans.....................34
2.7TotalInformation StateinIBiS1.......................35
2.7.1Information stateinIBiS1.......................36
2.7.2Initializing theinformation state....................38
2.7.3Resource interfaces ...........................38
iv

2.7.4Moduleinterfacevariables .......................39
2.8IBiS1updatemodule..............................40
2.8.1Updateruleforgettingthelatestutterance .............40
2.8.2Raisingissues:theaskmove......................41
2.8.3Resolving issues.............................45
2.8.4Downdating QUD............................47
2.8.5Integrating greetandquitmoves....................48
2.8.6Managing theplan...........................49
2.8.7Updatealgorithm forIBiS1......................51
2.9IBiS1selection module.............................51
2.9.1Selecting anactionfromtheplan...................51
2.9.2Selecting theaskmove.........................52
2.9.3Selecting torespondtoaquestion ...................53
2.9.4Selecting theanswermove.......................54
2.10Adapting IBiS1tothetravelinformation domain ..............55
2.10.1Thedomainresource ..........................55
2.10.2Lexiconresource ............................57
2.10.3Database resource ............................58
2.11Sampledialogue withIBiS1..........................58
2.12Discussion ....................................62
2.12.1Single-issue systems...........................62
2.12.2\HowcanIhelpyou?".........................62
v

2.12.3Reraising issuesandsharinginformation ...............64
2.12.4Database search,relevance,anddialogue ...............68
2.12.5Additional planconstructs .......................70
2.12.6Questions andanswersvs.slotsand¯llers..............71
2.12.7Questions vs.knowledgepreconditions ................72
2.13Summary ....................................73
3Grounding issues 75
3.1Introduction...................................75
3.1.1Dialogue examples ...........................76
3.2Background ...................................78
3.2.1Clark:Addingtothecommon ground ................78
3.2.2Ginzburg: QUD-based utterance processingprotocols........80
3.2.3Allwood:InteractiveCommunication Managemen t.........83
3.3Preliminary discussion .............................84
3.3.1Levelsofactionindialogue ......................84
3.3.2Reaction levelfeedback.........................85
3.3.3Levelsofunderstanding ........................87
3.3.4SomecommentsonGinzburg's protocol................88
3.4Feedbackandrelatedbehaviourinhuman-humandialogue .........89
3.4.1Classifying explicitfeedback......................90
3.4.2Positive,negative,andneutralfeedback................91
vi

3.4.3Eliciting andnon-eliciting feedback..................92
3.4.4Formoffeedback............................92
3.4.5Meta-lev elandobject-levelfeedback..................93
3.4.6Fragmentfeedback/clari¯cation ellipsis...............93
3.4.7OwnCommunication Managemen t..................94
3.4.8Repairandrequestforrepair.....................94
3.4.9Request forfeedback..........................95
3.5Updatestrategies forgrounding ........................95
3.5.1Optimistic andpessimistic strategies .................95
3.5.2Grounding updatesandactionlevels.................96
3.5.3Thecautious strategy ..........................97
3.6Feedbackandgrounding strategies forIBiS.................98
3.6.1Grounding strategies fordialogue systems ..............99
3.6.2\Implicit" and\explicit" veri¯cation indialogue systems ......100
3.6.3Issue-based grounding inIBiS.....................100
3.6.4Enhancing theinformation statetohandlefeedback.........103
3.6.5Feedbackandsequencing dialogue moves...............105
3.6.6Grounding ofuserutterances inIBiS2................109
3.6.7Grounding ofsystemutterances inIBiS2...............130
3.6.8Evidence requiremen tsandimplicitgrounding ............138
3.6.9Sequencing ICM:reraising issuesandloadingplans.........142
3.7Furtherimplemen tationissues.........................145
vii

3.7.1Updatemodule.............................146
3.7.2Selection module............................146
3.8Discussion ....................................148
3.8.1Somegrounding-related phenomena nothandled byIBiS2.....148
3.8.2Towardsanissue-based accountofgrounding andactionlevels...149
3.8.3Comparison toTraum'scomputational theoryofgrounding .....149
3.9Summary ....................................151
4Addressing unraisedissues 153
4.1Introduction...................................153
4.2Somelimitations ofIBiS2...........................154
4.3Thenature(s) ofQUD.............................155
4.3.1Ginzburg's de¯nition ofQUD.....................155
4.3.2Openquestions notavailableforellipsisresolution ..........157
4.3.3Openbutnotexplicitly raisedquestions ...............157
4.3.4GlobalandlocalQUD.........................158
4.3.5SomeothernotionsofwhataQUDmightbe.............159
4.4Question Accommo dation...........................160
4.4.1Background: Accommo dation.....................160
4.4.2Accommo dation,interpretation, andtacitmoves...........161
4.4.3Extending thenotionofaccommo dation...............161
4.5Formalizing question accommo dation.....................162
viii

4.5.1Information stateinIBiS3.......................162
4.6Varietiesofquestion accommo dationandreaccommo dation.........164
4.6.1Issueaccommo dation:fromdialogue plantoISSUES ........165
4.6.2Localquestion accommo dation:fromISSUES toQUD.......168
4.6.3Issueclari¯cation ............................169
4.6.4Dependentissueaccommo dation:fromdomainresource toISSUES 171
4.6.5Dependentissueclari¯cation ......................176
4.6.6Question reaccommo dation ......................178
4.6.7Openingupimplicitgrounding issues.................182
4.7Furtherimplemen tationissues.........................191
4.7.1Dialogue moves.............................191
4.7.2 IBiS3updatemodule..........................191
4.7.3Selection module............................197
4.8Discussion ....................................197
4.8.1Phrasespottingandsyntaxin°exibledialogue ............197
4.8.2Relaxing constrain tsusingdenialanddependentreaccommo dation 199
4.8.3\Smart" interpretation .........................200
4.8.4Separating understanding, acceptance, andintegration .......201
4.8.5Accommo dationandthespeaker'sownutterances ..........201
4.8.6Accommo dationvs.normalintegration ................202
4.8.7Dependentissueaccommo dationinVoiceXML? ...........203
4.9Summary ....................................203
ix

5Action-orien tedandnegotiativ edialogue 205
5.1Introduction...................................205
5.2Issuesandactionsinaction-orien teddialogue ................206
5.3Extending IBiStohandleactionorienteddialogue ..............206
5.3.1Enhancing theinformation state....................206
5.3.2Dialogue moves.............................208
5.4Interacting withmenu-baseddevices .....................209
5.4.1Connecting devicestoIBiS......................209
5.4.2Frommenutodialogue plan......................212
5.4.3Extending theresolvesrelationformenu-basedAOD........212
5.5Implemen tationoftheVCRcontroldomain .................213
5.6Updaterulesanddialogue examples ......................215
5.6.1Integrating andrejecting requests ...................215
5.6.2Executing deviceactions........................216
5.6.3Selecting andintegrating con¯rm-moves................217
5.6.4Dialogue example: menutraversalandmultiplethreads.......218
5.6.5Actionaccommo dationandclari¯cation ...............220
5.6.6Dialogue examples: actionaccommo dationandclari¯cation .....222
5.7Issuesundernegotiation innegotiativ edialogue ...............223
5.7.1Sidner's theoryofnegotiativ edialogue ................223
5.7.2Negotiation asdiscussing alternativ es.................226
5.7.3IssuesUnderNegotiation (IUN)....................228
x

5.7.4Anexample ...............................230
5.8Discussion ....................................230
5.8.1Negotiation ininquiry-orien teddialogue ...............230
5.8.2Rejection, negotiation anddownshifting ................232
5.9Summary ....................................233
6Conclusions andfutureresearch 235
6.1Introduction...................................235
6.2Summary ....................................235
6.3Dialogue typology................................236
6.3.1Relation toDahlbÄack'sdialogue taxonom y..............238
6.3.2Relation toAllenet.al.'sdialogue classi¯cation ...........239
6.4Dialogue structure ...............................241
6.5Futureresearchareas..............................243
6.5.1Developingtheissue-based approachtogrounding ..........243
6.5.2Otherdialogue andactivitytypes...................245
6.5.3Semantics................................246
6.5.4Generalinference ............................247
6.5.5Naturallanguage inputandoutput..................247
6.5.6Applications andevaluation ......................248
6.6Conclusion ....................................249
ATrindiKitfunctionalit y 259
xi

A.1Introduction...................................259
A.2Datatypes....................................260
A.2.1Datatypede¯nition format.......................260
A.3Methodsforaccessing theTIS.........................268
A.3.1Objects,functions, locations,andevaluation .............268
A.3.2Conditions ................................270
A.3.3Queries .................................272
A.3.4Updates.................................272
A.4Rulede¯nition format .............................273
A.4.1Backtrackingandvariablebindinginrules..............274
A.4.2Condition andoperationmacros....................274
A.4.3PrologvariablesintheTIS.......................275
A.5TheDME-ADL language ............................275
A.6TheControl-ADL language ..........................277
A.6.1Serialcontrolalgorithm syntax....................277
A.7Providedmodules................................278
A.7.1Simpletextinputmodule.......................278
A.7.2Simpletextoutputmodule.......................278
A.7.3Asimpleinterpretation module....................278
A.7.4Asimplegeneration module......................279
BRulesandclasses 281
xii

B.1IBiS1......................................281
B.1.1 IBiS1updatemodule.........................281
B.1.2 IBiS1selectmodule..........................282
B.2IBiS2......................................282
B.2.1 IBiS2updatemodule.........................282
B.2.2 IBiS2selectmodule..........................284
B.3IBiS3......................................284
B.3.1 IBiS3updatemodule.........................284
B.3.2 IBiS3selectmodule..........................286
B.4IBiS4......................................287
B.4.1 IBiS4updatemodule.........................287
B.4.2 IBiS4selectmodule..........................289
xiii

xiv

ListofFigures
1.1AsketchoftheTrindiKit architecture ...................8
1.2TherelationbetweenTrindiKit andIBiS..................12
2.1IBiS1architecture ...............................21
2.2IBiS1Information Statetype.........................36
3.1IBiS2Information Statetype.........................103
4.1IBiS3Information Statetype.........................163
4.2Issueaccommo dation..............................165
4.3Localquestion accommo dation ........................168
4.4Dependentissueaccommo dation........................172
5.1IBiS4Information Statetype.........................207
5.2Connecting devicestoIBiS..........................209
5.3Example dialogue ................................231
xv

xvi

ListofTables
2.1Resolving answerstoquestions .........................29
2.2Relevantbutnotresolving answerstoquestions ...............31
2.3Combiningquestions andanswersintopropositions .............31
2.4Sortalrestrictions onpropositions .......................57
2.5Synonymysetsde¯ning thefunction lexsem .................57
2.6AfragmentoftheEnglish IBiS1travelagencylexicon ...........57
5.1Conversionofmenusintodialogue plans...................213
6.1Dialogue types.................................237
6.2Dialogue features ................................237
6.3Activities ....................................237
xvii

xviii

Chapter 1
Introduction
1.1Theaimofthisstudy
Theprimary aimofthisstudyistoexploreissue-based dialogue managemen t,anap-
proachtodialogue managemen tanddialogue modellingwhichregardsissues,modelled
semanticallyasquestions, asaprimary organizing andmotivatingforceindialogue.
Thisexploration willproceedbothonatheoretical andapractical implemen tationlevel.
Starting fromabasicaccountofissue-based dialogue managemen t,wegradually extend
thecoverageofthetheoryandtheimplemen tationtomorecomplex typesofdialogue. A
secondary aimistoexploitthedi®erences betweenthesuccessiv eversionsofthetheory
(andimplemen tation)toprovideaformalcharacterization ofdi®erenttypesofdialogue.
Wewillonlybeconcerned withwhatAllenetal.(2001)refertoaspracticaldialogue,i.e.
dialogue focusedonaccomplishing aconcrete task.
Ourgeneralstrategy forreachingthesegoalswillbetotryasfaraspossibleto\keepthings
simple"; thatis,foreachtypeofdialogue wetrytogiveanaccountthathandlesexactly
thosephenomena appearinginthattypeofdialogue. However,wealsowanttokeepthings
fairlygeneral,toenablereuseofcomponentsofasimpleversioninamorecomplex version
ofthetheoryandimplemen tation.
Inthischapter,wewill¯rstmotivateexploring theissue-based approachtodialogue man-
agement.Wewillthengiveanoutlineofthisthesisandgivebriefdescriptions ofthe
implemen tations. Finally,wewillintroducetheTrindiKit ,atoolkitforbuilding and
experimentingwithdialogue systems, whichhasbeenusedfortheimplemen tations.
1

2 CHAPTER 1.INTR ODUCTION
1.2Rationale
1.2.1Whydialogue managemen t?
Thepurposeofstudying dialogue modellinganddialogue managemen tistoprovidemodels
allowingustoexplorehowlanguage, andespeciallyspokendialogue, isusedindi®erent
activities (inthesenseofAllwood,1995).Whatenablesagents(humanormachines)to
participate indialogue? Whatkindofinformation doesadialogue participan t(orDP)need
tokeeptrackof?Howisthisinformation usedforinterpreting andgenerating linguistic
behaviour?Howisdialogue structured, andhowcanthesestructures beexplained? These
aresomeofthequestions thatareaddressed bytheoriesofdialogue modellinganddialogue
managemen t.
Apartfromthesemoretheoretical motivations,therearealsopractical reasonsforbeing
interestedinthese¯elds.Ourmainpractical concernisbuilding dialogue systemstoenable
naturalhuman-computer interaction. Thereisawidelyheldbeliefthatinterfacesusing
spokendialogue maybethe\nextbigthing"inthe¯eldofhuman-computer interaction.
However,webelievethatbeforethiscanhappen,dialogue systemsmustbecomemore°ex-
iblethancurrentlyavailablecommercial systems. Andtoachievethis,weneedtobaseour
implemen tationsonreasonable theoriesofdialogue modellinganddialogue managemen t.
Theimplemen tationofdialogue systemscanalsofeedbackintothetheoretical modellingof
dialogue, providedtheactualimplemen tationsarecloselyrelatedtotheunderlying theory
ofdialogue. OneofthedesigngoalsbehindTrindiKit istomakethedistance between
theoryandimplemen tationasshortaspossible,byprovidingahigh-levelprogramming
toolallowingabstraction fromlow-levelcomputational matters.
1.2.2Whyexploretheissue-based approach?
Thisthesisshowshowissues(modelledsemanticallyasquestions) ingeneralcanbeused
asabasisfordialogue managemen t.Butwhyshouldweexploretheissue-based approach
todialogue managemen t?Toanswerthisquestion, we¯rstneedtosetthescenebysaying
something aboutdialogue managemen tingeneral. Thereisstillnosingledominating
paradigm indialogue managemen t,butwecanattempt todiscernafewmajorcompeting
approaches.
Theplan-basedapproachhasitsoriginsinclassicAIandappliesplanning andplanrecog-
nitiontechnologies tothemodellingofactionsindialogue (i.e.utterances) (seee.g.Allen
andPerrault(1980),CohenandLevesque(1990),SidnerandIsrael(1981),Moore(1994)

1.2.RATIONALE 3
andCarberry(1990)). Workinthisareahassofarbeenprimarily theoretical andfairly
complex fromacomputational pointofview.Examples ofimplemen tationsusingthis
approacharetheTRAINS andTRIPSsystems(Allenetal.,2001).
Therelatedlogic-basedapproachisthatofrepresentingdialogue anddialogue contextin
somelogicalformalism (seee.g.Hulstijn (2000)andSadek(1991)). Thismakesitpossi-
bleinprinciple tododialogue managemen tusinggeneralreasoning machinery(inference
engines) toderiveexpectations andsuitable utterances tobeperformed. Examples of
implemen tationsusingthisapproachisSadek(1991)andBosandGabsdil(2000).
Itcanbequestioned whether generalplanning and/orinference isreallyneededindialogue
managemen t,especiallyfortherathersimplekindsofdialogues thataresu±cientformany
usefulapplications. Indeed,we¯ndthatmostsystemsthatareactuallydeployedusemuch
simplermethodsformodellingandmanaging dialogue.
Inthe¯nitestateapproach,dialogues arescriptedutterance byutterance onaveryconcrete
level.Eachutterance leadstoanewstate,wherevariouspossiblefollowuputterances are
allowed,eachleadingtoanewstate.Asamodelofdialogue thisapproachisproblematic
sinceitdoesnotreallyexplaindialogue structure; rather,itdescribesit,andinavery
rigidway.Asatoolfordialogue modelling,the¯nitestateapproachisinpractice limited
toverysimpledialogue wherethenumberofavailableoptionsatanypointinthedialogue
isverysmall.The¯nite-state approachisusede.g.bySuttonandKayser(1996).
Intheform-based(orframe-based)approach,dialogue isreduced totheprocessof¯lling
inaform.Formsprovideaverybasicformalism whichissu±cientforsimpledialogue,
butitishardtoseehowitcanbeextended tohandlemorecomplex kindsofdialogue, e.g.
negotiativ e,tutorial, orcollaborativeplanning dialogue. Issue-based dialogue managemen t,
ontheotherhand,isindependentofthechoiceofsemanticformalism. Thisenablesan
issue-based systemtobeincremen tallyextended tohandledialogue phenomena involving
morecomplex semantics.Theform-based approachisusede.g.inVoiceXML (McGlashan
etal.,2001)andMIMIC(Chu-Carroll, 2000).
Inanabstract sense,thegoalofallpractical dialogue istocommunicateinformation which
isusefulinsomeactivity.Thismeansthatconversational goalsshoulddescribemissing
information. Toful¯laconversational goal,whatweneedtodoistocommunicatethe
missinginformation. Now,aprimary reasontosuspectthattheissue-based approachto
dialogue managemen tmightbeworthexploring isthatissues,orquestions, essentiallyare
entitiesspecifyingcertainpiecesofas-yet-unavailableinformation. Thatis,conversational
goalscantoalargeextentbemodelledasquestions.
Inaddition toissuesarisingfromtheactivityinwhichadialogue takesplace,therearealso
\meta-issues" whicharisefromthedialogue itself.Didtheotherparticipan tunderstand
myutterance correctly? ShouldIacceptwhatshejustsaidastrue?Havewereacheda

4 CHAPTER 1.INTR ODUCTION
mutualunderstanding ofwhatImeantwithmyprevious utterance?
Intheissue-based approachwetakequestions tobe¯rst-class (i.e.irreducible) objects.
Thisisgenerally notdoneineitherframe-based orplan-based approaches.Insteadofrep-
resentingquestions directly,frame-based andplan-based theories userelatedmechanisms
whichdosimilarworkbutdonothavethesameindependentmotivationasquestions.
1.3Outlineofthisthesis
Belowisanoverviewofthechaptersofthisthesis,withshortdescriptions oftheircontents.
Thebasicstructure ofthethesisisto¯rstexplorebasicissue-based dialogue managemen t
andimplemen tabasicsystemillustrating theuseofissue-based dialogue managemen t.
Inthefollowingchapters, thissimplesystemisextended tohandlethegrounding issues,
addressing unraised issues,action-orien teddialogue andandissuesundernegotiation.
²Chapter2:Basicissue-based dialoguemanagemen t.Asastarting pointfor
exploring issue-based dialogue managemen tusingtheinformation stateapproach,
Ginzburg's concept ofQuestions UnderDiscussion isintroduced,andwebeginto
exploretheuseofQUDasthebasisforthedialogue managemen t(Dialogue Move
Engine)componentofadialogue system.ThebasicusesofQUDistomodelraising
andaddressing issuesindialogue, including theresolution ofelliptical answers.Also,
dialogue plansandasimplesemanticsisintroducedandimplemen ted.
²Chapter3:Grounding issues. Inalldialogue, issuesconcerning contact,per-
ception, understanding andacceptance ofutterances areofcentralimportance. We
refertotheseas\meta-issues", or\grounding issues". Wegiveanaccountofthese
issueswheretheconcepts ofoptimism andpessimism regarding grounding areem-
ployed.Apartial-co veragemodeloffeedbackrelatedtogrounding ismotivatedfrom
theperspectiveofusefulness inadialogue system,andimplemen ted.Thisallows
thesystemtoproduceandrespondtofeedbackconcerning issuesdealingwiththe
grounding ofutterances.
²Chapter4:Addressing unraisedissues. Inchapter2,wesawhowdialogue
canbedrivenbyraisingandaddressing issues.Butinrealdialogue, oneoften
seesutterances whichcanbeconstrued asaddressing issueswhichhavenotbeen
explicitly raisedinthedialogue. Toenablemore°exibledialogue behaviour,we
makeadistinction betweenalocalandaglobalQUD(referring tothelatteras
\openissues",orjust\issues"). Thenotionsofquestion andissueaccommo dation
arethenintroducedtoallowthesystemtobemore°exibleinthewayutterances
areinterpreted relativetothedialogue context.Question accommo dationallowsthe

1.4.THEIBISFAMIL YOFSYSTEMS 5
systemtounderstand answersaddressing issueswhichhavenotyetbeenraised.In
casesofambiguity,whereananswermatchesseveralpossiblequestions, clari¯cation
dialogues maybeneeded.
²Chapter5:Action-orien tedandnegotiativ edialogue. Weextendourtheory
andtheIBiSsystemtohandleaction-orien teddialogue (AOD),whichinvolveDPs
performing non-comm unicativeactionssuchase.g.reserving tickets.Inaddition to
issuesandquestions underdiscussion, thissystemalsohastokeeptrackofactions.
Theconceptofissueaccommo dationisextended toincludeactionaccommo dation.
Weillustrate AODwithanimplemen tationofaVCRcontrolsystem,whosedialogue
plansarebasedonmenus.Anissue-based accountofnegotiativ edialogue (ND)is
thensketched(butnotimplemen ted).ThenotionofIssuesUnderNegotiation is
introducedtoaccountforsituations whereseveralalternativ esolutions (answers)to
aproblem (issue)arebeingdiscussed.
²Chapter6:Conclusions andfutureresearch.We¯rstsummarize theprevious
chapters. Wethenusetheresultstoclassifyvariousdialogue typesandapplications,
andsaysomething abouttherelation oftheissue-based modeltheanaccountof
dialogue structure. Finally,wediscussfutureresearchissues.
1.4TheIBiSfamilyofsystems
InthisthesiswedescribefourversionsoftheIBiSsystem1.Starting fromasimpleversion
(IBiS1)illustrating issue-based dialogue managemen tforwhatwe(followingHulstijn,
2000)refertoasinquiry-oriente ddialogue(e.g.database searchdialogue), thethesis
gradually developsboththeoryandimplemen tationtoalsohandlegrounding, question
accommo dationandaction-orien teddialogue. Below,welistsomeimportantfeatures of
eachofthefourversions.AppendixBlistsallrulesandruleclassesusedbytherespective
systems, withreferences tothepagewheretheyareexplained.
²IBiS1
{Inquiry-orien teddialogue
{Multitasking
{Information sharingbetweenplans
{Perfectcommunication assumed
{Application totravelinformation
1TheIBiSsystemislooselybasedontheprevious GoDiSsystem(Larsson etal.,2000a)However,the
dialogue managemen tcomponentswererewritten fromscratchforIBiS.

6 CHAPTER 1.INTR ODUCTION
²IBiS2
{InteractiveCommunication Managemen t(ICM),including grounding andse-
quencing
{Issue-based grounding
{Dynamic grounding andfeedbackstrategies
²IBiS3
{Question accommo dation
{Denyingandrevisinginformation
{Correcting thesystem
²IBiS4
{ActionOrientedDialogue
{Application tomenu-basedVCRcontrol
1.5TrindiKit
Fortheimplemen tationofIBiSwewilluseTrindiKit ,atoolkitforimplemen tingand
experimentingwithInformation StatesandDialogue MoveEngines2.Inthissection,we
givearoughoverviewoftheinformation stateapproachasimplemen tedinTrindiKit ;a
moredetailed descriptions ofrelevantpartsofTrindiKit canbefoundinAppendixA.
TheaimofTrindiKit istoprovideaframeworkforexperimentingwithimplemen tations
ofdi®erenttheories ofinformation state,information stateupdateanddialogue control.
Keytotheinformation stateapproachisidentifyingtherelevantaspectsofinformation
indialogue, howtheyareupdated,andhowupdatingprocessesarecontrolled. This
simpleviewcanbeusedtocompare arangeofapproachesandspeci¯ctheoriesofdialogue
managemen twithinthesameframework.
Theinformation stateofaDPrepresentstheinformation thattheDPhasataparticular
pointinthedialogue, incorporatingthecumulativeadditions fromprevious actionsinthe
dialogue, andmotivatingfutureaction.Forexample, statemen tsgenerally addproposi-
tionalinformation; questions generally providemotivationforotherstoprovidespeci¯c
statemen ts.Information stateisalsoreferredtobysimilarnames,suchas\conversational
score",or\discourse context"and\mentalstate".
2Thissectioncontainsmaterial fromLarssonandTraum(2000).

1.5.TRINDIKIT 7
TheTrindiKit isatoolkittoallowsystemdesigners tobuilddialogue managemen tcom-
ponentsaccording totheirparticular theories ofinformation states.Itallowsspeci¯c
theories ofdialogue tobeformalized, implemen ted,tested,compared, anditerativelyre-
formulated.Keytothisapproachisthenotionofupdateofinformation state,withmost
updatesrelatedtotheobservationandperformance ofdialoguemoves.
Weviewaninformation statetheoryofdialogue modellingasconsisting ofthefollowing:
²Adescription oftheinformational componentsofthetheoryofdialogue mod-
elling,including aspectsofcommon contextaswellasinternalmotivatingfactors
(e.g.,participan ts,common ground,linguistic andintentionalstructure, obligations
andcommitmen ts,beliefs,intentions,usermodels,etc.).
²Formalrepresentations oftheabovecomponents(e.g.,aslists,sets,typedfea-
turestructures, records, Discourse Represen tationStructures (DRSs), propositions
ormodaloperatorswithinalogic,etc.).
²Asetofdialoguemovesthatwilltriggertheupdateoftheinformation state.
Thesewillgenerally alsobecorrelated withexternally performed actions, suchas
particular naturallanguage utterances. Acomplete theoryofdialogue behaviourwill
alsorequirerulesforrecognizing andrealizing theperformance ofthesemoves,e.g.,
withtraditional speechandnaturallanguage understanding andgeneration systems.
²Asetofupdaterules,thatgoverntheupdatingoftheinformation state,given
variousconditions ofthecurrentinformation stateandperformed dialogue moves,
including (inthecaseofparticipating inadialogue ratherthanjustmonitoring one)
asetofselection rules,thatlicensechoosingaparticular dialogue movetoperform
givenconditions ofthecurrentinformation state.
²Anupdatestrategy fordeciding whichrule(s)toselectatagivenpoint,fromthe
setofapplicable ones.Thisstrategy canrangefromsomething assimpleas\pick
the¯rstrulethatapplies" tomoresophisticated arbitration mechanisms, basedon
gametheory,utilitytheory,orstatistical methods.
Because ofitsgenerality,TrindiKit allowsimplemen tation,andcomparison ofawide
rangeoftheoriesofdialogue managemen t,rangingfromsystemsbasedonFSAstocomplex
systems basedongeneralreasoning, planning, andplanrecognition. Importantdesign
goalsbehindtheTrindiKit architecture includemakingthedistance betweentheoryand
implemen tationasshortaspossible,andprovidingaframeworkenabling amodularplug-
and-playapproachtotheconstruction ofdialogue systems. TheTrindiKit architecture
supportsandencourages theseparation ofproceduraldialogue knowledge(whichisspeci¯c
todialogue type)fromdomainknowledge(whichisspeci¯ctoacertaindomain).

8 CHAPTER 1.INTR ODUCTION
Figure1.1:AsketchoftheTrindiKit architecture

1.5.TRINDIKIT 9
TrindiKit implemen tsanarchitecture basedonthenotionofaninformation state.Asys-
temconsistsofanumberofmodules(including speechrecognizer andsynthesizer, natural
language interpretation andgeneration, andaDialogue MoveEngine)whichcanreadfrom
andwritetotheinformation stateusinginformation stateupdaterules.External resources
canbehookeduptotheinformation state.Acontrollerwiresthemodulestogether. The
TrindiKit architecture isoutlined inFigure1.1.
Themaincomponentsofthearchitecture arethefollowing:
²theTotalInformation State(TIS),consisting of
{theInformation State(IS)variable
{moduleinterfacevariables
{resource interfacevariables;
²theDialogue MoveEngine(DME), consisting ofoneormoremodules;theDMEis
responsibleforupdatingtheTISbasedonobservedmoves,andselecting movesto
beperformed bythesystem;
²othermodules,operatingaccording tomodulealgorithms;
²acontroller,wiringtogether theothermodules,eitherinsequence orthrough some
asynchronous mechanism;and
²resources, suchaslexicons, databases, deviceinterfaces, etc.
TotalInformation StateTheTotalInformation State(TIS)consistsofthreecompo-
nents:theinformation statevariable(IS),themoduleinterfacevariables(MIVs), andthe
resource interfacevariables(RIVs).
TheISvariable,themoduleinterfacevariables, andtheresource interfacevariables go
underthecollectivenameTISvariables .InTrindiKit ,eachTISvariableisde¯nedas
anabstract datastructure, i.e.anobjectofacertaindatatype.TheTISisaccessed by
modulesthrough conditions andupdates,andthedatatypesofthevariouscomponentsof
theTISdetermine whichconditions andupdatesareavailable.
Information State(IS)TheInformation Staterepresentsinformation availabletoa
dialogue participan t,atanygivenstageofthedialogue. Theinformation stateismodelled
asanabstract datastructure (record, DRS,set,stacketc.)whichcanbeinspectedand
updatedbydialogue systemmodules.

10 CHAPTER 1.INTR ODUCTION
DialogueMoveEngine TheDialogueMoveEngineisthemoduleorcollection ofmod-
uleswhichupdatestheinformation statebasedonobserveddialogue moves,andforselect-
ingmovestobeperformed. Abstractly ,theDMEcanbeseenasimplemen tingafunction
fromacollection ofinputdialogue movesandaningoinginformation statetoacollection
ofoutputdialogue movesandanoutgoing state(seealsoLjunglÄof,2000).
ADMEcanberegarded asadialogue manager basedontheconcepts ofdialogue moves
andinformation states.ThismeansthataDMEisacertaintypeofdialogue manager,
i.e.onewhichaccesses aninformation stateandwhoseinputandoutputaredialogue
moves.Dialogue managers whicharenotDMEsaree.g.thosewhichuse¯nitestate
representationsofadialogue andtakestringsoftextasinputandoutput,suchasthe
CSLUtoolkit(SuttonandKayser,1996).
UpdaterulesUpdaterulesarerulesforupdatingtheinformation state.Theyconsist
ofarulename,aprecondition list,andane®ectlist.Thepreconditions areconditions on
theTIS,andthee®ectsareoperations ontheTIS.Ifthepreconditions ofarulearetrue
fortheTIS,thenthee®ectsofthatrulecanbeappliedtotheTIS.Rulesalsohaveaclass.
TothisextentourupdaterulesaresimilartoSTRIPS operators(FikesandNilsson,1971).
Theformatwewilluseisgivenin(1.1).
(1.1) rule:Rulename
class:Ruleclass
pre:8
>>><
>>>:Condition 1
Condition 2
...
Condition n
eff:8
>>><
>>>:Update 1
Update 2
...
Update m
Rulesaregroupedintoclassesandthereisanupdatealgorithm whichdetermines when
thevariousclassesofrulesshould¯re.Iftheconditions holdwhentheruleistried,the
updateswillbeappliedtotheinformation state.
Updatealgorithms Updatealgorithms arealgorithms forupdatingtheTIS.Theyin-
cludeconditions ontheTISandcallstoapply(classesof)updaterules.
Amodulecontainsoneormorealgorithms whichitexecutes according toinstructions from
thecontroller.Thealgorithm language containsthebasicimperativeconstructions, and

1.5.TRINDIKIT 11
allowscallstoupdaterulesandupdateruleclassesaswellaschecks,queriesandupdatesto
theTIS.TrindiKit providesalanguage forwritingmodulealgorithms, calledDME-ADL
(Dialogue MoveEngineAlgorithm De¯nition Language).
ModulesInaddition totheDMEtherearemoduleslikespeechrecognizers, parsers,
etcetera. Modulescaninspectandupdatethetotalinformation state.
Typically,non-DME modulescanonlyaccessacertainnumberofdesignated TISvariables,
so-called moduleinterfacevariables .Thepurposeofthesevariablesistoenablenon-DME
modulestointeractwitheachotherandwiththeDMEmodules.Itispossibletoallow
non-DME modulestoaccesstheIS,butthiswillsigni¯can tlyreducetheabilitytousethe
moduleinsystemsusingotherkindsofIStypes.
Controller Thecontrollerwiresthemodulestogether usingacontrolalgorithm. It
canalsoaccessthewholeTIS.ATrindiKit systemcanberuneitherseriallyorasyn-
chronously .
Resources andresourceinterfaces Resources areattachedtotheTISviaresource
interfaces, consisting ofadatatypede¯nition fortheresource andaresource variableof
thattype.AsotherpartsoftheTIS,theyareaccessed fromupdaterulesviaconditions
andupdates.
Anoteonthedi®erence betweenmodulesandresources: Resources aredeclarativ eknowl-
edgesources, external totheinformation state,whichareusedinupdaterulesandal-
gorithms. Modules,ontheotherhand,areagentswhichinteractwiththeinformation
stateandarecalleduponbythecontroller.Ofcourse,thereisaproceduralelementto
allkindsofinformation search,whichmeansamongotherthingsthatonemustbecareful
nottoengageinextensivetime-consuming searches.Conversely,modulescanbede¯ned
declarativ elyandthushaveadeclarativ eelement.Thereisnosharpdistinction dictat-
ingthechoicebetweenresource ormodule;forexample, itispossibletohavetheparser
bearesource. However,itisimportanttoconsider theconsequences ofchoosingtosee
something asaresource ormodule.
Bysupportingresources, TrindiKit encourages modularitywithregardtothevarious
knowledge-bases usedbyasystem.Forexample, separating domain-sp eci¯cbutlanguage-
independentknowledgefromalanguage-dep endent(anddomain-sp eci¯c)lexiconenables
loadinganewlanguage withouta®ecting thedomainknowledge,andthereisonlyone¯le
toeditwheneditingthedomainknowledge,whichdecreases theriskforerror.

12 CHAPTER 1.INTR ODUCTION
Buildingasystem
Tobuildasystem, onemustminimally supplyanInformation Statetypedeclaration,
aDMEconsisting ofTISupdaterulesandoneorseveralmodulealgorithm(s), anda
controller,operatingaccording toacontrolalgorithm. Anyusefulsystemisalsolikely
toneedadditional modules,e.g.forgettinginputfromtheuser,interpreting thisinput,
generating systemutterances, andprovidingoutputfortheuser.Alsoneededareinterface
variablesforthesemodules,whicharedesignated partsoftheTISwherethemodulesare
allowedtoreadandwriteaccording totheirassociatedTISaccessrestrictions.
Thisprovidesuswithadomain-indep endentsystem. Touseasystemforanapplica-
tiononemustalsoprovideresources suchasdatabases, planlibraries etc.Theresources
areaccessible fromthemodulesthrough theresource interfaces, whichde¯neapplicable
conditions and(optionally) operations ontheresource.
Figure1.2:TherelationbetweenTrindiKit andIBiS
Asanexample, therelationbetweenTrindiKit ,IBiS,andanIBiSapplication isshown

1.6.SUMMAR Y 13
inFigure1.2.
1.6Summary
Inthischapter,wepresentedtheaimofthisstudyandgavesomeinitialmotivations
forexploring theissue-based approachtodialogue managemen t.Wethengaveabrief
overviewofthethesisandtherelatedversionsoftheIBiSsystem.Finally,wegaveavery
briefintroductiontotheTrindiKit architecture andtheinformation stateapproachto
dialogue implemen tedtherein.

14 CHAPTER 1.INTR ODUCTION

Chapter 2
Basic issue-based dialogue
managemen t
2.1Introduction
Thischapterdescribesthetheoretical foundations andimplemen tationofthebasicIBiS
system(IBiS1)forhandling inquiry-orien teddialogue usingQuestions UnderDiscussion
anddomain-sp eci¯cdialogue plans.We¯rstdiscussthenotionofinquiry-orien teddialogue.
ThenwepresenttheIBiS1systemwhichimplemen tsourinitialaccountofinquiry-orien ted
dialogue. TheupdaterulesforthissystemarebasedonGinzburg's accountofquerying
andassertion indialogue (Ginzburg, forthand1996).Weargueforsomemodi¯cations
ofthetheory,partlyfromtheviewpointofusefulness inadialogue system. Wealsogive
examples ofdialogues withthesystem. Finally,wediscusstheissue-based approachto
dialogue managemen tandcompare itwithsomeotherapproaches.
2.1.1Asampledialogue
Belowisasimpleexample whatwewillrefertoasinquiry-oriente ddialogueconducted
betweenauserandIBiS11.
1Thedialogues numbered(dialogue x.y)areactualdialogues withtheIBiSsystem,generated auto-
matically bytheLATEXprintingfacilityinTrindiKit .Somedialogues havebeenmanuallypost-processed
toremoveirrelevantinformation andincreasereadabilit y.Forconvenience,thetextinterfacehasbeenused
togenerate theexamples, butIBiScanalsousespokeninputandoutput. Insomeexamples, numbers
areappendedtoutterances toindicate (fake)speechrecognition scores.Theinformation statesoccuring
insomedialogues haveoccasionally beenabbreviated byremovingorabbreviating irrelevantinformation.
15

16 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
(dialogue 2.1)
S>Welcome tothetravelagency!
U>hello
U>priceinformation please
S>Howdoyouwanttotravel?
U>aflightplease
S>Whatcitydoyouwanttogoto?
U>paris
S>Whatcitydoyouwanttogofrom?
U>fromlondon
S>Whatmonthdoyouwanttoleave?
U>inapril
S>Whatdaydoyouwanttoleave?
U>ascheapaspossible
S>Whatdaydoyouwanttoleave?
U>thefifth
S>Whatclassdidyouhaveinmind?
U>ascheapaspossible
S>Itwillcost123crowns.
U>bye
S>Thankyouforyourvisit!
Typically,aninquiry-orien teddialogue willstartwithaquestion fromtheinquirer(inthe
contextofadialogue system,user).Followingthis,theexpert(system) willasktheinquirer
anumberofquestions andperformadatabase searchbasedontheanswersgivenbythe
inquirer. Thissubsection ofthedialogue canbeviewedasaninformation-seeking dialogue
withtheexpertaskingthequestions andtheinquirer providingtheanswers.Finally,
theexpertcananswertheinquirers initialquerybasedontheresultsofthedatabase
search.Thepairingoftheinquirers initialqueryandtheexpert's¯nalanswercanalso
beregarded asaninformation-seeking dialogue (although discontinuous).Thedialogue as
awholecontainsquestions frombothexpertandinquirer andisthusaninquiry-orien ted
dialogue.
2.1.2Information exchangeandinquiry-orien teddialogue
If\exchangeofinformation" istakeninitswidestsense,itispossibletoarguethatall
dialogue isinformation exchangedialogue, sincealldialogue involvestheexchangeofin-
formation betweenDPs.Forexample, GeneralBgivinganordertoprivateHtocleanthe
hallcouldbeseenasexchanging theinformation thatHmustcleanthehall.Giventhis
de¯nition, theterm\information exchangedialogue" wouldmeanthesameas\dialogue".

2.1.INTR ODUCTION 17
Itisuseful,however,tohaveaconceptofinquiry-orien teddialogue whichdoesnotinclude
givingordersorinstructions toperformactionschanging thestateoftheworld(rather
thanjustchanging theinformation statesofDPs),orindeedanyutterance resulting ina
DPhavinganobligation orcommitmen ttoperformsomeaction.However,itmustalso
berememberedthatutterances arealsoactions,andDPscanbeobligedtoperformthem;
forexample, aquestion canbesaidtointroduceanobligation onthehearertorespondto
thatquestion. Sowestillwanttoallowutterances whichresultinobligations toperform
communicativeactionsthatarepartofthedialogue2.Ofcourse,thesameappliestothese
obligedactionsthemselv es.Ine®ect,thisde¯nitions servestoexcludeorders,instructions
etc.frominformation-orien teddialogue.
Withthismotivation,thetermInquiryOrientedDialogue, orIOD,willhenceforth betaken
torefertoanydialogue whosesolepurposeisthetransference ofinformation, andwhich
doesnotinvolveanyDPassuming (ortryingtomakeanotherDPassume) commitmen ts
orobligations concerning anynon-comm unicativeactionsoutsidethedialogue.
Hulstijn (2000)de¯nesthedialogue gameofinquiryinthefollowingway:
Thedialogue gameofinquiryisde¯nedastheexchangeofinformation between
twoparticipan ts:aninquirer andanexpert(...).Theinquirer hasacertain
information need.Hergoalinthegameistoaskquestions inthedomainin
ordertosatisfyherinformation need.Theexperthasaccesstoadatabase
aboutthedomain. Hisgoalistoanswerquestions. (...)[T]heexpertmayask
questions too.(Hulstijn, 2000p.66)
Here,tworolesareintroduced:inquirerandexpert.Thisconceptisparticularly wellsuited
fordialogue systemsfordatabase search,whichhappenstobethetypeofdialogue wewill
initiallybeexploring. Inadialogue systemsetting,thesystemistypicallytheexpertand
theuseristheinquirer.
Initially,wewillbedealingonlywithasubtypeofinquiry-orien teddialogue, namelynon-
negotiative IOD.Negotiativ edialogue hererefersto,roughly,dialogue whereDPscan
discussandcompare severaldi®erentalternativ esolutions toaproblem. Non-negotiativ e
dialogue issu±cientwhendatabase searchescanbeexpectedtoreturnonlyasingleresult
(ratherthane.g.atable).Obviouslythisisinsu±cien tfordealingwithmanyinformation-
seekingdomains andapplications. InChapter 4wewillbeabletohandlesemi-negotiative
dialogue, whereseveralalternativ escanbeintroducedinthedialogue; however,theintro-
ductionofanewalternativ ewillalwaysremovetheprevious alternativ ewhichthuscannot
bereturned tounlessreintroduced\fromscratch".
2Thereservationthattheobligedactionsarepartofthedialogue ismeanttoexcludeutterances which
imposeanobligation toperformacommunicativeactiondirected atsomeagentwhoisnotaDP,e.g.
\TellMarthatogohome".

18 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
2.2Sharedandprivateinformation indialogue
Thebasicideaofissue-based dialogue managemen tistodescribedialogue intermsof
issuesbeingraisedandresolved.TheDP'suserepresentationsoftheseissuestomanage
theircontributions todialogue. Theinformation stateapproachtodialogue managemen t
providesthetoolsforformalizing thetypeofinformation thatDP'skeeptrackof,andhow
thisinformation isupdatedasthedialogue proceeds.
Abasicdivision ofthisinformation isthatofprivateinformation and(whattheDP
believestobe)sharedinformation. Variousformulations ofthesharedparthasbeen
proposed,followingStalnaker(1979),andvarioustermshavebeenusedtodescribeit.
Theprivatepartoftheinformation statehasbeenthesubjectofmuchworkinAI,e.g.
CohenandLevesque(1990)andRaoandGeorge® (1991),andworkondialogue inspired
byAI,e.g.AllenandPerrault(1980),SidnerandIsrael(1981),Carberry(1990),Grosz
andSidner(1990)andSadek(1991).Thismodelhasalsobeenextended toincludeshared
information, e.g.socialattitudes suchasobligations (TraumandHinkelman,1992,Traum
andAllen,1994,Traum,1996).
InthisthesiswewillstartfromGinzburg's notionofaDialogue Gameboard(DGB)asa
modelofthesharedpartoftheinformation state.Ginzburg's modelalsoincludes whatcan
beseenasaplace-holder fortheprivatepartoftheinformation state:aDP'sunpublicized
mentalsituation (UNPUB-MS). Wewillprovideanexplicitstructuring ofUNPUB-MS
in°uenced bytheBDImodel.
Thissectionprovidesashortintroductiontothenotionofaconversational scoreboard,
andGinzburg's developmentofthisnotion,theDGB.Wealsogiveabriefintroductionto
theBDImodel.
2.2.1TheBDImodel
IntheBDImodel(Wooldridge andJennings, 1995,CohenandLevesque,1990,Raoand
George®, 1991),agentsaremodelledusingthreeprivateattitudes: Belief,Desire,and
Intention.Aroughdescription oftheseattitudes mayrunasfollows,although thereare
manyotherformulations: Beliefsarepropositionstakentobetruebyanagent;Desires
are,roughly,goalsthattheagentwishestoachieve(although hemaynotintendtodoso,
e.g.ifhebelievesthatthegoalcannotbeachieved).Intentionsareactionsthetheagent
intendstoperform.
Often,BDImodelsareusedasabasisforformulatingrationalit yconstrain tsguidingthe
behaviourofrationalagents.Theseconstrain tshavetheformoflogicalinference rulesin

2.2.SHARED AND PRIVATEINFORMA TION INDIALOGUE 19
somemodallogic,andthuspresupposecomplete andcorrectinferentialabilitiesinrational
agents.Inimplemen tations,inference usuallyrequires someinference heuristics inorder
toavoidexcessivecomputational complexit y.Adiscussion ofBDImodelsofdialogue and
therelationtoQUD-based modelscanbefoundinLarsson(1998).
2.2.2StalnakerandLewis
InStalnaker(1979),Stalnakerusestheconcept ofacommongroundwhichkeepstrack
ofthecurrentstateofadialogue. OnStalnaker'saccount,thecommon groundisan
unstructured setofpropositions; also,Stalnakeronlydealswiththee®ectsofassertions
onthescoreboard.Typically,thee®ectofasserting aproposition pistoaddptothe
scoreboard3
DavidLewis,inLewis(1979),drawingananalogue betweenconversation andbaseball,
usesa\conversational scoreboard"tokeeptrackofconversational interaction. Lewisalso
introducestheconceptofaccommodationtodescribehowthescoreboardcan\evolvein
suchawayasisrequired inordertomakewhateveroccurscountascorrectplay."This
notionwillbeexploited inChapter 4;inbrief,ifsomeutterance urequires Xtobeinthe
scoreboardinordertobefelicitous, andXisnotinthescoreboardwhenuisuttered, X
isaccommo dated(addedtothescoreboard)sothatubecomesfelicitous.
2.2.3Ginzburg's Dialogue Gameboard
Themaindi®erence betweenStalnaker'sandLewis'modelsandGinzburg's isthatwhile
theformerassumeafairlyunstructured formalization ofcommon ground-essentially,a
setofpropositions -thelatterprovidesaricherstructure whichincludes propositions,
questions, anddialogue moves.Also,whileStalnakerandLewisweremainlyinterested in
howassertions changethecommon ground,Ginzburg's inclusion ofquestions enablesthe
modellingofhowtheraisingofquestions a®ectthecommon ground.
Ginzburg alsostressesthattheDGBisaquasi-shar edobject,inthesensethateachDPhas
herownversionoftheDGBandtheremaybedi®erences (mismatc hes)betweentheDGBs
ofdi®erentDPs.ThisfollowsfromtheviewthatDGBandUNPUB-MS arecomponents
ofaDPsmentalstate.
InGinzburg (1996),Ginzburg structures aparticipan t'sversionoftheDGBintothree
3Tobemoreprecise,Stalnakerseesthecommon groundasthesetofpossibleworldscompatible with
allpropositionsasserted sofar,andthee®ectofasserting anewpropositionpistoremoveanyworldsin
whichPisnottrue.

20 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
separate ¯eldswhichhedescribesasfollows:
²FACTS:setofcommonly agreeduponfacts
²QUD('questions underdiscussion'): asetthatspeci¯esthecurrentlydiscussable
questions, partially orderedbyÁ('takesconversational precedence'). Ifqismaximal
inQUD,itispermissible toprovideanyinformation speci¯ctoqusing(optionally)
ashortanswer.
²LATEST-MO VE:contentofthelatestmovemade:itispermissible tomakewhatever
movesareavailableasreactions tothelatestmove.
QUDisintendedtomodelaviewofconversation asthesettingupofpossiblequestions
todiscussandthesubsequen tresolving ofsomeofthesequestions. Atanytime,aspeaker
maychoosetoaddsomething totheQUD,ortoaddressoneofthequestions intheQUD.
Thee®ectontheDGBofaDPaskingaquestion isto(a)\signi¯can tlyrestrictthespace
offelicitous follow-upassertions orqueries", and(b)\tolicenseanelliptical formwhich
(overtly)conveysonlythefocuscomponentoftheresponse".
Asanexample, S'sutterance in(2.1)resultsinthequestion \Whatcitydoestheuserwant
togoto?"beingaddedtoQUD.Thislicensestheelliptical responseinU'sutterance.
(2.1)S>Whatcitydoyouwanttogoto?
U>paris
2.3OverviewofIBiS1
Ourinitialsystemwillbeabletohandlesimplenon-negotiativ einquiry-orien teddialogue,
usinganaccountofbasicissue-based dialogue managemen tbasedonGinzburg's theory.
2.3.1IBiS1architecture
TheIBiS1architecture shownbelowisaninstantiationofthegeneralTrindiKit architec-
ture.Thecomponentsofthearchitecture arethefollowing:
²theInformation State(IS)

2.3.OVERVIEW OFIBIS1 21
²domain-indep endentmodules,operatingaccording tomodulealgorithms
²theDialogue MoveEngine(DME), consisting oftwomodules(UpdateandSelect);
theDMEisresponsibleforupdatingtheISbasedonobservedmoves,andselecting
movestobeperformed bythesystem.
²acontroller,wiringtogether theothermodules,eitherinsequence orthrough an
asynchronous mechanism.
²threedomain-dep endentresources: Database, Lexicon, andDomain Knowledge
Figure2.1:IBiS1architecture
Thisarchitecture isusedalsoforIBiS2andIBiS3;however,forIBiS4wewillusea
di®erentresource con¯guration.
Controlalgorithm
Thecontrolalgorithm usedbyIBiS1isshownin(2.2).

22 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
(2.2)repeathselect
ifnotisempty($nextmoves)
thenhgenerate
output
updatei
test($program state==run)
input
interpret
updatei
TheIBiSsystemusesmodulesincluded intheTrindiKit packageforinput,interpre-
tation,generation andoutput. Theinterpretation andgeneration modulesaredescribed
inSectionA.7.Theupdateandselection modulesaredescribedinSections 2.8and2.9,
respectively.
Turntakingisregulated bythefollowingprinciple: ifselect¯ndsamovetoperform,the
systemwillgenerate astringandoutputittotheuser.TheTISisthenupdated,and
providedtheprogram statevariableisstillsettorun,thesystemreadsinputfromthe
user,interpretsit,andagainupdatestheTIS.Thismeansthatifselect¯ndsnomoveto
perform,theturnwillbehandedovertotheuser.
2.3.2Simplifying assumptions
Forourinitialsystem,wewillmakesomesimplifying assumptions, whichine®ectwillpro-
videuswithasystemthatonlyhandlesalimitedrangeofdialogue phenomena. Later,we
willremovesomeoftheselimitations andextendtheimplemen tationcorrespondingly.The
simplifying assumptions willmakeiteasiertoformulateasimplebasicsetofinformation
stateupdaterules.
²Allutterancesareunderstoodandaccepted.Thisassumption willberemovedin
Section3.
²Utteranceinterpretationdoesnotinvolvetheidenti¯cationofreferents,andreferents
arenotrepresentedintheinformation state.Thisassumption willberemovedin
Chapter 5.
²Complex semantic representation isnotneededforsimplekindsofdialogue.This
assumption willnotberemoved;however,itisclearthatamorecomplex semantic
analysis involvinge.g.quanti¯cation, temporality,andmodalitywouldberequired

2.3.OVERVIEW OFIBIS1 23
formorecomplex dialogues. Webelieve,however,thattheaspectsofdialogue man-
agementproposedinthisthesisislargelyindependentofthismoredetailedsemantic
treatmen t.
Ofcourse,wedonotclaimthatthisisanexhaustiv elistofallthesimplifying assumptions
thathavebeenmade,consciously orunconsciously ,inthisthesis.
2.3.3IBiS1Datatypes
Asapreliminary tothepresentationofthesemanticsandupdatestrategies usedbyIBiS1,
wewilllistthesystem-sp eci¯ctypesusedbythesystem.
²Typesrelatedtosemantics
{Question
¤WHQ
¤YNQ
¤ALTQ
{Proposition
{ShortAns
{Ind
²Typesrelatedtoplansandactions
{Action
{PlanConstr
²Miscellaneous types
{Participan t
{ProgramState
Thetypesrelatedtosemanticsareexplained inSection2.4.Typesrelatedtoplansand
actionsareexplained inSection2.6.The¯naltwotypesarede¯nedin(2.3)(seeSection
A.2.1foranexplanation ofthetypede¯nition formatusedbyTrindiKit ).

24 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
(2.3)a.type:Participan t
objects:(
Usr
Sys
b.type:ProgramState
objects:(
Run
Quit
Thesetwotypesareonlyde¯nedextensionally ,i.e.norelations, functions, oroperations
arede¯nedforthem.InIBiS,theDPs(userandsystem)arerepresentedasobjectsoftype
Participan t.AnobjectoftypeProgramState intheTISdetermines whether thesystem
shouldhaltornot,asexplained inSection2.3.1.
2.4SemanticsinIBiS1
Forourbasicsystem,weuseaverysimplerepresentationofpropositionsbasedonpredicate
logicwithoutquanti¯cation. Weextendthiswithlambda-abstraction ofpropositionsand
aquestion operator\?"whichcanbethoughtofasafunction froma(possiblylambda-
abstracted) propositiontoaquestion. Wealsointroduceasemanticcategory toaccount
forthecontentofshortanswers(e.g.\yes"or\Paris").
Fortherepresentationofquestions weusepropositionspreceded byquestion marks(for
y/n-questions), lambdaabstracts ofpropositionswiththelambdareplaced byaquestion
mark(forwh-questions) andsetsofy/n-questions (foralternativ equestions).
2.4.1Formalsemanticrepresentations
HerewedescribethesyntaxoftheformalsemanticrepresentationusedinIBiS1.This
description de¯nesasetofcontenttypeswhichareexplained andexempli¯ed below.The
symbol\:"representstheof-typerelation, i.e.Expr:TypemeansthatExprisoftype
Type.
Atomtypes
Pred n,wheren=0orn=1:n-placepredicates, e.g.dest-city,month
Ind:Individual constants,e.g.paris,april
Var:Variables, e.g.x;y;:::;Q;P;:::

2.4.SEMANTICS INIBIS1 25
Sentences
Expr:Sentencei®Expr:PropositionorExpr:Question orExpr:ShortAns
Expr:Propositionif
²Expr:Pred 0or
²Expr=pred1(arg),wherearg:Indandpred1:Pred 1or
²Expr=:P,whereP:Propositionor
²Expr=fail(q),whereq:Question
Expr:Question ifExpr:YNQorExpr:WHQorExpr:ALTQ
?P:YNQifP:Proposition
?x:pred1(x):WHQifx:Varandpred1:Pred 1
fynq1;:::;ynqng:ALTQifynqi:YNQforallisuchthat1·i·n
Expr:ShortAns if
²Expr=yesor
²Expr=noor
²Expr:Indor
²Expr=:argwherearg:Ind
2.4.2Propositions
Propositionsarerepresentedbybasicformulaeofpredicate logicconsisting ofann-ary
predicate together withconstantsrepresentingitsargumen ts,e.g.loves(john,mary) .
Inadialogue systemoperatinginadomainoflimitedsize,itisoftennotnecessary to
keepafullsemanticrepresentationofutterances. Forexample, auserutterance of\I

26 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
wanttogotoParis"couldnormally berepresentedsemanticallyase.g.want(user,go-
to(user,paris))orwant(u,go-to(u,p)) &city(p)&name(p,paris)&user(u).
Wewillbeusingareducedsemanticrepresentationwithacoarser, domain-dep endent
levelofgranularity;forexample, theaboveexample willberendered asdest-city(paris) .
Thisreduced representationisinpartaconsequence oftheuseofkeyword-spottingin
interpreting utterances, butcanarguably alsoberegarded asare°ection ofthelevelof
semanticgranularityinherentintheunderlying domaintask.Asanexample ofthelatter,
inatravelagencydomainthereisnopointinrepresentingthefactthatitistheuser(or
customer) ratherthanthesystem(orclerk)whoisgoingtoParis;itisimplicitly assumed
thatthisisalwaysthecase.
Asaconsequence ofusingreduced semantics,itwillbeusefultoallow0-arypredicates,
e.g.return,meaning \theuserwantsareturnticket".0-arypredicates canofcourse
appearinnon-reduced semanticsaswell,e.g.intherepresentationof\It'sraining" ina
non-temp orallogicase.g.rain.(Ofcourse,non-temp orallogiccanalsobearguedtobe
akindofreducedsemanticrepresentation.)
Theadvantageofthissemanticrepresentationisthatthespeci¯cation ofdomain-sp eci¯c
semanticsbecomessimpler, andthatunnecessary \semanticclutter" isavoided.Onthe
otherhand,itseverelyrestricts thepossibilityofprovidinggenericsemanticanalyses that
canbeextended tootherdomains.
Ifthedatabase searchforananswertoaquestion qfailstheresulting propositionisfail(q).
Wehavechosenthisrepresentationbecauseitprovidesaconcisewayofencodingafailure
to¯ndananswertoqinthedatabase.
2.4.3Questions
Threetypesofquestions arehandledbyIBiS:y/n-questions, wh-questions, andalternativ e
questions. Herewedescribehowthesearerepresentedonasemanticlevel;thesyntactic
realization isde¯nedinthelexicon.
²y/n-questions arepropositionspreceded byaquestion mark,e.g.?dest-city(london)
(\DoyouwanttogotoLondon?")
²wh-questions arelambda-abstracts ofpropositions, withthelambdareplaced bya
question mark,e.g.?x.dest-city(x)(\Where doyouwanttogo?")
²alternativ equestions aresetsofy/n-questions, e.g.f?dest-city(london), ?dest-
city(paris) g(\DoyouwanttogotoLondonordoyouwanttogotoParis?")

2.4.SEMANTICS INIBIS1 27
2.4.4Shortanswers
Ginzburg usestheterm\shortanswers"forphrasalutterances indialogue suchas\paris"in
thedialogue aboveinSection2.1.1.Thesearestandardly referredtoasellipticalutterances.
Ginzburg arguesthat(syntactic)ellipsis,asitappearsinshortanswers,isbestviewedasa
semanticphenomenon withcertainsyntacticpresuppositions. Thatis,thesyntaxprovides
conditions onwhatcountsasashortanswerbuttheprocessingofshortanswersisanissue
forsemantics.
InIBiS,theinterpretation moduleisasimplekeyphrase spotterwhichdoesnotprovidea
syntacticanalysis oftheinput.Wearguethatthisissu±cientformanydialogue system
applications. Because ofthis,wealsothrowoutthesyntacticpresuppositionwhendealing
withshortanswers;weseethemonlyfromthesemanticpointofview.Whatthismeans,
ine®ect,isthatwearenotinterestedinellipsis,butratherinsemanticunderspeci¯cation.
Furthermore, thesemanticsusedbythesystemisdomain-dep endentandthuswhatweare
reallyinterested inissemanticunderspeci¯cation withregardtothedomain/activity .
Onthisaccount,anutterance issemanticallyunderspeci¯edi®itdoesnotdetermine a
uniqueandcomplete propositioninthegivenactivity.Ofcourse,thismeansthatwhether
anutterance isregarded asunderspeci¯edornotdependsonthe¯ne-grainedness ofpropo-
sitionalcontent,andwhattypesofentitiesareinteresting inacertainactivity.Forex-
ample,giventhetypeofsimplesemanticsthatweproposeforthetravelagencydomain,
\toparis"isnotsemanticallyelliptical, sinceitdetermines thecomplete propositiondest-
city(paris) .However,\toParis"wouldbesemanticallyunderspeci¯edinanactivity
whereitcouldalsobetakentomeane.g.\YoushouldgotoParis".
InIBiS,resolution ofunderspeci¯edcontentwillbehandled simultaneously withintegra-
tionofthecontentintotheinformation state.Thereasonfordoingthiswillbecomeclear
inChapter 4.(Roughly ,themotivationisthatellipsisresolution mayrequiremodi¯cation
oftheDGB,possiblyinvolvingclari¯cation questions, andisthustoberegarded asan
issueofdialogue managemen t.)
Ingeneral,semanticobjectsoftypeShortAns canbeseenasunderspeci¯edpropositions.
InIBiS1,weonlydealwithindividual constants(i.e.membersofInd),andanswersto
y/n-questions, i.e.yesandno.Individual constantscanbecombinedwithwh-questions
toformpropositions, andyesandnocanbecombinedwithy/n-questions.
Notethatweallowexpressions oftheform:argwherearg:Indasshortanswers.This
isusedforrepresentingthesemanticsofphraseslike\nottoParis".Inamoredeveloped
semanticrepresentationtheseexpressions couldbereplaced byatype-raisedexpression,
e.g.¸P::P(arg).

28 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
2.4.5Semanticsortalrestrictions
IBiSusesarudimentarysystemofdomain-dep endentsemanticsortalcategories. For
example, thetravelagencydomainincludes thesortscity,meansoftransport,class,
etc.AllmembersofIndareassigned asort;forexample, theindividual constantparis
hassortcityand°ighthassortmeansoftransport.
Sortsmakeitpossibletodistinguish non-meaningful propositionsfrommeaningful ones.
However,whatismeaningful inoneactivitymaynotbemeaningful inanother, andvice
versa.Therefore, thesortalsystemisimplemen tedasapartofthedomainknowledge.In
IBiS1,thesortsaremainlyusedfordetermining whether ananswerisrelevantto(about,
inGinzburg's terminology) acertainquestion (seeSection2.4.6).
Thepropertyofaproposition Pbeingsortallycorrectisimplemen tedinIBiS1assort-
restr(P).Apropositionissortallycorrectifitsargumen tful¯lthesortalconstrain tsof
thepredicate. Forexample, thepropositiondestcity(X)issortallycorrectifthesort
ofXiscity.Sortalconstrain tsofpredicates areimplemen tedinthedomainresource, as
exempli¯ed in(2.4).
(2.4)sortrestr(destcity(X))Ãsemsort(X,city).
2.4.6Relations betweenquestions andanswers
Ginzburg de¯nestworelations betweenquestions andanswersthatareusedindialogue
managemen tprotocols:resolvesandabout.InthissectionwewillreviewGinzburg's
de¯nitions oftheserelations andadaptthemforuseinIBiS1.
Theresolvesrelation
Ginzburg's notionofresolvednessisintendedascapturing
anagentrelativeviewofwhen[a]question hasbeendiscussed su±cientlyfor
currentpurposestobeconsidered \closed" (Ginzburg (1996),p.417)
Unfortunately ,thetechnicalde¯nition ofresolvesisrathercomplicated andwouldrequire
anot-so-brief excursion intosituation semantics.Instead, wewillmakedowithaless
technicalde¯nition.

2.4.SEMANTICS INIBIS1 29
Whatthede¯nition says,roughly,isthatanansweraresolvesaquestion qrelativetoan
agentincasea(1)providesinformation thatpositivelyornegativelyresolvesq,and(2)
ful¯lstheagent's(private)goalrelatedtothatquestion, relativetotheagent'sinferential
capabilities.
Condition (1)isasemanticcondition whichisnotrelatedtotheagent.Ifqisay/n-
question ?p,apositivelyresolvesqifaentailsp,andanegativelyresolvesqifaentails
:p.Ifqisawh-question ?x:p(x),apositivelyresolvesqifaentailsthattheextension of
¸x:p(x)isnon-empt y,andanegativelyresolvesqifaentailsthattheextension of¸x:p(x)
isempty.
Wewillnotmakeanydistinction betweenresolvednessingeneralandagent-related re-
solvedness. Webelievethatthedistinction onlybecomesrelevantifseveralDPswith
di®erentnotionsofgoal-ful¯lmen tarebeingmodelled.SinceIBiShasnousermodel
(apartfromwhatisassumed tobesharedinformation), thesystemassumes theuserand
thesystemhavethesamede¯nition ofresolvedness,andfurthermore thatthisde¯nition
isshared. Another wayofseeingthisisthatweuseamodi¯edversionofcondition (1)
andassumeitdetermines resolvednessandgoal-ful¯lmen twithrespecttoquestions forall
DPs.
However,ourconceptofresolvedness(asindeedallrelations betweenquestions andanswers
inIBiS)isdomain-dep endentinvirtueofincluding constrain tsonsortalcorrectness with
respecttothedomain.
BasedonGinzburg's de¯nition, wede¯netherelationthatananswerresolvesaquestion
usingtherelationresolves(A,Q),whereQisaQuestion andAisaPropositionorShort-
Ans.Thisrelationisdomain-dep endent,andformallyresolvesisarelationonthedomain
datatype.Table2.1showswhatcountsasresolving aquestion ofagiventype4.
Question Resolving answers
?x:pred1(x) aandpred1(a)
?P yes,no,P,and:P
f?P1,?P2,:::,?PngPi,1·i·n
Table2.1:Resolving answerstoquestions
Forexample, thecontentofaresolving answertoawh-question?x:dest-city(x)about
destination cityiseitherapropositionoftheformdest-city(C)oranunderspeci¯ed
propositional contentC,whereChastheconceptual category ofcity(seeSection2.10.1).
Forexample, ifparisisde¯nedtobeacityconcept, bothdest-city(paris) (e.g.\My
4Notethatthede¯nition ofresolvednessisindependentoftruth.Thatis,aquestion canberesolved
byafalseanswer.Ofcourse,ifaDPknowsthatananswerisfalsesheisnotlikelytoaccepttheanswer,
butthatisadi®erentmatter.

30 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
destination isParis")andparis(\Paris")resolve?x:dest-city(x).
Thepropositionfail(q)canbeparaphrased roughlyas\thedatabase containsnoanswer
toq,giventhecurrentsetofsharedcommitmen ts".Sinceitisimplicitly dependenton
asetofpropositions,fail(q)doesnotreallyrepresentade¯nitefailureto¯ndananswer
toq,onlyafailuregiventhecurrentsharedcommitmen ts.Therefore, wedonotregard
fail(q)asnegativelyresolving q.WediscussthisandrelatedmattersfurtherinSection
2.12.4.
Aboutnessandrelevance
According toGinzburg,
aboutisarelationthat,intuitively,captures therangeofinformation associated
withaquestion independentlyoffactualityorlevelofdetail.(Ginzburg, 1994,
p.7)
Aswithresolvedness,wewillnotgointothetechnicalde¯nition ofaboutness. Also,many
oftheintricacies ofthede¯nition arenotneededforthesimplekindofsemanticsweare
interested in.However,wedoneedarelationlikeaboutnessfordetermining whether the
contentofananswer-moveshouldberegarded asrelevanttoacertainquestion. Tore°ect
thatweareusingaslightlydi®erentconceptthanGinzburg, wewillusethetermrelevant
insteadofabout5.
Tobeginwith,allresolving answersarerelevant;thisisre°ected inthede¯nition in(2.5).
(2.5)relevant(A,Q)ifresolves(A,Q),whereA:PropositionorA:
ShortAns, andQ:Question
Inaddition, negated answerstowh-andalt-questions arerelevantbutnotresolving, as
showninTable2.2.
2.4.7CombiningQuestions andAnswerstoformPropositions
Questions andanswerscanbecombinedtoformpropositions. Thespecialcaseforwh-
questions issimilartofunctional application, aswhenthequestion?x.dest-city(x)
5Ofcourse,theconceptofrelevanceisnotwithoutitsproblems either.Insteadofgettingintoadebate
ofwhatrelevance\reallyis",wewillsimplystipulate whatitmeansinIBiS.

2.4.SEMANTICS INIBIS1 31
Question Relevant,non-resolving answers
?x:pred1(x):a,:pred1(a)
f?P1,?P2,:::,?Png:Pi,1·i·n
Q fail(Q)
Table2.2:Relevantbutnotresolving answerstoquestions
iscombinedwithparistoformdest-city(paris) .Questions canalsobecombinedwith
propositions, yieldingthesamepropositionsasresultprovidedthequestion andthepropo-
sitionshavethesamepredicate andthatthepropositionissortallycorrect.Itisalsopossi-
bletocombiney/n-questions andalternativ equestions withanswerstoformpropositions.
Ingeneral, wesaythataquestion qandanansweracombinetoformaproposition p.
Therelationbetweenquestions, answersandpropositionsde¯nedbythecombine-relation
isshowninTable2.3
Question Answer Proposition
?x:pred1(x) aorpred1(a)pred1(a)
:aor:pred1(a):pred1(a)
?P yesorP P
noor:P:P
f?P1;?P2;:::;?PngPi,(1·i·n)Pi
:Pi,(1·i·n):Pi
Table2.3:Combiningquestions andanswersintopropositions

32 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
2.5DialoguemovesinIBiS1
Intheinformation stateapproach,theprecisesemanticsofadialogue movetypeisde-
termined bytheupdateruleswhichareusedtointegratemovesofthattypeintothe
information state.Thismeansthatalloccurrences ofamovetypeareintegrated bythe
samesetofrules.
Whiledialogue movetypesareoftende¯nedintermsofsentencemood,speakerintentions,
and/ordiscourse relations (seee.g.CoreandAllen(1997),weoptforadi®erentsolution.
Inourapproach,thetypeofmoverealizedbyanutterance isdetermined bytherelation
betweenthecontentoftheutterance, andtheactivityinwhichtheutterance occurs.
Thefollowingdialogue movesareusedinIBiS1:
²ask(q),whereq:Question
²answer(a),wherea:ShortAns ora:Proposition
²greet
²quit
Ininquiry-orien teddialogue, thecentraldialogue movesconcern raisingandaddressing
issues.Thisisdonebytheaskandanswermoves,respectively.Thegreetandquitmoves
areusedinthebeginning andendofdialogues togreettheuserandindicate thatthe
dialogue isover,respectively.
Inourapproach,anutterance isclassi¯ed asrealizing ananswer-moveonlyifitscontent,
orpartofthecontent,istakentobearelevantanswertosomequestion availableinthe
domain. Similarly ,anutterance isclassi¯ed asrealizing anaskmoveonlyifitscontentis
takentobesomequestion availableinthedomain. Theavailablequestions areencoded
indialogue plansinthedomainknowledgeresource, eitherasissuestoberesolvedbya
planorasissuestoberaisedorresolvedaspartofaplan.Themapping fromutterances
tomoves(movetypepluscontent)isspeci¯edinthelexiconresource.
Onthisapproach,moveclassi¯cation doesnotrelyonthedialogue context,nor(exceptto
averysmallextent)onsyntacticform.Whether utterance uisinterpreted asanswer(A)is
independentofwhether acorrespondingquestion hasbeenraised.Itisalsoindependent
ofwhether uisadeclarativ e,interrogativ e,orimperativesentence,orasentencefragment.
Forexample, \IwanttogotoParis",\CanIgotoParis?",\GetmetoParis!"and\to
Paris"areallinterpreted asanswer(dest-city(paris)).Similarly ,\What's theprice?",

2.6.REPRESENTING DIALOGUE PLANS INIBIS1 33
\Givemepriceinformation!", \Iwanttoknowaboutprice.",\Iwantpriceinformation."
and\priceinformation" areallinterpreted askask(?x.price(x)).Foradescription ofhow
thisinterpretation works,seeSectionA.7.3.
Ofcourse,partofthereasonthatthisapproachworksisthatweareoperatinginsimpledo-
mainsandactivities whichcanbefairlywellcoveredbyakeyword-spottinginterpretation
module.However,theapproachcouldwellbeimprovedbyaddingamorecomplex kindof
grammar (e.g.HPSG), thusenabling thesystemtotakesyntacticfeatures ofutterances
intoaccount,whilestillusinganactivity-basedclassi¯cation. Whether activity-dependent
classi¯cation ofmovesisaviablealternativ etointention-andstructure-based classi¯cation
ingeneralisanissuewewillreturntoinChapter 6.Onehypothesisworthexploring isto
whatextenttraditional speechactscanbereplaced byacombination ofactivity-related
dialogue moves(toupdateISanddecideonfuturemoves)andsyntacticsentencemodes
(todecideonthesurfaceformoffuturemoves).
2.6RepresentingdialogueplansinIBiS1
Inthissectionweintroducetheconceptofdialogue plans,andshowhowthesearerep-
resentedinIBiS1.Inlaterchapters, theplanformalism willbeextended tohandlemore
powerfulconstructions.
2.6.1Domain plansanddialogue plans
Inourimplemen tation,thedomainknowledgeresource contains,amongotherthings,aset
ofdialogueplanswhichcontaininformation aboutwhatthesystemshoulddoinorderto
achieveitsgoals.
Inplan-based dialogue managemen t(e.g.AllenandPerrault,1980),ithasbeenassumed
thatgeneralplanners andplanrecognizers shouldbeusedtoproducecooperativebehaviour
fromdialogue systems. Onthisaccount,thesystemisassumed tohaveaccesstoalibrary
ofdomainplans,andbyrecognizing thedomainplanoftheuser,thesystemcanproduce
cooperativebehavioursuchassupplying information whichtheusermightneedtoexecute
herplan.Onthisapproach,plansforcarrying outdialogues arenotrepresentedexplicitly;
instead, thesystemiscontinuallyinspecting(andperhapsmodifying) domainplansto
determine whatdialogue movesneedtobeperformed.
Ourapproachisinsteadtodirectlyrepresentready-made plansforengaging incoopera-
tivedialogue andproducingcooperativebehaviour(suchasansweringquestions) which

34 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
indirectly re°ectdomainknowledge,butobviatestheneedfordynamic planconstruction.
Inthischaptertheplanswillbeusedtoproducefairlysimpleandmostlysystem-driv en
dialogue, butinChapter 4,wewillseehowready-made dialogue planscanbeusedina
°exiblewaytoenablemixedinitiativedialogue.
Ofcourse,thisdoesnotmeanthatgeneralreasoning capabilities forplanning andplan
recognition areneverneededindialogue systems; incomplex domains ready-made dialogue
plansaremostlikelytobeinsu±cien t.Infact,inChapter 5,we'llexplorethegeneration
ofdialogue plansfromdomainplans(whichcouldthemselv esbedynamically generated).
Buttherearealsootherpossiblesourcesfordialogue plans,andinthesecasesthedomain
plansmaynotbeneededtobeabletocarryoutusefuldialogues. Forexample, dialogue
plansmaybeconstructed bylookingatacorpusofrecorded human-humandialogues (as
doneinthischapter)orbyapplying aconversionschematomenu-baseddeviceinterfaces
(asdoneinSection5.4).
2.6.2Asyntaxforproceduralplans
Inthissection,weintroduceasimpleformalism forrepresentingproceduralplansasse-
quencesofactions. Theplanrepresentationsyntaxwillbeextended withadditional plan
constructs inlaterchapterstohandlemorecomplex plans,including branchingconditions
andsubplans.
Planconstructs
Theplanconstructs (oftypePlanConstr) inIBiS1areeithersimpleactionsoraction
sequences. Actionsequences havetheformha1;:::;aniwhereai:Action(1·i·n).
Actions
Alldialogue movesareactions. Therearealsomoreabstract actionswhichhoweverare
connected todialogue moves.Finally,thereareactionswhicharenotconnected tospeci¯c
dialogue moves.
Inthefollowing,qisaquestion, andpisaproposition.

2.7.TOTALINFORMA TION STATEINIBIS1 35
Actionsconnected todialoguemovesInIBiS1,therearethreeactiontypesclosely
relatedtodialogue movetypes.
²¯ndout( q):¯ndtheanswertoq.InIBiS1,thisisdonebyaskingaquestion tothe
user,i.e.byperforming anaskmove.Thepropositionresulting fromansweringthe
question isstoredin/shared/com .The¯ndoutactionisnotremoveduntilthe
question hasbeenanswered.
²raise(q):raisethequestion q.Thisactionissimilarto¯ndout,exceptthatitis
removedfromtheplanassoonastheask-moveisselected. Thismeansthatifthe
userdoesnotanswerthequestion whenithasbeenraised,itwillnotberaisedagain.
²respond(q):provideananswertoquestion q.Thisisdonebyperforming ananswer
movewithcontentp,andrequires thatthereisaresolving answerptoqinthe
/private/bel ¯eld.
Database consultation Thedatabase consultation actionisnotconnected toanyspe-
ci¯cdialogue move.Database consultation canbeseenasaspecialcaseofdomainactions.
Thedomainactionsaredetermined bytheapplication. Thesetofavailabledomainac-
tionsarede¯nedasrelations orupdatesintheresource interfacefortheapplication. Fora
typicalinformation-exc hangetask,theapplication isastaticdatabase. Notethat\static"
heredoesnotmeanthatthedatabase cannotbeupdated.Itonlymeansthatitisnot
updatedbythedialogue system.
Forourdatabase application inthetravelagencydomain, weuseasingledomainaction
consultDB( q)(where qisaquestion) whichwilltriggeradatabase searchwhichtakesall
thepropositionsin/shared/com andgiventhislooksuptheanswertoqinthedatabase.
Theresulting propositionisstoredin/private/bel.
2.7TotalInformation StateinIBiS1
TheTotalInformation State(TIS)inIBiS1isdividedintothreeparts:theInformation
State(IS),theresource interfacevariables, andthemoduleinterfacevariables. Inthis
sectionwewilldescribethesecomponents,comparing ittoGinzburg's DGB.

36 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
2.7.1Information stateinIBiS1
IBiS1information stateproper
TheInformation State(IS)isthemaincomponentoftheTotalInformation State(TIS).
Thetypeofinformation stateusedbyIBiS1(andextended laterinordertohandleother
dialogue types)canbeseenasavariantofGinzburg's DGB(whichrepresents,essen-
tially,sharedinformation) incombination witharepresentationofprivateattitudes which
addsdetailtoGinzburg's unpublicized mentalstate(seeSection2.2.3)byusingconcepts
in°uenced bytheBelief-Desire-In tentionmodel(seeSection2.2.1).
InrelationtoGinzburg's theory,inordertobuildasystemweneedtosaymoreabout
theUNPUB-MS andhowitisstructured. Inourinitialsystem,wehavearecordofinfor-
mationprivatetothesystemwhichcontainsanagendaofthingstodointhenearfuture
(/private/agenda),adialogue planformorelong-term actions(/private/plan ),anda
setofbeliefs(/private/bel).Thereisalsoarecordrepresentingsharedinformation con-
tainingasetofmutuallyagreed-up onpropositions, astackofquestions underdiscussion,
andinformation aboutthelatestutterance.
2
666666666664private:2
64agenda:Stack(Action)
plan :Stack(Action)
bel :Set(Prop)3
75
shared :2
6664com:Set(Prop)
qud:Stack(Question)
lu:"
speaker :Participan t
move:Move#3
77753
777777777775
Figure2.2:IBiS1Information Statetype
Itshouldbenotedthattheshared structure isessentiallypropositional innature,and
canthusbeviewedasasetofpropositionswhichaDPholdstobetrue.Forexample,
thefactthataquestion qistopmost onQUDcouldinprinciple berepresentedbya
propositionqud-maximal( q),andpushing andpoppingcouldbemodelledbyasserting
andretracting propositionsofthiskind.However,givingstructure totheinformation state
makesdialogue processingbothmoretransparen tandmoree±cient.
OnGinzburg's accountDPsdonotalwaysassumethattheDGBisshared. Webelieve
thismakesthetheoryunintuitiveandhardertounderstand. Wemakethisexplicitby
replacing thelabel\DGB"by\SHARED".
Ginzburg doesnotsaymuchaboutwhatUNPUB-MS containsorhowitisstructured, but
theagendaandplanprovideuswithawayofelaboratingonthispartofthetheory.

2.7.TOTALINFORMA TION STATEINIBIS1 37
The¯eld/private/agendaisoftypeStack(Action). Ingeneral,wetrytousedatastruc-
tureswhichareassimpleaspossible;astackisthesimplest orderedstructure soitisused
asadefaultdatastructure whereorderisneededaslongasitissu±cientforthepurposes
athand.Theagendaisreadbytheselection rulestodetermine thenextdialogue moveto
beperformed bythesystem.
The/private/plan isastackofplanconstructs. Someoftheupdaterulesformanaging
theplanhavetheformofrewriteruleswhichprocesscomplex planconstructs untilsome
actionistopmost ontheplan.Otherrulesexecutethisactionincaseitisasystemaction
ormoveittotheagendaincaseitisamove-related action.
InIBiS1,the¯eld/private/bel,asetofpropositions, isusedtostoretheresultsof
database searches.Ofcourse,thedatabase (andthedomainknowledge,andthelexicon)
canbeseenasapartofthesystem's privatebeliefset,butin/private/belwechooseto
representonlypropositionswhicharedirectlyrelevanttothetaskathandandwhichare
theresultofdatabase searches.Thisissimilartoseeingthedatabase asasetofimplicit
beliefs,anddatabase consultation asaninference processwhereimplicitbeliefsaremade
explicit. Thereasonforusingasetisthatasetisthesimplest unordered datastructure.
Questions UnderDiscussion arestoredin/shared/qud ,modelledasastackofquestions.
FollowingGinzburg, wede¯neQUDascontainingquestions whichhavebeenraisedbut
notyetresolved,andthuscurrentlyunderdiscussion. Thequestion topmost onQUDmay
beresolvedbyasemanticallyunderspeci¯edshortanswer.Notethatwehaveusedastack
ratherthane.g.apartialordering forthisinitialsystem;thisissu±cientforthesimple
kindsofdialogues thatIBiS1handles.
The¯eld/shared/com containsthesetofpropositionsthattheuserandthesystem
havemutuallyagreedtoduringthedialogue. Theyneednotactually bebelievedbyeither
participan t;theimportantthingisthattheDPshavecommitted tothesepropositions,
evenifonlyforthepurposesoftheconversation.
Tore°ectthatthecontentsneednotbetrue,orevenprivatelybelievedbytheDPS,and
becausewearenotusingsituation semantics(wherethereisadistinction betweenfactsand
propositions) weusethelabel\commitmen ts"or\committed propositions", abbreviated
ascom,insteadofFACTS.These,then,arepropositionstowhichtheDPsare(takento
be)jointlycommitted.
In/shared/lu werepresentinformation aboutthelatestutterance: thespeaker,andthe
moverealizedbytheutterance. Weassumeforthemomentthateachutterance canrealize
onlyonemove.Thisassumption willberemovedinthenextchapter.

38 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
2.7.2Initializing theinformation state
Thefollowinginitialization algorithm isperformed byIBiS1onstartup.
(2.6)set(program state,run)
set(lexicon ,lexicon-Domain-Lang)
set(database,database- Domain)
set(domain,domain- Domain)
push(/private/agenda,greet)
Here,Langisthevalueofthelanguage °ag,andDomainisthevalueofthedomain°ag.
Thisalgorithm setstheresource interfacevariabletothevaluesdetermined bythelanguage
anddomain°ags,therebyhookinguptheappropriate resources totheTIS.
Finally,anactiontoperformagreetmoveisplacedontheagenda.
2.7.3Resource interfaces
Therearethreeresources inIBiS:alexicon, adatabase andadomainresource. Each
resource isconnected totheTISviaadomaininterfacevariable.
²lexicon:Lexicon
²domain:Domain
²database:Database
TheTrindiKit de¯nitions ofresource interfaces seesthemasabstract datatypes,i.e.
speci¯edusingrelations, functions, andoperations. Allresources inIBiS1arestatic,
whichmeansthattherearenooperations availableforobjectsofthesetypes.Theformal
de¯nitions oftheresource interfacesisshownin(2.7)(where q:Question, A:ShortAns
orA:Prop,P:Prop,M:Move,PropSet:Set(Prop), Plan:StackSet(Action), and
Phraseisalistofwords.)

2.7.TOTALINFORMA TION STATEINIBIS1 39
(2.7)a.type:Domain
rel:8
>>><
>>>:relevant(A,Q)
resolves(A,Q)
combine(Q,A,P)
plan(Q,Plan)
b.type:Lexicon
rel:8
><
>:inputform(Phrase;M)
outputform(Phrase;M)
ynanswer(A)
c.type:Database
rel:n
consultDB( PropSet;Q;P)
Thedomainconditions \resolves",\relevant"and\combine"implemen ttheresolves,rel-
evantandcombine relations describedinSection2.4andde¯nedinTables2.1,2.2and
2.3,respectively.Thelexiconconditions arethoserequired bytheinterpretation andgen-
erationmodulessupplied withTrindiKit anddescribeddescribedinSectionA.7.The
database consultation condition isdescribedinSection2.6.
2.7.4Moduleinterfacevariables
The¯nalcomponentoftheTISisasetofmoduleinterfaceVariables. InIBiS,thereare
sixmoduleinterfacevariableshandling theinteraction betweenmodules:
TheIBiSmoduleinterfacevariableshavethefollowingtypes:
²input:String
²latestspeaker:Participan t
²latestmoves:Set(Move)
²nextmoves:Set(Move)
²output:String
²program state:ProgramState
Thefunction ofeachofthesevariablesisindicated below:

40 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
²input:Storesastringrepresentingthelatestuserutterance. Itiswrittentobythe
InputmoduleandreadbytheInterpretation module
²latest-speaker :Thespeakerofthelatestutterance; readandwrittenastheinput
variable,butalsowrittentobytheOutputmodule(whenthesystemmadethelast
utterance).
²latest-mo ves:Arepresentationofthemovesperformed inthelatestutterance, as
interpreted bytheInterpretmodule.
²next-mo ves:Thenextsystemmovestobeperformed, andtheinputtotheGenerate
module
²output:Astringrepresentingthesystemutterance, asgenerated bytheGenerate
module
²program-st ate:Whether IBiSshouldquit;either\run"or\quit".Readbythe
Controlmodule.
Notethatallvariablesareaccessible fromtheDMEmodules(i.e.UpdateandSelect).
2.8IBiS1updatemodule
InthissectionwereviewtheupdaterulesusedbyIBiS1,startingwithruleshandling the
basicrulesfordealingwithaskandanswermoves.TheserulesarebasedonGinzburg's
protocolsforraisingandresolving issuesindialogue. Wealsogivesomesimplerulesfor
handling greetandquitmoves.Wethenproceedtorulesforhandling plansandactions.
2.8.1Updateruleforgettingthelatestutterance
IBiS1assumes perfectcommunication, inthesensethatallsystemutterances arecor-
rectlyundersto odbytheuser,andallinterpretations ofuserutterances producedbythe
interpret modulearecorrect.
Theseassumptions areimplemen tedin(rule2.1).

2.8.IBIS1UPDATEMODULE 41
(rule2.1)rule:getLatestMo ve
class:grounding
pre:(
$latestmoves=Moves
$latestspeaker =DP
eff:(
/shared/lu/moves:=Moves
/shared/lu/speaker :=DP
Thisrulecopiestheinformation aboutthelatestutterance fromthelatestmovesand
latestspeaker tothe/shared/lu ¯eld.The¯rstcondition picksoutthe(singleton)
setofmovesstoredbytheinterpretation module,andthesecondcondition getsthevalue
ofthelatestspeaker variable. Theupdatessetthevaluesofthetwosub¯elds ofthe
/shared/lu recordcorrespondingly.
2.8.2Raisingissues:theaskmove
BeforeweexplaintherulesusedbyIBiS1fordealingwiththeaskmove,wewillreview
Ginzburg's protocolsforquerying andassertion onwhichtherulesarebased.Wewillalso
argueforsomemodi¯cations ofGinzburg's protocols,mostofwhicharemotivatedbythe
factthatwearedealingwithasimpledialogue systemratherthanahumanDP.However,
somemodi¯cations haveamoregeneralmotivation.Forinstance, whereas Ginzburg's
protocolsoftendescribetheupdatesfortheaddressee DP,adialogue systemusuallyneeds
toaccountfortwocases:onewherethesystemhasperformed amoveofacertaintype,
andonewheretheuserhasperformed thesametypeofmove.Forsomemovetypes,one
rulecanbedevisedwhichcoversbothcases,whileinothercasestwoseparate rulesare
required.
Ginzburg's Cooperativequeryingprotocol
1.Aposesq
²A'slatest-mo ve:AASKq
2.Brealizesaquerywasposedandacceptsthequestion:
²B'slatest-mo ve:AASKq
²qbecomesmaximal inB'sQUD
3.Bprovidesaresponseuthataddresses q

42 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
ThisprotocolaccountsfortheupdatesofDPBwhenDPAhasposedaquestion; thisis
thepartoftheprotocolwewilluseasabasisforintegrating askmoves.Theprotocolalso
restricts B'sresponse;thispartoftheprotocolisdealtwithinSection2.8.2below.
Question dependence,speci¯city,andrelevance
BeforewepresentGinzburg's protocolsweneedtointroducetworelevantrelations involv-
ingquestions de¯nedbyGinzburg: dependencebetweenquestions, andquestion-sp eci¯city
ofutterances. Wealsoindicate howtheserelations havebeenimplemen tedinIBiS.
Ginzburg's de¯nition oftheDEPENDS-ON relationformally asin(2.8)(Ginzburg (1994)).
(2.8)q1DEPENDS-ON q2i®q1isresolvedbyafact¿onlyifq2is
alsoresolvedby¿
Thisisintendedtocapturetherelationthattheresolution ofq2isanecessary condition for
theresolution ofq1.Webelieveitisusefultorelaxthede¯nition ofquestion dependence;
speci¯cally,wewanttorelatedependence todomainplans.Wetherefore proposethe
partialde¯nition ofquestion dependence in(2.9).
(2.9)q1dependsonq2ifresolving q2isastepinaplanforresolving
q1
InIBiS,dependence isimplemen tedasarelationonthedomainasshownin(2.10).
(2.10)depends(Domain,Q1,Q2)ÃDomainincludes aplanPfor
dealingwithQ1and¯ndout( Q)2Plan.
Inaddition, domain-sp eci¯cdependencies whichdonot¯tthede¯nition in(2.10)between
questions canbeencodeddirectlyinthedomainresource, e.g.asin(2.11).
(2.11)depends(?x.dest-city(x),?needvisa)
Thisstatesthattheissueofdestination citydependsonwhether avisaisneeded6.
Theconverserelationofdependsisin°uences ,asde¯nedin(2.12).
(2.12)in°uences (Domain,Q1,Q2)i®depends(Domain,Q2,Q1)
6Giventhede¯nition of\irrelevantfollowups"inSection3.6.8),addingthisdependency willresultin
thesystemregarding \DoIneedavisa?"isarelevantfollowupto\Wheredoyouwanttotravel?".

2.8.IBIS1UPDATEMODULE 43
Ginzburg's cooperativequerying protocolincludes thereaction oftheaddressee: \Bpro-
videsaresponseuthataddresses q".According toGinzburg's de¯nition, anutterance u
addresses qi®either(a)thecontentofuisaproposition pandpisaboutq,or(b)the
contentofuisaquestion q1andq1in°uences q.
Giventhenotionofquestion dependence, Ginzburg alsode¯nesarelation \question-
speci¯c"betweenquestions andutterances, shownin(2.13).
(2.13)Givenaquestion q,aq-speci¯cutterance isonethateither
1.Conveysinformation ABOUT qor
2.Conveysaquestion onwhichqdepends
Wehavenotimplemen tedthisrelationdirectlyinIBiS,howeverbothrelevance(ourversion
of'ABOUT') anddependence arede¯ned.
Integrating askmoves
Thebasicruleexpressed bytheintegration ruleforaskmovesisshownin(2.14).
(2.14)Tointegrateanaskmovewithcontentq,makeqtopmost on
QUD
Forintegration ofaskmoves,di®erentrulesareuseddependingonwhothespeakeris:the
system(rule2.2)ortheuser(rule2.3.)
(rule2.2)rule:integrateSysAsk
class:integrate
pre:(
$/shared/lu/speaker ==sys
in($/shared/lu/moves,ask(Q))
eff:n
push(/ shared/qud,Q)
Theconditions oftherulein(2.14)checksthatthelatestspeakerissysandthatthelatest
movewasanaskmovewithcontentQ.TheupdatepushesQon/shared/qud .

44 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
(rule2.3)rule:integrateUsrAsk
class:integrate
pre:(
$/shared/lu/speaker ==usr
in($/shared/lu/moves,ask(Q))
eff:(
push(/ shared/qud,Q)
push(/ private/agenda,respond(Q))
Theupdaterulein(rule2.3)forintegrating userqueriesisslightlydi®erent:iftheuser
asksaquestion q,thesystemwillalsopushrespond(q)ontheagenda. Thisdoesnot
happenifthesystemasksthequestion, sinceitistheuserwhoisexpectedtoanswerthis
question.
Eventually,the¯ndPlan (seeSection2.8.6)rulewillloadtheappropriate planfordealing
withQ.Thisassumes thatforanyuserquestion thatthesystemisabletointerpret,there
isaplanfordealingwiththatquestion. Ifthiswerenotthecase,IBiSwouldsomehow
havetorejectQ;inChapter 3wewilldiscussthisfurther.
Reasonsforansweringquestions
Thesolution ofpushingrespond(Q)ontheagendawhenintegrating auserask(Q)moveis
nottheonlypossibleoption.Itcanbeseenasasimple\intention-based" strategy involving
minimal reasoning; \Iftheuseraskedq,I'mgoingtorespondtoq".Alternativ ely,one
couldoptforamoreindirect linkbetweentheuseraskingaquestion andthesystem
intendingtorespondtoit.
Onesuchindirectapproachistonotpushrespond(Q)ontheagendawhenintegrating a
userask(Q)move,butonlypushQonQUD7.Aseparate rulewouldthenpushrespond(Q)
ontheagendagiventhatQisonQUDandthesystemhasaplanforrespondingtoQ.
Thisreasoning behindthisrulecouldbeparaphrased roughlyas\Ifqisunderdiscussion
andIknowawayofdealingwithq,Ishouldtrytorespondtoq".Onthisapproach,
itwouldbeassumed thatDPsdonotcareaboutwhoaskedaquestion; theywillsimply
attempt toansweranyquestion thatisunderdiscussion, regardless ofwhoraisedit.
Asecondindirectapproachistoassumethataskingaquestion introducesobligations on
theaddressee. This\obligation-based approach"wouldrequirerepresentingobligations as
partoftheshared information. Foranobligation-based accountofdialogue, seeTraum
(1996);foracomparison ofQUD-based andobligation-based approaches,seeKreuteland
7Ifthesystemcanunderstand userquestions whichitcannotrespondto(whichIBiS1doesnot),the
integration ruleforuseraskmoveswouldstillneedtocheckthatthereisaplanfordealingwithQ,orelse
rejectQ;issuerejection isdiscussed furtherinChapter 3.

2.8.IBIS1UPDATEMODULE 45
Matheson (1999).Asimilarsolution wouldbetoassociateeachquestion onQUDwith
theDPwhoraisedit.However,thesesolutions seemlessconsisten twiththesemantically-
basedaccountofissue-based dialogue managemen tweareexploring here.Forthekinds
ofdialogue wearedealingwithinthisthesis,webelievethatitisnotnecessary tomodel
obligations explicitly .However,formorecomplex dialogues acombination ofQUDand
obligations maybeneeded;seeSection6.5.2forfurtherdiscussion.
2.8.3Resolving issues
Cooperativeassertion protocol
Ginzburg providesaprotocolforcooperativeassertion, shownin(2.15).
1.Aassertsp:
²p?becomesmaximal inA'sQUD
²A'slatest-mo ve:AASSERTp
2.B'sreaction:
²B'slatest-mo ve:AASSERTp
²p?becomesmaximal inB'sQUD
3.Option1-acceptance:
²Bmakesana±rmativ eutterance uaboutp?
²Bincremen tsherFACTSbyadding p
²Bdowndates herQUD
4.Option2-discuss
²Bprovidesaresponsethataddresses p?
Dealingwithshortanswers
Ginzburg providesaninterpretation ruleforshortanswerstowh-questions. Anotationally
alteredversionofthisruleisshownin(2.15)8.
8Thealterations mostlyhavetodowiththefactthatGinzburg usessituation semantics.Also,therule
hasbeenalteredforreadabilit y.

46 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
S!XP
Content(S)=q[content(XP)],whereqisQUD-maximal
WhatthisrulesaysisthatifasentenceSconsists ofsome(elliptical) phrase XP,the
contentofScanbeobtained byapplying aQUD-maximal question qtothecontentof
XP.Thisruleisextended tohandley/n-questions and(usingtype-raising andapplying
theanswertothequestion ratherthantheotherwayaround) morecomplex kindsof
answers.However,wewillnotdiscusstheseissuesheresincethesimplecasesweare
dealingwithherearehandled bythecombine function describedinSection2.4.7.
Integrating answermoves
Forourcurrentpurposes,Ginzburg's assertion protocolisinonerespectmorecomplicated
thanwhatwewantrightnow.Theissueofutterance acceptance willbedealtwithin
Chapter 3;forthemomentwewillignorethisaspect.Thismeansthatoption2isnot
included here;weassumethatallutterances areaccepted, andwedonothavetorepresent
theissue?p.
Afurthermodi¯cation ofGinzburg's accountisthatwewillnotbedealingwithassertions
assuch;rather,wewillusethemove-labelofanswerformoveswith(possiblyunderspeci-
¯ed)propositional contentrelevanttosomeissueinthecurrentdomain. Thisalsorequires
checkingthisrelevancepriortointegrating ananswer-move.Thereaderwhodoesnotap-
proveoftheterminology usedherecanthinkofanswer-movesasassertions; itisaquestion
ofterminology withlittletheoretical importance.
WhileGinzburg viewsshortanswersasassertions andusesQUDtodetermine theircontent,
wedividethingsupinadi®erentway.WewillnotuseQUDtodetermine thecontent
ofashortanswer,aspartoftheinterpretation process;instead, weuseittodetermine
theupdatee®ects.Thatis,insteadofhavingtheinterpret modulecheckthecontents
ofQUDanduseitforcomputing thecontentsofashort-answ erassertion, weregard
theshortanswerashavinganunderspeci¯edcontent.Thismovestheresolution ofshort
answersfromtheinterpreter tothedialogue moveengine.Thereasonforthiswillbecome
apparentinchapter4;inshort,¯ndingtherightquestion toresolveashortanswermay
requirecomplex processing,possiblyinvolvingaskingtheuserclari¯cation questions, and
thusitisataskmoresuitedfortheDMEthantheinterpretation module.Thisalsoenables
ustokeeptheinterpretation moduleindependentofthecurrentdialogue state(however,
itisstillcrucially dependentonthedomain).
Theruleforintegrating answersisseenin(rule2.4).

2.8.IBIS1UPDATEMODULE 47
(rule2.4)rule:integrateAnsw er
class:integrate
pre:8
><
>:in($/shared/lu/moves,answer(A))
fst($/shared/qud,Q)
$domain ::relevant(A,Q)
eff:(
!$domain ::combine(Q,A,P)
add(/shared/com,P)
The¯rstcondition checksthatthelatestmovewasananswermovewithcontentA,and
thenexttwoconditions checkthatAisrelevanttosomequestion Qtopmost onQUD.
The¯rstupdatescombinesQandAtoformaproposition Paccording tothede¯nition
inSection2.4.7.Finally,Pisaddedtothesharedcommitmen ts.
2.8.4Downdating QUD
QUDdowndating principle
Ginzburg's \QUDdowndating principle" goesasfollows:
Assume qiscurrentlymaximal inA'sQUD,andthatthereexistsapinA's
FACTSsuchthatpisgoal-ful¯lling information forAwithrespecttoq.Then,
andonlythen,permitAtoremoveqfromQUD.
AsmentionedinSection2.4.6,wemakenodistinction betweenananswerbeinggoal-
ful¯lling foraDPwithrespecttoQandtheanswerresolving aquestion Q.
UpdateruleforQUDdowndate
InourversionoftheQUDdowndateprinciple, aquestion isremovedfromQUDifitis
resolvedbysharedinformation:
(2.15)Ifqison/shared/qud andthereisaproposition pin
/shared/com suchthatpresolves q,removeqfromQUD
Thecorrespondingupdateruleisshownin(rule2.5).

48 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
(rule2.5)rule:downdateQUD
class:downdatequd
pre:8
><
>:fst($/shared/qud,Q)
in($/shared/com,P)
$domain ::resolves(P,Q)
eff:n
pop(/shared/qud)
Theparaphrase ofthisruleisstraightforwardandisleftasanexercisetothereader.
Thisruleisperhapsine±cien tinthesensethatitmayrequirecheckingallpropositionsin
/shared/com everytimetheupdatealgorithm isexecuted. However,inthesystemswe
areconcerned withthenumberofpropositionsisnotveryhigh,andinaddition wefavour
clarityandsimplicityintheimplemen tationovere±ciency .
2.8.5Integrating greetandquitmoves
InIBiS1greetings havenoe®ectontheinformation state.Theruleforintegrating greetings
isshownin(rule2.6).
(rule2.6)rule:integrateGreet
class:integrate
pre:n
in($/shared/lu/moves,greet)
eff:f
Theupdaterulesforintegrating quitmovesperformed bytheuserorsystemareshownin
(rule2.7)and(rule2.8,)respectively.
(rule2.7)rule:integrateUsrQuit
class:integrate
pre:(
$/shared/lu/speaker ==usr
in($/shared/lu/moves,quit)
eff:n
push(/ private/agenda,quit)
Ifthequitmoveisperformed bytheuser,thee®ectisthatthesystemputsquitonthe
agendasothatitgetstosay\Goodbye"totheuserbeforethedialogue ends.

2.8.IBIS1UPDATEMODULE 49
(rule2.8)rule:integrateSysQuit
class:integrate
pre:(
$/shared/lu/speaker ==sys
in($/shared/lu/moves,quit)
eff:n
program state:=quit
Integrating aquitmoveperformed bythesystemcausestheprogram statevariableto
besettoquit.Thiswilleventuallycausetheprogram tohalt.
Thegreetmovedoesnothaveanye®ectontheinformation state,andthusnoupdaterule
isneededtointegrateit.
2.8.6Managing theplan
Thedialogue plansareinterpreted byaclassofupdaterulescalledexecplan.Whena
planhasbeenenteredintothe/private/plan ¯eld,itisprocessedincremen tallybythe
planmanagemen trules.Theserulesdetermine whichactionsendupontheagenda.
Findingandloadingaplan
Whenintegrating auseraskmovewithcontentQ,theactionrespond(Q)ispushedonthe
agenda,thusenabling (rule2.9)totriggerandloadaplanfordealingwithQ.
(rule2.9)rule:¯ndPlan
class:¯ndplan
pre:8
><
>:fst($/private/agenda,respond(Q))
$domain ::plan(Q,Plan)
notin($/private/bel,P)and$domain ::resolves(P,Q)
eff:(
pop(/private/agenda)
set(/private/plan,Plan)
The¯rsttwoconditions checkthatthereisanactionrespond(Q)ontheagendaandthat
thesystemhasaplanfordealingwithQ.Thethirdcondition checksthatthesystemdoes
notalreadyknowananswertoQ(ifitdoes,thesystemshouldinsteadrespondtoQ).If
theseconditions hold,theupdatespoprespond(Q)o®theagendaandloadtheplan.

50 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
Executing theplan
Ginzburg providesadialogue-lev elappropriateness condition forquerying:
Aquestion qcanbesuccessfully posedbyAonlyiftheredoesnotexistafact¿
suchthat¿2DGB(A)jFACTSand¿resolves qrelativetoUNPUB-MS(A).
Whatthisbasically saysisthatoneshouldnotaskaquestion whoseanswerisalready
shared.Onanindividual level,eachDPshouldmakesuretonotasksuchquestions. In
IBiS1,thiswillbeguaranteedbytheremoveFindout (rule2.10).
(rule2.10) rule:removeFindout
class:execplan
pre:8
><
>:fst($/private/plan,¯ndout( Q))
in($/shared/com,P)
$domain ::resolves(P,Q)
eff:n
pop(/private/plan)
Thisruleremovesa¯ndout( Q)actionfromtheplanincasethereisaresolving proposition
Pin/shared/com .
IfthereisaconsultDB actiontopmost ontheplan,(rule2.11)willtriggeradatabase
search.
(rule2.11) rule:execconsultDB
class:execplan
pre:n
fst($/private/plan,consultDB( Q))
eff:8
>>><
>>>:!$/shared/com=B
!$database::consultDB( Q,B,C)
add(/private/bel,C)
pop(/private/plan)
Thisruletakesallthepropositionsin/shared/com andgiventhislooksuptheanswer
toqinthedatabase. Theresulting propositionisstoredin/private/bel.

2.9.IBIS1SELECTION MODULE 51
2.8.7Updatealgorithm forIBiS1
Theupdatealgorithm usedbyIBiS1isshownin(2.16).
(2.16)ifnotlatestmoves==failed
thenhapplyclear(/private/agenda),
getLatestMo ve,
integrate,
trydowndatequd,
tryloadplan,
repeatexecplani
Ifinterpretation failed,theupdatealgorithm willstop.Otherwise, thesystem¯rstclears
theagendatomakeplaceforanyactionsthatmaybeselected duringgrounding (and
selection). Then,itdealswithgrounding (getLatestMo ve)andintegration ofthelatest
utterance. ThentheQUDisdowndated ifpossible,andifnecessary aplanmaybeloaded.
Finally,theplanisexecuted byrepeatedlyremovingactionsfromtheplan,orexecuting
consultDB actions,untilnomoreactionscanbeexecuted.
2.9IBiS1selectionmodule
Thetaskoftheselection moduleinIBiS1istodetermine thenextmovetobeperformed
bythesystem. InIBiS1,thisisafairlytrivialtask,involvingtwoparts:¯rst,selectan
agendaitembyeitherselecting torespondtoanissueortakingthetopmost actionfrom
theplanandmoveittotheagenda;second,selectamovewhichrealizesthisaction.
2.9.1Selecting anactionfromtheplan
Theruleforselecting anactionfromtheplanisshownin(rule2.12).
(rule2.12) rule:selectFromPlan
class:selectaction
pre:(
isempty($/private/agenda)
fst($/private/plan,Action)
eff:n
push(/ private/agenda,Action)

52 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
Thecondition thattheagendamustbeemptyensuresthatthereisnevermorethanone
actionontheagendastack.Inprinciple, thestackofactionscouldtherefore bereplaced
byasingleaction.Notethatthisruledoesnotremovetheactionfromtheplan;whenthis
shouldbedonedependsontheaction;forexample, anaction¯ndout( Q)isnotremoved
untilQisresolved.
2.9.2Selecting theaskmove
Ginzburg providesaQueryAppropriateness Condition, quotedin(2.17).
(2.17)Aquestion qcansuccessfully beposedbyAwhenandonlywhen
1.either
(a)A'sQUDisempty,or
(b)maximal inA'sQUDisaquestion q1suchthatq
in°uences q1relativetoA'sUNPUB-MS
2.thereisnopropositionpinA'sDGBjFACTSsuchthatp
resolves qrelativetoA'sUNPUB-MS.
InIBiS1,Ginzburg's condition isguaranteedtoholdandneedsnotbeexplicitly checked.
Regarding the¯rstpartofthecondition, IBiS1willnotloadaplanunlessthereisan
issueq1onQUDwhichneedstoberesolved,andanyquestion qwhichispartoftheplan
(byvirtueofa¯ndoutaction)willbesuchthatitin°uences q1;indeed,thisisexactlythe
de¯nition ofin°uences thatweassume(seeSection2.8.2).
Also,thesecondpartofthecondition isguaranteedtoholdbyvirtueoftherulere-
moveFindout describedinSection2.8.6.Thisruleremovesanaction¯ndout( q)fromthe
planincasethereisaresolving propositionin/shared/com .
Theruleforselecting anaskmoveisshownin(rule2.13).
(rule2.13) rule:selectAsk
class:selectmove
pre:(
fst($/private/agenda,¯ndout( Q))orfst($/private/agenda,
raise(Q))
eff:(
add(nextmoves,ask(Q))
ifdo(fst($/ private/plan,raise(A)),pop(/private/plan))

2.9.IBIS1SELECTION MODULE 53
Thecondition checksifa¯ndoutorraiseactionwithcontentQisontheagenda. Ifso,
the¯rstupdateaddsanask(Q)movetonextmoves.Thesecondupdateremovesthe
actionfromtheplanincaseitwasaraiseaction.Thisisactually abitpremature, sinceQ
hasnotyetbeenraised;however,theassumption ofperfectcommunication madeinIBiS1
licensesthisupdate.WereturntothisissueinSection3.6.9.
2.9.3Selecting torespondtoaquestion
Ginzburg doesnotprovidean\Assertion Appropriateness Condition" correspondingtothe
oneforquerying.
WewillassumethatforaDPAtoselectananswermovewith(propositional) contentp,
theremustbeaquestion Qtopmost onQUDandapropositionPwhichresolves Qsuch
thatAprivatelybelievesthatpistrue.
Also,pmustnotbeinwhatAtakestobethesharedcommitmen ts;ifitwere,theanswer
movewouldbeirrelevant.However,thedowndateQUD ruledescribedinSection2.8.4
guaranteesthatresolvedissuesareremovedfromQUD.
Wedividetheselection ofananswermoveintotwosteps:¯rst,theselection ofarespond
actionandsecond,theselection ofananswermove.Themotivationforthisisthatthe
answermovecouldalsobeselected without beingpreceded bytheselection ofarespond
action,inthecasewheretheuserasksaquestion whichthesystemalreadyknowsthe
answerto.
Theruleforselecting torespondtoaquestion isshownin(rule2.14).
(rule2.14) rule:selectResp ond
class:selectaction
pre:8
>>>>>>>><
>>>>>>>>:isempty($/private/agenda)
isempty($/private/plan)
fst($/shared/qud,Q)
in($/private/bel,P)
notin($/shared/com,P)
$domain ::relevant(P,Q)
eff:n
push(/ private/agenda,respond(Q))
The¯rsttwoconditions checkthatthereisnothingelsethatcurrentlyneedstobedone.
Theremaining conditions checkthatsomequestion Qistopmost onQUD,thesystem
knowsarelevantanswerPtoQwhichisnotyetshared.

54 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
Iftheuserraisesaquestion q,IBiSwillpushqonQUDandrespond(q)ontheagenda.
Ifthereisnopropositionresolving qin/private/bel,aplanfordealingwithqwillbe
loaded. Whenthisplanhasbeenexecuted, theremaybeapropositionresolving qin
/private/bel (e.g.theresultofadatabase search).Ifthisisthecase,therulein(2.17)
canbeapplied, andrespond(q)isagainpushedontheagenda. Thistimeitwillleadto
thesystemprovidingananswertoq.
Asanaside,wemaynotethatthisselection strategy wouldcovercaseswhereaDPAasks
q(e.g.\What's thetime?") butthen¯ndsananswertoqindependentlyofthedialogue
(e.g.bylocatingaclock).Inthiscase,Awilleventuallyanswerherownquestion (e.g.
\Oh,it's5pm."),thusenabling theotherDPtoremoveqfromhisQUDaswell.Thisrule
alsohasthenice(butperhapsnotextremely useful)featurethatitwouldcoverrhetorical
questions aswellasordinary ones(however,thiswouldrequireselection rulesforasking
questions towhichonealreadyknowstheanswer).
2.9.4Selecting theanswermove
Giventhatarespond(Q)actionisontheagenda,andthesystemknowsarelevantanswer
PtoQwhichisnotyetshared,therulein(2.18)selectsanaskmovewithcontentPto
bepushedonnextmoves.
(rule2.15) rule:selectAnsw er
class:selectmove
pre:8
>>><
>>>:fst($/private/agenda,respond(Q))
in($/private/bel,P)
notin($/shared/com,P)
$domain ::relevant(ºA,Q)
eff:n
add(nextmoves,answer(P))
Again,itmaybearguedthatitisine±cien ttohavetocheckthesameconditions twicein
thecasewhereselectAnsw erispreceded byselectResp ond.However,aswementioned
abovetherespondactionmayalsohavebeenpushedontheagendawhenintegrating a
useraskmove,andinthiscasetheconditions needtobechecked.

2.10. ADAPTING IBIS1TOTHETRAVELINFORMA TION DOMAIN 55
2.10Adapting IBiS1tothetravelinformation domain
Thedomainwewilluseasanexample isatravelagencywheretheusercan¯ndoutthe
priceofatripbygivinginformation aboutdestination, whentotravel,etc.Itshouldbe
stressed thatthetravelagencydomainisonlyintendedasanexample; theIBiS1system
itself,whilelimitedtoverysimpleinformation-seeking dialogue, isnotdomain-dep endent.
Allinformation speci¯ctothetravelagencydomainisstoredinthelexicon,domain, and
database resources andtoadaptthesystemtoanewdomainonlythesecomponentsneed
tobecreated. Also,asthisisonlyanexample, theimplemen tationisnotintendedas
aready-to-use systeminarealapplication andtheresources aretherefore merely\toy"
resources.
2.10.1Thedomainresource
ThedomainknowledgeusedbyIBiS1inthetravelagencydomainconsistsofadialogue
planandaspeci¯cation ofsortalrestrictions.
Dialogueplansforthetravelagencydomain
Inthetravelagencydomain, wehaveimplemen tedtwoplans:oneforpriceinformation
(shownin(2.18))andoneforvisainformation (shownin(2.18)). Theplanstructure is
simple;¯rst,thesystem¯ndsouttheanswerstoanumberofquestions byaskingtheuser.
Then,thesystemperformsadatabase searchtogetthepriceforthespeci¯edtrip,and
placestheresultin/private/bel.
Itshouldbestressedthatthepurposeofthisimplemen tationoftheTAdomainisonlyto
allowustogiveconcrete examples ofthedialogue managemen tstrategies implemen tedin
IBiS.Itisbynomeansintendedasafull-scale application, andmuchcouldbesaidabout
itsinsu±ciencies evenasatoyapplication.

56 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
(2.18) issue:?x.price(x)
plan:h
¯ndout(?x:meansoftransport(x)),
¯ndout(?x:destcity(x)),
¯ndout(?x:depart-cit y(x)),
¯ndout(?x:depart-mon th(x)),
¯ndout(?x:depart-da y(x)),
¯ndout(?x:class(x)),
consultDB(?x:price(x))
i
(2.19) issue:?needvisa
plan:h
¯ndout(?x:destcity(x)),
¯ndout(?x:citizenship( x)),
consultDB(?needvisa),
i
Sortalhierarchy
top8
>>>>>>>>>>>>>>>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:city8
>>><
>>>:paris
london
goteborg
...
means oftranspor t8
><
>:plane
boat
train
month8
><
>:january
february
...
dayn
1;2;:::;31
class(
economy
business
pricen
Nat
Sortalrestrictions
Thesortalrestrictions on(argumen tsof)propositionsareshowninTable2.4.

2.10. ADAPTING IBIS1TOTHETRAVELINFORMA TION DOMAIN 57
proposition restriction
destcity(X)) X2location
departcity(X)) X2location
how(X)) X2means oftranspor t
departmonth(X))X2month
class(X)) X2class
price(X)) X2price
Table2.4:Sortalrestrictions onpropositions
2.10.2Lexiconresource
Theinterpretation lexiconconsistsoftwoparts:lexicalsemanticsandaphrase-to-mo ve
translation table.Thelexicalsemanticssimplylistsanumberofalternativ ewordsor
phraseswhichareseenasrealizations ofthesamesemanticconcept. Forsomeconcepts
(i.e.cities)thesynonymysetisasingleton, whichmeanstherearenosynonyms.Apart
ofthelexicalsemanticsforIBiS1isshowninTable2.5.
phrase lexicalsemantics
\°ight",\°ights",\plane", \°y",\airplane" plane
\cheap",\secondclass",\second" economy
\¯rstclass",\¯rst",\expensive",\business class"business
\Paris" paris
Table2.5:Synonymysetsde¯ning thefunction lexsem
Thephrase-to-mo vetranslation tablebasically consistsofalistofpairshWordList;Movei,
whereWordListisalistofwordtokensorPrologvariables, andMoveisadialogue move.
Anyuserutterance (inputstring)containingasequence ofwordsmatchingWordListwill
beinterpreted asaninstance ofMove.Wherethewordlistscontainsvariables, thereare
alsosortalconditions ontheconceptcorrespondingtothewordinstantiatingthevariable.
Auserutterance mayrealizeseveralmoves,incaseitmatchesseveralwordlists.
wordsequence move restriction
hWi answer(C)lexsem( W)=C,Cisofsortconcept
hto,Wi answer(to(C))lexsem( W)=C,Cisofsortcity
...
hhelloi greet
...
Table2.6:AfragmentoftheEnglish IBiS1travelagencylexicon
Similarly ,thegeneration lexiconisalistofpairshMove;Stringi,whereMoveisadialogue
moveandStringisthecorrespondingoutputstring.

58 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
2.10.3Database resource
Thedatabase forthetravelagencydomaincontainsinformation aboutthepriceoftrips,
andinformation aboutvisaregulations. Ifthereisnodatabase entrymatchingtheinfor-
mationspeci¯edinthequeryq,thedatabase willreturnafail(q)message.
2.11SampledialoguewithIBiS1
Inthissectionweshowasampleinteraction withIBiS1.Fortheexamples wehaveused
text-based inputandoutput,butthesystemcanalsousespeech.Inthis¯rstdialogue we
showsomeupdaterulesincluding theire®ects,information states,andutterances.
(dialogue 2.2)
selectOther©
add(nextmoves,greet)
S>Welcome tothetravelagency!
getLatestMo ve½
set(/shared/lu/moves,set([greet]) )
set(/shared/lu/speaker ,sys)
integrateGreet
2
666666664private=2
4agenda=hi
plan =hi
bel =fg3
5
shared =2
664com=fg
qud=hi
lu=·speaker =sys
moves =©greetª¸3
7753
777777775
2
666666664latestspeaker =sys
latestmoves =©
greetª
nextmoves =fg
program state=run
lexicon =lexicontravelenglish
domain =domaintravel
database =database travel3
777777775
U>priceinformation please

2.11. SAMPLE DIALOGUE WITH IBIS1 59
getLatestMo ve½set(/shared/lu/moves,set([ask(?A.price(A))]))
set(/shared/lu/speaker ,usr)
integrateUsrAsk½push(/ shared/qud,?A.price(A))
push(/ private/agenda,respond(?A.price(A)))
¯ndPlan½
pop(/private/agenda)
set(/private/plan,stack([raise(? C.how(C)),¯ndout(?D.destcity(D)),:::]))
2
666666666666666666664private=2
6666666666664agenda=hi
plan =*raise(?A.how(A))
¯ndout(?B.destcity(B))
¯ndout(?C.deptcity(C))
¯ndout(?D.month(D))
¯ndout(?E.deptday(E))
¯ndout(?F.class(F))
consultDB(? G.price(G))+
bel =fg3
7777777777775
shared =2
664com=fg
qud=­?H.price(H)®
lu=·speaker =usr
moves =©
ask(?H.price(H))ª¸3
7753
777777777777777777775
selectFromPlan©
push(/ private/agenda,raise(?A.how(A)))
selectAsk½add(nextmoves,ask(?A.how(A)))
ifdo(fst($/ private/plan,raise(?A.how(A))),pop(/private/plan))
S>Howdoyouwanttotravel?
getLatestMo ve
integrateSysAsk©push(/ shared/qud,?A.how(A))
2
666666666666666666664private=2
66666666664agenda=hi
plan =*¯ndout(?A.destcity(A))
¯ndout(?B.deptcity(B))
¯ndout(?C.month(C))
¯ndout(?D.deptday(D))
¯ndout(?E.class(E))
consultDB(? F.price(F))+
bel =fg3
77777777775
shared =2
66664com=fg
qud=¿
?G.how(G)
?H.price(H)À
lu=·speaker =sys
moves =©
ask(?G.how(G))ª¸3
777753
777777777777777777775

60 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
U>aflight
getLatestMo ve
integrateAnsw er½
!$domain ::combine(?A.how(A),plane,B)
add(/shared/com,B)
downdateQUD
2
6666666666666666664private=2
66666666664agenda=hi
plan =*¯ndout(?A.destcity(A))
¯ndout(?B.deptcity(B))
¯ndout(?C.month(C))
¯ndout(?D.deptday(D))
¯ndout(?E.class(E))
consultDB(? F.price(F))+
bel =fg3
77777777775
shared =2
664com=©
how(plane)ª
qud=­?G.price(G)®
lu=·speaker =usr
moves =©
answer(plane)ª¸3
7753
7777777777777777775
selectFromPlan
selectAsk
S>Whatcitydoyouwanttogoto?
U>paris
S>Whatcitydoyouwanttogofrom?
U>london
S>Whatmonthdoyouwanttoleave?
U>inapril
S>Whatdaydoyouwanttoleave?
U>thefifth
S>Whatclassdidyouhaveinmind?
U>ascheapaspossible
getLatestMo ve

2.11. SAMPLE DIALOGUE WITH IBIS1 61
integrateAnsw er
downdateQUD
removeFindout
execconsultDB8
>><
>>:!$/shared/com=B
!$database::consultDB(? A.price(A),B,C)
add(/private/bel,C)
pop(/private/plan)
2
6666666666666666664private=2
4agenda=hi
plan =hi
bel =©
price(123)ª3
5
shared =2
6666666666664com=8
>>>>>><
>>>>>>:class(economy )
deptday(¯fth)
month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>>>>>=
>>>>>>;
qud=­
?A.price(A)®
lu=·speaker =usr
moves =©
answer(class(economy ))ª¸3
77777777777753
7777777777777777775
selectResp ond©
push(/ private/agenda,respond(?A.price(A)))
selectAnsw er©
add(nextmoves,answer(price(123)) )
S>Thepriceis123crowns.
getLatestMo ve
integrateAnsw er
downdateQUD
2
666666666666666666664private=2
4agenda=hi
plan =hi
bel =©
price(123)ª3
5
shared =2
666666666666664com=8
>>>>>>>><
>>>>>>>>:price(123)
class(economy )
deptday(¯fth)
month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>>>>>>>=
>>>>>>>>;
qud=hi
lu=·speaker =sys
moves =©
answer(price(123))ª¸3
7777777777777753
777777777777777777775

62 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
2.12Discussion
Inthissection,wediscusssomewaystoextendandmodifyIBiS1,andalsosomemore
generalissuesconcerning issue-based dialogue managemen t.
2.12.1Single-issue systems
Forsystemswhichareonlyabletoanswerasinglequestion, itisperhapsagoodideato
notforcetheusertoaskthequestion, butratherputitintheagendawheninitializing
theIS,andpushingthequestion onQUD.Thisamountstoassuming attheoutsetofthe
dialogue thattheuserandsystemalreadyhaveestablished whatquerythesystemcan
answer.
Suchasystemwoulddowithout theintegrateUsrAsk rule,sincetheusercannotask
anyquestions. (Note,however,thatthesystemcanbothaskandanswerquestions, sowe
arenotdealingwithpurelyinformation-seeking dialogue.) Toloadthequestion andplan
attheoutsetofthedialogue, theresetoperations wouldbemodi¯edasseenin(2.20).
(2.20)set(program state,run)
set(lexicon ,lexicon-Domain-Lang)
set(database,database- Domain)
set(domain,domain- Domain)
check(domain ::plan(Q,TopPlan))
push(/private/plan ,TopPlan)
push(/shared/qud ,Q)
push(/private/agenda,greet)
2.12.2\HowcanIhelpyou?"
The¯rstuserutterance inthedialogue inSection2.11is\priceinformation please". Now,
IBiS1interpretsthisasanaskmove,whichmayappearodd.However,theutterance does
explicitly raiseanissue(regarding price),andthisistheonlycriteriaweusetoclassify
something asanaskmove.Analternativ enameforthisdialogue movewouldhavebeen
raise,butwehavechosentogowithasksinceitcorrespondsnaturally totheanswermove.
Theusercouldalsohavesaid\What's theprice?" orsomething similar,howeverthis
doesnotsoundverynaturalunlesssupplemen tedwithsomeadditional information, e.g.
\What's thepriceofatriptoParisinApril?". Whileutterances suchasthesearenot
handled byIBiS1,theywillbehandled byIBiS3whichisintroducedinChapter 4.

2.12. DISCUSSION 63
Actually,\priceinformation please"couldalsoberegarded asananswertoaquestion,
e.g.\WhatcanIdoforyou?"or"Whatkindofinformation doyouwant?"or\Doyou
wantpriceinformation orvisainformation?". Infact,wewouldarguethatthesekinds
ofquestions areresolvedbyaskingotherquestions. Ingeneral, anaskmoveisamove
whosecontentresolvestheissue\whatquestion shouldweaddressnext?",whichmaybe
formalized as?x.issue(x).Wecallsuchquestions issue-questions .
Ausefulextension ofIBiS1wouldbetoaddaplanforaddressing thisissue,andload
thisplanwhenthesystemisstartedup.Iftheuserdoesnotanswerthewh-question (e.g.
\WhatcanIdoforyou?")ifwouldbehelpfulifthesystemspeci¯edtheavailablechoices
usinganalternativ e-question (e.g.\Doyouwantpriceinformation orvisainformation?").
Thiscanbeaccomplished bytheplanin(2.21).
(2.21) issue:?x.issue(x)
plan:h
raise(?x.issue(x)),
¯ndout( f?issue(? x.price(x)),?issue(?need visa)g)
i
The¯rstactionraisesthewh-question; iftheuserdoesnotaddressit(byaskingaques-
tion!),thesystemwillproceedtoaskthealt-question. However,iftheuseraddresses the
wh-question the¯ndoutactionwillbepoppedo®theplansincethealt-question hasalready
beenresolved.
Onewayofimplemen tingthisistohaveruleswhichremoveactionsandquestions which
concernwhatissuetoaddressfromtheplan,agenda,andQUDbasedonthecontentsof
QUD(ratherthanbasedonlyonthesharedcommitmen ts,ashasbeendoneuntilnow).
Forexample, forremovingresolvedissue-questions o®QUD,(rule2.16)wouldneedto
beadded(notethatthisrulerequires QUDtobeanopenstack).
(rule2.16) rule:downdateQUD2
class:downdatequd
pre:8
><
>:in($/shared/qud,IssueQ)
fst($/shared/qud,Q)
$domain ::resolves(Q,IssueQ)
eff:n
del(/shared/qud,IssueQ)
Wealsoneedtode¯neresolvednessconditions forissue-questions (forexample, anissue-
question cannotberesolvedbyanissue-question). Inaddition, rulesforremoving¯ndout
andraiseactionsfromtheplanbasedonthecontentsofQUDwouldneedtobeadded.

64 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
Thisallowsdialogues likethatin(dialogue 2.3).Notethattheuser'sutterance \price
information please"isstillclassi¯ed asanaskmove.
(dialogue 2.3)
S>Welcome tothetravelagency!
U>
S>HowcanIhelpyou?
U>
S>Doyouwantpriceinformation orvisainformation?
U>priceinformation please
S>Howdoyouwanttotravel?
2.12.3Reraising issuesandsharinginformation
IBiS1isabletoansweranynumberofquerieswhichtheresources aresetuptohandle,
aslongaseachissueisresolvedbeforemovingontothenextone.Iftheuserasksqand
thenasksq0beforeqhasbeenresolved,IBiS1willforgetitsplanfordealingwithqand
insteadloadtheplanfordealingwithq0.Whenq0hasbeenresolved,IBiS1willwaitfor
anewquestion fromtheuser.However,qisstillonQUD,andbyaddingasimplerulewe
couldmakeIBiS1reloadtheplanfordealingwithqandgetbacktoworkonit.
TherecoverPlanrule(rule2.17)willpickupanyquestion QlyingaroundonQUD
whentheplanandagendaisempty,checkifthereisaplanforresolving it,andifsoload
thisplan.
(rule2.17) rule:recoverPlan
class:execplan
pre:8
>>><
>>>:fst($/shared/qud,Q)
isempty($/private/agenda)
isempty($/private/plan)
$domain ::plan(Q,Plan)
eff:n
set(/private/plan,Plan)
However,thissolution hasaproblem. If,whendealingwithaquestion q,thesystem
asksaquestion quandtheuserdoesnotanswerthisquestion butinsteadraisesanew
question q1,bothqandquwillremainonQUDwhenq1hasbeenresolved.Now,ifthe
usersimplyanswersquimmediately afterq1hasbeenresolved,everything is¯neandthe
systemwillreloadtheplanfordealingwithq.However,iftheuserdoesnotanswerqu,

2.12. DISCUSSION 65
thisquestion willbetopmost onQUDandblockrecoverPlanfromtriggering. Because of
thesimplestructure ofQUD, IBiS1seesnoreasontoaskquagain;afterall,itisalready
underdiscussion, andtheuserisexpectedtoprovideananswer.
ThereraiseIssue shownin(rule2.18)ruleprovidesasolutiontothisproblem. Itreraises
anyquestions onQUDwhicharenotassociatedwithanyplan(i.e.whichhavebeenraised
previously bythesystem).
(rule2.18) rule:reraiseIssue
class:selectaction
pre:(
fst($/shared/qud,Q)
not$domain ::plan(Q,SomePlan)
eff:n
push(/ private/agenda,raise(A))
Issuesaredividedupbetweenthoseforwhichthesystemhasanassociatedplaninits
domainresource andthoseforwhichitdoesnot.Forexample, the\priceissue"isonefor
whichthereisaplan:thesystemhastoaskwheretheuserwantstogo,wherefrom,when
etc.However,thereisnoplanassociatedwiththequestion ofwheretheuserwantstogo
from.Thisquestion issimplypartoftheplanforthepriceissue.Thus,whenthesystem
¯ndsthisquestion inthelistofopenissues(the¯rstcondition ofthisrule)andit¯nds
thatitdoesnothaveaplanforthisissue(thesecondcondition), itplanstoreraisethe
question.
Twofurthermodi¯cations areneededtomakethisworksmoothly.Firstly,whenaquestion
isreraised thatwaspreviously onQUD,thesimplestackstructure ofQUDwillresultin
twoinstances ofthesamequestion beingtopmost onQUD.Onewayofsolvingthisisto
changethedatatypeof/shared/qud intoan\openstack"or\stackset";thisdatatype
canberegarded asamixofastackandaset.Thepropertyofopenstacksrelevanttoour
problem isthatwhensomeelementxispushedonastackwhichalreadycontainsx(or
anelementuni¯able withx),theresulting openstackwillcontainasingleinstance ofx,
whichisalsotopmost ontheopenstack.
Secondly ,weneedaruleforremovingraise(Q)actionsfromtheplanincaseQhasalready
beenresolved;thisruleissimilartotheremoveFindout ruledescribedinSection2.8.6.

66 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
(rule2.19) rule:removeRaise
class:execplan
pre:8
><
>:fst($/private/plan,raise(A))
in($/shared/com,B)
$domain ::resolves(B,A)
eff:n
pop(/private/plan)
Thisruleisneededtoavoidaskingthesamequestion twiceincaseitis¯rstreraisedand
thenalsoincluded inarecoveredplan.
Asampledialogue involvingthesystemreraising anissueandrecoveringaplanisshown
in(dialogue 2.4).Incidentally,thisdialogue alsodemonstrates information sharingbe-
tweendialogue plans;whentheuserasksaboutvisa,thesystemalreadyknowswhatthe
destination cityisandthusdoesnotaskthisagain.Bycontrast,inVoiceXML (McGlashan
etal.,2001),user-initiated subdialogues willcauseprevious dialogue tobeforgotten. Only
ifthereisapre-scripted, system-initiated transition fromoneformtoanother canthe
previous dialogue beresumed afterthesubdialogue hasbeencompleted9.
(dialogue 2.4)
S>Welcome tothetravelagency!
U>priceinformation please
S>Howdoyouwanttotravel?
U>plane
S>Whatcitydoyouwanttogoto?
U>paris
S>Whatcitydoyouwanttogofrom?
U>doineedavisa
getLatestMo ve
9Information sharinginVoiceXML isonlypossibleinthecasewhereaformF1callsanotherformF2.
WhenF2is¯nishedandcontrolispassedbacktoF1,information maybesentfromF2toF1.Information
sharingisnotsupportede.g.incaseswhereuserinitiativeleadstotheadoption ofF2whileF1isbeing
executed.

2.12. DISCUSSION 67
integrateUsrAsk
¯ndPlan
removeFindout
selectFromPlan
selectAsk
S>Whatcountry areyoufrom?
U>sweden
S>Yes,youneedaVisa.
U>
reraiseIssue©
push(/ private/agenda,raise(?A.deptcity(A)))
selectAsk
S>Whatcitydoyouwanttogofrom?
U>london
getLatestMo ve
integrateAnsw er
downdateQUD
recoverPlan
removeRaise
removeFindout
removeFindout
2
66666666666666666666664private=2
6666664agenda=hi
plan =*¯ndout(?A.month(A))
¯ndout(?B.deptday(B))
¯ndout(?C.class(C))
consultDB(? D.price(D))+
bel =©
needvisaª3
7777775
shared =2
66666666664com=8
>>>><
>>>>:deptcity(london)
needvisa
citizenship(sw eden)
destcity(paris)
how(plane)9
>>>>=
>>>>;
qud=­
?E.price(E)®
lu=·speaker =usr
moves =©
answer(london)ª¸3
777777777753
77777777777777777777775

68 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
selectFromPlan
selectAsk
S>Whatmonthdoyouwanttoleave?
2.12.4Database search,relevance,anddialogue
Whenconnecting adatabase resource toIBiS,theresource interfacespeci¯cation models
adatabase postasasetofpropositions, eachspecifyingavalueofadatabase parameter.
Ingeneral, whenconsulting adatabase thevaluesofsomeparameters areknown,and
thevaluesofsomeotherparameters arerequested fromthedatabase. Theremayalsobe
parameters inthedatabase whichareneitherspeci¯edorrequested.
InIBiS,wehaveassumed thatasingleparameter isrequested; therequested parameter
isspeci¯edbyaquestion q.Allpropositionsin/shared/com areincluded inthecallto
thedatabase, andthosepropositionsthatspecifyparameters inthedatabase tablewhere
therequested parameter isde¯nedareusedtorestrictthedatabase search;wereferto
thissetasSpecProp.Theresultofthedatabase searchiscurrentlyeitheraproposition
specifyingauniquevalueoftherequested parameter, orapropositionfail(q)indicating
thatnoanswertothequestion wasfound.
First,letusassumethatallparameters requested bythesystem(questions raisedbythe
system)havebeenspeci¯ed(answered)bytheuser,andthatthedatabase containsexactly
oneanswertoq.Now,ifthedatabase isconsulted fortheanswertoq,apositivesearch
resulthasthelogicalformofanimplication10VSpecProp!a,wherearesolves q.
Next,assumethatthedatabase containsnoanswertoq,givenSpecProp.Aparaphrase of
theresultfail(q)isthenthis:\Giventheconjunction ofallthepropositionsinSpecProp,
thedatabase containsnoanswertoq".Thisisclearlyrelevanttoq,butitdoesnotsay
thatqhasnoansweringeneralandisthusnotnegativelyresolving toq;givenadi®erent
setSpecProp,qmayhaveananswer.Therefore, weregardfail(q)asarelevantbutnot
resolving answertoq;thisisre°ected inourde¯nitions inSection2.4.6.
Tohandletheaforemen tionedtwocases,itissu±cienttostoreeitheraorfail(q),depend-
ingonwhether ananswerwasfoundornot,astheresultofthedatabase search.Thisis
whathasbeenimplemen tedinIBiSsofar.However,thereareothercaseswherethisis
notsu±cient.
Whatifnotallrelevantparameters arespeci¯ed?InIBiS,thiscanhappenifsomequestion
10TheoperatorVisafunction fromasetSofpropositionstotheconjunction ofallpropositionsinS.

2.12. DISCUSSION 69
isincluded inthedialogue planinaraiseaction.Inthiscase,severalanswersa1;:::;an
toqmaybefound11.Inthiscase,thedi®erentanswersmaycorrespondtodi®erentvalues
ofoneormoreoftheunspeci¯edparameters. Wewillrefertothesetofpropositions
specifyingtheseparameters (inthedatabase) foranansweraiasUnspecPropi.Inthis
case,apositiveresultofthedatabase searchcanberegarded ashavingthelogicalformin
(2.22).
(2.22)VSpecProp!
((VUnspecProp1!a1)&:::&(VUnspecPropn!an))
Thisconditional canbeusedinvariouswaysbyadialogue system. First,thesystem
cankeeptrackofwhether thesearchresultisstillrelevant;ifsomesharedcommitmen t
whichisalsoinSpecPropisremovedorchanged, theconsequen toftheconditional may
nolongerhold.Second,thesystemcanpresenttheresultinvariousways,eitherbysimply
asserting theconsequen t(VUnspecProp1!a1)&:::&(VUnspecPropn!an)(e.g.\For
economyclass,thepriceis$123.Forbusiness class,thepriceis$1234."), orbyaskingwhich
ofUnspecProp1;:::VUnspecPropnhold(e.g.\Doyouwanteconomyclassorbusiness
class?").
Totakeanexample fromtheTAdomain, supposetheuserdidnotanswerthequestion
whethertotravelineconomyorbusiness class.Then,di®erentanswerstothepricequestion
maybereturned: oneforbusiness classandoneforeconomyclass.Inthiscase,thesystem
couldgivebothanswersandalsoindicate thecorrespondingvaluesoftheunspeci¯ed
parameters.
Infact,analternativ edatabase searchoptionhasbeenimplemen tedasanextension to
IBiS1tohandlecaseslikethese.Theresultofasuccessful database searchinthisversion
isasetofpropositionsoftheformdbentry(SpecProp,UnspecProp,a).Thismaynot
betheoptimalrepresentationformat,butthisextension allowsdialogue likethatin(2.23)
(Here,thedialogue planonlyraisestheissueofclass,whichmakesitpossiblefortheuser
nottoanswerit.)
(dialogue 2.5)
S>Welcome tothetravelagency!
U>priceinformation please
S>Howdoyouwanttotravel?
U>aflight
S>Whatcitydoyouwanttogoto?
U>paris
11Itisalsopossiblethatseveralanswersarefoundevenifallparameters arespeci¯ed.

70 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
S>Whatcitydoyouwanttogofrom?
U>london
S>Whatmonthdoyouwanttoleave?
U>april
S>Whatdaydoyouwanttoleave?
U>fifth
S>Whatclassdidyouhaveinmind?
U>
S>Thepriceis7654crowns, economy class. Thepriceis456crowns,
business class.
Afurtherpossibility(thathasnotbeenimplemen ted)isthattheuserprovidesarelevant
butnotresolving answertooneormorequestions raisedbythesystem,e.g.byproviding
adestination countrywhenaskedforadestination city.Inthiscase,eitherthelessspeci¯c
answermustmatchsomeotherparameter inthedatabase (e.g.ifdestination countries
areincluded inaddition todestination cities),orsomeinference mustbeperformed. This
inference mayresultinadisjunction ofanswersspecifying parameters whichareinthe
database, e.g.thedisjunction ofallavailabledestination citiesinsomespeci¯edcountry.
Thisdisjunction canthenbeusedtosearchthedatabase. Furtherdatabase variations
includerequesting answerstomorethatonequestion atatime(e.g.\Iwantinformation
aboutpriceinformation anddeparture datesfor°ightstoParisinApril.").
2.12.5Additional planconstructs
InIBiS1wehaveusedaverybasicsetofplanconstructs. However,itisfairlystraight-
forwardtoaddnewconstructs, byaddingnewobjectsoftypePlanConstruct andupdate
rules(oftheclassexecplan)fordealingwiththem.Somemorecomplex constructs which
arenotusedherebuthavebeenusedinGoDiS,thepredecessor ofIBiS(seee.g.Larsson
andZaenen, 2000),arelistedbelow,withbriefexplanations ofwhatthecorresponding
updaterulesdo.
²ifthen(P,C)whereP:propositionandC:PlanConstruct; ifPisin/private/bel
or/shared/com ,thenreplaceifthen(P,C)withC1;otherwise, deleteit
²ifthenelse(P,C1,C2)whereP:propositionandC1:PlanConstruct andC2:
PlanConstruct; ifPisin/private/bel or/shared/com ,thenreplaceifthen(P,
C)withC1;otherwise, replaceitbyC2
²exec(®),where®:Actionisanactionsuchthatthereisaplan¦fordoing®;replace
exec(®)with¦(seeChapter 5foradiscussion ofaction-related plans)

2.12. DISCUSSION 71
²hC1;:::;CniwhereCi:PlanConstruct (1·i·n);prependC1;:::;Cntothe
/private/plan ¯eld.
Theseconstructs addconsiderably totheversatilityofdialogue plans,andallowe.g.asking
whether theuserwantsareturntrip(formalized e.g.asaquestion?return),andask
appropriate questions (returndateetc.)onlyiftheusersgivesapositiveresponse(i.e.if
thepropositionreturnisin/shared/com ).Adialogue planforaccomplishing thisis
shownin(2.23).
(2.23) issue:?x.price(x)
plan:h
¯ndout(?x:meansoftransport(x)),
¯ndout(?x:destcity(x)),
¯ndout(?x:depart-cit y(x)),
¯ndout(?x:depart-mon th(x)),
¯ndout(?x:depart-da y(x)),
¯ndout(?x:class(x)),
¯ndout(?return),
ifthen(return,h¯ndout(?x:return-mon th(x)),
¯ndout(?x:return-day(x))i),
consultDB(?x:price(x))
i
2.12.6Questions andanswersvs.slotsand¯llers
Inprinciple, aslotinaformcanbeseenasaquestion, anda¯llercanbeseenasananswer
tothatquestion. Theresult,aslot-¯ller pair,istheequivalentofaproposition. Ifthe
valueofaslotisbinary(0/1oryes/no),theslotcorrespondstoay/n-question; otherwise,
itcorrespondstoawh-oralternativ equestion.
Forexample, inatravelagencysettingaform-based systemmighthaveaformcontaining
aslotdest-cityforthedestination city;thiswouldcorrespondtoaquestion represented
inlambda-calculus as?x:dest-city(X)(\Whatisthedestination city?").A¯llerforthis
wouldbee.g.paris,whichwouldalsoconstitute ananswertothequestion. Theslot-
¯llerpairdest-city=paris wouldthencorrespondtotheFOLpropositionresulting from
applying thequestion totheanswer,dest-city(paris) .
Buttherearealsoimportantdi®erences betweenform-based andissue-based dialogue
managemen t.Forexample, asingleanswermayberelevanttoquestions inseveralplans.
Thisenablesinformation-sharing betweenplans,i.e.whenexecuting aplanthesystem

72 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT
cantakeadvantageofanyinformation supplied bytheuserwhileexecuting aprevious
plan,incasetheplansshareoneormorequestions. Another wayofputtingthisisthat
information informsarelocaltothatform,whilepropositional information canbeglobal
tothewholedialogue.
Formsprovideaverybasicsemanticformalism whichissu±cientforsimpleinquiry-
oriented(andtosomeextentaction-orien teddialogue), butitishardtoseehowitcanbe
extended tohandlemorecomplex kindsofdialogue, e.g.negotiativ e,tutorial, orcollab-
orativeplanning dialogue. Issue-based dialogue managemen tisindependentofthechoice
ofsemanticformalism. Thisenablesanissue-based systemtobeincremen tallyextended
tohandledialogue phenomena involvingmorecomplex semantics.
2.12.7Questions vs.knowledgepreconditions
Intraditional workondialogue intheplanning/plan-recognition paradigm, questions are
notrepresenteddirectlyasindependentobjects;insteadtheyareembeddedinrepresenta-
tionsofgoal-states.
Anexample isAllen(1987). Here,therearetwomaintypesofgoal-states relevantto
questions: toknowifapropositionholds,andtoknowareferentofwhichaproposition
holds.Thesecorrespondtoy/n-questions andwh-questions, respectively.Wecancallsuch
goalsinformation-goals, orinfo-goals. Typically,anagentaskingaquestion ismotivated
bywantingtoachieveaninfo-goal.
²knowif(A;p):Aknowswhether p
²knowref(A;x;p(x)):AknowsanxsuchthatP(x)holds
InAllen(1987),speechactscontainingquestions areanalyzed asrequests toinformthe
speakerofwhether apropositionholds(inform-if, correspondingtoaknowifgoalstate)
orofareferentsuchthatapropositionholdsofit(inform-ref, correspondingtoaknowref
goalstate).
(2.24)A:Wheredoyouwanttogo?
REQUEST( A,B,INFORM-REF( B,A,x,dest-city(x)))
Whilethisisclearlyanimprovementovertheframe-based approach,itstilldoesnotadmit
questions as¯rst-class semanticalobjects.Amuchsimpleranalysis oftheabovedialogue
wouldseemtobe

2.13. SUMMAR Y 73
(2.25)A:Wheredoyouwanttogo?
ASK(A,B,?x:dest-city(x)))
Also,ofcourse,theplan-based approachtoquestions moreorlesspresupposesthewhole
frameworkofplanning andplanrecognition withitsassociatedproblem ofcomplexit y.
Itappearsthatthereareinfacttwoseparate issueshere:thesemanticcontentofquestions,
andtheclassi¯cation ofutterances involvingquestions intermsofdialogue movetype.In
principle, itwouldbepossibletocombineananalysis ofquestions as¯rst-class semantic
objectswithananalysis ofquestion-mo vesasrequests involvingsuchobjects,e.g.asin
(2.26).
(2.26)A:Wheredoyouwanttogo?
REQUEST( A,B,RESPOND( B,?x:dest-city(x)))
Embeddingthisananalysisofutterances conveyingquestions inaframeworksuchasthat
describedinthischapterwouldallowtheuseofanswerhoodconditions inthesameway
wehavedone.However,onouranalysisask-moveshavethee®ectofupdatingQUDina
speci¯cway.Whenweintroducerequest-movesinChapter 5,wewillseethatwhilethere
areimportantsimilarities betweenrequestandaskmoves,requests donothavethesame
updatee®ectsontheinformation stateasquestions do.Sinceonourapproachupdate
e®ectsofutterances aredetermined bydialogue movetype,thisisanargumen tforkeeping
thesetwomovetypesseparate.
Although wewillnotdealmuchwithissuesinvolvedinplanning andplanrecognition, we
wanttostressthatthereisnoreasonwhytheissue-based approachcouldnotbefruitfully
combinedwithmechanisms forplanning andplanrecognition. Infact,inChapter 4we
willimplemen taverybasicformofplanrecognition.
2.13Summary
Inthischapter,wehavelaidthegroundw orkforfurtherexplorations ofissue-based dialogue
managemen tanditsimplemen tationintheIBiSsystem. Asastarting pointweused
Ginzburg's conceptofQuestions UnderDiscussion ,andweexplored theuseofQUDas
thebasisforthedialogue managemen t(Dialogue MoveEngine) componentofadialogue
system. ThebasicusesofQUDistomodelraisingandaddressing issuesindialogue,
including theresolution ofelliptical answers.Also,dialogue plansandasimplesemantics
wereintroducedandimplemen ted.

74 CHAPTER 2.BASIC ISSUE-BASED DIALOGUE MANA GEMENT

Chapter 3
Grounding issues
3.1Introduction
Intheprevious chapter,weassumed \perfectcommunication" inthesensethatallut-
terances wereassumed tobecorrectly perceivedandundersto od,andfullyaccepted. Of
course,theseassumptions areunrealistic bothinhuman-humanandhuman-computer con-
versation. Ausefuldialogue systemneedstobeabletodealwithcasesofmiscomm unica-
tionandrejections.
Wewillnotattempt togiveacomplete computational theoryaboutthegrounding process
inhuman-humandialogue. Rather,wewillprovideabasicissue-based account,in°uenced
byGinzburg, whichtriestocoverthemainphenomena thatadialogue systemneeds
tobeabletohandle. Forinstance, thefactthatspeechrecognition ismuchharderfor
machinesthanforhumansmaymotivatedi®erentgrounding strategies forhandling system
utterances thanforhandling userutterances.
First,weprovidesomedialogue examples wherevariouskindsoffeedbackareused.We
thenreviewanddiscusssomerelevantbackground, anddiscussgeneraltypesandfeatures
offeedbackasitappearsinhuman-humandialogue. Next,wediscusstheconcept of
grounding fromaninformation updatepointofview,andintroducetheconcepts ofopti-
mistic,cautious andpessimistic grounding strategies. Thisisfollowedbythemainsection
ofthischapter,wherewerelategrounding andfeedbacktodialogue systems, discussthe
implemen tationofissue-based grounding andfeedbackinIBiS2,andprovidedialogue ex-
amplesshowingthesystem's behaviourandhowitrelatestointernalupdates.Wethen
reviewadditional implemen tationissues,andprovidea¯naldiscussion.
75

76 CHAPTER 3.GROUNDING ISSUES
3.1.1Dialogue examples
Thehuman-humandialogue excerpt1in(3.1)showstwocommon kindsoffeedback.J's
\mm"showsthatJ(thinksthathe)understo odP'sprevious utterance; P's\pardon"
showsthatPwasnotabletohearJ'sprevious utterance. Theexample alsoincludes a
hesitation sound(\um")fromJ.(Pisacustomer andJatravelagent.)
(3.1)P:Äom(.)°ygtiparis
um(.)°ighttoparis
J:mm(.)skaduhaenreturbiljett
mm(.)doyouwantareturnticket
P:vasadu
pardon
J:skaduhaenturºaretur
doyouwantaroundtrip
Thefeedbackin(3.1)consisted ofconventionalized feedbackwords(\mm", \pardon").
However,feedbackmayalsobemoreexplicitandrepeatthecentralcontentoftheprevious
utterance, asK'ssecondfeedbackutterance in(3.2).
(3.2)B:jaskavaframmei[1gÄoteborg]1eeungefÄarvinietiden om
de¯nnsnºatidit[2morgon°yg ]2
IneedtobeinGothenbur gereraroundnineifthereisanearly
morning °ight
K:[1m]1
m
K:[2vi]2nietiden mviskase
Aroundninemlet'ssee
Thefunction ofanutterance answeringaquestion isnotprimarily togivefeedback,but
rathertoprovidetask-related information. However,anansweralsoshowsthatthepre-
viousquestion wasundersto odandintegrated. Example (3.3)showsthatfeedbackis
sometimes giveninreaction toaquestion beforethequestion isanswered.
(3.3)J:senmºasteduhaesºandÄarintenationellt studentkortocksºa
hadude
thenyouneedoneofthoseinternational studentcardsdoyou
havethat
P:mmnÄa
mmno
1Exceptwherenoted,thehuman-humandialogues inthischapterhavebeencollected bytheUniversity
ofLundaspartoftheSDSproject.Wequotetranscriptions doneinGÄoteborgaspartofthesameproject.
The(.)symbolindicates apause.

3.1.INTR ODUCTION 77
However,oftenhuman-humancommunication proceedswithoutexplicitfeedback,asinthe
excerptfromatelephone dialogue in(3.4).
(3.4)K:vartskaduºaka
whereareyougoing
B:ejagskaºakatillgÄoteborg
eri'mgoingtogothenbur g
K:vilketdatum
whatdate
B:densjÄattejuni
thesixthofjune
K:villduºakame°ygellermetºag
doyouwantto°yortakethetrain
Bycontrast,incurrentcommercial systems itiscommon tocheckthesystem's interpre-
tationofrecognized userinputaskingay/n-question, asseeninthe(invented)dialogue
in(3.5).Thisbehaviourismuchlesscommon inhuman-humandialogue, butmayoccur
innoisyenvironmen tsorwhencommunicating overanunreliable communication channel
(e.g.whenusingamobilephoneonatrain).
(3.5)S:Whatdaydoyouwishtotravel?
U:Friday
S:Fridaythe5thofApril,isthatcorrect?
Asimilarbutnotidenticalbehaviourdoesoccurinhuman-humandialogue, asin(3.6),
takenfromtheLondon-Lund corpusandusedbyClarkinClarkandSchaefer(1989a). In
thisexample, BgivesandexplicitreportofhowA'sutterance wasinterpreted, whereupon
Acon¯rms thattheinterpretation iscorrectbysaying\yes".
(3.6)A:F.sixtwo
B:Fsixtwo
A:yes
B:thanksverymuch
Thedialogue in(dialogue 3.1)givesanimpression ofwhatfeedbackcapabilities weaim
toaddtoIBiSinthischapter.
(dialogue 3.1)
S>Welcome tothetravelagency!

78 CHAPTER 3.GROUNDING ISSUES
S>hello
U>priceinformation please
S>Youaskedaboutprice. Howdoyouwanttotravel?
U>pardon
S>Howdoyouwanttotravel?
U>byplane
S>Byplane,isthatcorrect?
U>yes
S>Okay.Whatcitydoyouwanttogoto?
U>lododo
S>Pardon?
U>london
S>Okay,tolondon. Whatcitydoyouwanttogofrom?
U>lyons
S>Sorry,Lyonsisnotinthedatabase. So,Whatcitydoyouwanttogo
from?
U>paris
...
U>Whataboutconnecting flights?
S>Youaskedaboutconnecting flights. Sorry,Icannotanswerthat.
3.2Background
Inthissection,weprovideabriefoverviewandofsomeprevious accountsofgrounding
andfeedback.
3.2.1Clark:Addingtothecommon ground
ClarkandSchaefer(1989a)describegrounding astheprocessofaddingtothecommon
ground(seeSection2.2.2).Theyalsoformulatethegroundingcriterion :
Grounding criterion: Thecontributor andthepartners mutuallybelievethat
thepartners haveundersto odwhatthecontributor meant,toacriterion su±-
cientforcurrentpurposes.(ClarkandSchaefer,1989a,p.148)
Toachievethis,eachgrounding processgoesthrough twophases:

3.2.BACKGROUND 79
²Presentationphase:Apresentsutterance uforBtoconsider. Hedoessoonthe
assumption that,ifBgivesevidence eorstronger, hecanbelievethatBunderstands
whatAmeansbyu.
²Acceptance phase.Bacceptsutterance ubygivingevidence e0thathebelieves
heunderstands whatAmeansbyu.Hedoessoontheassumption that,onceA
registers evidence e0,hewillalsobelievethatBunderstands. (ClarkandSchaefer,
1989a,p.151)
Clark(1996)arguesthatutterances involveactionson(atleast)fourdi®erentlevels:
(3.7)LevelSpeakerA'sactions Addressee B'sactions
4AisproposingajointprojectwtoBBisconsidering A's
proposalofw
3Aissignalling thatpforB Bisrecognizing thatp
2AispresentingsignalstoB Bisidentifyings
1Aisexecuting behaviourtforB Bisattending tot
Examples ofjointprojectsareadjacency pairs,e.g.oneDPaskingaquestion andtheother
answeringit.According toClark,thesefourlevelsofactionconstitute anactionladder,
andassuchitissubjecttotheprinciple ofdownwardevidence:\Inaladderofactions,
evidence thatoneleveliscomplete isalsoevidence thatalllevelsbelowitarecomplete".
Forexample, ifHunderstands u,HmustalsohaveperceiveduandHandSmusthave
established contact;however,Hmaynotacceptu.
InClarkandSchaefer(1989a), itisunclearwhether grounding includes theproposal/
consideration levelinaddition tounderstanding2.However,inClark(1996),grounding
isrede¯ned toincludealllevelsofaction,i.e.attention,identi¯cation, recognition and
consideration.
Togroundathing(:::)istoestablish itaspartofcommongroundwellenough
forcurrentpurposes.(:::)Onthishypothesis,grounding shouldoccuratall
levelsofcommunication. (Clark,1996,p.221,italicsinoriginal)
Wewilladoptthisgeneraluseofthetermgrounding toincludeallfouractionlevels.Also,
weassumethattheacceptance phase(potentially)concerns allfouractionlevels,rather
thanonlyunderstanding3.
2Thede¯nition suggests onlyunderstanding isinvolved,butsomeexamples indicate thatutterances
whicharerejected becauseofbeinginappropriate arenotgrounded.
3Theterm\acceptance phase"isabitunfortunate, since\acceptance" isusedbye.g.Ginzburg to
designate theproposal-consideration actionlevel.

80 CHAPTER 3.GROUNDING ISSUES
Clarklists¯vewaystosignalthatacontribution hasbeensuccessfully interpreted and
accepted, orderedfromweakesttostrongest:
²Continuedattention
²Relevantnextcontribution
²Acknowledgemen t:\uh-huh",nodding,etc.
²Demonstration: reformulation,collaborativecompletion
²Display:verbatimdisplayofpresentation
Thepresentationandacceptance phasesbothfocusonexternally observablecommunicative
behaviour.However,correspondingtopresentationsbyaspeakeroneachlevelofaction
thereisalsoan\internal"actioncarriedoutbytheaddressee.
Clarkviewstheproposal-consideration processintermsofnegotiation, whereanutter-
ancesuchasanassertion oraquestion isseenasaproposalforajointproject,followed
byaresponsetothisproposal.ClarkfollowsGo®man (1976)andStenstrÄom(1984)in
distinguishing fourmaintypesofresponsestoproposalsofjointprojects:
1.fullcompliance, e.g.answeringaquestion [acceptance]
2.alteration ofproject,whereHalterstheproposedprojecttosomething heiswilling
tocomplywith;Clarkassertsthatalterations maybecooperative(inwhichcasethe
alteredprojectisstillrelevanttotheoriginalone)oruncooperative[alteration]
3.declination ofproject,whereHisunableorunwillingtocomplywiththeprojectas
proposed.Declinations areoftenperformed byo®eringareasonorjusti¯cation for
declining theproposal.Clarkgivestheresponse\Idon'tknow"toaquestion asan
example ofdeclination. [rejection]
4.withdrawalfromproject,whereHwithdrawsfromconsidering theproposal,e.g.by
deliberatelyignoring aquestion andchanging thetopic[withdrawal]
3.2.2Ginzburg: QUD-based utterance processingprotocols
Ginzburg o®ersanissue-based modelofgrounding ontheunderstanding andacceptance
levelsbypositingtwokindsofgrounding-related questions: meaning-questions andaccep-
tancequestions4.IfAproducesutterance u,Bisfacedwithameaning-question, roughly
4Thelattertermisours.ItreferstoGinzburg's MAX-QUD questions discussed below.

3.2.BACKGROUND 81
\Whatdoesumean?". IfBcannot¯ndananswertothisquestion, Bshouldproduce
anutterance identicalorrelatedtothemeaning-question, e.g.\Whatdoyoumean?". If
Bmanages to¯ndananswertothisquestion, heproceedstoconsider theacceptance-
question, roughly\Should ubeaccepted?".
Ginzburg's utterance processingprotocol(pt.1)Ginzburg formulateshistheory
intermsofanutterance processingprotocol.Assuming theotherDPAhasuttered u,this
isroughlywhathappensinthe¯rstpartoftheprotocol:
Bisfacedwiththecontent-question qcontent(u),whichweformalize as?x.content(u;x),
paraphrasable roughlyas\Whatdoesumean(giventhecurrentcontext)?". Toanswer
thisquestion, Bmustbeabletoprovideacontextualinterpretation cofu.Thisinvolves,
amongotherthings,¯ndingreferentsforNPs.IfBisnotabletoanswerqcontent(u),B
placesqcontent(u)onQUDandproducesaqcontent(u)-speci¯cutterance, e.g.arequestfor
clari¯cation. Onceananswertoqcontent(u)hasbeenfound,Bcanbesaidtohavean
understanding ofu(whichmay,ofcourse,beamisunderstanding).
Ginzburg notesthatutterances behavedi®erentlywithregardtoacceptance dependingon
whether theyhavepropositionsorquestions ascontent.Apropositionpcanbeaccepted in
twoways:asafactorasatopic(issue)ofdiscussion. Inthelattercase,thequestion under
discussion is,roughly,whether pshouldbeaccepted asafact(atleastforthepurposes
ofcurrentdiscussion) ornot.Accepting apropositionentailsaccepting italsoasanissue
fordiscussion (although the\discussion" inthiscasewillconsistonlyoftheacceptance of
pasafact).Theexchangesin(3.8)showsomeexamples ofreactions toassertions (note
thattheseexamples arenotGinzburg's).
(3.8)a.A:Thetrainleavesat10a.m.[answer/assert p]
B:OK,thanks.[accept p]
b.A:Thetrainleavesat10a.m.[answer/assert p]
B:Noitdoesn't![rejectp,accept?pfordiscussion]
c.A:Thetrainleavesat10a.m.[answer/assert p]
B:I'dprefernottodiscussthisrightnow[reject?pfordis-
cussion]
d.A:Thetrainleavesat10a.m.[answer/assert p]
B:Niceweather,isn'tit[ignore p]
Questions, bycontrast,canonlybeaccepted asissuesfordiscussion. However,accepting q
doesnotnecessarily resultinansweringq.Onthisaccount,answeringqshouldbeviewed
asonepossiblewayofdisplayinginternalacceptance ofq;however,contrarytoClarkwe
alsoallowthepossibilityofdisplayingacceptance ofqwithoutansweringq.

82 CHAPTER 3.GROUNDING ISSUES
(3.9)a.A:Wheredoyouwanttogo[askq]
B:Paris[answerq,implicitly acceptq]
b.A:Wheredoyouwanttogo[askq]
B:Hmmm, goodquestion... Doyouhaveanyrecommenda-
tions?[explicitly acceptq]
c.A:Wheredoyouwanttogo[askq]
B:That'snoneofyourbusiness [explicitly rejectqbecause
ofunwillingness]
d.A:Wheredoyouwanttogo[askq]
B:Idon'tknow[explicitly rejectqbecauseofinability]
e.A:Wheredoyouwanttogo[askq]
B:I'dliketotravelinApril[ignoreq,answerotherquestion]
f.A:Wheredoyouwanttogo[askq]
B:Doyouhaveastudentdiscount?[ignoreq,askother
question]
Ginzburg's utterance processingprotocol,pt.2AswesawaboveinSection3.2.2,
according toGinzburg's utterance processingprotocol,foraDPBtounderstand anut-
terance uamountsto¯ndingananswertothecontent-question qc.
OnceBisableto¯ndananswercwhichresolves?x.content(u;x),Bisfacedwiththe
question qaccept(c)ofwhether ornottoacceptcfordiscussion, formalized byGinzburg
as?MAX-QUD( c)(\Whether cshouldbecomeQUD-maximal"5).Atthispoint,the
protocolisdi®erentforquestions andpropositions(\facts"). Ifcisaquestion andB
answersqaccept(c)negatively(rejects cfordiscussion), BpushesconQUDandproducesan
c-speci¯cutterance (e.g.\Idon'twanttodiscussthat").Ifqaccept(c)isansweredpositively
andBaccepts c,cwillbeaddedtoQUDandBwillproduceac-speci¯cutterance, e.g.
ananswertothequestion c.
IfcinsteadisapropositionandifBanswersqaccept(c)negativelyBshouldpushqaccept(c)
onQUDandproduceaqaccept(c)-speci¯cutterance. Butifqaccept(c)isansweredpositively,
Bmustnowconsider thequestion whether c,i.e.?c.Iftheanswerisnegative(i.e.B
doesnotacceptc),thecorrespondingy/n-question ?cispushedonQUD.Thisamounts
toaccepting ?cfordiscussion, whichisnotthesameasaccepting c.IfBanswersqaccept(c)
positively,BshouldaddctoherFACTS.
5Thismeansthatthearguably moreintuitiveinterpretation of?MAX-QUD( c)as\whethercismaximal
onQUD"iswrong.

3.2.BACKGROUND 83
Forclarity,wereproducethefullprotocolinamoreschematic way:
tryto¯ndananswerresolving qcontent(u)=?x.content(u,x)
²noanswerfound!pushqcontent(u)onQUD,produceqcontent(u)-speci¯cutterance
²answercfound!
{cisaquestion!consider qaccept(c)=?MAX-QUD( c)
¤decideon\no"!pushqaccept(c)onQUD,produceqaccept(c)-speci¯cutter-
ance[rejectc]
¤decideon\yes"!pushconQUD,producec-speci¯cutterance [accept c]
{cisaproposition!consider qaccept(?c)
¤no!pushqaccept(?c)onQUD,produceqaccept(?c)-speci¯cutterance [reject
?castopicfordiscussion]
¤yes!consider ?c[accept?castopicfordiscussion]
¢no!push?conQUD,produce?c-speci¯cutterance [rejectcasfact]
¢yes!addctoFACTS[accept casfact]
Notethatthereareanumberofdecisions thatneedtobemadebyB,andforeachofthese
decisions thereisthepossibilityofrejecting uonthecorrespondinglevel.Foraquestion,
thereisonlyonewayofrejecting it(oncethecontentquestion hasbeenresolved):toreject
itasaquestion underdiscussion. Thisamountstorefusing todiscussthequestion. For
aproposition p,therearetwodi®erentwaysofrejecting it.Firstly,onemayrejectthe
issue\whether p"completely; thisamountstorefusingtodiscusswhether pistrueornot.
Alternativ ely,onemayaccept\whether p"fordiscussion butrejectpasafact.
3.2.3Allwood:InteractiveCommunication Managemen t
Allwood(1995)usestheconceptof\InteractiveCommunication Managemen t"todesignate
allcommunication dealingwiththemanagemen tofdialogue interaction. Thisincludes
feedbackbutalsosequencing andturnmanagement .Sequencing \concerns themecha-
nisms,wherebyadialogue isstructured intosequences, subactivities, topicsetc....".
Here,wewillusethetermICMasageneraltermforcoordination ofthecommon ground,
whichinaninformation stateupdateapproachcomestomeanexplicitsignalsenabling
coordination ofupdatestothecommon ground. Whilefeedbackisassociatedwithspeci¯c
utterances, ICMingeneraldoesnotneedtoconcernanyspeci¯cutterance.

84 CHAPTER 3.GROUNDING ISSUES
Aswillbeseenbelow,wewillalsobemakinguseofvariousotherpartsofAllwood's
\activity-basedpragmatics" (Allwood,1995),including Allwood'sactionlevelterminol-
ogy,theconcept ofOwnCommunication Managemen t(OCM), andvariousdistinctions
concerning ICM.
3.3Preliminary discussion
Intheprevious sectionwehaveseenexamples ofdi®erentwaysofaccountingforgrounding
andfeedback.Wefeelthattheyallo®erusefulinsights,andthattheytogether canserve
asabasisforourfurtherexplorations.
Therefore, inthissectionwewilldiscusstheaccountspresentedinSection3.2,relatethem
toeachother,andestablish somebasicprinciples andterminological conventions.
3.3.1Levelsofactionindialogue
BothAllwood(1995)andClark(1996)distinguish fourlevelsofactioninvolvedincom-
munication (Sisthespeakerofutterance u,Histhehearer/addressee). Theyuseslightly
di®erentterminologies; hereweuseAllwood'sterminology andaddClark's(and,forthe
reaction level,alsoGinzburg's) correspondingtermsinparenthesis.Thede¯nitions are
mainlyderivedfromAllwood.
²Reaction (acceptance, consideration): whether Hhasintegrated (thecontentof)u
²Understanding (recognition): whether Hunderstands u
²Perception (identi¯cation): whether Hperceivesu
²Contact(attention):whether HandShavecontact,i.e.iftheyhaveestablished a
channelofcommunication
Theselevelsofactionareinvolvedinalldialogue, andtotheextentthatcontact,per-
ception, understanding andacceptance canbesaidtobenegotiated, allhuman-human
dialogue hasanelementofnegotiation builtin.Notethattheabovelistoflevelsisformu-
latedintermsofthehearer'sperspective.
Giventhatgrounding isconcerned withalllevels,itfollowsthatfouraspectsofanutterance
uinadialogue betweenHandScaninprinciple berepresentedinthecommon ground,
oneforeachactionlevel:

3.3.PRELIMINAR YDISCUSSION 85
²whether uhasbeenintegrated (takenup,accepted)
²whether uhasbeenundersto od
²whether uhasbeenperceived
²whether SandHhavecontact
Also,grounding-related feedbackmayconcernany(andpossiblyseveral)oftheselevels.
Thelevelreferredtoasreaction/acceptance/consideration inthelistaboveisde¯neddif-
ferentlybydi®erentauthors. Allwoodcallsit\reaction (tomainevocativeintention)",
Ginzburg talksabout\acceptance", andClarkusestheterm\consideration (ofjoint
project)".Perhapsitcouldbearguedthatthesedi®erentde¯nitions arenotconcerned
withtheexactsamephenomena. Sincewewanttousethedistinction ratherthandebate
it,wechoosetoemphasize thesimilarities ratherthanthedi®erences.
3.3.2Reaction levelfeedback
Onceanutterance hasbeenundersto od(orisbelievedtobeundersto od),inthesensethat
thehearerhasinterpreted theutterance tohaveameaning andpurposewhichisrelevant
intheactivity(asperceivedbythehearer), thehearermustdecidewhattodowiththe
utterance. Shouldhee.g.trytoanswerthequestion thatwasasked,orrefuse?Shouldhe
choosetocommittoanasserted proposition,orraiseobjections?
Thereaction processwhichfollowstheunderstanding ofamoveMcanbeanalytically
dividedintothreesubsteps:
²consideration: whether ornottoacceptandintegrate M(andconsequen tly(tryto)
actontheevocativeintention)
²integration: updatingthecommon groundaccording toM
²feedback:signalling theresultsofconsideration ofM
Thedivisionofthereaction phaseintoconsideration andfeedbackisalsomadeinAllwood
(1995),usingtheterms\evaluation" and\report"(respectively),and(thoughperhapsnot
soexplicitly) inClark(1996).However,theintegration stepisnot(atleastnotexplicitly)
included ineitheroftheseaccounts.

86 CHAPTER 3.GROUNDING ISSUES
Intheconsideration phase,theDPinvestigates whether hecanandwantstoacceptthe
proposedjointprojectornot.Ifnot,heneedstodecidewhether toalter,decline,orignore
theproposal.
Wewillusethetermintegrationforthesilent(internal)consequence ofdeciding toaccept
(comply with)aproposedjointproject,modelledastheprocessofupdatingone'sview
ofthecommon groundwiththefulle®ectsofaperformed move.By\thefulle®ects"we
meane.g.takingapropositiontobetrue(atleastforthepurposesoftheconversation)
ortakingaquestion asbeingunderdiscussion. InrelationtoClark'suseof\uptake",we
wouldsaythatuptakesignalsintegration. (Ofcourse,uptakemaybemorethanmerely
asignalthataprevious utterance hasbeenintegrated, e.g.inthecaseofansweringa
question.)
Inthefeedbackphase,theresultsoftheconsideration process(acceptance orrejection of
issueorproposition)aresignalled. Thepossibilityofsilentacceptance meansthatthe
feedbackphaseisoptional.
Issueandfactacceptance Extending Clark'sterminology ,wecancalltheacceptance
ofapropositionorquestion asatopicfordiscussion issueacceptance,andtheacceptance
ofapropositionasafactfactacceptance.(Wewillalsousethetermpropositionaccep-
tanceforthelatter).Theformerkindofacceptance isavailablebothforquestions and
propositions, whilethelatterisavailableonlyforpropositions. Correspondingly,wecan
makeadistinction betweenissuerejection andfactrejection inthecaseofpropositions.
Reasonsforutterance rejection Ifaquestion isaskedandtheaddressee DPdecides
nottoacceptit(explicitly orimplicitly), thismaybeexplained inatleasttwoways:
²unwillingness: DPdoesnotwanttodiscusstheissue,e.g.becauseDPbelievesother
information ismoreimportantatthemoment
²inability:DPisnotabletodiscusstheissue,e.g.becauseofcon¯dentialityorlack
ofknowledge
Regarding theupdatee®ectsofdeclining aquestion, thereseemstobeanimportant
di®erence betweenbeingunabletoansweraquestion (ase.g.inthecasewheretheresponse
is\Idon'tknow"),andbeingunwillingtoanswerit.Intheformercase,itisnotclearthat
thequestion isactually rejected asatopicfordiscussion. Theaddressee ofthequestion
maythinkthathemighteventuallycomeupwithananswer(asaresultofnewinformation
orinference); inthiscase\Idon'tknow"canbeinterpreted as\Idon'tknowrightnow,but

3.3.PRELIMINAR YDISCUSSION 87
I'llkeepthequestion inmind".Inthiscase,thequestion mightnothavetobeexplicitly
raisedagainbeforebeingrespondedto.
Inthecasewheretherejection displaysunwillingness toanswerthequestion (e.g.\No
comment",\Iwillnotanswerthat",\That'snoneofyourbusiness"), itismuchclearer
thatthequestion isactually rejected asatopicfordiscussion.
Thereisalsoadi®erence betweenquestions andpropositionsregarding thereasonsfor
rejection. AsGinzburg notes,asserted propositionsmayberejectedasissuesfordiscussion,
butevenifaccepted asissuestheymayberejected asfacts.Soforpropositions, the
consideration phaseismorecomplex thanforquestions, potentiallyinvolvingtwodecisions
(e.g.rejecting theasserted propositionasafact,butaccepting itasanissue).
Rejecting apropositionasanissuecanbeexplained bythesamekindsofreasonsasfor
anyissue.Rejecting apropositionasafactmaybecausede.g.bytheaddressee having
acon°icting belief,ornottrusting thespeaker.Itmayalsobeexplained byabeliefthat
accepting thepropositionwillnotservethegoalsoftheDPs,ase.g.ifacustomer in
atravelagencyassertsthatthedestination cityofher°ightisKualaLumpur, whenin
facttheagencyonlyservesdestinations inEurope.Ofcourse,thepropositionthatthe
customer wantstotraveltoKualaLumpur canhardlyberejected bytheclerk;however,
thepropositionthatKualaLumpur isthedestination cityofatripthattheclerkwill
provideinformation aboutcanberejected. Thiskindofexample isespeciallyrelevantfor
database searchsystems, whereinformation abouttheuser'sdesiresandintentionsisnot
storedassuch.
3.3.3Levelsofunderstanding
Concerning thelevelsofactiondescribedinSection3.2.1,wecanmakefurtherdistinctions
betweendi®erentlevelsofunderstanding, correspondingtothreelevelsofmeaning. These
sublevelsgivea¯nergradingtothelevelofunderstanding. (Asimilardistinction isalso
usedbyGinzburg (forth)).
²domain-dep endentanddiscourse-dep endentmeaning (roughly,\content"intheter-
minology ofBarwise andPerry,1983andKaplan, 1979)
{referentialmeaning ,e.g.referentsofpronouns, temporalexpressions
{pragmatic: therelevanceofuinthecurrentcontext
²discourse-indep endent(butpossiblydomain-dep endent)meaning (roughly correspond-
ingto\meaning" intheterminology ofBarwise andPerry,1983andKaplan, 1979),
e.g.staticwordmeanings

88 CHAPTER 3.GROUNDING ISSUES
By\discourse-indep endent"wemean\independentofthedynamic dialogue context"
(modelledinIBiSbytheinformation stateproper).However,discourse-indep endentmean-
ingmaystillbedependentonstaticaspectsoftheactivity/domain. Itisobviousthatthese
levelsofmeaning areintertwinedanddonothaveperfectlyclearboundaries. Nevertheless,
webelievetheyareusefulasanalytical approximations.
Sincedialogue systemsusuallyoperateinlimiteddomains, wewillassumethatwedonot
havetodealwithambiguities whichareresolvedbystaticknowledgerelatedtothedomain.
Forexample, adialogue systemforaccessing bankaccountsdoesnothavetoknowthat
\bank"mayalsorefertothebankofariver;itissimplyveryunlikely(though ofcourse
notimpossible)thatthewordwillbeusedwiththismeaning intheactivity.Itcanbe
arguedwhether thisisalwaysagoodstrategy,butfornowweacceptthisasareasonable
simpli¯cation.
3.3.4SomecommentsonGinzburg's protocol
The¯rstthingtonoteaboutGinzburg's grounding protocolisthatitdoesnotspecify
exactlywhatkindoffeedbackshouldbeproduced.Thenotionofquestion-sp eci¯city(see
Section2.8.2)isaminimal requiremen tthatneedstobesupplemen tedwithadditional
heuristics todecideonexactlywhatfeedbacktoprovide.Also,itdoesnotspecifyhow
aDPdecideswhenasatisfactory interpretation hasbeenfound,orhowtoresolvethe
content-andacceptance questions. Theseareallthingsweneedtobespeci¯caboutwhen
implemen tingadialogue system. (Ofcourse,totheextenttheyaredomain-dep endent,
wewouldnotexpectto¯ndtheminageneraltheoryofdialogue. Whether theyare
domain-dep endentornotis,onourview,anopenquestion.)
Second,Ginzburg seemstoassumeacertaindegreeoffreedom concerning thesharedness
ofQUD.According tothegrounding protocol,DPsarefreetoaddagrounding-related
question qtoQUDwithoutinforming theotherDP(s),providedthisisfollowedbyanut-
terancespeci¯ctotheaddedquestion. Infact,themechanismofquestion accommo dation
thatwillbepresentedinChapter 4providesanexplanation ofhowDPscanunderstand
answerstounaskedquestions. However,itisnotclearthatthisshouldallowthespeaker
tomodifyQUDbeforeuttering theq-speci¯cutterance. Itseemsinconsisten ttosaythat
aDPthatassumes QUDissharedcanmodifyQUDwithouthavinggivenanyindication
ofthistotheotherDP;howwouldtheotherDPbeabletoknowaboutthismodi¯cation
beforetheq-speci¯cutterance hasbeenmade?SoitappearsthatGinzburg hasanotion
ofQUDasnotnecessarily entirelyshared,andthisisslightlydi®erentfromthenotionof
QUDweareusing.(SeealsoSection4.8.5.)
Third,Ginzburg onlydealswithunderstanding andacceptance; contactandperception
areleftout.Sotheprotocolabovedoesnotdealexplicitly withcaseswhereaDPisunsure

3.4.FEEDBA CKAND RELA TED BEHA VIOUR INHUMAN-HUMAN DIALOGUE 89
whichwordswereuttered(however,itdealswithperception indirectly sinceunderstanding
isbasedonperception).
RelationbetweenClark'sandGinzburg's accounts
Itseemspossibletodrawsomeparallels betweenthetwoaccountsreviewedabove.Clark's
\recognition ofmeaning" wouldpresumably bemodelledbyGinzburg as¯ndingananswer
tothecontent-question. Similarly ,Clark's\consideration ofproposal"ismodelledas
consideration oftheacceptance question.
Clarktalksaboutjointprojectsin\track2"(meta-comm unication, asopposedto\track
1",fortask-levelcommunication) asinvolvingspeakers(oftenimplicitly) raisingvarious
issuesrelatedtogrounding, e.g.\Doyouunderstand this?",andtheresponderanswering
theseissues(oftenimplicitly). This¯tswellwiththeissue-based approachproposedby
Ginzburg.
OnClark'saccount,thereisnoasymmetry betweenquestions andpropositionsconcern-
ingacceptance. Thequestion-related counterpartofaccepting apropositionasafact,
according toClark,isansweringthequestion. However,itcanbearguedthatanswering
thequestion ismerelyanexternal behaviourcausedby(andactingaspositivefeedback
concerning) theactualacceptance ofthequestion asanissue.Clark'squestion-related
counterpartofrejecting apropositionasafact(declination )isansweringe.g.\Idon't
know"(Clark,1996,p.204),andtherebysignalling lackofabilityorwillingness to\com-
plywiththeprojectasproposed".Presumably ,\Nocomment"or\Irefusetoanswer
thatquestion" wouldalsocountasrejections onthesamelevel,whichindicates thatthey
arereallyissue-rejections. The\withdra wal"thatClarktalksabout,wheretheaddressee
deliberatelyignoresaproposal,seemstobeequallyapplicable tobothassertions andques-
tions.(Infact,Lewin(2000)viewscaseswhereaDPanswersadi®erentquestion thanthe
onethatwasasked,therebywithdrawingfromtheproposedquestion, asrejections.)
3.4Feedbackandrelatedbehaviourinhuman-human
dialogue
Byfeedbackwemeanbehaviourwhoseprimaryfunction istodealwithgrounding ofutter-
ancesindialogue6.Thisdistinguishes feedbackfrombehaviourwhoseprimary function is
relatedtothedomain-lev eltaskathand,e.g.gettingpriceinformation. Non-feedbac kbe-
6Sincethisthesisisnotconcerned withmultimodaldialogue, wewillonlydiscussverbalfeedback.

90 CHAPTER 3.GROUNDING ISSUES
haviourinthissenseincludesaskingandansweringtask-levelquestions, givinginstructions,
etc.(cf.the\CoreSpeechActs"ofPoesioandTraum,1998).Answeringadomain-lev el
question (e.g.saying\Paris"inresponseto\Whatcitydoyouwanttogoto?")certainly
involvesaspectsofgrounding andacceptance, sinceitshowsthatthequestion wasunder-
stoodandaccepted. However,theprimary function ofadomain-lev elansweristoresolve
thequestion, nottoshowthatitwasundersto odandaccepted.
Asingleutterance mayincludebothfeedbackanddomain-lev elinformation. Clarktalks
aboutcommunication ofthesetwotypesofinformation asbelonging todi®erent\tracks":
domain-lev elinformation isontrack1whilefeedback,andgrounding-related communica-
tioningeneral,isontrack2.
Inthissectionwewillattempt togiveanoverviewofvariousaspectsoffeedback.Wewill
returntosequencing ICMinSection3.6.9.
3.4.1Classifying explicitfeedback
Togetanoverviewoftherangeofexplicitfeedbackbehaviourthatexistsinhuman-human
dialogue, wewillclassifyfeedbackaccording tofourcriteria. WewillassumethatDPS
hasjustutteredorisuttering utoDPH,whenthefeedbackutterance f(uttered byH
toS)occurs.
²levelofaction/basiccommunicativefunction (contact,perception, understanding,
reaction /acceptance)
²polarity(positive/negative):whether findicates contact/perception /under-
standing /acceptance orlackthereof
²eliciting /non-eliciting: whether fisintendedtoevokearesponse(e.g.areformu-
lationorareasontoacceptsomecontent)
²formoff:singleword,repetitionetc.
²contentoff:object-levelormeta-level
Theactionlevelcriterion hasbeenexplained above;theotherswillbeexplained presently.
Thecriteriaofbasiccommunicativefunction, polarity,eliciting/non-eliciting, andsurface
formareallderivedfromAllwoodetal.(1992)andAllwood(1995).

3.4.FEEDBA CKAND RELA TED BEHA VIOUR INHUMAN-HUMAN DIALOGUE 91
3.4.2Positive,negative,andneutralfeedback
Positivefeedbackindicates oneorseveralofcontact,perception, understanding, andinte-
gration,whilenegativefeedbackindicates lackthereof.
Whilethereareclearcasesofpositive(\uhuh",\ok")andnegative(\pardon?", \Idon't
understand") feedback,therearealsosomecaseswhicharenotsoclear.Forexample,
arecheck-questions (e.g.\ToParis?"inresponseto\IwanttogotoParis")positiveor
negative?Ifpositivefeedbackshowsunderstanding, andnegativefeedbacklackofunder-
standing, thencheck-questions aresomewhere inbetween;theyindicateunderstanding but
alsothatthelackofcon¯dence inthatunderstanding.
Herewewillassumeathirdcategory ofneutralfeedbackforcheck-questions andsimilar
feedbacktypes.Ifnegativefeedbackindicates alackofunderstanding, neutralfeedback
indicates lackofcon¯dence inone'sunderstanding.
Negativefeedbackcanbecausedbyfailuretointegrate Uonanyofthelevelsofactionin
dialogue:
²lackofcontact-HdidnotnoticethatSsaidsomething
²lackofperception -HdidnothearwhatSsaid
²lackofunderstanding onasemantic/pragmatic level-Hrecognized allthewords,
butcouldnotextractacontent
{context-indep endentmeaning, e.g.wordmeanings
{context-dependentmeaning, e.g.referents
{pragmatic meaning, i.e.therelevanceofS'sutterance inrelationtothecontext
²rejection ofcontent
Fornegativefeedback,detecting thelevelwithwhichthefeedbackisconcerned isimportant
forbeingabletorespondappropriately .Herearesomepossibilities forthedi®erentlevels:
²contact:trytoestablish contact(\Heythere")
²perception: speaklouder,articulate
²understanding
{meaning: reformulate

92 CHAPTER 3.GROUNDING ISSUES
{pragmatic meaning: reformulate,orexplainhowtheutterance isrelevant
²rejection: abandon orarguefortheacceptance ofthecontent
3.4.3Eliciting andnon-eliciting feedback
Wewillusetheterm\eliciting feedback",borrowedfromAllwoodetal.(1992),torefer
tofeedbackutterances intendedtoelicitaresponse,ormorespeci¯cally utterances u0such
thatu0isintendedtomakeSrespondtou0becauseHisnotsureabouthowtointerpret
S'sutterance u.Check-questions (bothy/n-andalternativ e-questions) areseenaseliciting
feedbackinthissense.Eliciting feedbackcanalsooccurafterS'sutterance uis¯nished.
3.4.4Formoffeedback
Aswithallutterances, feedbackutterances canhavevarioussyntacticforms:
²assertion
{declarativ e(\Iheardyousay`gotoParis'.",\YouwanttogotoParis.")
²imperative(\Please repeat.")
²interrogativ e
{y/n-question (\Didyousay`Paris'?",\DoyouwanttogotoParis?")
{wh-question (\Whatdidyousay?",\Whatdoyoumean?", \Wheredoyouwant
togo?")
{alternativ e-question (\Didyousay`Paris'or`Ferris'?",\Doyouwanttogoto
Paris,FranceorParis,Texas?")
²ellipsis(\Paris?",\toParis.")
²conventional(\Pardon?")
Apartfromshowingthespeakerthatonehasundersto od,feedbackintheformofanexplicit
declarativ ereport,repetitionorreformulationhastheadditional function ofmakingsure
thattheunderstanding isactually correct,byprovidingachanceforcorrection. Ay/n-
question hasasimilarfunction, butitindicates lesscon¯dence intheinterpretation (i.e.is

3.4.FEEDBA CKAND RELA TED BEHA VIOUR INHUMAN-HUMAN DIALOGUE 93
moreneutral) andhasastronger elicitingelementthananassertion; aquestion requiresan
answer,whileanassertion canoftenbeassumed tobeaccepted intheabsenceofprotest.
Arelateddimension ofclassi¯cation ishowtheformofthefeedbackutterance relatesto
theprevious utterance. Onewayofgivingpositivefeedbackistosimplyrepeatverbatim
theprevious utterance (e.g.\ToParis."inresponseto\ToParis.").Asimilarstrategy is
toprovideareformulation(e.g.\Yourdestination cityisParis,thecapitalofFrance.").
Thelatterisperhapsastronger signalofunderstanding thentheformer,sinceaverbatim
repetitiondoesnotinprinciple requirethattheutterance wasundersto od.
3.4.5Meta-lev elandobject-levelfeedback
A¯naldistinction canbemadedependingonwhether thefeedbackexplicitly talksabout
whatthespeakersaidormeant,inwhichcasethefeedbackcanbesaidtobemeta-level
feedback,orifinsteadittalksaboutthesubjectmatterofthedialogue, inwhichcasewe
talkaboutobject-levelfeedback.
²Meta-lev el
{perception (\Didyousay`Paris'?")
{understanding (\DidyoumeanthatyouwanttogotoParis?")
²Object-level(\DoyouwanttogotoParis?")
Thisdistinction doesnotnecessarily applytoallkindsoffeedback.Forexample, for
conventionalphraseslike\Pardon?" andelliptical phraseslike\Paris?"itisnotclearif
theyrefertowhatthespeakersaidormeant,oraboutthesubjectmatterofthedialogue,
orneither.
3.4.6Fragmentfeedback/clari¯cation ellipsis
Often,feedbackdoesnotconcernacomplete utterance, butonlyapartofit;thisisthe
casee.g.withfailuretoidentifyareferenttoanNP.Wecanrefertothiskindoffeedback
asfragmentfeedback(exempli¯ed in(3.10))andcontrastitwithcompletefeedbackwhich
concerns awholeutterance (asin(3.11)).

94 CHAPTER 3.GROUNDING ISSUES
(3.10)A:ImetJimyesterday.
B:Who?[negativepartialunderstanding ICM]
Whodidyousayyoumet?[partialnegativeunderstanding ICM
+partialpositiveunderstanding ICM]
Jim?[partialinterrogativ eunderstanding ICM]
JimJones?[intermediate partialunderstanding]
JimJonesorJimLewis?[partialintermediate understanding]
No,itwasBobthatyoumet[partialacceptance, partialrejec-
tion1]
(3.11)A:ImetJimyesterday.
B:Pardon?[negativecomplete perception]
B:Whatdoyoumean?[negativecomplete understanding]
B:Liar![(probably) complete rejection]
Itisalsopossibletogivenegativepartialfeedbacktoonepartofanutterance andsimul-
taneously givepositivepartialfeedbacktosomeotherpart,aswhenBsays\Whodidyou
sayyoumet?";here,BgivespositivefeedbackthatBundersto odthatAmetsomeone, but
negativefeedbackconcerning whoAmet.CooperandGinzburg (2001)discussnegative
partialfeedbackusingtheterm\clari¯cation ellipsis" andgiveanaccountintheQUD
framework.
3.4.7OwnCommunication Managemen t
AfurtheraspectrelatedtofeedbackandICMiswhatAllwoodreferstoasOwnCommuni-
cationManagemen t,whichinvolveshesitation sounds,suchas\um",\er"etc.,(whichalso
havethee®ectofkeepingtheturn),andself-corrections (initiated eitherbythespeakeror
bythehearer). ItshouldalsobenotedthatsomefeedbackbehaviouralsohasanOCM
aspect;forexample, onecanexplicitly acceptaquestion to\buytime"forcomingupwith
ananswer.
3.4.8Repairandrequestforrepair
Onetypeofbehaviourverycloselyrelatedtofeedback,andalsotoOwnCommunication
Managemen t(seebelow),iswhatTraumreferstoas\other-initiated repair".
1Thatis,acceptance oftheproposition\Ametsomeone", butrejection oftheproposition\theperson
thatAmetwasJim".

3.5.UPDATESTRA TEGIES FORGROUNDING 95
²other-initiated other-repair: repairbyA(\YoumeanParis.")
²other-initiated self-repair: requestforrepairbyA(\DoyoumeanParis?")
ThisoverlapswithwhatClarkcallsalteration,i.e.thecasewhereAacceptsanaltered
versionoftheproposedjointproject.
3.4.9Request forfeedback
Above,wehaveanalyzed feedbackproducedbytheaddressee Ainresponsetoanutterance
uproducedbyaspeakerS.Anadditional typeoffeedbackbehaviourswhichareproduced
bythespeakerofuarerequests forfeedback,e.g.\Doyouunderstand?", \Gotthat?".
²understanding (\Gotthat?",\Doyouunderstand?")
²acceptance (\OK?", \Doyouagree?")
3.5Updatestrategies forgrounding
Afterhavingreviewedgrounding-related interactivecommunication managemen tinhuman-
humandialogue, wewillnowexploreupdatestrategies relatedtogrounding. Inthissection,
weintroducetheconcepts ofoptimism, caution, andpessimism regarding grounding update
strategies.
3.5.1Optimistic andpessimistic strategies
According toClarkandSchaefer(1989a), manymodelsofdialogue makeatacitidealization
(1)thatDPsassumethatthecontentofeachutterance isautomatically addedtothe
common ground. Somemodelsmaketheweakeridealization (2)thatDPsassumethatthe
contentofeachutterance isautomatically addedtothecommon groundunlessthereis
evidence tothecontrary.ClarkandSchaeferargueagainsttheseidealizations andpropose
toreplacethemwith\systematic procedures" forestablishing mutualbeliefregarding the
addressee's understanding ofutterances.
FollowingClark,morerecentcomputational modelsofgrounding (e.g.Traum(1994)and
Ginzburg (forth))takeitforgrantedthatutterances arenottakentobegrounded until

96 CHAPTER 3.GROUNDING ISSUES
someformoffeedbackhasbeenproduced.Thisfeedbackneednotbeexplicit: forexample,
arelevantanswertoaquestion showsthattheDPproducingtheanswerhasundersto od
andaccepted thequestion posedintheprevious utterance. Thatis,DPsdonotmake
assumptions aboutgrounding untilthereissomeevidence.
However,asnotedbyTraumthiscannotapplytoallutterances. Ifitdid,eachcon¯rma-
tionofunderstanding wouldagainhavetobecon¯rmed andsoonadin¯nitum. Inour
terminology ,thismeansthatitisnecessary toassumeoptimism onsomelevel.InTraum's
model,acknowledgemen tsareoptimistically assumed tobegrounded (thatis,theydonot
needtobeacknowledged themselv esbeforebeingaddedtothecommon ground) whereas
anyotherconversational actsmustreceivesomeacknowledgemen tbeforebeinggrounded.
WhilewebelievethatClarkiscorrectincriticizing tacitidealizations aboutDPsassump-
tionsregarding grounding, wealsobelievethatthesetacitassumptions, ifmadeinanex-
plicitandsystematic fashion,arenotnecessarily incorrect ormoreidealizing thanClark's
alternativ e.Furthermore, theydeservetobeexplored boththeoretically andforpractical
useindialogue systems. WeshouldalsokeepopenthepossibilitythatDPsmaymake
di®erentassumptions regarding grounding dependingonvariousfactorsofthecontext.
Ifissuesoftacitness areputaside,itseemsthatwhatwearedealingwitharedi®erent
accountsofwhenanutterance istoberegarded asgrounded. Theneedforsuchan
assumption arisespartlybecausethecommunicativebehaviouritselfdoesnotcompletely
determine whether anutterance isgrounded. Atsomepoint,aDPmustsimplyassume
thatanutterance hasbeengrounded, andwebelievethatthemaindi®erence between
themcanbedescribedintermsofoptimism andpessimism .
The¯rsttypeof\tacitidealization" describedbyClark((1)above)canthusberestated
asanoptimistic grounding assumption; aDPadhering tothisassumption willassume,
foranyutterance u,thatuisgrounded assoonasithasbeenuttered, withnoregardto
feedback.Thesecondtypeof\idealization" ((2)above)canberestated asapessimistic
grounding assumption, sinceitrequires somewayofdetermining theabsenceofnegative
feedbackbeforegrounding isassumed. Clark'ssuggested assumption isalsopessimistic,
sinceDPsadhering toitwillrequirepositiveevidence beforeassuming thatanutterance
isgrounded.
3.5.2Grounding updatesandactionlevels
Fromaninformation stateupdateperspective,itseemssensibletoregardanutterance as
grounded whenithasbeenaddedtothecommon ground. Eachactionlevelconnected
toanutterance canbeassociatedwithacertaintypeofupdate.Toassumegrounding
ontheperception levelcanbeseenasupdatingthecommon groundwiththeassumed

3.5.UPDATESTRA TEGIES FORGROUNDING 97
surfaceformoftheutterance; toassumegrounding ontheunderstanding levelistoupdate
thecommon groundwithasemanticrepresentationoftheutterance. Finally,toassume
anutterance hasbeengrounded ontheacceptance levelistoupdatethecommon ground
withtheintendede®ectsoftheutterance (e.g.pushing aquestion onQUD).Thus,the
grounding assumption canbedividedintofourindependentassumptions, oneforeachof
theselevels;wewillconcentrateontheunderstanding andintegration levels.
Theindependenceoftheseassumptions meanse.g.thatitispossibletomakeanoptimistic
assumption aboutunderstanding butapessimistic oneaboutacceptance. Thiswouldmean
assuming thatanutterance wasundersto odassoonasitwasuttered,butrequiring positive
evidence beforeitisassumed tobeaccepted.
3.5.3Thecautious strategy
Clarkseemstoassumethatonceanutterance hasbeengrounded, thereisnoturningback;
thegrounding assumption cannotbeundone. Thatis,themomentinformation aboutan
utterance isaddedtothecommon groundthereisnoway(shortofgeneralstrategies for
beliefrevision) ofunderstanding negativefeedbackandreacttoitbymodifyingorremoving
thegrounded material.
However,webelievethatthereisadi®erence betweenassuming anutterance asgrounded
(addedtothecommon ground) andgivingupthepossibilityofmodifyingorcorrecting
thegrounded material. Thisopensupanewkindofgrounding strategy notincluded in
Clark'saccount:thecautious strategy.
ForaDPusingacautious strategy,itispossibletoassumeanutterance asbeinggrounded,
whilestillbeingabletounderstand andreactappropriately tonegativefeedback.This
requires(1)thatnegativefeedback,whichisoftenunderspeci¯edinthesensethatitdoes
notexplicitly identifywhichpartofanutterance itconcerns, canbecorrectly interpreted,
and(2)thattheDPcanrevisethecommon groundinawaywhichundoesalle®ectsof
theerroneous assumption thattheutterance wasgrounded. Asimpleexample isshownin
(3.12).
(3.12)A:DoIneedavisa?
Aoptimistic allyassumes that\doesAneedavisa?"isnow
underdiscussion.
B:Pardon?
AcorrectlyinterpretsB'sutteranceasnegativefeedback(proba-
blyontheperceptionlevel)regardingthepreviousutterance,and
retractstheassumption that\doesAneedavisa?"isonQUD.

98 CHAPTER 3.GROUNDING ISSUES
Onthisview,theupdatesassociatedwithgrounding involvestwosteps:addingthemate-
rialtothecommon ground,andconsequen tly,removingthepossibilityof(easily)undoing
theupdatesfromthe¯rststep.
Oneadvantageofthecautious strategy isthatinferences resulting fromanutterance can
bedrawnimmediately ,without havingtowaitforfeedback,whilenotrequiring costly
strategies forgeneralbeliefrevisionincaseswherethegrounding assumption turnsoutto
bepremature.
Weleaveopenthequestion ofwhichstrategy isthemostcognitivelyplausible; infact,the
mostreasonable assumption isprobably thatanintelligentcombination ofdi®erentstrate-
giesisthemostrealistic model.Butwedobelievethatthecautious strategy deserves
thesameattentionasthepessimistic strategy advocatedbyClark.Moreover,wedonot
wanttopreclude thepossibilitythateventheoptimistic strategy mightcomeinhandy
sometimes. Asalways,questions ofcognitiveplausibilit yarebestresolvedbyempirical
experimentationratherthanbyrhetoric. Whatwewanttodohere,apartfromimple-
mentingusefulgrounding mechanisms foradialogue system,istoshowthatthecautious
approachisatleastapossiblealternativ e.
Torepeat,wewillusethequali¯cation \optimistic", \cautious" and\pessimistic" for
grounding updatestrategies, withthefollowingmeanings:
²optimistic grounding update:DGB7isupdatedimmediately afteruwasproduced
(and,inthecaseofutterances producedbyotherDP,understo odandaccepted); no
backtrackingmechanismavailable
²cautious grounding update:DGBisupdatedimmediately afteruwasproduced(and,
inthecaseofutterances producedbyotherDP,understo odandaccepted); however,
backtrackingisavailable
²pessimistic grounding update:DGBisupdatedwhenpositiveevidence ofgrounding
havebeenacquired
3.6Feedbackandgrounding strategies forIBiS
Intheprevious sections, wediscussed grounding-related ICM(andinparticular feedback)
andgrounding strategies inhuman-humandialogue. Inthissection,wediscussfeedback
andgrounding fromtheperspectiveofdialogue systemsingeneral,andIBiSinparticular.
7Dialogue Gameboard,i.e.theshared partoftheinformation stateinIBiS.SeeSection2.2.3.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 99
Most(ifnotall)dialogue systems todayhaveanasymmetrical treatmen tofgrounding,
i.e.thegrounding ofsystemutterances ishandled verydi®erentlyfromthegrounding of
userutterances. Typically,thesystemwillprovidefairlyelaboratefeedbackonuserinput,
usuallyintheformofquestions suchas\DidyousayyouwanttogotoParis?".Theuser
mustthenanswerthesequestions a±rmativ elybeforethesystemwillgoon.Thereason
forthis,ofcourse,isthelowqualityofspeechrecognition.
3.6.1Grounding strategies fordialogue systems
Inthissection,wediscussgrounding updatestrategies fromtheviewpointoftheiruseful-
nessindialogue systems. Thetwomainfactorsdetermining theusefulness ofanupdate
strategy inadialogue systemisusability(including e±ciency ofdialogue interaction) and
thee±ciency ofinternalprocessing.Onthisview,pessimism hasthedisadvantagethatit
makesdialogue lesse±cientsinceeachutterance mustbeexplicitly grounded andaccepted;
foruserutterances thisisoftenachievedbyaskingcheckquestions towhichtheusermust
replybeforecommunication canproceed.
However,thecautiously optimistic approachhasthedisadvantagethatrevisionisnecessary
whengrounding oracceptance fails,whichhappensiftheuserrespondsnegativelytothe
feedback.Thesolution presentedsolvestherevisionproblem bykeepingrelevantpartsof
previous information statesaround.
Acommon methodistousetherecognition scoreofauserutterance todetermine the
feedbackbehaviourfromthesystem,giventhatthesystemhasundersto odtheutterance
su±ciently.Webelievethatthebestsolutionforanexperimentalspeech-to-speechdialogue
systemistoswitchbetweengrounding updatestrategies dependingonthereliabilityof
communication (whichdependsonnoisiness ofenvironmen t,previous ratioofsuccessful vs.
unsuccessful communication, etc).Welinkpessimistic andoptimistic grounding updateto
interrogativ eandpositivefeedback,respectively.Interrogativ efeedbackfromthesystem
raisesaquestion regarding themeaning ofaprevious utterance, whichwouldnotmake
senseifthesystemhadalreadyassumed thatacertainanswertothemeaning question had
beengrounded; ine®ect,thiswouldamounttoraisingaquestion whoseansweris(already)
assumed tobepartofthecommon ground. Similarly ,givingpositivefeedbackcorresponds
naturally tothecasewheresomeinterpretation isdeemedtobealreadygrounded.
Amoresophisticated methodfordetermining whatgrounding andfeedbackstrategy to
usewouldalsotakeintoconsideration thedegreeofrelevanceofacertaininterpretation in
thecurrentdialogue context.Ifarecognition hypothesiswhichdoesnothavethehighest
scoreisnevertheless morerelevantthanthehypothesiswiththehighestscore,thiscould
resultinchoosingtheformerhypothesis.Thishasnotbeenimplemen tedinIBiS,andis

100 CHAPTER 3.GROUNDING ISSUES
anareaforfutureresearch.8
3.6.2\Implicit" and\explicit" veri¯cation indialogue systems
Intheliterature concerning practical dialogue systems (e.g.San-Segundo etal.,2001),
grounding isoftenreduced toveri¯cation ofthesystem's recognition ofuserutterances.
Twocommon waysofhandling veri¯cation aredescribedas\explicit" and\implicit" ver-
i¯cation, exempli¯ed in(3.13)(example fromSan-Segundo etal.,2001).
(3.13)a.Iundersto odyouwanttodepartfromMadrid. Isthatcor-
rect?[explicit]
b.YouleavefromMadrid. Whereareyouarriving at?[im-
plicit]
Actually,both\explicit" and\implicit" feedbackcontainaverbatimrepetitionorarefor-
mulationoftheoriginalutterance, andinthissensetheyarebothexplicit. Theactual
baseforthedistinction iswhatwehaveherereferredtoaspolarity:\explicit" veri¯cation
isneutral(andeliciting andinterrogativ e)whereas \implicit" veri¯cation ispositive.
Giventhatveri¯cation isarathermarginal phenomena inhuman-humandialogue, itis
perhapssurprising thatitisoftentheonlyaspectoffeedbackcoveredindialogue systems
literature. Firstly,becauseitisusuallynotnecessary forhumanstoverifywhatthey(think
they)haveheard;thatis,itisaratheruncommon grounding procedureinhuman-human
dialogue. Second,becauseitonlyinvolvespartofthefullspectrumoffeedbackbehaviour,
excluding e.g.acceptance-related feedbackbehaviour.
3.6.3Issue-based grounding inIBiS
Inthissectionweoutlinea(partially) issue-based accountofgrounding intermsofinfor-
mationstateupdates,inspiredbyGinzburg's accountofcontentquestions andacceptance-
questions. However,wemakesigni¯can tdepartures fromGinzburg's account,forvarious
reasons.
AbasicideaoftheaccountusedinIBiS2isthatmeta-issues (thecontentandacceptance
questions) donotalwayshavetoberepresentedexplicitly .However,incertaincasesitis
usefultorepresentgrounding issuesexplicitly .
8Forexample, onecouldassessthedegreeofrelevanceofacertainanswer-movebycheckinghowmany
accommo dationsteps(seeChapter 4)wouldbenecessary beforeintegrating thequestion.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 101
Contentquestions inIBiS
Weregardexplicitinterrogativ eunderstanding feedbackasexplicitly raisingcontentques-
tions,whichmayberespondedtoexplicitly orimplicitly .Wealsorefertotheseasunder-
standing questions .Explicit interrogativ efeedbackisveryrelevantfordialogue systems,
wherepoorspeechrecognition oftenmakesitnecessary forthesystemtoexplicitly verify
eachrecognized userutterance, givingtheuserachancetocorrectanymisunderstandings.
Interrogativ efeedbackcaninprinciple bewh-questions (\What doyoumean?"), y/n-
questions (\DoyoumeanParis?",\Paris,isthatcorrect?"), oralternativ equestions (\Do
youmeantoParisorfromParis?").However,wehavechosennegativefeedback(\Idon't
understand") ratherthany/n-questions toindicate lackofunderstanding. Clari¯cation
questions arenotusedinIBiS2;however,theywillbeintroducedinChapter 4.This
leavesuswithy/nunderstanding questions, whichconcernonespeci¯cinterpretation ofa
previous utterance. ThesearerepresentedinIBiS2as?und(DP*C)whereDPisaDP
andCisaproposition,andcanbeparaphrased as\DidDPmeanC?"or\IsCacorrect
understanding ofDPsutterance?". Inthecasewheretheunderstanding question concerns
aquestion (raisedbyanask-move),thepropositionCisissue(Q)whereQisaquestion.
Inthiscase,theparaphrase canbefurtherspeci¯edas\DidDPmeantoraiseQ?".
Toallowthis,wehaveextended theIBiSsemanticpresentedinChapter 2toincludetwo
newkindsofpropositions.
²und(DP;P):PropositionwhereP:PropositionandDP:Participan t9
²issue(Q):PropositionwhereQ:Question10
Implicitunderstanding-questions Actually,theuseoftheterm\implicit" inthe
contextofgrounding (orveri¯cation) canbeusedtodescribenotthegrounding behaviour
itselfbut,rather,thestatusofthegrounding issue.Whatisoftenreferredtoasimplicit
veri¯cation canarguably beseenasimplicitly raisingagrounding question, whichmayor
maynotberespondedto.
Thisideawillnotbeimplemen teduntilChapter 4,sinceitrequiressomeadditional mech-
anismswhichwillbeneededanywayforthekindofbehavioursweintroducethere.Specif-
9Notethatthisde¯nition allowsPtoitselfbeapropositionoftheformund(DP;P0);however,we
allowthistopassintheinterestofbrevity.
10Thisde¯nition allowsissue(Q)asapropositionevenwhenitisnotembeddedinaproposition
und(DP,issue(Q)).InIBiS,thepropositionissue(Q)onlyappearsinsideunderstanding questions
orasanargumen ttoanICMmove(seeSection3.6.5).However,inChapter 4wewillusethecorrespond-
ingquestion?issue(Q).Asuitableparaphrase ofthisquestion wouldbe\ShouldQbecomeanissue?"or
\ShouldQbeopenedfordiscussion"; thisissimilartoGinzburg's MAX-QUD question.

102 CHAPTER 3.GROUNDING ISSUES
ically,weneedadistinction betweenaglobalandalocalQUD(seealsoCooperetal.
(2000)andCooperandLarsson (2002)), wheretheformercontainsexplicitly raisedor
addressed (butasyetunresolved)issues,andthelattercontainsquestions whichcanbe
usedforresolving shortanswers.
Togiveashortpreview, thebasicideaisthatexplicitpositivefeedbackimplicitly raises
anunderstanding-issue, i.e.whentheimplicitfeedbackisintegrated, theunderstanding
question ispushedonlocalQUD.Thisallowstheusertodiscardthesystem's interpretation
simplybyprovidinganegativeanswertothegrounding question, orcon¯rmitbygivinga
positiveanswer.Sincethequestion isaddedonlytothelocalQUD,andnottotheglobal
one,itwilleventuallydisappearifitisnotanswered.Thisallowsdialogues toproceed
moree±ciently,sincetheuserdoesnothavetogiveexplicitcon¯rmations allthetime.
Again,thiswillbeexplained indetailinChapter 4.
Acceptance questions
InGinzburg's protocol,aDPwhohasperceivedandinterpreted anutterance isfacedwith
theacceptance-question; whether toacceptthecontentoftheutterance ornot.Ifthe
contentisnotaccepted, theDPshouldpushtheintegratequestion (pushitonQUD)and
addressit.
Onewayofdealingwithacceptance wouldbetofollowGinzburg's accountandexplicitly
representanacceptance-question whichispushedonQUDincaseswhereauserutterance
isundersto odbutcannotbeintegrated, andsubsequen tlyproduceanutterance addressing
theacceptance question. Weregardfeedback-movesonthereaction level(compliance and
declination moves,inClark'sterminology) asaddressing acceptance questions. Above,we
havearguedagainstpushing anythingonQUDinthiscasesinceitisasharedstructure,
andtheuserinthiscasehasnochanceofdoingthecorrespondingupdateonherown
QUDuntiltheutterance hasbeenproduced.Soanalternativ estrategy wouldbeto¯rst
producetheutterance addressing theacceptance question andsubsequen tlyassumethat
theuserwillaccommo dateitandpushitonQUD;atthistime,thesystemcandothe
same.
However,itappearsthatitisonlyusefultorepresenttheacceptance question explicitly
onQUDincaseswhereitcangiverisetoadiscussion whereDPsargueforandagainst
theacceptance ofaquestion asatopicfordiscussion, orforapropositionasafactor
asatopicfordiscussion. Foradialogue systemunabletoperformsuchargumen tation
dialogues, itappearspointlesstorepresenttheacceptance question explicitly .Sincean
acceptance orrejection movecannotbechallenged, themovewillprovideade¯niteanswer
totheintegration question whichwouldthusbeimmediately removedfromQUDoncethe
rejection hadbeengrounded.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 103
Forthesereasons, wewillnotrepresentacceptance issuesexplicitly inIBiS.Inasystem
capableofnegotiation and/orargumen tation,however,itwouldbenecessary todoso,and
toregardfeedback-movesontheacceptance levelasrelevantanswerstothisquestion (see
Section5.8.2forfurtherdiscussion).
Temporarystorage
Toenablecautious grounding weneedsomewayofrevisingthedialogue gameboardwhen
optimistic grounding assumptions turnouttobepremature, withouthavingtodealwith
theproblems ofgeneralized beliefrevision GÄardenfors (1988).Astraightforwardwayof
doingthisistokeeparoundrelevantpartsofprevious dialogue gameboardstates,and
copythecontentsofthesebacktotheDGBwhennecessary .Thisstrategy willbeusedfor
systemutterances inIBiS2,andalsoforuserutterances inIBiS3.
3.6.4Enhancing theinformation statetohandlefeedback
Inthissection,weshowhowtheIBiSinformation stateneedstobemodi¯edtohandle
grounding andfeedback.Thenewinformation statetypeisshowninFigure3.1.
2
66666666666666666666666664private:2
66666666666664agenda:OpenQueue(Action)
plan :OpenStack(PlanConstruct)
bel :Set(Prop)
tmp :2
6664com :set(Prop)
qud :OpenStack(Question)
agenda:Stack(Action)
plan :Stack(PlanConstruct)3
7775
nim :OpenQueue(Mo ve)3
77777777777775
shared :2
6666664com:Set(Prop)
qud:OpenStack(Question)
pm:OpenQueue(Mo ve)
lu:"
speaker :Participan t
move:Set(Move)#3
77777753
77777777777777777777777775
Figure3.1:IBiS2Information Statetype

104 CHAPTER 3.GROUNDING ISSUES
Temporarystore
Toenablethesystemtobacktrackifanoptimistic assumption turnsouttobemistaken,
relevantpartsoftheinformation stateiskeptin/private/tmp.Thequdandcom¯elds
maychangewhenintegrating anaskoranswermove,respectively.Theplanmayalsobe
modi¯ed,e.g.ifaraiseactionisselected. Finally,ifanyactionsareontheagendawhen
selection starts(whichmeanstheywereputthereduringbytheupdatemodule),these
mayhavebeenremovedduringthemoveselection process.
Non-integratedmoves
Sinceseveralmovescanbeperformed perturn,IBiSneedssomewayofkeepingtrackof
whichmoveshavebeeninterpreted. Thisisdonebyputtingallmovesinlatestmoves
inaqueuestructure callednim,forNon-Integrated Moves.Thisstructure isprivate,since
itisaninternalmatterforthesystemhowmanymoveshavebeenintegrated sofar.Once
amoveisassumed tobegrounded ontheunderstanding levelthemoveisaddedtothe
/shared/lu/mo vesset.Sincethemovehasnowbeenundersto odonthepragmatic
level,thecontentofthemovewillbeaquestion orafullproposition(forshortanswers,
thepropositionresulting fromcombiningitwithaquestion onQUD).
Previousmoves
Tobeabletodetectirrelevantfollowups,IBiSneedstoknowwhatmoveswereperformed
(andgrounded) intheprevious utterance. Thesearestoredinthe/shared/pm ¯eld.
Timeout
Tobeabletodecidewhentheuserhasgivenupherturn,wehaveaddedaTISvariable
timeout oftypeReal,whosevalueisthetime(inseconds) afterwhichthesystemwill
assumethattheturnhasbeengivenupifnospeechhasbeendetected. Thisvariablewill
befurtherdiscussed inSection3.6.6.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 105
3.6.5Feedbackandsequencing dialogue moves
Inthissection,we¯rstshowhowfeedbackdialogue movesinIBiS2arerepresented.We
thenreviewthefullrangeoffeedbackmoves,startingwithsystem-generated feedbackand
thenmovingontouserfeedback.
Thegeneralnotation forICMdialogue movesusedinIBiSisthefollowing:
(3.14)icm:L*Pf:Argsg
whereLisanactionlevel,Pisapolarity,andArgsareargumen ts.
²L:actionlevel
{con:contact(\Areyouthere?")
{per:perception (\Ididn'thearanythingfromyou",\Iheardyousay'toParis"')
{sem:semanticunderstanding (\Idon'tunderstand", \ToParis.")
{und:pragmatic understanding (\Idon'tquiteunderstand", \Youwanttoknow
aboutprice.")
{acc:acceptance/reaction (\Sorry,Ican'tanswerquestions aboutconnecting
°ights",\Okay.")
²P:polarity
{neg:negative
{int:interrogativ e
{pos:positive
²Args:argumen ts
Notethatthe\neutral" polarityhasbeenreplaced bythelabel\int";wehavemadea
simplifying assumption thatneutralfeedbackisalwayseliciting andinterrogativ e.11
Theargumen tsaredi®erentaspectsoftheutterance ormovewhichisbeinggrounded,
dependingactionlevel:
11Note,however,thatifwehadincluded feedbackformslike\Whatdidyousay?",thiswouldstill
beregarded asnegativefeedback.The\int"labelonlyreferstocheck-questions, whichareusually y/n-
questions. Thisisarguably notanoptimallabellingconvention.

106 CHAPTER 3.GROUNDING ISSUES
²forper-level:String,therecognized string
²forsem-level:Move,amoveinterpreted fromtheutterance
²forund-level:DP¤P,where
{DP:Participan tistheDPwhoperformed theutterance
{C:Propositionisthepropositional contentoftheutterance
²foracc-level:C:Proposition,thecontentoftheutterance
Forexample, theICMmoveicm:und*p os:usr*dest city(paris)providespositivefeedbackre-
gardingauserutterance thathasbeenundersto odasmeaning thattheuserwantstogo
toParis.
Inaddition, sequencing ICMmovesforindicating reraising ofissuesandloadingaplanare
included:
²icm:reraise :indicate reraising implicitly (\So,...")
²icm:reraise: Q:reraising anissueQexplicitly (\Returning totheissueofPrice.")
²icm:loadplan (\Let'ssee.")
Systemfeedbacktouserutterances inIBiS2
Inthissectionandthefollowingsection,wereviewsurfaceformsrelatedtofeedbackand
otherICMbehaviourthatwillbeimplemen tedinIBiS2.
Foruserutterances, IBiS2willbeabletoproducee.g.thefollowingkindsoffeedback
utterances (fortheexamples, assumethattheuserjustsaid\IwanttogotoParis"):
²contact
{negative;icm:con*neg (\Ididn'thearanythingfromyou")
²perception
{negative;icm:per*negrealizedasfb-phrase (\Pardon?", \Ididn'thearwhatyou
said.")

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 107
{positive;icm:per*pos:Stringrealizedasmetalevelverbatimrepetition(\Iheard
`toparis'")
²understanding (semantic)
{negative;icm:sem*neg realizedasfb-phrase (\Idon'tunderstand.")
{positive;icm:sem*p os:Contentrealized asrepetition/reform ulationofcontent
(object-level)(\Paris.")
²understanding (pragmatic)
{negative;icm:und*neg realizedasfb-phrase (\Idon'tquiteunderstand.")
{positive;icm:und*p os:DP*Contentrealizedasrepetition/reform ulationofcon-
tent(object-level)(\ToParis.")
{interrogativ e;icm:und*int: DP*Contentrealizedasaskaboutinterpretation (\To
Paris,isthatcorrect?")
²integration
{negative
¤proposition-rejection; icm:acc*neg: Contentrealizedasexplanation (\Sorry,
Parisisnotavaliddestination city")
{positive;icm:acc*p osrealizedasfb-word(\Okay")
Inaddition, IBiS2willbeabletoperformissue-rejection usingthemoveicm:acc*neg:issue( Q),
whereQ:Question asillustrated in(dialogue 3.2).
(dialogue 3.2)
U>Whataboutconnecting flights?
S>Sorry,Icannotanswerquestions aboutconnecting flights.
Wearenotclaiming thathumansalwaysmakethesedistinctions betweenactionexplicitly
orevenconsciously ,northatthelinkbetweensurfaceformandfeedbacktypeisasimple
one-to-one correspondence; forexample, \mm"maybeusedaspositivefeedbackonthe
perception, understanding, andacceptance levels.Feedbackis,simply,oftenambiguous.
However,sinceIBiSismakingallthesedistinctions internally wemightaswelltryto
producefeedbackwhichisnotsoambiguous. Ofcourse,thereisalsoatradeo®inrelation
tobrevity;extremely explicitfeedback(e.g.\Iundersto odthatyoureferred toParis,
butIdon'tseehowthatisrelevantrightnow.")couldbeirritating andmightdecrease
thee±ciency ofthedialogue. Wefeelthatthecurrentchoicesofsurfaceformsarefairly

108 CHAPTER 3.GROUNDING ISSUES
reasonable, buttestingandevaluation onrealuserswouldbeneededto¯ndthebestways
toformulatefeedbackondi®erentlevels.Thisisanareaforfutureresearch.
Ageneralstrategy usedbyIBiSinICMselection isthatifnegativeorinterrogativ efeed-
backonsomelevelisprovided,thesystemshouldalsoprovidepositivefeedbackonthe
levelbelow.Forexample, ifthesystemproducesnegativefeedbackonthepragmatic un-
derstanding level,itshouldalsoproducepositivefeedbackonthesemanticunderstanding
level.
(3.15)S>Paris. Idon'tunderstand.
Insomesystems, positiveorinterrogativ efeedbacktouserutterances isnotgivenimme-
diately;instead,thesystemrepeatsalltheinformation ithasreceivedjustbeforemaking
adatabase queryandaskstheuserifitiscorrect.Itisalsopossibletocombinefeedback
aftereachutterance witha¯nalcon¯rmation. InIBiS2,wehavenotimplemen ted¯nal
con¯rmations. Itcanbearguedthat¯nalcon¯rmations aremoreimportantinaction-
orienteddialogue (seeChapter 5),whereas theyarenotsoimportantininquiry-orien ted
dialogue sincetheyneverresultinanyactionsotherthandatabase searches.
Userfeedbacktosystemutterances inIBiS2
Forsystemutterances, IBiS2willreactappropriately tothefollowingtypesofuserfeed-
back:
²perception level
{negative;fb-phrase (\Pardon?", \Excuse me?",\Sorry,Ididn'thearyou")in-
terpreted asicm:per*neg
²reaction/acceptance level
{positive;fb-phrase (\Okay.")interpreted asicm:acc*p os
{negative;issuerejection fb-phrase (\Idon'tknow",\Nevermind",\Itdoesn't
matter") interpreted asicm:acc*neg:issue
Inaddition, irrelevantfollowupstosystemask-movesareregarded asimplicitissue-rejections.
Thecoverageofuserfeedbackbehaviouristhusmorelimitedthanthecoverageforsystem
behaviour.Themainmotivationforthisisthatsystemutterances arelesslikelytobe
problematic fortheusertointerpretthanviceversa.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 109
Still,theavailablecoverageallowssomeusefulfeedback-phrases, including negativeper-
ceptionfeedbackwhichisusefuliftheoutputfromthesystem's speechsynthesizerisof
poorquality.Ideally,thiswouldprovideaslightreformulationbythesystem,butsince
generation isnotamaintopichere,thishasnotbeenimplemen ted.
Understanding-lev elfeedbackhasnotbeenincluded butmaybeusefulincaseswherethe
userhearsthesystembutcannotunderstand themeaning ofthewordsutteredbythe
system.Inthiscase,areformulationbythesystemmayagainbeuseful.
3.6.6Grounding ofuserutterances inIBiS2
Inthissectionweshowhowoptimistic andpessimistic grounding ofuserutterances has
beenintegrated inIBiS2.Firstweshowhowgrounding strategies aredynamically selected
dependingonrecognition score,inthecasewhereamovehasbeenfullyundersto odand
accepted. Next,weshowhowtodealwithsystemresponsestointerrogativ efeedback
associatedwithpessimistic grounding. Finally,weshowhowthesystemdealswithfailure
toperceive,understand, andintegrateuserutterances bygivingnegativefeedbackonthe
appropriate actionlevel.
Dynamic selectionofgrounding strategies forusermoves
Foruserutterances, IBiS2usesoptimistic orpessimistic grounding strategies basedonthe
recognition scoreandthedialogue movetype.Thismakesthecorrespondingintegration
rulesmorecomplex thantheonesinIBiS1.Foruser\core"moves(inIBiS2,askand
answer),theintegration strategy dependsontherecognition scorefortheutterance in
question. Thischoiceisdetermined bytworecognition thresholds, T1andT2,where
T1>T2.Iftherecognition scoreishigherthanT2,anoptimistic strategy ischosen;
positiveacceptance feedback(\OK")isselected, andifthescoreislowerthanT1positive
understanding feedback(\ToParis.")isalsoselected.
IfthescoreislowerthanT2,themoveisnotintegrated andintheselection phasea
pessimistic strategy involvinginterrogativ eunderstanding feedback(e.g.\ToParis,isthat
correct?") isselected(seeSection3.6.6).
Ofcourse,theideaofusingrecognition scorefordetermining whether andhowtocon¯rm
userutterances isnotnew(seee.g.San-Segundo etal.,2001),andmoresophisticated
decision proceduresarecertainly possible. WeuseitheretoshowhowIBiS2enables
°exiblechoicebothoffeedbacktypeandofgrounding updatestrategy.

110 CHAPTER 3.GROUNDING ISSUES
Inaddition tobeingcheckedforrelevance,contentfulmovesarecheckedforintegratabilit y
(acceptabilit y)andiftheseconditions arenotful¯lledthemovewillnotbeintegrated;
instead,itwillgiverisetonegativeacceptance feedbackasexplained inSection3.6.6.
Integration ofuseraskmoveTheintegration ruleforuseraskmoveimplemen tingthe
optimistic grounding strategy isshownin(rule3.1).
(rule3.1)rule:integrateUsrAsk
class:integrate
pre:8
>>>>>><
>>>>>>:$/shared/lu/speaker ==usr
fst($/private/nim,ask(Q))
$score=Score
Score>0.7
$domain ::plan(Q,Plan)
eff:8
>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>:1pop(/private/nim)
2push(/ private/agenda,icm:acc*p os)
3add(/shared/lu/moves,ask(Q))
4ifdo(Score·0.9,
push(/ private/agenda,icm:und*p os:usr*issue(Q)))
5ifdo(in($/ shared/qud,Q)andnotfst($/shared/qud,Q),
push(/ private/agenda,icm:reraise: Q))
6push(/ shared/qud,Q)
7push(/ private/agenda,respond(Q))
The¯rsttwoconditions picksoutauseraskmoveonnim.Thethirdandfourthcon-
ditionschecktherecognition scoreoftheutterance andifitishigherthan0.7(T2),the
ruleproceedstocheckforacceptabilit y.Ifthescoreistoolow,themoveshouldnotbe
optimistically integrated; instead,apessimistic grounding strategy shouldbeappliedand
interrogativ efeedbackselected(seebelow).
The¯fthcondition checksforacceptabilit y,i.e.thatthesystemisabletodealwiththis
question, i.e.thatthereisacorrespondingplaninthedomainresource. Ifnot,the
integration rulewillnottriggerandtheaskmovewillremainonnimuntiltheselection
phase,whereitwillgiverisetoanissuerejection (seeSection3.6.6).
The¯rstupdatepopstheintegrated moveo®nim.Inupdate2,positiveintegration
feedbackisaddedtotheagenda,toindicate thatthesystemcanintegratetheask-move.
Update3addsthemoveto/shared/lu/mo ves,therebyre°ecting theoptimistic ground-
ingassumption ontheunderstanding level.Inupdate4,positiveunderstanding feedback
isselectedunlessthescoreishigherthan0.9(T1).

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 111
Update5checksifthisquestion isalreadyonQUD;ifso,thesystemselectssequencing
feedbacktoshowthatithasundersto odthattheuserisreraising anopenissue.(Ifthe
question isalreadyontopofQUD,however,itisnotseenasacaseofreraising.) See
Section3.6.9formorecasesofreraising. Update6pushes QonQUD;notthatifQwas
alreadyonQUDbutnottopmost, pushingitwillbeequivalenttoraisingittothetopmost
position.ThisisapropertyoftheOpenStackdatatype(seeSectionA.2.1).
Update7pushestheactiontorespondtoQontheagenda. Thiscanberegarded asa
shortcut forreasoning aboutobligations andintentions;whenaccepting auserquestion,
thusaccepting theobligation totrytorespondtoit,thesystemwillautomatically intend
torespondtoit.
DefaultICMmoveselection ruleTheroleoftheICMmoveselection rulesisto
addmovestobegenerated tothenextmovesTISvariablebasedonthecontentsof
theagenda. ICMwhichisaddedtotheagendabytheupdatemodulewillbemovedto
nextmovesbythedefaultICMselection rule(rule3.2).
(rule3.2)rule:selectIcmOther
class:selecticm
pre:(
in($/private/agenda,icm:A)
notin($nextmoves,B)andB=ask(C)
eff:(
push(nextmoves,icm:A)
del(/private/agenda,icm:A)
Dialogueexample: integrating userask-moveThedialogue belowshowshowauser
askmovewithascoreof0.76issuccessfully integrated, andpositiveunderstanding and
acceptance feedbackisproduced.
(dialogue 3.3)
S>Welcome tothetravelagency!
U>priceinformation please[0.76]
getLatestMo ves8
>><
>>:set(/private/nim,oqueue([ask(? A.price(A))]))
set(/shared/lu/speaker ,usr)
clear(/ shared/lu/moves)
set(/shared/pm,set([greet]) )
integrateUsrAsk

112 CHAPTER 3.GROUNDING ISSUES
8
>>>>>>>>>><
>>>>>>>>>>:pop(/private/nim)
push(/ private/agenda,icm:acc*p os)
add(/shared/lu/moves,ask(?A.price(A)))
ifdo(0.76·0.9,push(/ private/agenda,icm:und*p os:usr*issue(?A.price(A))))
ifdo(in($/ shared/qud,?A.price(A))andnotfst($/shared/qud,?A.price(A)),
push(/ private/agenda,icm:reraise:? A.price(A)))
push(/ shared/qud,?A.price(A))
push(/ private/agenda,respond(?A.price(A)))
¯ndPlan
2
6666666666664private=2
664agenda=**icm:acc*p os
icm:und*p os:usr*issue(?A.price(A))
icm:loadplan++
nim =hhii3
775
shared =2
66664com=fg
qud=­
?A.price(A)®
pm=©greetª
lu=·speaker =usr
moves =©
ask(?A.price(A))ª¸3
777753
7777777777775
backupShared
selectFromPlan
selectIcmOther½
push(nextmoves,icm:acc*p os)
del(/private/agenda,icm:acc*p os)
selectIcmOther½push(nextmoves,icm:und*p os:usr*issue(?A.price(A)))
del(/private/agenda,icm:und*p os:usr*issue(?A.price(A)))
selectIcmOther
selectAsk
S>Okay.Youwanttoknowaboutprice. Letssee.Howdoyouwantto
travel?
Interrogativ eunderstanding feedbackforuseraskmoveIfauseraskmovecannot
beassumed tobeundersto odbecauseofalowrecognition score,interrogativ efeedbackon
theunderstanding levelisselectedby(rule3.3).
(rule3.3)rule:selectIcmUndIn tAsk
class:selecticm
pre:8
><
>:$/shared/lu/speaker ==usr
fst($/private/nim,ask(Q))
$score·0.7
eff:(
pop(/private/nim)
push(nextmoves,icm:und*int:usr *issue(Q))

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 113
Theconditions arestraightforward.The¯rstupdateremovesthemovefromnim,even
thoughithasnotbeenintegrated. Analternativ eapproachwouldbetokeepthismove
onnimandexplicitly representthegrounding asconcerning thismove.However,this
wouldrequirelabellingallmoveswithuniquemoveIDs;instead, wefollowthegeneral
philosoph yofIBiSoftryingtokeepourrepresentationassimpleaspossibleaslongas
itworks.Theinterrogativ efeedbackselected inthesecondupdatewill,inasense,take
overthefunction oftheoriginalmove;ifthefeedbackisansweredpositively,theendresult
willbethesameasiftheaskmovehadbeenintegrated immediately (seeSection3.6.6for
furtherexplanation).
Integration ofuseranswermoveTheintegration ruleforuseranswermoves,shownin
(rule3.4)issimilartothatforaskmoves,exceptthatanswersarecheckedforrelevance
aswellasreliabilityandacceptabilit y.
(rule3.4)rule:integrateUsrAnsw er
class:integrate
pre:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:1fst($/private/nim,answer(A))
2$/shared/lu/speaker ==usr
3!$score=Score
4Score>0.7
5fst($/shared/qud,Q)
6$domain ::relevant(A,Q)
7$domain ::combine(Q,A,P)
8$database::validDBparameter( P)orP=not(X)
eff:8
>>>>>>>><
>>>>>>>>:1pop(/private/nim)
2add(/shared/lu/moves,answer(P))
3push(/ private/agenda,icm:acc*p os)
4ifdo(Score·0.9andA6=yesandA6=no,
push(/ private/agenda,icm:und*p os:usr*P))
5add(/shared/com,P)
Conditions 1-4aresimilartothosefortheintegrateUsrAsk rule.Therelevanceofthe
contentoftheanswertoaquestion onQUDischeckedincondition 6.
Theacceptabilit ycondition inthecondition 8makessurethatthepropositional content
resulting fromcombiningthequestion topmost onQUDwiththecontentoftheanswer-
moveiseither
²avaliddatabase parameter, or
²anegatedproposition

114 CHAPTER 3.GROUNDING ISSUES
Negated propositionscanalwaysbeintegrated (aslongastheyarerelevant);forexample,
itisokaytosaythatyoudonotwanttogotoParis,evenifParisisnotinthedatabase.
Updates1-3againcorrespondcloselytothoseinintegrateUsrAsk .Update4checksif
thescorewaslowerthanorequalto0.9;ifso,apositiveunderstanding feedbackmoveis
selected. Ifthescoreishigherthan0.9oriftheanswerisyesorno,nounderstanding
feedbackisproduced.Thespecialspecialstatusof\yes"and\no"buildsontheassumption
thattheseareeasilyrecognized; ifthisisnotthecase,theirspecialstatusshouldbe
removed.Finally,update5addsthepropositionresulting fromcombiningthequestion on
QUDwiththecontentoftheanswermovetothesharedcommitmen ts.
Interrogativ eunderstanding feedbackforuseraskmoveIfauseraskmovereceives
alowscore(lowerthanT2,whichisheresetto0.7)andthequestion raisedbythemoveis
acceptable tothesystem,interrogativ eunderstanding feedbackisselectedby(rule3.5).
(Ifthequestion isnotacceptable itwillinsteadberejected; seeSection3.6.6).
(rule3.5)rule:selectIcmUndIn tAnswer
class:selecticm
pre:8
>>>>>>>><
>>>>>>>>:fst($/private/nim,answer(A))
$/shared/lu/speaker ==usr
$score·0.7
fst($/shared/qud,B)
$domain ::relevant(A,B)
$domain ::combine(B,A,C)
eff:(
pop(/private/nim)
push(nextmoves,icm:und*int:usr *C)
Theconditions checkthatthereisauseranswermoveonnimwhosecontentisrelevant
toandcombineswithaquestion onQUD,andthattherecognition scorewaslessthanor
equalto0.7.Iftheseconditions aretrue,themoveispoppedo®nimandinterrogativ e
understanding feedbackisselected.
Integrating andrespondingtointerrogativ efeedback
Integrating interrogativ eunderstanding feedbackAsexplained inSection3.6.3,
Interrogativ efeedbackraisesunderstanding questions. Thisisre°ected in(rule3.6).

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 115
(rule3.6)rule:integrateUndIn tICM
class:integrate
pre:n
fst($/private/nim,icm:und*int: DP*C)
eff:8
><
>:pop(/private/nim)
add(/shared/lu/moves,icm:und*int: DP*C)
push(/ shared/qud,und(DP*C))
Thecondition simplychecksthatthereisanicm:und*int: DP*Cmoveonnim,whichis
thenpoppedo®bythe¯rstupdateandaddedto/shared/lu/mo vesbythesecond
update.Thethirdupdatepushestheunderstanding question?und(DP*C)onQUD.
Integrating positiveanswertounderstanding-question Whenthesystemraises
anunderstanding question (e.g.bysaying\ToParis,isthatcorrect?"), theusercaneither
say\yes"or\no".(Thecasewheretheuserdoesnotgivearelevantanswertotheinter-
rogativefeedbackistreatedinSection3.6.8).InIBiS2,wedonotrepresentpropositions
relatedtotheunderstanding ofutterances inthesamewayasotherpropositions(which
arestoredin/shared/com ).Therefore, specialrulesareneededfordealingwithanswers
tounderstanding-questions.
Theruleforintegrating anegativeanswertoanunderstanding-question isshownin(rule
3.7).
(rule3.7)rule:integrateNegIcmAnsw er
class:integrate
pre:(
fst($/private/nim,answer(no))
fst($/shared/qud,und(DP*C))
eff:8
>>><
>>>:pop(/private/nim)
add(/shared/lu/moves,answer(und(DP*C)))
pop(/shared/qud)
push(/ private/agenda,icm:und*p os:DP*not(C))
Theconditions checkthatthere'sananswer(yes)moveonnimandanunderstanding-
question onQUD.The¯rstthreeupdatesestablish themoveassharedandpopthe
understanding-question o®QUD.Finally,positivefeedbackisselected toindicate that
thesystemhasundersto odthattheassumed interpretation Cwasincorrect.
Integrating positiveanswertounderstanding question Theruleforintegrating a
positiveanswertoanunderstanding-question isshownin(rule3.8).

116 CHAPTER 3.GROUNDING ISSUES
(rule3.8)rule:integratePosIcmAnsw er
class:integrate
pre:(
fst($/private/nim,answer(yes))
fst($/shared/qud,und(DP*Content))
eff:8
>>>>>>>>>>><
>>>>>>>>>>>:pop(/private/nim)
add(/shared/lu/moves,answer(und(DP*Content)))
pop(/shared/qud)
ifthenelse(Content=issue(Q),[
push(/ shared/qud,Q)
push(/ private/agenda,respond(Q))],
add(/shared/com,Content))
Theconditions andthe¯rstthreeupdatesaresimilartothoseintheintegrateNegIc-
mAnswerrule.The¯nal(conditionalized) updateintegrates thecontentC.Ifthe\orig-
inal"move(themovewhichcausedtheinterrogativ efeedbacktobeproducedinthe¯rst
place)wasask,Cwillbeapropositionissue(Q).Consequen tly,integrating thispropo-
sitionshasthesamee®ectsasintegrating anask-move:pushing thequestion QonQUD
andpushingtheactionrespond(Q)ontheagenda. Ifthepropositionisnotofthistype,it
issimplyaddedto/shared/com .
Dialogueexample: positiveandnegativeresponsetointerrogativ efeedbackIn
thefollowingdialogue, thesystemproducesinterrogativ eunderstanding feedbackfortwo
userutterances, onecontaininganaskmoveandtheothercontainingananswermove.The
¯rstinterrogativ efeedbackisansweredpositivelyandthesecondnegatively.
(dialogue 3.4)
U>priceinformation please[0.65]
getLatestMo ves2
666666664private=2
4agenda=hhii
plan =hi
nim =­­
ask(?A.price(A))®®3
5
shared =2
664com=fg
qud=hi
lu=·
speaker =usr
moves =fg¸3
7753
777777775
backupShared
selectIcmUndIn tAsk ½
pop(/private/nim)
push(/ private/agenda,icm:und*int:usr *issue(?A.price(A)))

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 117
selectIcmOther½push(nextmoves,icm:und*int:usr *issue(?A.price(A)))
del(/private/agenda,icm:und*int:usr *issue(?A.price(A)))
S>Youwanttoknowaboutprice,isthatcorrect?
getLatestMo ves
integrateUndIn tICM8
<
:pop(/private/nim)
add(/shared/lu/moves,icm:und*int:usr *issue(?A.price(A)))
push(/ shared/qud,und(usr*issue(?A.price(A))))
2
666666664private=2
4agenda=hhii
plan =hi
nim =hhii3
5
shared =2
664com=fg
qud=­
und(usr*issue(?A.price(A)))®
lu=·speaker =sys
moves =©
icm:und*int:usr *issue(?A.price(A))ª¸3
7753
777777775
U>yes
getLatestMo ves
integratePosIcmAnsw er8
>>>>>>>><
>>>>>>>>:pop(/private/nim)
add(/shared/lu/moves,answer(und(usr *issue(?A.price(A)))))
pop(/shared/qud)
ifthenelse(issue(?A.price(A))=issue(B),[
push(/ shared/qud,B)
push(/ private/agenda,respond(B))],
add(/shared/com,issue(?A.price(A))))
¯ndPlan
2
666666666666666666664private=2
6666666666664agenda=­­
icm:loadplan®®
plan =*¯ndout(?A.how(A))
¯ndout(?B.destcity(B))
¯ndout(?C.deptcity(C))
¯ndout(?D.month(D))
¯ndout(?E.deptday(E))
¯ndout(?F.class(F))
consultDB(? G.price(G))+
nim =hhii3
7777777777775
shared =2
664com=fg
qud=­?H.price(H)®
lu=·speaker =usr
moves =©
answer(und(usr *issue(?H.price(H))))ª¸3
7753
777777777777777777775
backupShared
selectFromPlan

118 CHAPTER 3.GROUNDING ISSUES
selectIcmOther
selectAsk
S>Letssee.Howdoyouwanttotravel?
getLatestMo ves
integrateOtherICM
integrateSysAsk
U>byplane[0.56](useractuallysaid\bytrain")
getLatestMo ves
backupShared
selectIcmUndIn tAnswer ½pop(/private/nim)
push(/ private/agenda,icm:und*int:usr *how(plane))
selectIcmOther
S>byflight,isthatcorrect?
getLatestMo ves
integrateUndIn tICM8
<
:pop(/private/nim)
add(/shared/lu/moves,icm:und*int:usr *how(plane))
push(/ shared/qud,und(usr*how(plane)) )
2
6666666666666666666666664private=2
6666666666664agenda=hhii
plan =*¯ndout(?A.how(A))
¯ndout(?B.destcity(B))
¯ndout(?C.deptcity(C))
¯ndout(?D.month(D))
¯ndout(?E.deptday(E))
¯ndout(?F.class(F))
consultDB(? G.price(G))+
nim =hhii3
7777777777775
shared =2
6666664com=fg
qud=*und(usr*how(plane))
?H.how(H)
?I.price(I)+
lu=·speaker =sys
moves =©
icm:und*int:usr *how(plane)ª¸3
77777753
7777777777777777777777775
U>no
getLatestMo ves
integrateNegIcmAnsw er

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 119
8
>><
>>:pop(/private/nim)
add(/shared/lu/moves,answer(und(usr *how(plane))) )
pop(/shared/qud)
push(/ private/agenda,icm:und*p os:usr*not(how(plane)) )
2
66666666666666666666664private=2
6666666666664agenda=­­icm:und*p os:usr*not(how(plane))®®
plan =*¯ndout(?A.how(A))
¯ndout(?B.destcity(B))
¯ndout(?C.deptcity(C))
¯ndout(?D.month(D))
¯ndout(?E.deptday(E))
¯ndout(?F.class(F))
consultDB(? G.price(G))+
nim =hhii3
7777777777775
shared =2
66664com=fg
qud=¿
?H.how(H)
?I.price(I)À
lu=·speaker =usr
moves =©answer(und(usr *how(plane)))ª¸3
777753
77777777777777777777775
backupShared
reraiseIssue
selectIcmOther½
push(nextmoves,icm:und*p os:usr*not(how(plane)) )
del(/private/agenda,icm:und*p os:usr*not(how(plane)) )
selectIcmOther
selectAsk
S>notbyflight. So,Howdoyouwanttotravel?
Negativecontactandperception levelfeedback
Whathappensifnosystemutterance isdetected, orifthespeechrecognizer fails?Most
speechrecognizers cantellthedi®erence betweennothearinganythingatall,andhearing
something butnotbeingabletocomeupwithanyhypothesisregarding whatwassaid.We
willusethisdistinction toenable IBiStoproducefeedbackonthecontactandperception
levels.
IfIBiSdoesnotreceiveanyinputwithinacertaintime-frame (speci¯edbythetimeout
TISvariable), itwillproducefeedbackindicating thatnothingwasperceived,e.g.\Ididn't
hearanythingfromyou.".Weclassifythisasnegativefeedbackonthecontactlevel.It
couldperhapsbearguedthatthedistinction betweencontactandperception levelfeedback
isnotverysharp,andthatthiskindoffeedbackactually concerns theperception level.
However,itispossiblethatthereasonthatnothingwasregistered bytherecognizer was
afailuretoestablish achannelofcommunication fromtheusertothesystem,e.g.ifa

120 CHAPTER 3.GROUNDING ISSUES
microphone isbrokenornotpluggedinproperly.
Ifsomething isdetected bythespeechrecognizer butitwasnotabletocomeupwitha
goodenoughguessaboutwhatwassaid,thesystemwillproducenegativefeedbackonthe
perception level,e.g.\Ididn'thearwhatyousaid.".
Wehavecon¯gured theinputmoduletosettheinputvariableto`TIMEDOUT'ifnothing
isdetected, andto`FAIL'ifsomething unrecognizable wasdetected.
NegativesystemcontactfeedbackIfthespeechrecognizer doesnotgetanyinput
withinacertaintimeframe(speci¯edbythetimeout TISvariable), theinputvariable
willbesetto`TIMEDOUT'bytheinputmodule.Theruleforselection ofnegativecontact
feedbackisshownin(rule3.9).
(rule3.9)rule:selectIcmConNeg
class:selecticm
pre:8
><
>:$input=`TIMEDOUT'
isempty($nextmoves)
isempty($/private/agenda)
eff:n
push(nextmoves,icm:con*neg )
Unlessthesystemhassomething elsetodo,thiswilltriggernegativecontactICMbythe
system,realisede.g.as\Ididn'thearanythingfromyou.".Thepurposeofthisisprimarily
toindicate totheuserthatnothingwasheard,butperhapsalsotoelicitsomeresponse
fromtheusertoshowthatsheisstillthere.Admittedly ,thisisaratherundeveloped
aspectofICMinthecurrentIBiSimplemen tation,andalternativ estrategies couldbe
explored. Forexample, thesystemcouldincrease thetimeoutspansuccessiv elyinsteadof
repeatingnegativecontactICMevery¯veseconds. Otherformulationswithmorefocuson
theeliciting function couldalsobeconsidered, e.g.\Areyouthere?"orsimply\Hello?".
Thesecondandthirdcondition checkthatnothingisontheagendaorinnextmoves.
Themotivationforthisisthatthereisnoreasontoaddresscontactexplicitly inthiscase,
sinceanyutterance fromthesystemimplicitly triestoestablish contact.
DefaultICMintegration ruleSincecontactisnotexplicitly representedintheinfor-
mationstateproper,integration ofnegativesystemcontactICMmoveshavenospeci¯c
e®ectontheinformation state,andaretherefore integrated bythedefaultICMintegration
ruleshownin(rule3.10).UnlessanICMmovehasaspeci¯cintegration rulede¯nedfor
it,itwillbeintegrated bythisrule.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 121
(rule3.10) rule:integrateOtherICM
class:integrate
pre:n
fst($/private/nim,icm:A)
eff:(
pop(/private/nim)
add(/shared/lu/moves,icm:A)
Thecondition andupdatesinthisrulearestraightforward.
Negativesystemperception feedbackIfthespeechrecognizer getssomeinputfrom
theuserbutisnotabletoreliably¯gureoutwhatwassaid(therecognition scoremaybe
toolow),theinputvariablegetssetto`FAIL'.Thiswilltriggernegativeperception ICM,
e.g.\Ididn'thearwhatyousaid".
(rule3.11) rule:selectIcmP erNeg
class:selecticm
pre:(
$input='FAIL'
notin($nextmoves,icm:per*neg)
eff:n
push(nextmoves,icm:per*neg)
Thepurposeofthesecondcondition istopreventselecting negativeperception feedback
morethanonceintheselection phase.Aswithnegativesystemcontactfeedback,negative
systemperception feedbackisintegrated bytheintegrateOtherICM rule.
Negativeunderstanding levelfeedback
Negativefeedbackcanconcerneitherofthetwosublevelsoftheunderstanding level:se-
manticandpragmatic understanding.
Negativesystemsemanticunderstanding feedbackIfsomeinputisrecognized
bytherecognition module,theinterpretation modulewilltryto¯ndaninterpretation
oftheinput.Ifthisfails,thelatestmovesgetssettofailedwhichtriggersselection
ofnegativesemanticunderstanding feedback(e.g.\Idon'tunderstand"). Inaddition,
positiveperception feedback(e.g.\Iheard`perish'")isproducedtoindicate totheuser
whatthesystemthoughtshesaid.

122 CHAPTER 3.GROUNDING ISSUES
Thiswillonlyoccuriftherecognition lexiconcoverssentencesnotcoveredbytheinter-
pretation lexicon.
(rule3.12) rule:selectIcmSemNeg
class:selecticm
pre:8
><
>:$latestmoves=failed
$input=String
notin($nextmoves,icm:sem*neg )
eff:(
push(nextmoves,icm:per*pos:String)
push(nextmoves,icm:sem*neg )
Thepurposeofthethirdcondition istopreventnegativesemanticunderstanding feedback
frombeingselected morethanonetime.Sinceonlyonestringisrecognized perturn,
thereisneveranyreasontoapplytherulemorethanonce;andifanythingatallcanbe
interpreted, therulewillnottriggeratallevenifsomematerial wasnotusedininterpreta-
tion.Inasystemwithawide-coveragerecognizer andamoresophisticated interpretation
module,onemayconsider producingnegativesemanticunderstanding feedbackforany
material whichcannotbeinterpreted (e.g.\Iunderstand thatyouwanttogotoParis,
butIdon'tunderstand whatyoumeanby`Londres'.").
The¯rstupdateinthisruleselectspositiveperception ICMtoshowtheuserwhatthe
systemheard.Thesecondupdateselectsnegativesemanticunderstanding ICM.
Negativesystempragmatic understanding feedbackThesystemwilltrytointe-
gratethemovesaccording totherulesaboveinSection3.6.7.Ifthisfails(iftherearestill
moveswhichhavenotbeenintegrated), therulein(rule3.13)willbetriggered anda
icm:und*neg -movewillbeselectedbythesystem.However,ifthereasonthatthemovewas
notintegrated isthatithadalowscoreorwasnotacceptable tothesystem,interrogativ e
understanding feedback(Section 3.6.6)ornegativeacceptance feedback(Section 3.6.6),
respectively,willinsteadbeselectedandthemovewillbepoppedo®nimbeforetherule
in(rule3.13)istried.
InIBiS,onlyask-movescanbeirrelevant.Othermoves,including ask,donothaveany
relevancerequiremen ts.Thismeansthatanswermovesaretheonlymovesthatcanfail
tobeundersto odonthepragmatic level,giventhattheyhavebeenundersto odonthe
semanticlevel.Also,foranutterance tobecompletely irrelevant,nopartofitmusthave
beenintegrated. Forthesereasons, therulein(rule3.13)willtriggeronlyifnomove
inthelatestutterance wasintegrated, andtheutterance wasinterpreted ascontainingat
leastoneanswer-move.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 123
(rule3.13) rule:selectIcmUndNeg
class:selecticm
pre:8
>>>>>>>><
>>>>>>>>:notin($nextmoves,icm:und*neg )
in($latestmoves,answer(A))
forall($ latestmoves/elem=Move,
$/private/nim/elem=Move)
forall($ latestmoves/elem=answer(A0),
notfst($/shared/qud,D)and$domain ::relevant(A0,Q))
eff:8
><
>:foralldo($latestmoves/elem=Move,
push(nextmoves,icm:sem*p os:Move))
push(nextmoves,icm:und*neg )
The¯rstrulechecksthatnegativepragmatic understanding feedbackhasnotalreadybeen
selected. Thesecondcondition checksthatthelatestutterance containedananswermove,
andthethirdchecksthatnoneofthemovesperformed inthelatestutterance hasbeen
integrated; allmovesinlatestmovesarestillonnim.Finally,thefourthcondition
checksthatnoanswerisrelevanttoanyquestion onQUD.
The¯rstupdateselectspositivefeedbackonthesemanticunderstanding levelforeachmove
performed inthelatestutterance, toshowthattheutterance wasatleastundersto odto
someextent.Thesecondupdateselectsnegativefeedbackandpushesitonnextmoves.
Thesystemisthusabletomakeadistinction betweenutterances itcannotinterpret(and
thusnotground), andutterances thatitcaninterpretandgroundbutnotintegrate. The
rulein(3.15)triggerswhenintegration failsbecausethesystemcannotseetherelevance
oftheuserutterance inthecurrentdialogue context.Negativepragmatic understanding
feedbackiscurrentlyrealizedas\Idon'tquiteunderstand"; theideaistoindicate that
theutterance wasalmostfullyundersto od,butnotquite.Again,itcanbearguedwhat
thebestrealization is.
Dialogue example: negativesystemcontact,perception, andunderstanding
feedbackInthisdialogue, weseeexamples ofnegativesystemfeedbackonthecontact,
perception, andunderstanding (bothsemanticandpragmatic) levels.(Sincethisdialogue
usesthetext-based inputmodule,wehavesimulatedtimeoutandrecognition failure.)
(dialogue 3.5)
S>Welcome tothetravelagency!
U>'TIMED_OUT'

124 CHAPTER 3.GROUNDING ISSUES
getLatestMo ves
integrateNoMo ve©
pop(/private/nim)
selectIcmConNeg©
push(nextmoves,icm:con*neg )
S>Ididnthearanything fromyou.
getLatestMo ves
integrateOtherICM©
pop(/private/nim)
U>'FAIL'
backupShared
selectIcmP erNeg©
push(nextmoves,icm:per*neg)
S>Sorry,Ididnthearwhatyousaid.
getLatestMo ves
integrateOtherICM©
pop(/private/nim)
U>jfdbhajhdgarbledfdasd
backupShared
selectIcmSemNeg
S>Iheardyousayjfdbhajhdgarbledfdasd. Sorry,Idontunderstand.
getLatestMo ves
integrateOtherICM©
pop(/private/nim)
integrateOtherICM©
pop(/private/nim)
U>paris
getLatestMo ves
backupShared
selectIcmUndNeg

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 125
8
>>>><
>>>>:foralldo($/shared/lu/moves/elem=A,push(nextmoves,icm:sem*p os:A))
push(nextmoves,icm:und*neg )
foralldo(in($/ shared/lu/moves,E)andE=answer(C)and$lexicon ::ynanswer(C)and
in($/private/nim,E),
del(/private/nim,E))
S>paris.Idontquiteunderstand.
getLatestMo ves
integrateOtherICM©
pop(/private/nim)
integrateOtherICM©pop(/private/nim)
Negativereactionlevelfeedback
Tobeabletodistinguish relevantbutnon-integratable utterances fromutterances which
arebothrelevantandintegratable, adialogue systemingeneralneedstobeabletodistin-
guishbetweenrelevanceandintegratabilit y(acceptabilit y),i.e.itneedstounderstand the
relevanceofutterances thatitcannotintegrate.
Systemproposition-rejection Inaddition toissue-rejection, proposition-rejection is
alsoarguably relevanttoadialogue system. Acaseinpointiswhentheusersupplies
information whichresultsinaninvaliddatabase query,i.e.aquerywhichwouldyieldno
results.Anexample isgivenin(dialogue 3.6)(understanding-feedbac khasbeenremoved
forreadabilit y).
(dialogue 3.6)
U(1)>Priceinformation please
S(1)>OK.Wheredoyouwanttotravel?
U(2)>toParis
S(2)>OK.Whatcityyouwanttotravelfrom?
U(3)>Oslo
S(3)>Oslo.Sorry,therearenoflights matching yourspecification.
However,thiscaseisabitmoreproblematic -isS(3)reallyarejection ofU(3),orshould
itberegarded asanegativeanswertotheuser'squeryinU(1)?Webelieveitmakesmore
sensetodothelatter.Onthisview,theissueofpricewillberegarded as(negatively)
resolvedafterS(3).(Notethatwearehereassuming thatOsloisinfactavaliddeparture

126 CHAPTER 3.GROUNDING ISSUES
city,buttherehappentobeno°ightsfromOslotoParisinthedatabase.)
Avariantofthedialogue in(dialogue 3.6)thatisperhapsabettercaseofrejection is
wheretheusersupplies adestination whichisnotavailableinthedatabase. Inthiscase,
itseemstomakesensetosaythatitisindeedtheutterance containingtheinformation
aboutthedestination thatisrejected.
(dialogue 3.7)
U(1)>Priceinformation please
S(1)>OK.Wheredoyouwanttotravel?
U(2)>toParis
S(2)>OK.Whatcityyouwanttotravelfrom?
U(3)>KualaLumpur
S(3)>Sorry,KualaLumpurisnotinthedatabase. So,Whatcitydoyou
wanttotravelfrom?12
Inthiscase,theissueofpriceisstillunresolved,asistheissueofdestination city.Tohandle
adialogue likethatin(dialogue 3.7),asystemagainneedstobeabletorecognize relevant
information thatitcannotdealwith,anddistinguish itfromsuchinformation thatitcan
dealwith.Onewayofdoingthisistoencoderelevantinformation inthedomainknowledge
resource thatisnotnecessarily inthedatabase. Ifauserutterance thatcontainsarelevant
answerorassertion isperceivedandundersto od,thesystemshouldperformadatabase
searchtocheckifitisabletodealwiththatinformation; ifnot,theuser'sutterance should
berejected.
Ofcourse,itisawell-knownproblem thatbiggervocabularies makespeechrecognition
harder,andconsequen tlythere'satradeo®betweenrecognizing anddealingcorrectly with
non-acceptable information, andgettingtheacceptable information right.Possibly,one
couldusecollected dialogues inadomaintodecidehowmuchnon-acceptable information
thesystemshouldbeabletorecognize andunderstand.
InIBiS,wehaveimplemen tedtheabilitytorejectuseranswersbycheckingwhether
theyprovidevaliddatabase parameters. Thisrequires anadditional database resource
condition \validDBparameter( P)"whichistrueifPisavalidparameter inthedatabase.
Forexample, ifatravelagencydatabase contains°ightswithinEurope,anydestination
outsideEuropeisaninvaliddatabase parameter andshouldberejected bythesystem.
12Optionally ,onemightwantasystemtobemorehelpfulando®erasuitablealternativ edestination.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 127
(rule3.14) rule:rejectProp
class:selectaction
pre:8
>>>>>>>><
>>>>>>>>:in($/private/nim,answer(A))
$/shared/lu/speaker =usr
fst($/shared/qud,Q)
$domain ::relevant(A,Q)
$domain ::combine(Q,A,P)
not$database::validDBparameter( P)
eff:8
><
>:del(/private/nim,answer(A))
push(/ private/agenda,icm:und*p os:usr*P)
push(/ private/agenda,icm:acc*neg :P)
The¯rst¯veconditions areidenticaltothosefortheruleforintegrating useranswers,
integrateUsrAnsw er(Section 3.6.6).The¯nalcondition checksthatthepropositionP,
resulting fromcombiningaquestion onQUDwiththecontentoftheanswermove,isnot
avaliddatabase parameter. Theupdatesremovethemovefromnimandselectspositive
understanding feedbacktoshowwhatthesystemundersto od,andnegativeacceptance
feedback.
Ofcourse,itisnotoptimally e±cientthatthesamesequence ofconditions ischeckedby
severaldi®erentrules;analternativ eapproachwouldbetoletoneruledetermine e.g.how
ananswermoveisrelevant,combine itwithaquestion onQUD,andstoretheresultin
adatastructure containingpragmatically interpreted material. Thisdatastructure could
thenbeinspectedbybothintegration andrejection rules.(SeealsoSection6.5.1.)
Dialogue example: systempropositionrejection Inthefollowingdialogue, weil-
lustratesystemrejection ofthepropositionthatthemeansoftransporttosearchforwill
betrain.Amotivationisalsogivenbythesystem,i.e.that\train"isnotavailableasa
meansoftransportinthedatabase.
(dialogue 3.8)
S>Okay.Ineedsomeinformation. Howdoyouwanttotravel?
getLatestMo ves
integrateOtherICM
integrateOtherICM
integrateSysAsk
U>trainplease

128 CHAPTER 3.GROUNDING ISSUES
getLatestMo ves
backupShared
rejectProp8
<
:del(/private/nim,answer(train))
push(/ private/agenda,icm:und*p os:usr*how(train))
push(/ private/agenda,icm:acc*neg :how(train))
selectIcmOther½
push(nextmoves,icm:und*p os:usr*how(train))
del(/private/agenda,icm:und*p os:usr*how(train))
selectIcmOther½push(nextmoves,icm:acc*neg :how(train))
del(/private/agenda,icm:acc*neg :how(train))
S>bytrain.Sorry, bytrainisnotinthedatabase.
getLatestMo ves
integrateOtherICM
integrateOtherICM
Systemissue-rejection Forexample, thesystemmightknowsomequestions whichare
relevantinacertainactivity,butnotbeabletoanswerthem.Thisisnotusuallythe
casewithexistingdialogue systems. Forexample, theSwedishrailwayinformation system
(basedonthePhilipsdialogsystem(Austetal.,1994)cannotanswerquestions about
theavailabilityofacafeteria onatrain.Ifthisquestion isasked,thesystemwilltryto
interpretitasananswertosomething itjustaskedabout(asillustrated inthemade-up
dialogue (3.16)). Butonecouldimagine asystemthatwouldhaveastoreofpotentially
relevantquestions whichitcannothandle,enabling ittorespondtosuchquestions ina
moreappropriate way,e.g.bysaying\Sorry,Icannotanswerthatquestion". Thiswould
constitute arejection (anissue-rejection, tobeprecise)ofaquestion whosemeaning has
beenundersto od.An(made-up) example isshownin(3.17).
(3.16)U:Isthereacafeteria onthetrain?
S:YouwanttotraveltoSiberia,isthatcorrect?
(3.17)U:Isthereacafeteria onthetrain?
S:Sorry,Icannotanswerquestions aboutcafeteria availability.
Issuerejection hasbeenimplemen tedinIBiS2forthetravelagencydomain; inthetravel
agencydomain, thesystemwillrecognize andunderstand, butreject,questions about
connecting °ights.Apossibleextension ofthiswouldbetomakethesystemmorehelpful
andmakeitexplainwhyitcannotanswerthequestion; thishasnotyetbeendoneinIBiS.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 129
Incasethesystemhasinterpreted auserutterance asanask-movewithcontentq,butthe
systemdoesnothaveaplanfordealingwithq,thesystemmustrejectqandindicate this
totheuserusingappropriate feedback.Thisruleallowsthesystemtorespondintelligently
touserquestions evenifitcannotanswerthem(giventhattheycanberecognized and
interpreted).
(rule3.15) rule:rejectIssue
class:selectaction
pre:8
><
>:in($/private/nim,ask(Q))
$/shared/lu/speaker =usr
not$domain ::plan(Q,Plan)
eff:8
><
>:del(/private/nim,ask(Q))
push(/ private/agenda,icm:und*p os:usr*issue(Q))
push(/ private/agenda,icm:acc*neg :issue(Q))
TheruleissimilartotherejectProp rule.Thethirdcondition checksthatthereisno
planfordealingwiththequestion Q.
Dialogue example: systemissuerejection Inthefollowingdialogue, theuser'sre-
questforinformation aboutconnecting °ightsisrejected onthegrounds thatthesystem
doesnotknowhowtoaddressthatissue.
(dialogue 3.9)
S>Okay. Thepriceis123crowns.
U>whataboutconnecting flights
getLatestMo ves
backupShared
rejectIssue8
<
:del(/private/nim,ask(?A.con°ight(A)))
push(/ private/agenda,)
push(/ private/agenda,icm:acc*neg :issue(?A.con°ight(A)))
selectIcmOther½
push(nextmoves,icm:und*p os:usr*issue(? A.con°ight(A)))
del(/private/agenda,icm:und*p os:usr*issue(? A.con°ight(A)))
selectIcmOther½push(nextmoves,icm:acc*neg :issue(?A.con°ight(A)))
del(/private/agenda,icm:acc*neg :issue(?A.con°ight(A)))
S>Youaskedaboutconnecting flights. Sorry,Icannotanswerquestions

130 CHAPTER 3.GROUNDING ISSUES
aboutconnecting flights.
getLatestMo ves
integrateOtherICM
integrateOtherICM
3.6.7Grounding ofsystemutterances inIBiS2
Inthissection,weshowhowacautiously optimistic grounding strategy forsystemutter-
anceshasbeenimplemen tedinIBiS2.We¯rstpresentbasicupdaterulesre°ecting the
cautious strategy.Wethenpresentintegration rulesforthe\core"systemdialogue moves
(askandanswer),anddescribetherulesforintegrating userfeedbacktosystemmoves.
Enabling cautiousupdates
IBiS2usesamixofvariousgrounding strategies. Forsystemutterances, acautiously
optimistic strategy isused.
MovinglatestmovestonimTheIBiS2versionoftheupdaterulegetLatestMo ves
isshownin(rule3.16).
(rule3.16) rule:getLatestMo ves
class:grounding
pre:8
><
>:$latestmoves=Moves
$latestspeaker =DP
$/shared/lu/moves=PrevMoves
eff:8
>>><
>>>:set(/private/nim,Moves)
set(/shared/lu/speaker ,DP)
clear(/ shared/lu/moves)
set(/shared/pm,PrevMoves)
Theruleloadsinformation regarding thelatestutterance performed intonimandcopies
thepreviously grounded moves(in/shared/lu/mo ves)tothe/shared/pm ¯eld.Note
thatthisrulehaschangedsigni¯can tlycompared toIBiS1;nooptimistic assumption
aboutunderstanding ofthelatestutterance ismadehere.Insteadofputtingthelatest
movesin/shared/lu/mo ves,whichwouldbetoassumethattheyhavebeenmutually

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 131
understo od,IBiS2clears/shared/lu/mo vessothatmovescanbeaddedwhentheyare
actually integrated; onlythenaretheyassumed tobeundersto od.
Savingpreviousstatebeforeintegration Beforeselecting, producing,andintegrat-
inganewsystemutterance, therulein(rule3.17)copiesrelevantpartsoftheIStothe
tmp¯eld.Thismakesitpossibletobacktracktoaprevious state,shouldtheoptimistic
grounding assumptions concerning asystemmoveturnouttobemistaken.Thismeans
thatanyoptimistic updatesassociatedwithintegration ofsystemmovesarenowcautiously
optimistic.
(rule3.17) rule:backupShared
class:none
pre:f
eff:8
>>><
>>>:/private/tmp/qud:=$/shared/qud
/private/tmp/com:=$/shared/com
/private/tmp/agenda:=$/private/agenda
/private/tmp/plan:=$/private/plan
Therearenoconditions onthisrule.Itisexecuted atthestartoftheselection algorithm
describedinSection3.7,andisthusonlycalledbeforesystemutterances.
Cautiously optimistic integration ofsystemmoves
Forsystemaskandanswermoves,theintegration rulesaresimilartothoseinIBiS1;
however,ratherthanpickingoutmovesfrom/shared/lu/mo ves,IBiS2picksmoves
from/private/nimandaddsthemto/shared/lu/mo ves,therebyassuming grounding
ontheunderstanding level,onlyinconnection withintegration. Sinceoptimistic grounding
isassumed forsystemmoves,itwouldbeokaytohandlethemthesamewaywedid
inIBiS1;however,usermovesarenolonger(always)optimistically grounded, andwe
havechosentogiveauniform treatmen ttoallmoves.SinceinIBiSsystemmovesare
alwayssuccessfully integrated, however,thereisnorealdi®erence betweenthewaythey
arehandled inIBiS1andIBiS2.

132 CHAPTER 3.GROUNDING ISSUES
(rule3.18) rule:integrateSysAsk
class:integrate
pre:(
$/shared/lu/speaker ==sys
fst($/private/nim,ask(A))
eff:8
><
>:pop(/private/nim)
add(/shared/lu/moves,ask(A))
push(/ shared/qud,A)
(rule3.19) rule:integrateSysAnsw er
class:integrate
pre:8
>>>>>><
>>>>>>:fst($/private/nim,answer(A))
$/shared/lu/speaker ==sys
$domain ::proposition( A)
fst($/shared/qud,B)
$domain ::relevant(A,B)
eff:8
><
>:pop(/private/nim)
add(/shared/lu/moves,answer(A))
add(/shared/com,A)
Onecomplication isthatinIBiS2,severalmovesmaybeperformed inasingleutter-
ance.Tokeeptrackofwhichutterances havebeenintegrated, the/private/nim stack
ofnon-integrated movesispoppedforeachmovethatgetsintegrated. Notealsothat
eachintegrated (andthusundersto od)moveisaddedto/shared/lu/mo ves(whereas in
IBiS1thiswasdoneatthestartoftheupdatecycle).
Thecautiously optimistic acceptance assumptions builtintotheserulescanberetracted
onintegration ofnegativeuserperception feedback,asexplained inSection3.6.6,oron
negativeuserintegration feedback,asshowinSection3.6.7.Dialogue examples involving
therulesshownabovewillbegiveninthesesections.
Userfeedbacktosystemutterances
Inthissectionwereviewuserfeedbacktosystemutterances andhowthesea®ectthe
optimistic grounding assumptions.
Negativeuserperception feedbackIfthesystemmakesanutterance, itwillassume
itisgrounded andaccepted. Iftheuserindicates thatshedidnotunderstand theutterance,
therulein(rule3.20)makesitpossibletoretractthee®ectsofthesystem's latestmove,
thuscancelling theassumptions ofgrounding andacceptance.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 133
(rule3.20) rule:integrateUsrP erNegICM
class:integrate
pre:(
$/shared/lu/speaker ==usr
fst($/private/nim,icm:per*neg)
eff:8
>>>>>><
>>>>>>:pop(/private/nim)
/shared/qud:=$/private/tmp/qud
/shared/com:=$/private/tmp/com
/private/agenda:=$/private/tmp/agenda
/private/plan:=$/private/tmp/plan
Thefourlastupdatesrevertthecom,qud,planandagenda¯eldstothevaluesstored
in/private/tmp.
Dialogue example: negativeuserperception feedbackThisdialogue showshow
IBiS2isabletoreacttonegativeuserperception feedback(e.g.\pardon") byretracting
theoptimistic grounding assumption bybacktrackingrelevantpartsofshared tothestate
in/private/tmp/sys ,storedbeforethesystemutterance wasgenerated. Also,theplan
andagendaarebacktrackedtoenablethesystemtocontinuethedialogue properly.
(dialogue 3.10)
S>Okay.Youaskedaboutprice. Ineedsomeinformation. Howdoyouwant
totravel?
getLatestMo ves
integrateOtherICM
integrateOtherICM
integrateOtherICM
integrateSysAsk

134 CHAPTER 3.GROUNDING ISSUES
2
666666666666666666666666666666666666666666666666664pr.=2
666666666666666666666666666666666666664agenda=hhii
plan =*¯ndout(?A.how(A))
¯ndout(?B.destcity(B))
¯ndout(?C.deptcity(C))
¯ndout(?D.month(D))
¯ndout(?E.deptday(E))
¯ndout(?F.class(F))
consultDB(? G.price(G))+
bel =fg
tmp =2
6666666666666666664com =fg
qud =­
?H.price(H)®
agenda=**icm:acc*p os
icm:und*p os:usr*issue(?H.price(H))
icm:loadplan++
plan =*¯ndout(?A.how(A))
¯ndout(?B.destcity(B))
¯ndout(?C.deptcity(C))
¯ndout(?D.month(D))
¯ndout(?E.deptday(E))
¯ndout(?F.class(F))
consultDB(? G.price(G))+3
7777777777777777775
nim =hhii3
777777777777777777777777777777777777775
sh.=2
6666664com=fg
qud=¿?I.how(I)
?H.price(H)À
lu=·speaker =sys
moves =­­icm:acc*p os,:::®®¸
pm=­­
ask(?H.price(H))®®3
77777753
777777777777777777777777777777777777777777777777775
U>pardon
getLatestMo ves
integrateUsrP erNegICM8
>>>><
>>>>:pop(/private/nim)
/shared/qud:=$/private/tmp/qud
/shared/com:=$/private/tmp/com
/private/agenda:=$/private/tmp/agenda
/private/plan:=$/private/tmp/plan

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 135
2
6666666666666666666666666666664private=2
666666666666666666664agenda=**icm:acc*p os
icm:und*p os:usr*issue(?A.price(A))
icm:loadplan++
plan =*¯ndout(?B.how(B))
¯ndout(?C.destcity(C))
¯ndout(?D.deptcity(D))
¯ndout(?E.month(E))
¯ndout(?F.deptday(F))
¯ndout(?G.class(G))
consultDB(? H.price(H))+
bel =fg
tmp =:::
nim =hhii3
777777777777777777775
shared =2
66664com=fg
qud=­?A.price(A)®
lu=·
speaker =usr
moves =oqueue([icm:p er*neg])¸
pm=:::3
777753
7777777777777777777777777777775
backupShared
selectFromPlan
selectIcmOther
selectIcmOther
selectIcmOther
selectAsk
S>Okay.Youaskedaboutprice. Ineedsomeinformation. Howdoyouwant
totravel?
Explicituserissuerejection Therulein(rule3.21)allowstheusertorejectasystem
question (byindicating inabilitytoanswer,i.e.byuttering \Idon'tknow"orsimilar). If
thisisdone,theoptimistic grounding updateisretracted byrestoring thesharedparts
storedinnim,i.e.qudandcom,totheirprevious states.
(rule3.21) rule:integrateUsrAccNegICM
class:integrate
pre:8
><
>:$/shared/lu/speaker ==usr
fst($/private/nim,icm:acc*neg :issue)
in($/shared/pm,ask(Q))
eff:8
>>><
>>>:pop(/private/nim)
add(/shared/lu/moves,icm:acc*neg :issue)
/shared/qud:=$/private/tmp/qud
/shared/com:=$/private/tmp/com

136 CHAPTER 3.GROUNDING ISSUES
Thethirdcondition checksthattheprevious utterance containedanaskmove.The¯nal
twoupdatesretracttheoptimistic grounding assumption ontheintegration /acceptance
/reaction level.
Ofcourse,ifaquestion isrejected bytheuserthismayresultinafaileddatabase query
(unlessthealternativ edatabase accessmethoddescribedinSection2.12.4isused).But
howshouldasystemreactiftheuserrejectsasystemquestion? Insomeframe-based
dialogue systemsfordatabase search(e.g.Chu-Carroll, 2000),¯eldsintheframecanbe
labelledasobligatory oroptional. InIBiS,thiscorrespondsroughlytothedistinction
betweentheraiseand¯ndoutactions;theformerhassucceeded assoonasthesystemasks
thequestion, whereasthelatterrequiresthequestion toberesolved.Soifaquestion which
wasraisedbyaraiseactionwasrejected, itwillnotbeaskedagain.Questions raisedby
¯ndoutactions,however,willcurrentlyberaisedagainbyIBiS2immediately afterauser
rejection, sincetheactionisstillontopoftheplan.Thisisperhapsnotverycooperative,
andalternativ estrategies needtobeexplored. Forexample, the¯ndoutactioncouldbe
movedfurtherdownintheplansothatitwillnotbeaskedimmediately again,oritmay
beraisedagainonlyifthedatabase searchfails.
Dialogueexample: explicituserissuerejection Inthefollowingdialogue example,
theuserrejectsthesystemquestion regarding howtotravel.Inthisexample, theplanhas
beenalteredsothat¯ndout(?x.class(x))hasbeenreplaced byraise(?x.class(x)),thereby
makingtheclass-question optional. Also,thealternativ edatabase accessmethoddescribed
inSection2.12.4isused.
(dialogue 3.11)
S>Whatclassdidyouhaveinmind?
getLatestMo ves
integrateSysAsk½
pop(/private/nim)
push(/ shared/qud,?A.class(A))

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 137
2
666666666666666666666666666666666666664private=2
666666666666666666664agenda=hhii
plan =¿
raise(?A.class(A))
consultDB(? B.price(B))À
bel =fg
tmp =2
66666666664com =8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;
qud =­
?C.price(C)®
agenda=hhii
plan =¿
raise(?A.class(A))
consultDB(? B.price(B))À3
77777777775
nim =hhii3
777777777777777777775
shared =2
6666666666664com=8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;
qud=¿?D.class(D)
?C.price(C)À
lu=·speaker =sys
moves =­­
ask(?D.class(D))®®¸
pm=­­
icm:acc*neg :issue®®3
77777777777753
777777777777777777777777777777777777775
U>itdoesntmatter
getLatestMo ves
integrateUsrAccNegICM8
>><
>>:pop(/private/nim)
add(/shared/lu/moves,icm:acc*neg :issue)
/shared/qud:=$/private/tmp/qud
/shared/com:=$/private/tmp/com
execconsultDB

138 CHAPTER 3.GROUNDING ISSUES
2
666666666666666666666666666666666666666666664pr.=2
66666666666666666666666666664bel=8
>>>>>>>>>><
>>>>>>>>>>:dbentry(8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;,fclass(economy )g,price(123))
dbentry(8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;,fclass(business) g,price(1234))9
>>>>>>>>>>=
>>>>>>>>>>;
tmp=2
66666666664com =8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;
qud =­
?B.price(B)®
agenda=hhii
plan =¿raise(?C.class(C))
consultDB(? D.price(D))À3
77777777775
nim=hhii3
77777777777777777777777777775
sh.=2
66666666664com=8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;
qud=­
?B.price(B)®
lu=·speaker =usr
moves =­­
icm:acc*neg :issue®®¸
pm=­­ask(?C.class(C))®®3
777777777753
777777777777777777777777777777777777777777775
backupShared
selectResp ond
selectAnsw er
S>Thepriceis123crowns. cheap. Thepriceis1234crowns.
business class.
3.6.8Evidence requiremen tsandimplicitgrounding
Inthissection,wediscussevidence requiremen tsforgrounding andhowthesehavebeen
implemen tedintheformofupdaterulesforimplicitgrounding.
InIBiS2weuseacautiously optimistic grounding strategy forsystemutterances. This
assumption canberetracted ifnegativeevidence concerning grounding isfound.So,what
countsasnegativeandpositiveevidence? RecallClark'sranking ofdi®erentformsof
positiveevidence, rangingfromweakesttostrongest:

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 139
²Continuedattention
²Relevantnextcontribution
²Acknowledgemen t:\uh-huh",nodding,etc.
²Demonstration: reformulation,collaborativecompletion
²Display:verbatimdisplayofpresentation
Regarding theattentionlevel,wewillnothavemuchtosay13.Thelevelsofacknowl-
edgemen t,demonstration anddisplayarepresumably whatwewouldregardasexplicit
feedback,although wehavebeenmainlyconcerned withtheacknowledgemen tlevel.
Evidence andrelevance
Theremaining levelinClark'stypologyofevidence ofunderstanding is\relevantnext
contribution". Twoquestions arisehere.First,whatcountsasarelevantfollowup?Second,
ifnorelevantfollowupisproduced,shouldthiscountasnegativeevidence ofgrounding,
andifso,onwhatactionlevel?
Apropertyofdialogue systems sometimes discussed intheliterature (TheDISCconsor-
tium,1999,Bohlinetal.,1999)istheabilityofasystemtounderstand andintegrate
information di®erentfromthatwhichwasrequested bythesystem. Howdoesthisrelate
torelevanceandgrounding? Onewaytoformulatetheproblem isthis:ifthesystemjust
askedq,andtheuser'sresponseudidnotcontainananswerrelevanttoqorfeedback
concerning theuser'sutterance, whatshouldbeassumed aboutthegrounding statusofq?
Thisis,ofcourse,alsoaproblem thathumanDPsmustresolve;however,Clarkdoesnot
(toourknowledge)directlydiscussthiscase.
(3.18)a.A:Whatcitydoyouwanttogoto?[askq]
B:I'dliketotravelinApril[answerotherquestion]
b.A:Whatcitydoyouwanttogoto?[askq]
B:Doyouhaveastudentdiscount?[askotherquestion]
13Clarkincludes \continuedattention"astheweakestformofpositiveevidence ofgrounding. However,
inprinciple continuedattentionfromanaddresseeAafteranutteranceuisconsisten twithacomplete
lackofperception onA'sside;Amaynotevenhaveperceivedubutisstillwaitingforthenextutterance.
Whilethisexample maynotbeveryrelevantforhuman-humancommunication, itisnotacompletely
unlikelyscenario ifAisadialogue system.Also,contactlevelfeedbackappearsrelatedtothis.

140 CHAPTER 3.GROUNDING ISSUES
Regarding caseswhereaquestion isignored(i.e.neitheraddressed byarelevantanswer,
explicitly accepted, norexplicitly rejected), itisnotobviouswhether thequestion was
accepted ornot.Thereasonisthatthereareseveralpossibleexplanations forthisbe-
haviour:onecomplies silentlywiththequestion butthinksthatotherinformation ismore
importantrightnow(inwhichcasethequestion wasintegrated bythehearer,andwillbe
answeredeventually),oronemisheard ordidnothearthequestion atall(inwhichcase
itwasnotundersto od,andthusneitheraccepted orrejected), oronedoesnotthinkthat
thequestion isappropriate (inwhichcasethequestion wasimplicitly rejected).
Onepossiblestrategy for¯ndingnegativeevidence istolookforsignsofmisunderstanding,
andtotrytocomeupwithaplausible explanation forhowthismisunderstanding came
about.Thisis,however,afairlydi±culttaskevenforhumansandnotoneweintendto
explorehere.
Caseswhereaquestion isnotfollowedbyarelevantanswerorrelevantICM,canbe
regarded asimplicit rejections ofthatquestion. However,ifthefollowupisrelevantin
someotherwaytothequestion asked,thisshouldnotberegarded asrejection. Onetype
ofrelevantfollowupcanbede¯nedusingGinzburg's notionofquestion dependence:
(3.19)Anask-movewithcontentqisarelevantfollowuptoanask-move
withcontentq0ifq0dependsonq.
InSection2.8.2,wede¯nedadomain-dep endentnotionofquestion dependence relatedto
termsofplans,whereq0dependsonqifthereisaplanfordealingwithq0whichincludes
anaction¯ndout( q).
Consequen tly,inIBiS2wehavechosenthefollowingrequiremen tsonanutterance uto
countasanirrelevantfollowuptoanutterance raisingaquestion q:
²ucontainsnoICM
²theprevious moveraisedaquestion q
²ucontainsnoanswertoq
²ucontainsnoask-moveraisingaquestion q0suchthatqdependsonq0
Concerning oursecondquestion, areirrelevantfollowupstoberegarded asnegativeground-
ingevidence? OrcoulditbethecasethataDPundersto odandaccepted anutterance u
butoptedtochangethesubjecttemporarily,planning torespondtoueventually?
Iftheirrelevantfollowupisinterpreted asnegativegrounding evidence, howdoweknow
whatactionlevelisconcerned? Didtheuserimplicitly rejecttheissuebyignoring it,or

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 141
didshesimplynotperceiveorunderstand it?Wesuspectthatthechoicebetweenthese
twointerpretations mightdependonquitesubtleissuesconcerning timing.Forexample,
iftheuser'sfollowupoverlapswiththesystem's question itispossiblethattheuserhas
notevenheardthesystem's question.
InIBiS2wehavechosentoconsider irrelevantfollowupstosystemaskmovesasimplicit
rejections. However,thischoiceisnotobviousandisafurthertopicforfutureresearch.
Implicituserrejectionofissue
Ifanirrelevantfollowupisdetected, thisisinterpreted asanimplicitissuerejection and
consequen tlytheoptimistic assumption thatthequestion q0wasintegrated bytheuseris
assumed tobemistaken.Therefore, theoptimistic assumption isretracted byreverting
theprevious sharedstatefortherelevantpartsofshared.
(rule3.22) rule:irrelevantFollowup
class:none
pre:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:1$/private/nim=Moves
2$/shared/lu/speaker ==usr
3notA/elem=icm:
4in($/shared/pm,PrevMove)
5PrevMove=ask(Q)or
(PrevMove=icm:und*int: DP*CandQ=und(DP*C))
6notMoves/elem=ask(Q0)and$domain ::depends(Q,Q0)
7notA/elem=answer(A)and$domain ::relevant(A,Q)
eff:(
/shared/qud:=$/private/tmp/qud
/shared/com:=$/private/tmp/com
(Sincethisruleiscalled\byname"fromtheupdatealgorithm, thereisnoneedforincluding
itinaruleclass.)Condition 3checksthatnoICMwasincluded inthelatestmove.
Condition 4and5triesto¯ndaquestion Qraisedbytheprevious move,possiblyan
understanding-question. NoteherethatwedonotcheckQUD;inIBiS2,questions remain
onQUDonlyforoneturnbutitmaybethecasethatwewantquestions toremainon
QUDoverseveralturns.Whatweareinterested hereisthusnotwhichquestions areon
QUDbutwhichquestions wereraisedbytheprevious utterance, andthisisthereason
forlookinginpmratherthanqud.Conditions 6and7checkthatnomoveperformed in
thelatestutterance isrelevanttoQ,neitherbyansweringitnorbyaskingaquestion on
whichQdepends.Theupdatesaresimilartothoseforintegration ofnegativeacceptance
feedback(Section 3.6.7).

142 CHAPTER 3.GROUNDING ISSUES
Asisthecaseforexplicitrejections, questions raisedby¯ndoutactionswillbeasked
again,butquestions raisedbyraiseactionswillnot.ICM-related questions (interrogativ e
understanding feedback)arenotrepeatedsincetheyarenotintheplanbutonlyonthe
agenda.
Adialogue involvingimplicituserrejection ofanissuewillbeshownlaterin(dialogue
3.12).
3.6.9Sequencing ICM:reraising issuesandloadingplans
Inthissection,wereviewsequencing-related ICMandshowhowthishasbeenimplemen ted
inIBiS2.
Webelieveitisgoodpracticetotrytokeeptheuserinformed aboutwhat'sgoingoninside
thesystem,atleasttoadegreethatfacilitates anaturaldialogue wheresystemutterances
\feelnatural". OnewayofdoingthisistoproduceICMphrasesindicating signi¯can t
updatestotheinformation statewhicharenotdirectlyrelatedtospeci¯cuserutterances.
UsingAllwood's(1995)terminology ,werefertotheseinstances ofICMas\sequencing
ICM".
ForIBiS2,wewillimplemen ttwotypesofsequencing ICM.First,whenloadingaplan
IBiS2willindicate this.Second, IBiS2willproduceICMtoindicate whenanissueis
beingreraised(incontrasttobeingraisedforthe¯rsttime).
Loadingplans
IBiS2willindicatewhenaplanisbeingloaded,thuspreparing theusertoanswerquestions.
Thisiscurrentlygenerated as\Let'ssee."
Therulefor¯ndinganappropriate plantodealwitharespond-action ontheagendais
similartothatinIBiS1.Thedi®erence isthattheIBiS2ruleproducesICMtoindicate
thatithasloadedaplan,formalized asicm:loadplan andgenerated e.g.as\Let'ssee".
Again,thechoiceofoutputformisprovisory.

3.6.FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 143
(rule3.23) rule:¯ndPlan
class:loadplan
pre:8
><
>:in($/private/agenda,respond(Q))
$domain ::plan(Q,Plan)
notin($/private/bel,P)and$domain ::resolves(P,Q)
eff:8
><
>:del(/private/agenda,respond(Q))
set(/private/plan,Plan)
push(/ private/agenda,icm:loadplan ))
ThisruleisidenticaltothatinIBiS1(Section 2.8.6),expectforthe¯nalupdatewhich
pushestheicm:loadplan moveontheagenda.
Reraising issues
SystemreraisingofissueassociatedwithplanIftheuserraisesaquestion Qand
thenraisesQ0beforeQhasbeenresolved,thesystemshouldreturntodealingwithQonce
Q0isresolved;thiswasdescribedinSection3.6.9.TherecoverPlanruleinIBiS2,shown
in(3.20),isalmostidenticaltotheoneinIBiS1,exceptthatICMisproducedtoindicate
thatanissue(q1)isbeingreraised. ThisICMisformalized asicm:reraise: qwhereqisthe
question beingreraised, andexpressed e.g.as\Returning totheissueofprice".
(rule3.24) rule:recoverPlan
class:loadplan
pre:8
>>>>>><
>>>>>>:in($/shared/qud,Q)
isempty($/private/agenda)
isempty($/private/plan)
$domain ::plan(Q,Plan)
notin($/private/bel,P)and$domain ::resolves(P,Q)
eff:8
><
>:set(/private/plan,Plan)
push(/ private/agenda,icm:reraise: Q)
push(/ private/agenda,icm:loadplan ))
IssuereraisingbyuserInthecasewheretheuserreraisesanopenissue,anicm:reraise: Q
moveisselectedbytheintegrateUsrAsk describedinSection3.6.6.
SystemreraisingofissuenotassociatedwithplanTheIBiS1reraiseIssue rule
describedinSection2.12.3reraisesanyquestions onQUDwhicharenotassociatedwith

144 CHAPTER 3.GROUNDING ISSUES
anyplan(i.e.whichhavebeenraisedpreviously bythesystem). Inthiscaseitisagain
helpfultoindicatethatthesystemisawarethattheissueisbeingreraised. However,since
theissuewillbereraised, thesequencing ICMdoesnotneedtoindicate whichquestion is
beingreraised.
(rule3.25) rule:reraiseIssue
class:selectaction
pre:(
fst($/shared/issues,Q)
not$domain ::plan(Q,P)
eff:(
push(/ private/agenda,icm:reraise )
push(/ private/agenda,raise(Q))
Theconditions ofthisrulechecksthatthereisaquestion Qonissuesforwhichthesystem
hasnoplan,i.e.onethatthesystemneedstoasktheuser.
The¯rstupdateaddsanicm:reraise (without anargumen t)tosignalthatitisreraising
aquestion; thisiscurrentlygenerated aspre¯xing \so"tothenextaskmove,whichis
anordinary raisingofthequestion (placedontheagendabythesecondupdateinthe
rule).Inamoresophisticated implemen tationonecouldconsider abbreviating theoriginal
raisingofthequestion tomakeanappropriate reraising, e.g.\So,fromwhatcity?"But
wedonothaveageneralmethodfordoingthatyet,eveninthesesimpledialogues. To
doitproperlywouldprobably requiremoredetailed syntacticandsemanticanalysis of
contributions thanwecurrentlyhaveinIBiS.
Dialogueexample: userandsystemreraising (dialogue 3.12)isanexample ofa
dialogue wheretheuserreraisesanissuewhichwaspreviously raisedbutnotresolved.
Alsosubsequen tlythesystemreraisesanissuewhichisrelevantforaddressing theissue
thattheuserreraised. Inordertoaddresstheissueofpricethesystemneedstoget
information fromtheuserconcerning whereshewishestotravelfrom.
(dialogue 3.12)
S>Welcome tothetravelagency!
U>priceinformation please
S>Okay.Letssee.Howdoyouwanttotravel?
U>aflight
S>Okay.Whatcitydoyouwanttogoto?
U>paris
S>Okay.Whatcitydoyouwanttogofrom?

3.7.FURTHER IMPLEMENT ATION ISSUES 145
U>right... actually, doineedavisa
useracceptsdeparturecityissue,thenraisesvisaissue
S>Okay.Letssee.Whatcountry areyoufrom?
U>um...letstalkaboutpriceagain
userimplicitly rejects(avoids) citizenship issue,reraisespriceissue
S>Okay.Returning totheissueofprice. Letssee.So,Whatcitydoyou
wanttogofrom?
systemindicatesreturning topriceissue,thenreraisesdeparturecityissue
U>london
S>Okay.Whatmonthdoyouwanttoleave?
U>april
S>Okay.Whatdaydoyouwanttoleave?
U>fifth
S>Okay.Whatclassdidyouhaveinmind?
U>cheap
S>Okay.Thepriceis123crowns. Returning totheissueofvisa.Let's
see.Whatcountry areyoufrom?
systemanswerspriceissue,therebyresolvingit,thenreraisesthevisaissue,indicatesplan
loading,andreraisescitizenship issue
The¯rstcaseofreraising here,whereitistheuserwhoreraisesthepriceissue,ishandled
bytheconditional updateoftheintegrateUsrAnsw er(Section 3.6.6)whichselectsan
icm:reraise: Qmovetosignalthatthesystemisawarethatissuewasalreadyopenbysaying
\Youreraised theissueofprice".Inthesameutterance, thesystemreraisestheissueof
wheretheuserwantstotravelfrom,requiresaselection ruleforthesystem.Whenreraising
anissue,IBiS2producesICMtoindicate awarenessthattheissuehasbeenraisedbefore.
ThisICMisformalized asicm:reraise andcanberealizede.g.bythediscourse particle
\So".Notethatthiswouldnothavehappenediftheuserhadnotaccepted thisquestion
(bysaying\right")whenitwas¯rstraised.Sincethesystemdoesnotregardthedeparture
cityquestion asdependentonthevisaissue,raisingthevisaissueinresponsetoasking
fordeparture citywouldhavebeenregarded asanimplicitrejection (Section 3.6.8).
Oncethepriceissuehasbeenresolved,thesystemreraisesthevisaissuewhichisstill
unresolved;thisisdonebytherecoverPlanruleasdescribedinSection3.6.9.
3.7Furtherimplemen tationissues
Inthissectionwedescribepartsoftheimplemen tationofIBiS2whichhavenotbeen
discussed earlierinthischapter,andwhicharenotdirectlyreusedfromIBiS1.

146 CHAPTER 3.GROUNDING ISSUES
3.7.1Updatemodule
TheIBiS2updatealgorithm isshownin(3.20).
(3.20)1ifnotlatestmoves==failed
2thenhgetLatestMo ve,
3 tryirrelevantFollowup,
4 repeatintegrate,
5 tryloadplan,
6 repeatmanageplan
7 trydowndatequdi
8elsetryunclearFollowup
Line1checksthattheinterpretation ofthelatestutterance wassuccessful (ofcourse,
inthecaseofsystemutterances thisisalwaystrue).Ifnot,theunclearFollowuprule
describedinSection3.6.8istried.Ifinterpretation wassuccessful, thelatestmovesare
incorporatedintheinformation stateproperbythegetLatestMo vesrule(seeSection
3.6.7).Beforeintegration starts,theirrelevantFollowupruledescribedinSection3.6.8
istriedtocatchcaseswhereasystemquestion hasbeenignoredbytheuser.Afterthis,
theintegration ruleclassisrepeatedlyapplieduntilthesystemhastriedtointegrateall
movesin/private/nim.Iftheuseraskedaquestion, theappropriate planwillbeloaded
byline5.Anyloadedplanisexecuted byapplying theexecplanruleclassuntilnomore
execution ispossibleatthecurrentstageofthedialogue.
3.7.2Selection module
AsinIBiS1,actionselection rulesaddactionstotheagenda. However,whileinIBiS1only
oneactionwasselected perturn,inIBiS2severalactionsmaybeselected perturn.For
example, theselectResp ondinIBiS2,shownin(rule3.26),doesnotrequiretheagenda
tobeempty,butonlythattherespondactionhasnotalreadybeenselected, andthusit
allowsseveralmovestobeselectedperturn.

3.7.FURTHER IMPLEMENT ATION ISSUES 147
(rule3.26) rule:selectResp ond
class:selectaction
pre:8
>>>>>>>><
>>>>>>>>:isempty($/private/plan)
fst($/shared/qud,A)
in($/private/bel,B)
notin($/shared/com,B)
$domain ::resolves(B,A)
notin($/private/agenda,respond(A))
eff:n
push(/ private/agenda,respond(A))
Similarly ,themoveselection rulesinIBiS2arerepeatedlyapplied,poppingactionso®the
agendaqueueandpushing thecorrespondingmovesonnextmoves.Asanexample,
theselectAnsw erruleisshownin(rule3.27).
(rule3.27) rule:selectAnsw er
class:selectmove
pre:8
>>><
>>>:fst($/private/agenda,respond(A))
in($/private/bel,B)
notin($/shared/com,B)
$domain ::resolves(B,A)
eff:(
push(nextmoves,answer(B))
pop(/private/agenda)
Theselection algorithm forIBiS2isshownin(3.21).
(3.21)hbackupShared ,
ifnotin($/private/agenda,A)andqraisingaction(A)
thentryselectaction,
repeat(selecticmorelseselectmove)i
Theselectactionruleclassselectsactionsandplacesthemontheagenda,whereas
theselectmoveandselecticmruleclassesselects agendaitemsandplacesthemon
nextmoves.Beforeselection, thebackupShared (Section 3.6.7)isappliedtocopy
relevantpartsoftheinformation stateto/private/nim.
Thebasicstrategy forselection inIBiSisthatonlyonequestion shouldberaisedbythe
systemineachutterance. TheIBiS2selection algorithm ¯rstchecksifsomequestion-
raisingactionisalreadyontheagenda; ifnot,ittriestoselectanewaction.Then,it
selectsmovesandICMrepeatedlyuntilnothingmorecanbeselected.

148 CHAPTER 3.GROUNDING ISSUES
The\qraisingaction(A)"condition usesamacrocondition (seeSectionA.4.2)whose
de¯nition isshownin(3.22).Whatthissaysis,basically,thatinterrogativ eICM,raise
and,¯ndoutactionsraisequestions.
(3.22)qraisingaction(Move)if
Move=icm:und*int: XorMove=raise(X)orMove=¯ndout( X)
3.8Discussion
3.8.1Somegrounding-related phenomena nothandled byIBiS2
Inthissectionwementionsomeareaswhichhavenotbeenaccountedforintheissue-based
approachpresentedhere.Wedonotbyanymeansclaimthatthislistiscomplete.
Perhapsthemostsigni¯can tomission inIBiS2isatreatmen tofsemanticambiguity,e.g.
ambiguous words.Apossibledirection ofresearchinthisareaistohandlesemantic
ambiguityonapragmatic level.Speci¯cally,therelevanceofanambiguousmoveinthe
currentdialogue contextmaybesu±cienttoresolvethesemanticambiguity,oratleast
reducethenumberofpossiblesemanticinterpretations. Inanycase,weseenoreason
thatmechanisms similartothosefordealingwithpragmatic ambiguitycouldbeusedfor
semanticambiguity.
Another areathatremainsunexplored fromthepointofviewofissue-based dialogue man-
agementissemanticvagueness. Forinstance, onemightwantasystemtounderstand
vagueanswers(e.g.\Iwanttogotosouthern France",\Iwanttotravelaroundthe10th
ofApril"), andperhapsalsotoasklessspeci¯cquestions whichleavemoreroomforthe
usertochoosehowtospecifye.g.parameters fordatabase search(e.g.\Where doyou
wanttotravel?"ratherthan\Whatcitydoyouwanttogoto?").
Onthepragmatic understanding level,wehaveconcentratedonellipsisresolution and
relevance,howeverwearestilllackingatreatmen tofreferentresolution. Onereasonfor
thisisofcoursethatIBiS2doesnotrepresentreferents.Thisisafairlywell-researc hed
area,andwehopetobeabletoincludesomeexistingaccountofreferentresolution when
thisbecomesnecessary .

3.8.DISCUSSION 149
Overlapping userfeedbackandandbarge-in
Mostdialogue systemsdonothandlefeedbackfromtheuserinanyform,andmost(ifnot
all)existing systems whichhandlebarge-in willstoptalkingiftheyperceiveanysound
fromthespeaker.Thismeansthatevenpositivefeedback(e.g.\uhuh")fromtheuser
willcausethesystemtostopspeaking.Thisproblem isaggravatedinnoisyenvironmen ts,
wherenoisesmaybemisinterpreted asspeechfromtheuserandcauseasystemtostop
speaking.Whatisneededisclearlythatthesystemmakesadistinction betweendi®erent
kindsoffeedbackfromtheuser;positivefeedbackshouldusuallynotcausethesystemto
stopspeaking.
Mechanisms forhandling overlapping userfeedbackhasbeenexplored withintheGoDiS
framework(Berman, 2001),butarenotincluded here.However,theinclusion ofpositive
userfeedbackinIBiSprovidesabasisforfurtherexplorations inthisarea.
3.8.2Towardsanissue-based accountofgrounding andaction
levels
Wehavehintedthatafull-coverageaccountofgrounding shouldincludegrounding onall
fouraction-lev els.Ginzburg's content-andacceptance-questions indicate howthiscould
beaccomplished inanissue-based theoryofdialogue. Foreachactionlevel,grounding
issuescanberaisedandaddressed; feedbackmovesonlevelLareregarded asaddressing
grounding issuesonlevelL.
Thiswouldallowgrounding tobehandled bythesamebasicupdatemechanisms asques-
tionsandanswers.Adistinction canbemadebetweenshort(elliptical, underspeci¯ed)
answers(feedbackutterances whoseactionlevelisnotexplicit) andfullanswers(feedback
utterances whoseactionlevelisclearfromtheformandcontentoftheutterance).
InIBiS,westriveforsimplicityatthecostofcompleteness; however,theaccountgiven
herecanbeseenasa¯rststeptowardsamorecomplete issue-based accountofgrounding
anactionlevelsindialogue. Asketchofamorecomplete accountcanbefoundinSection
6.5.1.
3.8.3Comparison toTraum'scomputational theoryofgrounding
Traum(1994)providesacomputational accountofgrounding basedonacombination of
¯niteautomata andcognitivemodelling.ThismodelbuildsonClarkandSchaefer(1989b)

150 CHAPTER 3.GROUNDING ISSUES
butattempts tosolvesomecomputational problems inherentinthataccount.
TraumarguesthatClark'saccountofthepresentationandacceptance phasesisproblem-
aticfromacomputational pointofview.Firstly,itmaybehardtotellifaspeechsignal
ispartofthepresentationoracceptance phase.Second,itishardtoknowwhenapresen-
tationoracceptance is¯nished; often,thisisonlypossibleinhindsight,whichmaycause
problems foradialogue systemengaged inreal-time spokendialogue. Third,itisunclear
whether grounding acts(inourterminology ,ICMdialogue moves)themselv esneedtobe
grounded.
Regarding thelastpoint,wefollowTrauminassuming thatICMmovesdonotneedto
begrounded. Infact,onourviewthisamountstoanoptimistic grounding strategy where
ICMmovesareconcerned.
Weagreethatingeneraltheproblem ofdeciding whenacontribution endsisonethat
shouldbehandled asapartofdialogue managemen t,andthatsomething likeTraum's
atomicgrounding actsareneededforthis.However,forthetimebeingwemakethesim-
plifyingassumption thatcontributions arealreadysegmentedbeforedialogue managemen t
starts;intheimplemen tation,werelyonthespeechrecognizer's built-inalgorithms for
deciding whenanutterance is¯nished.
Ouraccountdoesnotaddressthe¯rstpoint,i.e.theproblem ofjointlyproducedcontri-
butions, whereDPse.g.canrepaireachother'sutterances. Traumproposesarecursive
transition network(RTN)modelofthegrounding processwhichincludes repairs,requests
forrepairs,acknowledgemen tsandrequests foracknowledgemen ts(asimpler¯nitestate
modelisalsoprovided).Ouraccountdoesnotincluderepairsorrequests foracknowledge-
ments;however,Traum'sacknowledgemen tscorrespondroughlytopositivefeedbackand
requests forrepairscorrespond(very)roughlytonegativefeedback.
ItisimportanttonoteherethatTraum(1994)usestheterm\grounding" toreferexclu-
sivelytowhatwecall\understanding-lev elgrounding". ItisnotablethatTramfocuses
almostexclusivelyonpositivefeedback,whereas negativefeedbackisgivenalessdetailed
treatmen t.Thegrounding actmostcloselycorrespondingtonegativefeedbackisrequest
forrepair;however,itisdoubtful whether allnegativefeedbackcanberegarded asrequests
(e.g.\Idon'tunderstand"). TouseAllwood'sterminology ,feedbackhasbothanexpres-
sivedimension (expressing lackofperception, understanding, acceptance) andanevocative
dimension (requesting a\repair" orrepetition/reform ulation). ItappearsthatTraumhas
focusedmoreontheevocativedimension whereas wehavebeenmoreconcerned withthe
expressiv edimension. (Wedofeelthattheevocativeaspectoffeedbackissomething that
perhapsdeservesmoreattentionthanwehavegivenitsofar;thisisyetanotherareafor
futureresearch.)
Thedialogue acts\accept" and\reject"areregarded byTraumas\CoreSpeechActs"on

3.9.SUMMAR Y 151
thesamelevelasassertions, askingquestions, givinginstructions etc.Theacceptactis
de¯nedas\agreeing toaproposal"(p.58),whichgivestheimpression thatanacceptance
actisanaturalfollowuptosomeproposalact.
However,Traum'sacceptance actalsohassimilarities towhatwerefertoaspositive
reaction-lev elfeedback.Forexample, anacceptance movemayfollowanassertion oran
instruction, andthee®ectsoftheacceptactistochangethestatusofthecontentofthe
assertion orinstruction frombeingmerelyproposedtoactually beingshared.Regarding
questions, itisunclearwhether theyneedtobeaccepted beforebeingshared.According to
Traum,askingaquestion imposesanobligation ontheaddressee toaddressthequestion,
i.e.toeitheransweritortorejectit.Thisseems(although itisfarfromclear)toindicate
thatquestions onTraum'saccountareoptimistically assumed tobegrounded whereas
assertions andinstructions arenot.
InChapter 5,weextendtheissue-based accountofdialogue tonegotiativ edialogue, andar-
guethattwokindsofacceptances needtobedistinguished: acceptance aspositivefeedback
onthereaction level,andacceptance ofaproposedalternativ esolution tosomeproblem
(e.g.acertaindomainplanasoneamongseveralwaystoreachsomegoal).
3.9Summary
Afterprovidingsomedialogue examples wherevariouskindsoffeedbackareused,we
reviewedsomerelevantbackground, anddiscussed generaltypesandfeatures offeedback
asitappearsinhuman-humandialogue. Next,wediscussed theconcept ofgrounding
fromaninformation updatepointofview,andintroducedtheconcepts ofoptimistic,
cautious andpessimistic grounding strategies. Wethenrelatedgrounding andfeedbackto
dialogue systems, anddiscussed theimplemen tationofapartial-co veragemodeloffeedback
relatedtogrounding inIBiS2.Thisallowsthesystemtoproduceandrespondtofeedback
concerning issuesdealingwiththegrounding ofutterances.

152 CHAPTER 3.GROUNDING ISSUES

Chapter 4
Addressing unraised issues
4.1Introduction
Intheprevious chapter,wediscussed variousmechanisms forhandling grounding. Oneof
theactionlevelstowhichgrounding appliesisthatofpragmatic understanding, i.e.making
senseofthemeaning ofanutterance inthecurrentdialogue context.Somebasicmecha-
nismsforgrounding ontheunderstanding levelwereimplemen tedinIBiS2.However,the
kindsofdialogues handled bythissystemarestillratherrigidandsystem-con trolled.
Theaimofthecurrentchapteristoenablemore°exibledialogue. Afterreviewing some
shortcomings ofIBiS2,wetakeacloserlookatthenotionsunderlying theQUDdata
structure, whichresultsindividing QUDintotwosubstructures, oneglobalandonelocal.
Next,thenotionofquestion accommo dationisintroducedtoallowthesystemtobemore
°exibleinthewayutterances areinterpreted relativetothedialogue context.Amongother
things,question accommo dationallowsthesystemtounderstand answerstoquestions
whichhavenotyetbeenasked,andtounderstand suchanswersevenbeforeanyissue
hasbeenexplicitly raised.Incasesofambiguity,clari¯cation dialogues maybeneeded.
Question accommo dationcombinedwith(verybasic)beliefrevision abilities alsoallows
IBiStoreaccommo datequestions whichhavepreviously beenresolved.Finally,aversion
ofreaccommo dation,wherereaccommo dationofoneissuerequires reaccommo dationofa
dependentissueaswell,allowsforsuccessiv emodi¯cations ofdatabase queries.
ThedivisionofQUDintoaglobalandalocalstructure alsoenablesasimpleaccommo-
dationmechanismallowingtheusertocorrectthesystemincaseswhereexplicitpositive
feedbackshowsthatthesystemhasmisundersto odauserutterance.
153

154 CHAPTER 4.ADDRESSING UNRAISED ISSUES
Apartfromtheinitialand¯nalsections, thischapterisstructured aroundthevariousques-
tionaccommo dationmechanisms. Foreachtypeofaccommo dation,thereisaninformal
description, aformalization consisting ofoneormoreupdaterules,anddialogue examples.
4.2Somelimitations ofIBiS2
Handling answerstounaskedquestions
Thedialogue structure allowedbytheIBiS2systemisratherrigidandsystem-con trolled.
Themainpartofthedialogue consistsofthesystemaskingquestions whichtheuserhas
toanswer.Theuserisnotallowedtogivemoreinformation, ordi®erentinformation, than
whatthesystemhasjustaskedfor.
Ingeneral, werequirethatthecontentofeachanswer-movemustmatchaquestion on
QUD.InIBiS2,theonlywayquestions canenduponQUDisbybeingexplicitly asked.
Thisforcesasimpletreestructure ondialogue. Inrealdialogue, however,peopleoften
performutterances whichcanbeseenasanswerstoquestions, oraddressing issues,which
havenotyetbeenraised.
Revisinginformation
Oncetheuserhassupplied someinformation toIBiS2,thisinformation cannotbechanged.
Thisisclearlyundesirable, andsolvingthisproblem wouldprovideseveraladvantages:
²Theusermaychangehismindduringthespeci¯cation ofthedatabase query
²Aftertheuserhasbeengivene.g.priceinformation foraspeci¯edtrip,hecan
modifysomeoftheinformation toproduceanewquery,withouthavingtoenterall
information again
Correcting explicitpositivefeedback
Animportantfactorin°uencing thechoiceoffeedbackandgrounding strategies inadia-
loguesystemisusability(including e±ciency ofdialogue interaction). Adisadvantageof
thecon¯rmation-question approachisthatthedialogue becomesslowandtiringforthe
user,whichdecreases thee±ciency andusabilityofthesystem.

4.3.THENATURE(S) OFQUD 155
Forthisreason,intheprevious chapterweaddedthecapabilityofproducingfeedbackon
theunderstanding levelinnon-eliciting form,i.e.asadeclarativ eorelliptical sentence
(without question intonation). However,thissolution isunsatisfactory sincethesystem
maybemistakenandthereisnowaytocorrectit.Averynaturalresponsetopositive
explicitfeedbackwhichindicates amisunderstanding istoprotest,e.g.bysaying\no!",
possiblyfollowedbyacorrection.
Inthischapter,weuseaspecialcaseofquestion accommo dationtoallowthis,thusex-
tendingtheissue-based accountofgrounding. Iftheuserissatis¯ed withthesystem's
interpretation, shedoesnothavetodoanything;thesystemwilleventuallycontinue(pos-
siblyafterashortpause)withthenextstepinthedialogue plan.Theuser'ssilenceis
regarded asanimplicitcompliance withthesystem's feedback.Thereisalsotheoptionof
givinganexplicitpositiveresponsetothefeedback(e.g.\yes"or\right").Finally,ifthe
userrespondsnegativelytothesystem's feedback(e.g.bysaying\no"),thesystemwill
understand thatitmisundersto odtheuserandactaccordingly .
4.3Thenature(s) ofQUD
Beforeextending thecapabilities ofIBiS,wewillinvestigatethenatureofQUDandmake
somedistinctions betweenthedi®erenttasksthatQUDcanbeusedfor.Wewilldrawthe
conclusion thatQUDneedstobedividedintotwosubstructures, oneglobalandonelocal.
Inthissection,wepresentandcompare somealternativ enotionsofQUD.
4.3.1Ginzburg's de¯nition ofQUD
InGinzburg (1997),Ginzburg providesthefollowingde¯nition ofQUD:
QUD('questions underdiscussion'): asetthatspeci¯esthecurrentlydiscuss-
ablequestions, partially orderedbyÁ('takesconversational precedence'). Ifq
ismaximal inQUD,itispermissible toprovideanyinformation speci¯ctoq
using(optionally) ashort-answ er.(Ginzburg, 1997,p.63)
Whilethede¯nition abovemerelystatesthatQUDisapartially orderedset,theoperations
performed onQUDinGinzburg's protocolssuggestthatinfactitismorelikeapartially

156 CHAPTER 4.ADDRESSING UNRAISED ISSUES
orderedstack1.InIBiS1andIBiS2wemadethesimpli¯cation thatQUDissimplya
stack.
Ginzburg thususesasinglestructure todotwojobs:(1)specifyingthequestions thatare
currentlyavailablefordiscussion (\open"questions), and(2)specifyingthequestions that
canbeaddressed byashortanswer(namely,thosethatareQUD-maximal).
BasedonGinzburg's QUDquerying protocol(Section 2.8.2),Ginzburg's QUDcanalsobe
saidto(3)representquestions whichhavebeenexplicitly raisedinthedialogue. Whilethis
isnotexplicitly stated,itappearsthattheonlywayatask-levelquestion canenterQUD
onGinzburg's accountisbybeingexplicitly asked.(However,grounding-related questions
mayenterQUDwithoutbeingraisedaspartoftheinternalreasoning ofaDP;seeSection
3.2.2).
Similarly ,theQUDdowndateprotocol(Section 2.8.4)suggests thatQUDalsoful¯llsafur-
therproperty(4)ofcontainingas-yetunresolvedquestions. Opennessandunresolvedness
maynotbeidenticalproperties;arguably,resolvedquestions maystilltosomeextentbe
openfordiscussion, andaquestion couldbediscarded fromtheopenissueswithoutbeing
resolved,e.g.ifitbecomesirrelevant(Larsson, 1998).
Tosummarize, giventhisbasiccharacterization ofQUD,wecansaythatquestions on
QUDare
1.openfordiscussion,
2.availableforellipsisresolution,
3.explicitly raised,and
4.notyetresolved.
InIBiS2,theimplemen tedQUDessentially¯tswithGinzburg's de¯nition, exceptforthe
simpli¯cation thatitisaplainstackratherthananopen,partially orderedstack.Thisis
su±cientfortherelativelysystem-con trolled,rigiddialogue handled byIBiS2.Whenthe
dialogue structure becomesmore°exible, however,thesevariouspropertiesoftheQUD
listedabovenolongerappeartoco-occurinallsituations.
1Apartially orderedstackwouldbeastructure whereelementscanbepushedandpopped,butwhich
onlyhasapartialordering. Forexample, morethanoneelementcanbetopmost onthestack.

4.3.THENATURE(S) OFQUD 157
4.3.2Openquestions notavailableforellipsisresolution
Regarding QUDasastack(orstack-like)structure suggests thatwhenthetopmost element
(orsetofelements)ispoppedo®thestack,theelement(orsetofelements)thatwas
previously next-to-maximal becomesmaximal. Thisimpliesthatquestions canbeanswered
elliptically atanarbitrary distance fromwhentheywereraised.However,itcanbeargued
thatinmanycasesaquestion whichhasbeenraisedafewturnsbackisnolongeravailable
forellipsisresolution (oratleastsigni¯can tlylessavailablethanitwasrightafterthe
question wasraised).Forexample, B's¯nalutterance inthemade-up dialogue in(4.1)is
unlikelytooccuranditwouldberatherconfusing ifitdid,simplybecauseitisnotclear
whichquestion Bisanswering.
(4.1)A:Who'scomingtotheparty?
B:Thatdepends,isJillcoming
A:JillJennings?
B:Yes
A:Bytheway,didyouhearaboutherbrother? What'shis
nameanyway?
B:Umm..I'mnotsure.Anyway,I'drathernottalkaboutit.
A:OK.So,No
B:So,Jim
Ifthisargumen tisaccepted, weseethataquestion maysatisfyrequiremen ts(1)and(3)
above,tobeacurrentlyopenfordiscussion, explicitly raisedquestion, whilenotsatisfying
property(2)ofbeingavailableforellipsisresolution.
4.3.3Openbutnotexplicitly raisedquestions
Studying recorded travelagencydialogues inlightoftheQUDapproachindicates thatit
maybethecasethataquestion whichhasnotbeen(explicitly) raisedisinfactdiscussable,
andevenavailableforellipsisresolution, asthedialogue in(4.2)shows2.
(4.2)A:Whendoyouwanttotravel?
B:April,ascheapaspossible
Thus,wecanobservethataquestion maysatisfyrequiremen ts(1)ofbeingopenfor
discussion and(2)ofbeingavailableforellipsisresolution, withoutsatisfying property(3)
ofhavingbeenexplicitly raised.
2Thisisasimpli¯ed versionofthedialogue inexample 4.6.

158 CHAPTER 4.ADDRESSING UNRAISED ISSUES
4.3.4GlobalandlocalQUD
TheobservationsabovesuggestthatitisnotidealtomodelQUDusingasinglestructure
satisfying properties(1)to(4).Thesolution weproposeistodivideQUDintoaglobal
andalocalstructure; theformersatisfying property(1)ofbeingopenfordiscussion and
(4)ofbeingunresolved,andthelattersatisfying property(2)ofbeingavailableforellipsis
resolution. Property(3)ofbeingexplicitly raisedisnotsatis¯ed byeitherstructure. This
enablesmore°exiblewaysofintroducingquestions intoadialogue. Thisdivisionoflabour
alsoappearstoallowtheuseofsimplerdatastructures thanpartially orderedsets.
De¯nition oflocalQUD
ForthelocalQUD,asetseemsappropriate formodellingthequestions currentlyavailable
forellipsisresolution. Astack-likestructure wouldsuggeste.g.the(made-up) dialogues
(4.3)shouldbeeasilyprocessedbyDPs,butinfactitisveryunclearwhatBmeans.
(4.3)A:Whereareyougoing?Whereisyourwifegoing?
B:Paris.London.
Also,consider example (4.4):
(4.4)A:Whenareyouleaving?Whenareyoucomingback?
B:tenthirtyandeleventhirty
Asimplestackstructure alsosuggests averyunintuitiveinterpretation ofB'sanswer,
where10:30isthetimewhenBiscomingbackand11:30isthetimewhenBisleaving.
Itappearsthatamongtheconstrain tsguidingellipsisresolution incaseswheremultiple
questions areavailable,theorderinwhichthequestions wereaskedisnotverysigni¯can t.
Ofcourse,Ginzburg realizesthisandthisappearstobethemainreasonforlettingQUD
beapartially orderedsetwhereseveralinternallyunordered elementsmaybetopmost on
QUD,andthusavailableforellipsisresolution.
InIBiS3wede¯neQUDtobeanopenstackofquestions thatcanbeaddressed using
shortanswers.Thereasonforusinganopenstackisthatithastheset-likepropertieswe
want,butalsoretainsastackstructure incaseitshouldbeusefulforellipsisresolution.

4.3.THENATURE(S) OFQUD 159
De¯nition ofglobalQUD,or\LiveIssues"
TheglobalQUDcontainsallquestions whichhavebeenraisedinadialogue (explicitly or
implicitly) butnotyetresolved.Itthuscontainsacollection ofcurrent,or\live"issues.
Asuitable datastructure appearstobeanopenstack,i.e.astackwherenon-topmost
elementscanbeaccessed. Thisallowsanon-rigid modellingofcurrentissuesandtask-
relateddialogue structure.
4.3.5SomeothernotionsofwhataQUDmightbe
Infact,therearesomeadditional notionsofwhatQUDmightbe,allofwhichinsome
sensecontainquestions thatareunderdiscussion, andallofwhichhavepotentialusesin
atheoryofdialogue managemen tandinadialogue system.
²closedissues:questions thathavebeenraisedandresolved(seeSection3.6.9)
²raisabledomainissues:allissuespotentiallyrelevantinregardtothedomain
²potentialgrounding issues:allissuespertaining togrounding of(a)recentutter-
ance(s)
²resolvableissues(foraDP):allissuesthataDPknowssomewayofdealingwith,
eitherbyansweringdirectlyorbyenteringasubdialogue
However,whileallthesemaybeuseful,itmaynotbenecessary tomodelthemexplicitly
asseparate structures inadialogue system. Forexample, \raisable domainissues"and
\resolvableissues"maybederivedfromthe(static)domainknowledge.
Regarding \closedissues",wecantosomeextentderivethemfromthesharedcommitmen ts
bycheckingwhichissuesareresolvedbypropositional information, asin(4.5).
(4.5)Qisaclosedissuei®thereissomeP2/shared/com such
thatPresolves QandPdoesnotresolveanyotherquestion (in
thedomain)
However,thisonlyworksaslongaseachpropositionresolvesauniqueissue.Ifthisisnot
true,aseparate storeofclosedissuesisneedede.g.fordetecting reraisings ofpreviously
discussed issues.

160 CHAPTER 4.ADDRESSING UNRAISED ISSUES
4.4Question Accommo dation
Inthissection,weintroducetheconceptofaccommo dationandshowhowitcanbeex-
tendedtohandleaccommo dationofquestions invariousways.Wealsoshowhowquestion
accommo dationcanbeimplemen tedinIBiS.
4.4.1Background: Accommo dation
Lewis'notionofaccommodation
DavidLewis,inLewis(1979),indiscussing theconcept ofaconversational scoreboard,
compares conversation toabaseball game:
...conversational scoredoestendtoevolveinsuchawayasisrequired inorder
tomakewhateveroccurscountascorrectplay(Lewis,1979,p.347)
Healsoprovidesageneralschemeforrulesofaccommodationforconversational score:
Ifattimetsomething issaidthatrequires componentsnofconversational
scoretohaveavalueintherangerifwhatissaidistobetrue,orotherwise
acceptable; andifsndoesnothaveavalueintherangerjustbeforet;andif
such-and-suc hfurtherconditions hold;thenattthescore-comp onentsntakes
somevalueintheranger.(Lewis,1979,p.347)
Thisverygeneralschemacanbeusedfordealingwithde¯nitedescriptions, presupposition
projection(seee.g.vanderSandt,1992),anaphora resolution, andmanyotherpragmatic
andsemanticproblems.
Onemotivationforthinking intermsofaccommo dationhastodowithgenerality.We
couldassociateexpressions whichintroduceapresuppositionasbeingambiguousbetween
apresuppositional readingandasimilarreadingwherewhatisthepresuppositionispart
ofwhatisasserted. Forexample, anutterance of\ThekingofFranceisbald"canbe
understo odeitherasanassertion ofthepropositionthatthereisakingofFranceandhe
isbald,orasanassertion ofthepropositionthatheisbaldwiththepresuppositionthat
thereisakingofFranceandthat\he"referstothatindividual. However,ifweassume
thataccommo dationtakesplacebeforetheintegration oftheinformation expressed bythe
utterance thenwecansaythattheutterance alwayshasthesameinterpretation.

4.4.QUESTION ACCOMMOD ATION 161
4.4.2Accommo dation,interpretation, andtacitmoves
Inaninformation updateframework,accommo dationisnaturally implemen tedasanup-
daterulewhichmodi¯estheinformation statetoincludetheinformation presupposedby
anutterance, insuchawayastomaketheutterance felicitous, i.e.tomakeitpossibleto
understand therelevanceofandpossiblyintegratethemove(s)associatedwiththeutter-
ance.Theaccommo dationupdateactsasareplacemen tforadialogue move,whichwould
haveprepared the(common) groundfortheutterance actually performed. Forthisreason,
accommo dationupdatesmaybereferredtoasakindoftacitmove.Forexample, thesilent
accommo dationmovewhichadds\thereisakingofFrance"toallowtheintegration of
\ThekingofFranceisbald"correspondstoadialogue moveasserting thisproposition.
Thus,wecansimplify ourdialogue moveanalysis sothattheupdatestotheinformation
statenormally associatedwithadialogue moveareactually carriedoutbytacitaccommo-
dationmoves.
This¯tswellwiththefactthatveryfew(ifany)e®ectsofadialogue moveareguaranteed
asaconsequence ofperforming themove;rather,theactualresulting updatesdependon
reasoning bytheaddressed participan t.Accommo dationisonetypeofreasoning involved
inunderstanding andintegrating thee®ectsofdialogue moves.
4.4.3Extending thenotionofaccommo dation
Inthissection, weextendthenotionofaccommo dationintroducedbyLewistocover
accommo dationofQuestions UnderDiscussion.
Asde¯nedbyLewis,accommo dationisnotlimitedtoonlypropositions3.Itstatesthat
anycomponentofthescoreboardcanbemodi¯edbyaccommo dation. Ifwecarrythis
overtotheissue-based approachtodialogue managemen t,itfollowsthatinaddition to
theaccommo dationofpropositionstothesetofjointlycommitted propositions, questions
canbeaccommo datedtoQUD.
Thus,question accommo dationcanbeexploited toprovideanexplanation ofthefactthat
questions canbeaddressed (evenelliptically) withouthavingbeenexplicitly raised.This
isveryrelevantforadialogue system,sinceitallowstheusermorefreedom regarding
whenandhowtoprovideinformation tothesystem. Inaddition, therelatedconceptof
3Ofcourse,allinformation ontheDGBis,intheend,propositional innature;aDGBcontaininga
question QatthetopofQUDcouldinprinciple bedescribedbyasetofpropositionsincluding \Qis
topmost onQUD".This,however,wouldbeimpractical andine±cien tcompared tomaintainingaproper
stack-likestructure.

162 CHAPTER 4.ADDRESSING UNRAISED ISSUES
question reaccommodationcanbeusedtoenableaddressing resolvedissues,whichamong
otherthingsprovidesawayofhandling revision ofjointlycommitted propositionsina
principled manner.
Beforeproceedingtoexploretheexactformulationandformalization ofquestion accom-
modation,weprovidearoughcharacterization ofthenotionsused:
²question/issue accommo dation:adjustmen tsofcommon groundrequired tounder-
standanutterance addressing anissuewhichhasnotbeenraised,butwhichis
{relevanttothecurrentdialogue plan
{relevanttosomeissueinthedomain
²question/issue reaccommo dation:adjustmen tsofcommon groundrequired tounder-
standanutterance addressing anissuewhichhasbeenresolvedand
{doesnotin°uence anyotherresolvedissue
{in°uences anotherresolvedissue
{concerns grounding ofaprevious utterance
Utterances whicharerelevanttothecurrentdialogue plancanalsoberegarded asbeing
indirectlyrelevanttothegoalofthatplan.Ininquiry-orien teddialogue wemodelgoals
asissueswhichallowsanalternativ eformulationofaccommo dationas\adjustmen tsof
common groundrequired forunderstanding anutterance addressing anissuewhichhas
notbeenraised,butwhichis(directly orindirectly) relevanttosomeissueinthedomain."
Inaction-orien teddialogue (Chapter 5),utterances mayalsobeindirectly relevanttosome
goalaction.
4.5Formalizing questionaccommodation
Inthissectionwediscussthevarioustypesofquestion accommo dationandshowhowthey
areformalized inIBiS3.Westartbyexplaining andmotivatingsomemodi¯cations ofthe
information statetyperequired tohandledialogues involvingquestion accommo dation.
4.5.1Information stateinIBiS3
Theinformation stateusedinIBiS3isshowninFigure4.1.

4.5.FORMALIZING QUESTION ACCOMMOD ATION 163
2
666666666666666666666664private:2
666666664agenda:OpenQueue(Action)
plan :OpenStack(PlanConstruct)
bel :Set(Prop)
tmp :"
usr:Tmp
sys:Tmp#
nim :OpenQueue(P air(DP,Move))3
777777775
shared :2
666666664com :Set(Prop)
issues :OpenStack(Question)
qud :OpenStack(Question)
pm :OpenQueue(Mo ve)
lu :"
speaker :Participan t
moves:Set(Move)#3
7777777753
777777777777777777777775
Tmp=2
6666664com :Set(Prop)
issues :OpenStack(Question)
qud :OpenStack(Question)
agenda:OpenQueue(Action)
plan :OpenStack(PlanConstruct)3
7777775
Figure4.1:IBiS3Information Statetype
The¯rstchangecompared totheIBiS2information stateistheaddition oftheopenstack
/shared/issues ,whichcontainstheopenissues.The/shared/qud ¯eldhasnotbeen
modi¯edintermsofdatatype,butisnowusedformodellingthelocalQUD.
Thesecondchangeisthedivisionof/shared/tmp intotwosub¯elds. Thesyssub¯eld
correspondstothetmp¯eldinIBiS2,andcontainspartsoftheinformation statecopied
rightbeforeintegrating thelatestsystemutterance. AsinIBiS2,systemutterances are
optimistically assumed tobegrounded, andiftheusergivesnegativefeedbackthetmp/sys
¯eldisusedtoretracttheoptimistic assumption. Inaddition, thesystemsometimes
makesanoptimistic assumption regarding thegrounding andunderstanding ofauser
utterance, andproducespositivefeedback(e.g.\OK.ToParis."). InIBiS3,wewill
useatypeofquestion accommo dationtoenableretraction oftheoptimistic grounding
assumption regarding userutterances, incaseswheretheuserrejectsthesystem's reported
interpretation. Forthis,wealsoneedtokeepacopyofrelevantpartsoftheinformation
stateastheywererightbeforetheuser'sutterance wasinterpreted andintegrated; thisis
whatthetmp/usr ¯eldcontains.
Finally,theitemson/private/nim arenowpairs,wherethe¯rstelementistheDP
whomadethemove,andthesecondisthemoveitself.InIBiS2,itcanbeassumed
thatallnon-integrated moveswereperformed inthelatestutterance. InIBiS3,question
accommo dationmechanisms allowlessrestricted dialogues, andthereisnolongerany
guaranteethatallnon-integrated movesweremadeinthelatestutterance. Movesmaybe

164 CHAPTER 4.ADDRESSING UNRAISED ISSUES
storedinnimforseveralturnsbeforebeingintegrated.
4.6Varietiesofquestion accommodationandreac-
commodation
Asshownbythedialogue in(4.6)4,questions canbeanswered(evenelliptically) without
previously havingbeenraised.
(4.6)J:vickenmºanadskaduºaka
whatmonthdoyouwanttogo
B:ja:typden:Äa:tredjefjÄardeapril/nºangºangdÄar
wellaround3rd4thapril/sometimethere
P:sºabillitsommÄojlit
ascheapaspossible
Butwheredoestheaccommo datedquestion comefrom?Inprinciple, wecouldimaginea
hugenumberofpossiblequestions associatedwithanyanswer,especiallyifitiselliptical or
semanticallyunderspeci¯ed.Howisthissearchspaceconstrained? Theanswerliesinthe
activitywhichisbeingperformed; thequestion mustbeavailableaspartoftheknowledge
associatedwiththeactivity-eitherstaticknowledgedescribing howtheactivityistypically
performed, ordynamic knowledgeofthecurrentstateoftheactivity.
Inthissectionwe¯rstdescribethethreebasicquestion accommo dationmechanisms: global
question accommo dation(issueaccommo dation),localquestion accommo dation(QUDac-
commodation)anddependentissueaccommo dation.Wethendiscusstheneedforclari-
¯cationquestions incaseswhereitisnotclearwhichquestion isbeingaddressed, before
movingontodescribing reaccommo dationanddependentreaccommo dation.Foreachtype
ofaccommo dationwealsodescribetheimplemen tationandprovidedialogue examples from
theimplemen tedsystem.
Ingeneral, accommo dationistriedonlyafter\normal" integration hasfailed.Thecoor-
dination oftheaccommo dationrulesinrelationtogrounding (including integration) rules
ishandled bytheupdatealgorithm describedinSection4.7.2.
4Thisdialogue hasbeencollected bytheUniversityofLundaspartoftheSDSproject.Wequotethe
transcription doneinGÄoteborgaspartofthesameproject.

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION165
4.6.1Issueaccommo dation:fromdialogue plantoISSUES
Thistypeofaccommo dationoccurswhenaDPaddresses anissuewhichisnotyetopen
butwhichispartofthecurrentplan5.Inthedialogue inexample 6,P'ssecondutterance
(\ascheapaspossible") addresses theissueofwhichpriceclassPisinterested in.Atthis
stageofthedialogue, thisissuehasnotbeenraised,butpresumably Jwasplanning to
raiseiteventually.
Before IBiScanintegrateananswer,itneedsto¯ndanopenissuetowhichtheanswer
isrelevant(seethede¯nition oftheintegrateUsrAnsw erruleinSection3.6.6).Thus,
tohandleadialogue likethatinexample 6somemechanismisneededfor¯ndingan
appropriate issueinthecurrentdialogue planandmovingittotheissuesstack.A
schematic representationofissueaccommo dationisshowninFigure4.2. 
	


 
 



 



 "!$#%'&)(+*", -"
 
./&102%13!$46570289*2 :;&=<)
 %>&1,?
- @.A>&B!$4C<=*",
DE  FHGJI
 LKEMONI'PQI
LKEMONSRTD 



 "!$UV*XW2Y,
Z\[[[[[[]I>^


 
 
_a`D b.A&Y!$4C<=*",IYIG

I
@./&102%13!c

Y:d&)(	*2,eG
 @./&102%13!c

Y:d&)(	*2,D @



"!fUg*XW2B,-G
F
I
 

hQ
 b4i02<;&)(	%(	 0j/&D
`J
 @.A&Y!fUg*XW2B,R
Z\[[[[[[]
Z\[[[[[[[[[[[[[[[[[[]
Figure4.2:Issueaccommo dation
Theissueaccommo dationupdaterulein(rule4.1)¯rstcheckswhether aquestion which
matchestheansweroccursinthecurrentdialogue plan(providedthereisone).Aquestion
matchesanansweriftheanswerisrelevantto,or(inGinzburg's terminology) aboutthe
question. Ifsuchaquestion canbefound,itcanbeassumed thatthisisnowanopen
issue.Accommo datingthisamountstopushingthequestion ontheISSUES stack.
5Sincethecurrentplanispresumably beingcarriedoutinordertodealwithsomeopenissue,wemay
regardtheutterance asindirectly relevanttosomeopenissue(viatheplan).

166 CHAPTER 4.ADDRESSING UNRAISED ISSUES
(rule4.1)rule:accommodatePlan2Issues
class:accommodate
pre:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:$/private/nim/elem/snd=answer(A)
not$lexicon ::ynanswer(A)
in($/private/plan,¯ndout( Q))
$domain ::relevant(A,Q)
$domain ::defaultquestion( Q)or
not(in($/private/plan,¯ndout( Q0))
andQ6=C
and$domain ::relevant(A,Q0))
eff:n
push(/ shared/issues,B)
The¯rstcondition picksoutanon-integratedanswermovewithcontentA.Thesecond
condition checksthatAisnotay/nanswer(e.g.yes,no,maybeetc.),andthusim-
plementsanassumption thatsuchanswerscannottriggerquestion accommo dation,since
theyaretooambiguous6.Thethirdandfourthconditions checkifthereisa¯ndoutaction
withcontentQinthecurrentlyloadedplan,suchthatAisrelevanttoQ.The¯nalcon-
ditionchecksthatthereisnootherquestion intheplanthattheanswerisrelevantto,or
alternativ elythatQhasthestatusofadefaultquestion. Ifthiscondition doesnothold,a
clari¯cation question shouldberaisedbythesystem;thisisdescribedinSection4.6.3.The
\default question" optionallowsencodingofthefactthatoneissuemaybesigni¯can tly
moresalientinacertaindomain. Forexample, inatravelagencysettingthedestination
citymayberegarded asmoresalientthanthedeparture cityquestion. Ifthisisencoded
asadefaultquestion, theniftheusersayssimply\Paris"itisinterpreted asanswering
thedestination cityquestion; noclari¯cation istriggered7
Example dialogue: issueaccommodation Thedialogue in(dialogue 4.1)illus-
tratesaccommo dationofthequestion?C.class(C)fromtheplantothestackofopen
issues.
(dialogue 4.1)
6However,ingeneralonecannotruleoutthepossibilitythaty/nanswerscantriggeraccommo dationin
severelyrestricted domains. Theassumption thatthiscannothappencanberegarded asaverysimpli¯ed
versionofaconstrain tonthenumberofquestions whichananswermayberelevantwithout making
question accommo dationinfeasible.
7Thenormalgrounding mechanisms shouldofcourseenablecorrection ofthisassumption. InIBiS3
thechoiceofgrounding strategy dependssolelyontherecognition scorewhichmeansthatahigh-scoring
answermaybeinterpreted asananswertoadefaultquestion andnotreceiveanyexplicitfeedback.Thisis
onecasewhichindicates aneedfortakingmorefactorsintoaccountwhenchoosingfeedbackandgrounding
strategy.

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION167
S>Whatmonthdoyouwanttoleave?
2
66666666666666666666666666664private=2
666666664agenda=hhii
plan =*¯ndout(?A.month(A))
¯ndout(?B.deptday(B))
¯ndout(?C.class(C))
consultDB(? D.price(D))+
bel =fg
nim =hhii3
777777775
shared =2
666666666666664com =8
<
:destcity(paris)
deptcity(london)
how(plane)9
=
;
issues =¿?F.month(F)
?E.price(E)À
qud =­
?F.month(F)®
pm =:::
lu =2
4speaker =sys
moves =ask(?F.month(F))
score =13
53
7777777777777753
77777777777777777777777777775
U>aprilascheapaspossible
getLatestMo ves
backupSharedUsr
integrateUsrShortAnsw er
downdateISSUES
removeFindout
accommo datePlan2Issues©
push(/ shared/issues,?A.class(A))
integrateUsrF ullAnswer
downdateISSUES
removeFindout
downdateQUD

168 CHAPTER 4.ADDRESSING UNRAISED ISSUES
2
666666666666666666666666664private=2
66664agenda=­­icm:acc*p os®®
plan =¿
¯ndout(?A.deptday(A))
consultDB(? B.price(B))À
bel =fg
nim =hhii3
77775
shared =2
66666666666666664com =8
>>>><
>>>>:class(economy )
month(ap ril)
destcity(paris)
deptcity(london)
how(plane)9
>>>>=
>>>>;
issues =­
?D.price(D)®
qud =hi
pm =­­
icm:acc*p os,icm:loadplan, ask(?C.month(C))®®
lu =2
4speaker =usr
moves =­­answer(april),answer(class(economy ))®®
score =13
53
777777777777777753
777777777777777777777777775
S>Okay.Whatdaydoyouwanttoleave?
4.6.2Localquestion accommo dation:fromISSUES toQUD
Ifamovewithunderspeci¯edcontentismadewhichdoesnotmatchanyquestion onthe
QUD,theclosestplacetolookforsuchaquestion isISSUES, andifitcanbefoundthere
itshouldbepushedonthelocalQUDtoenableellipsisresolution. Asaside-e®ect, the
question hasnowbeenbroughtintofocusandshould,ifitisnottopmost ontheopen
issuesstack,beraisedtothetopofopenissues.Aschematic overviewoflocalquestion
accommo dationisshowninFigure4.3. 
	


 
 



 



 "!$#%'&)(+*", -"
 
./&102%13!$46570289*2 :;&=<)
 %>&1,?
- @.A>&B!$4C<=*",
DE  FHGJI
 LKEMONI'PQI
LKEMONSRTD 



 "!$UV*XW2Y,
Z\[[[[[[]I>^


 
 
_a`D b.A&Y!$4C<=*",IYIG

I
@./&102%13!c

Y:d&)(	*2,eG
 @./&102%13!c

Y:d&)(	*2,D @



"!fUg*XW2B,-G
F
I
 

hQ
 b4i02<;&)(	%(	 0j/&D
`J
 @.A&Y!fUg*XW2B,R
Z\[[[[[[]
Z\[[[[[[[[[[[[[[[[[[]
Figure4.3:Localquestion accommo dation
Thistypeofaccommo dationcane.g.occurifaquestion whichwasraisedpreviously has
droppedo®thelocalQUDbuthasnotyetbeenresolvedandremainsonISSUES. Itshould
alsobenotedthatseveralaccommo dationstepscanbetakenduringtheprocessingofa

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION169
singleutterance; forexample, ifanissuethatisintheplanbuthasnotyetbeenraisedis
answeredelliptically .
(rule4.2)rule:accommodateIssues2QUD
class:accommodate
pre:8
>>>>>>>><
>>>>>>>>:$/private/nim/elem=usr-answer(A)
$domain ::shortanswer(A)
not$lexicon ::ynanswer(A)
in($/shared/issues,Q)
notin($/shared/qud,Q)
$domain ::relevant(A,Q)
eff:(
push(/ shared/qud,Q)
raise(/ shared/issues,Q)
Thesecondcondition in(rule4.2)checksthatthecontentoftheanswermovepickedout
bycondition 1issemanticallyunderspeci¯ed.Thethirdcondition imposesaconstrain t
onlocalquestion accommo dation,excluding shortanswerstoy/n-questions (\yes",\no",
\maybe"etc.).Theremaining conditions checkthattheanswer-contentisrelevanttoan
issuewhichisonissuesbutnotonqud.The¯rstoperationpushestheaccommo dated
question onqud,andthe¯nalupdateraisesthequestion tothetopofthestackofopen
issues.
4.6.3Issueclari¯cation
InIBiS2,useranswersareeitherpragmatically relevanttothequestion topmost onQUD,
ornotrelevantatall.Whenweaddmechanisms ofaccommo dationtoallowforanswers
tounraised questions, itbecomesnecessary todealwithcaseswhereananswermaybe
potentiallyrelevanttoseveraldi®erentquestions.
Semanticallyunderspeci¯edanswersmay(butneednot)bepragmatically ambiguous, i.e.
itisnotclearwhatquestion theyprovideananswerto.Thiscanberesolvedbyasking
thespeakerwhatquestion sheintendedtoanswer(orequivalently,whichpropositionshe
wantedtoconvey).
Inthiscase,wecanusethesamestrategy asfornegativegrounding, i.e.whenapragmat-
icallyambiguousutterance istobeinterpreted thesystemraisesaquestion whoseanswer
willbeintegrated insteadoftheambiguousanswer.Forexample, \Paris"mayberelevant
toeitherthedestination cityquestion orthedeparture cityquestion. Whenthetheclari-
¯cationquestion \DoyoumeanfromParisortoParis?"israiseditisexpectedthatthe

170 CHAPTER 4.ADDRESSING UNRAISED ISSUES
userwillanswerthisquestion, whichmeansthattheambiguousanswernolongerneedsto
beintegrated andcanbethrownaway8.
Inthiswayweseehowquestion accommo dation,amended withamechanismforresolving
whichquestion toaccommo date,canbeusedtoresolvepragmatic ambiguities inuserinput.
Theaccommo dationmechanismcanthusberegarded asare¯nemen toftheaccountof
grounding ontheunderstanding levelputforwardinChapter 3.Therulewhichselects
theissueclari¯cation issueisshownin(rule4.3).
(rule4.3)rule:clarifyIssue
class:selectaction
pre:8
>>><
>>>:in($/private/nim,usr-answer(A))
setof(C,in($/private/plan,¯ndout( Q))and
$domain ::relevant(A,Q),QSet)
$$arity(QSet)>1
eff:8
><
>:!setof(?P,in(QSet,Q)and$domain ::combine(Q,A,P),AltQ)
push(/ private/agenda,¯ndout( AltQ))
del(/private/nim,usr-answer(A))
The¯rstcondition picksouttheanswer-movefromthenimqueue.Thesecondandthird
conditions checkthatthereismorethanonequestion intheplantowhichtheanswer
isrelevant,byconstructing thesetofsuchquestions. The¯rstoperationconstructs the
alternativ e-question byapplying eachquestion inthesetconstructed incondition 2tothe
answertogetapropositionandpre¯xing thequestion operator'?'toeachproposition
togetay/n-question. Thealternativ equestion isthissetofy/n-questions. Thesecond
operationpushestheactiontoraisethealternativ equestion ontheagenda,andthe¯nal
operationremovestheanswermovefromnim;thisismotivatedabove.
Asampledialogue withissueclari¯cation isshownin(dialogue 4.2).
(dialogue 4.2)
S>Welcome tothetravelagency!
U>priceinformation please
S>Okay.Ineedsomeinformation. Howdoyouwanttotravel?
U>flightumparis
S>OK,byflight. Doyoumeanfromparisortoparis?
8IBiS3onlyhandlesfullanswerstoclari¯cation questions, i.e.\ToParis."or\FromParis.".Aslightly
moreadvancedsemanticswouldberequired tohandlecaseswheretheuseragaingivesanunderspeci¯ed
responsewhichresolvesthequestion, i.e.\To."or\From.".

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION171
Theuser'sutterance of\paris"isinterpreted asanswer(paris),whichisrelevanttotwo
questions intheplan:?x.destcity(x)and?x.deptcity(x).Because ofthis,theissue
accommo dationrulein1willnot¯reandtheanswerisnotintegrated. Thisallowsthe
clarifyIssue ruleto¯reintheselection phase.Bycombiningeachofthesequestions
withthecontentoftheanswer(paris),andturningeachresulting propositionintoay/n-
question, thesetf?destcity(paris),?dest city(paris)gisobtained. Thissetalsoworks
asanalternativ e-question, whichisusedasthecontentoftheclari¯cation question inthe
system's ¯nalutterance in(4.6).
Notethattheseclari¯cation questions aredynamically puttogether bythesystemand
thusdonotneedtobepre-programmed. Thismeansthattheapplication designer does
notevenneedtorealizethatanambiguityexists.
4.6.4Dependentissueaccommo dation:fromdomainresource to
ISSUES
Issueaccommo dation,introducedabove,presupposesthatthereisacurrentplaninwhich
tolookforanappropriate question; this,inturn,presupposesthatthereissomeissue
underdiscussion whichtheplanismeanttodealwith.Butwhatifthereiscurrentlyno
plan?
Inthiscase,itmaybenecessary tolookinatthesetofstoreddomain-sp eci¯cdialogue
plans(orcomeupwithanewplan)totryto¯gureoutwhichissuethelatestutterance
wasaddressing. Anappropriate planshouldcontainaquestion matchingsomeinformation
providedinthelatestutterance. Ifsuchaplanisfound,itispossiblethat,inaddition tothe
question answeredbythelatestutterance, afurtherissueshouldalsobeaccommo dated:
the\goal-issue" whichtheplaninquestion isaimedatdealingwith.Givenourde¯nition
ofdependence betweenquestions inSection2.8.2,thegoalissueisdependentontheissue
directlyaddressed, andhencewerefertothisasdependentissueaccommo dation.
Dependentissueaccommo dationisthustheprocessof¯ndinganappropriate background
issueandaplanfordealingwiththatissuewhichmakesthelatestutterance relevant,given
\normal" globalissueaccommo dation.Thatis,dependentissueaccommo dationisalways
followedbyglobalissueaccommo dation.Dependentissueaccommo dationapplieswhenno
issuesareunderdiscussion, andapreviously unraised question isansweredusingafullor
shortanswer(inthelattercase,globalissueaccommo dationmustinturnbefollowedby
localquestion accommo dation). Aschematic overviewofdependentissueaccommo dation
isshowninFigure4.4,andtheupdateruleisshownin(4.7).

172 CHAPTER 4.ADDRESSING UNRAISED ISSUES 
	


 
 



 



 "!$#%'&)(+*", -"
 
./&102%13!$46570289*2 :;&=<)
 %>&1,?
- @.A>&B!$4C<=*",
DE  FHGJI
 LKEMONI'PQI
LKEMONSRTD 



 "!$UV*XW2Y,
Z\[[[[[[]I>^


 
 
_a`D b.A&Y!$4C<=*",IYIG

I
@./&102%13!c

Y:d&)(	*2,eG
 @./&102%13!c

Y:d&)(	*2,D @



"!fUg*XW2B,-G
F
I
 

hQ
 b4i02<;&)(	%(	 0j/&D
`J
 @.A&Y!fUg*XW2B,R
Z\[[[[[[]
Z\[[[[[[[[[[[[[[[[[[]
DOMAIN
RESOURCE
Figure4.4:Dependentissueaccommo dation
(rule4.4)rule:accommodateDependentIssue
class:accommodate
pre:8
>>>>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>>>>:setof(A,$/private/nim/elem/snd=answer(A),AnsSet)
$$arity(AnsSet)>0
isempty($/private/plan)
$domain ::plan(DepQ,Plan)
forall(in( AnsSet,A),in(Plan,¯ndout( Q))and
$domain ::relevant(A,Q))
not($domain ::plan(DepQ0,Plan0)andDepQ06=DepQand
forall(in( AnswerSet,A),in(Plan0,¯ndout( Q))and
$domain ::relevant(A,Q)))
notin($/private/agenda,icm:und*int:usr *issue(DepQ))
eff:8
>>>>>><
>>>>>>:push(/ shared/issues,DepQ)
push(/ private/agenda,icm:accommo date:DepQ)
push(/ private/agenda,icm:und*p os:usr*issue(DepQ))
set(/private/plan,Plan)
push(/ private/agenda,icm:loadplan )
The¯rsttwoconditions construct asetofallnon-integrated answersandcheckthatthe
arityofthissetislargerthanzero,i.e.thatthereisatleastonenon-integrated answer.

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION173
Itshouldbenotedthatthisformulationoftherulereliesontheassumption thatall
unintegrated answershavebeenprovidedbytheuser.ThisistrueforIBiS3,sinceall
systemanswersareintegrated immediately andneverneedaccommo dation.However,ina
morecomplex systemthismaynotalwaysbetrue;inthiscase,therulewouldneedsome
slightmodi¯cations toonlypickoutusermoves.
Thethirdcondition checksthattheplanisempty.Theconsequence ofthisisthatde-
pendentissueaccommo dationisnotavailablewhensomeplanisbeingexecuted, soifan
issueisbeingdealtwiththeonlywaytoraiseanewissueistodosoexplicitly .Webelieve
thisisareasonable restriction, butifdesireditcanbedisabled byremovingthecondition.
However,doingsomaygiveproblems incasespeechrecognition mistakenlyrecognizes an
answernotmatchingthecurrentplan;ifthisanswertriggersdependentaccommo dation
thismayresultinconfusing utterances fromthesystem.
Thefourthand¯fthconditions lookforaplaninthedomainresource towhichallnon-
integrated answersarerelevant.Thiscanberegarded asasimpleversionofplanrecog-
nition:givenanobservedsetofactions(useranswers),tryto¯ndaplanandagoal(an
issue)suchthattheactions¯ttheplan.Here,theuseranswers¯ttheplanbybeingrele-
vantanswerstoquestions intheplan(moreprecisely,questions suchthattheplanincludes
actionstoresolvethem).
The¯nalcondition checksthatthereisonlyoneplantowhichalltheanswersarerelevant.
Ifthereareseveralsuchplans,theaccommo dationruleshouldnottrigger;instead, a
clari¯cation question shouldberaisedbythesystem(seeSection4.6.5).
Theupdatespushthedependentissueonissues,loadstheplan,andpushestheappropri-
ateICMmovesontheagenda:positivefeedbackconcerning theaccommo datedissue(\You
wanttoknowaboutprice.")andfeedbackindicating thatanewplanhasbeenloaded(\I
needsomeinformation"). Inaddition, ICMindicating accommo dationisproduced(see
Section4.7.1).
(dialogue 4.3)
S>Welcome tothetravelagency!
U>iwantaflight
getLatestMo ves
backupSharedUsr
accommo dateDependentIssue

174 CHAPTER 4.ADDRESSING UNRAISED ISSUES
8
>>>><
>>>>:push(/ shared/issues,?C.price(C))
push(/ private/agenda,icm:accommo date:?C.price(C))
push(/ private/agenda,icm:und*p os:usr*issue(?C.price(C)))
set(/private/plan,stackset([¯ndout(? D.how(D)),¯ndout(?E.destcity(E)),:::]))
push(/ private/agenda,icm:loadplan )
accommo datePlan2Issues©push(/ shared/issues,?A.how(A))
accommo dateIssues2QUD½push(/ shared/qud,?A.how(A))
raise(/ shared/issues,?A.how(A))
integrateUsrAnsw er
downdateISSUES
removeFindout
downdateQUD
backupSharedSys
selectIcmOther
selectIcmOther
2
666666666666666666666666664private=2
6666666666664agenda=­­
icm:loadplan, icm:acc*p os®®
plan =*¯ndout(?A.destcity(A))
¯ndout(?B.deptcity(B))
¯ndout(?C.month(C))
¯ndout(?D.deptday(D))
¯ndout(?E.class(E))
consultDB(? F.price(F))+
bel =:::
nim =:::3
7777777777775
shared =2
666666664com =©how(plane)ª
issues =­
?G.price(G)®
qud =hi
pm =­­greet®®
lu =2
4speaker =usr
moves =­­answer(plane)®®
score =13
53
7777777753
777777777777777777777777775
S>Alright. Youwanttoknowaboutprice.
U>
S>Ineedsomeinformation. Okay.Byflight. Whatcitydoyouwanttogo
to?
Thecurrentsolution hasanoptimistic strategy fordependentaccommo dation:theissue
isassumed tobeunderdiscussion andthesystemgivesexplicitpositivefeedbackofthis
assumption. Itmaybearguedthatapessimistic strategy ismoreappropriate fordependent
accommo dation;thiscanbeachievedbyreplacing thelistofupdatesin4withtheupdate

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION175
in(4.7).
(4.7)push(/ private/agenda,icm:und*int:usr *issue(D))
Thiswillprovideinterrogativ efeedbackfromthesystemconcerning whether thedependent
issueshouldbeopened,e.g.\Youwanttoknowaboutprice,isthatcorrect?". Iftheuser
givesapositiveresponsetothisfeedback,thesystemwillusethesameupdaterulesas
usualforintegrating theuser'sresponsetointerrogativ efeedback.
(dialogue 4.4)
S>Welcome tothetravelagency!
U>iwantaflight
getLatestMo ves
backupSharedUsr
accommo dateDependentIssue©push(/ private/agenda,icm:und*int:usr *issue(?C.price(C)))
downdateQUD
backupSharedSys
selectIcmUndNeg
selectIcmOther
S>flight. Idontquiteunderstand. Youwanttoknowaboutprice,is
thatcorrect?
getLatestMo ves
integrateOtherICM
integrateOtherICM
integrateUndIn tICM
U>yes
getLatestMo ves
integratePosIcmAnsw er
¯ndPlan
accommo datePlan2Issues
accommo dateIssues2QUD
integrateUsrAnsw er
downdateQUD

176 CHAPTER 4.ADDRESSING UNRAISED ISSUES
2
6666666666666666666666666666664private=2
666666666666664agenda=­­icm:loadplan, icm:und*int:usr *how(plane)®®
plan =*¯ndout(?A.how(A))
¯ndout(?B.destcity(B))
¯ndout(?C.deptcity(C))
¯ndout(?D.month(D))
¯ndout(?E.deptday(E))
¯ndout(?F.class(F))
consultDB(? G.price(G))+
bel =fg
nim =hhii)3
777777777777775
shared =2
66666666664com =fg
issues =¿?A.how(A)
?H.price(H)À
qud =hi
pm =­­icm:sem*p os:answer(plane),:::®®
lu =2
4speaker =usr
moves =oqueueansw er(yes)
score =13
53
777777777753
7777777777777777777777777777775
backupSharedSys
selectIcmOther
selectIcmOther
S>Ineedsomeinformation. byflight,isthatcorrect?
4.6.5Dependentissueclari¯cation
Ifnoplanisloadedandoneorseveralnon-integrated answersarerelevanttoseveralplans,
aclari¯cation question shouldberaisedbythesystemto¯ndoutwhichissuetheuser
wantsthesystemtodealwith.Thisisdonebytheselection rulein(rule4.5).
(rule4.5)rule:clarifyDep endentIssue
class:selectaction
pre:8
>>>>>>>>>>><
>>>>>>>>>>>:in($/private/nim,pair(usr,answer(A)))
setof(Q0,$domain ::plan(Q0,Plan)and
in(Plan,¯ndout( SomeQ))and
$domain ::relevant(A,SomeQ),
QSet0)
removeuni¯ables( QSet0,QSet)
$$arity(QSet)>1
eff:(
!setof(IssueQ,in(QSet,I)andIssueQ=?issue(I),AltQ)
push(/ private/agenda,¯ndout( AltQ))

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION177
The¯rstcondition checksifthereisatleastonenon-integrated useranswerleftafter
thesystemhasattempted tointegratethelatestuserutterance. Thesecondandthird
conditions constructs thesetQSetofdependentissuesthatthenon-integrated answeris
indirectly relevantto(i.e.issuesforwhichthereisaplancontaininganactiontoresolve
aquestion towhichtheanswerisrelevant)9.The¯nalcondition checksthatthereismore
thanonesuchdependentissue.
The¯rstupdateconstructs analternativ e-question bypickingouteachquestion IinQSet
andadding?issue( I)tothesetwhichconstitutes thealternativ e-question. The¯nal
updatepushesanactiontoresolvealternativ e-question ontheagenda.
Inthetravelagencydomain, anexample ofdependentissueclari¯cation occursifthe
user's¯rstutterance is\toParis",interpreted asanswer(destcity(paris)).Thisanswer
isrelevanttothequestion?x.destcity(x)whichoccursinboththeplanforaddressing
thepriceissueandthatforaddressing thevisaissue.Thisblocksthedependentissue
accommo dationrule.Inthedialogue in(dialogue 4.5),thesysteminsteadraisesa
clari¯cation question. NotethatIBiS3heremakesuseofthefactthatanask-movecan
supplyananswertoaquestion concerning whichissuetopursue.
(dialogue 4.5)
S>Welcome tothetravelagency!
U>toparis
getLatestMo ves
backupSharedUsr
downdateQUD
backupSharedSys
clarifyDep endentIssue½
!setof(E,in(set([need visa,?D.price(D)]),F)andE=issue(F),G)
push(/ private/agenda,¯ndout(G))
selectIcmUndNeg
selectAsk
S>toparis. Idontquiteunderstand. Doyoumeantoaskaboutvisaor
toaskaboutprice?
9Theremoveuni¯ables condition isusedtoremovemultipleoccurrences ofthesameissue.Notethat
theseoccurrences arenotidentical,sincetheymaydi®erintheidentityofvariables. Onemayofcourse
arguewhether setsshouldhavethisproperty,butinthecurrentTrindiKit implemen tationtheydo.

178 CHAPTER 4.ADDRESSING UNRAISED ISSUES
getLatestMo ves
integrateOtherICM
integrateOtherICM
integrateSysAsk
U>visa
getLatestMo ves
backupSharedUsr
integrateUsrAsk
downdateISSUES
¯ndPlan
accommo datePlan2Issues
integrateUsrAnsw er
downdateQUD
S>Okay.Ineedsomeinformation. toparis,isthatcorrect?
4.6.6Question reaccommo dation
InIBiS1andIBiS2theuserhasalimitedabilitytoreraisepreviously resolvedissues;this
willtypically resultinthesystemgivingthesameansweragain.However,thiskindof
reraising isnotveryusefulsincetheuserisnotabletomodifyherownanswerstothe
system's previous questions.
Globalquestionreaccommo dation(Issuereaccommo dation)
Ingeneral,iftheuserprovidesanalternativ eresolution ofanissuewhichhasbeenprevi-
ouslyresolved,thistriggersareraising ofthatissue.Iftheprevious answerisincompatible
withthenewone,theoldanswerisremoved.Thisallowstheusertochangehis/hermind
duringthedialogue. Hereisanexample dialogue withthesystem:
(dialogue 4.6)
S>Welcome tothetravelagency!
U>priceinformation please
S>Youaskedaboutprice. Howdoyouwanttotravel?

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION179
U>aflight, aprilthefifth
S>byflight. inapril. thefifth. Okay.Whatcitydoyouwanttogo
to?
U>london
S>Okay.tolondon.
U>actually, iwanttogoonthefourth
S>thefourth. Whatcitydoyouwanttogofrom?
Initially,integration oftheanswerusingintegrateUsrAnsw er(Section 3.6.6)willfail
sincethereisnomatchingquestion onissues.Thesystemwillthentryvariousaccom-
modationstrategies, including accommo dationfrom/shared/com formulatedin(rule
4.6).
(rule4.6)rule:accommodateCom2Issues
class:accommodate
pre:8
>>>>>><
>>>>>>:$/private/nim/elem/snd=answer(A)
in($/shared/com,P)
$domain ::question( Q)
$domain ::relevant(A,Q)
$domain ::relevant(P,Q)
eff:n
push(/ shared/issues,Q)
Thisaccommo dationrulelooksforananswerAamongthemoveswhichhavenotyetbeen
integrated (¯rstcondition). Itthenlooksforapropositionamongthesharedcommitmen ts
established inthedialogue sofar(secondcondition) whichaccording tothesystem's domain
resource isanappropriate answertosomequestion forwhichAisalsoananswer(thirdto
¯fthconditions). Giventhatinthissimplesystemanswerscanonlyberelevanttoasingle
question10,thisstrategy willbesuccessful inidentifyingcaseswherewehavetwoanswers
tothesamequestion. Asystemthatdealswithmorecomplex dialogues wherethisisnot
thecasewouldneedtokeeptrackofclosedissuesinaseparate listofclosedissues.Thus
theconditions willsucceedifthereisaquestion suchthatboththeuseranswerandastored
propositionarerelevantanswerstoit;intheexample dialogue above,\departure dateis
thefourth"and\departure dateisthe¯fth"arebothrelevantanswerstothequestion
\whichdaydoyouwanttotravel?".Ifsuchaquestion isfounditisaccommo datedto
issues,thatis,itbecomesanopenissueagain.
WhenaccommodateCom2Issues hasbeensuccessfully applied,theretractrulein(rule
10Thatis,inthefullforminwhichtheyappearin$/shared/com.\Chicago" canbeananswerto
\Whichcitydoyouwanttogoto?"and\Whichcitydoyouwanttogofrom?"butwhenithasbeen
combinedwiththequestions theresultwillbe\destination(Chicago)" and\from(Chicago)" respectively
anditisthiswhichisenteredintothecommitmen ts.

180 CHAPTER 4.ADDRESSING UNRAISED ISSUES
4.7)willremovetheincompatible information fromthesystem's viewofsharedcommit-
mentsrepresentedin/shared/com .
(rule4.7)rule:retract
class:integrate
pre:8
>>>>>>>>>>><
>>>>>>>>>>>:$/private/nim/elem/snd=answer(A)
in($/shared/com,P0)
fst($/shared/issues,Q)
$domain ::relevant(P,Q)
$domain ::relevant(A,Q)
$domain ::combine(Q,A,P)
$domain ::incompatible( P,P0)
eff:n
del(/shared/com,P0)
Theconditions herearesimilartothosein(rule4.6).Welookforanunintegrated
answer(¯rstcondition) whichisrelevanttoaquestion attheheadofthelistofopenissues
(thirdand¯fthconditions) andforwhichthereisalreadyarelevantanswerintheshared
commitmen ts(secondandfourthconditions). Finally,wedetermine thattheresultof
combiningtheanswerwiththequestion (sixthcondition) isincompatible withtheanswer
alreadyfound(seventhcondition). Ifallthisistruewedeletetheanswerwhichiscurrently
inthesharedcommitmen ts.Thiswill¯nallyallowthenewanswertobeintegrated bya
rulethatintegrates ananswerfromtheuser,andafurtherrulewillremovetheresolved
issuefromQUD.Notethatthisruleisofclassintegrate.Asisindicated inAppendixB,it
istriedbeforeanyotherintegration rule,toavoidintegration ofcon°icting information.
Notealsothatthe\incompatible" relationisde¯nedasapartofthedomainresource, and
canthusbedomainspeci¯c.Thesimplekindofrevision thatIBiScurrentlydealswith
isalsohandled bysomeform-based systems(although theyusuallydonotgivefeedback
indicating thatinformation hasbeenremovedorreplaced, asIBiSdoes).Forexample,
Chu-Carroll (2000)achievesasimilarresultbyextracting parameter valuesfromthelatest
userutterance andsubsequen tly(ifpossible)copyingvaluesfromtheprevious formfor
anyparameters notspeci¯edinthelatestutterance. Asimilarmechanismisreferredto
as\overlay"byAlexandersson andBecker(2000).Whilewearedealingonlywithvery
simplerevisionhere,therulein(rule4.7)andthe\incompatible" relationcanbeseenas
placeholders foramoresophisticated mechanismofbeliefrevision.
Itisalsopossibletoremovetheoldanswerbydenyingit(asserting itsnegation) asin
(dialogue 4.7).
(dialogue 4.7)

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION181
S>Welcome tothetravelagency!
U>priceinformation foraflighttoparisonaprilthefifth
S>Youaskedaboutprice. byflight. toparis. inapril. thefifth.
Whatcitydoyouwanttogofrom?
U>actually, notthefifth
S>notthefifth. So,whatdaydoyouwanttoleave?
Inthiscase,thesystemwillexplicitly reraisetheissuetogetanewresponsefromthe
user.Again,thesystemwillusetherulein25andsignalreraising using"so,".Allthe
ruleswillbeappliedasintheprevious case,butthedeparture datequestion willnotbe
removedsinceitisnotresolvedbythegivenanswer.Eventually,thisleadstothesystem
reraising thequestion.
Reraising ofdependentquestions (dependentissuereaccommo dation)
Insomecases,anissuemightbereraised whichin°uences theanswertoafurtherissue
thathasalsobeenresolved.Forexample, thechoiceofpriceclassfora°ightin°uences the
priceofthe°ight.Inthiscase,thein°uenced question alsoneedstobereaccommo dated
andansweredagain.
(dialogue 4.8)
S>Welcome tothetravelagency!
U>what'sthepriceofaflightfromlondontoparisaprilthefifth?
S>Youaskedaboutprice. byflight. fromlondon. toparis. inapril.
thefifth. Whatclassdidyouhaveinmind?
U>ascheapaspossible
S>cheap. Okay.Thepriceis123crowns.
U>actually, imightgoforbusiness class
S>firstclass. Okay.Concerning yourquestion aboutprice:Theprice
is1234crowns.
Therulethatachievesthereraising ofadependentquestion com-to-issuesaccommo dation
isshownin(rule4.8).

182 CHAPTER 4.ADDRESSING UNRAISED ISSUES
(rule4.8)rule:accommodateCom2IssuesDep endent
class:accommodate
pre:8
>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>:$/private/nim/elem/snd=answer(A)
in($/shared/com,P)
$domain ::question( Q)
$domain ::relevant(A,Q)
$domain ::relevant(P,Q)
isempty($/shared/issues)
$domain ::depends(Q0,Q)
in($/shared/com,P0)
$domain ::relevant(P0,Q0)
eff:8
>>>>>><
>>>>>>:del(/private/bel,P0)
del(/shared/com,P0)
push(/ shared/issues,Q0)
push(/ shared/issues,Q)
push(/ private/agenda,respond(Q0))
Thisruleissimilarto6exceptthatislooksforaquestion whichdependsonthequestion
it¯ndscorrespondingtotheanswerprovidedbytheuser.Itputsbothquestion ontothe
listofopenissuesandplanstorespondtothedependentquestion. Thisrule,ascurrently
implemen ted,isspeci¯ctotheparticular casetreatedinthesystem.Thereis,ofcourse,a
greatdealmoretosayaboutwhatitmeansforonequestion tobedependentonanother
andhowthesystemknowswhether itshouldrespondtodependentquestions orraisethem
withtheuser.
4.6.7Openingupimplicitgrounding issues
InChapter 3weoutlined ageneralissue-based accountofgrounding, whereissuesofcon-
tact,perception, understanding andacceptance ofutterances mayberaisedandaddressed.
Partsofthisaccountwereimplemen tedinIBiS2,allowingthesysteme.g.toraiseunder-
standing questions regarding theuser'sinput(e.g.\ToParis,isthatcorrect?"). Thisis
acaseofexplicitly raisingtheunderstanding-question whichresultsinthisquestion being
underdiscussion.
Thesystemcouldalsoproducepositiveexplicitfeedback(e.g.\ToParis");thiskindof
feedbackdoesnotexplicitly raisetheunderstanding question, andthereisnoobligation
ontheusertorespondtoitbeforethedialogue canproceed.However,itcanbeargued
thatevenpositivefeedbackraisesgrounding-related issues,although notexplicitly .This
isgivensomesupportfromthefactthatitispossiblefortheusertoprotestagainstthe
system's feedbackincasethesystemgotsomething wrong.

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION183
According toGinzburg, anassertion canbefollowedbyanyutterance addressing the
acceptance ofthisquestion asafact,e.g.bysaying\no!".Thisisthenregarded asa
shortanswertotheacceptance question; ine®ect,arejection. Inthecaseofanassertion
addressing understanding (i.e.positiveunderstanding feedback),theacceptance question
canbeparaphrased \Isitcorrectthatyoumeant'toParis'?".Thatis,theacceptance-
question regarding thesystem's understanding isexactlythesamequestion whichisraised
explicitly byaninterrogativ efeedbackutterance.
InIBiS,wehavechosennottorepresentacceptance-questions explicitly; however,inthe
caseofpositiveexplicitgrounding therearegoodreasonstodoso.Positivefeedbackhas
theadvantageofincreased e±ciency compared tointerrogativ efeedback,butthedisad-
vantageisthattheuserisnotabletocorrectthesystem's interpretation. However,ifthe
positivefeedbackmoveimplicitly raisesthequestion whether thesystem's interpretation
wascorrect,wecanusethistoallowtheusertorejectfaultysysteminterpretations. Be-
sides,wealreadyhavemechanisms inplaceforrepresentinganddealingwithanswersto
theunderstanding-question.
Tomodelthefactthattheacceptance question regarding understanding isimplicitrather
thanexplicit, wepushitontothelocalQUDonly.Iftheuseraddresses it(e.g.bysaying
\no"),theimplicit issueis\openedup",i.e.itbecomesanopenissue;itispushedon
ISSUES.
(rule4.9)rule:accommodateQUD2Issues
class:accommodate
pre:8
>>><
>>>:$/private/nim/elem/snd=answer(A)
in($/shared/qud,Q)
$domain ::relevant(A,Q)
notin($/shared/issues,Q)
eff:n
push(/ shared/issues,Q)
Therulein(rule4.9)picksoutanon-integrated answer-movewhichisrelevant toa
question onQUDwhichisnotcurrentlyanopenissue,andpushesitonissues.
Tohandleintegration responsestopositiveunderstanding feedback,wealsoneedtomod-
ifytheintegrateNegIcmAnsw erruledescribedinSection3.6.6.Asigni¯can tdi®erence
betweenpositiveandinterrogativ efeedbackinIBiSisthattheformerisassociatedwith
cautiously optimistic grounding, whilethelatterisusedinthepessimistic grounding strat-
egy.Thismeansthatanegativeresponsetofeedbackontheunderstanding levelmustbe
handled di®erentlydependingonwhether thecontentinquestion hasbeenaddedtothe
dialogue gameboardornot.Speci¯cally,ifthepositivefeedbackisrejected theoptimistic
grounding assumption mustberetracted.

184 CHAPTER 4.ADDRESSING UNRAISED ISSUES
(rule4.10) rule:integrateNegIcmAnsw er
class:integrate
pre:8
>>>>>>>><
>>>>>>>>:$/private/nim/fst/snd=answer(A)
fst($/shared/issues,Q)
$domain ::resolves(A,Q)
fst($/shared/qud,Q)
$domain ::combine(Q,A,P)
P=not(und( DP*C))
eff:8
>>>>>>>>>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>>>>>>>>>:pop(/private/nim)
pop(/shared/issues)
ifdo(in($/ shared/com,C)or
C=issue(Q0)andin($/shared/issues,Q0),[
/shared/qud:=$/private/tmp/DP/qud
/shared/issues:=$/private/tmp/DP/issues
/shared/com:=$/private/tmp/DP/com
/private/agenda:=$/private/tmp/DP/agenda
/private/plan:=$/private/tmp/DP/plan])
push(/ private/agenda,icm:und*p os:DP*not(C))
clear(/ private/nim)
initshift(/private/nim)
Therulein(rule4.10)issimilartothoseforintegrating \normal" useranswers(seeSec-
tion3.6.6),becauseofthespecialnatureofgrounding issues,weincludeissuedowndating
intheruleratherthanaddingafurtherrulefordowndating issuesforthisspecialcase.
Thismeanstherulehastocheckthattheanswerresolvesthegrounding issue,ratherthan
merelycheckingthatitisrelevant;thisisdoneinthethirdcondition. Thecontentresult-
ingfromcombiningtheissueonQUDandtheansweriscomputed inthe¯fthcondition.
Finally,thesixthcondition checksthatthecontentisnot(und( DP*C))whereDPisaDP
andCisthecontentthatisbeinggrounded (orinthiscase,notgrounded).
Thesecondupdateremovesthegrounding question fromissues.Thethirdupdate¯rst
checksifChasbeenoptimistically grounded. Inthiscase,theoptimistic grounding as-
sumption regarding thegrounding ofCisretracted. Thisiswherethenewtmp/usr ¯eld,
containingrelevantpartsoftheinformation stateastheywerebeforethelatestuserutter-
ancewasoptimistically assumed tobegrounded, isused.IfChasnotbeenoptimistically
assumed tobegrounded, nothinginparticular needstobedone.
Thefourthupdateaddspositivefeedbackthatthesystemhasundersto odthatCwasfalse.
Notethatnot(C)isnotaddedto/shared/com .Thereasonforthisisthatthenegated
propositionisnotsomething thattheuserintendedtoaddtotheDGB-itwassimplya
resultofamisunderstanding bythesystem.

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION185
Notealsothatthisfeedbackwillnotraiseagrounding issueaccording tothede¯nition of
question-raising ICMinSection3.7.1.Sincethecontentnot(C)hasnotbeenaddedto
theinformation state,thereisnopointindealingwithgrounding.
The¯naltwoupdatesclearthenimqueue,whichmeansthatthesystemwilldisregard any
moveswhichhavenotyetbeenintegrated. Onemotivationforthisisthatifthesystem
hasmisheard somepartoftheuser'sutterance, itislikelythatitalsomisheard therest.
Clearing thenimstackisalsousefulindialogues suchasthatin(dialogue 4.9).
(dialogue 4.9)
S>Welcome tothetravelagency!
U>flighttoparis
$S>flight. toparis. Idontquiteunderstand. Youwanttoknowabout
price,isthatcorrect?
U>no
S>Youdidnotaskaboutprice.
Whenintegrating theuser's\no"(anegativeresponsetosystemICM),theanswer-moves
realizedintheutterance \°ighttoparis"arediscarded;. Thesystemhastriedtomake
senseofitbuttheuserrejectedthisattempt. Atthispoint,thesystemsimplycannotdeal
withthemandratherthangettingstuckintryingto¯gureoutwhattheusermeant,the
movesarethrownout.
Notethattheruleasimplemen tedisactually moregeneralthanwhatisneededfor(or
usedin)IBiS3.SincethepartoftmpthatitbacktrackstodependsontheDPvariable,
inprinciple itcouldbeusedforcaseswheretheusergivespositivefeedbackandthesystem
rejectsthisasmistaken.
Asampledialogue withanegativeresponsetoanimplicitgrounding question isshownin
(dialogue 4.10).
(dialogue 4.10)
S>Welcome tothetravelagency!
U>visainformation please(0.78)(useractually saidsomething else)
getLatestMo ves
backupSharedUsr
integrateUsrAsk

186 CHAPTER 4.ADDRESSING UNRAISED ISSUES
¯ndPlan
downdateQUD
backupSharedSys
selectIcmOther
selectIcmOther
S>Okay.Youwanttoknowaboutprice.
getLatestMo ves
integrateOtherICM
integrateUndP osICM
2
666666666666666666666666666666666666664private=2
6666666666666666666666664agenda=­­
icm:loadplan®®
plan =*¯ndout(?A.how(A))
¯ndout(?B.destcity(B))
¯ndout(?C.deptcity(C))
¯ndout(?D.month(D))
¯ndout(?E.deptday(E))
¯ndout(?F.class(F))
consultDB(? G.price(G))+
bel =fg
tmp =2
66664usr=2
66664com =fg
qud =hi
issues =hi
agenda=hhii
plan =hi3
777753
77775
nim =hhii3
7777777777777777777777775
shared =2
666666664com =fg
issues =­
?H.price(H)®
qud =­
und(usr*issue(?I.price(I)))®
pm =©ask(?H.price(H))ª
lu =2
4speaker =sys
moves =½icm:und*p os:usr*issue(?I.price(I))
icm:acc*p os¾3
53
7777777753
777777777777777777777777777777777777775
U>no
getLatestMo ves
accommo dateQUD2Issues©
push(/ shared/issues,und(usr*issue(?A.price(A))))
integrateNegIcmAnsw er

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION187
8
>>>>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>>>>:pop(/private/nim)
pop(/shared/issues)
ifdo(in($/ shared/com,issue(?A.price(A)))or
issue(?A.price(A))=issue(D)andin($/shared/issues,D),[
/shared/qud:=$/private/tmp/usr/qud
/shared/issues:=$/private/tmp/usr/issues
/shared/com:=$/private/tmp/usr/com
/private/agenda:=$/private/tmp/usr/agenda
/private/plan:=$/private/tmp/usr/plan])
push(/ private/agenda,icm:und*p os:usr*not(issue(? A.price(A))))
clear(/ private/nim)
initshift(/private/nim)
downdateQUD
2
666666666666666666666666664private=2
666666666666664agenda=¿¿
icm:loadplan
icm:und*p os:usr*not(issue(? A.price(A)))ÀÀ
plan =hi
bel =fg
tmp =2
66664usr=2
66664com =fg
qud =hi
issues =hi
agenda=hhii
plan =hi3
777753
77775
nim =hhii3
777777777777775
shared =2
6666664com =fg
issues =hi
qud =hi
pm =©
icm:und*p os:usr*issue(?A.price(A)),icm:acc*p osª
lu =·speaker =usr
moves =©answer(not(und(usr *issue(?A.price(A)))))ª¸3
77777753
777777777777777777777777775
backupSharedSys
selectIcmOther
S>Youdidnotaskaboutprice.
Feedbackforutterances realizingseveralmoves
Inthecasewhereauserutterance providesanswerstoseveralquestions (andperhaps
alsoasksaquestion), thestrategy wehavechosenistoproducefeedbackforeachmove
individually togivetheuserachancetocorrectmishearings ormisunderstandings. If
positivefeedbackregarding onepieceofinformation isrejected, theoptimistic assumption
isretracted bymodifyingtheinformation stateaccording tothe/private/tmp/usr saved
state.Iffeedbackregarding onepieceofinformation isaccepted, thisinformation should
notdisappearifalaterfeedbackutterance fromthesystemshouldberejected.

188 CHAPTER 4.ADDRESSING UNRAISED ISSUES
(dialogue 4.11)
S>Welcome tothetravelagency!
U>priceinformation please
S>Okay.Ineedsomeinformation. Howdoyouwanttotravel?
U>aflighttoferris[0.78]
S>Okay.byflight.
U>yes
S>toparis.
U>no
S>nottoparis.So,whatcitydoyouwanttogoto?
Forexample, inthedialogue in(dialogue 4.11),theuseracceptsthesystem's feedback
\by°ight",butrejects\toparis";however,theinformation thattheuserwantstotravel
by°ightisretained.
Tohandlethis,eachtimepositivefeedbackisaccepted, thepartsofthe/private/tmp/usr
structure correspondingtotheshared ¯eldaremodi¯ed.Afurthermodi¯cation isthus
neededfortheintegratePosIcmAnsw errulepreviously de¯nedinSection3.6.6.

4.6.VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION189
(rule4.11) rule:integratePosIcmAnsw er
class:integrate
pre:8
>>>>>>>><
>>>>>>>>:$/private/nim/fst/snd=answer(A)
fst($/shared/issues,Q)
$domain ::resolves(A,Q)
fst($/shared/qud,Q)
$domain ::combine(Q,A,P)
P=und(DP*Content)
eff:8
>>>>>>>>>>>>>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>>>>>>>>>>>>>:pop(/private/nim)
pop(/shared/issues)
ifthenelse(Content=issue(Q0),[
push(/ private/tmp/DP/qud,Q0)
push(/ private/tmp/DP/issues,Q0)
push(/ private/tmp/DP/agenda,respond(Q0))],
add(/private/tmp/DP/com,Content))
ifdo(not(in($/shared/com,Content)or
Content=issue(Q0)andin($/shared/issues,Q0)),
ifthenelse(Content=issue(Q0),[
push(/ shared/qud,Q0)
push(/ shared/issues,Q0)
push(/ private/agenda,respond(Q0))],
add(/shared/com,Content)))
Theconditions aresimilartothoseoftheprevious versionoftherule,exceptforinspecting
issuesinsteadofqud.The¯rsttwoupdatesarealsothesame.Thethirdupdateaddsthe
contentContentwhichisbeinggrounded totmp/usr (incaseDPisusr,whichitalways
isinIBiS3).Thismeansthatiffuturefeedback(concerning thesameutterance) fromthe
systemisrejected, thesystemwillbacktracktoastatewhereContentisintegrated. The
conditionals inthethirdandfourthupdatesre°ectthefactthatquestions areintegrated
di®erentlyfrompropositions. Thefourthupdateissimilartothethirdupdateinthe
previous versionoftherule.
Implicitacceptance
Beforewemoveonthereisonemorethingtoconsider. Iftheuserdoesnotrejectthe
system's positivefeedbackconcerning apieceofinformation, thisisregarded asanimplicit
acceptance. Therefore, wealsoneedtoaddanoFollowuprule,forcaseswherepositive
systemfeedbackisnotrespondedtoatall(i.e.theuserdoesnottaketheturno®ered).

190 CHAPTER 4.ADDRESSING UNRAISED ISSUES
(rule4.12) rule:noFollowup
class:(none)
pre:(
$input,'TIMEDOUT'
in($/shared/pm,icm:und*p os:usr*Content)
eff:8
>>>>>><
>>>>>>:ifthenelse(Content=issue(Q),[
push(/ private/tmp/usr/qud,Q)
push(/ private/tmp/usr/issues,Q)
push(/ private/tmp/usr/agenda,respond(Q))],
add(/private/tmp/usr/com,Content))
The¯rstcondition istrueonlyiftheuserdidnotproduceanyutterance (thatthesystem
heard)duringherlatestturn11.Thesecondcondition checksthatthemovesperformed in
theprevious utterance includes positiveunderstanding feedbackregarding Content.The
¯rstupdatesareidenticaltothethirdupdateintheintegratePosIcmAnsw errulein
Section4.6.7.
Belowisadialogue example involvingpositive,implicitpositive,andnegativefollowups
tosystemfeedback.
(dialogue 4.12)
S>Welcome tothetravelagency!
U>priceinformation please
S>Okay.Letssee.Howdoyouwanttotravel?
U>aflighttoparisinapril
S>Okay.byflight.
U>yes
S>toparis.
U>
S>inapril.
U>no
S>notinapril.Whatcitydoyouwanttogoto?
Implicitquestions andellipticalanswers
Inthecaseofimplicitacceptance questions inEnglish(andSwedish)itappearsthatthey
canbeaddressed byshortanswers;however,wecannotassumethatallimplicit issues
canbeaddressed elliptically .TheuseofQUDforstoringimplicitissuesreliesonthefact
11SeeSection3.6.6foranexplanation of'TIMEDOUT'.

4.7.FURTHER IMPLEMENT ATION ISSUES 191
thatquestions onQUDhavenotnecessarily beenraisedexplicitly; however,questions on
QUDarealsobyde¯nition availableforresolution ofshortanswers.Torepresentimplicit
questions whichcannotbeaddressed elliptically ,afurtherlocaldatastructure forimplicit
questions underdiscussion wouldbeneeded.
4.7Furtherimplemen tationissues
Inthissectionwedescribepartsoftheimplemen tationofIBiS3whichhavenotbeen
discussed earlierinthischapter,andwhicharenotdirectlyreusedfromIBiS2.
4.7.1Dialogue moves
ForIBiS3,onlyonedialogue movehasbeenadded:ICMindicating accommo dationofa
dependentissue.InEnglish, wehavechosen\alright,youwanttoknowabout:::"toindi-
catethatsomeinference hasbeenperformed, andthatithasbeensuccessful. Thischoice
isbasedontheintuitionthatthisindicates someprocessinference whichhasconcluded
successfully; thisshouldberegarded asapreliminary andtemporarysolution awaiting
furthercorpusandusabilitystudies.
²icm:accommo date:Q:MoveifQ:Question
4.7.2IBiS3updatemodule
Updaterules
Themainadditions totheupdaterulecollection neededtohandleaccommo dationand
reaccommo dationweredescribedaboveinSection4.6.
Inthissection, wedescribechangesappliedtootherrulesfromIBiS2to¯twiththe
modi¯edinformation stateusedbyIBiS3.

192 CHAPTER 4.ADDRESSING UNRAISED ISSUES
Backinguptmp/usr
Thetmp/usr ¯eldcontainscopiesofpartsoftheinformation stateastheywerebefore
thelatestuserutterance wasintegrated. Iftheoptimistic assumption shouldturnoutto
bewrong,thetmp/usr ¯eldisusedtoundotheoptimistic grounding assumption without
theneedforcomplex revisionprocessing(seeSection4.6.7).
ThebackupSharedUsr in(4.8)iscalledeachtimeanutterance istobeintegrated and
storesthecurrentqud,issues,com,planandagenda¯elds;theseareallpotentially
a®ectedbytheintegration ofthemovesinthelatestutterance, andarealsoimportantfor
determining whattodonext.
Thisbacktrackingmechanismonlyappliestodomain-lev elcommunication; userICMmoves
arealwaysoptimistically assumed tobecorrectly understo odandintegration alwayssuc-
ceeds.SinceICM\subdialogues", suchasthatin(dialogue 4.13)areusedtoestablish
thefactthataprevious userutterance wasmisundersto odbythesystem,itisimportant
thattmp/usr isnotoverwritten duringthesubdialogue. Forexample, thebackupShare-
dUsrruleshouldnottriggerbeforeintegrating theuser's\pardon" ortheuser'sanswer
\no"tothesystemICM\byboat".
(dialogue 4.13)
S>Okay.Letssee.Howdoyouwanttotravel?
U>byboat[0.76](useractually saidsomething else)
S>Okay.byboat.
U>pardon?
S>Okay.byboat.
U>no
S>notbyboat.So,howdoyouwanttotravel?

4.7.FURTHER IMPLEMENT ATION ISSUES 193
(rule4.13) rule:backupSharedUsr
class:(none)
pre:8
>>>>>>>>>>><
>>>>>>>>>>>:$latestspeaker =usr
$latestmoves=Moves
notin(Moves,icm:X)
notin(Moves,nomove)
not(fst($/shared/qud,und(usr*C))and
in(A,answer(D))and
$domain ::relevant(D,und(usr*C)))
eff:8
>>>>>><
>>>>>>:/private/tmp/usr/qud:=$/shared/qud
/private/tmp/usr/issues:=$/shared/issues
/private/tmp/usr/com:=$/shared/com
/private/tmp/usr/agenda:=$/private/agenda
/private/tmp/usr/plan:=$/private/plan
The¯rstcondition checksthatthelatestspeakerwasindeedtheuser;ifnot,therule
shouldofcoursenottrigger. Thenextfourconditions areusedtopreventtriggering in
caseofanICMsubdialog,i.e.iftheuserproducedanICMmoveorrespondedtoonefrom
thesystem.(NotethatnomovemaycountasimplicitICMiftheuserdoesnotrespondto
ICMfromthesystem;seeSection4.6.7).The¯fthcondition checksiftheuserutterance
containsananswerrelevanttoagrounding-question onQUD.Thee®ectssimplycopythe
contentsoftmp/usr tothecorrespondingpathsintheinformation state.
Integration rulesandnim
InIBiS2,theintegration rulesinspectnimusingthecondition in(/private/nim,Moves).
SinceTrindiKit usesbacktrackingto¯ndinstantiationsofvariablesinconditions (see
AppendixA),thisresultsineachintegration rulelookingthroughthewholequeueofnon-
integrated moves.Thus,inIBiS2theordering oftheintegration rulesdetermines which
moveisintegrated ¯rst.Thisisokayfordialogues withaverysimplestructure, butwhen
dialogues becomemorecomplex (e.g.becauseofaccommo dation), theordering ofthe
movesbecomesmoreimportant.
Therefore, inIBiS3allintegration rulesinspectonlythe¯rstmoveonthenimqueue,using
thecondition fst(/private/nim,Move)orsimilar.Incombination withthequeue-shifting
techniquedescribedinSection4.7.2,thismeansthatthealgorithm triestointegratemoves
intheordertheywereperformed.

194 CHAPTER 4.ADDRESSING UNRAISED ISSUES
Updatealgorithm
Because ofthemorecomplex dialogues handled byIBiS3,theupdatealgorithm isabit
morecomplex thanthatforIBiS2.
(4.8)1ifnot($latestmoves==failed)
2thenhgetLatestMo ves,
3 trybackupSharedUsr ,
4 tryirrelevantFollowup,
5 repeath
6 repeat(hintegrate,
7 trydowndateissues,
8 tryremoveFindout ,
9 tryloadplani,
10 orelseapplyshift(/private/nim))
11 untilfullyshifted($ /private/nim),
12 applyshift(/private/nim),
13 tryselectaction
14 accommodatei,
15 applycancelshift(/private/nim ),
16 repeatexecplan,
17 trydowndatequdi
18elsehfailedFollowuporelseunclearFollowupi
Line1checksthattheinterpretation ofthelatestutterance wassuccessful (ofcourse,in
thecaseofsystemutterances thisisalwaystrue).Ifnot,thefailedFollowupandun-
clearFollowuprulesinline18,describedinSection3.6.8,aretried.Ifinterpretation
wassuccessful, thelatestmovesareincorporatedintheinformation stateproperbythe
getLatestMo vesrule(seeSection3.6.7).AfterthisthebackupSharedUsr ruleistried;
itsconditions aresatis¯ed, therulewilltriggerandstoreacopyofrelevantpartsofthein-
formation stateincasethesystemmakesanoptimistic grounding assumption whichturns
outtobemistaken(seeSection4.7.2).Also,beforeintegration starts,theirrelevantFol-
lowupruledescribedinSection3.6.8istriedtocatchcaseswhereasystemquestion has
beenignoredbytheuser.
Afterthis,aloopinvolvingintegration andaccommo dationisexecuted untilnothingmore
canbeintegrated (i.e.untiltheloopcannolongerbeexecuted). Thebasicideaisthis:
¯rsttrytointegrateasmanymovesaspossiblebycyclingthrough thenimqueue;then,
ifaccommo dationcanbeapplied, dothesamethingagain.Repeatthisuntilnothingcan
beintegrated andnoaccommo dationispossible.

4.7.FURTHER IMPLEMENT ATION ISSUES 195
The¯rstpartofthisloopstartsinline6andisitselfaloopforcyclingthrough allnon-
integrated movesandtryingtointegratethem.Ifintegration succeeds, thealgorithm tries
toremoveanyresolvedissuesfromissuesandplan,andifnecessary loadanewplan
(e.g.ifanaskmovefromtheuserwasintegrated). Thenittriesintegration again.If
integration fails,thenimqueueisshiftedonestep,i.e.thetopmost elementisremoved
fromthetopandpushedtotheendofthequeue.Then,integration istriedagain.This
continuesuntilthequeuehasbeencompletely cycledthrough once,andallmoveshave
hadashotatbeingintegrated.
Afterthisloopis¯nished, accommo dationwillattempt toadjustthe/shared ¯eldso
thatanymovesstillnotintegrated maybeundersto odonthepragmatic level,andinte-
grated.However,weneedtoavoidaproblem thatarisesasaconsequence ofhavingthe
integration ruleshandlepragmatic understanding, acceptance, andintegration inasingle
step.Theproblem arisesifsomemoveisregarded asrelevant(i.e.understo odonthe
pragmatic level)butnotacceptable, orifarelevantmovehaslowreliabilityandshould
beveri¯edbeforebeingintegrated. Inthiscase,accommo dationshouldnotbetriedsince
thepurposeofaccommo dationistounderstand someutterance onthepragmatic level,
andthishasalreadybeenachieved.Tosolvethisproblem, someactionselection rules(of
classselectaction)havebeenmovedfromtheselection moduletotheupdatemodule(for
alistoftheserules,seeAppendixB).Beforetryingaccommo dation,line13oftheupdate
algorithm thustriestoselectrejection movesandinterrogativ efeedbackmovestocatch
anymoveswhichhavealreadybeenundersto od.
Line14callstheaccommo dationruleclass.Ifthissucceeds, thereisachancethatsome
movesthatcouldnotbeintegrated beforecannowbeintegrated, sotheloopstarting in
line6isrestarted. Whennothingcanbeintegrated andnothingcanbeaccommo dated,
thesequence startingatline6andendingatline14cannotbeexecuted, andconsequen tly
theloopstartedinline5willbe¯nished. Line15cancelsshiftingofthenimqueue(see
SectionA.2.1).
Anyloadedplanisexecuted inline16byrepeatedlyapplying theexecplanruleclass
untilnomoreexecution ispossibleatthecurrentstageofthedialogue. Finally,QUDis
downdated.
Asanexample ofhowintegration andaccommo dationinteract,inthedialogue in
(dialogue 4.14),\toparis"isintegrated beforeaccommo dationistried,sotheonly
question availableforellipsisresolution of\paris"istheoneconcerning departure city.
(dialogue 4.14)
S>Welcome tothetravelagency!
U>pricelondontoparis[0.78]

196 CHAPTER 4.ADDRESSING UNRAISED ISSUES
S>Okay.Youwanttoknowaboutprice.
S>Ineedsomeinformation. toparis.
S>fromlondon.
S>Howdoyouwanttotravel?
Accommo dationruleordering Fortheaccommodateruleclass,theordering inwhich
thevariousaccommo dationrulesaretriedmaybeimportantinsomecases.Theordering
usedinIBiS3isshownin(4.9).
(4.9)accommodate
1.accommodateIssues2QUD
2.accommodateQUD2Issues
3.accommodatePlan2Issues
4.accommodateCom2Issues
5.accommodateCom2IssuesDep endent
6.accommodateDependentIssue
Thisorderinwhichtotrytheaccommo dationruleshasbeenchosenbasedonintuitions
abouthowaccessible questions aredependingonwheretheyareretrieved.Byexperiment-
ingwiththeordering, di®erentbehaviourscanbeobtained. Thecurrentordering should
beregarded asprovisional, and¯ndingthe\best"ordering isanobjectforfutureresearch.
Itmayalsosometimes benecessary todoclari¯cation ifananswermatchesseveralques-
tionswhoseaccommo dationruleshavethesameornearlythesamepriority;thishasnot
beenimplemen tedinIBiS3.
Possiblecriteriaforjudgingwhetheroneordering isbetterthananotherare(1)howreason-
abletheresulting behavioursare,(2)howe±cienttheoverallprocessingbecomes,and(3)
howsimilartohumancognitiveprocessescorrespondingtoaccommo dationtheprocessing
is(assuming question accommo dationiscognitivelyplausible).
First,accommo dationinvolvingonlyissuesandqudistried,sincethesearethecentral
structures fordealingwithquestions. Ifthisfails,accommo dationfromthedialogue plan
istried;ifthisfails,reaccommo dationfromcomisattempted. First\normal" reaccom-
modation,thendependentreaccommo dation.Finally,dependentissueaccommo dationis
tried;thisistriedlastsinceit¯ndsthequestion inthedomainresource ratherthanthe
information stateproper.

4.8.DISCUSSION 197
4.7.3Selection module
Theselection moduleisalmostunchangedfromIBiS2.Someminoradjustmen tshavebeen
madetoadapttherulestothechangesintheinformation statetype:thatobjectsinnim
arepairsofDPsandmoves,andthattmpisdividedintotwosubstructures.
4.8Discussion
Inthissectionwediscusssomevariations onIBiS3,showsomeadditional \emergen t"
features, anddiscussvariousaspectsofquestion accommo dation.
4.8.1Phrasespottingandsyntaxin°exibledialogue
Asitturnsout,IBiS3sometimes runsintotroubleiftheinterpreter recognizes several
answerstothesamequestion inanutterance. Whereas IBiS2wouldsimplyintegratethe
¯rstanswerandignorethesecond, IBiS3willtrytomakesenseofallthemovesinan
utterance, whichmayleadtoproblems iftheaccommo dationrulesarenotdesigned to
coverthecaseathand.
Forexample, ifthesystemrecognizes \paristolondon" asa¯rstutterance inadialogue,
thesystemwilltrydependentissueaccommo dation(seeSection4.6.4)andnotethatthe
setofanswers(answer(paris)andanswer(destcity(london) ))is(indirectly) relevantto
boththepriceissueandthevisaissue.Itmightseemthatthisiswrong,sincethetwo
answersareinfactrelevanttothesamequestion (regarding destination city)inthe\visa"
plan,whereas itisrelevanttotwoseparate questions (destination anddeparture city)in
the\price"plan,soitshouldbeindirectly relevantonlytothe\price"issue.Butin
general, onecannotrequirethatthetwoanswersmustbeanswerstodi®erentquestions,
sincethesecondanswermaybeacorrection ofthe¯rst.Thismayofcoursebesignalled
moreclearly,asin\toparisuhnotolondon", butthecorrection signalsmaybeleftout,
inaudible, ornotrecognized.
Onewaytosolvethisproblem istosometimes lookforconstructions whichrealizemore
thanonemove,anddosome\cleaning up"intheinterpretation phasesothattheDME
willnotgetintotrouble. Forexample, wecanaddalexicalentrylookingforphrases
oftheform\XtoY"andinterpretthisas\fromXtoY",i.e.answer(deptcity(X))
andanswer(destcity(Y)).
Arelatedproblem occursiftheuser¯rstchoosesGothenburgasdeparture cityandthen

198 CHAPTER 4.ADDRESSING UNRAISED ISSUES
says\notfromgothenburg london".Sinceplan-to-issues accommo dationhasprece-
denceovercom-to-issues, \london" willbeintegrated ¯rstbyaccommo datingthedes-
tination cityquestion, whichiswrong.Onesolution isofcoursetogivecom-to-issues
accommo dationprecedence, butthenfor\parisfromlondon",\fromlondon"will¯rst
beintegrated andthen\paris"willbeseenasarevisionofthedeparture city,whichis
alsowrong.
AsmentionedbeforeinSection4.7.2,theexactprecedence ordering betweenaccommo da-
tionrulesisatopicforfutureresearch,anditmaysometimes benecessary todoclari¯cation
ifananswermatchesseveralquestions whoseaccommo dationruleshavethesameornearly
thesamepriority.However,aneasiersolutionistoaddafurtherinterpretation rulesaying
that\notPX,Y"shouldbeinterpreted asaparaphrase of\notPX,PY".
Aslightlyirritating butnotveryserious\bug"inIBiSoccursifauserutterance contains
twoanswerstothesamequestion (e.g.\tokualalumpurtolondon"), andthe¯rstof
theseisaninvaliddatabase parameter. The¯rstanswerwillberejected, andappropriate
feedbackwillbeputontheagenda. Thesecondanswerwillthen(correctly) replacethe
¯rstanswerusingretraction, buttherejection feedbackconcerning thenowreplaced ¯rst
answerremains ontheagenda. Thismeansthatthesystemwillgivesomeirrelevant
information, namelythatthe¯rstanswerwasrejected. Thiscanbe¯xedtosomeextent
byinterpreting phrasesoftheform\PXPY"as\PY",i.e.thesecondpartisregarded as
acorrection ofthe¯rstpart.Similarly ,phrasesoftheform\PXno(P)Y",where\no"
isregarded asacorrection indicator andthesecondPisoptional, canalsobeinterpreted
as\PY".Ingeneral,itisusefultodetectcorrections intheinterpretation phasetoavoid
potentiallyexpensiverevisions intheintegration phase.
Ofcourse,thesesimple¯xeswillonlygetussofar,sincetheyonlycapture thevery
simplest cases.Forexample, wewouldnotbeabletonoticethatanutterance contains
twoanswerstothesamequestion unlesstheyareadjacent.Whatisreallyneededhereis
aproperparser(e.g.aHPSG-based parser)andgrammar.
Whatthisshowsus,then,isthattakingsyntaxintoaccountininterpretation becomes
increasingly importantwhenthedialogue managemen tbecomesmore°exible. Thismight
notbeverysurprising, butbystartingoutwithverysimplekeywordspottingandkeeping
itaslongaspossible,we¯ndoutexactlywhereitbecomesinsu±cien t.Hadweuseda
sophisticated parserfromtheoutset,wewouldnothavehadthisinsight.

4.8.DISCUSSION 199
4.8.2Relaxing constrain tsusingdenialanddependentreaccom-
modation
Ininquiry-orien teddialogue itisoftenusefultobeabletorelaxconstrain tsonthedatabase
search,especiallyincaseswherenoresultisreturned fromthedatabase. Asitturns
out,existingaccommo dationmechanisms inIBiS3incombination withtheslightlymore
complex database resultformatwhichwasintroducedasanextension ofIBiS2(seeSection
2.12.4)providesawayofdoingexactlythis.
Theideaisthis:ifthesystemreturnsanemptyorotherwise unsatisfactory database result,
theusercanmodifytheinformation giventothesystembydenyingsomepartofit.This
triggersreaccommo dationofthedependentissuethatthedatabase searchtriedto¯ndan
answerto,andthecorrespondingplanisreloaded. Sincesomeinformation isnowmissing,
thesystemwillagainaskforit;therestoftheactionsintheplanwillberemovedsincethe
questions havealreadybeenanswered.Byrejecting therepeatedquestion (e.g.bysaying
\Itdoesn'tmatter" or\Idon'tknow"),theusermakesthesystemsearchthedatabase
again,butthistimewithrelaxedconstrain ts.
(dialogue 4.15)
S>Welcome tothetravelagency!
U>aflighttoparisfromgothenburg inapril
S>Alright. Youwanttoknowaboutprice.
S>Letssee.Okay.Whatdaydoyouwanttoleave?
U>thefifth
S>Okay.Whatclassdidyouhaveinmind?
U>business class
$S>Okay.Sorry,thereisnothing matching yourrequest aboutprice.
U>okay,notbusiness classthen
S>Youwanttoknowaboutprice.
$S>Letssee.Okay.So,Whatclassdidyouhaveinmind?
U>itdoesntmatter
S>Thepriceis7654crowns. economy class.
Theexample in(dialogue 4.15)illustrates theprinciple. Tomakethisfeaturemore
useful,onewouldneedtobeabletogivedisjunctiv eanswers(\Iwanttoleaveonthe
twenty-¯rstorthetwenty-second"), specifyarangeofallowable\parameter values"(\I
wanttoleavebetweenthetwenty-¯rstandthetwenty-¯fth"), andgiveanswerswhichare
unspeci¯cinrelationtothequestion (\IwanttogotoFrance"inresponseto\Whatcity
doyouwanttogoto").Ofcourse,thisisausefulfeaturealsowhenprovidinganswersin
theinitialdatabase queryspeci¯cation stage.Thisisanareaforfurtherimplemen tation.

200 CHAPTER 4.ADDRESSING UNRAISED ISSUES
Thenicethingaboutthisapproachtorelaxing constrain tsisthatitrequires nospecial
machinery,butitemerges asapossibilitygivenmechanisms whichareindependentlymo-
tivated.
4.8.3\Smart" interpretation
Thedialogues in(dialogue 4.16)and(dialogue 4.17)showhowtheintegration strategy
inIBiS2isabletousealltheinformation providedinanutterance ascluesforhow
tointerpretunderspeci¯edinformation. Theinterpretation of\paris"asdestination or
departure citydependsonwhatotherinformation isgivenintheutterance, speci¯cally
whether destination ordeparture cityisspeci¯edelsewhere intheutterance.
(dialogue 4.16)
U>priceinformation please
S>Okay.Letssee.Howdoyouwanttotravel?
U>parisfromlondon[0.78]
S>Okay.fromlondon.
S>toparis.
(dialogue 4.17)
U>priceinformation please
S>Okay.Letssee.Howdoyouwanttotravel?
U>paristolondon[0.78]
S>Okay.tolondon.
S>fromparis.
Thesampledialogue in(dialogue 4.18)showshowthesystemcanintegratesuccessiv e
hintsfromtheuseraboutwhatshewantstodo.
(dialogue 4.18)
S>Welcome tothetravelagency!
U>umiwouldliketogotoparis
S>toparis. Idontquiteunderstand. Doyoumeantoaskaboutvisaorto
askaboutprice?
U>umiwanttogobyflight
S>Alright. Youwanttoknowaboutprice.

4.8.DISCUSSION 201
4.8.4Separating understanding, acceptance, andintegration
Theintegration rulesinIBiS3performseveraltasks:contextualinterpretation (e.g.for
underspeci¯edanswers),deciding whether toacceptorrejectamoveandtheircontents,
and(ifacceptance isdecidedon)integration ofthefulle®ectsofthemove.Whilethis
wasagoodapproachinIBiS1andIBiS2,inIBiS3thisapproachsometimes obscures the
workingsofthesystemandmakerulesrathercomplex.
Analternativ eapproachwouldbetoimplemen tcontextualinterpretation, theaccep-
tance/rejection decision, andintegration asseparate ruleclasses. Thecontextualinter-
pretation ruleswouldtakemoveso®aqueueofmovesprovidedbytheinterpretation
module(correspondingtothecurrentnim¯eld);wecouldcallthisqueueofpossiblyun-
derspeci¯edmovesSUM(SemanticallyUndersto odMoves).Theresulting fullyspeci¯ed
movescouldthenbeaddedtoaPUM(Pragmatically Understo odMoves)queue,which
wouldserveasinputfortheacceptance/rejection decision rules.Rejected moveswould
beputonaRM(Rejected Moves)queue,whichwouldlaterbeinspectedintheselection
phasetoproducesuitablefeedback.Accepted moveswouldbeaddedtoanAM(Accepted
Moves)stack,whichinturnwouldserveasinputtotheintegration rules.Whilethiswould
probably requirealargernumberofrulesandalsosomeadditional datastructures inthe
information state,thecomplexit yoftheindividual rulescouldbegreatlyreducedandthe
clarityoftheoverallprocessingwouldimprove.Itisalsolikelythatthiswouldleadtoa
lessbug-prone andtheoretically moresatisfying implemen tation.
4.8.5Accommo dationandthespeaker'sownutterances
Inthischapterwehavebeenmainlyconcerned withissueaccommo dationasawayof
interpreting utterances fromtheotherDP(foradialogue system,theuser).Buthowdoes
accommo dationrelatetothegeneration andintegration ofone'sownutterances? This
issuesdoesnotcomeupinIBiSsincethesystemneverproducesutterances thatcanbe
expectedtorequireaccommo dationonthepartoftheuser(e.g.endingalongdialogue
with\$100"ratherthan\Thepriceis$100").
Ginzburg allowsthespeakertoupdateQUDwithaquestion andthenaddressit.This
will(probably) requireaccommo dationonthepartofthehearer.Thesequence ofevents
hereisroughlythefollowing(Sisthespeaker,Hthehearer):
²SpushesQonQUD,thenaddresses Q
²Sintegrates A

202 CHAPTER 4.ADDRESSING UNRAISED ISSUES
²Haccommo datesQ,integrates A
However,wehavenotedaboveinSection3.3.4thatthisseemsinconsisten twiththeview
ofQUDassomething thatisassumed tobeshared.Possibly,onecouldhavea\fuzzier"
conceptofQUD(andperhapstheDGBingeneral) thatleavessomefreedom ofmodifying
itprivately,aslongasthehearercanbeexpectedtoaccommo datethesemodi¯cations.
Theotheralternativ eistoallowthespeakertogenerate utterances thatdonotexactly
matchthecurrentinformation state,andthenperformaccommo dationtointegrateher
ownutterance. Inthiscase,thesequence ofeventsisinstead:
²Saddresses Q,believingthattheinformation statecanbeadjusted (usingaccom-
modation)soastomakethisutterance felicitous
²SandHaccommo dateQandintegrate A
Whether thechoicebetweenthesetwoapproachesmakeanyrealdi®erence totheinternal
processingand/orexternal behaviourofthesystemremains afutureresearchissue.For
example, ifQUDisupdatedwithQbeforeAisproduced,andtheutterance realizing A
isinterrupted, shouldQberemovedfromQUD?
4.8.6Accommo dationvs.normalintegration
Aswehaveseen,question accommo dationallowsageneralized accountforhowanswers
areintegrated intotheinformation state,regardless ofthestatusofthecorresponding
question. Theaccommo dationproceduremayalsohaveside-e®ects (e.g.loadinganew
dialogue plan)whichservetodrivethedialogue forward.
Insteadofgivingrulesforaccommo dationandintegration separately ,onecoulddenythe
existence ofaccommo dationandjustgivemorecomplex integration rules.Theintegration
ruleforshortanswersrequires thatthereisaquestion ontheQUDtowhichthelatest
moveisanappropriate answer,andtheaccommo dationrulesareusedifnosuchquestion
canbefound.Thealternativ eistoskiptheQUDrequiremen t,thusincorporatingthe
accommo dationmechanisms intotheintegration rule,whichwouldthensplitintoseveral
rules.Forexample, therewouldbeoneruleforintegrating answersbymatchingthemto
questions intheplandirectly.
Apartfromthetheoretical argumen tthatquestion accommo dationprovidesageneraliza-
tionofthewayanswersareintegrated, therearealsopractical motivations.Inparticular,

4.9.SUMMAR Y 203
thefactthatseveralstepsofaccommo dationmaybenecessary tointegrateasingleanswer
meansthatthetotalnumberofrulesforintegrating answerswouldbehigherifaccom-
modationwasnotused-onewouldneedatleastoneintegration ruleforeachpossible
combination ofaccommo dationrules.
Afurtherargumen twhichisnotexplored inthisthesis(butseeEngdahl etal.,1999)is
thatquestion presuppositionandaccommo dationinteractwithintra-sententialinformation
structure ininteresting andusefulways.
4.8.7Dependentissueaccommo dationinVoiceXML?
OnaclosereadingoftheVoiceXML speci¯cation (McGlashan etal.,2001),itmayap-
pearthatVoiceXML o®ersamechanismsimilartodependentissueaccommo dation12.In
VoiceXML, agrammar canhavescopeoverasingleslot,overaform,oroverawhole
document(containingseveralforms).Givenagrammar withdocumentscope(de¯ning a
setofsentenceswhichtheVoiceXML interpreter willlistenforduringthewholedialogue),
iftheusergivesinformation whichdoesnotmatchthecurrentlyactiveform,VoiceXML
willjumptoaformmatchingtheinput13.Thiscorrespondsroughlytothedependentissue
accommo dationmechanisminIBiS.However,ifinputmatchesmorethanonetask(e.g.
\raisethevolume"couldmatchataskrelatedtotheTVoronerelatedtotheCDplayer),
VoiceXML willnotaskwhichofthesetaskstheuserwantstoperformbutinsteadgoto
theoneit¯nds¯rst,regardless ofwhattheuserintended.Generally ,itishardtoseehow
clari¯cation questions couldbehandled inageneralwayinVoiceXML, sincetheydonot
belongtoaparticular form.
4.9Summary
Toenablemore°exibledialogue behaviour,wemadeadistinction betweenalocaland
aglobalQUD(referring tothelatteras\openissues",orjust\issues"). Thenotionsof
12Thisdiscussion isbasedontheVoiceXML speci¯cation ratherthanhands-on experienceofVoiceXML.
Thismeansthatsomeunclarityremains aboutthecapabilities ofVoiceXML ingeneral, andindividual
implemen tationsofVoiceXML serversinparticular. Forboththesereasons, thediscussion shouldbe
regarded astentativeandopenforrevision. However,itshouldalsobepointedoutthatitisfairly
clearwhatissupportedinVoiceXML; mostoftheunclarities refertowhatispossible,butnotexplicitly
supported,inVoiceXML. Ingeneral,itismoreimportanttoknowwhatissupportedbyastandard than
whatispossible,sincealmostanythingispossibleinanyprogramming environmen t(givenasu±cient
numberofhacks).
13Although theVoiceXML documentationdoesnotprovideanyexamples ofthiskindofbehaviour,it
appearstobepossible,atleastinprinciple.

204 CHAPTER 4.ADDRESSING UNRAISED ISSUES
question andissueaccommo dationwerethenintroducedtoallowthesystemtobemore
°exibleinthewayutterances areinterpreted relativetothedialogue context.Question
accommo dationallowsthesystemtounderstand answersaddressing issueswhichhavenot
yetbeenraised.Incasesofambiguity,whereananswermatchesseveralpossiblequestions,
clari¯cation dialogues maybeneeded.

Chapter 5
Action-orien tedandnegotiativ e
dialogue
5.1Introduction
Inthischapter,weextendtheissue-based approachtosimpleaction-orien tedandnego-
tiativedialogue. First,wedealwithaction-orien teddialogue (AOD),whichinvolvesDPs
performing non-comm unicativeactionssuchase.g.addingaprogram toaVCRorreserv-
ingticketsinatravelagency.WeextendtheIBiSsystemtohandleasimplekindofAOD.
Inaddition toissuesandquestions underdiscussion, thissystemalsohastokeeptrackof
actions. Usually,itisusefulforanAODsystemtoalsohandleIOD.
Theconceptofissueaccommo dationisextended toactionaccommo dation.Wealsoshow
howmultiplesimultaneous plansmaybeusedtoenablemorecomplex dialogue structures,
andhowmultipleplansinteractwithactionsandissues.Weshowhowdialogue plans
maybeconstructed frommenus,andillustrate menu-basedAODwithexamples froman
implemen tationofamenu-basedVCRinterface.
Next,weturntonegotiativ edialogue, anddescribeanissue-based accountofasimplekind
ofcollaborativenegotiativ edialogue. Wealsosketchaformalization ofthisaccountand
discussitsimplemen tationinIBiS.
205

206 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
5.2Issuesandactionsinaction-orien teddialogue
InIBiS3,eachdialogue planwasaimedatresolving aspeci¯cissue.Ingeneral,ofcourse,
notalldialogue isaimedatresolving issues;oftenitisaimedtowardstheperformance of
some(non-comm unicative)action.Forexample, turningonoro®thelightsinaroom,
addingaprogram toaVCR,callingsomebodyup,ormakingareservationinatravel
agency.Actionorienteddialogue ingeneralplacesobligations onDPstoperformactions,
eitherduringthedialogue orafter.Forexample, bookingaticketinvolvesanobligation
ontheclerktosendatickettothecustomer, andonthecustomer topayfortheticket.
Requesting aVCRmanager toaddaprogram putsanobligation onthemanager addthe
program totheVCRtimerrecording memory bank.
WewillbedealingwithasimplekindofAOD,whereeachactioncanonlybeperformed
byoneoftheDPs,similartoourassumptions regarding issues.Thisallowsasimple
representationofactionsthatdoesnottakeintoaccountwhohastheobligation toperform
eachaction.Sincewearegivingexamples fromadevicecontroldomain(VCRcontrol),
wewillinfactonlydealwiththecasewhereallactionsareperformed bythesystem1.
Previous workwithGoDiS,thepredecessor ofIBiS,hasalsoaddressed thecasewherethe
userperformsalltheactions(Larsson, 2000,LarssonandZaenen,2000).
5.3Extending IBiStohandleactionorienteddialogue
Inthissection,wedescribeadditions totheinformation state,semantics,anddialogue
moves.Updateruleswillbediscussed inSection5.6.
5.3.1Enhancing theinformation state
Inthissection,weshowhowtheIBiSinformation stateneedstobemodi¯edtohandle
ActionOrientedDialogue. Thenewinformation statetypeisshowninFigure5.1.
Theonlyaddition istheactions¯eldwhichhasbeenaddedto/shared and/pri-
vate/tmp.Weassumetheactionsstackisanopenstack,whichisthesamestructure
thatweuseforissues.
1Ofcourse,eveninthissimpledomainitcannotreallybeassumed generally thatthesystemperforms
alltheactions; onecouldwellimagine aVCRcontroldialogue systemwhich,forexample, requests the
usertoinsertatapeintotheVCR.

5.3.EXTENDING IBISTOHANDLE ACTION ORIENTED DIALOGUE 207
2
66666666666666666666666664private:2
666666664agenda:OpenQueue(Action)
plan :OpenStack(PlanConstruct)
bel :Set(Prop)
tmp :"
usr:Tmp
sys:Tmp#
nim :OpenQueue(P air(DP,Move))3
777777775
shared :2
666666666664com :Set(Prop)
issues :OpenStack(Question)
actions :OpenStack(Action)
qud :OpenStack(Question)
pm :OpenQueue(Mo ve)
lu :"
speaker :Participan t
moves:Set(Move)#3
7777777777753
77777777777777777777777775
Tmp=2
666666664com :Set(Prop)
issues :OpenStack(Question)
actions :OpenStack(Action)
qud :OpenStack(Question)
agenda:OpenQueue(Action)
plan :OpenStack(PlanConstruct)3
777777775
Figure5.1:IBiS4Information Statetype
Semantics
TohandleactionAODweneedtoextendoursemantics.Giventhat®:Action,wehave
²action( ®):Proposition
²done(®):Proposition
Roughparaphrases ofthesepropositionsare\action ®shouldbeperformed (byanyDP
whocanperform®)",and\action ®hasbeensuccessfully performed", respectively.
Actionsandpostconditions
Thesetofactionsthatcanberequested dependsonthedomain; forexample, inthetravel
bookingdomainoneactionwouldbemakereservation ,andanexample fromtheVCR

208 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
controldomainisvcraddprogram.Fordialogues wherethetheuserrequests actionsto
beperformed bythesystem,eachsuchaction(whichwemayrefertoasagoal-action )is
associatedwithadialogue plan.
Indevicecontroldialogue, thereisalsoanadditional kindofactions,namelythosethat
arespeci¯edbythedeviceitself;werefertotheseasdeviceactions.Wewillalsogeneralize
overdeviceactionsusingtheUPnPprotocol(\UniversalPlug'n'Pla y",Microsoft, 2000,
Boyeetal.,2001,Lewinetal.,2001);thisrequires afurthertypeofupnpactionwhose
argumen tsisadeviceandadeviceaction.Thisallowsustoaccessmultipledevicesde¯ned
usingacommon interface.Thiswillbefurtherclari¯ed inSection5.4.1.
DeviceactionsandUPnPactionscanbethoughtofasatomicactions,whereasgoalactions
aremorecomplex; speci¯cally,theexecution ofasinglegoalaction(e.g.turningo®allthe
lightsinaroom)mayinvolvetheexecution ofseveraldeviceactions(e.g.turningo®each
individual light).
Inaddition todomain-sp eci¯cgoalactionsanddeviceactions,westillhavetheissue-related
actions¯ndout,raiseandrespondintroducedinChapter 2,andthesetofdialogue moves.
Forissues,theresolvesrelationprovidedawaytodecidewhenanissuehasbeensuccess-
fullyperformed andshouldbepoppedo®the/shared/issues stack.Foractions, we
insteadneedtode¯nepostconditions whicharede¯nedasrelations betweenactionsand
propositionsinthedomainresource; thesecanthenbeusedwhentodetermine whenan
actioncanberemovedfrom/shared/a ctions.
5.3.2Dialogue moves
Inaddition tothedialogue movesintroducedinChapters 2and3,IBiS4usesthefollowing
twomoves:
²request( ®),where®:Action
²con¯rm( ®),where®:Action
Thesetwomovesaresu±cientforactivities whereactionsareperformed instantlyornear-
instantly,andalwayssucceed. Iftheserequiremen tsarenotful¯lled, thecon¯rmmovecan
bereplaced byorcomplemen tedwithamoregeneralreport(®,Status)movewhichreports
onthestatusofaction®.PossiblevaluesofStatuscouldbedone,failed,pending,initiated
etc.;report(®,done)wouldcorrespondtocon¯rm( ®).

5.4.INTERA CTING WITH MENU-BASED DEVICES 209
5.4Interacting withmenu-baseddevices
Asasamplesubtypeofactionorienteddialogue wewillexploremenu-basedAOD.While
menuinterfacesareubiquitous inmoderntechnology theyareoftentediousandfrustrat-
ing.Themechanisms ofaccommo dationintroducedinChapter 4o®ersthepossibilityof
allowingtheusertopresentseveralpiecesofrelevantinformation atonetimeortopresent
information intheorderinwhichtheuser¯ndsmostnatural. Thismeansthatuserscan
usetheirownconception oftheknowledgespaceandnotbelockedtothatofthedesigner
ofthemenusystem.
First,wedescribeageneralmethodforconnecting devicestoIBiS,andthenweshowhow
menuinterfacescanbeconvertedintodialogue plansusingasimpleconversionschema.
5.4.1Connecting devicestoIBiS
Figure5.2:Connecting devicestoIBiS
Inthissectionwedescribebrie°yhowIBiScaninteractwithdevicesusingtheUPnP
protocol.InFigure5.2,weseeanimpression ofhowvariousdevicescanbeconnected to

210 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
IBiS.Wewillmainlybedealingwithdevicesthatcanbemodelledasresources, i.e.that
arepassive(orreactive)inthesensethattheycannotsendoutinformation unlessqueried
bysomeothermodule.Ofcourse,manydevicesarenotpassiveinthissensebutrather
active(orpro-active),e.g.burglaralarmsorrobots.Tohandleactivedevices,wewould
needtobuildaTrindiKit modulewhichcouldwriteinformation toadesignated partof
theinformation statebasedonsignalsfromthedevice;thisinformation couldthentrigger
variousprocessesinothermodules.Still,evenforanactivedevicethesolution wepresent
herewouldbeveryuseful;minimally ,wewouldonlyneedtoaddamodulewhichsetsa°ag
intheinformation statewheneverthedeviceindicates thatsomething needstobetaken
careof,triggering othermodulestoquerythedeviceaboutexactlywhathashappened.
TobeabletohookuppassiveUPnPdevicestoIBiS,weneedthefollowing:
1.devicehandlerresources whichcommunicatedirectlywiththedeviceitself;thedevice
handlers canbesaidtorepresentthedeviceinIBiS;
2.aresource typeforUPnPdevices,specifyinghowdevicesmaybeaccessed asobjects
ofthistype;
3.aresource interfacevariabletotheTISwhosevaluesareoftheUPnPresource type;
thisvariablehooksupdevicestotheTIS;
4.planconstructs forinteracting withdevices, andupdaterulesforexecuting these
planconstructs;
5.dialogue plansforinteracting withdevices.
UPnPdevicehandlers
Thedevicehandlermediates communication betweenIBiSandthedeviceitself,andcan
besaidtorepresentthedeviceforIBiS.Weassumethateachspeci¯cdevicehasaunique
ID,andisaccessed viaaseparate devicehandlerprocess.Adevicehandlerisbuiltfor
acertaindevicetype(e.g.thePanasonic NV-SD200 VCR),andeachdeviceofthattype
needstobeconnected toaprocessrunningthedevicehandler, inordertobeaccessed by
IBiS.
ForUPnPdevices, thedevicehandlercontainsaspeci¯cation partlyderivablefromthe
UPnPspeci¯cations, butmadereadable forIBiS(i.e.convertedfromXMLtoprolog).
Thedevicehandlerdoesthefollowing:
²speci¯esasetofactionsandassociatedargumen ts

5.4.INTERA CTING WITH MENU-BASED DEVICES 211
²speci¯esasetofvariables, theirrangeofallowedvalues,and(optionally) theirdefault
value
²routines forsettingandreading variables (devsetanddevget),forperforming
queries(devquery),andforexecuting actions(devdo)
²accesses thedevicesim ulation
TheUPnPresourceinterface
InordertohookupadevicetoIBiSoneneedstode¯neanabstract datatypefordevices
anddeclareasetofconditions andoperations onthatdatatype.ForIBiS,weimplemen t
agenericresource interfaceintheformofanabstract datatypeforUPnPdevices.
InUPnP,adeviceisde¯nedintermsof
²asetofvariables
²asetofactionswithoptional argumen ts
Inaddition togettingthevalueofavariable,settingavariabletoanewvalue,andissuing
acommand, wealsoaddtheoptionofde¯ningqueriestothedevice.Thesequeriesallow
morecomplex conditions tobechecked,e.g.whether twovariableshavethesamevalue.
Basedonthiswede¯nethedatatypeupnpdevasin(5.1);here,Varisadevicevariable;
Valisthevalueofadevicevariable, Queryisaquestion, Answerisaproposition, ®devis
adeviceaction,andPropSetisasetofpropositions.
(5.1) type:upnpdev
rel:(
devget(Var;Val)
devquery(Query,Answer)
op:(
devset(Var,Val)
devdo(®dev,PropSet)
Deviceactionsmayhaveoneormoreparameters; forexample, intheVCRcontroldomain
thereisanactionAddProgram whichtakesparameters specifyingdate,program number,
starttime,andendtime.ThePropSetargumen tofdevdoisasetofpropositions, some
ofwhichmayserveasargumen tsto®dev.Intheresource interfacede¯nition, thissetis
searchedbythedeviceinterfaceforargumen ts.ThismeansthatPropSetisnottheexact
setofargumen tsneededfor®dev;rather,itisarepositoryofpotentialargumen ts.

212 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
TherelationbetweenUPnPactions,deviceactions,anddeviceoperations isexempli¯ed
below:
²devdo(myvcr,AddProgram) isaUPnPaction,whichmayappearinaplan
²AddProgram isadeviceaction
²devdo(AddProgram, fchanneltostore(1),starttimetostore(13:45), :::g)
isadeviceupdateoperation
Inaddition tothedatatypede¯nition, onecande¯neobjectstobeofthatdatatype.For
eachdevicethatthesystemshouldrecognize, thedeviceIDshouldbedeclared tobeof
typeupnpdev.
5.4.2Frommenutodialogue plan
Havingdescribeageneralmethodforconnecting devicestoIBiS,wewillnowshowhow
menuinterfacescanbeconvertedintodialogue plansusingasimpleconversionschema.
Weassumemenuinterfacesconsistof(atleast)thefollowingelements:
²multi-choic elists,wheretheuserspeci¯esoneofseveralchoices
²dialoguewindows,wheretheuserentersrequested information usingthekeyboard
²tick-box,whichtheusercanselectorde-select
²pop-upmessages con¯rming actionsperformed system
Thecorrespondence betweenmenuelementsandplanconstructs isshowninTable5.1.
Regarding con¯rmations, weprovideageneralsolution forcon¯rming actionsinSection
5.6.3.Con¯rmations thusdonotneedtobeincluded intheplan.
5.4.3Extending theresolvesrelationformenu-basedAOD
Inmenu-basedAOD,thesystemmayaskanalternativ e-question aboutwhichactionthe
userwantsthesystemtoperform.Theusermaythenanswerbychoosingoneofthelisted

5.5.IMPLEMENT ATION OFTHEVCRCONTR OLDOMAIN 213
Menuconstruct Planconstruct
multi-choicelist actiontoresolvealternativ equestion aboutaction
h®1;®2;:::;®ni ¯ndout(n
?action( ®1),...,?action( ®n)o
)
tick-boxorequivalent actiontoresolvey/n-question
+/-P ¯ndout(? P)
dialogue window actiontoresolvewh-question
parameter= ¯ndout(? x:parameter(x))
pop-upmessage con¯rming ®con¯rm( ®)
Table5.1:Conversionofmenusintodialogue plans
alternativ es.However,iftheuserselectsanactionwhichisnotinthelistedalternativ es
butfurtherdowninthehierarchyofactions,thisshouldalsoberegarded asasananswer
thatresolvesthesystem's question. Tohandlethis,weneedtoextendthede¯nition ofthe
resolvesrelation(seeSection2.4.6).
(5.2)action( ®)resolves f?action( ®1),:::,?action( ®n)gif
²®=®ior
²®idominates ®(1·i·n)
Thedominates relationisde¯nedrecursivelyasin(5.3).
(5.3)®dominates ®0if
²thereisaplanPfor®suchthatPincludes¯ndout( AltQ)
and?action( ®)2AltQ,or
²®dominates someaction®00and®00dominates ®0
Theideais,then,thatdomination re°ectsthemenustructure sothatanactiondominates
anyactionsbelowitinthemenu.
5.5Implemen tationoftheVCRcontroldomain
AVCRmenusection
Westartfromasectionofthemenustructure foraVCRasshownin(5.4).

214 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
(5.4)²toplevel:hchange-pla y-status, change-channel, timer-
recording, :::i
{changeplaystatus:hplay,stop,:::i
{changechannel
¤new-channel=
¤con¯rmnewchannel
{timerrecording:hadd-program, delete-programi
¤addprogram
¢channel-to-store =
¢date-to-store =
¢start-time-to-store =
¢end-time-to-store =
¢con¯rmprogram added
¤deleteprogram
¢displayexistingprograms
¢program-to-delete:
¢con¯rmprogram deleted
{change-settings:hset-clock,:::i
DialogueplansforVCRcontrol
UsingtheconversionschemainTable5.1wecanconvertthemenustructures in(5.4)into
dialogue plansasthoseshownin(5.5).

5.6.UPDATERULES AND DIALOGUE EXAMPLES 215
(5.5)a.action :vcrtop
plan:h
raise(?x.action( x))
¯ndout(8
>>><
>>>:?action(vcrchangeplaystatus)
?action(vcrnewchannel)
?action(vcrtimerrecording)
?action(vcrsettings)9
>>>=
>>>;)
i
post:-
b.action :vcrtimerrecording
plan:¯ndout((
?action(vcraddprogram),
?action(vcrdeleteprogram))
)
post:done(vcraddprogram) or
done(vcrdeleteprogram)
c.action :vcraddprogram
plan:h
¯ndout(?x.channeltostore(x))
¯ndout(?x.datetostore(x))
¯ndout(?x.starttimetostore(x))
¯ndout(?x.stoptimetostore(x))
devdo(vcr,'AddProgram')
i
post:done('AddProgram')
5.6Updaterulesanddialogueexamples
Inthissectionweshowhowupdaterulesforactionorienteddialogue havebeenimple-
mentedinIBiS4,andgiveexamples ofdialogues fromtheVCRcontroldomain.
5.6.1Integrating andrejecting requests
First,weintroduceupdaterulesforintegrating requestmoves.Sincewearelimiting
thisimplemen tationtodomains wherethesystemperformsalltheactions, wewillnot
providerulesforintegrating requests fromthesystemtotheuser;however,thesecould
bestraightforwardlyimplemen tedsincetherelation betweensystemrequests anduser
requests isverysimilartotherelationbetweensystemanduseraskmoves.

216 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Theruleforintegrating userrequests isshownin(rule5.1).
(rule5.1)rule:integrateUsrRequest
class:integrate
pre:8
>>>>>><
>>>>>>:$/private/nim/fst/snd=request( A)
$/shared/lu/speaker ==usr
$score=Score
Score>0.7
$domain ::plan(A,Plan)
eff:8
>>>>>>>>>>><
>>>>>>>>>>>:pop(/private/nim)
add(/shared/lu/moves,request( A))
push(/ private/agenda,icm:acc*p os)
ifdo(Score·0.9,
push(/ private/agenda,icm:und*p os:usr*action( A)))
push(/ shared/actions,A)
push(/ private/agenda,A)
Thisruleissimilartothatforintegrating useraskmoves(seeSection3.6.6);insteadof
pushinganissueQonISSUESandQUD,andpushingrespond(Q)ontheagenda,thisrule
pushestherequested actionAon/shared/a ctionsand/private/agenda.
Asforuseraskmoveswealsoneedtodealwiththecasewherethesystemmustrejectan
actionsinceitdoesnothaveaplanfordealingwithit.Thisruleisshownin(rule5.2).
(rule5.2)rule:rejectAction
class:selectaction
pre:8
><
>:in($/private/nim,request( A))
$/shared/lu/speaker =usr
not$domain ::plan(A,Plan)
eff:8
><
>:del(/private/nim,request( A))
push(/ private/agenda,icm:und*p os:usr*action( A))
push(/ private/agenda,icm:acc*neg :action(A))
5.6.2Executing deviceactions
Theupdateruleforexecuting thedevdodeviceactionisshownin(rule5.3).

5.6.UPDATERULES AND DIALOGUE EXAMPLES 217
(rule5.3)rule:execdevdo
class:execplan
pre:n
fst($/private/plan,devdo(Dev,Adev))
eff:8
>>><
>>>:pop(/private/plan)
!$/shared/com=PropSet
devices /Dev::devdo(PropSet,Adev)
add(/private/bel,done(Adev))
Thecondition looksforadevdoupnpactionintheplan,withargumen tsDev,thedevice
pathname,andAdev,thedeviceaction.Theupdatespoptheactiono®theplan,and
appliesthecorrespondingupdatedevdo(PropSet,Adev)tothedeviceDev.Finally,the
propositiondone(Adev)isaddedthetheprivatebeliefs.
Inaddition, wehaveimplemen tedrulesforexecuting thedevget,devsetanddevquery
actions.
5.6.3Selecting andintegrating con¯rm-moves
Theselection ruleforthecon¯rmactionisshownin(rule5.4).
(rule5.4)rule:selectCon¯rmAction
class:selectaction
pre:8
>>><
>>>:fst($/shared/actions,A)
$domain ::postcond( A,PC)
in($/private/bel,PC)
notin($/shared/com,PC)
eff:n
push(/ private/agenda,con¯rm( A))
Theconditions inthisrulecheckthatthethereisanactionin/shared/a ctionswhose
postcondition isbelievedbythesystemtobetrue,however,thisisnotyetsharedinfor-
mation. Ifthisistrue,acon¯rmactionispushedontheagenda. Eventually,thisaction
(whichalsoisadialogue move)ismovedtonextmovesby(rule5.5).
(rule5.5)rule:selectCon¯rm
class:selectmove
pre:n
fst($/private/agenda,con¯rm( A))
eff:(
push(nextmoves,con¯rm( A))
pop(/private/agenda)

218 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Whenthecon¯rmation movehasbeenmade,itisintegrated bytherulein(rule5.6).
(rule5.6)rule:integrateCon¯rm
class:integrate
pre:n
$/private/nim/fst/snd=con¯rm( A)
eff:(
pop(/private/nim)
add(/shared/com,done(A))
Thisruleaddsthepropositiondone(A)tothesharedcommitmen tswhichenablesthe
downdateActions rulein(rule5.7)totrigger.
(rule5.7)rule:downdateActions
class:downdateissues
pre:8
><
>:fst($/shared/actions,A)
$domain ::postcond( A,PC)
in($/shared/com,PC)
eff:n
pop(/shared/actions)
ThisruleremovesanactionAwhosepostcondition isjointlybelievedtobetruefrom
actions2.
5.6.4Dialogue example: menutraversalandmultiplethreads
In(dialogue 5.1)weshowasampledialogue interaction withthemenu-based VCR
application. Itshowsbothmenutraversalandaccommo dation,aswellasdealingwith
multipletasks(issuesandactions).
(dialogue 5.1)
S>Welcome totheVCRmanager!
S>Letssee.WhatcanIdoforyou?
U>
2Notethatdone(®)istrivially apostcondition foranyaction®.

5.6.UPDATERULES AND DIALOGUE EXAMPLES 219
$S>Doyouwanttochangeplaystatus,changechannel ,gototimer
recording orgotosettings?
U>gototimerrecording
$S>Okay.Letssee.Doyouwanttoaddaprogram ordeleteaprogram?
U>addaprogram today
S>Okay.Letssee.Whatchannel doyouwant?
U>whatchannel isonnow
2
66666666666666666666664private=2
66664agenda=­­
icm:acc*p os®®
plan =hi
bel =©
currentchannel(1)ª
tmp =:::
nim =hhii3
77775
shared =2
6666666666664com =©
datetostore(today)ª
actions =*vcraddprogram
vcrtimerrecording
vcrtop+
issues =­?E.currentchannel(E)®
qud =hi
pm =©
ask(?A.channeltostore(A)),icm:loadplan, icm:acc*p osª
lu =·speaker =usr
moves =©
ask(?E.currentchannel(E))ª¸3
77777777777753
77777777777777777777775
S>Okay.Thecurrent channel is1
S>Returning toaddaprogram. Whatchannel doyouwant?
U>one
S>Okay.Whattimedoyouwanttostartrecording?
U>stopthevcr
deviceresourceissuescommand todevice:[UPnP]Stop
S>Okay.TheVCRisnowstopped.
S>Returning toaddaprogram. Whattimedoyouwanttostartrecording?
U>twelvethirty

220 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
S>Okay.Whattimedoyouwanttostoprecording?
U>twofifteen
deviceresourceissuescommand todevice:[UPnP]AddProgram(1,to day,1230,215)
S>Okay.Theprogram hasbeenadded.
S>Returning totimerrecording. Doyouwanttoaddaprogram ordeletea
program?
N.B.:Inthisdialogue, theuser'squestion \Whatchannelisonnow"isregarded asan
irrelevantfollowupto\Whatchanneldoyouwant?".Tochangethisonecouldadda
dependency betweenthesequestions tothedomainresource (seeSection2.8.2),asin(5.6).
(5.6)depends(?x.channeltoadd(x),?x.currentchannel( x)))
5.6.5Actionaccommo dationandclari¯cation
Wealsoimplemen tanaction-related counterparttotheruleaccommodateDependen-
tIssuepresentedinSection4.6.4.Thisallowstheusertoprovideparameters forsome
actionwithoutmakinganexplicitrequest.

5.6.UPDATERULES AND DIALOGUE EXAMPLES 221
(rule5.8)rule:accommodateAction
class:accommodate
pre:8
>>>>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>>>>:setof(A,$/private/nim/elem/snd=answer(A),AnsSet)
$$arity(AnsSet)>0
$domain ::plan(Action,Plan)
$domain ::action(Action)
forall(in( AnsSet,A),in(Plan,¯ndout( Q))and
$domain ::relevant(A,Q))
not$domain ::plan(Action0,Plan0)andAction06=Actionand
forall(in( AnsSet,A),in(Plan0,¯ndout( Q))and
$domain ::relevant(A,Q))
notin($/private/agenda,icm:und*int:usr *action( Action))
eff:8
>>>>>><
>>>>>>:push(/ shared/actions,Action)
push(/ private/agenda,icm:accommo date:Action)
push(/ private/agenda,icm:und*p os:usr*action( action))
set(/private/plan,Plan)
push(/ private/agenda,icm:loadplan )
ThisruleisverysimilartotheaccommodateDependentIssue(seeSection4.6.4),except
thatitaccommo datesadependentactionratherthanadependentissue.
Ifthesystem¯ndsseveralactionsmatchingtheinformation givenbytheuser,aclari¯cation
question israised.ThisisagainsimilartothebehaviourforissuesdescribedinSection
4.6.5;infact,therulebelowreplaces thepreviousclarifyDep endentIssuerule.
(rule5.9)rule:clarifyIssueAction
class:selectaction
pre:8
>>>>>><
>>>>>>:in($/private/nim,pair(usr,answer(A)))
setof(Action,$domain ::depends(®,Q)and
$domain ::relevant(A,Q),ActionS et)
removeuni¯ables( Actions,Actions0)
$$arity(Actions0)>1
eff:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:!setof(?IssueProp,in(Actions0,Issue0)and
not$domain ::action(Issue0)and
IssueProp=issue(Issue0),IssueQuestions )
!setof(?ActionP rop,in(Actions0,Action0)and
$domain ::action(Action0)and
ActionP rop=action(Action),ActionQuestions )
!union(IssueQuestions ,ActionQuestions ,AltQ)
push(/ private/agenda,¯ndout( AltQ))

222 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Thepreconditions checkthatthereismorethanoneplan(forperforming actionsorresolv-
ingissues)towhichallanswersin/private/nim arerelevant.The¯rstupdatecreates
analternativ equestion regarding allissueswhichthenon-integrated answersarerelevant
to,andthesecondupdatedoesthesameforactions. Thethirdupdatejoinsthesetwo
alternativ e-questions (setsofy/n-questions) intoasingley/n-question, whichisaddedto
theagendabythe¯nalupdate.
5.6.6Dialogue examples: actionaccommo dationandclari¯ca-
tion
Thedialogue in(dialogue 5.2)demonstrates actionaccommo dation,andthedialogue in
(dialogue 5.3)demonstrates aclari¯cation question bythesystem.
(dialogue 5.2)
S>Welcome totheVCRmanager!
S>Letssee.WhatcanIdoforyou?
U>todayfromfivethirtyonchannel one
S>Alright. addaprogram.
S>Letssee.Okay.Whattimedoyouwanttostoprecording?
(dialogue 5.3)
S>Welcome totheVCRmanager!
S>Letssee.WhatcanIdoforyou?
U>sixthirty
$S>sixthirty. Idontquiteunderstand. Doyouwanttoaddaprogram
orsettheclock?
U>addaprogram
$S>Okay.Letssee.Doyouwanttorecordfromsixthirtyoruntil
sixthirty?
U>fromsixthirty
S>Okay.Whatchannel doyouwant?

5.7.ISSUES UNDER NEGOTIA TION INNEGOTIA TIVE DIALOGUE 223
5.7Issuesundernegotiation innegotiativ edialogue
Wewillnowturntonegotiativ edialogue, anddescribeanissue-based accountofasimple
kindofcollaborativenegotiativ edialogue. Wealsosketchaformalization ofthisaccount
anddiscussitsimplemen tationinIBiS.
Westartfromaprevious formalaccountofnegotiativ edialogue (Sidner, 1994a)andargue
foraslightlydi®erentideaofwhatnegotiativ edialogue is.Wewanttomakeadistinc-
tionbetweentheprocessofaccepting anutterance anditscontent,whichappliestoall
utterances, andaconcept ofnegotiation de¯ned, roughly,asadiscussion ofseveralal-
ternativesolutions tosomeproblem. ThislatteraccountisformulatedintermsofIssues
UnderNegotiation (IUN),representingthequestion orproblem toberesolved,andaset
ofalternativ eanswers,representingtheproposedsolutions.
First,wewillgiveabriefreviewofSidner's theoryanddiscussitsmeritsanddrawbacks3.
Wethenprovideanalternativ eaccountbasedontheconceptofIssuesUnderNegotiation.
WeexplainhowIUNcanbeaddedtoIBiS,andgiveaninformation stateanalysis ofa
simplenegotiativ edialogue.
5.7.1Sidner's theoryofnegotiativ edialogue
Asthetitleofthepapersays,Sidner's (1994a)theoryisformulatedas\anarti¯cial dis-
courselanguage forcollaborativenegotiation". Thislanguage consistsofasetofmessages
(ormessage types)withpropositional contents(\beliefs"). Thee®ectsofanagenttrans-
mittingthesemessages toanotheragentisformulatedintermsofthe\stateofcommunica-
tion"afterthemessage hasbeenreceived.Thestateofcommunication includes individual
beliefsandintentions,mutualbeliefs,andtwostacksforOpenBeliefsandRejected Beliefs.
Someofthecentralmessages are
²ProposeForAccept (PFAagt1beliefagt2):agt1expresses belieftoagt2.
²Reject(RJagt1beliefagt2):agt1doesnotbelievebelief,whichhasbeen
o®eredasaproposal
²AcceptProp osal(APagt1beliefagt2):agt1andagt2nowholdbeliefasa
mutualbelief
3Anin-depth description ofSidner's accountanditsrelationtotheGoDiSsystem,including arefor-
mulationofSidner's arti¯cial negotiation language intermsofGoDiSinformation stateupdates,canbe
foundinCooperetal.(2001).

224 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
²Counter(COagt1belief1 agt2belief2) :Without rejecting belief1,agt1of-
fersbelief2 toagt2
Inaddition, therearethreekindsofacknowledgemen tmessages, themostimportantbeing
AcknowledgeReceipt (ARagt1beliefagt2),whichmayoccurafteraProposeFor-
Acceptmessage andresultsinbeliefbeingpushedonthestackforOpenBeliefs. Ac-
knowledgemen tindicates thataprevious message fromagt2aboutbeliefhasbeenheard;
theagentswillnotholdbeliefasamutualbeliefuntilanAcceptProp osalmessage has
beensent.
Whilewewillnotgiveadetailed analysis ofthee®ectsofeachofthesemessages, some
observationsareimportantforthepurposesofthispaper.Speci¯cally,acounter-proposal
(COagt1belief1 agt2belief2) isanalyzed asacompositemessage consisting oftwo
PFAmessages withpropositional contents.The¯rstproposedpropositionisbelief2
(the\new"proposal),andthesecondis(Supports (Notbelief1) belief2) ,i.e.that
belief2 supportsthenegation ofbelief1 (the\old"proposal).Exactlywhatismeant
by\supports"hereisleftunspeci¯ed,butperhapslogicalentailmentisatleastasimple
kindofsupport.
²(PFAagt1belief2 agt2)
²(PFAagt1(Supports (Notbelief1) belief2) agt2)
Sidner'sanalysisofproposalsisonlyconcerned withpropositional contents.ARequest for
actionismodelledasaproposalwhosecontentisoftheform(Should-Do AgtAction).
Aquestion isaproposalfortheactiontoprovidecertaininformation. Thisbringsusto
our¯rstproblem withSidner's account.
Problem1:Negotiation vs.utterance acceptance
InSidner's theory,alldialogue isnegotiativ einthesensethatallutterances (exceptac-
ceptances, rejections, andacknowledgemen ts)areseenasproposals.Thisiscorrectif
weconsider negotiation aspossiblyconcerning meta-asp ectsofthedialogue. Sinceany
utterance (content)canberejected, allutterances canindeedbeseenasproposals.
Soinonesenseof\negotiativ e",alldialogue isnegotiativ esinceassertions (andquestions,
instructions etc.)canberejected oraccepted aspartofthegrounding process.Butsome
dialogues arenegotiativ einanothersense,inthattheycontainexplicitly discussions about
di®erentsolutions toaproblem. Negotiation, onthisview,isdistinctfromgrounding.

5.7.ISSUES UNDER NEGOTIA TION INNEGOTIA TIVE DIALOGUE 225
Thereisthusastronger senseofnegotiation whichisnotpresentinalldialogue. A
minimumrequiremen tonnegotiation inthisstronger sensecouldbethatseveralalternativ e
solutions (answers)toaproblem (question orissue)canbediscussed andcompared before
asolutionis¯nallysettledon.Sidnerisawareofthisaspectofnegotiation, andnotesthat
\maintainingmorethanoneopenproposalisacommon featureofhumandiscourses and
negotiations." Whatwewanttodoisto¯ndawayofcapturing thispropertyindependently
ofgrounding andofotheraspectsofnegotiation, anduseitasaminimal requiremen ton
anydialogue thatistoberegarded asnegotiativ e.
Onourview,proposal-movesaremovesonthesamelevelasotherdialogue moves:greet-
ings,questions, answersetc.,andcanthusbeaccepted orrejectedonthegrounding level.
Accepting aproposal-moveonthegrounding levelmerelymeansaccepting thecontent
ofthemoveasaproposal,i.e.asapotentialanswertoaquestion. Thisisdi®erent
fromaccepting theproposedalternativ eastheactualsolution toaproblem (answertoa
question).
Togiveaconcrete example ofthesedi®erentconcepts ofnegotiativit y,wecancompare the
dialogues inExamples (5.5)and(5.6).
(5.7)A:TodayisJanuary6th.
proposeproposition
B(alt.1):Uhuh
acceptproposition
B(alt.2):No,it'snot!
rejectproposition
(5.8)S:wheredoyouwanttogo?
askquestion
U:°ightstoparisonseptember13please
answerquestion
S:thereisone°ightat07:45andoneat12:00
proposealternatives, giveinformation aboutalternatives
U:whatairlineisthe12:00one
askquestion
S:the12:00°ightisanSAS°ight
answerquestion
U:I'lltakethe7:45°ightplease
acceptalternative, answerquestion \which°ight?"
Thetypenegotiation in(5.7)concerns acceptance-lev elgrounding oftheutterance andits
content.Bycontrast,thetypeofnegotiation in(5.8)concerns domain-lev elissuesrather
thansomeaspectofgrounding.

226 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Problem2:Alternativ esandcounterproposals
Whenanalyzing atravelagencydialogue (Sidner,1994b),thetravelagent'ssuccessiv epro-
posalsof°ightsareseenascounterproposalstohisownprevious proposals,eachmodelled
asaproposition.Thedi®erence betweenproposalsandcounterproposalsisthatthelatter
notonlymakeanewproposalbutalsoproposesthepropositionthatthenewproposal
con°icts withtheprevious proposal(bysupportingthenegation oftheprevious proposal).
Thiscanbeseenasanattempt bySidnertoestablish theconnection betweenthetwo
proposalsassomehowconcerning thesameissue.
Thisanalysis isproblematic inthatitexcludes caseswherealternativ esarenotmutually
exclusive,whichisnaturalwhene.g.bookinga°ight(sincetheuserpresumably onlywant
one°ight)butnote.g.whenbuyingaCD(sincetheusermaywanttobuymorethanone).
Also,itseemsoddtomakecounterproposalstoyourownprevious proposals,especially
sincemakingaproposalcommits youtointendingtheaddressee toacceptthatproposal
ratherthanyourprevious ones.Inmanycases(including thetravelagencydomain) it
seemsthattheagentmayoftenbequiteindi®eren ttowhich°ighttheuserselects.Travel
agentsmayoftenmakeseveralproposalsinoneutterance, e.g.\Thereisone°ightat7:45
andanotheroneat12:00",inwhichcaseitdoesnotmakesensetosee\oneat12:00"as
acounterproposalasSidnerde¯nesthem.
Wedonotwanttousetheterm\counterproposal"inthesecases;whatweneedissome
wayofproposingalternativ eswithoutseeingthemascounterproposals.Thebasicproblem
seemstobethatwhenseveralproposalsare\onthetable"atonce,oneneedssomeway
ofrepresentingthefactthattheyarenotindependentofeachother.Sidnerdoesthis
byaddingpropositionsoftheform(Supports (Notbelief1) belief2) toshowthat
belief1andbelief2arenotindependent;however,thispropositionnotonlyclaimsthat
thepropositionsaresomehowdependent,butalsothattheyare(logically orrhetorically)
mutuallyexclusive.Inourview,thisindicates aneedforatheoryofnegotiation which
makesitpossibletorepresentseveralalternativ esassomehowconcerningthesameissue,
independentlyofrhetorical orlogicalrelations betweenthealternativ es.Negotiation, in
ourview,shouldnotingeneralbeseenintermsofproposalsandcounterproposals,butin
termsofproposingandchoosingbetweenseveralalternativ es.
5.7.2Negotiation asdiscussing alternativ es
Inthissection,wewillattempt toprovideamoredetailed description ofnegotiativ edi-
alogue.Clearly,negotiation isatypeofproblem-solving (DiEugenio etal.,1998).We
de¯nenegotiativ edialogue morespeci¯cally tobedialoguewhereDPsdiscussseveralal-
ternative solutions toaproblem(issue)beforechoosingone(orseveral)ofthem.Inline

5.7.ISSUES UNDER NEGOTIA TION INNEGOTIA TIVE DIALOGUE 227
withourissue-based approachtodialogue managemen t,weproposetomodelnegotiable
problems (issues)semanticallyasquestions andalternativ esolutions asalternativ eanswers
toaquestion.
Wealsoproposetokeeptrackofissuesundernegotiation andtheanswersbeingconsidered
aspotentialsolutions toeachissueinthe/shared/issues ¯eld,representedasquestions
associatedwithsetsofanswers.
Degreesofnegotiativit y
Starting fromthisde¯nition, wecandistinguish betweenfullynegotiativ edialogue and
semi-negotiativ edialogue (seealsoSection2.1.2).Innon-negotiativ edialogue, onlyone
alternativ ecanbediscussed. Insemi-negotiativ edialogue, anewalternativ ecanbeintro-
ducedbyrevising parameters oftheprevious alternativ e;however,previous alternativ es
arenotretained. Finally,innegotiativ edialogue: severalalternativ escanbeintroduced,
andoldalternativ esareretained andcanbereturned to.
Semi-negotiativ einformation-orien teddialogue doesnotrequirekeepingtrackofseveral
alternativ es.Allthatisrequired isthatinformation isrevisable, andthatnewdatabase
queriescanbeformedfromoldonesbyreplacing somepieceofinformation. Thisproperty
isimplemen tedinalimitedwayforexample intheSwedishrailwayinformation system(a
variantofthePhilipssystemdescribedinAustetal.,1994),whichafterprovidinginfor-
mationaboutatripwillasktheuser\Doyouwantanearlierorlatertrain?". Thisallows
theusertomodifytheprevious query(although inaverylimitedway)andgetinforma-
tionaboutfurtheralternativ es.However,itisnotpossibletocompare thealternativ es
byaskingquestions aboutthem;indeed,thereisnosignthatinformation aboutprevious
alternativ esisretained inthesystem. Theimplemen tationofreaccommo dationinIBiS3
(Section 4.6.6)alsoallowedsemi-negotiativ edialogue inthissense.
Factorsin°uencing negotiation
Thereareanumberofaspectsofthedialogue situation whicha®ectthecomplexit yof
negotiativ edialogues, andallowsfurthersub-classi¯cation ofthem.Thissub-classi¯cation
allowsustopickoutasubspeciesofnegotiativ edialogue toimplemen t.
Onourde¯nition, negotiation doesnotrequirecon°icting goalsorinterests,andforthis
reasonitmaynotcorrespondperfectlytotheeverydayuseoftheword\negotiation".
However,wefeelitisusefultokeepcollaborativity(i.e.lackofcon°icting goals)asa
separate dimension fromnegotiation. Also,itiscommon practice inother¯eldsdealing

228 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
withnegotiation (e.g.gametheory,economy)toincludecollaborativenegotiation (cf.
Lewinetal.,2000).
Asecondfactorin°uencing negotiation isthedistribution ofinformation betweenDPs.In
someactivities, information maybesymmetrically distributed, i.e.DPshaveroughlythe
samekindofinformation, andalsothesamekindofinformation needs(questions they
wantanswered).Thisisthecasee.g.intheCoconut(DiEugenio etal.,1998)dialogues
whereDPseachhaveanamountofmoneyandtheyhavetodecidejointlyonanumberof
furniture itemstopurchase.Inotheractivities, suchasatravelagency,theinformation
andinformation needsoftheDPsisasymmetrically distributed. Thecustomer hasaccess
toinformation aboutherdestination, approximatetimeoftraveletc.,andwantstoknow
e.g.exact°ighttimesandprices.Thetravelagenthasaccesstoadatabase of°ight
information, butneedstoknowwhenthecustomer wantstoleave,whereshewantsto
travel,etc.
Athirdvariableiswhether DPsmustcommitjointly(asine.g.theCoconutdialogues)
oroneDPcanmakethecommitmen tbyherself(ase.g.in°ightbooking).Inthelatter
case,theacceptance ofoneofthealternativ escanbemodelledasananswertoanIUN
bytheDPresponsibleforthecommitmen t,without theneedforanexplicitagreemen t
fromtheotherDP.Intheformercase,asimilaranalysis ispossible,buthereitismore
likelythatanexplicitexpression ofagreemen tisneededfrombothDPs.Thisvariable
mayperhapsbereferredtoas\distribution ofdecision rights".Insomedialogues (such
asticketbooking)oneDPhasthedecision rightsforallnegotiable issues;inthiscase
thereisnoneedforexplicitly representingdecision rights.However,ifdecision rightsare
distributed di®erentlyfordi®erentissues,anexplicitrepresentationofrightsisneeded.
Ticketbookingdialogue, anddialogue inotherdomains withcleardi®erences ininformation
anddecision-righ tdistribution betweenroles,hastheadvantageofmakingdialogue move
interpretation easiersincethepresence ofacertainbitsofinformation inanutterance
together withknowledgeabouttheroleofthespeakerandtherole-related information
distribution oftencanbeusedtodetermine dialogue movetype.Forexample, anutterance
containingthephrase\toParis"spokenbyacustomer inatravelagencyislikelytobe
intendedtoprovideinformation aboutthecustomer's desireddestination.
5.7.3IssuesUnderNegotiation (IUN)
InthissectionwediscussthenotionofIssuesUnderNegotiation representedbyquestions,
andhowproposalsrelatetosuchissues.Wealsodiscusshowthisapproachdi®ersfrom
Sidner's.

5.7.ISSUES UNDER NEGOTIA TION INNEGOTIA TIVE DIALOGUE 229
Negotiable issuesandactivity
Whichissuesarenegotiable dependsontheactivity.Forexample, itisusuallynotthe
casethatthenameofaDPisanegotiable issue;thisiswhyitwouldperhapsseem
counterintuitivetoviewanintroduction(\Hi,mynameisNN")asaproposal(asisdone
inSidner,1994b).However,itcannotberuledoutthatthereissomeactivitywhereeven
thismaybecomeamatterofnegotiation. Also,itisusuallypossibleinprinciple tomake
anyissueintoanegotiable issue,e.g.byraisingdoubtsaboutaprevious answer(see
Section5.8.2).
Alternativ esasanswerstoIssuesUnderNegotiation
GiventhatweanalyzeIssuesUnderNegotiation asquestions, itisnaturaltoanalyzethe
alternativ esolutions tothisissueaspotentialanswers.Onthisview,aproposalhasthe
e®ectofaddinganalternativ eanswertothesetofalternativ eanswerstoanIUN.ForaDP
withdecision rightsoveranIUN,givingananswertothisIUNisequivalenttoaccepting
oneofthepotentialanswersastheactualanswer.Thatis,anIUNisresolvedwhenan
alternativ eanswerisaccepted.
Hereweseehowourconceptofacceptance di®ersfromSidner.Onourviewaproposed
alternativ ecanbeaccepted intwodi®erentways:asaproposal,orastheanswertoanIUN.
Accepting aproposalmoveasaddinganalternativ ecorrespondstometa-levelacceptance.
However,accepting analternativ eastheanswertoanIUNisdi®erentfromaccepting an
utterance. Giventheoptimistic approachtoacceptance, allproposalswillbeassumed to
beaccepted asproposals;however,ittakesananswer-movetogettheproposedalternativ e
accepted asthesolution toaproblem.
Semantics
Torepresentissuesundernegotiation, wewillusepairsofquestions (usuallywh-questions
butpossiblyalsoy/n-questions) andsetsofproposedanswers.Thisisinfactanalter-
nativerepresentationofalternativ e-questions tothatwhichwehaveusedpreviously .The
additional semanticrepresentationisshownin(5.9).
(5.9)Q²AnsSet:AltQifQ:WHQ(orQ:YNQ)andAnsSet:
Set(ShortAns)

230 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
5.7.4Anexample
Inthe(invented)example inFigure5.3,thequestion onissuesis?x:desired°ight(x),
i.e.\Which°ightdoestheuserwant?".Theusersupplies information aboutherdesired
destination anddeparture date;thisutterance isinterpreted asasetofanswer-movesby
thesystemsinceitprovidesanswerstoquestions thatthesystemhasaskedorwasgoingto
ask.Asaresponsetothis,thesystemperformsadatabase searchwhichreturnstwo°ights
f1andf2matchingthespeci¯cation, andstoresthedatabase resultsin/private/bel.
Thesystemthenproposesthese°ightsasanswerstothecurrentIUN.Thesystemalso
supplies someinformation aboutthem.Asaresult,theIUNisnowassociatedwithtwo
alternativ eanswers,f1andf2.Finally,theuserprovidesananswertothecurrentIUN,
therebyaccepting oneofthesealternativ esasthe°ightshewantstotake.
Thisdialogue doesnotincludeanydiscussion orcomparison ofalternativ es,butitcould
easilybeextended tocovere.g.thedialogue in(5.8).
5.8Discussion
5.8.1Negotiation ininquiry-orien teddialogue
Themodelpresentedhereisnotcommitted totheviewthatnegotiation onlytakesplace
inthecontextofcollaborativeplanning, orevenaction-orien teddialogue. Inthesenseof
negotiativ edialogue usedhere,i.e.dialogue involvingseveralalternativ esolutions tosome
problem, negotiation mayalsoconcernmattersoffact.Thiscanbeusefule.g.intutorial
dialogue whereatutorasksaquestion, givessomealternativ eanswers,andthestudent's
taskistoreasonaboutthedi®erentalternativ esanddecideononeofthem.Inthetravel
agencydomain, itisoftennotnecessary toexplicitly represente.g.thatdeciding ona
°ightisaprecondition ofageneralplanfortravelling;instead,wecanrepresentitsimply
asafactconcerning which°ighttheuserwantstotake.
Arelatedpointisthatcollaborativeplanning dialogue isnotnecessarily action-orien ted
dialogue, sincetheactivityofplanning maybedirected atcomingupwithanabstract plan
regardless ofwhoactually performstheactionsintheplan.OnlywhensomeDPbecomes
obligedtocarryoutsomepartoftheplandoesthedialogue becomewhatwerefertoas
anaction-orien teddialogue.

5.8.DISCUSSION 231
A>flights toparis,june13
answer(desireddestcity(paris))
answer(desireddeptdate(13/5) )
B>OK,there's oneflightleaving at07:45andoneat12:00
propose(f1)
propose(f2)
inform(depttime(f1,07:45) )
inform(depttime(f2,12:00) )
2
66666666666666666666666666664private=2
6666664agenda=h¯ndout(?x:desired°ight(x))i
plan =h¯ndout(?x:credit-card-no( x))
updateDB(add reservation)i
bel =8
<
:°ight(f1)
depttime(f1,0745)
...9
=
;3
7777775
shared =2
66666666666666664com =8
>><
>>:depttime(f1,0745)
depttime(f2,1200)
desireddestcity(paris)
desireddeptdate(13/5) :::9
>>=
>>;
issues =h?x:desired°ight(x)²©
f1,f2ª
i
actions =hbookticketi
xsqud=hi
lu =2
664speaker =sys
moves =8
<
:propose(f1)
propose(f2)
:::9
=
;3
7753
777777777777777753
77777777777777777777777777775
A>I'lltakethe07:45one
answer(desired°ight(X)&depttime(X,07:45))
(aftercontextualinterpretation: answer(desired°ight(f1)))
2
666666666666666666666666664private=2
66664agenda=h¯ndout(?x:credit-card-no( x))i
plan =hupdateDB(add reservation)i
bel =8
<
:°ight(f1)
depttime(f1,0745)
...9
=
;3
77775
shared =2
66666666666666664com =8
>>>><
>>>>:desired°ight(f1)
depttime(f1,0745)
depttime(f2,1200)
desireddestcity(paris)
desireddeptdate(13/5) :::9
>>>>=
>>>>;
issues =hi
actions =hbookticketi
qud =hi
lu =2
4speaker =sys
moves =½
answer(desired°ight(f1)
:::¾3
53
777777777777777753
777777777777777777777777775
Figure5.3:Example dialogue

232 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
5.8.2Rejection, negotiation anddownshifting
Inthecontextofdiscussing referentidenti¯cation ininstructional assemblydialogues,
Cohen(1981)makesananalogy betweenshiftsindialogue strategy andshiftinggears
whendrivingacar.Inadialogue inhighgear,thespeakerintroducesseveralsubgoals
ineachutterance, whereas fewergoalsareintroducedinlow-geardialogue. Thetypeof
subgoals discussed byCohenaremainlyidentifyingareferent,requests topickupobjects,
andrequesting anassemblyaction.Aslongasthedialogue proceedssmoothlyandthe
hearerisabletocorrectly identifyreferentsandcarryoutactions, thespeakerrequests
assemblyactionsandexpectsthehearertobeabletoidentifyandpickuptheobjects
referredtowithoutexplicitrequests forthis.However,whenthisfailsandthehearerfails
toidentifyareferent,thespeakermayshiftintoalowergear(downshift) andmakeexplicit
requests foridenti¯cation ofreferents.Atalaterstage,thespeakermayshifttoahigher
gearandrequestthehearertopickupanobjectandthentoperformanassemblyaction.
Finally,thespeakermayreturntotheinitialgearandonlymakerequests forassembly
actions.
Severinsson (1983)viewstotheprocessofdownshifting asmakinglatentsubgames into
explicitsubgames. Inthecasementionedabove,thegoalsofthelatentsubgames are(1)
togetthehearertoidentifyareferent,and(2)forthehearertopickuptheobjectreferred
to.Inhighgear,thesesubgames arelatentinthesensethattheydonotgiverisetoany
utterances (dialogue moves).Whenthelatentsubgames becomeexplicit, theprocessthat
waspreviously carriedoutsilentlyisinsteadcarriedoutusingutterances.
Thisview¯tswellwiththeconceptoftacitmovesintroducedinSection4.4.2.Updatesfor
latentreferentidenti¯cation andutterance acceptance canberegarded astacitmoves(or
games)correspondingtoexplicitreferentidenti¯cation ornegotiation subdialogues, similar
tothewaythatquestion accommo dationupdatesaretacitmovescorrespondingtotheask
dialogue moves.
Boththesenotions, shiftinggearsindialogue andlatentsubgames, areusefulforshedding
lightontherelationbetweennegotiativ edialogue andutterance acceptance. Firstly,the
notionsofoptimism andpessimism regarding grounding strategies seemintimately related
tothenotionofgears,bothmetaphorically andfactually.Metaphorically ,wemaysaythat
anoptimistic driverwilluseahighergearthanapessimistic one;onlywhensheencounters
abumpyroadwillsheshiftintolowergear(thustakingamorepessimistic approach).
Later,whentheroadbecomessmoother,shemayagainresumeheroptimistic strategy
anduseahighergear.Similarly ,speakerscanbeexpectedtoswitchbetweenhigherand
lowergears,andbetweenoptimistic andpessimistic grounding strategies regarding the
grounding oftheirutterances. Thusweclaimthatthenotionofshiftinggearsisapplicable
notonlytoreferentidenti¯cation, butalsotoothergrounding relatedgames,including
utterance acceptance.

5.9.SUMMAR Y 233
InChapter 3,wetalkedaboutoptimism andpessimism inregardtogrounding onthe
acceptance level;wenowaddthatDPsmayshiftgearsregarding grounding ontheaccep-
tancelevel.Inadialogue inhighgear,thespeakeroptimistically assumes thehearerto
acceptherutterances. However,shouldthespeakerrejectsomeutterance, thedialogue is
downshifted andthelatentuptakesubgame becomesexplicit. Wewouldclaim(contrary
toSidner)thatitisonlywhenthedialogue isdownshifted inthissensethatmovessuchas
questions andassertions shouldberegarded asproposals.Atthisstage,DPsmayintroduce
alternativ estotheproposal,andtheymayarguefororagainstproposals.
TheconceptofdownshiftisrelatedtoGinzburg's casewhereaproposition pisrejected
asafactbut?pisaccepted asaquestion fordiscussion. Thisappearstobeapotential
caseofdownshifting whichcouldbemodelledbyregarding?p²fyes,nogasanissue
undernegotiation. Inaddition, alterations ofpmaybeproposed,roughlycorresponding
toClark's\cooperativealterations". Itappearsthiscanbemodelledasanissueunder
negotiation ?x.px²fa;b;:::g(wherepxisthepropositionpwithsomeargumen tareplaced
byx,andthusp=px(a)).Thealterations arethenrepresentedasalternativ esb;:::toa.
Thus,ifaquestion qhasbeenraisedinadialogue andifananswerarelevanttoqis
rejected(onthegrounding level),qmaybecomenegotiable (dependingontheactivity).If
so,theDPwhorejected amayproposeanalternativ eanswera0toq.Itisthenpossible
fortheDPstostarta(probably argumen tative)negotiation regarding whichofaanda0,
orperhapssomeotheranswer,shouldbeaccepted astheanswertoq.Wethusbelieve
thatdownshifting ofdialogue fromoptimistic acceptance tonegotiation canshedlighton
variousgrounding-related phenomena, e.g.alterations (seeSection3.2.1),andtherelation
betweengrounding andnegotiation.
5.9Summary
Firstly,weextended theissue-based approachtoaction-orien teddialogue, andimplemen ted
adialogue interfacetoaVCRwheredialogue planswerebasedonanexisting menuin-
terface. Wemodi¯edtheinformation statebyaddinga¯eld/shared/a ctions,and
alsoaddedtwonewdialogue movesspeci¯ctoAODrequestandcon¯rm.Wealsoimple-
mentedupdaterulesinIBiStohandleintegration andselection ofthesemoves,aswellas
interaction withadevice,andalsoprovidedanadditional accommo dationruleforactions.
Secondly ,weproposedaviewofnegotiation asdiscussing severalalternativ esolutions to
anissueundernegotiation. Onourapproach,anissueundernegotiation isrepresentedas
aquestion, e.g.what°ighttheuserwants.Ingeneral, thismeansviewingproblems as
issuesandsolutions asanswers.Thisapproachhasseveraladvantages.Firstly,itprovides
astraightforwardanintuitivelysoundwayofcapturing theideathatnegotiativ edialogue

234 CHAPTER 5.ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
involvesseveralalternativ esolutions tosomeissueorproblem, andthatproposalsintroduce
suchalternativ es.Secondly ,itdistinguishes twotypesofnegotiation (grounding-related
negotiation andnegotiation ofissues)andclari¯estherelationbetweenthem.

Chapter 6
Conclusions andfuture researc h
6.1Introduction
Inthis¯nalchapter,we¯rstsummarize theprevious chapters. Wewillthenusetheresults
toclassifyvariousdialogue typesandactivities, andsaysomething abouttherelationof
theissue-based modeltoGroszandSidner's (1986)accountofdialogue structure. Finally,
wediscussfutureresearchissues.
6.2Summary
InChapter 1,wepresentedtheaimofthisstudyandgavesomeinitialmotivationsfor
exploring theissue-based approachtodialogue managemen t.Wethengaveabriefoverview
ofthethesisandtherelatedversionsoftheIBiSsystem. Finally,wegaveaverybrief
introductiontotheTrindiKit architecture andtheinformation stateapproachtodialogue
implemen tedtherein.
InChapter 2,welaidthegroundw orkforfurtherexplorations ofissue-based dialogue
managemen tanditsimplemen tationintheIBiSsystem. Asastarting pointweused
Ginzburg's conceptofQuestions UnderDiscussion, andweexplored theuseofQUDas
thebasisforthedialogue managemen t(Dialogue MoveEngine) componentofadialogue
system. ThebasicusesofQUDistomodelraisingandaddressing issuesindialogue,
including theresolution ofelliptical answers.Also,dialogue plansandasimplesemantics
wereintroducedandimplemen ted.
235

236 CHAPTER 6.CONCLUSIONS AND FUTURE RESEAR CH
InChapter 3wediscussed generaltypesandfeatures offeedbackasitappearsinhuman-
humandialogue. Next,wediscussed theconceptofgrounding fromaninformation state
updatepointofview,andintroducedtheconcepts ofoptimistic, cautious andpessimistic
grounding strategies. Wethenrelatedgrounding andfeedbacktodialogue systems, and
discussed theimplemen tationofapartial-co veragemodeloffeedbackrelatedtogrounding
inIBiS2.Thisallowsthesystemtoproduceandrespondtofeedbackconcerning issues
dealingwiththegrounding ofutterances.
InChapter 4,wemadeadistinction betweenalocalandaglobalQUD(referring tothe
latteras\openissues",orjust\issues"). Thenotionsofquestion andissueaccommo dation
werethenintroducedtoallowthesystemtobemore°exibleinthewayutterances are
interpreted relativetothedialogue context.Question accommo dationallowsthesystemto
understand answersaddressing issueswhichhavenotyetbeenraised.Incasesofambiguity,
whereananswermatchesseveralpossiblequestions, clari¯cation dialogues maybeneeded.
InChapter 5,we¯rstextended theissue-based approachtoaction-orien teddialogue, and
implemen tedadialogue interfacetoaVCRwheredialogue planswerebasedonanexisting
menuinterface.Wethenproposedaviewofnegotiation asdiscussing severalalternativ e
solutions toanissueundernegotiation. Onourapproach,anissueundernegotiation is
representedasaquestion, e.g.what°ighttheuserwants.Ingeneral,thismeansviewing
problems asissuesandsolutions asanswers.
6.3Dialoguetypology
Inthissection, wewillusesomedistinctions madeinprevious chaptersasabasisfor
classifying dialogues anddialogue segmentsalongvariousdimensions. Whilethesedi-
mensions cantosomeextentbeusedtoclassifydialogue systems according tothekinds
ofdialogues theycanhandle,theyarenotintendedasaclassi¯cation ofhuman-human
dialogues. Rather,theyshouldberegarded asdescribing propertiesofdialogue segments.
Aswehavepreviously stated,wemakeadistinction betweenInquiry-orien tedandAction-
orienteddialogue according towhether thedialogue concerns non-comm unicativeactions
tobeperformed byaDP.Usually,butnotnecessarily ,AODsubsumes IOD.Oneexample
of\pure"actionorienteddialogue, wherenoquestions areasked,isWittgenstein's simple
\slab"gameinWittgenstein (1953).Another example issimplevoicecommand systems.
AODandIODareshownwiththeircorrespondingdialogue movesandinformation state
componentsinTable6.1.
Wecanalsoclassifydialogues according tothepresence orabsence ofgeneraldialogue
features suchasgrounding, question accommo dation,andnegotiation. Thisisdonein

6.3.DIALOGUE TYPOLOGY 237
Dialogue typeMovesIScomponents
IOD ask qud
answerissues
AOD request actions
con¯rm
Table6.1:Dialogue types
Table6.2.Whilegrounding andaccommo dationisprobably presentinallhuman-human
dialogue, negotiation maybelessfrequent.
Feature Moves IScomponent
Grounding icm tmp,grounding issues
Accommo dationaccommodateX-
(tacit)
Negotiation propose Question²Set(Answ er)
Table6.2:Dialogue features
Finally,wecanalsoclassifyactivities according tovariousaspectsofdialogue, asinTable
6.3.Notethatthisclassi¯cation isindependentofthatinTable6.2.Webelievethat
dialogue inalltheseactivities maybenegotiativ eornon-negotiativ e,andnegotiation may
beargumen tativeornon-argumen tative.
Activity Dialogue Result External Decision
type type type process rights
Database search IOD simple:priceetc. passiveuser
complex: itinerary
Ticketbooking AOD simple:bookticketpassiveuser
Simpledevicecontrol AOD simple:action passiveoruser
activeshared
O²ineplanning, incl. AOD complex: plan passiveshared
itinerary planning,
complex devicecontrol
Onlineplanning, incl. AOD complex: plan activeshared
rescueplanning (TRIPS)
Explanation IOD complex: explanation passiveshared
Tutorial IODorAODcomplex ? tutor
Table6.3:Activities
Wewillnowrelatethetaxonom yabovetothetaxonomies inDahlbÄack(1997)andAllen
etal.(2001).Itshouldbestressed thatneitherAllennotDahlbÄackhavethesamegoals
withtheirclassi¯cations aswedohere,andthoughsomeformulations mayappearcritical
theyaremainlyintendedtoclarifytherelationbetweentheseclassi¯cations andours.

238 CHAPTER 6.CONCLUSIONS AND FUTURE RESEAR CH
6.3.1Relation toDahlbÄack'sdialogue taxonom y
DahlbÄack(1997)taxonomizes dialogue according tosevencriteria:
²modality:spokenorwritten
²kindsofagents:humanorcomputer
²interaction: dialogue ormonologue
²context:spatial,temporal
²numberandtypeofpossible/sim ultaneous tasks
²dialogue-task distance: longorshort
²kindsofsharedknowledgeused:perceptual, linguistic, cultural
Ourtypologyappearstobeonadi®erentlevelandisindependentofmanyofDahlbÄack's
criteria, andbothcoverimportant(butforthemostpartdistinct) dimensions ofclassi¯-
cation.Ingeneral, theinteraction betweenthedimensions coveredbyDahlbÄackandthe
onescoveredinourtypologyisaninteresting areaforfutureresearch.
Modalityisnotincluded inourtypology;however,IBiSisabletousebothwrittenand
spokenlanguage. Regarding kindsofagents,wehaveofcoursebeendealingmainlywith
human-computer interaction; however,wehavebasedboththeoryandimplemen tationon
observationsofhuman-humandialogue.
Ourdialogue typologyshouldberegarded asprimarily concerning dialogue interaction;
however,aversionofGoDiS(thepredecessor ofIBiS)hasbeenusedtoproducemonologue
outputfromadomainplanspeci¯cation whichwasalsousedforgenerating dialogue plans
(seeLarssonandZaenen,2000).
Wehavenotincluded aspectsofspatialandtemporalcontextinourtypology;forour
theoryandsystemwehavenotexplored theimpactofanyotherkindofcontextthan
(pre-stored information about)thedomain(activity)andthedialogue itself.
Regarding thenumberandtypeofpossibleand/orsimultaneous tasks,theuseoftheissues
andactionsstacksallows,atleastinprinciple, anarbitrary numberofsimultaneous tasks.
Sincethesimplest versionofourtheoryandsystemcanhandlethis,wehavenotusedthis
asadimension ofclassi¯cation.

6.3.DIALOGUE TYPOLOGY 239
Thedialogue-task distance dimension isperhapslessobviousthantheothers.Thisisbased
ontheobservationthatsomekindsofdialogue haveastructure closelycorresponding
tothetaskstructure (e.g.planning oradvisory dialogue), whilesomehavea\longer
distance" betweenthesetwostructures (e.g.information retrievaldialogue). DahlbÄack
arguesthatfordialogues withashortdialogue-task distance, intention-based methodsfor
dialogue actrecognition isbothmoreusefulandeasierthanfordialogues withalong
dialogue-task distance. Forthelatter,surface-based actinterpretation iseasierandmore
appropriate, whereasintention-based methodsarelessusefulandmoredi±cult. Regarding
thisdimension, wehavebeenmostlyconcerned withdialogues withalongdialogue-task
distance, andifDahlbÄackisrightanintention-based andcontext-dependentinterpretation
modulewillbeneededwhenextending theissue-based approachtoe.g.collaborative
planning dialogue. Whilethismaya®ecthowdialogue movesarede¯ned, webelieve
(although wecannotbesure)thatthesetofdialogue moveswehaveproposedinour
taxonom ycanstillbemaintained.
Finally,regarding thekindsofsharedknowledgethatareused,ourtaxonom ydoesnotsay
much.Wehavenotbeenconcerned withtheperceptual andcultural context,exceptto
theextentthattheseareencodedinthestaticdomainknowledgeresources. Theuseof
domain-sp eci¯clexiconscanperhapsberegarded asasimplistic formoflinguistic context.
6.3.2Relation toAllenet.al.'sdialogue classi¯cation
Theclassi¯cation byAllenetal.(2001)appearstobecloserinspirittotheoneproposed
here.Dialogues areclassi¯ed according tothedialogue managemen ttechnique(minimally)
required byadialogue systemcapableofhandling therespectivekindsofdialogue. Each
classisfurtherspeci¯edbyexample tasks,adegreeoftaskcomplexit y(ranging fromleast
tomostcomplex), andasetofdialogue phenomena handled.
²¯nite-state script
{example task:long-distance calling
{dialogue phenomena: useranswersquestions
²frame-based
{example tasks:gettingtraintimetable information
{dialogue phenomena: useranswersquestions, simpleclari¯cations bysystem
²setsofcontexts
{example tasks:travelbookingagent

240 CHAPTER 6.CONCLUSIONS AND FUTURE RESEAR CH
{dialogue phenomena: shiftsbetweenpredetermined topics
²plan-based models
{example tasks:kitchendesignconsultan t
{dialogue phenomena: dynamically generated topicstructures, collaborativene-
gotiation subdialogues
²agent-basedmodels
{example tasks:disasterreliefmanagemen t
{dialogue phenomena: di®erentmodalities(e.g.plannedworldandactualworld)
The¯rstthingtonoteaboutthisclassi¯cation isthatitdoesnotdistinguish separate
dimensions ofclassi¯cation, butratherreduceseveraldimensions toone;thiskindof
simpli¯cation andgeneralization doesofcoursehaveitsmerits,butmayalsobeconfusing.
Regarding thetaxonom yoftechnologies usedinthisclassi¯cation, itappearsthatthe
closestcorrespondingdimensions inourtypologyisthedi®erentkindsofinformation states
anddialogue movesusedforvariousdialogue types,dialogue phenomena, andactivities.
However,theclassi¯cations arealsoquitedi®erent;foronething,the¯nite-state-based
andform-based techniques usuallydonotevenusedialogue moves.Bycontrast,our
classi¯cation reliesonspecifyingdialogue movesevenforverysimpledialogues. Wewill
notgointoadiscussion oftherelativemeritsofthesegroundsofclassi¯cation; su±cetosay
thatatheory-dep endentclassi¯cation (whichourstosomeextentis)allowsagreaterlevel
ofdetailintheclassi¯cation, butitsusefulness isofcoursedependentontheacceptance
ofthebasictheoretical assumptions thataremade.
The¯rsttwotechnologies listedbyAllenet.al.werediscussed inChapter 1,andthe
distinction betweenthemareprettymuchstandard. However,theclassi¯cation ofthe
remaining threetechnologies ismoreproblematic.
Regarding the\setsofcontexts"technology,furtherspeci¯edastheuseofseveralforms,
itcanberegarded asambiguousbetweentheuseofseveralformsofthesametypeand
theuseofseveralformsofdi®erenttypes.Theexample taskprovidedis\travelbooking
agent",ormorespeci¯cally,itinerary booking.Thisseemstoindicate thattheintended
meaning of\setsofcontexts"istheuseofseveralformsofthesametype(e.g.oneforeach
legoftheitinerary). Inourtypologyofactivities inTable6.3,thiswouldcorrespondtoa
dialogue withacomplex result.However,theuseofseveralformsofdi®erenttypesseems
rathertothepossibilityofseveralsimultaneous tasks(e.g.askingaboutwhichchannelis
onwhileprogramming theVCR).

6.4.DIALOGUE STRUCTURE 241
Thelevelofplan-based technology isfurtherspeci¯edas\interactivelyconstructing a
planwiththeuser"(Allenetal.,2001,p.30).Thisspeci¯cation thussayssomething
abouttheresultofthedialogue (aplan)andhowthisresultisconstructed (interactively).
Notethatthisisnotexactlywhatwereferredtoastheplan-based approachinChapter
1;atleastinprinciple (andperhapsalsoinpractice; thisisanempirical issuerelatedto
DahlbÄack'sconceptofdialogue-task distance) itappearstobepossibleforadialogue system
toengageinthiskindofdialogue evenifthesystemitselfdoesnotusecomplex planning
andplanrecognition (e.g.fordialogue actrecognition). Relating thistoourclassi¯cation
ofactivities, itappearsthattheplan-based levelcorrespondsroughlytodialogues with
complex results(plans)anddistributed decision rights(interactivit y).Asisindicated by
Table6.3,thetechniquesneededtohandlethe\plan-based" levelwouldalsobeneeded
fore.g.explanatory andtutorialdialogue.
Finally,regarding thelevelofagent-basedtechnology,furtherspeci¯edaspossiblyinvolving
execution andmonitoring ofoperations inadynamically changing world,itappearsthat
themaindi®erence totheplan-based modeliswhatwerefertoas(pro)activ enessofthe
external process.
Toconclude, itappearsfromthepointofviewofourtypologythattheclassi¯cation by
Allenetal.(2001)isbasedonamixofcriteria, including information statecomponents
(e.g.forms)butalsoactivitytype,resulttype,pro-activ enessofexternal process,decision
rights,anddialogue features suchasgrounding (\simple clari¯cations") andnegotiation
(\collaborativenegotiation subdialogues"). TheAOD/IOD distinction appearsnottobe
included atall.
6.4Dialoguestructure
Inthissectionwediscusstheimplications ofissue-based dialogue managemen tonthe
structure ofdialogue. Wediscussthedialogue modelofGroszandSidner(1986),elaborated
inGroszandSidner(1987),andrelateittotheissue-based model.Theauthorspresenta
theoryofdiscourse structure basedonthreestructural components:
²linguistic structure: utterances, phrases, clausesetc.
²intentionalstructure: intentions,relatedbydominance andsatisfaction-precedence
²attentionalstate:salientobjects,properties,relations anddiscourse intentions
Theintentionalstructure isrelatedtodialogue structure throughDiscourseSegmentPur-
poses(DSPs).Adialogue canbedividedintosegmentswhereeachsegmentisengaged

242 CHAPTER 6.CONCLUSIONS AND FUTURE RESEAR CH
inforthepurposeofsatisfying aparticular intention,designated astheDSPofthatseg-
ment.Thisrelationisusedtoexplaintheclosecorrespondence betweentaskstructure and
dialogue structure observedincollaborativeplanning dialogue. Withregardtodialogue
managemen t,itisclaimedthat\aconversational participan tneedstorecognize theDSPs
andthedominance relationships betweentheminordertoprocesssubsequen tutterances
ofthediscourse" (GroszandSidner,1987,p.418).Theauthorsalsosketchaprocess
modelbasedontheconceptofaSharedPlan,formalized intermsofindividual intentions
andmutualbeliefs.
Therearesomeinteresting butroughcorrespondences betweenthismodelandtheissue-
basedmodel,andthelattercanperhapsbeseen(atleasttosomeextent)asanalternativ e
(orcomplemen t)totheSharedPlans formalization.
Thesimplest correspondence isthatbetweenthelinguistic structure andthelu¯eld(and
perhapsalsotheinputvariable)intheissue-based model,although ourmodeloflinguistic
structure isextremely impoverished.
Intheissue-based model,DSPsroughlycorrespondtotheissuesand(inAOD)actions
¯elds,andshouldthusbeusefulforsegmentingdialogue inamannersimilartoGroszand
Sidner's. Sequencing ICM,which(amongotherthings)re°ectchangesinissuescanthus
beregarded asindicating dialogue segmentshifts.
Thelocalfocusofattentionispartially modelledbyQUD,although sofarourattentional
modellackse.g.arepresentationof\objectsunderdiscussion". Discourse intentionsseem
tocorrespondroughlytotheagenda¯eld,andpossiblyalsotheplan¯eldalthough the
latterismoreglobalinnature. Ofcourse,ourrepresentationofdialogue plansisquite
di®erentfromthatofGroszandSidner,whouseamodallogicwithoperatorsforintentions.
Itshouldbenotedthattheintentionalstructure, modelledasSharedPlans, ispartofthe
sharedknowledge. GroszandSidnerareprimarily interested indialogues aimedatthe
collaborativecreation andexecution oftheseSharedPlans, whichmeansthattheirmodel
doesnottriviallyextendtootherkindsofdialogue, e.g.simpleinquiry-orien teddialogue or
tutorialdialogue. Forthekindsofdialogue wehavedealtwithsofar,thekindofcomplex
representationsneededformodellingSharedPlans appearnottobeneeded. Theclosest
correspondence toSharedPlans inourmodelistheactions¯eldwhichcontainsdomain
actionstobeperformed byoneoftheDPs.Itcanbeexpectedthatwhentheissue-based
modelisextended tohandlecollaborativeplanning dialogue, thestructure oftheactions
¯eldwillbecomemorecomplex andmoresimilartoSharedPlans.

6.5.FUTURE RESEAR CHAREAS 243
6.5Futureresearchareas
Inthissection,webrie°ymentionsomefutureareasforresearchusingtheissue-based
approachtodialogue managemen t.Wealsomentionsomedesirable improvementsto
IBiS.
6.5.1Developingtheissue-based approachtogrounding
Representationofutterances Starting fromGinzburg's grounding protocols,wehave
formalized andimplemen tedabasicversionofissue-based grounding andfeedback.How-
ever,someaspectsofthecurrentsolution arenotcompletely satisfactory ,anditappears
thatabettersolution couldbeobtained byexplicitly representingutterances invarious
stagesofgrounding toalargerextentthaninthecurrentsystem.
Grounding issues Also,toincrease thecoverageofthetheoryandtheabilities ofthe
systemitwouldbeusefultorepresentgrounding issuesexplicitly onseverallevelsofground-
ingtoalargerextentthaniscurrentlydone.Someofthepossiblegrounding issuesthat
couldberepresentedarethefollowing(Sisthespeaker,Aistheaddressee, uisanutterance
byS).
²Contactlevel
{SandA:DoIhavecontactwithotherDP?
²Perception level
{S:DidAperceiveucorrectly? Ifnot,whatdidAperceive?
{A:WhatdidSsay?DidSsayX?WhichofX1;:::;XndidSsay?
{SandA:Isugrounded ontheperception level?
²Semanticunderstanding level
{S:DidAunderstand theliteralmeaning ofu?Ifnot,whatdoesAthinkI
meant(literally)?
{A:Whatdoesumean(literally)? DoesumeanX?WhichofX1;:::;Xndoes
umean?
{SandA:Isugrounded onthesemanticunderstanding level?
²Pragmatic understanding level

244 CHAPTER 6.CONCLUSIONS AND FUTURE RESEAR CH
{S:DidAunderstand thepragmatic meaning ofu?Ifnot,whatdoesAthinkI
meant(pragmatically)?
{A:WhatdidSmeanbyumean,giventhecurrentcontext?Howisurelevant
inthecurrentcontext?DidSmeanX?WhichofX1;:::;XndidSmean?
{SandA:Isugrounded onthepragmatic understanding level?
²Reaction level
{S:WillAaccept(thecontentof)u?
{A:ShouldIaccept(thecontentof)u?Ifuisanassertion, shouldIacceptu
asafactoronlyasatopicfordiscussion? IfIdon'tacceptu,howshouldI
indicate this?ShouldIacceptanalteredversionofu?ShouldIacceptonlya
partofu?
Increased coverageOuraccountofgrounding andICMissofaronlypartialincover-
age;phenomena thatremaintobeaccountedforand/orimplemen tedincludeclari¯cation
ellipsis,semanticambiguityresolution, collaborativecompletions andrepair,andturntak-
ingICM.Whilewehaveincluded somerudimentarysequencing ICM,furtherinvestigations
oftheappropriateness andusefulness oftheseutterances areneeded;here,researchondis-
coursemarkers(e.g.Schi®rin,1987)andcuephrases(e.g.GroszandSidner,1986,Polanyi
andScha,1983,andReichman-Adar, 1984)canbeofgreatuse.Wealsowanttoexplore
turntakinginasynchronousdialogue managemen t,andhowthisrelatestoturntakingICM.
OwnCommunication Managemen thassofarnotbeenhandled atall,andthisisclearly
anareawherethesystemcouldbeimprovedbothontheinterpretation andgeneration
side.Wehopethattheissue-based approachcouldhelpclarifytherelationbetweenICM
andOCMaspectsofgrounding-related utterances.
Methodsforchoosinggrounding andICMstrategies Wehaveusedaverybasic
methodforchoosinggrounding andICMstrategies; thiscouldbedevelopedtoinclude
context-related aspectsoftheutterance tobegrounded. Thisalsogoesforthestrategies
forchoosingbetweenseveralcompetinginterpretation hypothesesontheperception and
understanding levels.
Implicitissues Webelievethatthemodellingofimplicitissues,bothgrounding-related
andothers,canbeveryusefulforaccountingfortherelevanceofmanyutterances. We
therefore needtodevelopageneralwayofdealingwithimplicitquestions andtheaccom-
modationofthese.Webelievethatsuchanaccountshouldbebasedondynamic generation
andaccommo dationofimplicitissueswhentheyareneeded,ratherthancalculating all
possibleimplicitissuesavailableatanystageofthedialogue.

6.5.FUTURE RESEAR CHAREAS 245
6.5.2Otherdialogue andactivitytypes
Ofcourse,anobviouscontinuationoftheworkpresentedhereistocontinueextending the
coverageofissue-based dialogue managemen ttootherkindsofdialogues. Inthissection
wewilldiscusssomepossibilities.
Pro-activedevices Tohandledialogue withpro-activ edevices, itisnotsu±cientto
modelthedeviceonlyasaresource, sincethelatterarebyde¯nition passive.Whatis
neededisamodulewhichisconnected totheactivedevice;wecancallsuchamodulean
actionmanager.Dialogue withpro-activ edeviceswillalsorequireasynchronous dialogue
processing,atleastonsomelevel.Thesimplest solution istocheckformessages fromthe
devicewhenthesystemhastheturn.Tohandlethis,itisprobably su±cienttohavethe
wholesystemexcepttheactionmanager runningasasingleprocess.However,itmayalso
benecessary forthesystemtointerrupttheuser(orindeeditself)inmid-turn, togivea
reportonthestateofsomeactionorplanbeingexecuted. Thisislikelytorequireamore
advancedasynchronous setup,whereseveralprocessesareneeded.
Complex results Wehavesofaronlybeendealingwithdialogues wherethe\result"
(answer,action)isnotverycomplex. Ine.g.itinerary information dialogue, theresultmay
beamorecomplex structure. Incollaborativeplanning dialogue theresultisapotentially
complex planwithseveralactionsrelatedinvariousways.Similarly ,explanatory dialogue
mayrequirerepresentationofcomplex explanations orproofs.Todealwithdialogue with
complex results,weneedtobeabletorepresentthesecomplex structures, andperhaps
alsotoincremen tallyconstruct thembysuccessiv eadditions andmodi¯cations. However,
webelievethattheessentialfeatures ofinquiry-orien ted,action-orien ted,andnegotiativ e
dialogue arethesameregardless ofwhether theresultsarecomplex orsimple.
Argumentation Tohandleargumen tation,whichismostlikelytoappearinnegotiativ e
dialogue, wehopetobeabletoexploitprevious workinthisarea,e.g.MannandThompson
(1983)andAsherandLascarides (1998),andrelateittotheissue-based approach.
Useofobligations TraumandAllen(1994)proposeobligations asacentralsocial
attitude drivingdialogue. Forexample, ifDPAasksaquestion QtoDPB,Bwillhave
anobligation toaddress Q;typically,thisobligation willthengiverisetoanintentionto
address Q.InIBiS,weinsteadaddQtoQUD(globalandlocal),andifthesystemcan
answeraquestion onQUDitwilldoso.Ithasbeennotedthatthejobdonebyobligations
andQUDoverlaptoalargeextent(Kreutel andMatheson, 1999),andinmanykinds

246 CHAPTER 6.CONCLUSIONS AND FUTURE RESEAR CH
ofdialogue thechoicebetweenQUDandobligations willnotresultinanydi®erences in
behaviour.However,therearealsodi®erences betweenQUDandobligations.
Foronething,QUDdoesnotrepresentwhoraisedthequestion, orwhoshouldrespond
toit.Aninteresting question thenbecomes: giventhatweincludeaglobalQUDinour
information state,whendoesitbecomenecessary toalsoincludeobligations? Itappears
thatonetypeofdialogue whereQUDonitsownisinsu±cien tistutorialdialogue, where
thetutorasksthestudentaso-called \examquestion" towhichthetutoralreadyknows
thecorrectanswer.Giventhestrategy usedbyIBiS,thesystemwouldraisethequestion
andthenimmediately answerit,whichisprobably notaverygoodteachingstrategy.
However,inmanyotherkindsofdialogues itappearsthatthestrategy ofansweringa
question regardless ofwhoanswereditisausefulstrategy.Forexample, ifaDPA(a
humanorperhapsarobotequippedwithvision)asksanotherDPBwheresomeobjectis
locatedandthen¯ndstheobject,itappearsmorefelicitous forAtoanswerthequestion
(\Ah,thereitis!")thantowaitforBtodoso.Moreimportantly,wehaveinthepreceding
chaptersdemonstrated severalusesofaglobalQUD(modellinggrounding issues,handling
issueaccommo dation,representingissuesundernegotiation) whichitmayormaynot
bepossibletohandleusingobligations. Forthesereasons, weareinterested infurther
exploring thesimilarities, di®erences, andinteraction betweenQUDandobligations, and
possiblyextendtheissue-based dialogue modelbyaddingobligations, atleastformodelling
somecomplex kindsofdialogue.
Generalplanning Asimilarcaseappliestogeneralized planning. Wehavesofaronly
usedpre-scripted dialogue planswhichareusedina°exiblewaybythedialogue manager to
enablesomedegreeofrudimentaryreplanning, butitcanbeexpectedthatforsu±ciently
complex dialogues thenumberofdialogue plansthatareneededwillbecomesolargethat
pre-scripting isnolongerfeasible. Atthispoint,dynamic planning willbeneeded.Weare
interested in¯ndingoutforwhichkindsofdialogues dynamic general-purp oseplanning
isneeded,andinintegrating dynamic planning intheissue-based approachtodialogue
managemen t.
6.5.3Semantics
ThesemanticscurrentlyusedinIBiSisobviouslyverysimple,andintegrating theissue-
basedapproachtodialogue managemen twithamorepowerfulsemanticsislikelytoim-
proveboththetheoretical depthofanalysis, especiallyregarding thesemanticsofquestions,
andtheperformance ofthesystem.Arelevantissueinthiscontextistheconnection be-
tweendialogue featuresandrequiremen tsonthesemanticrepresentationused-whendoes
morecomplex semanticsbecomenecessary?

6.5.FUTURE RESEAR CHAREAS 247
Speci¯cally,wewouldliketoexploreandimplemen tsemanticsusingdependentrecord
types(Cooper,1998),andintegratethiswithissue-based dialogue managemen t.One
reasonforthisisthatdependentrecordtypesappearstoprovideacomputationally sound
frameworkforimplemen tingideasfromsituation semantics;thelatterhasbeenusedby
Ginzburg informulatingthesemanticsofquestions onwhichtheissue-based approachto
dialogue managemen tisbased.
Itshouldbenotedthatthesystemitselfisindependentofwhichsemanticsisused;this
isratherafeatureofthedomain-sp eci¯cresources and(tosomeextent)theresource
interfaces. Addingamorepowerfulsemanticswilltherefore notrequireanysigni¯can t
modi¯cations ofupdaterulesetc.
6.5.4General inference
Whileupdaterulescanberegarded asspecialized (forward-chaining) inference rules,we
havesofarnotdealtwithgeneralinference andbackward-chaininginference. Inference
couldbeusefulevenindatabase searchdialogue toreasonaboutthebestwayofdealing
withsearchresultsintheformofconditionals (seeSection2.12.4). Oneideahereisto
introduceaprivateissue-structure representingquestions thatthesystemisinterested in
resolving; thiscouldberegarded asmodellingthe\wonder"attitude. A¯ndout( Q)action
ontheagendacouldthenresultinQbeingaddedtoa¯eld/private/wonder,whichcan
eitherleadtoadatabase search,backward-chainingreasoning fromavailableinformation,
oraskingtheuserforananswer.Asanexample ofbackward-chainingreasoning usingthe
\wonder"attitude, ifthesystembelievesp!randwondersabout?r,arulecouldadd?p
tothewonder¯eld;thisrulewouldthenimplemen tbackward-chainingmodusponens.
6.5.5Naturallanguage inputandoutput
Parsingandgeneration InIBiSwehavesofarconcentratedondialogue managemen t
andusedveryrudimentarymodulesforinterpretation andgeneration ofnaturallanguage.
Weneedtoexplorethepossibleuseofrobustparsingtechniques(seee.g.Milward,2000)
and\real"grammars. Itwouldalsobeusefultobeabletoautomatically generate speech
recognition grammars (whichareusually¯nite-state) fromtheparsinggrammar. Using
thesamegrammar forparsingandgeneration wouldfurtherdecrease theamountofwork
neededforportingthesystemtoanewdomainorlanguage.
Dialoguemoveinterpretation Sincewehavebeendealingwithsimpledialogue intoy
domains, wehavesofarbeenabletogetawaywithdoingdialogue moveinterpretation

248 CHAPTER 6.CONCLUSIONS AND FUTURE RESEAR CH
independentlyofthedynamic context.Instead, contextdependentinterpretation isper-
formedbythedialogue moveengineasasubtaskofintegrating moves.Whilewebelieve
thatthisisagoodstrategy touseaslongasitworkswell,itmayeventuallybecomenec-
essarytobeabletorecognize indirectspeechacts(inourcase,indirectdialogue moves),
whichprobably requires someformofcontext-dependentintentionrecognition todecide
whatmovehasbeenperformed.
Focusintonation Oneareaofresearchthatwehavenotmentionedsofar,butwhere
theissue-based approachshowsgreatpromise, isthegeneration andinterpretation of
focusintonation withrespecttotheinformation state.Someworkwasdoneonthisinthe
TRINDI project(Engdahl etal.,1999),andiscurrentlybeingdevelopedfurtherinthe
followupSIRIDUS project.
Speechrecognition for°exibledialogue Oneproblem foranydialogue systemallow-
ingforuserinitiativeand°exibilityisthatalargerspeechrecognition lexiconisneeded,
whichnegativelya®ectsthequalityofspeechrecognition. Wewanttoexploretheuseof
theinformation state,andespeciallyQUD,forimprovingrecognition, e.g.byrunning a
\global" recognizer listening foranythingthatthesystemcanunderstand, anda\local"
recognizer, listening e.g.foranswerstoquestions onQUD,inparallel.
6.5.6Applications andevaluation
Toproperlytesttheissue-based approachtodialogue managemen t,webelieveitisnec-
essarytobuildfull-scale prototypeapplications andevaluatethesebasedoninteractions
withnaiveusers.Onepossiblesuchapplication isVCRcontrol;another islocaltravel
information.
Although wehavenotsaidmuchaboutithere,wehavepreviously explored variouswaysof
acquiring dialogue plansappropriate foragivendomainorapplication. Amongtheoptions
wehaveusedisdialogue distillation (seeLarssonetal.,2000b),conversionofdomainplans
todialogue plans(seeLarsson, 2000),andconversionofmenuinterfacestodialogue plans.
AfurtheroptionwewanttoexploreistheuseofVoiceXML (McGlashan etal.,2001)
dialogue speci¯cations asabasisfordialogue plans.Wehopetobeabletoautomatically
orsemi-automatically convertVoiceXML scriptsintocomplete domainandlexiconspec-
i¯cations forIBiS,whichwehopewouldallowtheuseofgeneraldialogue mechanisms
(e.g.grounding, accommo dation,negotiation) toenable°exibledialogue givenfairlysim-
pleVoiceXML scripts.Thiswoulddecrease theamountofworkonthepartofthedialogue

6.6.CONCLUSION 249
designer, andthusenablerapidprototyping.
6.6Conclusion
Theissue-based approachtodialogue managemen thasproventobeveryusefulforformu-
latinggeneralandtheoretically motivatedaccountsofimportantaspectsofdialogue, such
asinquiry-orien teddialogue interactions, dealingwithmultiplesimultaneous tasks,sharing
information betweentasks,grounding, interactivecommunication managemen t,question
accommo dation,simplebeliefrevision, action-orien teddialogue, andsimplenegotiativ e
dialogue. Themodelcanbeimplemen tedratherstraightforwardlyusingtheTrindiKit ,
whichhasproventobeaveryusefultoolforexploring theissue-based approach.Some
aspectsoftheaccountaspresentedherecanbeimprovedon,e.g.byproperlydividing the
tasksofutterance understanding andintegration intoseparate rules,andimprovingthe
treatmen tofsemantics.
Toreallyshowthattheissue-based approachisaviablealternativ etomorecomplex
approachessuchastheplan-based approachasusede.g.intheTRIPSsystem(Allenet
al.(2001)), weneedtoextendthecoverageoftheissue-based accounttoincludemore
complex typesofdialogue, involvinge.g.collaborativeplanning andreal-time monitoring
ofadynamic environmen t.Webelievethisisfeasible, andanexcitingfutureresearcharea.
ThemodularityoftheIBiSsystemenablesrapidprototypingofsimpleexperimentalap-
plications. Webelievethatitwillbepossibletoscaleupthemethodspresentedhereto
morerealisticapplications whichcanbeevaluatedonnaivesubjects.

250 CHAPTER 6.CONCLUSIONS AND FUTURE RESEAR CH

Bibliograph y
Alexandersson, JanandBecker,Tilman2000.Overlayasthebasicoperationfordiscourse
processinginamultimodaldialogue system. InProceedingsoftheIJCAIWorkshop on
KnowledgeandReasoninginPracticalDialogueSystems.8{14.
Allen,J.F.andPerrault,C.1980.Analyzing intentioninutterances. Arti¯cialIntelligence
15(3):143{178.
Allen,JamesF.;Byron,DonnaK.;Dzikovska,Myroslava;Ferguson, George; Galescu,
Lucian;andStent,Amanda 2001.Towardconversational human-computer interaction.
AIMagazine 22(4):27{37.
Allen,J.F.1987.NaturalLanguage Understanding .Benjamin Cummings, MenloPark,
CA.
Allwood,Jens;Nivre,Joakim; andAhlsen,Elisabeth1992.Onthesemanticsandprag-
maticsoflinguistic feedback.JournalofSemantics 9:1{26.
Allwood,Jens1995.Anactivitybasedapproachtopragmatics. TechnicalReport(GPTL)
75,GothenburgPapersinTheoretical Linguistics, UniversityofGÄoteborg.
Asher,N.andLascarides, A.1998.Thesemanticsandpragmatics ofpresupposition.
JournalofSemantics 15(3):239{299.
Aust,H.;Oerder,M.;Seide,F.;andSteinbiss,V.1994.ExperiencewiththePhilips
automatic traintableinformation system. InProc.ofthe2ndWorkshop onInteractive
VoiceTechnologyforTelecommunic ationsApplications(IVTTA),Kyoto,Japan.67{72.
Barwise, J.andPerry,J.1983.Situations andAttitudes.TheMITPress.
Berman, Alexander 2001.Asynchronous feedbackandturn-taking. ms.
Bohlin,Peter;Bos,Johan;Larsson, Sta®an;Lewin,Ian;Matheson, Colin;andMilward,
David1999.Surveyofexistinginteractivesystems. TechnicalReportDeliverableD1.3,
Trindi.
251

252 BIBLIOGRAPHY
Bos,JohanandGabsdil, Malte2000.First-order inference andtheinterpretation of
questions andanswers.InPoesioandTraum2000.
Boye,J.;Larsson, S.;Lewin,I;Matheson, C.;Thomas, J.;andBos,J.2001.Standards in
homeautomation andlanguage processing.TechnicalReportDeliverableD1.1,D'Homme.
BÄauerle,Rainer;Reyle,Uwe;andZimmermann, Thomas Ede,editors2002.Presupposi-
tionsandDiscourse.CurrentResearchintheSemantics/Pragmatics Interface.Amster-
dam(Elsevier).
Carberry,S.1990.PlanRecognitioninNaturalLanguage Dialogue.TheMITPress,
Cambridge,MA.
Chu-Carroll, Jennifer 2000.Mimic:Anadaptivemixedinitiativespokendialogue system
forinformation queries.InProceedingsofthe6thConferenceonAppliedNaturalLanguage
Processing.97{104.
Clark,H.H.andSchaefer,E.F.1989a.Contributing todiscourse. CognitiveScience
13:259{94.
Clark,HerbertH.andSchaefer,EdwardF.1989b.Contributing todiscourse. Cognitive
Science13:259{294. AlsoappearsasChapter 5inClark(1992).
Clark,HerbertH.1992.ArenasofLanguage Use.UniversityofChicago Press.
Clark,H.H.1996.UsingLanguage.CambridgeUniversityPress,Cambridge.
Cohen,P.andLevesque,H.1990.Intentionischoicewithcommitmen t.Arti¯cialIntel-
ligence42:213{261.
Cohen,P.1981.Theneedforreferentidenti¯cation asaplanned action.InProceedings
ofthe7thInternational JointConferenceofArti¯cialIntelligence,Toronto.31{36.
Cooper,RobinandGinzburg, Jonathan 2001.Resolving ellipsisinclari¯cation. InPro-
ceedingsofthe39thmeetingoftheAssocationforComputational Linguistics, Toulouse.
236{243.
Cooper,RobinandLarsson, Sta®an2002.Accommo dationandreaccommo dationin
dialogue. InBÄauerleetal.2002.
Cooper,Robin;Engdahl, Elisabet;Larsson, Sta®an; andEricsson, Stina2000.Accom-
modatingquestions andthenatureofqud.InPoesioandTraum2000.57{61.
Cooper,Robin; Ericsson, Stina;Larsson, Sta®an; andLewin,Ian2001. An
information stateupdateapproachtocollaborativenegotiation. InKÄuhnlein,
Peter;Rieser, Hannes; andZeevat,Henk,editors 2001,BI-DIALOG 2001|
Proceedingsofthe5thWorkshop onFormalSemantics andPragmatics ofDialogue,
http://www.uni-bielefeld.de/BIDIALOG .ZiF,Univ.Bielefeld. 270{9.

BIBLIOGRAPHY 253
Cooper,R.1998.Information states,attitudes anddependentrecordtypes.InProceedings
ofITALLC-98 .
Core,MarkG.andAllen,JamesF.1997.Codingdialogues withtheDAMSLanno-
tationscheme.InTraum,David,editor1997,Working Notes:AAAIFallSymposium
onCommunic ativeActioninHumans andMachines ,MenloPark,California. American
AssociationforArti¯cial Intelligence. 28{35.
DahlbÄack,Nils1997.Towardsadialogue taxonom y.InMaier,Elisabeth;Mast,Mar-
ion;andLuperFoy,Susann, editors1997,DialogueProcessinginSpokenLanguage Sys-
tems,number1236inSpringer VerlagSeriesLNAI-Lecture NotesinArti¯cial Intelligence.
Springer Verlag.
DiEugenio, B.;Jordan,P.W.;Thomason, R.H.;andMoore,J.D.1998.Anempirical
investigation ofproposalsincollaborativedialogues. InProceedingsofACL{COLING 98:
36thAnnualMeetingoftheAssociationofComputational Linguistics and17thInterna-
tionalConferenceonComputational Linguistics .325{329.
TheDISCconsortium, 1999.Discdialogue engineering model.Technicalreport,DISC,
http://www.disc2.dk/slds/.
Engdahl, Elisabet;Larsson, Sta®an;andBos,Johan1999.Focus-ground articulation and
parallelism inadynamic modelofdialogue. TechnicalReportDeliverableD4.1,Trindi.
Fikes,R.E.andNilsson, N.J.1971.STRIPS: Anewapproachtotheapplication of
theorem provingtoproblem solving.Arti¯cialIntelligence2:189{208.
GÄardenfors, P.1988.KnowledgeinFlux:ModelingtheDynamic ofEpistemic States.The
MITPress,Cambridge,MA.
Ginzburg, J.1994.Anupdatesemanticsfordialogue. Inal,H.Buntet,editor1994,
ProceedingsoftheInternational Workshop onComputational Semantics .ITK.Tilburg.
111{120.
Ginzburg, J.1996.Interrogativ es:Questions, factsanddialogue. InTheHandbookof
Contemp orarySemantic Theory.Blackwell,Oxford.
Ginzburg, J.1997.Structural mismatchindialogue. InJaeger,G.andBenz,A,edi-
tors1997,ProceedingsofMunDial 97,TechnicalReport97-106.UniversitaetMuenchen
CentrumfuerInformations- undSprachverarbeitung,Muenchen.59{80.
Ginzburg, J.forth.Questions andthesemanticsofdialogue. Forthcoming book,partly
availablefromhttp://www.dcs.kcl.ac.uk/staff/ginzburg/papers.html .
Go®man, E.1976.Repliesandresponses.Language inSociety5:257{313.

254 BIBLIOGRAPHY
Grosz,B.J.andSidner,C.L.1986.Attention,intention,andthestructure ofdiscourse.
Computational Linguistics 12(3):175{204.
Grosz,B.J.andSidner,C.L.1987.Plansfordiscourse. InSymposiumonIntentions
andPlansinCommunic ationandDiscourse.
Grosz,B.J.andSidner,C.L.1990.Plansfordiscourse. InCohen,P.R.;Morgan, J.;and
Pollack,M.E.,editors1990,Intentions inCommunic ation.TheMITPress,Cambridge,
MA.chapter20,417{444.
Hulstijn, J.2000.DialogueModelsforInquiryandTransaction .Ph.D.Dissertation,
UniversityofTwente.
Jennings, N.andLesperance,Y,editors2000.Proceedingsofthe6thInternational Work-
shoponAgentTheories,Architectures,andLanguages (ATAL'1999) ,Springer Lecture
NotesinAI1757.Springer Verlag,Berlin.
Kaplan,D.1979.Dthat.InCole,P.,editor1979,SyntaxandSemantics v.9,Pragmatics .
Academic Press,NewYork.221{243.
Kreutel, JornandMatheson, Colin1999.Modellingquestions andassertions indialogue
usingobligations. InVanKuppeveltetal.1999.
vanKuppevelt,Jan;vanLeusen,Noor;vanRooy,Robert;andZeevat,Henk,editors1999.
ProceedingsofAmstelogue'99Workshop ontheSemantics andPragmatics ofDialogue.
Larsson, Sta®anandTraum,David2000.Information stateanddialogue managemen tin
thetrindidialogue moveenginetoolkit.NLESpecialIssueonBestPracticeinSpoken
Language DialogueSystems Engineering323{340.
Larsson, Sta®anandZaenen, Annie2000.Documenttransformations andinformation
states.InProceedingofthe1stSigDialWorkshop, HongKong.ACL.112{120.
Larsson, Sta®an;LjunglÄof,Peter;Cooper,Robin;Engdahl, Elisabet;andEricsson, Stina
2000a.Godis-anaccommo datingdialogue system. InProceedingsofANLP/NAA CL-
2000Workshop onConversational System.
Larsson, Sta®an; Santamarta, Lena;andJÄonsson,Arne2000b.Usingtheprocessof
distilling dialogues tounderstand dialogue systems. InProceedingsof6thInternational
ConferenceonSpokenLanguage Processing(ICSLP2000/INTERSPEECH2000), Volume
III.374{377.
Larsson, Sta®an1998.Questions underdiscussion anddialogue moves.InProceedingsof
theTwenteWorkshop onLanguage Technology.163{171.
Larsson, Sta®an2000.Frommanualtexttoinstructional dialogue: aninformation state
approach.InPoesioandTraum2000.203{206.

BIBLIOGRAPHY 255
Lewin,Ian;Cooper,Robin;Ericsson, Stina;andRupp,C.J.2000.Dialogue movesin
negotiativ edialogues. Projectdeliverable1.2,SIRIDUS.
Lewin,I.;Larsson, S.;Ericsson, S.;andThomas, J.2001.Thed'homme deviceselection.
TechnicalReportDeliverableD5.1,D'Homme.
Lewis,D.K.1979.Scorekeepinginalanguage game.JournalofPhilosophic alLogic
8:339{359.
LjunglÄof,Peter2000.Formalizing thedialogue moveengine.InProceedingsofGÄotalog
2000workshop onsemantics andpragmatics ofdialogue.207{210.
Mann,W.C.andThompson, S.A.1983.Relational propositionsindiscourse. Technical
ReportISI/RR-83-115, USC,Information Sciences Institute.
McGlashan, S.;Burnett, D;Danielsen, P.;Ferrans,J.;Hunt,A.;Karam,G;Ladd,D.;
Lucas,B.;Porter,B.;andRehor,K.2001.Voiceextensible markuplanguage (voicexml)
version2.0.Technicalreport,W3C.W3CWorkingDraft,23October2001.
Microsoft, 2000.Universal PlugandPlayDeviceArchitectureVersion1.0.URL:
http://www.upnp.org/do wnload/UPnPD A1020000613.h tm.
Milward,D.2000.Distributing representationforrobustinterpretation ofdialogue ut-
terances. InProceedingsofthe38thAnnualMeetingoftheAssociationofComputational
Linguistics, ACL-2000.133{141.
Moore,Johanna D.1994.ParticipatinginExplanatory Dialogues:Interpretingand
RespondingtoQuestions inContext.Acl-MitPressSeriesinNaturalLanguage Processing.
MITPress.
Poesio,Massimo andTraum,DavidR.1998.Towardsanaxiomatization ofdialogue acts.
InProceedingsofTwendial'98, 13thTwenteWorkshop onLanguage Technology:Formal
Semantics andPragmatics ofDialogue.207{222.
Poesio,Massimo andTraum,David,editors2000.ProceedingsofGÄotalog2000,number
00-5inGPCL(GothenburgPapersComputational Linguistics).
Polanyi,L.andScha,R.1983.Ontherecursivestructure ofdiscourse. InEhlich,K.and
Riemsdijk, H.van,editors1983,ConnectednessinSentence,DiscourseandText.Tilburg
University.141{178.
Rao,A.S.andGeorge®, M.P.1991.Modelingrationalagentswithinabdi-architecture. In
Allen,James;Fikes,Richard;andSandewall,Eric,editors1991,ProceedingsoftheSecond
International ConferenceonPrinciples ofKnowledgeRepresentation andReasoning(KR-
91),Cambridge,MA.473{484.

256 BIBLIOGRAPHY
Reichman-Adar, R.1984.Extended man-mac hineinterface. Arti¯cialIntelligence
22(2):157{218.
Sadek,M.D.1991.Dialogue actsarerational plans.InProceedingsoftheESCA/ETR
workshop onmulti-mo daldialogue.1{29.
vanderSandt,R.A.1992.Presuppositionprojectionasanaphora resolution. Journalof
Semantics 9(4):333{377.
San-Segundo, Ruben;Montero,JuanM.;Guitierrez, JuanaM.;Gallardo, Ascension;
Romeral, JoseD.;andPardo,JoseM.2001.Atelephone-based railwayinformation system
forspanish: Developmentofamethodologyforspokendialogue design.InProceedingsof
the2ndSIGdialWorkshop onDiscourseandDialogue.140{148.
Schi®rin,D.1987.DiscourseMarkers.CambridgeUniversityPress,Cambridge.
SeverinsonEklundh, Kerstin1983.Thenotionoflanguage game{anaturalunitof
dialogue anddiscourse. TechnicalReportSIC5,UniversityofLinkÄoping,Studiesin
Communication.
Sidner,Candace L.andIsrael,DavidJ.1981.Recognizing intendedmeaning andspeak-
ers'plans.InProceedingsoftheSeventhInternational JointConferenceonArti¯cial
Intelligence,Vancouver,BritishColumbia.International JointCommittee onArti¯cial
Intelligence. 203{208.
Sidner,Candace L.1994a.Anarti¯cial discourse language forcollaborativenegotiation.
InProceedingsoftheforteenthNational ConferenceoftheAmericanAssociationforAr-
ti¯cialIntelligence(AAAI-94) .814{819.
Sidner,Candace. L.1994b.Negotiation incollaborativeactivity:Adiscourse analysis.
Knowledge-BasedSystems 7(4):265{267.
Stalnaker,R.1979.Assertion. InCole,P.,editor1979,SyntaxandSemantics ,volume9.
Academic Press.315{332.
StenstrÄom,Anna-Brita 1984.Questions andResponses.LundStudiesinEnglish: Number
68.Lund:CWKGleerup.
Sutton,S.andKayser,E.1996.Thecslurapidprototyper:Version1.8.Technicalreport,
OregonGraduate Institute, CSLU.
Traum,D.R.andAllen,J.F.1994.Discourse obligations indialogue processing. In
Proc.ofthe32ndAnnualMeetingoftheAssociationforComputational Linguistics ,New
Mexico. 1{8.
Traum,D.R.andHinkelman,E.A.1992.Conversation actsintask-orien tedspoken
dialogue. Computational Intelligence8(3):575{599. SpecialIssueonNon-literal Language.

BIBLIOGRAPHY 257
Traum,D.R.1994.AComputational TheoryofGroundinginNaturalLanguageConver-
sation.Ph.D.Dissertation, UniversityofRochester,Departmen tofComputer Science,
Rochester,NY.
Traum,DavidR.1996.Areactive-deliberativemodelofdialogue agency.InMÄuller,J.P.;
Wooldridge, M.J.;andJennings, N.R.,editors1996,IntelligentAgentsIII|Proceedings
oftheThirdInternational Workshop onAgentTheories,Architectures,andLanguages
(ATAL-96),LectureNotesinArti¯cial Intelligence. Springer-V erlag,Heidelberg.151{
157.
Wittgenstein, Ludwig1953.Philosophic alInvestigations .BasilBlackwellLtd.
Wooldridge, M.andJennings, N.R.1995.Intelligentagents:Theoryandpractice. Knowl-
edgeEngineeringReview10(2):115{152.

258 BIBLIOGRAPHY

Appendix A
TrindiKit functionalit y
A.1Introduction
Inthisappendix,wegiveamoredetaileddescription ofsomepartsofTrindiKit relevant
totheimplemen tationoftheIBISsystems. Thisdescription referstoversion3.0aof
TrindiKit1.
Apartfromthegeneralarchitecture de¯nedin1.5,theTrindiKit provides,amongother
things,
²de¯nitions ofdatatypes,foruseinTISvariablede¯nitions
²aformatforde¯ning datatypes
²methods(checks,queriesandupdates)foraccessing theTIS
²alanguage forspecifyingTISupdaterules
²anupdatealgorithm language formodules
²acontrolalgorithm language forthecontroller,including concurren tcontrol
²simpledefaultmodulesforinput,interpretation, generation andoutput
²useofexternal resources
1Thelatesto±cial versionofTrindiKit isavailable fromtheTrindiKit webpage,
www.ling.gu.se/projekt/trindi .Version3.0aisavailablefromwww.ling.gu.se/~sl/Thesis .
259

260 APPENDIX A.TRINDIKIT FUNCTIONALITY
Wewill¯rstexplainhowdatatypesarede¯ned,andgivespeci¯cations ofsomedatatypes
usedbyIBIS.Wethenshowhowthesede¯nitions relatetothesyntaxandsemanticsof
conditions, queriesandupdates.Wegoontoshowhowconditions, queriesandupdatesare
usedinformulatingupdaterules.Twoalgorithm speci¯cation languages, forcoordinating
updaterulesandmodules,respectively,arethenintroduced.Finally,wedescribesomeof
themodulesincluded intheTrindiKit package.
A.2Datatypes
Datatypes2areusedextensivelyintheTrindiKit architecture, mostimportantlyfor
modellingtheTIS.Datatypesprovideanaturalwayofformalizing information states.
TheTISisspeci¯edusingabstract datatypes,eachpermitting aspeci¯csetofqueriesto
inspectthetypeandoperations tochangeit.
TheTrindiKit providesanumberofdatatypede¯nitions, towhichtheusermayaddher
own.
A.2.1Datatypede¯nition format
Adatatypede¯nition mayincludethefollowing:
1.relations
2.functions
3.selectors
4.operations
Datatypesareimplemen tedintheformofPrologclauses,hererepresentedintheform
HeadClauseÃBodyorsimplyHeadClause.
2Analternativ etermis\(abstract) datastructure".

A.2. DATATYPES 261
Relations
Theargumen tsofarelationareobjects,andthede¯nition oftherelationspeci¯esbetween
whichobjectstherelationholds.Forexample, therelationinhastwoargumen ts,asetS
ofobjectsoftypeTandanobjectXoftypeT,andholdsifXisamemberofS.
Theheadclauseofarelationde¯nition hastheformin(A.1).
(A.1)relation( Rel,[Arg1;:::;Argn])
Asamplede¯nition ofarelationisisshownin(A.2).
(A.2)relation( <,[A;B])ÃA<B
Relations mayalsobeindirectly de¯nedbyfunctions andselectors, aswillbeexplained
below.
Functions
Functions takeobjectsasargumen tsandreturnanewobject.Forexample, thefunction
fsttakesastackSoftypestack(T)andgivesthetopmost elementX(oftypeT)ofthe
stack.Ifthestackisempty,theresultofthefunction isunde¯ned; thatis,functions may
bepartial.
Theheadclauseofafunction de¯nition hastheformin(A.3).
(A.3)function( Fun,[Arg1;:::;Argn],Result)
Asamplede¯nition ofarelationisisshownin(A.4).
(A.4)function( arity,[set(Xs)],N)Ãlength(Xs;N).
Everyfunction correspondstoarelationaccording totheschemain(A.5).
(A.5)relation( Fun,[Arg1;:::;Argn;Result])Ã
function( Fun,[Arg1;:::;Argn],Result)
Forexample, giventhefunction aritywealsohavearelationaritywhoseargumen tsisa
setSandanintegerN;thisrelationholdsiftheNistheresultofapplying aritytoS,i.e.
ifNisthearityofS.

262 APPENDIX A.TRINDIKIT FUNCTIONALITY
Selectors
Selectors canberegarded asaspecialkindoffunctions whichcanbeappliedtocollections
ofobjects(i.e.objectscontainingotherobjects,e.g.sets,stacksandrecords) toselect
objectsinthecollection.
Theheadclauseofafunction de¯nition hastheformin(A.6).
(A.6)selector( Sel,Coll,Obj,CollWithHole,Hole)
Here,Collisacollection (e.g.astack),ObjistheobjectinCollselected bySel.
CollWithHoleisacopyofCollwithObjreplaced byaprologvariable Hole.Thereason
forthiswayofimplemen tingselectors israthertechnicalandwewillnotbepursued here.
Asamplede¯nition ofaselectorisisshownin(A.7).
(A.7)selector( fst,stack([FstjRest]),Fst,stack([HolejRest]),Hole
)
Everyselectorcorrespondstoafunction according totheschemain(A.8).
(A.8)function( Sel,[Coll],Obj)Ã
selector( Sel,Coll,Obj,CollWithHole,Hole)
Forexample, giventheselectorfstwhichselectsanobjectObjinastackS,wealsohave
afunction fstwhoseargumen tisSandanwhoseresultisObj.Theresultofapplying this
function toSisObjifObjisthetopmost elementofS.
Sinceeachselectorcorrespondstoafunction andeachfunction correspondstoarelation,
itfollowsthateachselectorcorrespondstoarelation. Forexample, giventheselectorfst
whichselectsanobjectObjinastackS,wealsohavearelation fstwhichholdsiffst
selectsObjinS.
Operations
Operations takeaninputobjectand(optional) argumen tsandreturnanoutputobject.
TheobjectsinTrindiKit areimmutable ,whichmeanstheycannotbechanged. What
operations doistoreplaceanobjectwithanotherobjectwhichistheresultofapplying
theoperationtotheoriginalobject.

A.2. DATATYPES 263
Theheadclauseofanoperationde¯nition hastheformin(A.9).
(A.9)operation( Opr,Objin,[Arg1;:::;Argn],Objout)
Asamplede¯nition ofanoperationisisshownin(A.10).
(A.10)operation( push,stack(Xs),[X],stack([XljXs]))
Everyoperationcorrespondstoarelationaccording totheschemain(A.11).
(A.11)relation( Opr,[Objin,Arg1;:::;Argn,Objout])Ã
operation( Opr,Objin,[Arg1;:::;Argn],Objout)
Forexample, giventheoperationpushwhichpushesanobjectXonastackStack in,
resulting inastackStack out,wealsohavearelationpushwhoseargumen tsareStack in,
X,andStack out.ThisrelationholdsifStack outistheresultofpushing XonStack in.
SomedatatypesusedbyIBiS
Inthissection,welistthede¯nitions ofsomeofthedatatypesusedintheimplemen tation
ofIBiS.Relations, functions, selectors andoperationsarehererepresentedastheyappear
inupdaterules,ratherthanhowtheyappearinthedatatypede¯nitions. Therelation
betweentheserepresentationisthefollowing:
²Rel(Arg1;:::;Argn)givenrelation( Rel,[Arg1;:::;Argn])
²Fun(Arg1;:::;Argn)givenrelation( Fun,[Arg1;:::;Argn],Result)
²Coll=Selgivenselector( Sel,Coll,Obj,CollWithHole,Hole)
²Opr(Arg1;:::;Argn)givenrelation( Opr,Objin,[Arg1;:::;Argn],Objout)
Relations aredescribedintermsoftruthconditions, i.e.whathastobetruefortherelation
tohold.Forfunctions, thereisadescription oftheresultofapplying thefunction toits
argumen ts.Forselectors, theselectedobjectisdescribed.Foroperations, thedescription
explains howtheoperationmodi¯estheobjecttowhichitisapplied.
Someofthedescriptions belowarepartialinthesensethatnotallrelations, functions,
selectors andoperations areincluded. Wehavemainlyincluded thoseusedinIBiS.

264 APPENDIX A.TRINDIKIT FUNCTIONALITY
Set
Simpleunordered set.
type:set
rel:n
in(Set,X):Xisuni¯able withanelementofSet
fun:n
arity(Set):thenumberofelements inSet
sel:n
Set/elem:anelement(member)ofSet
opr:8
><
>:add(X):addsanelement X
del(X):deletesanelementuni¯able withX,failsifnoelementisuni¯able withX
extend( Set):addallelements ofSet
Stack
Simplestack.
type:stack
rel:n
fst(Stack,X):Xisuni¯able withthetopmostelementofStack
fun:n
arity(Stack):thenumberofelements inStack
sel:n
Set/fst:thetopmostelementofSet
opr:(
push(X):makeXthetopmostelement
pop:popthestack,i.e.removethetopmostelement
Openstack(\stackset")
Stackwithsomeset-likeproperties.Non-topmost elementscanbeaccessed. Openstacks
cannotcontaintwouni¯able elements.
type:openstack
rel:(
fst(Stack,X):Xisuni¯able withthetopmostelementofStack
in(Stack,X):Xisuni¯able withanelementofSet
fun:n
arity(Stack):thenumberofelements inStack
sel:n
Set/fst:thetopmostelementofSet

A.2. DATATYPES 265
opr:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:push(X):ifnoelementisuni¯able withX,makeXtopmost;
ifXisuni¯able withanelement Y,makeYthetopmostelement
raise(X):makeanelementuni¯able withXthetopmostelement;
failsifXisnotuni¯able withanyelement
pop:popthestack,i.e.removethetopmostelement;
failsifthestackisempty
del(X):deletesanelementuni¯able withX;
failsifnoelementisuni¯able withX
Queue
FIFOqueue.
type:queue
rel:n
none3
fun:n
arity(Queue):thenumberofelements inQueue
sel:(
Queue/fst:the¯rst(closesttoendtop)elementofSet
Queue/lst:thelast(closesttotheend)elementofSet
opr:(
push(X):makeXthelastelement
pop:popthequeue,i.e.removethe¯rstelement
OpenQueue
FIFOqueuewithsomeset-likepropertiesanda\shift"operation.
type:openqueue
rel:8
>>><
>>>:fst(Queue,X):Xisuni¯able withthetopmostelementofQueue
in(Queue,X):Xisuni¯able withanelementofSet
fullyshifted( Queue):Queuehasbeenshiftedonecycle,
i.e.allelements havebeenshiftedonce
fun:n
arity(Queue):thenumberofelements inQueue
sel:(
Queue/fst:the¯rst(closesttoendtop)elementofSet
Queue/lst:thelast(closesttotheend)elementofSet

266 APPENDIX A.TRINDIKIT FUNCTIONALITY
opr:8
>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>:push(X):ifnoelementisuni¯able withX,makeXthelastelement;
ifXisuni¯able withanelement Y,makeYthelastelement
pop:popthequeue,i.e.removethe¯rstelement; failsifthestackisempty
del(X):deletesanelementuni¯able withX;
failsifnoelementisuni¯able withX
shift:popandpush¯rstelementtotheend;
requiresshiftingenabled
initshift:initialize queueforshifting
cancelshift:disableshifting
pair
Simplepairofobjects,possiblyofdi®erenttypes.Wewillsometimes usethenotation
Fst-Sndforpairs.
type:pair
rel:n
none
fun:n
none
sel:(
Pair/fst:the¯rstelementofPair
Pair/snd:thesecondelementofPair
opr:(
setfst(X):setthe¯rstelementtoX
setsnd(X):thesecondelementtoX
record
Recursiverecordstructure.
type:record
rel:n
none
fun:n
none
sel:n
Record/Label:thevalueofLabelinRecord
opr:n
add¯eld(Label;Obj):adda¯eldwithlabelLabelandvalueObj

A.2. DATATYPES 267
Typeindependent
Apartfromthetype-speci¯crelations, functions, selectors andoperations, therearesome
thatapplytoobjectsofalltypes.
type:(anytype)
rel:8
><
>:isset:theobjectisset(itisnotnil)
isunset:theobjectisnotset(itisnil)
isempty:theobjectisempty(onlyusefulforcollections)
fun:n
(none)
sel:n
(none)
opr:8
>>><
>>>:set(Obj):thevariableissettoObj
unset:thevariableisunset(settonil)
clear:thevalueofthevariableissettobeanemptyobjectoftypeT
(onlyusefulforcollections)
Resource objects,types,andvariables
Eachresource mustbede¯nedasaresourceobjectofacertaintype,aresourcetype.The
de¯nition ofthistypecanberegarded asainterfacetowhateverinput/output facilities
areavailablefortheresource itself,enabling theresource tobeaccessed byTrindiKit .
Resources arehookeduptotheTISusingresource interfacevariables, andthevalueofa
resource interfacevariableisaresource object.
Asampleinterfacetypede¯nition foralexicon(muchliketheoneusedbyIBiS)isshown
in(A.12).
(A.12) type:lexiconT
rel:8
>>><
>>>:inputform(Lexicon; Phrase;Moves):Phraseisinterpretedas
MovesbyLexicon
outputform(Lexicon; Move;Phrase):Moveisgeneratedas
PhrasebyLexicon
fun:n
(none)
sel:n
(none)
opr:n
(none)
Theremaybeseveralresources ofeachtype;forexample, theremaybelexiconsforseveral
languages whichallareofthetypelexiconT. Foreachobject,atypedeclaration suchas
thosein(A.13)isneeded.

268 APPENDIX A.TRINDIKIT FUNCTIONALITY
(A.13)lexicontravelenglish:lexiconT
lexicontravelswedish:lexiconT
lexiconvcrenglish:lexiconT
lexiconvcrswedish:lexiconT
Tohookuparesource totheTIS,weneedaresource interfacevariabletypedeclaration
andanassignmen tofaresource objecttothatvariable,asshownin(A.14).(SeeSection
A.3.4foranexplanation oftheassignmen tsyntax.)
(A.14) lexicon:lexiconT
lexicon :=lexicontravelenglish
Anoteonthedi®erence betweenmodulesandresources: Resources aredeclarativ eknowl-
edgesources, external totheinformation state,whichareusedinupdaterulesandal-
gorithms. Modules,ontheotherhand,areagentswhichinteractwiththeinformation
stateandarecalleduponbythecontroller.Ofcourse,thereisaproceduralelementto
allkindsofinformation search,whichmeansamongotherthingsthatonemustbecareful
nottoengageinextensivetime-consuming searches.Conversely,modulescanbede¯ned
declarativ elyandthushaveadeclarativ eelement.Thereisnosharpdistinction dictat-
ingthechoicebetweenresource ormodule;forexample, itispossibletohavetheparser
bearesource. However,itisimportanttoconsider theconsequences ofchoosingtosee
something asaresource ormodule.
A.3Methodsforaccessing theTIS
TheTIScanbeaccessed inthreeways:conditions ,queries,andupdates.Checkingand
querying arewaysto¯ndoutwhattheinformation stateislike,andtheycanbindPro-
logvariables. Updateschangetheinformation state,butcannotbindPrologvariables.
Conditions aretrueorfalse,whereas queryandapply-calls failorsucceed.
A.3.1Objects,functions, locations,andevaluation
Theinformation stateinTrindiKit consists ofvariables whosevaluesareobjectsof
di®erenttypes.Whenexplaining thesyntaxforconditions inSectionA.3.2wewilluse
Objasavariablerangingoverallobjects;forexample, Objcanbeastackoraninteger.TIS
variablesareevaluatedusingthevariableevaluation operator\$",whichcanberegarded
asafunction fromTISvariablestoobjects.ThesyntaxruleforObjallowingobjectsto
bespeci¯edusingevaluation ofaTISvariable TISvarisshownin(A.15).

A.3. METHODS FORACCESSING THETIS 269
(A.15) Obj!$TISvar
Objectscanalsobespeci¯edusingevaluation offunctions; thefunction evaluation operator
isdenoted \$$".Givenafunction Funtakingargumen tsArg1;:::;Argn,thesyntaxrule
in(A.16)allowsspecifyinganobjectbyapplying FuntoObj1;:::;Objn.
(A.16) Obj!$$Fun(Obj1;:::;Objn)
Byusingpaths,builtupbyselectors, itispossibleto\point"atanobjectembeddedatthe
correspondinglocationinsidea(complex) objectandinspectormanipulate it.Pathsthus
appearintwocontexts:inspection,wheretheyspecifyobjects,andmanipulation, where
theyspecifylocations.
AnobjectXcanbespeci¯edbyacomplex objectandaselector SelpointingoutXinside
thecomplex object.Thesyntaxruleforpointingoutembeddedobjectsusingselectors is
shownin(A.17).
(A.17) Obj!Obj=Sel
Thisrecursivede¯nition allowsselectors tobeiterativelyappliedtoobjects,usingexpres-
sionsoftheformObj=Sel1=Sel2:::=Seln;thisisequivalentto(:::((Obj=Sel1)=Sel2):::
=Seln).
Another basicconceptinTrindiKit isthatoflocationsinobjects.Thegeneralsyntax
forlocationsisshownin(A.18);here,SelisaselectorandObjisacomplex object(a
collection).
(A.18) Loc!Loc=Sel
Loc!TISvar
Again,therecursivede¯nition allowsselectors tobeiterativelyapplied, usingexpressions
oftheformTISvar=Sel1=Sel2:::=Seln;thisisequivalentto(:::((TISvar=Sel1)=Sel2):::
=Seln).
Forexample, assumewehaveaTISwheretheinformation stateproper(theISvariable)
hasthetypegivenin(A.19)andthevaluegivenin(1.19.)(Thisexamples assumes there
arede¯nitions ofthetypesPropositionandTopic.)
(A.19) is:"
beliefs :Set(Prop osition)
topics =Stack(Topic)#
(A.20) is="
beliefs =fhappy(sys),frustrated(usr) g
topics =htheweather,foreignpoliticsi#

270 APPENDIX A.TRINDIKIT FUNCTIONALITY
Then,thefollowingholds:
²thelocationpointedtobyis/topics containstheobjecthweather,foreignpolitics
i
²$is/topics/fst isequivalenttotheweather
²thelocation is/beliefs/elem contains(indeterministically) somememberoftheset
fhappy(sys),frustrated(usr) g
²htheweather,foreignpoliticsi/fstisequivalenttotheweather
²$$arity($is/beliefs )isequivalentto2
TrindiKit o®ersashortcut representationforpathsintheinformation stateproper:
²theobject$/Pathisequivalentto$is=Path
²thelocation /Pathisequivalenttois=Path
A.3.2Conditions
Thebasicsyntaxrulesforconditions isshownin(A.21).Argumen ts(Argi;1·i·n)are
eitherobjectsor(ifallowedbytherelationde¯nition) prologvariables.
(A.21)a.Cond!Rel(Arg11;:::;Argn
e.g.fst($/topics ,Q)
b.Cond!Arg1::Rel(Arg2;:::;Argn)
e.g.$/shared/qud ::fst(Q)
c.Cond!Obj1=Obj2
ThisholdsifObj1andObj2areuni¯able.
d.Cond!Obj1==Obj2
ThisholdsifObj1andObj2areidentical.
Givenconditions Cond,Cond1andCond2,thefollowingconstructs arealsopossible:
²Cond1andCond2
ThisistrueifCond1istrueandCond2istrue.

A.3. METHODS FORACCESSING THETIS 271
²Cond1orCond2
ThisistrueifCond1istrueorCond2istrue.Cond1willbetested¯rst,andonlyif
itisfalsewillCond2betested.
²notCond
ThisistrueifCondisfalse.
²forall(Cond1,Cond2)
Thisisequivalenttonot(Cond1and(notCond2)).
²setof(Obj,Cond,ObjSet)
ObjSetisthesetofobjectsObjsatisfying Cond.
Conditions andFirstOrderLogic
IntermsofFirstOrderLogic(FOL),acondition canbeseenasaproposition(whichis
trueorfalseoftheTIS),existentiallyquanti¯edoverallPrologvariablesoccuringinthe
condition -exceptforvariables occuringonlywithinthescopeofnegation oruniversal
quanti¯cation.
Anillustration isshownin(A.22)(C1(X),C2(X;Y)andC3(Y;Z)areconditions; X,Y
andZarePrologvariables, andx;yandzarethecorrespondingFOLvariables).
(A.22)(C1(X)andC2(X;Y)andC3(Y;Z))»
9x;y;z(C1(x)^C2(x;y)^C3(y;z))
Negation
Whenevaluating \notCond",somePrologvariablesappearinginCondmayalreadyhave
becomebound(whenevaluating aprevious check).Anypreviously boundvariablesap-
pearinginCondwillstillbeboundwhenevaluating "notCond.
(A.23)(C1(X)and(notC2(X))andC3(Y;Z))»
9x;y;z(C1(x))^:C2(x)^C3(y;z)
Anypreviously unboundvariablesappearinginCondwillnotbeboundbychecking\not
Cond".Theyareinterpreted asexistentiallyquanti¯edwithinthescopeofthenegation,
asillustrated in(A.24).Anyoccurrences ofthesevariablesoccuringinfollowingconditions
willbeindependent,i.e.theycanberegarded asseparate variables.

272 APPENDIX A.TRINDIKIT FUNCTIONALITY
(A.24)(C1(X)and(notC2(X;Y))andC3(Y;Z))»
9x;y;z(C1(x))^:9y0(C2(x;y0))^C3(y;z)
Universalquanti¯cation
ThebindingbehaviourofPrologvariablesinsidethescopeof\forall"issimilartothatfor
\not",whichisnaturalsince\forall"isde¯nedusing\not".
IfX1;:::;XnarevariablesinCond1whicharenotpreviously bound,andY1;:::;Ymare
variablesinCond2whicharenotpreviously boundanddonotoccurinCond1,theFOL
interpretation isasshownin(A.25).
(A.25)forall(Cond1;Condn)»
8x1;:::;xn(Cond1!9y1;:::;ym(Cond2))
Anypreviously boundvariables appearinginCond1orCond2willstillbeboundwhen
evaluating \forall(Cond1;Cond2)".Anypreviously unboundvariablesappearinginCond1
orCond2willnotbeboundbychecking\forall(Cond1;Cond2)".Anyoccurrences ofthese
variablesoccuringinfollowingconditions willbeindependent,i.e.theycanberegarded
asseparate variables.
A.3.3Queries
Queriesaresimilartoconditions inthattheydonotmodifytheinformation state;however,
theyarealsosimilartoupdatesinthattheydonotbacktrack,andiftheyfailtheyproduce
anerrormessage. Thesyntaxforqueriesisshownin(A.26).
(A.26) Query!!Cond
Forexample, aquery\!in($/topics ,Q)"willbindQtothetopmost elementofthestack
in/topics .However,ifthestackisemptyanerrormessage willbereported.
A.3.4Updates
UpdatesmodifyTIS,andifanupdatefails,anerrormessage isreported.Thebasicsyntax
forupdatesisshownin(A.27).

A.4. RULEDEFINITION FORMA T 273
(A.27)a.Update!Opr(Loc;Obj1;:::;Objn)
e.g.push(/topics, sports)
b.Update!Loc::Obj1;:::;Objn)
e.g./topics::push(sports)
c.Update!Loc:=Obj
Equivalenttoset(Loc;Obj).
GivenupdatesUpdate,Update 1;:::;Update n,theconstructions in(A.28)arealsopossible.
(A.28)a.Update![Update 1;:::;Update n]
Execute Update 1;:::;Update ninsequence.
b.Update!ifdo(Cond,Update)
IfCondholds,execute Update.
c.Update!ifthenelse(Cond,Update 1,Update 2)
IfCondholds,execute Update 1;otherwise, execute Update 2.
d.Update!foralldo(Cond,Update)
(Seebelowforexplanation)
Itispossibletoapplyanoperationrepeatedlyusingasingleupdatecallwiththesyntax
\foralldo(Cond,Update)",whereCondisacondition andUpdateisanupdate.
LetX1;:::;XnbeallunboundPrologvariablesinCond(i.e.thosewhicharenotbound
whentheupdateisapplied). Now,theinterpretation of\foralldo(Cond,Update)"goes
asfollows:\Forallbindings ofX1;:::;XnwhichmakeCondtrue,applyUpdate."
Asanexample, forallAsuchthatAisintheset/beliefs ,(A.29)willpushAonthe
stackat/topics .
(A.29)foralldo(in($ /beliefs ,A),push(/topics ,A))
A.4Rulede¯nition format
UpdaterulesarerulesforupdatingtheTIS.Theyconsistofarulename,aprecondition list,
andane®ectlist.Preconditions areconditions, ande®ectscanbequeriesorupdate-calls.
Ifthepreconditions ofarulearetruefortheTIS,thenthee®ectsofthatrulecanbe
appliedtotheTIS.Rulemayalsobelongtoaclass.

274 APPENDIX A.TRINDIKIT FUNCTIONALITY
Therulede¯nition formatisshownin(A.30).
(A.30) rule:RuleName
class: RuleClass
pre:n
PrecondList
eff:n
EffectsList
Here,PrecondList isalistofconditions andEffectsList isalistofqueriesandupdates.
TheRuleClassmaybeusedinde¯ning DMEalgorithms (Section A.5).
Theprecondition listCond1;:::;Cond2inaruleisequivalenttoaconjunction \Cond1
and:::andCondn".Anyvariablesthatbecomeboundwhilecheckingthepreconditions
willstillbeboundwhenexecuting thee®ects.
A.4.1Backtrackingandvariablebindinginrules
WhenaruleisappliedtotheTIS,thepreconditions willbeevaluatedintheorderthey
appear.Sinceconditions maybenondeterministic, conditions containingPrologvariables
mayhaveseveralpossibleresults.Forexample, checking\member(X)"onasetfa,b,cg
hasX=a,X=bandX=caspossibleresults.
The¯rsttimethischeckismade,the¯rstsolution willbereturned, i.e.Xwillbecome
boundtoa.Ifalaterprecondition whichusesXisnottrueforX=a,TrindiKit willuse
Prolog's backtrackingfacilitytogobackandgetthesecondsolution X=b.Inthisway,the
TrindiKit ruleinterpreter willtryto¯ndawaytobindthePrologvariablesappearing
intheprecondition list4sothatallthepreconditions hold.
Oncethishassucceeded, thee®ectsoftherulewillbeappliedusingthevariablebindings
obtained whencheckingthepreconditions. Continuingtheexample above,ifallprecon-
ditionssucceed withXboundtoa,thisbindingwill\survive"tothee®ectsandany
appearanceofXinthee®ectswillbeequivalenttoanappearanceofa.
A.4.2Condition andoperationmacros
Inaddition totheconditions andoperationsprovidedbythedatatypede¯nitions, itisalso
possibletowritemacros.Macrosde¯nesequences ofconditions (forcondition macros)
4apartfromthoseappearinginthescopeofanegation oruniversalquanti¯cation, seeA.3.2andA.3.2
respectively

A.5. THEDME-ADL LANGUA GE 275
oroperations (foroperationmacros).Likeconditions andoperations (butunlikerules),
macroscantakeargumen ts.
Macrosarede¯nedbyassociatingamacrowithalistofTISconditions oralistofTIS
updates.
(A.31)macrocond(beliefandtopic(X),[in($/belief,X),in(
$/topic,X)])
(A.32)macroupdate(addtobeliefandtopic,[add(/belief,X),
push(/topic,X)])
A.4.3PrologvariablesintheTIS
TrindiKit doesnotprohibit PrologvariablesaspartoftheTIS,i.e.objectscancontain
Prologvariables. Thishastheadvantagethatitispossibletohavepartially uninstan tiated
objects(non-groundtermsinPrologterminology) whichmaybecomefullyinstantiatedat
alaterpoint.
However,thisalsomakesitpossibleforchecksandqueriestotemporarilychangethe
information statebyunifying apartially instantiatedobjectintheTISwithamorespeci¯c
object.Forexample, ifthevalueoftheTISvariable latestmoveisask(?happy(X)),
checking$latestmove=ask(?happy(john))willhavethee®ectthatlatestmove
nowhasthevalueask(?happy(john)).
Ifthischeckispartofthepreconditions listofarule,andalaterprecondition fails,
TrindiKit maybacktrackwhichmayresultinXbecoming unboundagain.Thesebind-
ings\survive"withinthescopeofanupdateruleorasequence ofconditions. Afterthe
ruleorsequence ofchecksisdone,anyPrologvariablesintheTISwillagainbeunbound.
A.5TheDME-ADL language
DME-ADL (Dialogue MoveEngineAlgorithm De¯nition Language) isalanguage forwrit-
ingalgorithms forupdatingtheTIS.Algorithms inDME-ADL areexpressions ofanyof
thefollowingkinds(CisaTIScondition; R,SandTarealgorithms, Ruleisthenameof
anupdaterule,andRuleClassisaruleclass):

276 APPENDIX A.TRINDIKIT FUNCTIONALITY
1.Rule
applytheupdateruleRule
2.RuleClass
applyanupdateruleofclassRuleClass;rulesaretriedintheordertheyaredeclared
3.[R1;:::;Rn]
execute R1;:::;Rninsequence
4.ifCthenSelseT
IfCistrueoftheTIS,execute S;otherwise, execute T
5.whileCdoR
whileCistrueoftheTIS,execute Rrepeatedly
6.repeatRuntilC
execute RrepeatedlyuntilCistrueoftheTIS
7.repeatR
execute Rrepeatedlyuntilitfails;reportnoerrorwhenitfails
8.repeat+R
execute Rrepeatedly,butatleastonce,untilitfails;reportnoerrorwhenitfails
9.tryR
trytoexecute R;ifitfails,reportnoerror
10.RorelseS
Trytoexecute R;ifitfails,reportnoerrorandexecute Sinstead
11.testC
ifCistrueoftheTIS,donothing; otherwise, haltexecution ofthecurrentalgorithm
12.applyOp
applyoperation Op
13.SubAlg
executesubalgorithm SubAlg
Subalgorithms aredeclared using),whichispreceded bythesubalgorithm nameand
followedbythealgorithm, asin(A.33).
(A.33)mainupdate)hgrounding ,
repeat+(integrate orelseaccommodate)i

A.6. THECONTR OL-ADL LANGUA GE 277
AsampleDME-ADL algorithm isshownin(A.34).
(A.34)if$latestmoves==failed
thenrepeatre¯ll
elsehgrounding,
repeat+(integrate orelseaccommodate),
if$latestspeaker ==usr
thenhrepeatre¯ll,
trydatabasei
elsestore
i
A.6TheControl-ADL language
Thecontrolalgorithm speci¯eswhether asystemshouldberuninserialorasynchronously .
Serialalgorithms aresimplerthanasynchronousones,andthesyntaxusedforasynchronous
algorithms subsumes thesyntaxforserialalgorithms. SinceIBiSusesonlyserialcontrol,
wewillnotintroducethesyntaxforasynchronous controlhere.
A.6.1Serialcontrolalgorithm syntax
TheserialControl-ADL language issimilartotheDME-ADL language, exceptthatitcalls
modulealgorithms insteadofrules,anditcanincludethe\printstate"instruction. Each
algorithm hasaname,andeachmodulemayde¯neoneormorealgorithms.
AsampleserialControl-ADL algorithm isshownin(A.35).
(A.35)hreset,
repeathselect,
generate ,
output,
update,
printstate,
test($program state==run),
input,
interpret,
update,
printstatei
i

278 APPENDIX A.TRINDIKIT FUNCTIONALITY
A.7Providedmodules
TheTrindiKit packageincludes acoupleofsimplemoduleswhichcanbeusedtoquickly
buildprototypesystems.
²inputsimpletext :asimplemodulewhichreadstextinputfromtheuserandstores
itintheTIS
²outputsimpletext :asimpletextoutputmodule
²intpretsimple1 :aninterpretation modulewhichusesalexiconofkeywordsand
phrasestointerpretuserutterances intermsofdialogue moves
²generatesimple1 :ageneration modulewhichusesalexiconofmainlycanned
sentencestogenerate systemutterances frommoves
A.7.1Simpletextinputmodule
Theinputmoduleinputsimpletext readsastring(untilnew-line) fromthekeyboard,
preceded bytheprintingofaninputprompt. Thesystemvariable inputisthensettobe
thevalueread.
A.7.2Simpletextoutputmodule
Theoutputmoduleoutputsimpletext takesthestringinthesystemvariable output
andprintsitonthecomputer screen,preceded bytheprintingofanoutputprompt. The
contentsoftheoutput variableisthendeleted. Themodulealsomovesthecontentsof
thesystemvariable nextmovestothesystemvariable latestmoves.Finallyitsets
thesystemvariable latestspeaker tobethesystem.
A.7.3Asimpleinterpretation module
Theinterpretation moduleinterpretsimple1 takesastringoftext,turnsitintoase-
quenceofwords(a\sentence")andproducesasetofmoves.The\grammar" consists
ofpairings betweenlistswhoseelementsarewordsorsemanticallyconstrained variables.
Semanticconstrain tsareimplemen tedbyasetofsemanticcategories (location,month,

A.7. PROVIDED MODULES 279
meansoftransportetc.)andsynonymysets.Asynonymysetisasetofwordswhich
allareregarded ashavingthesamemeaning.
Thesimplest kindoflexicalentryisonewithoutvariables. Forexample, theword\hello"
isassumed torealizeagreetmove.:
(A.36)inputform([hello],greet)
Thefollowingrulesaysthataphraseconsisting oftheword\to"followedbyaphraseS
constitutes ananswermovewithcontentto(C)providedthatthelexicalsemanticsofS
isC,andCisalocation .Thelexicalsemanticsofawordisimplemen tedbyacoupling
betweenasynsetandameaning; thelexicalsemanticsofSisC,providedthatSisa
memberofasynonymysetofwordswiththemeaning C.
(A.37)inputform([tojS],answer(to(C))Ãlexsem( S,C),loca-
tion(C).
Toputitsimply,theparsertriestodividethesentenceintoasequence ofphrases(found
inthelexicon), coveringasmanywordsaspossible.
A.7.4Asimplegeneration module
Thegeneration modulegenerateoutputform takesasequence (list)ofmovesandout-
putsastring.Thegeneration grammar/lexicon isalistofpairsofmovetemplates and
strings.
(A.38)outputform(greet,"Welcometothetravelagency!" ).
TorealizealistofMoves,thegenerator looks,foreachmove,inthelexiconforthecor-
respondingoutputform(asastring),andthenappendsallthesestringstogether. The
outputstringsisappendedinthesameorderasthemoves.

280 APPENDIX A.TRINDIKIT FUNCTIONALITY

Appendix B
Rules andclasses
ThisappendixlistsruleclassesusedbythevariousversionsofIBiS.Rulesarelistedin
theordertheyaretriedwhenthecorrespondingruleclassiscalledinamodulealgorithm.
TheIBiSsystemsandTrindiKit canbedownloaded from:
http://www.ling.gu.se/~sl/Thesis .
Thesizeofthesystemsrangefromapproximately 1,200linesofcode(32kbyte)forIBiS1
toabout2,500lines(75kbyte)forIBiS4,excluding domain-sp eci¯cresources.
B.1IBiS1
B.1.1IBiS1updatemodule
²grounding
{getLatestMo ve(rule3.1)(p.41)
²integrate
1.integrateUsrAsk (rule3.3)(p.44)
2.integrateSysAsk (rule3.2)(p.43)
3.integrateAnsw er(rule3.4)(p.47)
4.integrateGreet (rule3.6)(p.48)
5.integrateSysQuit (rule3.8)(p.49)
281

282 APPENDIX B.RULES AND CLASSES
6.integrateUsrQuit (rule3.7)(p.48)
²downdatequd
1.downdateQUD (rule3.5)(p.48)
2.downdateQUD2 (rule3.16)(p.63)
²loadplan
1.recoverPlan (rule3.17)(p.64)
2.¯ndPlan (rule3.9)(p.49)
²execplan
1.removeFindout (rule3.10)(p.50)
2.removeRaise (rule3.19)(p.66)
3.execconsultDB (rule3.11)(p.50)
B.1.2IBiS1selectmodule
²selectaction
1.selectResp ond(rule3.14)(p.53)
2.selectFromPlan (rule3.12)(p.51)
3.reraiseIssue (rule3.18)(p.65)
²selectmove
1.selectAnsw er(rule3.15)(p.54)
2.selectAsk (rule3.13)(p.52)
3.selectOther
B.2IBiS2
B.2.1IBiS2updatemodule
²grounding
{getLatestMo ves(rule4.16)(p.130)

B.2.IBIS2 283
²integrate
1.integrateUsrAsk (rule4.1)(p.110)
2.integrateSysAsk (rule4.18)(p.132)
3.integrateNegIcmAnsw er(rule4.7)(p.115)
4.integratePosIcmAnsw er(rule4.8)(p.116)
5.integrateUsrAnsw er(rule4.4)(p.113)
6.integrateSysAnsw er(rule4.19)(p.132)
7.integrateUndIn tICM (rule4.6)(p.115)
8.integrateUsrP erNegICM (rule4.20)(p.133)
9.integrateUsrAccNegICM (rule4.21)(p.135)
10.integrateOtherICM (rule4.10)(p.121)
11.integrateGreet
12.integrateSysQuit
13.integrateUsrQuit
14.integrateNoMo ve
²downdatequd
{downdateQUD
{downdateQUD2
²loadplan
1.recoverPlan (rule4.24)(p.143)
2.¯ndPlan (rule4.23)(p.143)
²execplan
1.removeFindout
2.execconsultDB
²(none)
{irrelevantFollowup(rule4.22)(p.141)
{unclearFollowup

284 APPENDIX B.RULES AND CLASSES
B.2.2IBiS2selectmodule
²selectaction
1.rejectIssue (rule4.15)(p.129)
2.rejectProp (rule4.14)(p.127)
3.selectIcmUndIn tAsk(rule4.3)(p.112)
4.selectIcmUndIn tAnswer(rule4.5)(p.114)
5.selectResp ond(rule4.26)(p.147)
6.selectFromPlan
7.reraiseIssue (rule4.25)(p.144)
²selecticm
1.selectIcmConNeg (rule4.9)(p.120)
2.selectIcmP erNeg (rule4.11)(p.121)
3.selectIcmSemNeg (rule4.12)(p.122)
4.selectIcmUndNeg (rule4.13)(p.123)
5.selectIcmOther (rule4.2)(p.111)
²selectmove
1.selectAnsw er(rule4.27)(p.147)
2.selectAsk
3.selectOther
4.selectIcmOther (rule4.2)(p.111)
²(none)
{backupShared (rule4.17)(p.131)
B.3IBiS3
B.3.1IBiS3updatemodule
²grounding
{getLatestMo ves

B.3.IBIS3 285
²integrate
1.retract (rule5.7)(p.180)
2.integrateUsrAsk
3.integrateSysAsk
4.integrateNegIcmAnsw er(rule5.10)(p.184)
5.integratePosIcmAnsw er(rule5.11)(p.189)
6.integrateUsrAnsw er
7.integrateSysAnsw er
8.integrateAccommo dationICM
9.integrateUndP osICM
10.integrateUndIn tICM
11.integrateUsrP erNegICM
12.integrateUsrAccNegICM
13.integrateOtherICM
14.integrateGreet
15.integrateSysQuit
16.integrateUsrQuit
17.integrateNoMo ve
²accommodate
1.accommodateIssues2QUD (rule5.2)(p.169)
2.accommodateQUD2Issues (rule5.9)(p.183)
3.accommodatePlan2Issues (rule5.1)(p.166)
4.accommodateCom2Issues (rule5.6)(p.179)
5.accommodateCom2IssuesDep endent(rule5.8)(p.182)
6.accommodateDependentIssue (rule5.4)(p.172)
²downdateissues
{downdateISSUES
{downdateISSUES2 (similartodowndateQUD2 inIBiS1)
²downdatequd
{downdateQUD

286 APPENDIX B.RULES AND CLASSES
²loadplan
1.recoverPlan
2.¯ndPlan
²execplan
1.removeFindout
2.execconsultDB
²selectaction
1.selectIcmUndIn tAsk
2.selectIcmUndIn tAnswer
3.selectIcmUndIn tRequest
4.rejectIssue
5.rejectAction
6.rejectProp
²none
{irrelevantFollowup
{unclearFollowup
{failedFollowup
{noFollowup(rule5.12)(p.190)
{backupSharedUsr (rule5.13)(p.193)
B.3.2IBiS3selectmodule
²selectaction
1.clarifyIssue (rule5.3)(p.170)
2.clarifyDep endentIssue (rule5.5)(p.176)
3.selectResp ond
4.selectFromPlan
5.reraiseIssue
²selecticm
1.selectIcmConNeg

B.4.IBIS4 287
2.selectIcmP erNeg
3.selectIcmSemNeg
4.selectIcmUndNeg
5.selectIcmOther
²selectmove
1.selectQuit
2.selectAnsw er
3.selectAsk
4.selectGreet
5.selectIcmOther
²none
{backupSharedSys
B.4IBiS4
B.4.1IBiS4updatemodule
²grounding
{getLatestMo ves
²integrate
1.retract
2.integrateUsrAsk
3.integrateSysAsk
4.integrateUsrRequest (rule6.1)(p.216)
5.integrateCon¯rm (rule6.6)(p.218)
6.integrateNegIcmAnsw er
7.integratePosIcmAnsw er
8.integrateUsrAnsw er
9.integrateSysAnsw er
10.integrateAccommo dationICM

288 APPENDIX B.RULES AND CLASSES
11.integrateUndP osICM
12.integrateUndIn tICM
13.integrateUsrP erNegICM
14.integrateUsrAccNegICM
15.integrateOtherICM
16.integrateGreet
17.integrateSysQuit
18.integrateUsrQuit
19.integrateNoMo ve
²accommodate
1.accommodateIssues2QUD
2.accommodateQUD2Issues
3.accommodatePlan2Issues
4.accommodateCom2Issues
5.accommodateCom2IssuesDep endent
6.accommodateDependentIssue
7.accommodateAction (rule6.8)(p.221)
²downdateissues
1.downdateISSUES
2.downdateISSUES2
3.downdateISSUES3 (downdates resolvedaction-issue)
4.downdateActions (rule6.7)(p.218)
²downdatequd
{downdateQUD
²loadplan
1.¯ndPlan
2.¯ndActionPlan
²execplan
1.recoverPlan
2.recoverActionPlan

B.4.IBIS4 289
3.removeFindout
4.execconsultDB
5.execdevget
6.execdevset
7.execdevdo(rule6.3)(p.217)
8.execdevquery
²selectaction
1.selectIcmUndIn tAsk
2.selectIcmUndIn tAnswer
3.selectIcmUndIn tRequest
4.rejectIssue
5.rejectProp
6.rejectAction (rule6.2)(p.216)
²(none)
{backupSharedUsr
{irrelevantFollowup
{irrelevantFollowup
{unclearFollowup
{failedFollowup
{noFollowup
{declineProp
B.4.2IBiS4selectmodule
²selectaction
1.clarifyIssue
2.clarifyIssueAction (rule6.9)(p.221)
3.selectCon¯rmAction (rule6.4)(p.217)
4.selectResp ond
5.reraiseIssue
6.selectFromPlan

290 APPENDIX B.RULES AND CLASSES
²selecticm
1.selectIcmConNeg
2.selectIcmP erNeg
3.selectIcmSemNeg
4.selectIcmUndNeg
5.selectIcmOther
²selectmove
1.selectQuit
2.selectAnsw er
3.selectAsk
4.selectCon¯rm (rule6.5)(p.217)
5.selectGreet
6.selectIcmOther
²(none)
{backupSharedSys