Chapter 3
Grounding issues
3.1 Introduction
Intheprevious chapter,weassumed \perfectcommunication" inthesensethatallut-
terances wereassumed tobecorrectly perceivedandundersto od,andfullyaccepted. Of
course,theseassumptions areunrealistic bothinhuman-humanandhuman-computer con-
versation. Ausefuldialogue systemneedstobeabletodealwithcasesofmiscomm unica-
tionandrejections.
Wewillnotattempt togiveacomplete computational theoryaboutthegrounding process
inhuman-humandialogue. Rather,wewillprovideabasicissue-based account,influenced
by Ginzburg, whichtriestocoverthemainphenomena thatadialogue systemneeds
tobeabletohandle. Forinstance, thefactthatspeechrecognition ismuchharderfor
machinesthanforhumansmaymotivatedifferentgrounding strategies forhandling system
utterances thanforhandling userutterances.
First,weprovidesomedialogue examples wherevariouskindsoffeedbackareused. We
thenreviewanddiscusssomerelevantbackground, anddiscussgeneraltypesandfeatures
offeedbackasitappearsinhuman-humandialogue. Next,wediscusstheconcept of
grounding fromaninformation updatepointofview,andintroducetheconcepts ofopti-
mistic,cautious andpessimistic grounding strategies. Thisisfollowedbythemainsection
ofthischapter,wherewerelategrounding andfeedbacktodialogue systems, discussthe
implementationofissue-based grounding andfeedbackin IBi S2,andprovidedialogue ex-
amplesshowingthesystem's behaviourandhowitrelatestointernalupdates. Wethen
reviewadditional implementationissues,andprovideafinaldiscussion.
75

76 CHAPTER 3. GROUNDING ISSUES
3.1.1 Dialogue examples
Thehuman-humandialogue excerpt 1 in(3.1)showstwocommon kindsoffeedback. J's
\mm"showsthat J(thinksthathe)understo od P'sprevious utterance; P's\pardon"
showsthat Pwasnotabletohear J'sprevious utterance. Theexample alsoincludes a
hesitation sound(\um")from J.(Pisacustomer and Jatravelagent.)
(3.1)P:öom(.)flygtiparis
um(.)flighttoparis
J:mm(.)skaduhaenreturbiljett
mm(.)doyouwantareturnticket
P:vasadu
pardon
J:skaduhaenturÅaretur
doyouwantaroundtrip
Thefeedbackin(3.1)consisted ofconventionalized feedbackwords(\mm", \pardon").
However,feedbackmayalsobemoreexplicitandrepeatthecentralcontentoftheprevious
utterance, as K'ssecondfeedbackutterance in(3.2).
(3.2)B:jaskavaframmei[1 göoteborg]1 eeungeföarvinietiden om
definnsnÅatidit[2 morgonflyg ]2
Ineedtobein Gothenbur gereraroundnineifthereisanearly
morning flight
K:[1 m]1
m
K:[2 vi]2 nietiden mviskase
Aroundninemlet'ssee
Thefunction ofanutterance answeringaquestion isnotprimarily togivefeedback,but
rathertoprovidetask-related information. However,anansweralsoshowsthatthepre-
viousquestion wasundersto odandintegrated. Example (3.3)showsthatfeedbackis
sometimes giveninreaction toaquestion beforethequestion isanswered.
(3.3)J:senmÅasteduhaesÅandöarintenationellt studentkortocksÅa
hadude
thenyouneedoneofthoseinternational studentcardsdoyou
havethat
P:mmnöa
mmno
1Exceptwherenoted,thehuman-humandialogues inthischapterhavebeencollected bythe University
of Lundaspartofthe SDSproject. Wequotetranscriptions donein Göteborgaspartofthesameproject.
The(.)symbolindicates apause.

3.1. INTR ODUCTION 77
However,oftenhuman-humancommunication proceedswithoutexplicitfeedback,asinthe
excerptfromatelephone dialogue in(3.4).
(3.4)K:vartskaduÅaka
whereareyougoing
B:ejagskaÅakatillgöoteborg
eri'mgoingtogothenbur g
K:vilketdatum
whatdate
B:densjöattejuni
thesixthofjune
K:villduÅakameflygellermetÅag
doyouwanttoflyortakethetrain
Bycontrast,incurrentcommercial systems itiscommon tocheckthesystem's interpre-
tationofrecognized userinputaskingay/n-question, asseeninthe(invented)dialogue
in(3.5).Thisbehaviourismuchlesscommon inhuman-humandialogue, butmayoccur
innoisyenvironmen tsorwhencommunicating overanunreliable communication channel
(e.g.whenusingamobilephoneonatrain).
(3.5)S:Whatdaydoyouwishtotravel?
U:Friday
S:Fridaythe 5 thof April,isthatcorrect?
Asimilarbutnotidenticalbehaviourdoesoccurinhuman-humandialogue, asin(3.6),
takenfromthe London-Lund corpusandusedby Clarkin Clarkand Schaefer(1989 a). In
thisexample, Bgivesandexplicitreportofhow A'sutterance wasinterpreted, whereupon
Aconfirms thattheinterpretation iscorrectbysaying\yes".
(3.6)A:F.sixtwo
B:Fsixtwo
A:yes
B:thanksverymuch
Thedialogue in(dialogue 3.1)givesanimpression ofwhatfeedbackcapabilities weaim
toaddto IBi Sinthischapter.
(dialogue 3.1)
S>Welcome tothetravelagency!

78 CHAPTER 3. GROUNDING ISSUES
S>hello
U>priceinformation please
S>Youaskedaboutprice. Howdoyouwanttotravel?
U>pardon
S>Howdoyouwanttotravel?
U>byplane
S>Byplane,isthatcorrect?
U>yes
S>Okay. Whatcitydoyouwanttogoto?
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
3.2 Background
Inthissection,weprovideabriefoverviewandofsomeprevious accountsofgrounding
andfeedback.
3.2.1 Clark:Addingtothecommon ground
Clarkand Schaefer(1989 a)describegrounding astheprocessofaddingtothecommon
ground(see Section 2.2.2).Theyalsoformulatethegroundingcriterion :
Grounding criterion: Thecontributor andthepartners mutuallybelievethat
thepartners haveundersto odwhatthecontributor meant,toacriterion suffi-
cientforcurrentpurposes.(Clarkand Schaefer,1989 a,p.148)
Toachievethis,eachgrounding processgoesthrough twophases:

3.2. BACKGROUND 79
²Presentationphase:Apresentsutterance ufor Btoconsider. Hedoessoonthe
assumption that,if Bgivesevidence eorstronger, hecanbelievethat Bunderstands
what Ameansbyu.
²Acceptance phase. Bacceptsutterance ubygivingevidence e 0 thathebelieves
heunderstands what Ameansbyu. Hedoessoontheassumption that,once A
registers evidence e 0,hewillalsobelievethat Bunderstands. (Clarkand Schaefer,
1989 a,p.151)
Clark(1996)arguesthatutterances involveactionson(atleast)fourdifferentlevels:
(3.7)Level Speaker A'sactions Addressee B'sactions
4Aisproposingajointprojectwto BBisconsidering A's
proposalofw
3Aissignalling thatpfor B Bisrecognizing thatp
2Aispresentingsignalsto B Bisidentifyings
1Aisexecuting behaviourtfor B Bisattending tot
Examples ofjointprojectsareadjacency pairs,e.g.one DPaskingaquestion andtheother
answeringit. According to Clark,thesefourlevelsofactionconstitute anactionladder,
andassuchitissubjecttotheprinciple ofdownwardevidence:\Inaladderofactions,
evidence thatoneleveliscomplete isalsoevidence thatalllevelsbelowitarecomplete".
Forexample, if Hunderstands u,Hmustalsohaveperceiveduand Hand Smusthave
established contact;however,Hmaynotacceptu.
In Clarkand Schaefer(1989 a), itisunclearwhether grounding includes theproposal/
consideration levelinaddition tounderstanding 2. However,in Clark(1996),grounding
isredefined toincludealllevelsofaction,i.e.attention,identification, recognition and
consideration.
Togroundathing(:::)istoestablish itaspartofcommongroundwellenough
forcurrentpurposes.(:::)Onthishypothesis,grounding shouldoccuratall
levelsofcommunication. (Clark,1996,p.221,italicsinoriginal)
Wewilladoptthisgeneraluseofthetermgrounding toincludeallfouractionlevels. Also,
weassumethattheacceptance phase(potentially)concerns allfouractionlevels,rather
thanonlyunderstanding 3.
2Thedefinition suggests onlyunderstanding isinvolved,butsomeexamples indicate thatutterances
whicharerejected becauseofbeinginappropriate arenotgrounded.
3Theterm\acceptance phase"isabitunfortunate, since\acceptance" isusedbye.g. Ginzburg to
designate theproposal-consideration actionlevel.

80 CHAPTER 3. GROUNDING ISSUES
Clarklistsfivewaystosignalthatacontribution hasbeensuccessfully interpreted and
accepted, orderedfromweakesttostrongest:
²Continuedattention
²Relevantnextcontribution
²Acknowledgemen t:\uh-huh",nodding,etc.
²Demonstration: reformulation,collaborativecompletion
²Display:verbatimdisplayofpresentation
Thepresentationandacceptance phasesbothfocusonexternally observablecommunicative
behaviour. However,correspondingtopresentationsbyaspeakeroneachlevelofaction
thereisalsoan\internal"actioncarriedoutbytheaddressee.
Clarkviewstheproposal-consideration processintermsofnegotiation, whereanutter-
ancesuchasanassertion oraquestion isseenasaproposalforajointproject,followed
byaresponsetothisproposal. Clarkfollows Goffman (1976)and Stenströom(1984)in
distinguishing fourmaintypesofresponsestoproposalsofjointprojects:
1.fullcompliance, e.g.answeringaquestion [acceptance]
2.alteration ofproject,where Halterstheproposedprojecttosomething heiswilling
tocomplywith;Clarkassertsthatalterations maybecooperative(inwhichcasethe
alteredprojectisstillrelevanttotheoriginalone)oruncooperative[alteration]
3.declination ofproject,where Hisunableorunwillingtocomplywiththeprojectas
proposed. Declinations areoftenperformed byofferingareasonorjustification for
declining theproposal. Clarkgivestheresponse\Idon'tknow"toaquestion asan
example ofdeclination. [rejection]
4.withdrawalfromproject,where Hwithdrawsfromconsidering theproposal,e.g.by
deliberatelyignoring aquestion andchanging thetopic[withdrawal]
3.2.2 Ginzburg: QUD-based utterance processingprotocols
Ginzburg offersanissue-based modelofgrounding ontheunderstanding andacceptance
levelsbypositingtwokindsofgrounding-related questions: meaning-questions andaccep-
tancequestions 4. If Aproducesutterance u,Bisfacedwithameaning-question, roughly
4Thelattertermisours. Itrefersto Ginzburg's MAX-QUD questions discussed below.

3.2. BACKGROUND 81
\Whatdoesumean?". If Bcannotfindananswertothisquestion, Bshouldproduce
anutterance identicalorrelatedtothemeaning-question, e.g.\Whatdoyoumean?". If
Bmanages tofindananswertothisquestion, heproceedstoconsider theacceptance-
question, roughly\Should ubeaccepted?".
Ginzburg's utterance processingprotocol(pt.1)Ginzburg formulateshistheory
intermsofanutterance processingprotocol. Assuming theother DPAhasuttered u,this
isroughlywhathappensinthefirstpartoftheprotocol:
Bisfacedwiththecontent-question qcontent(u),whichweformalize as?x.content(u;x),
paraphrasable roughlyas\Whatdoesumean(giventhecurrentcontext)?". Toanswer
thisquestion, Bmustbeabletoprovideacontextualinterpretation cofu. Thisinvolves,
amongotherthings,findingreferentsfor NPs. If Bisnotabletoanswerqcontent(u),B
placesqcontent(u)on QUDandproducesaqcontent(u)-specificutterance, e.g.arequestfor
clarification. Onceananswertoqcontent(u)hasbeenfound,Bcanbesaidtohavean
understanding ofu(whichmay,ofcourse,beamisunderstanding).
Ginzburg notesthatutterances behavedifferentlywithregardtoacceptance dependingon
whether theyhavepropositionsorquestions ascontent. Apropositionpcanbeaccepted in
twoways:asafactorasatopic(issue)ofdiscussion. Inthelattercase,thequestion under
discussion is,roughly,whether pshouldbeaccepted asafact(atleastforthepurposes
ofcurrentdiscussion) ornot. Accepting apropositionentailsaccepting italsoasanissue
fordiscussion (although the\discussion" inthiscasewillconsistonlyoftheacceptance of
pasafact).Theexchangesin(3.8)showsomeexamples ofreactions toassertions (note
thattheseexamples arenot Ginzburg's).
(3.8)a. A:Thetrainleavesat 10 a.m.[answer/assert p]
B:OK,thanks.[accept p]
b. A:Thetrainleavesat 10 a.m.[answer/assert p]
B:Noitdoesn't![rejectp,accept?pfordiscussion]
c. A:Thetrainleavesat 10 a.m.[answer/assert p]
B:I'dprefernottodiscussthisrightnow[reject?pfordis-
cussion]
d. A:Thetrainleavesat 10 a.m.[answer/assert p]
B:Niceweather,isn'tit[ignore p]
Questions, bycontrast,canonlybeaccepted asissuesfordiscussion. However,accepting q
doesnotnecessarily resultinansweringq. Onthisaccount,answeringqshouldbeviewed
asonepossiblewayofdisplayinginternalacceptance ofq;however,contraryto Clarkwe
alsoallowthepossibilityofdisplayingacceptance ofqwithoutansweringq.

82 CHAPTER 3. GROUNDING ISSUES
(3.9)a. A:Wheredoyouwanttogo[askq]
B:Paris[answerq,implicitly acceptq]
b. A:Wheredoyouwanttogo[askq]
B:Hmmm, goodquestion... Doyouhaveanyrecommenda-
tions?[explicitly acceptq]
c. A:Wheredoyouwanttogo[askq]
B:That'snoneofyourbusiness [explicitly rejectqbecause
ofunwillingness]
d. A:Wheredoyouwanttogo[askq]
B:Idon'tknow[explicitly rejectqbecauseofinability]
e. A:Wheredoyouwanttogo[askq]
B:I'dliketotravelin April[ignoreq,answerotherquestion]
f. A:Wheredoyouwanttogo[askq]
B:Doyouhaveastudentdiscount?[ignoreq,askother
question]
Ginzburg's utterance processingprotocol,pt.2Aswesawabovein Section 3.2.2,
according to Ginzburg's utterance processingprotocol,fora DPBtounderstand anut-
terance uamountstofindingananswertothecontent-question qc.
Once Bisabletofindananswercwhichresolves?x.content(u;x),Bisfacedwiththe
question qaccept(c)ofwhether ornottoacceptcfordiscussion, formalized by Ginzburg
as?MAX-QUD( c)(\Whether cshouldbecome QUD-maximal"5).Atthispoint,the
protocolisdifferentforquestions andpropositions(\facts"). Ifcisaquestion and B
answersqaccept(c)negatively(rejects cfordiscussion), Bpushescon QUDandproducesan
c-specificutterance (e.g.\Idon'twanttodiscussthat").Ifqaccept(c)isansweredpositively
and Baccepts c,cwillbeaddedto QUDand Bwillproduceac-specificutterance, e.g.
ananswertothequestion c.
Ifcinsteadisapropositionandif Banswersqaccept(c)negatively Bshouldpushqaccept(c)
on QUDandproduceaqaccept(c)-specificutterance. Butifqaccept(c)isansweredpositively,
Bmustnowconsider thequestion whether c,i.e.?c. Iftheanswerisnegative(i.e. B
doesnotacceptc),thecorrespondingy/n-question ?cispushedon QUD. Thisamounts
toaccepting ?cfordiscussion, whichisnotthesameasaccepting c. If Banswersqaccept(c)
positively,Bshouldaddctoher FACTS.
5Thismeansthatthearguably moreintuitiveinterpretation of?MAX-QUD( c)as\whethercismaximal
on QUD"iswrong.

3.2. BACKGROUND 83
Forclarity,wereproducethefullprotocolinamoreschematic way:
trytofindananswerresolving qcontent(u)=?x.content(u,x)
²noanswerfound!pushqcontent(u)on QUD,produceqcontent(u)-specificutterance
²answercfound!
{cisaquestion!consider qaccept(c)=?MAX-QUD( c)
¤decideon\no"!pushqaccept(c)on QUD,produceqaccept(c)-specificutter-
ance[rejectc]
¤decideon\yes"!pushcon QUD,producec-specificutterance [accept c]
{cisaproposition!consider qaccept(?c)
¤no!pushqaccept(?c)on QUD,produceqaccept(?c)-specificutterance [reject
?castopicfordiscussion]
¤yes!consider ?c[accept?castopicfordiscussion]
¢no!push?con QUD,produce?c-specificutterance [rejectcasfact]
¢yes!addcto FACTS[accept casfact]
Notethatthereareanumberofdecisions thatneedtobemadeby B,andforeachofthese
decisions thereisthepossibilityofrejecting uonthecorrespondinglevel. Foraquestion,
thereisonlyonewayofrejecting it(oncethecontentquestion hasbeenresolved):toreject
itasaquestion underdiscussion. Thisamountstorefusing todiscussthequestion. For
aproposition p,therearetwodifferentwaysofrejecting it. Firstly,onemayrejectthe
issue\whether p"completely; thisamountstorefusingtodiscusswhether pistrueornot.
Alternativ ely,onemayaccept\whether p"fordiscussion butrejectpasafact.
3.2.3 Allwood:Interactive Communication Managemen t
Allwood(1995)usestheconceptof\Interactive Communication Managemen t"todesignate
allcommunication dealingwiththemanagementofdialogue interaction. Thisincludes
feedbackbutalsosequencing andturnmanagement .Sequencing \concerns themecha-
nisms,wherebyadialogue isstructured intosequences, subactivities, topicsetc....".
Here,wewillusetheterm ICMasageneraltermforcoordination ofthecommon ground,
whichinaninformation stateupdateapproachcomestomeanexplicitsignalsenabling
coordination ofupdatestothecommon ground. Whilefeedbackisassociatedwithspecific
utterances, ICMingeneraldoesnotneedtoconcernanyspecificutterance.

84 CHAPTER 3. GROUNDING ISSUES
Aswillbeseenbelow,wewillalsobemakinguseofvariousotherpartsof Allwood's
\activity-basedpragmatics" (Allwood,1995),including Allwood'sactionlevelterminol-
ogy,theconcept of Own Communication Managemen t(OCM), andvariousdistinctions
concerning ICM.
3.3 Preliminary discussion
Intheprevious sectionwehaveseenexamples ofdifferentwaysofaccountingforgrounding
andfeedback. Wefeelthattheyallofferusefulinsights,andthattheytogether canserve
asabasisforourfurtherexplorations.
Therefore, inthissectionwewilldiscusstheaccountspresentedin Section 3.2,relatethem
toeachother,andestablish somebasicprinciples andterminological conventions.
3.3.1 Levelsofactionindialogue
Both Allwood(1995)and Clark(1996)distinguish fourlevelsofactioninvolvedincom-
munication (Sisthespeakerofutterance u,Histhehearer/addressee). Theyuseslightly
differentterminologies; hereweuse Allwood'sterminology andadd Clark's(and,forthe
reaction level,also Ginzburg's) correspondingtermsinparenthesis. Thedefinitions are
mainlyderivedfrom Allwood.
²Reaction (acceptance, consideration): whether Hhasintegrated (thecontentof)u
²Understanding (recognition): whether Hunderstands u
²Perception (identification): whether Hperceivesu
²Contact(attention):whether Hand Shavecontact,i.e.iftheyhaveestablished a
channelofcommunication
Theselevelsofactionareinvolvedinalldialogue, andtotheextentthatcontact,per-
ception, understanding andacceptance canbesaidtobenegotiated, allhuman-human
dialogue hasanelementofnegotiation builtin. Notethattheabovelistoflevelsisformu-
latedintermsofthehearer'sperspective.
Giventhatgrounding isconcerned withalllevels,itfollowsthatfouraspectsofanutterance
uinadialogue between Hand Scaninprinciple berepresentedinthecommon ground,
oneforeachactionlevel:

3.3. PRELIMINAR YDISCUSSION 85
²whether uhasbeenintegrated (takenup,accepted)
²whether uhasbeenundersto od
²whether uhasbeenperceived
²whether Sand Hhavecontact
Also,grounding-related feedbackmayconcernany(andpossiblyseveral)oftheselevels.
Thelevelreferredtoasreaction/acceptance/consideration inthelistaboveisdefineddif-
ferentlybydifferentauthors. Allwoodcallsit\reaction (tomainevocativeintention)",
Ginzburg talksabout\acceptance", and Clarkusestheterm\consideration (ofjoint
project)".Perhapsitcouldbearguedthatthesedifferentdefinitions arenotconcerned
withtheexactsamephenomena. Sincewewanttousethedistinction ratherthandebate
it,wechoosetoemphasize thesimilarities ratherthanthedifferences.
3.3.2 Reaction levelfeedback
Onceanutterance hasbeenundersto od(orisbelievedtobeundersto od),inthesensethat
thehearerhasinterpreted theutterance tohaveameaning andpurposewhichisrelevant
intheactivity(asperceivedbythehearer), thehearermustdecidewhattodowiththe
utterance. Shouldhee.g.trytoanswerthequestion thatwasasked,orrefuse?Shouldhe
choosetocommittoanasserted proposition,orraiseobjections?
Thereaction processwhichfollowstheunderstanding ofamove Mcanbeanalytically
dividedintothreesubsteps:
²consideration: whether ornottoacceptandintegrate M(andconsequen tly(tryto)
actontheevocativeintention)
²integration: updatingthecommon groundaccording to M
²feedback:signalling theresultsofconsideration of M
Thedivisionofthereaction phaseintoconsideration andfeedbackisalsomadein Allwood
(1995),usingtheterms\evaluation" and\report"(respectively),and(thoughperhapsnot
soexplicitly) in Clark(1996).However,theintegration stepisnot(atleastnotexplicitly)
included ineitheroftheseaccounts.

86 CHAPTER 3. GROUNDING ISSUES
Intheconsideration phase,the DPinvestigates whether hecanandwantstoacceptthe
proposedjointprojectornot. Ifnot,heneedstodecidewhether toalter,decline,orignore
theproposal.
Wewillusethetermintegrationforthesilent(internal)consequence ofdeciding toaccept
(comply with)aproposedjointproject,modelledastheprocessofupdatingone'sview
ofthecommon groundwiththefulleffectsofaperformed move. By\thefulleffects"we
meane.g.takingapropositiontobetrue(atleastforthepurposesoftheconversation)
ortakingaquestion asbeingunderdiscussion. Inrelationto Clark'suseof\uptake",we
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
²unwillingness: DPdoesnotwanttodiscusstheissue,e.g.because DPbelievesother
information ismoreimportantatthemoment
²inability:DPisnotabletodiscusstheissue,e.g.becauseofconfidentialityorlack
ofknowledge
Regarding theupdateeffectsofdeclining aquestion, thereseemstobeanimportant
difference betweenbeingunabletoansweraquestion (ase.g.inthecasewheretheresponse
is\Idon'tknow"),andbeingunwillingtoanswerit. Intheformercase,itisnotclearthat
thequestion isactually rejected asatopicfordiscussion. Theaddressee ofthequestion
maythinkthathemighteventuallycomeupwithananswer(asaresultofnewinformation
orinference); inthiscase\Idon'tknow"canbeinterpreted as\Idon'tknowrightnow,but

3.3. PRELIMINAR YDISCUSSION 87
I'llkeepthequestion inmind".Inthiscase,thequestion mightnothavetobeexplicitly
raisedagainbeforebeingrespondedto.
Inthecasewheretherejection displaysunwillingness toanswerthequestion (e.g.\No
comment",\Iwillnotanswerthat",\That'snoneofyourbusiness"), itismuchclearer
thatthequestion isactually rejected asatopicfordiscussion.
Thereisalsoadifference betweenquestions andpropositionsregarding thereasonsfor
rejection. As Ginzburg notes,asserted propositionsmayberejectedasissuesfordiscussion,
butevenifaccepted asissuestheymayberejected asfacts. Soforpropositions, the
consideration phaseismorecomplex thanforquestions, potentiallyinvolvingtwodecisions
(e.g.rejecting theasserted propositionasafact,butaccepting itasanissue).
Rejecting apropositionasanissuecanbeexplained bythesamekindsofreasonsasfor
anyissue. Rejecting apropositionasafactmaybecausede.g.bytheaddressee having
aconflicting belief,ornottrusting thespeaker. Itmayalsobeexplained byabeliefthat
accepting thepropositionwillnotservethegoalsofthe DPs,ase.g.ifacustomer in
atravelagencyassertsthatthedestination cityofherflightis Kuala Lumpur, whenin
facttheagencyonlyservesdestinations in Europe. Ofcourse,thepropositionthatthe
customer wantstotravelto Kuala Lumpur canhardlyberejected bytheclerk;however,
thepropositionthat Kuala Lumpur isthedestination cityofatripthattheclerkwill
provideinformation aboutcanberejected. Thiskindofexample isespeciallyrelevantfor
database searchsystems, whereinformation abouttheuser'sdesiresandintentionsisnot
storedassuch.
3.3.3 Levelsofunderstanding
Concerning thelevelsofactiondescribedin Section 3.2.1,wecanmakefurtherdistinctions
betweendifferentlevelsofunderstanding, correspondingtothreelevelsofmeaning. These
sublevelsgiveafinergradingtothelevelofunderstanding. (Asimilardistinction isalso
usedby Ginzburg (forth)).
²domain-dep endentanddiscourse-dep endentmeaning (roughly,\content"intheter-
minology of Barwise and Perry,1983 and Kaplan, 1979)
{referentialmeaning ,e.g.referentsofpronouns, temporalexpressions
{pragmatic: therelevanceofuinthecurrentcontext
²discourse-indep endent(butpossiblydomain-dep endent)meaning (roughly correspond-
ingto\meaning" intheterminology of Barwise and Perry,1983 and Kaplan, 1979),
e.g.staticwordmeanings

88 CHAPTER 3. GROUNDING ISSUES
By\discourse-indep endent"wemean\independentofthedynamic dialogue context"
(modelledin IBi Sbytheinformation stateproper).However,discourse-indep endentmean-
ingmaystillbedependentonstaticaspectsoftheactivity/domain. Itisobviousthatthese
levelsofmeaning areintertwinedanddonothaveperfectlyclearboundaries. Nevertheless,
webelievetheyareusefulasanalytical approximations.
Sincedialogue systemsusuallyoperateinlimiteddomains, wewillassumethatwedonot
havetodealwithambiguities whichareresolvedbystaticknowledgerelatedtothedomain.
Forexample, adialogue systemforaccessing bankaccountsdoesnothavetoknowthat
\bank"mayalsorefertothebankofariver;itissimplyveryunlikely(though ofcourse
notimpossible)thatthewordwillbeusedwiththismeaning intheactivity. Itcanbe
arguedwhether thisisalwaysagoodstrategy,butfornowweacceptthisasareasonable
simplification.
3.3.4 Somecommentson Ginzburg's protocol
Thefirstthingtonoteabout Ginzburg's grounding protocolisthatitdoesnotspecify
exactlywhatkindoffeedbackshouldbeproduced. Thenotionofquestion-sp ecificity(see
Section 2.8.2)isaminimal requiremen tthatneedstobesupplemen tedwithadditional
heuristics todecideonexactlywhatfeedbacktoprovide. Also,itdoesnotspecifyhow
a DPdecideswhenasatisfactory interpretation hasbeenfound,orhowtoresolvethe
content-andacceptance questions. Theseareallthingsweneedtobespecificaboutwhen
implemen tingadialogue system. (Ofcourse,totheextenttheyaredomain-dep endent,
wewouldnotexpecttofindtheminageneraltheoryofdialogue. Whether theyare
domain-dep endentornotis,onourview,anopenquestion.)
Second,Ginzburg seemstoassumeacertaindegreeoffreedom concerning thesharedness
of QUD. According tothegrounding protocol,DPsarefreetoaddagrounding-related
question qto QUDwithoutinforming theother DP(s),providedthisisfollowedbyanut-
terancespecifictotheaddedquestion. Infact,themechanismofquestion accommodation
thatwillbepresentedin Chapter 4 providesanexplanation ofhow DPscanunderstand
answerstounaskedquestions. However,itisnotclearthatthisshouldallowthespeaker
tomodify QUDbeforeuttering theq-specificutterance. Itseemsinconsisten ttosaythat
a DPthatassumes QUDissharedcanmodify QUDwithouthavinggivenanyindication
ofthistotheother DP;howwouldtheother DPbeabletoknowaboutthismodification
beforetheq-specificutterance hasbeenmade?Soitappearsthat Ginzburg hasanotion
of QUDasnotnecessarily entirelyshared,andthisisslightlydifferentfromthenotionof
QUDweareusing.(Seealso Section 4.8.5.)
Third,Ginzburg onlydealswithunderstanding andacceptance; contactandperception
areleftout. Sotheprotocolabovedoesnotdealexplicitly withcaseswherea DPisunsure

3.4. FEEDBA CKAND RELA TED BEHA VIOUR INHUMAN-HUMAN DIALOGUE 89
whichwordswereuttered(however,itdealswithperception indirectly sinceunderstanding
isbasedonperception).
Relationbetween Clark'sand Ginzburg's accounts
Itseemspossibletodrawsomeparallels betweenthetwoaccountsreviewedabove. Clark's
\recognition ofmeaning" wouldpresumably bemodelledby Ginzburg asfindingananswer
tothecontent-question. Similarly ,Clark's\consideration ofproposal"ismodelledas
consideration oftheacceptance question.
Clarktalksaboutjointprojectsin\track 2"(meta-comm unication, asopposedto\track
1",fortask-levelcommunication) asinvolvingspeakers(oftenimplicitly) raisingvarious
issuesrelatedtogrounding, e.g.\Doyouunderstand this?",andtheresponderanswering
theseissues(oftenimplicitly). Thisfitswellwiththeissue-based approachproposedby
Ginzburg.
On Clark'saccount,thereisnoasymmetry betweenquestions andpropositionsconcern-
ingacceptance. Thequestion-related counterpartofaccepting apropositionasafact,
according to Clark,isansweringthequestion. However,itcanbearguedthatanswering
thequestion ismerelyanexternal behaviourcausedby(andactingaspositivefeedback
concerning) theactualacceptance ofthequestion asanissue. Clark'squestion-related
counterpartofrejecting apropositionasafact(declination )isansweringe.g.\Idon't
know"(Clark,1996,p.204),andtherebysignalling lackofabilityorwillingness to\com-
plywiththeprojectasproposed".Presumably ,\Nocomment"or\Irefusetoanswer
thatquestion" wouldalsocountasrejections onthesamelevel,whichindicates thatthey
arereallyissue-rejections. The\withdra wal"that Clarktalksabout,wheretheaddressee
deliberatelyignoresaproposal,seemstobeequallyapplicable tobothassertions andques-
tions.(Infact,Lewin(2000)viewscaseswherea DPanswersadifferentquestion thanthe
onethatwasasked,therebywithdrawingfromtheproposedquestion, asrejections.)
3.4 Feedbackandrelatedbehaviourinhuman-human
dialogue
Byfeedbackwemeanbehaviourwhoseprimaryfunction istodealwithgrounding ofutter-
ancesindialogue 6. Thisdistinguishes feedbackfrombehaviourwhoseprimary function is
relatedtothedomain-leveltaskathand,e.g.gettingpriceinformation. Non-feedbac kbe-
6Sincethisthesisisnotconcerned withmultimodaldialogue, wewillonlydiscussverbalfeedback.

90 CHAPTER 3. GROUNDING ISSUES
haviourinthissenseincludesaskingandansweringtask-levelquestions, givinginstructions,
etc.(cf.the\Core Speech Acts"of Poesioand Traum,1998).Answeringadomain-level
question (e.g.saying\Paris"inresponseto\Whatcitydoyouwanttogoto?")certainly
involvesaspectsofgrounding andacceptance, sinceitshowsthatthequestion wasunder-
stoodandaccepted. However,theprimary function ofadomain-levelansweristoresolve
thequestion, nottoshowthatitwasundersto odandaccepted.
Asingleutterance mayincludebothfeedbackanddomain-levelinformation. Clarktalks
aboutcommunication ofthesetwotypesofinformation asbelonging todifferent\tracks":
domain-levelinformation isontrack 1 whilefeedback,andgrounding-related communica-
tioningeneral,isontrack 2.
Inthissectionwewillattempt togiveanoverviewofvariousaspectsoffeedback. Wewill
returntosequencing ICMin Section 3.6.9.
3.4.1 Classifying explicitfeedback
Togetanoverviewoftherangeofexplicitfeedbackbehaviourthatexistsinhuman-human
dialogue, wewillclassifyfeedbackaccording tofourcriteria. Wewillassumethat DPS
hasjustutteredorisuttering uto DPH,whenthefeedbackutterance f(uttered by H
to S)occurs.
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
formareallderivedfrom Allwood et al.(1992)and Allwood(1995).

3.4. FEEDBA CKAND RELA TED BEHA VIOUR INHUMAN-HUMAN DIALOGUE 91
3.4.2 Positive,negative,andneutralfeedback
Positivefeedbackindicates oneorseveralofcontact,perception, understanding, andinte-
gration,whilenegativefeedbackindicates lackthereof.
Whilethereareclearcasesofpositive(\uhuh",\ok")andnegative(\pardon?", \Idon't
understand") feedback,therearealsosomecaseswhicharenotsoclear. Forexample,
arecheck-questions (e.g.\To Paris?"inresponseto\Iwanttogoto Paris")positiveor
negative?Ifpositivefeedbackshowsunderstanding, andnegativefeedbacklackofunder-
standing, thencheck-questions aresomewhere inbetween;theyindicateunderstanding but
alsothatthelackofconfidence inthatunderstanding.
Herewewillassumeathirdcategory ofneutralfeedbackforcheck-questions andsimilar
feedbacktypes. Ifnegativefeedbackindicates alackofunderstanding, neutralfeedback
indicates lackofconfidence inone'sunderstanding.
Negativefeedbackcanbecausedbyfailuretointegrate Uonanyofthelevelsofactionin
dialogue:
²lackofcontact-Hdidnotnoticethat Ssaidsomething
²lackofperception -Hdidnothearwhat Ssaid
²lackofunderstanding onasemantic/pragmatic level-Hrecognized allthewords,
butcouldnotextractacontent
{context-indep endentmeaning, e.g.wordmeanings
{context-dependentmeaning, e.g.referents
{pragmatic meaning, i.e.therelevanceof S'sutterance inrelationtothecontext
²rejection ofcontent
Fornegativefeedback,detecting thelevelwithwhichthefeedbackisconcerned isimportant
forbeingabletorespondappropriately .Herearesomepossibilities forthedifferentlevels:
²contact:trytoestablish contact(\Heythere")
²perception: speaklouder,articulate
²understanding
{meaning: reformulate

92 CHAPTER 3. GROUNDING ISSUES
{pragmatic meaning: reformulate,orexplainhowtheutterance isrelevant
²rejection: abandon orarguefortheacceptance ofthecontent
3.4.3 Eliciting andnon-eliciting feedback
Wewillusetheterm\eliciting feedback",borrowedfrom Allwood et al.(1992),torefer
tofeedbackutterances intendedtoelicitaresponse,ormorespecifically utterances u 0 such
thatu 0 isintendedtomake Srespondtou 0 because Hisnotsureabouthowtointerpret
S'sutterance u. Check-questions (bothy/n-andalternativ e-questions) areseenaseliciting
feedbackinthissense. Eliciting feedbackcanalsooccurafter S'sutterance uisfinished.
3.4.4 Formoffeedback
Aswithallutterances, feedbackutterances canhavevarioussyntacticforms:
²assertion
{declarativ e(\Iheardyousay`goto Paris'.",\Youwanttogoto Paris.")
²imperative(\Please repeat.")
²interrogativ e
{y/n-question (\Didyousay`Paris'?",\Doyouwanttogoto Paris?")
{wh-question (\Whatdidyousay?",\Whatdoyoumean?", \Wheredoyouwant
togo?")
{alternativ e-question (\Didyousay`Paris'or`Ferris'?",\Doyouwanttogoto
Paris,Franceor Paris,Texas?")
²ellipsis(\Paris?",\to Paris.")
²conventional(\Pardon?")
Apartfromshowingthespeakerthatonehasundersto od,feedbackintheformofanexplicit
declarativ ereport,repetitionorreformulationhastheadditional function ofmakingsure
thattheunderstanding isactually correct,byprovidingachanceforcorrection. Ay/n-
question hasasimilarfunction, butitindicates lessconfidence intheinterpretation (i.e.is

3.4. FEEDBA CKAND RELA TED BEHA VIOUR INHUMAN-HUMAN DIALOGUE 93
moreneutral) andhasastronger elicitingelementthananassertion; aquestion requiresan
answer,whileanassertion canoftenbeassumed tobeaccepted intheabsenceofprotest.
Arelateddimension ofclassification ishowtheformofthefeedbackutterance relatesto
theprevious utterance. Onewayofgivingpositivefeedbackistosimplyrepeatverbatim
theprevious utterance (e.g.\To Paris."inresponseto\To Paris.").Asimilarstrategy is
toprovideareformulation(e.g.\Yourdestination cityis Paris,thecapitalof France.").
Thelatterisperhapsastronger signalofunderstanding thentheformer,sinceaverbatim
repetitiondoesnotinprinciple requirethattheutterance wasundersto od.
3.4.5 Meta-levelandobject-levelfeedback
Afinaldistinction canbemadedependingonwhether thefeedbackexplicitly talksabout
whatthespeakersaidormeant,inwhichcasethefeedbackcanbesaidtobemeta-level
feedback,orifinsteadittalksaboutthesubjectmatterofthedialogue, inwhichcasewe
talkaboutobject-levelfeedback.
²Meta-level
{perception (\Didyousay`Paris'?")
{understanding (\Didyoumeanthatyouwanttogoto Paris?")
²Object-level(\Doyouwanttogoto Paris?")
Thisdistinction doesnotnecessarily applytoallkindsoffeedback. Forexample, for
conventionalphraseslike\Pardon?" andelliptical phraseslike\Paris?"itisnotclearif
theyrefertowhatthespeakersaidormeant,oraboutthesubjectmatterofthedialogue,
orneither.
3.4.6 Fragmentfeedback/clarification ellipsis
Often,feedbackdoesnotconcernacomplete utterance, butonlyapartofit;thisisthe
casee.g.withfailuretoidentifyareferenttoan NP. Wecanrefertothiskindoffeedback
asfragmentfeedback(exemplified in(3.10))andcontrastitwithcompletefeedbackwhich
concerns awholeutterance (asin(3.11)).

94 CHAPTER 3. GROUNDING ISSUES
(3.10)A:Imet Jimyesterday.
B:Who?[negativepartialunderstanding ICM]
Whodidyousayyoumet?[partialnegativeunderstanding ICM
+partialpositiveunderstanding ICM]
Jim?[partialinterrogativ eunderstanding ICM]
Jim Jones?[intermediate partialunderstanding]
Jim Jonesor Jim Lewis?[partialintermediate understanding]
No,itwas Bobthatyoumet[partialacceptance, partialrejec-
tion 1]
(3.11)A:Imet Jimyesterday.
B:Pardon?[negativecomplete perception]
B:Whatdoyoumean?[negativecomplete understanding]
B:Liar![(probably) complete rejection]
Itisalsopossibletogivenegativepartialfeedbacktoonepartofanutterance andsimul-
taneously givepositivepartialfeedbacktosomeotherpart,aswhen Bsays\Whodidyou
sayyoumet?";here,Bgivespositivefeedbackthat Bundersto odthat Ametsomeone, but
negativefeedbackconcerning who Amet. Cooperand Ginzburg (2001)discussnegative
partialfeedbackusingtheterm\clarification ellipsis" andgiveanaccountinthe QUD
framework.
3.4.7 Own Communication Managemen t
Afurtheraspectrelatedtofeedbackand ICMiswhat Allwoodreferstoas Own Communi-
cation Managemen t,whichinvolveshesitation sounds,suchas\um",\er"etc.,(whichalso
havetheeffectofkeepingtheturn),andself-corrections (initiated eitherbythespeakeror
bythehearer). Itshouldalsobenotedthatsomefeedbackbehaviouralsohasan OCM
aspect;forexample, onecanexplicitly acceptaquestion to\buytime"forcomingupwith
ananswer.
3.4.8 Repairandrequestforrepair
Onetypeofbehaviourverycloselyrelatedtofeedback,andalsoto Own Communication
Managemen t(seebelow),iswhat Traumreferstoas\other-initiated repair".
1Thatis,acceptance oftheproposition\Ametsomeone", butrejection oftheproposition\theperson
that Ametwas Jim".

3.5. UPDATESTRA TEGIES FORGROUNDING 95
²other-initiated other-repair: repairby A(\Youmean Paris.")
²other-initiated self-repair: requestforrepairby A(\Doyoumean Paris?")
Thisoverlapswithwhat Clarkcallsalteration,i.e.thecasewhere Aacceptsanaltered
versionoftheproposedjointproject.
3.4.9 Request forfeedback
Above,wehaveanalyzed feedbackproducedbytheaddressee Ainresponsetoanutterance
uproducedbyaspeaker S. Anadditional typeoffeedbackbehaviourswhichareproduced
bythespeakerofuarerequests forfeedback,e.g.\Doyouunderstand?", \Gotthat?".
²understanding (\Gotthat?",\Doyouunderstand?")
²acceptance (\OK?", \Doyouagree?")
3.5 Updatestrategies forgrounding
Afterhavingreviewedgrounding-related interactivecommunication managementinhuman-
humandialogue, wewillnowexploreupdatestrategies relatedtogrounding. Inthissection,
weintroducetheconcepts ofoptimism, caution, andpessimism regarding grounding update
strategies.
3.5.1 Optimistic andpessimistic strategies
According to Clarkand Schaefer(1989 a), manymodelsofdialogue makeatacitidealization
(1)that DPsassumethatthecontentofeachutterance isautomatically addedtothe
common ground. Somemodelsmaketheweakeridealization (2)that DPsassumethatthe
contentofeachutterance isautomatically addedtothecommon groundunlessthereis
evidence tothecontrary. Clarkand Schaeferargueagainsttheseidealizations andpropose
toreplacethemwith\systematic procedures" forestablishing mutualbeliefregarding the
addressee's understanding ofutterances.
Following Clark,morerecentcomputational modelsofgrounding (e.g. Traum(1994)and
Ginzburg (forth))takeitforgrantedthatutterances arenottakentobegrounded until

96 CHAPTER 3. GROUNDING ISSUES
someformoffeedbackhasbeenproduced. Thisfeedbackneednotbeexplicit: forexample,
arelevantanswertoaquestion showsthatthe DPproducingtheanswerhasundersto od
andaccepted thequestion posedintheprevious utterance. Thatis,DPsdonotmake
assumptions aboutgrounding untilthereissomeevidence.
However,asnotedby Traumthiscannotapplytoallutterances. Ifitdid,eachconfirma-
tionofunderstanding wouldagainhavetobeconfirmed andsoonadinfinitum. Inour
terminology ,thismeansthatitisnecessary toassumeoptimism onsomelevel. In Traum's
model,acknowledgemen tsareoptimistically assumed tobegrounded (thatis,theydonot
needtobeacknowledged themselv esbeforebeingaddedtothecommon ground) whereas
anyotherconversational actsmustreceivesomeacknowledgemen tbeforebeinggrounded.
Whilewebelievethat Clarkiscorrectincriticizing tacitidealizations about DPsassump-
tionsregarding grounding, wealsobelievethatthesetacitassumptions, ifmadeinanex-
plicitandsystematic fashion,arenotnecessarily incorrect ormoreidealizing than Clark's
alternativ e. Furthermore, theydeservetobeexplored boththeoretically andforpractical
useindialogue systems. Weshouldalsokeepopenthepossibilitythat DPsmaymake
differentassumptions regarding grounding dependingonvariousfactorsofthecontext.
Ifissuesoftacitness areputaside,itseemsthatwhatwearedealingwitharedifferent
accountsofwhenanutterance istoberegarded asgrounded. Theneedforsuchan
assumption arisespartlybecausethecommunicativebehaviouritselfdoesnotcompletely
determine whether anutterance isgrounded. Atsomepoint,a DPmustsimplyassume
thatanutterance hasbeengrounded, andwebelievethatthemaindifference between
themcanbedescribedintermsofoptimism andpessimism .
Thefirsttypeof\tacitidealization" describedby Clark((1)above)canthusberestated
asanoptimistic grounding assumption; a DPadhering tothisassumption willassume,
foranyutterance u,thatuisgrounded assoonasithasbeenuttered, withnoregardto
feedback. Thesecondtypeof\idealization" ((2)above)canberestated asapessimistic
grounding assumption, sinceitrequires somewayofdetermining theabsenceofnegative
feedbackbeforegrounding isassumed. Clark'ssuggested assumption isalsopessimistic,
since DPsadhering toitwillrequirepositiveevidence beforeassuming thatanutterance
isgrounded.
3.5.2 Grounding updatesandactionlevels
Fromaninformation stateupdateperspective,itseemssensibletoregardanutterance as
grounded whenithasbeenaddedtothecommon ground. Eachactionlevelconnected
toanutterance canbeassociatedwithacertaintypeofupdate. Toassumegrounding
ontheperception levelcanbeseenasupdatingthecommon groundwiththeassumed

3.5. UPDATESTRA TEGIES FORGROUNDING 97
surfaceformoftheutterance; toassumegrounding ontheunderstanding levelistoupdate
thecommon groundwithasemanticrepresentationoftheutterance. Finally,toassume
anutterance hasbeengrounded ontheacceptance levelistoupdatethecommon ground
withtheintendedeffectsoftheutterance (e.g.pushing aquestion on QUD).Thus,the
grounding assumption canbedividedintofourindependentassumptions, oneforeachof
theselevels;wewillconcentrateontheunderstanding andintegration levels.
Theindependenceoftheseassumptions meanse.g.thatitispossibletomakeanoptimistic
assumption aboutunderstanding butapessimistic oneaboutacceptance. Thiswouldmean
assuming thatanutterance wasundersto odassoonasitwasuttered,butrequiring positive
evidence beforeitisassumed tobeaccepted.
3.5.3 Thecautious strategy
Clarkseemstoassumethatonceanutterance hasbeengrounded, thereisnoturningback;
thegrounding assumption cannotbeundone. Thatis,themomentinformation aboutan
utterance isaddedtothecommon groundthereisnoway(shortofgeneralstrategies for
beliefrevision) ofunderstanding negativefeedbackandreacttoitbymodifyingorremoving
thegrounded material.
However,webelievethatthereisadifference betweenassuming anutterance asgrounded
(addedtothecommon ground) andgivingupthepossibilityofmodifyingorcorrecting
thegrounded material. Thisopensupanewkindofgrounding strategy notincluded in
Clark'saccount:thecautious strategy.
Fora DPusingacautious strategy,itispossibletoassumeanutterance asbeinggrounded,
whilestillbeingabletounderstand andreactappropriately tonegativefeedback. This
requires(1)thatnegativefeedback,whichisoftenunderspecifiedinthesensethatitdoes
notexplicitly identifywhichpartofanutterance itconcerns, canbecorrectly interpreted,
and(2)thatthe DPcanrevisethecommon groundinawaywhichundoesalleffectsof
theerroneous assumption thattheutterance wasgrounded. Asimpleexample isshownin
(3.12).
(3.12)A:Do Ineedavisa?
Aoptimistic allyassumes that\does Aneedavisa?"isnow
underdiscussion.
B:Pardon?
Acorrectlyinterprets B'sutteranceasnegativefeedback(proba-
blyontheperceptionlevel)regardingthepreviousutterance,and
retractstheassumption that\does Aneedavisa?"ison QUD.

98 CHAPTER 3. GROUNDING ISSUES
Onthisview,theupdatesassociatedwithgrounding involvestwosteps:addingthemate-
rialtothecommon ground,andconsequen tly,removingthepossibilityof(easily)undoing
theupdatesfromthefirststep.
Oneadvantageofthecautious strategy isthatinferences resulting fromanutterance can
bedrawnimmediately ,without havingtowaitforfeedback,whilenotrequiring costly
strategies forgeneralbeliefrevisionincaseswherethegrounding assumption turnsoutto
bepremature.
Weleaveopenthequestion ofwhichstrategy isthemostcognitivelyplausible; infact,the
mostreasonable assumption isprobably thatanintelligentcombination ofdifferentstrate-
giesisthemostrealistic model. Butwedobelievethatthecautious strategy deserves
thesameattentionasthepessimistic strategy advocatedby Clark. Moreover,wedonot
wanttopreclude thepossibilitythateventheoptimistic strategy mightcomeinhandy
sometimes. Asalways,questions ofcognitiveplausibilit yarebestresolvedbyempirical
experimentationratherthanbyrhetoric. Whatwewanttodohere,apartfromimple-
mentingusefulgrounding mechanisms foradialogue system,istoshowthatthecautious
approachisatleastapossiblealternativ e.
Torepeat,wewillusethequalification \optimistic", \cautious" and\pessimistic" for
grounding updatestrategies, withthefollowingmeanings:
²optimistic grounding update:DGB7 isupdatedimmediately afteruwasproduced
(and,inthecaseofutterances producedbyother DP,understo odandaccepted); no
backtrackingmechanismavailable
²cautious grounding update:DGBisupdatedimmediately afteruwasproduced(and,
inthecaseofutterances producedbyother DP,understo odandaccepted); however,
backtrackingisavailable
²pessimistic grounding update:DGBisupdatedwhenpositiveevidence ofgrounding
havebeenacquired
3.6 Feedbackandgrounding strategies for IBi S
Intheprevious sections, wediscussed grounding-related ICM(andinparticular feedback)
andgrounding strategies inhuman-humandialogue. Inthissection,wediscussfeedback
andgrounding fromtheperspectiveofdialogue systemsingeneral,and IBi Sinparticular.
7Dialogue Gameboard,i.e.theshared partoftheinformation statein IBi S. See Section 2.2.3.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 99
Most(ifnotall)dialogue systems todayhaveanasymmetrical treatmen tofgrounding,
i.e.thegrounding ofsystemutterances ishandled verydifferentlyfromthegrounding of
userutterances. Typically,thesystemwillprovidefairlyelaboratefeedbackonuserinput,
usuallyintheformofquestions suchas\Didyousayyouwanttogoto Paris?".Theuser
mustthenanswerthesequestions affirmativ elybeforethesystemwillgoon. Thereason
forthis,ofcourse,isthelowqualityofspeechrecognition.
3.6.1 Grounding strategies fordialogue systems
Inthissection,wediscussgrounding updatestrategies fromtheviewpointoftheiruseful-
nessindialogue systems. Thetwomainfactorsdetermining theusefulness ofanupdate
strategy inadialogue systemisusability(including efficiency ofdialogue interaction) and
theefficiency ofinternalprocessing. Onthisview,pessimism hasthedisadvantagethatit
makesdialogue lessefficientsinceeachutterance mustbeexplicitly grounded andaccepted;
foruserutterances thisisoftenachievedbyaskingcheckquestions towhichtheusermust
replybeforecommunication canproceed.
However,thecautiously optimistic approachhasthedisadvantagethatrevisionisnecessary
whengrounding oracceptance fails,whichhappensiftheuserrespondsnegativelytothe
feedback. Thesolution presentedsolvestherevisionproblem bykeepingrelevantpartsof
previous information statesaround.
Acommon methodistousetherecognition scoreofauserutterance todetermine the
feedbackbehaviourfromthesystem,giventhatthesystemhasundersto odtheutterance
sufficiently. Webelievethatthebestsolutionforanexperimentalspeech-to-speechdialogue
systemistoswitchbetweengrounding updatestrategies dependingonthereliabilityof
communication (whichdependsonnoisiness ofenvironmen t,previous ratioofsuccessful vs.
unsuccessful communication, etc).Welinkpessimistic andoptimistic grounding updateto
interrogativ eandpositivefeedback,respectively. Interrogativ efeedbackfromthesystem
raisesaquestion regarding themeaning ofaprevious utterance, whichwouldnotmake
senseifthesystemhadalreadyassumed thatacertainanswertothemeaning question had
beengrounded; ineffect,thiswouldamounttoraisingaquestion whoseansweris(already)
assumed tobepartofthecommon ground. Similarly ,givingpositivefeedbackcorresponds
naturally tothecasewheresomeinterpretation isdeemedtobealreadygrounded.
Amoresophisticated methodfordetermining whatgrounding andfeedbackstrategy to
usewouldalsotakeintoconsideration thedegreeofrelevanceofacertaininterpretation in
thecurrentdialogue context. Ifarecognition hypothesiswhichdoesnothavethehighest
scoreisnevertheless morerelevantthanthehypothesiswiththehighestscore,thiscould
resultinchoosingtheformerhypothesis. Thishasnotbeenimplemen tedin IBi S,andis

100 CHAPTER 3. GROUNDING ISSUES
anareaforfutureresearch.8
3.6.2\Implicit" and\explicit" verification indialogue systems
Intheliterature concerning practical dialogue systems (e.g. San-Segundo etal.,2001),
grounding isoftenreduced toverification ofthesystem's recognition ofuserutterances.
Twocommon waysofhandling verification aredescribedas\explicit" and\implicit" ver-
ification, exemplified in(3.13)(example from San-Segundo etal.,2001).
(3.13)a. Iundersto odyouwanttodepartfrom Madrid. Isthatcor-
rect?[explicit]
b. Youleavefrom Madrid. Whereareyouarriving at?[im-
plicit]
Actually,both\explicit" and\implicit" feedbackcontainaverbatimrepetitionorarefor-
mulationoftheoriginalutterance, andinthissensetheyarebothexplicit. Theactual
baseforthedistinction iswhatwehaveherereferredtoaspolarity:\explicit" verification
isneutral(andeliciting andinterrogativ e)whereas \implicit" verification ispositive.
Giventhatverification isarathermarginal phenomena inhuman-humandialogue, itis
perhapssurprising thatitisoftentheonlyaspectoffeedbackcoveredindialogue systems
literature. Firstly,becauseitisusuallynotnecessary forhumanstoverifywhatthey(think
they)haveheard;thatis,itisaratheruncommon grounding procedureinhuman-human
dialogue. Second,becauseitonlyinvolvespartofthefullspectrumoffeedbackbehaviour,
excluding e.g.acceptance-related feedbackbehaviour.
3.6.3 Issue-based grounding in IBi S
Inthissectionweoutlinea(partially) issue-based accountofgrounding intermsofinfor-
mationstateupdates,inspiredby Ginzburg's accountofcontentquestions andacceptance-
questions. However,wemakesignifican tdepartures from Ginzburg's account,forvarious
reasons.
Abasicideaoftheaccountusedin IBi S2 isthatmeta-issues (thecontentandacceptance
questions) donotalwayshavetoberepresentedexplicitly .However,incertaincasesitis
usefultorepresentgrounding issuesexplicitly .
8Forexample, onecouldassessthedegreeofrelevanceofacertainanswer-movebycheckinghowmany
accommodationsteps(see Chapter 4)wouldbenecessary beforeintegrating thequestion.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 101
Contentquestions in IBi S
Weregardexplicitinterrogativ eunderstanding feedbackasexplicitly raisingcontentques-
tions,whichmayberespondedtoexplicitly orimplicitly .Wealsorefertotheseasunder-
standing questions .Explicit interrogativ efeedbackisveryrelevantfordialogue systems,
wherepoorspeechrecognition oftenmakesitnecessary forthesystemtoexplicitly verify
eachrecognized userutterance, givingtheuserachancetocorrectanymisunderstandings.
Interrogativ efeedbackcaninprinciple bewh-questions (\What doyoumean?"), y/n-
questions (\Doyoumean Paris?",\Paris,isthatcorrect?"), oralternativ equestions (\Do
youmeanto Parisorfrom Paris?").However,wehavechosennegativefeedback(\Idon't
understand") ratherthany/n-questions toindicate lackofunderstanding. Clarification
questions arenotusedin IBi S2;however,theywillbeintroducedin Chapter 4. This
leavesuswithy/nunderstanding questions, whichconcernonespecificinterpretation ofa
previous utterance. Thesearerepresentedin IBi S2 as?und(DP*C)where DPisa DP
and Cisaproposition,andcanbeparaphrased as\Did DPmean C?"or\Is Cacorrect
understanding of DPsutterance?". Inthecasewheretheunderstanding question concerns
aquestion (raisedbyanask-move),theproposition Cisissue(Q)where Qisaquestion.
Inthiscase,theparaphrase canbefurtherspecifiedas\Did DPmeantoraise Q?".
Toallowthis,wehaveextended the IBi Ssemanticpresentedin Chapter 2 toincludetwo
newkindsofpropositions.
²und(DP;P):Propositionwhere P:Propositionand DP:Participan t 9
²issue(Q):Propositionwhere Q:Question 10
Implicitunderstanding-questions Actually,theuseoftheterm\implicit" inthe
contextofgrounding (orverification) canbeusedtodescribenotthegrounding behaviour
itselfbut,rather,thestatusofthegrounding issue. Whatisoftenreferredtoasimplicit
verification canarguably beseenasimplicitly raisingagrounding question, whichmayor
maynotberespondedto.
Thisideawillnotbeimplemen teduntil Chapter 4,sinceitrequiressomeadditional mech-
anismswhichwillbeneededanywayforthekindofbehavioursweintroducethere. Specif-
9Notethatthisdefinition allows Ptoitselfbeapropositionoftheformund(DP;P0);however,we
allowthistopassintheinterestofbrevity.
10Thisdefinition allowsissue(Q)asapropositionevenwhenitisnotembeddedinaproposition
und(DP,issue(Q)).In IBi S,thepropositionissue(Q)onlyappearsinsideunderstanding questions
orasanargumen ttoan ICMmove(see Section 3.6.5).However,in Chapter 4 wewillusethecorrespond-
ingquestion?issue(Q).Asuitableparaphrase ofthisquestion wouldbe\Should Qbecomeanissue?"or
\Should Qbeopenedfordiscussion"; thisissimilarto Ginzburg's MAX-QUD question.

102 CHAPTER 3. GROUNDING ISSUES
ically,weneedadistinction betweenaglobalandalocal QUD(seealso Cooper et al.
(2000)and Cooperand Larsson (2002)), wheretheformercontainsexplicitly raisedor
addressed (butasyetunresolved)issues,andthelattercontainsquestions whichcanbe
usedforresolving shortanswers.
Togiveashortpreview, thebasicideaisthatexplicitpositivefeedbackimplicitly raises
anunderstanding-issue, i.e.whentheimplicitfeedbackisintegrated, theunderstanding
question ispushedonlocal QUD. Thisallowstheusertodiscardthesystem's interpretation
simplybyprovidinganegativeanswertothegrounding question, orconfirmitbygivinga
positiveanswer. Sincethequestion isaddedonlytothelocal QUD,andnottotheglobal
one,itwilleventuallydisappearifitisnotanswered. Thisallowsdialogues toproceed
moreefficiently,sincetheuserdoesnothavetogiveexplicitconfirmations allthetime.
Again,thiswillbeexplained indetailin Chapter 4.
Acceptance questions
In Ginzburg's protocol,a DPwhohasperceivedandinterpreted anutterance isfacedwith
theacceptance-question; whether toacceptthecontentoftheutterance ornot. Ifthe
contentisnotaccepted, the DPshouldpushtheintegratequestion (pushiton QUD)and
addressit.
Onewayofdealingwithacceptance wouldbetofollow Ginzburg's accountandexplicitly
representanacceptance-question whichispushedon QUDincaseswhereauserutterance
isundersto odbutcannotbeintegrated, andsubsequen tlyproduceanutterance addressing
theacceptance question. Weregardfeedback-movesonthereaction level(compliance and
declination moves,in Clark'sterminology) asaddressing acceptance questions. Above,we
havearguedagainstpushing anythingon QUDinthiscasesinceitisasharedstructure,
andtheuserinthiscasehasnochanceofdoingthecorrespondingupdateonherown
QUDuntiltheutterance hasbeenproduced. Soanalternativestrategy wouldbetofirst
producetheutterance addressing theacceptance question andsubsequen tlyassumethat
theuserwillaccommo dateitandpushiton QUD;atthistime,thesystemcandothe
same.
However,itappearsthatitisonlyusefultorepresenttheacceptance question explicitly
on QUDincaseswhereitcangiverisetoadiscussion where DPsargueforandagainst
theacceptance ofaquestion asatopicfordiscussion, orforapropositionasafactor
asatopicfordiscussion. Foradialogue systemunabletoperformsuchargumen tation
dialogues, itappearspointlesstorepresenttheacceptance question explicitly .Sincean
acceptance orrejection movecannotbechallenged, themovewillprovideadefiniteanswer
totheintegration question whichwouldthusbeimmediately removedfrom QUDoncethe
rejection hadbeengrounded.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 103
Forthesereasons, wewillnotrepresentacceptance issuesexplicitly in IBi S. Inasystem
capableofnegotiation and/orargumen tation,however,itwouldbenecessary todoso,and
toregardfeedback-movesontheacceptance levelasrelevantanswerstothisquestion (see
Section 5.8.2 forfurtherdiscussion).
Temporarystorage
Toenablecautious grounding weneedsomewayofrevisingthedialogue gameboardwhen
optimistic grounding assumptions turnouttobepremature, withouthavingtodealwith
theproblems ofgeneralized beliefrevision Göardenfors (1988).Astraightforwardwayof
doingthisistokeeparoundrelevantpartsofprevious dialogue gameboardstates,and
copythecontentsofthesebacktothe DGBwhennecessary .Thisstrategy willbeusedfor
systemutterances in IBi S2,andalsoforuserutterances in IBi S3.
3.6.4 Enhancing theinformation statetohandlefeedback
Inthissection,weshowhowthe IBi Sinformation stateneedstobemodifiedtohandle
grounding andfeedback. Thenewinformation statetypeisshownin Figure 3.1.
2
66666666666666666666666664 private:2
66666666666664 agenda:Open Queue(Action)
plan :Open Stack(Plan Construct)
bel :Set(Prop)
tmp :2
6664 com :set(Prop)
qud :Open Stack(Question)
agenda:Stack(Action)
plan :Stack(Plan Construct)3
7775
nim :Open Queue(Mo ve)3
77777777777775
shared :2
6666664 com:Set(Prop)
qud:Open Stack(Question)
pm:Open Queue(Mo ve)
lu:"
speaker :Participan t
move:Set(Move)#3
77777753
77777777777777777777777775
Figure 3.1:IBi S2Information Statetype

104 CHAPTER 3. GROUNDING ISSUES
Temporarystore
Toenablethesystemtobacktrackifanoptimistic assumption turnsouttobemistaken,
relevantpartsoftheinformation stateiskeptin/private/tmp. Thequdandcomfields
maychangewhenintegrating anaskoranswermove,respectively. Theplanmayalsobe
modified,e.g.ifaraiseactionisselected. Finally,ifanyactionsareontheagendawhen
selection starts(whichmeanstheywereputthereduringbytheupdatemodule),these
mayhavebeenremovedduringthemoveselection process.
Non-integratedmoves
Sinceseveralmovescanbeperformed perturn,IBi Sneedssomewayofkeepingtrackof
whichmoveshavebeeninterpreted. Thisisdonebyputtingallmovesinlatestmoves
inaqueuestructure callednim,for Non-Integrated Moves. Thisstructure isprivate,since
itisaninternalmatterforthesystemhowmanymoveshavebeenintegrated sofar. Once
amoveisassumed tobegrounded ontheunderstanding levelthemoveisaddedtothe
/shared/lu/mo vesset. Sincethemovehasnowbeenundersto odonthepragmatic
level,thecontentofthemovewillbeaquestion orafullproposition(forshortanswers,
thepropositionresulting fromcombiningitwithaquestion on QUD).
Previousmoves
Tobeabletodetectirrelevantfollowups,IBi Sneedstoknowwhatmoveswereperformed
(andgrounded) intheprevious utterance. Thesearestoredinthe/shared/pm field.
Timeout
Tobeabletodecidewhentheuserhasgivenupherturn,wehaveaddeda TISvariable
timeout oftype Real,whosevalueisthetime(inseconds) afterwhichthesystemwill
assumethattheturnhasbeengivenupifnospeechhasbeendetected. Thisvariablewill
befurtherdiscussed in Section 3.6.6.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 105
3.6.5 Feedbackandsequencing dialogue moves
Inthissection,wefirstshowhowfeedbackdialogue movesin IBi S2 arerepresented. We
thenreviewthefullrangeoffeedbackmoves,startingwithsystem-generated feedbackand
thenmovingontouserfeedback.
Thegeneralnotation for ICMdialogue movesusedin IBi Sisthefollowing:
(3.14)icm:L*Pf:Argsg
where Lisanactionlevel,Pisapolarity,and Argsareargumen ts.
²L:actionlevel
{con:contact(\Areyouthere?")
{per:perception (\Ididn'thearanythingfromyou",\Iheardyousay'to Paris"')
{sem:semanticunderstanding (\Idon'tunderstand", \To Paris.")
{und:pragmatic understanding (\Idon'tquiteunderstand", \Youwanttoknow
aboutprice.")
{acc:acceptance/reaction (\Sorry,Ican'tanswerquestions aboutconnecting
flights",\Okay.")
²P:polarity
{neg:negative
{int:interrogativ e
{pos:positive
²Args:argumen ts
Notethatthe\neutral" polarityhasbeenreplaced bythelabel\int";wehavemadea
simplifying assumption thatneutralfeedbackisalwayseliciting andinterrogativ e.11
Theargumen tsaredifferentaspectsoftheutterance ormovewhichisbeinggrounded,
dependingactionlevel:
11Note,however,thatifwehadincluded feedbackformslike\Whatdidyousay?",thiswouldstill
beregarded asnegativefeedback. The\int"labelonlyreferstocheck-questions, whichareusually y/n-
questions. Thisisarguably notanoptimallabellingconvention.

106 CHAPTER 3. GROUNDING ISSUES
²forper-level:String,therecognized string
²forsem-level:Move,amoveinterpreted fromtheutterance
²forund-level:DP¤P,where
{DP:Participan tisthe DPwhoperformed theutterance
{C:Propositionisthepropositional contentoftheutterance
²foracc-level:C:Proposition,thecontentoftheutterance
Forexample, the ICMmoveicm:und*p os:usr*dest city(paris)providespositivefeedbackre-
gardingauserutterance thathasbeenundersto odasmeaning thattheuserwantstogo
to Paris.
Inaddition, sequencing ICMmovesforindicating reraising ofissuesandloadingaplanare
included:
²icm:reraise :indicate reraising implicitly (\So,...")
²icm:reraise: Q:reraising anissue Qexplicitly (\Returning totheissueof Price.")
²icm:loadplan (\Let'ssee.")
Systemfeedbacktouserutterances in IBi S2
Inthissectionandthefollowingsection,wereviewsurfaceformsrelatedtofeedbackand
other ICMbehaviourthatwillbeimplemen tedin IBi S2.
Foruserutterances, IBi S2 willbeabletoproducee.g.thefollowingkindsoffeedback
utterances (fortheexamples, assumethattheuserjustsaid\Iwanttogoto Paris"):
²contact
{negative;icm:con*neg (\Ididn'thearanythingfromyou")
²perception
{negative;icm:per*negrealizedasfb-phrase (\Pardon?", \Ididn'thearwhatyou
said.")

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 107
{positive;icm:per*pos:Stringrealizedasmetalevelverbatimrepetition(\Iheard
`toparis'")
²understanding (semantic)
{negative;icm:sem*neg realizedasfb-phrase (\Idon'tunderstand.")
{positive;icm:sem*p os:Contentrealized asrepetition/reform ulationofcontent
(object-level)(\Paris.")
²understanding (pragmatic)
{negative;icm:und*neg realizedasfb-phrase (\Idon'tquiteunderstand.")
{positive;icm:und*p os:DP*Contentrealizedasrepetition/reform ulationofcon-
tent(object-level)(\To Paris.")
{interrogativ e;icm:und*int: DP*Contentrealizedasaskaboutinterpretation (\To
Paris,isthatcorrect?")
²integration
{negative
¤proposition-rejection; icm:acc*neg: Contentrealizedasexplanation (\Sorry,
Parisisnotavaliddestination city")
{positive;icm:acc*p osrealizedasfb-word(\Okay")
Inaddition, IBi S2 willbeabletoperformissue-rejection usingthemoveicm:acc*neg:issue( Q),
where Q:Question asillustrated in(dialogue 3.2).
(dialogue 3.2)
U>Whataboutconnecting flights?
S>Sorry,Icannotanswerquestions aboutconnecting flights.
Wearenotclaiming thathumansalwaysmakethesedistinctions betweenactionexplicitly
orevenconsciously ,northatthelinkbetweensurfaceformandfeedbacktypeisasimple
one-to-one correspondence; forexample, \mm"maybeusedaspositivefeedbackonthe
perception, understanding, andacceptance levels. Feedbackis,simply,oftenambiguous.
However,since IBi Sismakingallthesedistinctions internally wemightaswelltryto
producefeedbackwhichisnotsoambiguous. Ofcourse,thereisalsoatradeoffinrelation
tobrevity;extremely explicitfeedback(e.g.\Iundersto odthatyoureferred to Paris,
but Idon'tseehowthatisrelevantrightnow.")couldbeirritating andmightdecrease
theefficiency ofthedialogue. Wefeelthatthecurrentchoicesofsurfaceformsarefairly

108 CHAPTER 3. GROUNDING ISSUES
reasonable, buttestingandevaluation onrealuserswouldbeneededtofindthebestways
toformulatefeedbackondifferentlevels. Thisisanareaforfutureresearch.
Ageneralstrategy usedby IBi Sin ICMselection isthatifnegativeorinterrogativ efeed-
backonsomelevelisprovided,thesystemshouldalsoprovidepositivefeedbackonthe
levelbelow. Forexample, ifthesystemproducesnegativefeedbackonthepragmatic un-
derstanding level,itshouldalsoproducepositivefeedbackonthesemanticunderstanding
level.
(3.15)S>Paris. Idon'tunderstand.
Insomesystems, positiveorinterrogativ efeedbacktouserutterances isnotgivenimme-
diately;instead,thesystemrepeatsalltheinformation ithasreceivedjustbeforemaking
adatabase queryandaskstheuserifitiscorrect. Itisalsopossibletocombinefeedback
aftereachutterance withafinalconfirmation. In IBi S2,wehavenotimplemen tedfinal
confirmations. Itcanbearguedthatfinalconfirmations aremoreimportantinaction-
orienteddialogue (see Chapter 5),whereas theyarenotsoimportantininquiry-oriented
dialogue sincetheyneverresultinanyactionsotherthandatabase searches.
Userfeedbacktosystemutterances in IBi S2
Forsystemutterances, IBi S2 willreactappropriately tothefollowingtypesofuserfeed-
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
behaviour. Themainmotivationforthisisthatsystemutterances arelesslikelytobe
problematic fortheusertointerpretthanviceversa.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 109
Still,theavailablecoverageallowssomeusefulfeedback-phrases, including negativeper-
ceptionfeedbackwhichisusefuliftheoutputfromthesystem's speechsynthesizerisof
poorquality. Ideally,thiswouldprovideaslightreformulationbythesystem,butsince
generation isnotamaintopichere,thishasnotbeenimplemen ted.
Understanding-levelfeedbackhasnotbeenincluded butmaybeusefulincaseswherethe
userhearsthesystembutcannotunderstand themeaning ofthewordsutteredbythe
system. Inthiscase,areformulationbythesystemmayagainbeuseful.
3.6.6 Grounding ofuserutterances in IBi S2
Inthissectionweshowhowoptimistic andpessimistic grounding ofuserutterances has
beenintegrated in IBi S2. Firstweshowhowgrounding strategies aredynamically selected
dependingonrecognition score,inthecasewhereamovehasbeenfullyundersto odand
accepted. Next,weshowhowtodealwithsystemresponsestointerrogativ efeedback
associatedwithpessimistic grounding. Finally,weshowhowthesystemdealswithfailure
toperceive,understand, andintegrateuserutterances bygivingnegativefeedbackonthe
appropriate actionlevel.
Dynamic selectionofgrounding strategies forusermoves
Foruserutterances, IBi S2 usesoptimistic orpessimistic grounding strategies basedonthe
recognition scoreandthedialogue movetype. Thismakesthecorrespondingintegration
rulesmorecomplex thantheonesin IBi S1. Foruser\core"moves(in IBi S2,askand
answer),theintegration strategy dependsontherecognition scorefortheutterance in
question. Thischoiceisdetermined bytworecognition thresholds, T1 and T2,where
T1>T2. Iftherecognition scoreishigherthan T2,anoptimistic strategy ischosen;
positiveacceptance feedback(\OK")isselected, andifthescoreislowerthan T1 positive
understanding feedback(\To Paris.")isalsoselected.
Ifthescoreislowerthan T2,themoveisnotintegrated andintheselection phasea
pessimistic strategy involvinginterrogativ eunderstanding feedback(e.g.\To Paris,isthat
correct?") isselected(see Section 3.6.6).
Ofcourse,theideaofusingrecognition scorefordetermining whether andhowtoconfirm
userutterances isnotnew(seee.g. San-Segundo etal.,2001),andmoresophisticated
decision proceduresarecertainly possible. Weuseitheretoshowhow IBi S2 enables
flexiblechoicebothoffeedbacktypeandofgrounding updatestrategy.

110 CHAPTER 3. GROUNDING ISSUES
Inaddition tobeingcheckedforrelevance,contentfulmovesarecheckedforintegratabilit y
(acceptabilit y)andiftheseconditions arenotfulfilledthemovewillnotbeintegrated;
instead,itwillgiverisetonegativeacceptance feedbackasexplained in Section 3.6.6.
Integration ofuseraskmove Theintegration ruleforuseraskmoveimplemen tingthe
optimistic grounding strategy isshownin(rule 3.1).
(rule 3.1)rule:integrate Usr Ask
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
>>>>>>>>>>>>>>>:1 pop(/private/nim)
2 push(/ private/agenda,icm:acc*p os)
3 add(/shared/lu/moves,ask(Q))
4 ifdo(Score·0.9,
push(/ private/agenda,icm:und*p os:usr*issue(Q)))
5 ifdo(in($/ shared/qud,Q)andnotfst($/shared/qud,Q),
push(/ private/agenda,icm:reraise: Q))
6 push(/ shared/qud,Q)
7 push(/ private/agenda,respond(Q))
Thefirsttwoconditions picksoutauseraskmoveonnim. Thethirdandfourthcon-
ditionschecktherecognition scoreoftheutterance andifitishigherthan 0.7(T2),the
ruleproceedstocheckforacceptabilit y. Ifthescoreistoolow,themoveshouldnotbe
optimistically integrated; instead,apessimistic grounding strategy shouldbeappliedand
interrogativ efeedbackselected(seebelow).
Thefifthcondition checksforacceptabilit y,i.e.thatthesystemisabletodealwiththis
question, i.e.thatthereisacorrespondingplaninthedomainresource. Ifnot,the
integration rulewillnottriggerandtheaskmovewillremainonnimuntiltheselection
phase,whereitwillgiverisetoanissuerejection (see Section 3.6.6).
Thefirstupdatepopstheintegrated moveoffnim. Inupdate 2,positiveintegration
feedbackisaddedtotheagenda,toindicate thatthesystemcanintegratetheask-move.
Update 3 addsthemoveto/shared/lu/mo ves,therebyreflecting theoptimistic ground-
ingassumption ontheunderstanding level. Inupdate 4,positiveunderstanding feedback
isselectedunlessthescoreishigherthan 0.9(T1).

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 111
Update 5 checksifthisquestion isalreadyon QUD;ifso,thesystemselectssequencing
feedbacktoshowthatithasundersto odthattheuserisreraising anopenissue.(Ifthe
question isalreadyontopof QUD,however,itisnotseenasacaseofreraising.) See
Section 3.6.9 formorecasesofreraising. Update 6 pushes Qon QUD;notthatif Qwas
alreadyon QUDbutnottopmost, pushingitwillbeequivalenttoraisingittothetopmost
position. Thisisapropertyofthe Open Stackdatatype(see Section A.2.1).
Update 7 pushestheactiontorespondto Qontheagenda. Thiscanberegarded asa
shortcut forreasoning aboutobligations andintentions;whenaccepting auserquestion,
thusaccepting theobligation totrytorespondtoit,thesystemwillautomatically intend
torespondtoit.
Default ICMmoveselection rule Theroleofthe ICMmoveselection rulesisto
addmovestobegenerated tothenextmoves TISvariablebasedonthecontentsof
theagenda. ICMwhichisaddedtotheagendabytheupdatemodulewillbemovedto
nextmovesbythedefault ICMselection rule(rule 3.2).
(rule 3.2)rule:select Icm Other
class:selecticm
pre:(
in($/private/agenda,icm:A)
notin($nextmoves,B)and B=ask(C)
eff:(
push(nextmoves,icm:A)
del(/private/agenda,icm:A)
Dialogueexample: integrating userask-move Thedialogue belowshowshowauser
askmovewithascoreof 0.76 issuccessfully integrated, andpositiveunderstanding and
acceptance feedbackisproduced.
(dialogue 3.3)
S>Welcome tothetravelagency!
U>priceinformation please[0.76]
get Latest Mo ves 8
>><
>>:set(/private/nim,oqueue([ask(? A.price(A))]))
set(/shared/lu/speaker ,usr)
clear(/ shared/lu/moves)
set(/shared/pm,set([greet]) )
integrate Usr Ask

112 CHAPTER 3. GROUNDING ISSUES
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
find Plan
2
6666666666664 private=2
664 agenda=**icm:acc*p os
icm:und*p os:usr*issue(?A.price(A))
icm:loadplan++
nim =hhii 3
775
shared =2
66664 com=fg
qud=­
?A.price(A)ff
pm=©greetª
lu=·speaker =usr
moves =©
ask(?A.price(A))ª¸3
777753
7777777777775
backup Shared
select From Plan
select Icm Other½
push(nextmoves,icm:acc*p os)
del(/private/agenda,icm:acc*p os)
select Icm Other½push(nextmoves,icm:und*p os:usr*issue(?A.price(A)))
del(/private/agenda,icm:und*p os:usr*issue(?A.price(A)))
select Icm Other
select Ask
S>Okay. Youwanttoknowaboutprice. Letssee. Howdoyouwantto
travel?
Interrogativ eunderstanding feedbackforuseraskmove Ifauseraskmovecannot
beassumed tobeundersto odbecauseofalowrecognition score,interrogativ efeedbackon
theunderstanding levelisselectedby(rule 3.3).
(rule 3.3)rule:select Icm Und In t Ask
class:selecticm
pre:8
><
>:$/shared/lu/speaker ==usr
fst($/private/nim,ask(Q))
$score·0.7
eff:(
pop(/private/nim)
push(nextmoves,icm:und*int:usr *issue(Q))

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 113
Theconditions arestraightforward. Thefirstupdateremovesthemovefromnim,even
thoughithasnotbeenintegrated. Analternativ eapproachwouldbetokeepthismove
onnimandexplicitly representthegrounding asconcerning thismove. However,this
wouldrequirelabellingallmoveswithuniquemove IDs;instead, wefollowthegeneral
philosoph yof IBi Softryingtokeepourrepresentationassimpleaspossibleaslongas
itworks. Theinterrogativ efeedbackselected inthesecondupdatewill,inasense,take
overthefunction oftheoriginalmove;ifthefeedbackisansweredpositively,theendresult
willbethesameasiftheaskmovehadbeenintegrated immediately (see Section 3.6.6 for
furtherexplanation).
Integration ofuseranswermove Theintegration ruleforuseranswermoves,shownin
(rule 3.4)issimilartothatforaskmoves,exceptthatanswersarecheckedforrelevance
aswellasreliabilityandacceptabilit y.
(rule 3.4)rule:integrate Usr Answ er
class:integrate
pre:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:1 fst($/private/nim,answer(A))
2$/shared/lu/speaker ==usr
3!$score=Score
4Score>0.7
5 fst($/shared/qud,Q)
6$domain ::relevant(A,Q)
7$domain ::combine(Q,A,P)
8$database::valid DBparameter( P)or P=not(X)
eff:8
>>>>>>>><
>>>>>>>>:1 pop(/private/nim)
2 add(/shared/lu/moves,answer(P))
3 push(/ private/agenda,icm:acc*p os)
4 ifdo(Score·0.9 and A6=yesand A6=no,
push(/ private/agenda,icm:und*p os:usr*P))
5 add(/shared/com,P)
Conditions 1-4 aresimilartothosefortheintegrate Usr Ask rule. Therelevanceofthe
contentoftheanswertoaquestion on QUDischeckedincondition 6.
Theacceptabilit ycondition inthecondition 8 makessurethatthepropositional content
resulting fromcombiningthequestion topmost on QUDwiththecontentoftheanswer-
moveiseither
²avaliddatabase parameter, or
²anegatedproposition

114 CHAPTER 3. GROUNDING ISSUES
Negated propositionscanalwaysbeintegrated (aslongastheyarerelevant);forexample,
itisokaytosaythatyoudonotwanttogoto Paris,evenif Parisisnotinthedatabase.
Updates 1-3 againcorrespondcloselytothoseinintegrate Usr Ask .Update 4 checksif
thescorewaslowerthanorequalto 0.9;ifso,apositiveunderstanding feedbackmoveis
selected. Ifthescoreishigherthan 0.9 oriftheanswerisyesorno,nounderstanding
feedbackisproduced. Thespecialspecialstatusof\yes"and\no"buildsontheassumption
thattheseareeasilyrecognized; ifthisisnotthecase,theirspecialstatusshouldbe
removed. Finally,update 5 addsthepropositionresulting fromcombiningthequestion on
QUDwiththecontentoftheanswermovetothesharedcommitmen ts.
Interrogativ eunderstanding feedbackforuseraskmove Ifauseraskmovereceives
alowscore(lowerthan T2,whichisheresetto 0.7)andthequestion raisedbythemoveis
acceptable tothesystem,interrogativ eunderstanding feedbackisselectedby(rule 3.5).
(Ifthequestion isnotacceptable itwillinsteadberejected; see Section 3.6.6).
(rule 3.5)rule:select Icm Und In t Answer
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
toandcombineswithaquestion on QUD,andthattherecognition scorewaslessthanor
equalto 0.7. Iftheseconditions aretrue,themoveispoppedoffnimandinterrogativ e
understanding feedbackisselected.
Integrating andrespondingtointerrogativ efeedback
Integrating interrogativ eunderstanding feedback Asexplained in Section 3.6.3,
Interrogativ efeedbackraisesunderstanding questions. Thisisreflected in(rule 3.6).

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 115
(rule 3.6)rule:integrate Und In t ICM
class:integrate
pre:n
fst($/private/nim,icm:und*int: DP*C)
eff:8
><
>:pop(/private/nim)
add(/shared/lu/moves,icm:und*int: DP*C)
push(/ shared/qud,und(DP*C))
Thecondition simplychecksthatthereisanicm:und*int: DP*Cmoveonnim,whichis
thenpoppedoffbythefirstupdateandaddedto/shared/lu/mo vesbythesecond
update. Thethirdupdatepushestheunderstanding question?und(DP*C)on QUD.
Integrating positiveanswertounderstanding-question Whenthesystemraises
anunderstanding question (e.g.bysaying\To Paris,isthatcorrect?"), theusercaneither
say\yes"or\no".(Thecasewheretheuserdoesnotgivearelevantanswertotheinter-
rogativefeedbackistreatedin Section 3.6.8).In IBi S2,wedonotrepresentpropositions
relatedtotheunderstanding ofutterances inthesamewayasotherpropositions(which
arestoredin/shared/com ).Therefore, specialrulesareneededfordealingwithanswers
tounderstanding-questions.
Theruleforintegrating anegativeanswertoanunderstanding-question isshownin(rule
3.7).
(rule 3.7)rule:integrate Neg Icm Answ er
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
question on QUD. Thefirstthreeupdatesestablish themoveassharedandpopthe
understanding-question off QUD. Finally,positivefeedbackisselected toindicate that
thesystemhasundersto odthattheassumed interpretation Cwasincorrect.
Integrating positiveanswertounderstanding question Theruleforintegrating a
positiveanswertoanunderstanding-question isshownin(rule 3.8).

116 CHAPTER 3. GROUNDING ISSUES
(rule 3.8)rule:integrate Pos Icm Answ er
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
Theconditions andthefirstthreeupdatesaresimilartothoseintheintegrate Neg Ic-
m Answerrule. Thefinal(conditionalized) updateintegrates thecontent C. Ifthe\orig-
inal"move(themovewhichcausedtheinterrogativ efeedbacktobeproducedinthefirst
place)wasask,Cwillbeapropositionissue(Q).Consequen tly,integrating thispropo-
sitionshasthesameeffectsasintegrating anask-move:pushing thequestion Qon QUD
andpushingtheactionrespond(Q)ontheagenda. Ifthepropositionisnotofthistype,it
issimplyaddedto/shared/com .
Dialogueexample: positiveandnegativeresponsetointerrogativ efeedback In
thefollowingdialogue, thesystemproducesinterrogativ eunderstanding feedbackfortwo
userutterances, onecontaininganaskmoveandtheothercontainingananswermove. The
firstinterrogativ efeedbackisansweredpositivelyandthesecondnegatively.
(dialogue 3.4)
U>priceinformation please[0.65]
get Latest Mo ves 2
666666664 private=2
4 agenda=hhii
plan =hi
nim =­­
ask(?A.price(A))ffff 3
5
shared =2
664 com=fg
qud=hi
lu=·
speaker =usr
moves =fg¸3
7753
777777775
backup Shared
select Icm Und In t Ask ½
pop(/private/nim)
push(/ private/agenda,icm:und*int:usr *issue(?A.price(A)))

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 117
select Icm Other½push(nextmoves,icm:und*int:usr *issue(?A.price(A)))
del(/private/agenda,icm:und*int:usr *issue(?A.price(A)))
S>Youwanttoknowaboutprice,isthatcorrect?
get Latest Mo ves
integrate Und In t ICM8
<
:pop(/private/nim)
add(/shared/lu/moves,icm:und*int:usr *issue(?A.price(A)))
push(/ shared/qud,und(usr*issue(?A.price(A))))
2
666666664 private=2
4 agenda=hhii
plan =hi
nim =hhii 3
5
shared =2
664 com=fg
qud=­
und(usr*issue(?A.price(A)))ff
lu=·speaker =sys
moves =©
icm:und*int:usr *issue(?A.price(A))ª¸3
7753
777777775
U>yes
get Latest Mo ves
integrate Pos Icm Answ er 8
>>>>>>>><
>>>>>>>>:pop(/private/nim)
add(/shared/lu/moves,answer(und(usr *issue(?A.price(A)))))
pop(/shared/qud)
ifthenelse(issue(?A.price(A))=issue(B),[
push(/ shared/qud,B)
push(/ private/agenda,respond(B))],
add(/shared/com,issue(?A.price(A))))
find Plan
2
666666666666666666664 private=2
6666666666664 agenda=­­
icm:loadplanffff
plan =*findout(?A.how(A))
findout(?B.destcity(B))
findout(?C.deptcity(C))
findout(?D.month(D))
findout(?E.deptday(E))
findout(?F.class(F))
consult DB(? G.price(G))+
nim =hhii 3
7777777777775
shared =2
664 com=fg
qud=­?H.price(H)ff
lu=·speaker =usr
moves =©
answer(und(usr *issue(?H.price(H))))ª¸3
7753
777777777777777777775
backup Shared
select From Plan

118 CHAPTER 3. GROUNDING ISSUES
select Icm Other
select Ask
S>Letssee. Howdoyouwanttotravel?
get Latest Mo ves
integrate Other ICM
integrate Sys Ask
U>byplane[0.56](useractuallysaid\bytrain")
get Latest Mo ves
backup Shared
select Icm Und In t Answer ½pop(/private/nim)
push(/ private/agenda,icm:und*int:usr *how(plane))
select Icm Other
S>byflight,isthatcorrect?
get Latest Mo ves
integrate Und In t ICM8
<
:pop(/private/nim)
add(/shared/lu/moves,icm:und*int:usr *how(plane))
push(/ shared/qud,und(usr*how(plane)) )
2
6666666666666666666666664 private=2
6666666666664 agenda=hhii
plan =*findout(?A.how(A))
findout(?B.destcity(B))
findout(?C.deptcity(C))
findout(?D.month(D))
findout(?E.deptday(E))
findout(?F.class(F))
consult DB(? G.price(G))+
nim =hhii 3
7777777777775
shared =2
6666664 com=fg
qud=*und(usr*how(plane))
?H.how(H)
?I.price(I)+
lu=·speaker =sys
moves =©
icm:und*int:usr *how(plane)ª¸3
77777753
7777777777777777777777775
U>no
get Latest Mo ves
integrate Neg Icm Answ er

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 119
8
>><
>>:pop(/private/nim)
add(/shared/lu/moves,answer(und(usr *how(plane))) )
pop(/shared/qud)
push(/ private/agenda,icm:und*p os:usr*not(how(plane)) )
2
66666666666666666666664 private=2
6666666666664 agenda=­­icm:und*p os:usr*not(how(plane))ffff
plan =*findout(?A.how(A))
findout(?B.destcity(B))
findout(?C.deptcity(C))
findout(?D.month(D))
findout(?E.deptday(E))
findout(?F.class(F))
consult DB(? G.price(G))+
nim =hhii 3
7777777777775
shared =2
66664 com=fg
qud=¿
?H.how(H)
?I.price(I)À
lu=·speaker =usr
moves =©answer(und(usr *how(plane)))ª¸3
777753
77777777777777777777775
backup Shared
reraise Issue
select Icm Other½
push(nextmoves,icm:und*p os:usr*not(how(plane)) )
del(/private/agenda,icm:und*p os:usr*not(how(plane)) )
select Icm Other
select Ask
S>notbyflight. So,Howdoyouwanttotravel?
Negativecontactandperception levelfeedback
Whathappensifnosystemutterance isdetected, orifthespeechrecognizer fails?Most
speechrecognizers cantellthedifference betweennothearinganythingatall,andhearing
something butnotbeingabletocomeupwithanyhypothesisregarding whatwassaid. We
willusethisdistinction toenable IBi Stoproducefeedbackonthecontactandperception
levels.
If IBi Sdoesnotreceiveanyinputwithinacertaintime-frame (specifiedbythetimeout
TISvariable), itwillproducefeedbackindicating thatnothingwasperceived,e.g.\Ididn't
hearanythingfromyou.".Weclassifythisasnegativefeedbackonthecontactlevel. It
couldperhapsbearguedthatthedistinction betweencontactandperception levelfeedback
isnotverysharp,andthatthiskindoffeedbackactually concerns theperception level.
However,itispossiblethatthereasonthatnothingwasregistered bytherecognizer was
afailuretoestablish achannelofcommunication fromtheusertothesystem,e.g.ifa

120 CHAPTER 3. GROUNDING ISSUES
microphone isbrokenornotpluggedinproperly.
Ifsomething isdetected bythespeechrecognizer butitwasnotabletocomeupwitha
goodenoughguessaboutwhatwassaid,thesystemwillproducenegativefeedbackonthe
perception level,e.g.\Ididn'thearwhatyousaid.".
Wehaveconfigured theinputmoduletosettheinputvariableto`TIMEDOUT'ifnothing
isdetected, andto`FAIL'ifsomething unrecognizable wasdetected.
Negativesystemcontactfeedback Ifthespeechrecognizer doesnotgetanyinput
withinacertaintimeframe(specifiedbythetimeout TISvariable), theinputvariable
willbesetto`TIMEDOUT'bytheinputmodule. Theruleforselection ofnegativecontact
feedbackisshownin(rule 3.9).
(rule 3.9)rule:select Icm Con Neg
class:selecticm
pre:8
><
>:$input=`TIMEDOUT'
isempty($nextmoves)
isempty($/private/agenda)
eff:n
push(nextmoves,icm:con*neg )
Unlessthesystemhassomething elsetodo,thiswilltriggernegativecontact ICMbythe
system,realisede.g.as\Ididn'thearanythingfromyou.".Thepurposeofthisisprimarily
toindicate totheuserthatnothingwasheard,butperhapsalsotoelicitsomeresponse
fromtheusertoshowthatsheisstillthere. Admittedly ,thisisaratherundeveloped
aspectof ICMinthecurrent IBi Simplementation,andalternativestrategies couldbe
explored. Forexample, thesystemcouldincrease thetimeoutspansuccessivelyinsteadof
repeatingnegativecontact ICMeveryfiveseconds. Otherformulationswithmorefocuson
theeliciting function couldalsobeconsidered, e.g.\Areyouthere?"orsimply\Hello?".
Thesecondandthirdcondition checkthatnothingisontheagendaorinnextmoves.
Themotivationforthisisthatthereisnoreasontoaddresscontactexplicitly inthiscase,
sinceanyutterance fromthesystemimplicitly triestoestablish contact.
Default ICMintegration rule Sincecontactisnotexplicitly representedintheinfor-
mationstateproper,integration ofnegativesystemcontact ICMmoveshavenospecific
effectontheinformation state,andaretherefore integrated bythedefault ICMintegration
ruleshownin(rule 3.10).Unlessan ICMmovehasaspecificintegration ruledefinedfor
it,itwillbeintegrated bythisrule.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 121
(rule 3.10) rule:integrate Other ICM
class:integrate
pre:n
fst($/private/nim,icm:A)
eff:(
pop(/private/nim)
add(/shared/lu/moves,icm:A)
Thecondition andupdatesinthisrulearestraightforward.
Negativesystemperception feedback Ifthespeechrecognizer getssomeinputfrom
theuserbutisnotabletoreliablyfigureoutwhatwassaid(therecognition scoremaybe
toolow),theinputvariablegetssetto`FAIL'.Thiswilltriggernegativeperception ICM,
e.g.\Ididn'thearwhatyousaid".
(rule 3.11) rule:select Icm P er Neg
class:selecticm
pre:(
$input='FAIL'
notin($nextmoves,icm:per*neg)
eff:n
push(nextmoves,icm:per*neg)
Thepurposeofthesecondcondition istopreventselecting negativeperception feedback
morethanonceintheselection phase. Aswithnegativesystemcontactfeedback,negative
systemperception feedbackisintegrated bytheintegrate Other ICM rule.
Negativeunderstanding levelfeedback
Negativefeedbackcanconcerneitherofthetwosublevelsoftheunderstanding level:se-
manticandpragmatic understanding.
Negativesystemsemanticunderstanding feedback Ifsomeinputisrecognized
bytherecognition module,theinterpretation modulewilltrytofindaninterpretation
oftheinput. Ifthisfails,thelatestmovesgetssettofailedwhichtriggersselection
ofnegativesemanticunderstanding feedback(e.g.\Idon'tunderstand"). Inaddition,
positiveperception feedback(e.g.\Iheard`perish'")isproducedtoindicate totheuser
whatthesystemthoughtshesaid.

122 CHAPTER 3. GROUNDING ISSUES
Thiswillonlyoccuriftherecognition lexiconcoverssentencesnotcoveredbytheinter-
pretation lexicon.
(rule 3.12) rule:select Icm Sem Neg
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
frombeingselected morethanonetime. Sinceonlyonestringisrecognized perturn,
thereisneveranyreasontoapplytherulemorethanonce;andifanythingatallcanbe
interpreted, therulewillnottriggeratallevenifsomematerial wasnotusedininterpreta-
tion. Inasystemwithawide-coveragerecognizer andamoresophisticated interpretation
module,onemayconsider producingnegativesemanticunderstanding feedbackforany
material whichcannotbeinterpreted (e.g.\Iunderstand thatyouwanttogoto Paris,
but Idon'tunderstand whatyoumeanby`Londres'.").
Thefirstupdateinthisruleselectspositiveperception ICMtoshowtheuserwhatthe
systemheard. Thesecondupdateselectsnegativesemanticunderstanding ICM.
Negativesystempragmatic understanding feedback Thesystemwilltrytointe-
gratethemovesaccording totherulesabovein Section 3.6.7. Ifthisfails(iftherearestill
moveswhichhavenotbeenintegrated), therulein(rule 3.13)willbetriggered anda
icm:und*neg -movewillbeselectedbythesystem. However,ifthereasonthatthemovewas
notintegrated isthatithadalowscoreorwasnotacceptable tothesystem,interrogativ e
understanding feedback(Section 3.6.6)ornegativeacceptance feedback(Section 3.6.6),
respectively,willinsteadbeselectedandthemovewillbepoppedoffnimbeforetherule
in(rule 3.13)istried.
In IBi S,onlyask-movescanbeirrelevant. Othermoves,including ask,donothaveany
relevancerequirements. Thismeansthatanswermovesaretheonlymovesthatcanfail
tobeundersto odonthepragmatic level,giventhattheyhavebeenundersto odonthe
semanticlevel. Also,foranutterance tobecompletely irrelevant,nopartofitmusthave
beenintegrated. Forthesereasons, therulein(rule 3.13)willtriggeronlyifnomove
inthelatestutterance wasintegrated, andtheutterance wasinterpreted ascontainingat
leastoneanswer-move.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 123
(rule 3.13) rule:select Icm Und Neg
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
Thefirstrulechecksthatnegativepragmatic understanding feedbackhasnotalreadybeen
selected. Thesecondcondition checksthatthelatestutterance containedananswermove,
andthethirdchecksthatnoneofthemovesperformed inthelatestutterance hasbeen
integrated; allmovesinlatestmovesarestillonnim. Finally,thefourthcondition
checksthatnoanswerisrelevanttoanyquestion on QUD.
Thefirstupdateselectspositivefeedbackonthesemanticunderstanding levelforeachmove
performed inthelatestutterance, toshowthattheutterance wasatleastundersto odto
someextent. Thesecondupdateselectsnegativefeedbackandpushesitonnextmoves.
Thesystemisthusabletomakeadistinction betweenutterances itcannotinterpret(and
thusnotground), andutterances thatitcaninterpretandgroundbutnotintegrate. The
rulein(3.15)triggerswhenintegration failsbecausethesystemcannotseetherelevance
oftheuserutterance inthecurrentdialogue context. Negativepragmatic understanding
feedbackiscurrentlyrealizedas\Idon'tquiteunderstand"; theideaistoindicate that
theutterance wasalmostfullyundersto od,butnotquite. Again,itcanbearguedwhat
thebestrealization is.
Dialogue example: negativesystemcontact,perception, andunderstanding
feedback Inthisdialogue, weseeexamples ofnegativesystemfeedbackonthecontact,
perception, andunderstanding (bothsemanticandpragmatic) levels.(Sincethisdialogue
usesthetext-based inputmodule,wehavesimulatedtimeoutandrecognition failure.)
(dialogue 3.5)
S>Welcome tothetravelagency!
U>'TIMED_OUT'

124 CHAPTER 3. GROUNDING ISSUES
get Latest Mo ves
integrate No Mo ve©
pop(/private/nim)
select Icm Con Neg©
push(nextmoves,icm:con*neg )
S>Ididnthearanything fromyou.
get Latest Mo ves
integrate Other ICM©
pop(/private/nim)
U>'FAIL'
backup Shared
select Icm P er Neg©
push(nextmoves,icm:per*neg)
S>Sorry,Ididnthearwhatyousaid.
get Latest Mo ves
integrate Other ICM©
pop(/private/nim)
U>jfdbhajhdgarbledfdasd
backup Shared
select Icm Sem Neg
S>Iheardyousayjfdbhajhdgarbledfdasd. Sorry,Idontunderstand.
get Latest Mo ves
integrate Other ICM©
pop(/private/nim)
integrate Other ICM©
pop(/private/nim)
U>paris
get Latest Mo ves
backup Shared
select Icm Und Neg

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 125
8
>>>><
>>>>:foralldo($/shared/lu/moves/elem=A,push(nextmoves,icm:sem*p os:A))
push(nextmoves,icm:und*neg )
foralldo(in($/ shared/lu/moves,E)and E=answer(C)and$lexicon ::ynanswer(C)and
in($/private/nim,E),
del(/private/nim,E))
S>paris. Idontquiteunderstand.
get Latest Mo ves
integrate Other ICM©
pop(/private/nim)
integrate Other ICM©pop(/private/nim)
Negativereactionlevelfeedback
Tobeabletodistinguish relevantbutnon-integratable utterances fromutterances which
arebothrelevantandintegratable, adialogue systemingeneralneedstobeabletodistin-
guishbetweenrelevanceandintegratabilit y(acceptabilit y),i.e.itneedstounderstand the
relevanceofutterances thatitcannotintegrate.
Systemproposition-rejection Inaddition toissue-rejection, proposition-rejection is
alsoarguably relevanttoadialogue system. Acaseinpointiswhentheusersupplies
information whichresultsinaninvaliddatabase query,i.e.aquerywhichwouldyieldno
results. Anexample isgivenin(dialogue 3.6)(understanding-feedbac khasbeenremoved
forreadabilit y).
(dialogue 3.6)
U(1)>Priceinformation please
S(1)>OK. Wheredoyouwanttotravel?
U(2)>to Paris
S(2)>OK. Whatcityyouwanttotravelfrom?
U(3)>Oslo
S(3)>Oslo. Sorry,therearenoflights matching yourspecification.
However,thiscaseisabitmoreproblematic -is S(3)reallyarejection of U(3),orshould
itberegarded asanegativeanswertotheuser'squeryin U(1)?Webelieveitmakesmore
sensetodothelatter. Onthisview,theissueofpricewillberegarded as(negatively)
resolvedafter S(3).(Notethatwearehereassuming that Osloisinfactavaliddeparture

126 CHAPTER 3. GROUNDING ISSUES
city,buttherehappentobenoflightsfrom Osloto Parisinthedatabase.)
Avariantofthedialogue in(dialogue 3.6)thatisperhapsabettercaseofrejection is
wheretheusersupplies adestination whichisnotavailableinthedatabase. Inthiscase,
itseemstomakesensetosaythatitisindeedtheutterance containingtheinformation
aboutthedestination thatisrejected.
(dialogue 3.7)
U(1)>Priceinformation please
S(1)>OK. Wheredoyouwanttotravel?
U(2)>to Paris
S(2)>OK. Whatcityyouwanttotravelfrom?
U(3)>Kuala Lumpur
S(3)>Sorry,Kuala Lumpurisnotinthedatabase. So,Whatcitydoyou
wanttotravelfrom?12
Inthiscase,theissueofpriceisstillunresolved,asistheissueofdestination city. Tohandle
adialogue likethatin(dialogue 3.7),asystemagainneedstobeabletorecognize relevant
information thatitcannotdealwith,anddistinguish itfromsuchinformation thatitcan
dealwith. Onewayofdoingthisistoencoderelevantinformation inthedomainknowledge
resource thatisnotnecessarily inthedatabase. Ifauserutterance thatcontainsarelevant
answerorassertion isperceivedandundersto od,thesystemshouldperformadatabase
searchtocheckifitisabletodealwiththatinformation; ifnot,theuser'sutterance should
berejected.
Ofcourse,itisawell-knownproblem thatbiggervocabularies makespeechrecognition
harder,andconsequen tlythere'satradeoffbetweenrecognizing anddealingcorrectly with
non-acceptable information, andgettingtheacceptable information right. Possibly,one
couldusecollected dialogues inadomaintodecidehowmuchnon-acceptable information
thesystemshouldbeabletorecognize andunderstand.
In IBi S,wehaveimplemen tedtheabilitytorejectuseranswersbycheckingwhether
theyprovidevaliddatabase parameters. Thisrequires anadditional database resource
condition \valid DBparameter( P)"whichistrueif Pisavalidparameter inthedatabase.
Forexample, ifatravelagencydatabase containsflightswithin Europe,anydestination
outside Europeisaninvaliddatabase parameter andshouldberejected bythesystem.
12Optionally ,onemightwantasystemtobemorehelpfulandofferasuitablealternativ edestination.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 127
(rule 3.14) rule:reject Prop
class:selectaction
pre:8
>>>>>>>><
>>>>>>>>:in($/private/nim,answer(A))
$/shared/lu/speaker =usr
fst($/shared/qud,Q)
$domain ::relevant(A,Q)
$domain ::combine(Q,A,P)
not$database::valid DBparameter( P)
eff:8
><
>:del(/private/nim,answer(A))
push(/ private/agenda,icm:und*p os:usr*P)
push(/ private/agenda,icm:acc*neg :P)
Thefirstfiveconditions areidenticaltothosefortheruleforintegrating useranswers,
integrate Usr Answ er(Section 3.6.6).Thefinalcondition checksthattheproposition P,
resulting fromcombiningaquestion on QUDwiththecontentoftheanswermove,isnot
avaliddatabase parameter. Theupdatesremovethemovefromnimandselectspositive
understanding feedbacktoshowwhatthesystemundersto od,andnegativeacceptance
feedback.
Ofcourse,itisnotoptimally efficientthatthesamesequence ofconditions ischeckedby
severaldifferentrules;analternativ eapproachwouldbetoletoneruledetermine e.g.how
ananswermoveisrelevant,combine itwithaquestion on QUD,andstoretheresultin
adatastructure containingpragmatically interpreted material. Thisdatastructure could
thenbeinspectedbybothintegration andrejection rules.(Seealso Section 6.5.1.)
Dialogue example: systempropositionrejection Inthefollowingdialogue, weil-
lustratesystemrejection ofthepropositionthatthemeansoftransporttosearchforwill
betrain. Amotivationisalsogivenbythesystem,i.e.that\train"isnotavailableasa
meansoftransportinthedatabase.
(dialogue 3.8)
S>Okay. Ineedsomeinformation. Howdoyouwanttotravel?
get Latest Mo ves
integrate Other ICM
integrate Other ICM
integrate Sys Ask
U>trainplease

128 CHAPTER 3. GROUNDING ISSUES
get Latest Mo ves
backup Shared
reject Prop 8
<
:del(/private/nim,answer(train))
push(/ private/agenda,icm:und*p os:usr*how(train))
push(/ private/agenda,icm:acc*neg :how(train))
select Icm Other½
push(nextmoves,icm:und*p os:usr*how(train))
del(/private/agenda,icm:und*p os:usr*how(train))
select Icm Other½push(nextmoves,icm:acc*neg :how(train))
del(/private/agenda,icm:acc*neg :how(train))
S>bytrain. Sorry, bytrainisnotinthedatabase.
get Latest Mo ves
integrate Other ICM
integrate Other ICM
Systemissue-rejection Forexample, thesystemmightknowsomequestions whichare
relevantinacertainactivity,butnotbeabletoanswerthem. Thisisnotusuallythe
casewithexistingdialogue systems. Forexample, the Swedishrailwayinformation system
(basedonthe Philipsdialogsystem(Aust et al.,1994)cannotanswerquestions about
theavailabilityofacafeteria onatrain. Ifthisquestion isasked,thesystemwilltryto
interpretitasananswertosomething itjustaskedabout(asillustrated inthemade-up
dialogue (3.16)). Butonecouldimagine asystemthatwouldhaveastoreofpotentially
relevantquestions whichitcannothandle,enabling ittorespondtosuchquestions ina
moreappropriate way,e.g.bysaying\Sorry,Icannotanswerthatquestion". Thiswould
constitute arejection (anissue-rejection, tobeprecise)ofaquestion whosemeaning has
beenundersto od. An(made-up) example isshownin(3.17).
(3.16)U:Isthereacafeteria onthetrain?
S:Youwanttotravelto Siberia,isthatcorrect?
(3.17)U:Isthereacafeteria onthetrain?
S:Sorry,Icannotanswerquestions aboutcafeteria availability.
Issuerejection hasbeenimplemen tedin IBi S2 forthetravelagencydomain; inthetravel
agencydomain, thesystemwillrecognize andunderstand, butreject,questions about
connecting flights. Apossibleextension ofthiswouldbetomakethesystemmorehelpful
andmakeitexplainwhyitcannotanswerthequestion; thishasnotyetbeendonein IBi S.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 129
Incasethesystemhasinterpreted auserutterance asanask-movewithcontentq,butthe
systemdoesnothaveaplanfordealingwithq,thesystemmustrejectqandindicate this
totheuserusingappropriate feedback. Thisruleallowsthesystemtorespondintelligently
touserquestions evenifitcannotanswerthem(giventhattheycanberecognized and
interpreted).
(rule 3.15) rule:reject Issue
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
Theruleissimilartothereject Prop rule. Thethirdcondition checksthatthereisno
planfordealingwiththequestion Q.
Dialogue example: systemissuerejection Inthefollowingdialogue, theuser'sre-
questforinformation aboutconnecting flightsisrejected onthegrounds thatthesystem
doesnotknowhowtoaddressthatissue.
(dialogue 3.9)
S>Okay. Thepriceis 123 crowns.
U>whataboutconnecting flights
get Latest Mo ves
backup Shared
reject Issue 8
<
:del(/private/nim,ask(?A.conflight(A)))
push(/ private/agenda,)
push(/ private/agenda,icm:acc*neg :issue(?A.conflight(A)))
select Icm Other½
push(nextmoves,icm:und*p os:usr*issue(? A.conflight(A)))
del(/private/agenda,icm:und*p os:usr*issue(? A.conflight(A)))
select Icm Other½push(nextmoves,icm:acc*neg :issue(?A.conflight(A)))
del(/private/agenda,icm:acc*neg :issue(?A.conflight(A)))
S>Youaskedaboutconnecting flights. Sorry,Icannotanswerquestions

130 CHAPTER 3. GROUNDING ISSUES
aboutconnecting flights.
get Latest Mo ves
integrate Other ICM
integrate Other ICM
3.6.7 Grounding ofsystemutterances in IBi S2
Inthissection,weshowhowacautiously optimistic grounding strategy forsystemutter-
anceshasbeenimplemen tedin IBi S2. Wefirstpresentbasicupdaterulesreflecting the
cautious strategy. Wethenpresentintegration rulesforthe\core"systemdialogue moves
(askandanswer),anddescribetherulesforintegrating userfeedbacktosystemmoves.
Enabling cautiousupdates
IBi S2 usesamixofvariousgrounding strategies. Forsystemutterances, acautiously
optimistic strategy isused.
Movinglatestmovestonim The IBi S2 versionoftheupdateruleget Latest Mo ves
isshownin(rule 3.16).
(rule 3.16) rule:get Latest Mo ves
class:grounding
pre:8
><
>:$latestmoves=Moves
$latestspeaker =DP
$/shared/lu/moves=Prev Moves
eff:8
>>><
>>>:set(/private/nim,Moves)
set(/shared/lu/speaker ,DP)
clear(/ shared/lu/moves)
set(/shared/pm,Prev Moves)
Theruleloadsinformation regarding thelatestutterance performed intonimandcopies
thepreviously grounded moves(in/shared/lu/mo ves)tothe/shared/pm field. Note
thatthisrulehaschangedsignifican tlycompared to IBi S1;nooptimistic assumption
aboutunderstanding ofthelatestutterance ismadehere. Insteadofputtingthelatest
movesin/shared/lu/mo ves,whichwouldbetoassumethattheyhavebeenmutually

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 131
understo od,IBi S2 clears/shared/lu/mo vessothatmovescanbeaddedwhentheyare
actually integrated; onlythenaretheyassumed tobeundersto od.
Savingpreviousstatebeforeintegration Beforeselecting, producing,andintegrat-
inganewsystemutterance, therulein(rule 3.17)copiesrelevantpartsofthe IStothe
tmpfield. Thismakesitpossibletobacktracktoaprevious state,shouldtheoptimistic
grounding assumptions concerning asystemmoveturnouttobemistaken. Thismeans
thatanyoptimistic updatesassociatedwithintegration ofsystemmovesarenowcautiously
optimistic.
(rule 3.17) rule:backup Shared
class:none
pre:f
eff:8
>>><
>>>:/private/tmp/qud:=$/shared/qud
/private/tmp/com:=$/shared/com
/private/tmp/agenda:=$/private/agenda
/private/tmp/plan:=$/private/plan
Therearenoconditions onthisrule. Itisexecuted atthestartoftheselection algorithm
describedin Section 3.7,andisthusonlycalledbeforesystemutterances.
Cautiously optimistic integration ofsystemmoves
Forsystemaskandanswermoves,theintegration rulesaresimilartothosein IBi S1;
however,ratherthanpickingoutmovesfrom/shared/lu/mo ves,IBi S2 picksmoves
from/private/nimandaddsthemto/shared/lu/mo ves,therebyassuming grounding
ontheunderstanding level,onlyinconnection withintegration. Sinceoptimistic grounding
isassumed forsystemmoves,itwouldbeokaytohandlethemthesamewaywedid
in IBi S1;however,usermovesarenolonger(always)optimistically grounded, andwe
havechosentogiveauniform treatmen ttoallmoves. Sincein IBi Ssystemmovesare
alwayssuccessfully integrated, however,thereisnorealdifference betweenthewaythey
arehandled in IBi S1 and IBi S2.

132 CHAPTER 3. GROUNDING ISSUES
(rule 3.18) rule:integrate Sys Ask
class:integrate
pre:(
$/shared/lu/speaker ==sys
fst($/private/nim,ask(A))
eff:8
><
>:pop(/private/nim)
add(/shared/lu/moves,ask(A))
push(/ shared/qud,A)
(rule 3.19) rule:integrate Sys Answ er
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
Onecomplication isthatin IBi S2,severalmovesmaybeperformed inasingleutter-
ance. Tokeeptrackofwhichutterances havebeenintegrated, the/private/nim stack
ofnon-integrated movesispoppedforeachmovethatgetsintegrated. Notealsothat
eachintegrated (andthusundersto od)moveisaddedto/shared/lu/mo ves(whereas in
IBi S1 thiswasdoneatthestartoftheupdatecycle).
Thecautiously optimistic acceptance assumptions builtintotheserulescanberetracted
onintegration ofnegativeuserperception feedback,asexplained in Section 3.6.6,oron
negativeuserintegration feedback,asshowin Section 3.6.7. Dialogue examples involving
therulesshownabovewillbegiveninthesesections.
Userfeedbacktosystemutterances
Inthissectionwereviewuserfeedbacktosystemutterances andhowtheseaffectthe
optimistic grounding assumptions.
Negativeuserperception feedback Ifthesystemmakesanutterance, itwillassume
itisgrounded andaccepted. Iftheuserindicates thatshedidnotunderstand theutterance,
therulein(rule 3.20)makesitpossibletoretracttheeffectsofthesystem's latestmove,
thuscancelling theassumptions ofgrounding andacceptance.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 133
(rule 3.20) rule:integrate Usr P er Neg ICM
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
Thefourlastupdatesrevertthecom,qud,planandagendafieldstothevaluesstored
in/private/tmp.
Dialogue example: negativeuserperception feedback Thisdialogue showshow
IBi S2 isabletoreacttonegativeuserperception feedback(e.g.\pardon") byretracting
theoptimistic grounding assumption bybacktrackingrelevantpartsofshared tothestate
in/private/tmp/sys ,storedbeforethesystemutterance wasgenerated. Also,theplan
andagendaarebacktrackedtoenablethesystemtocontinuethedialogue properly.
(dialogue 3.10)
S>Okay. Youaskedaboutprice. Ineedsomeinformation. Howdoyouwant
totravel?
get Latest Mo ves
integrate Other ICM
integrate Other ICM
integrate Other ICM
integrate Sys Ask

134 CHAPTER 3. GROUNDING ISSUES
2
666666666666666666666666666666666666666666666666664 pr.=2
666666666666666666666666666666666666664 agenda=hhii
plan =*findout(?A.how(A))
findout(?B.destcity(B))
findout(?C.deptcity(C))
findout(?D.month(D))
findout(?E.deptday(E))
findout(?F.class(F))
consult DB(? G.price(G))+
bel =fg
tmp =2
6666666666666666664 com =fg
qud =­
?H.price(H)ff
agenda=**icm:acc*p os
icm:und*p os:usr*issue(?H.price(H))
icm:loadplan++
plan =*findout(?A.how(A))
findout(?B.destcity(B))
findout(?C.deptcity(C))
findout(?D.month(D))
findout(?E.deptday(E))
findout(?F.class(F))
consult DB(? G.price(G))+3
7777777777777777775
nim =hhii 3
777777777777777777777777777777777777775
sh.=2
6666664 com=fg
qud=¿?I.how(I)
?H.price(H)À
lu=·speaker =sys
moves =­­icm:acc*p os,:::ffff¸
pm=­­
ask(?H.price(H))ffff 3
77777753
777777777777777777777777777777777777777777777777775
U>pardon
get Latest Mo ves
integrate Usr P er Neg ICM8
>>>><
>>>>:pop(/private/nim)
/shared/qud:=$/private/tmp/qud
/shared/com:=$/private/tmp/com
/private/agenda:=$/private/tmp/agenda
/private/plan:=$/private/tmp/plan

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 135
2
6666666666666666666666666666664 private=2
666666666666666666664 agenda=**icm:acc*p os
icm:und*p os:usr*issue(?A.price(A))
icm:loadplan++
plan =*findout(?B.how(B))
findout(?C.destcity(C))
findout(?D.deptcity(D))
findout(?E.month(E))
findout(?F.deptday(F))
findout(?G.class(G))
consult DB(? H.price(H))+
bel =fg
tmp =:::
nim =hhii 3
777777777777777777775
shared =2
66664 com=fg
qud=­?A.price(A)ff
lu=·
speaker =usr
moves =oqueue([icm:p er*neg])¸
pm=:::3
777753
7777777777777777777777777777775
backup Shared
select From Plan
select Icm Other
select Icm Other
select Icm Other
select Ask
S>Okay. Youaskedaboutprice. Ineedsomeinformation. Howdoyouwant
totravel?
Explicituserissuerejection Therulein(rule 3.21)allowstheusertorejectasystem
question (byindicating inabilitytoanswer,i.e.byuttering \Idon'tknow"orsimilar). If
thisisdone,theoptimistic grounding updateisretracted byrestoring thesharedparts
storedinnim,i.e.qudandcom,totheirprevious states.
(rule 3.21) rule:integrate Usr Acc Neg ICM
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

136 CHAPTER 3. GROUNDING ISSUES
Thethirdcondition checksthattheprevious utterance containedanaskmove. Thefinal
twoupdatesretracttheoptimistic grounding assumption ontheintegration /acceptance
/reaction level.
Ofcourse,ifaquestion isrejected bytheuserthismayresultinafaileddatabase query
(unlessthealternativ edatabase accessmethoddescribedin Section 2.12.4 isused).But
howshouldasystemreactiftheuserrejectsasystemquestion? Insomeframe-based
dialogue systemsfordatabase search(e.g. Chu-Carroll, 2000),fieldsintheframecanbe
labelledasobligatory oroptional. In IBi S,thiscorrespondsroughlytothedistinction
betweentheraiseandfindoutactions;theformerhassucceeded assoonasthesystemasks
thequestion, whereasthelatterrequiresthequestion toberesolved. Soifaquestion which
wasraisedbyaraiseactionwasrejected, itwillnotbeaskedagain. Questions raisedby
findoutactions,however,willcurrentlyberaisedagainby IBi S2 immediately afterauser
rejection, sincetheactionisstillontopoftheplan. Thisisperhapsnotverycooperative,
andalternativestrategies needtobeexplored. Forexample, thefindoutactioncouldbe
movedfurtherdownintheplansothatitwillnotbeaskedimmediately again,oritmay
beraisedagainonlyifthedatabase searchfails.
Dialogueexample: explicituserissuerejection Inthefollowingdialogue example,
theuserrejectsthesystemquestion regarding howtotravel. Inthisexample, theplanhas
beenalteredsothatfindout(?x.class(x))hasbeenreplaced byraise(?x.class(x)),thereby
makingtheclass-question optional. Also,thealternativ edatabase accessmethoddescribed
in Section 2.12.4 isused.
(dialogue 3.11)
S>Whatclassdidyouhaveinmind?
get Latest Mo ves
integrate Sys Ask½
pop(/private/nim)
push(/ shared/qud,?A.class(A))

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 137
2
666666666666666666666666666666666666664 private=2
666666666666666666664 agenda=hhii
plan =¿
raise(?A.class(A))
consult DB(? B.price(B))À
bel =fg
tmp =2
66666666664 com =8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;
qud =­
?C.price(C)ff
agenda=hhii
plan =¿
raise(?A.class(A))
consult DB(? B.price(B))À3
77777777775
nim =hhii 3
777777777777777777775
shared =2
6666666666664 com=8
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
ask(?D.class(D))ffff¸
pm=­­
icm:acc*neg :issueffff 3
77777777777753
777777777777777777777777777777777777775
U>itdoesntmatter
get Latest Mo ves
integrate Usr Acc Neg ICM8
>><
>>:pop(/private/nim)
add(/shared/lu/moves,icm:acc*neg :issue)
/shared/qud:=$/private/tmp/qud
/shared/com:=$/private/tmp/com
execconsult DB

138 CHAPTER 3. GROUNDING ISSUES
2
666666666666666666666666666666666666666666664 pr.=2
66666666666666666666666666664 bel=8
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
66666666664 com =8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;
qud =­
?B.price(B)ff
agenda=hhii
plan =¿raise(?C.class(C))
consult DB(? D.price(D))À3
77777777775
nim=hhii 3
77777777777777777777777777775
sh.=2
66666666664 com=8
>><
>>:month(ap ril)
deptcity(london)
destcity(paris)
how(plane)9
>>=
>>;
qud=­
?B.price(B)ff
lu=·speaker =usr
moves =­­
icm:acc*neg :issueffff¸
pm=­­ask(?C.class(C))ffff 3
777777777753
777777777777777777777777777777777777777777775
backup Shared
select Resp ond
select Answ er
S>Thepriceis 123 crowns. cheap. Thepriceis 1234 crowns.
business class.
3.6.8 Evidence requirementsandimplicitgrounding
Inthissection,wediscussevidence requirementsforgrounding andhowthesehavebeen
implemen tedintheformofupdaterulesforimplicitgrounding.
In IBi S2 weuseacautiously optimistic grounding strategy forsystemutterances. This
assumption canberetracted ifnegativeevidence concerning grounding isfound. So,what
countsasnegativeandpositiveevidence? Recall Clark'sranking ofdifferentformsof
positiveevidence, rangingfromweakesttostrongest:

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 139
²Continuedattention
²Relevantnextcontribution
²Acknowledgemen t:\uh-huh",nodding,etc.
²Demonstration: reformulation,collaborativecompletion
²Display:verbatimdisplayofpresentation
Regarding theattentionlevel,wewillnothavemuchtosay 13. Thelevelsofacknowl-
edgemen t,demonstration anddisplayarepresumably whatwewouldregardasexplicit
feedback,although wehavebeenmainlyconcerned withtheacknowledgemen tlevel.
Evidence andrelevance
Theremaining levelin Clark'stypologyofevidence ofunderstanding is\relevantnext
contribution". Twoquestions arisehere. First,whatcountsasarelevantfollowup?Second,
ifnorelevantfollowupisproduced,shouldthiscountasnegativeevidence ofgrounding,
andifso,onwhatactionlevel?
Apropertyofdialogue systems sometimes discussed intheliterature (The DISCconsor-
tium,1999,Bohlin et al.,1999)istheabilityofasystemtounderstand andintegrate
information differentfromthatwhichwasrequested bythesystem. Howdoesthisrelate
torelevanceandgrounding? Onewaytoformulatetheproblem isthis:ifthesystemjust
askedq,andtheuser'sresponseudidnotcontainananswerrelevanttoqorfeedback
concerning theuser'sutterance, whatshouldbeassumed aboutthegrounding statusofq?
Thisis,ofcourse,alsoaproblem thathuman DPsmustresolve;however,Clarkdoesnot
(toourknowledge)directlydiscussthiscase.
(3.18)a. A:Whatcitydoyouwanttogoto?[askq]
B:I'dliketotravelin April[answerotherquestion]
b. A:Whatcitydoyouwanttogoto?[askq]
B:Doyouhaveastudentdiscount?[askotherquestion]
13Clarkincludes \continuedattention"astheweakestformofpositiveevidence ofgrounding. However,
inprinciple continuedattentionfromanaddressee Aafteranutteranceuisconsisten twithacomplete
lackofperception on A'sside;Amaynotevenhaveperceivedubutisstillwaitingforthenextutterance.
Whilethisexample maynotbeveryrelevantforhuman-humancommunication, itisnotacompletely
unlikelyscenario if Aisadialogue system. Also,contactlevelfeedbackappearsrelatedtothis.

140 CHAPTER 3. GROUNDING ISSUES
Regarding caseswhereaquestion isignored(i.e.neitheraddressed byarelevantanswer,
explicitly accepted, norexplicitly rejected), itisnotobviouswhether thequestion was
accepted ornot. Thereasonisthatthereareseveralpossibleexplanations forthisbe-
haviour:onecomplies silentlywiththequestion butthinksthatotherinformation ismore
importantrightnow(inwhichcasethequestion wasintegrated bythehearer,andwillbe
answeredeventually),oronemisheard ordidnothearthequestion atall(inwhichcase
itwasnotundersto od,andthusneitheraccepted orrejected), oronedoesnotthinkthat
thequestion isappropriate (inwhichcasethequestion wasimplicitly rejected).
Onepossiblestrategy forfindingnegativeevidence istolookforsignsofmisunderstanding,
andtotrytocomeupwithaplausible explanation forhowthismisunderstanding came
about. Thisis,however,afairlydifficulttaskevenforhumansandnotoneweintendto
explorehere.
Caseswhereaquestion isnotfollowedbyarelevantanswerorrelevant ICM,canbe
regarded asimplicit rejections ofthatquestion. However,ifthefollowupisrelevantin
someotherwaytothequestion asked,thisshouldnotberegarded asrejection. Onetype
ofrelevantfollowupcanbedefinedusing Ginzburg's notionofquestion dependence:
(3.19)Anask-movewithcontentqisarelevantfollowuptoanask-move
withcontentq 0 ifq 0 dependsonq.
In Section 2.8.2,wedefinedadomain-dep endentnotionofquestion dependence relatedto
termsofplans,whereq 0 dependsonqifthereisaplanfordealingwithq 0 whichincludes
anactionfindout( q).
Consequen tly,in IBi S2 wehavechosenthefollowingrequirementsonanutterance uto
countasanirrelevantfollowuptoanutterance raisingaquestion q:
²ucontainsno ICM
²theprevious moveraisedaquestion q
²ucontainsnoanswertoq
²ucontainsnoask-moveraisingaquestion q 0 suchthatqdependsonq 0
Concerning oursecondquestion, areirrelevantfollowupstoberegarded asnegativeground-
ingevidence? Orcoulditbethecasethata DPundersto odandaccepted anutterance u
butoptedtochangethesubjecttemporarily,planning torespondtoueventually?
Iftheirrelevantfollowupisinterpreted asnegativegrounding evidence, howdoweknow
whatactionlevelisconcerned? Didtheuserimplicitly rejecttheissuebyignoring it,or

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 141
didshesimplynotperceiveorunderstand it?Wesuspectthatthechoicebetweenthese
twointerpretations mightdependonquitesubtleissuesconcerning timing. Forexample,
iftheuser'sfollowupoverlapswiththesystem's question itispossiblethattheuserhas
notevenheardthesystem's question.
In IBi S2 wehavechosentoconsider irrelevantfollowupstosystemaskmovesasimplicit
rejections. However,thischoiceisnotobviousandisafurthertopicforfutureresearch.
Implicituserrejectionofissue
Ifanirrelevantfollowupisdetected, thisisinterpreted asanimplicitissuerejection and
consequen tlytheoptimistic assumption thatthequestion q 0 wasintegrated bytheuseris
assumed tobemistaken. Therefore, theoptimistic assumption isretracted byreverting
theprevious sharedstatefortherelevantpartsofshared.
(rule 3.22) rule:irrelevant Followup
class:none
pre:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:1$/private/nim=Moves
2$/shared/lu/speaker ==usr
3 not A/elem=icm:
4 in($/shared/pm,Prev Move)
5Prev Move=ask(Q)or
(Prev Move=icm:und*int: DP*Cand Q=und(DP*C))
6 not Moves/elem=ask(Q0)and$domain ::depends(Q,Q0)
7 not A/elem=answer(A)and$domain ::relevant(A,Q)
eff:(
/shared/qud:=$/private/tmp/qud
/shared/com:=$/private/tmp/com
(Sincethisruleiscalled\byname"fromtheupdatealgorithm, thereisnoneedforincluding
itinaruleclass.)Condition 3 checksthatno ICMwasincluded inthelatestmove.
Condition 4 and 5 triestofindaquestion Qraisedbytheprevious move,possiblyan
understanding-question. Noteherethatwedonotcheck QUD;in IBi S2,questions remain
on QUDonlyforoneturnbutitmaybethecasethatwewantquestions toremainon
QUDoverseveralturns. Whatweareinterested hereisthusnotwhichquestions areon
QUDbutwhichquestions wereraisedbytheprevious utterance, andthisisthereason
forlookinginpmratherthanqud. Conditions 6 and 7 checkthatnomoveperformed in
thelatestutterance isrelevantto Q,neitherbyansweringitnorbyaskingaquestion on
which Qdepends. Theupdatesaresimilartothoseforintegration ofnegativeacceptance
feedback(Section 3.6.7).

142 CHAPTER 3. GROUNDING ISSUES
Asisthecaseforexplicitrejections, questions raisedbyfindoutactionswillbeasked
again,butquestions raisedbyraiseactionswillnot. ICM-related questions (interrogativ e
understanding feedback)arenotrepeatedsincetheyarenotintheplanbutonlyonthe
agenda.
Adialogue involvingimplicituserrejection ofanissuewillbeshownlaterin(dialogue
3.12).
3.6.9 Sequencing ICM:reraising issuesandloadingplans
Inthissection,wereviewsequencing-related ICMandshowhowthishasbeenimplemen ted
in IBi S2.
Webelieveitisgoodpracticetotrytokeeptheuserinformed aboutwhat'sgoingoninside
thesystem,atleasttoadegreethatfacilitates anaturaldialogue wheresystemutterances
\feelnatural". Onewayofdoingthisistoproduce ICMphrasesindicating significan t
updatestotheinformation statewhicharenotdirectlyrelatedtospecificuserutterances.
Using Allwood's(1995)terminology ,werefertotheseinstances of ICMas\sequencing
ICM".
For IBi S2,wewillimplemen ttwotypesofsequencing ICM. First,whenloadingaplan
IBi S2 willindicate this. Second, IBi S2 willproduce ICMtoindicate whenanissueis
beingreraised(incontrasttobeingraisedforthefirsttime).
Loadingplans
IBi S2 willindicatewhenaplanisbeingloaded,thuspreparing theusertoanswerquestions.
Thisiscurrentlygenerated as\Let'ssee."
Theruleforfindinganappropriate plantodealwitharespond-action ontheagendais
similartothatin IBi S1. Thedifference isthatthe IBi S2 ruleproduces ICMtoindicate
thatithasloadedaplan,formalized asicm:loadplan andgenerated e.g.as\Let'ssee".
Again,thechoiceofoutputformisprovisory.

3.6. FEEDBA CKAND GROUNDING STRA TEGIES FORIBIS 143
(rule 3.23) rule:find Plan
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
Thisruleisidenticaltothatin IBi S1(Section 2.8.6),expectforthefinalupdatewhich
pushestheicm:loadplan moveontheagenda.
Reraising issues
Systemreraisingofissueassociatedwithplan Iftheuserraisesaquestion Qand
thenraises Q0 before Qhasbeenresolved,thesystemshouldreturntodealingwith Qonce
Q0 isresolved;thiswasdescribedin Section 3.6.9. Therecover Planrulein IBi S2,shown
in(3.20),isalmostidenticaltotheonein IBi S1,exceptthat ICMisproducedtoindicate
thatanissue(q 1)isbeingreraised. This ICMisformalized asicm:reraise: qwhereqisthe
question beingreraised, andexpressed e.g.as\Returning totheissueofprice".
(rule 3.24) rule:recover Plan
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
Issuereraisingbyuser Inthecasewheretheuserreraisesanopenissue,anicm:reraise: Q
moveisselectedbytheintegrate Usr Ask describedin Section 3.6.6.
Systemreraisingofissuenotassociatedwithplan The IBi S1 reraise Issue rule
describedin Section 2.12.3 reraisesanyquestions on QUDwhicharenotassociatedwith

144 CHAPTER 3. GROUNDING ISSUES
anyplan(i.e.whichhavebeenraisedpreviously bythesystem). Inthiscaseitisagain
helpfultoindicatethatthesystemisawarethattheissueisbeingreraised. However,since
theissuewillbereraised, thesequencing ICMdoesnotneedtoindicate whichquestion is
beingreraised.
(rule 3.25) rule:reraise Issue
class:selectaction
pre:(
fst($/shared/issues,Q)
not$domain ::plan(Q,P)
eff:(
push(/ private/agenda,icm:reraise )
push(/ private/agenda,raise(Q))
Theconditions ofthisrulechecksthatthereisaquestion Qonissuesforwhichthesystem
hasnoplan,i.e.onethatthesystemneedstoasktheuser.
Thefirstupdateaddsanicm:reraise (without anargumen t)tosignalthatitisreraising
aquestion; thisiscurrentlygenerated asprefixing \so"tothenextaskmove,whichis
anordinary raisingofthequestion (placedontheagendabythesecondupdateinthe
rule).Inamoresophisticated implementationonecouldconsider abbreviating theoriginal
raisingofthequestion tomakeanappropriate reraising, e.g.\So,fromwhatcity?"But
wedonothaveageneralmethodfordoingthatyet,eveninthesesimpledialogues. To
doitproperlywouldprobably requiremoredetailed syntacticandsemanticanalysis of
contributions thanwecurrentlyhavein IBi S.
Dialogueexample: userandsystemreraising (dialogue 3.12)isanexample ofa
dialogue wheretheuserreraisesanissuewhichwaspreviously raisedbutnotresolved.
Alsosubsequen tlythesystemreraisesanissuewhichisrelevantforaddressing theissue
thattheuserreraised. Inordertoaddresstheissueofpricethesystemneedstoget
information fromtheuserconcerning whereshewishestotravelfrom.
(dialogue 3.12)
S>Welcome tothetravelagency!
U>priceinformation please
S>Okay. Letssee. Howdoyouwanttotravel?
U>aflight
S>Okay. Whatcitydoyouwanttogoto?
U>paris
S>Okay. Whatcitydoyouwanttogofrom?

3.7. FURTHER IMPLEMENT ATION ISSUES 145
U>right... actually, doineedavisa
useracceptsdeparturecityissue,thenraisesvisaissue
S>Okay. Letssee. Whatcountry areyoufrom?
U>um...letstalkaboutpriceagain
userimplicitly rejects(avoids) citizenship issue,reraisespriceissue
S>Okay. Returning totheissueofprice. Letssee. So,Whatcitydoyou
wanttogofrom?
systemindicatesreturning topriceissue,thenreraisesdeparturecityissue
U>london
S>Okay. Whatmonthdoyouwanttoleave?
U>april
S>Okay. Whatdaydoyouwanttoleave?
U>fifth
S>Okay. Whatclassdidyouhaveinmind?
U>cheap
S>Okay. Thepriceis 123 crowns. Returning totheissueofvisa. Let's
see. Whatcountry areyoufrom?
systemanswerspriceissue,therebyresolvingit,thenreraisesthevisaissue,indicatesplan
loading,andreraisescitizenship issue
Thefirstcaseofreraising here,whereitistheuserwhoreraisesthepriceissue,ishandled
bytheconditional updateoftheintegrate Usr Answ er(Section 3.6.6)whichselectsan
icm:reraise: Qmovetosignalthatthesystemisawarethatissuewasalreadyopenbysaying
\Youreraised theissueofprice".Inthesameutterance, thesystemreraisestheissueof
wheretheuserwantstotravelfrom,requiresaselection ruleforthesystem. Whenreraising
anissue,IBi S2 produces ICMtoindicate awarenessthattheissuehasbeenraisedbefore.
This ICMisformalized asicm:reraise andcanberealizede.g.bythediscourse particle
\So".Notethatthiswouldnothavehappenediftheuserhadnotaccepted thisquestion
(bysaying\right")whenitwasfirstraised. Sincethesystemdoesnotregardthedeparture
cityquestion asdependentonthevisaissue,raisingthevisaissueinresponsetoasking
fordeparture citywouldhavebeenregarded asanimplicitrejection (Section 3.6.8).
Oncethepriceissuehasbeenresolved,thesystemreraisesthevisaissuewhichisstill
unresolved;thisisdonebytherecover Planruleasdescribedin Section 3.6.9.
3.7 Furtherimplementationissues
Inthissectionwedescribepartsoftheimplementationof IBi S2 whichhavenotbeen
discussed earlierinthischapter,andwhicharenotdirectlyreusedfrom IBi S1.

146 CHAPTER 3. GROUNDING ISSUES
3.7.1 Updatemodule
The IBi S2 updatealgorithm isshownin(3.20).
(3.20)1 ifnotlatestmoves==failed
2 thenhget Latest Mo ve,
3 tryirrelevant Followup,
4 repeatintegrate,
5 tryloadplan,
6 repeatmanageplan
7 trydowndatequdi
8 elsetryunclear Followup
Line 1 checksthattheinterpretation ofthelatestutterance wassuccessful (ofcourse,
inthecaseofsystemutterances thisisalwaystrue).Ifnot,theunclear Followuprule
describedin Section 3.6.8 istried. Ifinterpretation wassuccessful, thelatestmovesare
incorporatedintheinformation stateproperbytheget Latest Mo vesrule(see Section
3.6.7).Beforeintegration starts,theirrelevant Followupruledescribedin Section 3.6.8
istriedtocatchcaseswhereasystemquestion hasbeenignoredbytheuser. Afterthis,
theintegration ruleclassisrepeatedlyapplieduntilthesystemhastriedtointegrateall
movesin/private/nim. Iftheuseraskedaquestion, theappropriate planwillbeloaded
byline 5. Anyloadedplanisexecuted byapplying theexecplanruleclassuntilnomore
execution ispossibleatthecurrentstageofthedialogue.
3.7.2 Selection module
Asin IBi S1,actionselection rulesaddactionstotheagenda. However,whilein IBi S1 only
oneactionwasselected perturn,in IBi S2 severalactionsmaybeselected perturn. For
example, theselect Resp ondin IBi S2,shownin(rule 3.26),doesnotrequiretheagenda
tobeempty,butonlythattherespondactionhasnotalreadybeenselected, andthusit
allowsseveralmovestobeselectedperturn.

3.7. FURTHER IMPLEMENT ATION ISSUES 147
(rule 3.26) rule:select Resp ond
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
Similarly ,themoveselection rulesin IBi S2 arerepeatedlyapplied,poppingactionsoffthe
agendaqueueandpushing thecorrespondingmovesonnextmoves. Asanexample,
theselect Answ erruleisshownin(rule 3.27).
(rule 3.27) rule:select Answ er
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
Theselection algorithm for IBi S2 isshownin(3.21).
(3.21)hbackup Shared ,
ifnotin($/private/agenda,A)andqraisingaction(A)
thentryselectaction,
repeat(selecticmorelseselectmove)i
Theselectactionruleclassselectsactionsandplacesthemontheagenda,whereas
theselectmoveandselecticmruleclassesselects agendaitemsandplacesthemon
nextmoves. Beforeselection, thebackup Shared (Section 3.6.7)isappliedtocopy
relevantpartsoftheinformation stateto/private/nim.
Thebasicstrategy forselection in IBi Sisthatonlyonequestion shouldberaisedbythe
systemineachutterance. The IBi S2 selection algorithm firstchecksifsomequestion-
raisingactionisalreadyontheagenda; ifnot,ittriestoselectanewaction. Then,it
selectsmovesand ICMrepeatedlyuntilnothingmorecanbeselected.

148 CHAPTER 3. GROUNDING ISSUES
The\qraisingaction(A)"condition usesamacrocondition (see Section A.4.2)whose
definition isshownin(3.22).Whatthissaysis,basically,thatinterrogativ e ICM,raise
and,findoutactionsraisequestions.
(3.22)qraisingaction(Move)if
Move=icm:und*int: Xor Move=raise(X)or Move=findout( X)
3.8 Discussion
3.8.1 Somegrounding-related phenomena nothandled by IBi S2
Inthissectionwementionsomeareaswhichhavenotbeenaccountedforintheissue-based
approachpresentedhere. Wedonotbyanymeansclaimthatthislistiscomplete.
Perhapsthemostsignifican tomission in IBi S2 isatreatmen tofsemanticambiguity,e.g.
ambiguous words. Apossibledirection ofresearchinthisareaistohandlesemantic
ambiguityonapragmatic level. Specifically,therelevanceofanambiguousmoveinthe
currentdialogue contextmaybesufficienttoresolvethesemanticambiguity,oratleast
reducethenumberofpossiblesemanticinterpretations. Inanycase,weseenoreason
thatmechanisms similartothosefordealingwithpragmatic ambiguitycouldbeusedfor
semanticambiguity.
Another areathatremainsunexplored fromthepointofviewofissue-based dialogue man-
agementissemanticvagueness. Forinstance, onemightwantasystemtounderstand
vagueanswers(e.g.\Iwanttogotosouthern France",\Iwanttotravelaroundthe 10 th
of April"), andperhapsalsotoasklessspecificquestions whichleavemoreroomforthe
usertochoosehowtospecifye.g.parameters fordatabase search(e.g.\Where doyou
wanttotravel?"ratherthan\Whatcitydoyouwanttogoto?").
Onthepragmatic understanding level,wehaveconcentratedonellipsisresolution and
relevance,howeverwearestilllackingatreatmen tofreferentresolution. Onereasonfor
thisisofcoursethat IBi S2 doesnotrepresentreferents. Thisisafairlywell-researc hed
area,andwehopetobeabletoincludesomeexistingaccountofreferentresolution when
thisbecomesnecessary .

3.8. DISCUSSION 149
Overlapping userfeedbackandandbarge-in
Mostdialogue systemsdonothandlefeedbackfromtheuserinanyform,andmost(ifnot
all)existing systems whichhandlebarge-in willstoptalkingiftheyperceiveanysound
fromthespeaker. Thismeansthatevenpositivefeedback(e.g.\uhuh")fromtheuser
willcausethesystemtostopspeaking. Thisproblem isaggravatedinnoisyenvironmen ts,
wherenoisesmaybemisinterpreted asspeechfromtheuserandcauseasystemtostop
speaking. Whatisneededisclearlythatthesystemmakesadistinction betweendifferent
kindsoffeedbackfromtheuser;positivefeedbackshouldusuallynotcausethesystemto
stopspeaking.
Mechanisms forhandling overlapping userfeedbackhasbeenexplored withinthe Go Di S
framework(Berman, 2001),butarenotincluded here. However,theinclusion ofpositive
userfeedbackin IBi Sprovidesabasisforfurtherexplorations inthisarea.
3.8.2 Towardsanissue-based accountofgrounding andaction
levels
Wehavehintedthatafull-coverageaccountofgrounding shouldincludegrounding onall
fouraction-levels. Ginzburg's content-andacceptance-questions indicate howthiscould
beaccomplished inanissue-based theoryofdialogue. Foreachactionlevel,grounding
issuescanberaisedandaddressed; feedbackmovesonlevel Lareregarded asaddressing
grounding issuesonlevel L.
Thiswouldallowgrounding tobehandled bythesamebasicupdatemechanisms asques-
tionsandanswers. Adistinction canbemadebetweenshort(elliptical, underspecified)
answers(feedbackutterances whoseactionlevelisnotexplicit) andfullanswers(feedback
utterances whoseactionlevelisclearfromtheformandcontentoftheutterance).
In IBi S,westriveforsimplicityatthecostofcompleteness; however,theaccountgiven
herecanbeseenasafirststeptowardsamorecomplete issue-based accountofgrounding
anactionlevelsindialogue. Asketchofamorecomplete accountcanbefoundin Section
6.5.1.
3.8.3 Comparison to Traum'scomputational theoryofgrounding
Traum(1994)providesacomputational accountofgrounding basedonacombination of
finiteautomata andcognitivemodelling. Thismodelbuildson Clarkand Schaefer(1989 b)

150 CHAPTER 3. GROUNDING ISSUES
butattempts tosolvesomecomputational problems inherentinthataccount.
Traumarguesthat Clark'saccountofthepresentationandacceptance phasesisproblem-
aticfromacomputational pointofview. Firstly,itmaybehardtotellifaspeechsignal
ispartofthepresentationoracceptance phase. Second,itishardtoknowwhenapresen-
tationoracceptance isfinished; often,thisisonlypossibleinhindsight,whichmaycause
problems foradialogue systemengaged inreal-time spokendialogue. Third,itisunclear
whether grounding acts(inourterminology ,ICMdialogue moves)themselv esneedtobe
grounded.
Regarding thelastpoint,wefollow Trauminassuming that ICMmovesdonotneedto
begrounded. Infact,onourviewthisamountstoanoptimistic grounding strategy where
ICMmovesareconcerned.
Weagreethatingeneraltheproblem ofdeciding whenacontribution endsisonethat
shouldbehandled asapartofdialogue management,andthatsomething like Traum's
atomicgrounding actsareneededforthis. However,forthetimebeingwemakethesim-
plifyingassumption thatcontributions arealreadysegmentedbeforedialogue management
starts;intheimplementation,werelyonthespeechrecognizer's built-inalgorithms for
deciding whenanutterance isfinished.
Ouraccountdoesnotaddressthefirstpoint,i.e.theproblem ofjointlyproducedcontri-
butions, where DPse.g.canrepaireachother'sutterances. Traumproposesarecursive
transition network(RTN)modelofthegrounding processwhichincludes repairs,requests
forrepairs,acknowledgemen tsandrequests foracknowledgemen ts(asimplerfinitestate
modelisalsoprovided).Ouraccountdoesnotincluderepairsorrequests foracknowledge-
ments;however,Traum'sacknowledgemen tscorrespondroughlytopositivefeedbackand
requests forrepairscorrespond(very)roughlytonegativefeedback.
Itisimportanttonoteherethat Traum(1994)usestheterm\grounding" toreferexclu-
sivelytowhatwecall\understanding-levelgrounding". Itisnotablethat Tramfocuses
almostexclusivelyonpositivefeedback,whereas negativefeedbackisgivenalessdetailed
treatmen t. Thegrounding actmostcloselycorrespondingtonegativefeedbackisrequest
forrepair;however,itisdoubtful whether allnegativefeedbackcanberegarded asrequests
(e.g.\Idon'tunderstand"). Touse Allwood'sterminology ,feedbackhasbothanexpres-
sivedimension (expressing lackofperception, understanding, acceptance) andanevocative
dimension (requesting a\repair" orrepetition/reform ulation). Itappearsthat Traumhas
focusedmoreontheevocativedimension whereas wehavebeenmoreconcerned withthe
expressiv edimension. (Wedofeelthattheevocativeaspectoffeedbackissomething that
perhapsdeservesmoreattentionthanwehavegivenitsofar;thisisyetanotherareafor
futureresearch.)
Thedialogue acts\accept" and\reject"areregarded by Traumas\Core Speech Acts"on

3.9. SUMMAR Y 151
thesamelevelasassertions, askingquestions, givinginstructions etc. Theacceptactis
definedas\agreeing toaproposal"(p.58),whichgivestheimpression thatanacceptance
actisanaturalfollowuptosomeproposalact.
However,Traum'sacceptance actalsohassimilarities towhatwerefertoaspositive
reaction-levelfeedback. Forexample, anacceptance movemayfollowanassertion oran
instruction, andtheeffectsoftheacceptactistochangethestatusofthecontentofthe
assertion orinstruction frombeingmerelyproposedtoactually beingshared. Regarding
questions, itisunclearwhether theyneedtobeaccepted beforebeingshared. According to
Traum,askingaquestion imposesanobligation ontheaddressee toaddressthequestion,
i.e.toeitheransweritortorejectit. Thisseems(although itisfarfromclear)toindicate
thatquestions on Traum'saccountareoptimistically assumed tobegrounded whereas
assertions andinstructions arenot.
In Chapter 5,weextendtheissue-based accountofdialogue tonegotiativedialogue, andar-
guethattwokindsofacceptances needtobedistinguished: acceptance aspositivefeedback
onthereaction level,andacceptance ofaproposedalternativesolution tosomeproblem
(e.g.acertaindomainplanasoneamongseveralwaystoreachsomegoal).
3.9 Summary
Afterprovidingsomedialogue examples wherevariouskindsoffeedbackareused,we
reviewedsomerelevantbackground, anddiscussed generaltypesandfeatures offeedback
asitappearsinhuman-humandialogue. Next,wediscussed theconcept ofgrounding
fromaninformation updatepointofview,andintroducedtheconcepts ofoptimistic,
cautious andpessimistic grounding strategies. Wethenrelatedgrounding andfeedbackto
dialogue systems, anddiscussed theimplementationofapartial-co veragemodeloffeedback
relatedtogrounding in IBi S2. Thisallowsthesystemtoproduceandrespondtofeedback
concerning issuesdealingwiththegrounding ofutterances.

152 CHAPTER 3. GROUNDING ISSUES

