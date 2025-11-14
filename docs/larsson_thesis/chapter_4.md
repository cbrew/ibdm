Chapter 4
Addressing unraised issues
4.1 Introduction
Intheprevious chapter,wediscussed variousmechanisms forhandling grounding. Oneof
theactionlevelstowhichgrounding appliesisthatofpragmatic understanding, i.e.making
senseofthemeaning ofanutterance inthecurrentdialogue context. Somebasicmecha-
nismsforgrounding ontheunderstanding levelwereimplemen tedin IBi S2. However,the
kindsofdialogues handled bythissystemarestillratherrigidandsystem-con trolled.
Theaimofthecurrentchapteristoenablemoreflexibledialogue. Afterreviewing some
shortcomings of IBi S2,wetakeacloserlookatthenotionsunderlying the QUDdata
structure, whichresultsindividing QUDintotwosubstructures, oneglobalandonelocal.
Next,thenotionofquestion accommodationisintroducedtoallowthesystemtobemore
flexibleinthewayutterances areinterpreted relativetothedialogue context. Amongother
things,question accommodationallowsthesystemtounderstand answerstoquestions
whichhavenotyetbeenasked,andtounderstand suchanswersevenbeforeanyissue
hasbeenexplicitly raised. Incasesofambiguity,clarification dialogues maybeneeded.
Question accommodationcombinedwith(verybasic)beliefrevision abilities alsoallows
IBi Storeaccommo datequestions whichhavepreviously beenresolved. Finally,aversion
ofreaccommodation,wherereaccommodationofoneissuerequires reaccommodationofa
dependentissueaswell,allowsforsuccessivemodifications ofdatabase queries.
Thedivisionof QUDintoaglobalandalocalstructure alsoenablesasimpleaccommo-
dationmechanismallowingtheusertocorrectthesystemincaseswhereexplicitpositive
feedbackshowsthatthesystemhasmisundersto odauserutterance.
153

154 CHAPTER 4. ADDRESSING UNRAISED ISSUES
Apartfromtheinitialandfinalsections, thischapterisstructured aroundthevariousques-
tionaccommodationmechanisms. Foreachtypeofaccommodation,thereisaninformal
description, aformalization consisting ofoneormoreupdaterules,anddialogue examples.
4.2 Somelimitations of IBi S2
Handling answerstounaskedquestions
Thedialogue structure allowedbythe IBi S2 systemisratherrigidandsystem-con trolled.
Themainpartofthedialogue consistsofthesystemaskingquestions whichtheuserhas
toanswer. Theuserisnotallowedtogivemoreinformation, ordifferentinformation, than
whatthesystemhasjustaskedfor.
Ingeneral, werequirethatthecontentofeachanswer-movemustmatchaquestion on
QUD. In IBi S2,theonlywayquestions canendupon QUDisbybeingexplicitly asked.
Thisforcesasimpletreestructure ondialogue. Inrealdialogue, however,peopleoften
performutterances whichcanbeseenasanswerstoquestions, oraddressing issues,which
havenotyetbeenraised.
Revisinginformation
Oncetheuserhassupplied someinformation to IBi S2,thisinformation cannotbechanged.
Thisisclearlyundesirable, andsolvingthisproblem wouldprovideseveraladvantages:
²Theusermaychangehismindduringthespecification ofthedatabase query
²Aftertheuserhasbeengivene.g.priceinformation foraspecifiedtrip,hecan
modifysomeoftheinformation toproduceanewquery,withouthavingtoenterall
information again
Correcting explicitpositivefeedback
Animportantfactorinfluencing thechoiceoffeedbackandgrounding strategies inadia-
loguesystemisusability(including efficiency ofdialogue interaction). Adisadvantageof
theconfirmation-question approachisthatthedialogue becomesslowandtiringforthe
user,whichdecreases theefficiency andusabilityofthesystem.

4.3. THENATURE(S) OFQUD 155
Forthisreason,intheprevious chapterweaddedthecapabilityofproducingfeedbackon
theunderstanding levelinnon-eliciting form,i.e.asadeclarativ eorelliptical sentence
(without question intonation). However,thissolution isunsatisfactory sincethesystem
maybemistakenandthereisnowaytocorrectit. Averynaturalresponsetopositive
explicitfeedbackwhichindicates amisunderstanding istoprotest,e.g.bysaying\no!",
possiblyfollowedbyacorrection.
Inthischapter,weuseaspecialcaseofquestion accommodationtoallowthis,thusex-
tendingtheissue-based accountofgrounding. Iftheuserissatisfied withthesystem's
interpretation, shedoesnothavetodoanything;thesystemwilleventuallycontinue(pos-
siblyafterashortpause)withthenextstepinthedialogue plan. Theuser'ssilenceis
regarded asanimplicitcompliance withthesystem's feedback. Thereisalsotheoptionof
givinganexplicitpositiveresponsetothefeedback(e.g.\yes"or\right").Finally,ifthe
userrespondsnegativelytothesystem's feedback(e.g.bysaying\no"),thesystemwill
understand thatitmisundersto odtheuserandactaccordingly .
4.3 Thenature(s) of QUD
Beforeextending thecapabilities of IBi S,wewillinvestigatethenatureof QUDandmake
somedistinctions betweenthedifferenttasksthat QUDcanbeusedfor. Wewilldrawthe
conclusion that QUDneedstobedividedintotwosubstructures, oneglobalandonelocal.
Inthissection,wepresentandcompare somealternativ enotionsof QUD.
4.3.1 Ginzburg's definition of QUD
In Ginzburg (1997),Ginzburg providesthefollowingdefinition of QUD:
QUD('questions underdiscussion'): asetthatspecifiesthecurrentlydiscuss-
ablequestions, partially orderedbyÁ('takesconversational precedence'). Ifq
ismaximal in QUD,itispermissible toprovideanyinformation specifictoq
using(optionally) ashort-answ er.(Ginzburg, 1997,p.63)
Whilethedefinition abovemerelystatesthat QUDisapartially orderedset,theoperations
performed on QUDin Ginzburg's protocolssuggestthatinfactitismorelikeapartially

156 CHAPTER 4. ADDRESSING UNRAISED ISSUES
orderedstack 1. In IBi S1 and IBi S2 wemadethesimplification that QUDissimplya
stack.
Ginzburg thususesasinglestructure todotwojobs:(1)specifyingthequestions thatare
currentlyavailablefordiscussion (\open"questions), and(2)specifyingthequestions that
canbeaddressed byashortanswer(namely,thosethatare QUD-maximal).
Basedon Ginzburg's QUDquerying protocol(Section 2.8.2),Ginzburg's QUDcanalsobe
saidto(3)representquestions whichhavebeenexplicitly raisedinthedialogue. Whilethis
isnotexplicitly stated,itappearsthattheonlywayatask-levelquestion canenter QUD
on Ginzburg's accountisbybeingexplicitly asked.(However,grounding-related questions
mayenter QUDwithoutbeingraisedaspartoftheinternalreasoning ofa DP;see Section
3.2.2).
Similarly ,the QUDdowndateprotocol(Section 2.8.4)suggests that QUDalsofulfillsafur-
therproperty(4)ofcontainingas-yetunresolvedquestions. Opennessandunresolvedness
maynotbeidenticalproperties;arguably,resolvedquestions maystilltosomeextentbe
openfordiscussion, andaquestion couldbediscarded fromtheopenissueswithoutbeing
resolved,e.g.ifitbecomesirrelevant(Larsson, 1998).
Tosummarize, giventhisbasiccharacterization of QUD,wecansaythatquestions on
QUDare
1.openfordiscussion,
2.availableforellipsisresolution,
3.explicitly raised,and
4.notyetresolved.
In IBi S2,theimplemen ted QUDessentiallyfitswith Ginzburg's definition, exceptforthe
simplification thatitisaplainstackratherthananopen,partially orderedstack. Thisis
sufficientfortherelativelysystem-con trolled,rigiddialogue handled by IBi S2. Whenthe
dialogue structure becomesmoreflexible, however,thesevariouspropertiesofthe QUD
listedabovenolongerappeartoco-occurinallsituations.
1Apartially orderedstackwouldbeastructure whereelementscanbepushedandpopped,butwhich
onlyhasapartialordering. Forexample, morethanoneelementcanbetopmost onthestack.

4.3. THENATURE(S) OFQUD 157
4.3.2 Openquestions notavailableforellipsisresolution
Regarding QUDasastack(orstack-like)structure suggests thatwhenthetopmost element
(orsetofelements)ispoppedoffthestack,theelement(orsetofelements)thatwas
previously next-to-maximal becomesmaximal. Thisimpliesthatquestions canbeanswered
elliptically atanarbitrary distance fromwhentheywereraised. However,itcanbeargued
thatinmanycasesaquestion whichhasbeenraisedafewturnsbackisnolongeravailable
forellipsisresolution (oratleastsignifican tlylessavailablethanitwasrightafterthe
question wasraised).Forexample, B'sfinalutterance inthemade-up dialogue in(4.1)is
unlikelytooccuranditwouldberatherconfusing ifitdid,simplybecauseitisnotclear
whichquestion Bisanswering.
(4.1)A:Who'scomingtotheparty?
B:Thatdepends,is Jillcoming
A:Jill Jennings?
B:Yes
A:Bytheway,didyouhearaboutherbrother? What'shis
nameanyway?
B:Umm..I'mnotsure. Anyway,I'drathernottalkaboutit.
A:OK. So,No
B:So,Jim
Ifthisargumen tisaccepted, weseethataquestion maysatisfyrequirements(1)and(3)
above,tobeacurrentlyopenfordiscussion, explicitly raisedquestion, whilenotsatisfying
property(2)ofbeingavailableforellipsisresolution.
4.3.3 Openbutnotexplicitly raisedquestions
Studying recorded travelagencydialogues inlightofthe QUDapproachindicates thatit
maybethecasethataquestion whichhasnotbeen(explicitly) raisedisinfactdiscussable,
andevenavailableforellipsisresolution, asthedialogue in(4.2)shows 2.
(4.2)A:Whendoyouwanttotravel?
B:April,ascheapaspossible
Thus,wecanobservethataquestion maysatisfyrequirements(1)ofbeingopenfor
discussion and(2)ofbeingavailableforellipsisresolution, withoutsatisfying property(3)
ofhavingbeenexplicitly raised.
2Thisisasimplified versionofthedialogue inexample 4.6.

158 CHAPTER 4. ADDRESSING UNRAISED ISSUES
4.3.4 Globalandlocal QUD
Theobservationsabovesuggestthatitisnotidealtomodel QUDusingasinglestructure
satisfying properties(1)to(4).Thesolution weproposeistodivide QUDintoaglobal
andalocalstructure; theformersatisfying property(1)ofbeingopenfordiscussion and
(4)ofbeingunresolved,andthelattersatisfying property(2)ofbeingavailableforellipsis
resolution. Property(3)ofbeingexplicitly raisedisnotsatisfied byeitherstructure. This
enablesmoreflexiblewaysofintroducingquestions intoadialogue. Thisdivisionoflabour
alsoappearstoallowtheuseofsimplerdatastructures thanpartially orderedsets.
Definition oflocal QUD
Forthelocal QUD,asetseemsappropriate formodellingthequestions currentlyavailable
forellipsisresolution. Astack-likestructure wouldsuggeste.g.the(made-up) dialogues
(4.3)shouldbeeasilyprocessedby DPs,butinfactitisveryunclearwhat Bmeans.
(4.3)A:Whereareyougoing?Whereisyourwifegoing?
B:Paris. London.
Also,consider example (4.4):
(4.4)A:Whenareyouleaving?Whenareyoucomingback?
B:tenthirtyandeleventhirty
Asimplestackstructure alsosuggests averyunintuitiveinterpretation of B'sanswer,
where 10:30 isthetimewhen Biscomingbackand 11:30 isthetimewhen Bisleaving.
Itappearsthatamongtheconstrain tsguidingellipsisresolution incaseswheremultiple
questions areavailable,theorderinwhichthequestions wereaskedisnotverysignifican t.
Ofcourse,Ginzburg realizesthisandthisappearstobethemainreasonforletting QUD
beapartially orderedsetwhereseveralinternallyunordered elementsmaybetopmost on
QUD,andthusavailableforellipsisresolution.
In IBi S3 wedefine QUDtobeanopenstackofquestions thatcanbeaddressed using
shortanswers. Thereasonforusinganopenstackisthatithastheset-likepropertieswe
want,butalsoretainsastackstructure incaseitshouldbeusefulforellipsisresolution.

4.3. THENATURE(S) OFQUD 159
Definition ofglobal QUD,or\Live Issues"
Theglobal QUDcontainsallquestions whichhavebeenraisedinadialogue (explicitly or
implicitly) butnotyetresolved. Itthuscontainsacollection ofcurrent,or\live"issues.
Asuitable datastructure appearstobeanopenstack,i.e.astackwherenon-topmost
elementscanbeaccessed. Thisallowsanon-rigid modellingofcurrentissuesandtask-
relateddialogue structure.
4.3.5 Someothernotionsofwhata QUDmightbe
Infact,therearesomeadditional notionsofwhat QUDmightbe,allofwhichinsome
sensecontainquestions thatareunderdiscussion, andallofwhichhavepotentialusesin
atheoryofdialogue managementandinadialogue system.
²closedissues:questions thathavebeenraisedandresolved(see Section 3.6.9)
²raisabledomainissues:allissuespotentiallyrelevantinregardtothedomain
²potentialgrounding issues:allissuespertaining togrounding of(a)recentutter-
ance(s)
²resolvableissues(fora DP):allissuesthata DPknowssomewayofdealingwith,
eitherbyansweringdirectlyorbyenteringasubdialogue
However,whileallthesemaybeuseful,itmaynotbenecessary tomodelthemexplicitly
asseparate structures inadialogue system. Forexample, \raisable domainissues"and
\resolvableissues"maybederivedfromthe(static)domainknowledge.
Regarding \closedissues",wecantosomeextentderivethemfromthesharedcommitmen ts
bycheckingwhichissuesareresolvedbypropositional information, asin(4.5).
(4.5)Qisaclosedissueiffthereissome P2/shared/com such
that Presolves Qand Pdoesnotresolveanyotherquestion (in
thedomain)
However,thisonlyworksaslongaseachpropositionresolvesauniqueissue. Ifthisisnot
true,aseparate storeofclosedissuesisneedede.g.fordetecting reraisings ofpreviously
discussed issues.

160 CHAPTER 4. ADDRESSING UNRAISED ISSUES
4.4 Question Accommo dation
Inthissection,weintroducetheconceptofaccommodationandshowhowitcanbeex-
tendedtohandleaccommodationofquestions invariousways. Wealsoshowhowquestion
accommodationcanbeimplemen tedin IBi S.
4.4.1 Background: Accommo dation
Lewis'notionofaccommodation
David Lewis,in Lewis(1979),indiscussing theconcept ofaconversational scoreboard,
compares conversation toabaseball game:
...conversational scoredoestendtoevolveinsuchawayasisrequired inorder
tomakewhateveroccurscountascorrectplay(Lewis,1979,p.347)
Healsoprovidesageneralschemeforrulesofaccommodationforconversational score:
Ifattimetsomething issaidthatrequires componentsnofconversational
scoretohaveavalueintherangerifwhatissaidistobetrue,orotherwise
acceptable; andifsndoesnothaveavalueintherangerjustbeforet;andif
such-and-suc hfurtherconditions hold;thenattthescore-comp onentsntakes
somevalueintheranger.(Lewis,1979,p.347)
Thisverygeneralschemacanbeusedfordealingwithdefinitedescriptions, presupposition
projection(seee.g.vander Sandt,1992),anaphora resolution, andmanyotherpragmatic
andsemanticproblems.
Onemotivationforthinking intermsofaccommodationhastodowithgenerality. We
couldassociateexpressions whichintroduceapresuppositionasbeingambiguousbetween
apresuppositional readingandasimilarreadingwherewhatisthepresuppositionispart
ofwhatisasserted. Forexample, anutterance of\Thekingof Franceisbald"canbe
understo odeitherasanassertion ofthepropositionthatthereisakingof Franceandhe
isbald,orasanassertion ofthepropositionthatheisbaldwiththepresuppositionthat
thereisakingof Franceandthat\he"referstothatindividual. However,ifweassume
thataccommodationtakesplacebeforetheintegration oftheinformation expressed bythe
utterance thenwecansaythattheutterance alwayshasthesameinterpretation.

4.4. QUESTION ACCOMMOD ATION 161
4.4.2 Accommo dation,interpretation, andtacitmoves
Inaninformation updateframework,accommodationisnaturally implemen tedasanup-
daterulewhichmodifiestheinformation statetoincludetheinformation presupposedby
anutterance, insuchawayastomaketheutterance felicitous, i.e.tomakeitpossibleto
understand therelevanceofandpossiblyintegratethemove(s)associatedwiththeutter-
ance. Theaccommodationupdateactsasareplacemen tforadialogue move,whichwould
haveprepared the(common) groundfortheutterance actually performed. Forthisreason,
accommodationupdatesmaybereferredtoasakindoftacitmove. Forexample, thesilent
accommodationmovewhichadds\thereisakingof France"toallowtheintegration of
\Thekingof Franceisbald"correspondstoadialogue moveasserting thisproposition.
Thus,wecansimplify ourdialogue moveanalysis sothattheupdatestotheinformation
statenormally associatedwithadialogue moveareactually carriedoutbytacitaccommo-
dationmoves.
Thisfitswellwiththefactthatveryfew(ifany)effectsofadialogue moveareguaranteed
asaconsequence ofperforming themove;rather,theactualresulting updatesdependon
reasoning bytheaddressed participant. Accommo dationisonetypeofreasoning involved
inunderstanding andintegrating theeffectsofdialogue moves.
4.4.3 Extending thenotionofaccommodation
Inthissection, weextendthenotionofaccommodationintroducedby Lewistocover
accommodationof Questions Under Discussion.
Asdefinedby Lewis,accommodationisnotlimitedtoonlypropositions 3. Itstatesthat
anycomponentofthescoreboardcanbemodifiedbyaccommodation. Ifwecarrythis
overtotheissue-based approachtodialogue management,itfollowsthatinaddition to
theaccommodationofpropositionstothesetofjointlycommitted propositions, questions
canbeaccommo datedto QUD.
Thus,question accommodationcanbeexploited toprovideanexplanation ofthefactthat
questions canbeaddressed (evenelliptically) withouthavingbeenexplicitly raised. This
isveryrelevantforadialogue system,sinceitallowstheusermorefreedom regarding
whenandhowtoprovideinformation tothesystem. Inaddition, therelatedconceptof
3Ofcourse,allinformation onthe DGBis,intheend,propositional innature;a DGBcontaininga
question Qatthetopof QUDcouldinprinciple bedescribedbyasetofpropositionsincluding \Qis
topmost on QUD".This,however,wouldbeimpractical andinefficien tcompared tomaintainingaproper
stack-likestructure.

162 CHAPTER 4. ADDRESSING UNRAISED ISSUES
question reaccommodationcanbeusedtoenableaddressing resolvedissues,whichamong
otherthingsprovidesawayofhandling revision ofjointlycommitted propositionsina
principled manner.
Beforeproceedingtoexploretheexactformulationandformalization ofquestion accom-
modation,weprovidearoughcharacterization ofthenotionsused:
²question/issue accommodation:adjustmen tsofcommon groundrequired tounder-
standanutterance addressing anissuewhichhasnotbeenraised,butwhichis
{relevanttothecurrentdialogue plan
{relevanttosomeissueinthedomain
²question/issue reaccommodation:adjustmen tsofcommon groundrequired tounder-
standanutterance addressing anissuewhichhasbeenresolvedand
{doesnotinfluence anyotherresolvedissue
{influences anotherresolvedissue
{concerns grounding ofaprevious utterance
Utterances whicharerelevanttothecurrentdialogue plancanalsoberegarded asbeing
indirectlyrelevanttothegoalofthatplan. Ininquiry-orienteddialogue wemodelgoals
asissueswhichallowsanalternativ eformulationofaccommodationas\adjustmen tsof
common groundrequired forunderstanding anutterance addressing anissuewhichhas
notbeenraised,butwhichis(directly orindirectly) relevanttosomeissueinthedomain."
Inaction-orienteddialogue (Chapter 5),utterances mayalsobeindirectly relevanttosome
goalaction.
4.5 Formalizing questionaccommodation
Inthissectionwediscussthevarioustypesofquestion accommodationandshowhowthey
areformalized in IBi S3. Westartbyexplaining andmotivatingsomemodifications ofthe
information statetyperequired tohandledialogues involvingquestion accommodation.
4.5.1 Information statein IBi S3
Theinformation stateusedin IBi S3 isshownin Figure 4.1.

4.5. FORMALIZING QUESTION ACCOMMOD ATION 163
2
666666666666666666666664 private:2
666666664 agenda:Open Queue(Action)
plan :Open Stack(Plan Construct)
bel :Set(Prop)
tmp :"
usr:Tmp
sys:Tmp#
nim :Open Queue(P air(DP,Move))3
777777775
shared :2
666666664 com :Set(Prop)
issues :Open Stack(Question)
qud :Open Stack(Question)
pm :Open Queue(Mo ve)
lu :"
speaker :Participan t
moves:Set(Move)#3
7777777753
777777777777777777777775
Tmp=2
6666664 com :Set(Prop)
issues :Open Stack(Question)
qud :Open Stack(Question)
agenda:Open Queue(Action)
plan :Open Stack(Plan Construct)3
7777775
Figure 4.1:IBi S3Information Statetype
Thefirstchangecompared tothe IBi S2 information stateistheaddition oftheopenstack
/shared/issues ,whichcontainstheopenissues. The/shared/qud fieldhasnotbeen
modifiedintermsofdatatype,butisnowusedformodellingthelocal QUD.
Thesecondchangeisthedivisionof/shared/tmp intotwosubfields. Thesyssubfield
correspondstothetmpfieldin IBi S2,andcontainspartsoftheinformation statecopied
rightbeforeintegrating thelatestsystemutterance. Asin IBi S2,systemutterances are
optimistically assumed tobegrounded, andiftheusergivesnegativefeedbackthetmp/sys
fieldisusedtoretracttheoptimistic assumption. Inaddition, thesystemsometimes
makesanoptimistic assumption regarding thegrounding andunderstanding ofauser
utterance, andproducespositivefeedback(e.g.\OK. To Paris."). In IBi S3,wewill
useatypeofquestion accommodationtoenableretraction oftheoptimistic grounding
assumption regarding userutterances, incaseswheretheuserrejectsthesystem's reported
interpretation. Forthis,wealsoneedtokeepacopyofrelevantpartsoftheinformation
stateastheywererightbeforetheuser'sutterance wasinterpreted andintegrated; thisis
whatthetmp/usr fieldcontains.
Finally,theitemson/private/nim arenowpairs,wherethefirstelementisthe DP
whomadethemove,andthesecondisthemoveitself. In IBi S2,itcanbeassumed
thatallnon-integrated moveswereperformed inthelatestutterance. In IBi S3,question
accommodationmechanisms allowlessrestricted dialogues, andthereisnolongerany
guaranteethatallnon-integrated movesweremadeinthelatestutterance. Movesmaybe

164 CHAPTER 4. ADDRESSING UNRAISED ISSUES
storedinnimforseveralturnsbeforebeingintegrated.
4.6 Varietiesofquestion accommodationandreac-
commodation
Asshownbythedialogue in(4.6)4,questions canbeanswered(evenelliptically) without
previously havingbeenraised.
(4.6)J:vickenmÅanadskaduÅaka
whatmonthdoyouwanttogo
B:ja:typden:öa:tredjefjöardeapril/nÅangÅangdöar
wellaround 3 rd 4 thapril/sometimethere
P:sÅabillitsommöojlit
ascheapaspossible
Butwheredoestheaccommo datedquestion comefrom?Inprinciple, wecouldimaginea
hugenumberofpossiblequestions associatedwithanyanswer,especiallyifitiselliptical or
semanticallyunderspecified. Howisthissearchspaceconstrained? Theanswerliesinthe
activitywhichisbeingperformed; thequestion mustbeavailableaspartoftheknowledge
associatedwiththeactivity-eitherstaticknowledgedescribing howtheactivityistypically
performed, ordynamic knowledgeofthecurrentstateoftheactivity.
Inthissectionwefirstdescribethethreebasicquestion accommodationmechanisms: global
question accommodation(issueaccommodation),localquestion accommodation(QUDac-
commodation)anddependentissueaccommodation. Wethendiscusstheneedforclari-
ficationquestions incaseswhereitisnotclearwhichquestion isbeingaddressed, before
movingontodescribing reaccommodationanddependentreaccommodation. Foreachtype
ofaccommodationwealsodescribetheimplementationandprovidedialogue examples from
theimplemen tedsystem.
Ingeneral, accommodationistriedonlyafter\normal" integration hasfailed. Thecoor-
dination oftheaccommodationrulesinrelationtogrounding (including integration) rules
ishandled bytheupdatealgorithm describedin Section 4.7.2.
4Thisdialogue hasbeencollected bythe Universityof Lundaspartofthe SDSproject. Wequotethe
transcription donein Göteborgaspartofthesameproject.

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION165
4.6.1 Issueaccommodation:fromdialogue planto ISSUES
Thistypeofaccommodationoccurswhena DPaddresses anissuewhichisnotyetopen
butwhichispartofthecurrentplan 5. Inthedialogue inexample 6,P'ssecondutterance
(\ascheapaspossible") addresses theissueofwhichpriceclass Pisinterested in. Atthis
stageofthedialogue, thisissuehasnotbeenraised,butpresumably Jwasplanning to
raiseiteventually.
Before IBi Scanintegrateananswer,itneedstofindanopenissuetowhichtheanswer
isrelevant(seethedefinition oftheintegrate Usr Answ errulein Section 3.6.6).Thus,
tohandleadialogue likethatinexample 6 somemechanismisneededforfindingan
appropriate issueinthecurrentdialogue planandmovingittotheissuesstack. A
schematic representationofissueaccommodationisshownin Figure 4.2. 
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
_a`D b. A&Y!$4C<=*",IYIG

I
@./&102%13!c

Y:d&)(	*2,e G
 @./&102%13!c

Y:d&)(	*2,D @



"!f Ug*XW2B,-G
F
I
 

h Q
 b 4 i 02<;&)(	%(	 0 j/&D
`J
 @.A&Y!f Ug*XW2B,R
Z\[[[[[[]
Z\[[[[[[[[[[[[[[[[[[]
Figure 4.2:Issueaccommodation
Theissueaccommodationupdaterulein(rule 4.1)firstcheckswhether aquestion which
matchestheansweroccursinthecurrentdialogue plan(providedthereisone).Aquestion
matchesanansweriftheanswerisrelevantto,or(in Ginzburg's terminology) aboutthe
question. Ifsuchaquestion canbefound,itcanbeassumed thatthisisnowanopen
issue. Accommo datingthisamountstopushingthequestion onthe ISSUES stack.
5Sincethecurrentplanispresumably beingcarriedoutinordertodealwithsomeopenissue,wemay
regardtheutterance asindirectly relevanttosomeopenissue(viatheplan).

166 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(rule 4.1)rule:accommodate Plan 2Issues
class:accommodate
pre:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:$/private/nim/elem/snd=answer(A)
not$lexicon ::ynanswer(A)
in($/private/plan,findout( Q))
$domain ::relevant(A,Q)
$domain ::defaultquestion( Q)or
not(in($/private/plan,findout( Q0))
and Q6=C
and$domain ::relevant(A,Q0))
eff:n
push(/ shared/issues,B)
Thefirstcondition picksoutanon-integratedanswermovewithcontent A. Thesecond
condition checksthat Aisnotay/nanswer(e.g.yes,no,maybeetc.),andthusim-
plementsanassumption thatsuchanswerscannottriggerquestion accommodation,since
theyaretooambiguous 6. Thethirdandfourthconditions checkifthereisafindoutaction
withcontent Qinthecurrentlyloadedplan,suchthat Aisrelevantto Q. Thefinalcon-
ditionchecksthatthereisnootherquestion intheplanthattheanswerisrelevantto,or
alternativ elythat Qhasthestatusofadefaultquestion. Ifthiscondition doesnothold,a
clarification question shouldberaisedbythesystem;thisisdescribedin Section 4.6.3. The
\default question" optionallowsencodingofthefactthatoneissuemaybesignifican tly
moresalientinacertaindomain. Forexample, inatravelagencysettingthedestination
citymayberegarded asmoresalientthanthedeparture cityquestion. Ifthisisencoded
asadefaultquestion, theniftheusersayssimply\Paris"itisinterpreted asanswering
thedestination cityquestion; noclarification istriggered 7
Example dialogue: issueaccommodation Thedialogue in(dialogue 4.1)illus-
tratesaccommodationofthequestion?C.class(C)fromtheplantothestackofopen
issues.
(dialogue 4.1)
6However,ingeneralonecannotruleoutthepossibilitythaty/nanswerscantriggeraccommodationin
severelyrestricted domains. Theassumption thatthiscannothappencanberegarded asaverysimplified
versionofaconstrain tonthenumberofquestions whichananswermayberelevantwithout making
question accommodationinfeasible.
7Thenormalgrounding mechanisms shouldofcourseenablecorrection ofthisassumption. In IBi S3
thechoiceofgrounding strategy dependssolelyontherecognition scorewhichmeansthatahigh-scoring
answermaybeinterpreted asananswertoadefaultquestion andnotreceiveanyexplicitfeedback. Thisis
onecasewhichindicates aneedfortakingmorefactorsintoaccountwhenchoosingfeedbackandgrounding
strategy.

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION167
S>Whatmonthdoyouwanttoleave?
2
66666666666666666666666666664 private=2
666666664 agenda=hhii
plan =*findout(?A.month(A))
findout(?B.deptday(B))
findout(?C.class(C))
consult DB(? D.price(D))+
bel =fg
nim =hhii 3
777777775
shared =2
666666666666664 com =8
<
:destcity(paris)
deptcity(london)
how(plane)9
=
;
issues =¿?F.month(F)
?E.price(E)À
qud =­
?F.month(F)ff
pm =:::
lu =2
4 speaker =sys
moves =ask(?F.month(F))
score =13
53
7777777777777753
77777777777777777777777777775
U>aprilascheapaspossible
get Latest Mo ves
backup Shared Usr
integrate Usr Short Answ er
downdate ISSUES
remove Findout
accommo date Plan 2Issues©
push(/ shared/issues,?A.class(A))
integrate Usr F ull Answer
downdate ISSUES
remove Findout
downdate QUD

168 CHAPTER 4. ADDRESSING UNRAISED ISSUES
2
666666666666666666666666664 private=2
66664 agenda=­­icm:acc*p osffff
plan =¿
findout(?A.deptday(A))
consult DB(? B.price(B))À
bel =fg
nim =hhii 3
77775
shared =2
66666666666666664 com =8
>>>><
>>>>:class(economy )
month(ap ril)
destcity(paris)
deptcity(london)
how(plane)9
>>>>=
>>>>;
issues =­
?D.price(D)ff
qud =hi
pm =­­
icm:acc*p os,icm:loadplan, ask(?C.month(C))ffff
lu =2
4 speaker =usr
moves =­­answer(april),answer(class(economy ))ffff
score =13
53
777777777777777753
777777777777777777777777775
S>Okay. Whatdaydoyouwanttoleave?
4.6.2 Localquestion accommodation:from ISSUES to QUD
Ifamovewithunderspecifiedcontentismadewhichdoesnotmatchanyquestion onthe
QUD,theclosestplacetolookforsuchaquestion is ISSUES, andifitcanbefoundthere
itshouldbepushedonthelocal QUDtoenableellipsisresolution. Asaside-effect, the
question hasnowbeenbroughtintofocusandshould,ifitisnottopmost ontheopen
issuesstack,beraisedtothetopofopenissues. Aschematic overviewoflocalquestion
accommodationisshownin Figure 4.3. 
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
_a`D b. A&Y!$4C<=*",IYIG

I
@./&102%13!c

Y:d&)(	*2,e G
 @./&102%13!c

Y:d&)(	*2,D @



"!f Ug*XW2B,-G
F
I
 

h Q
 b 4 i 02<;&)(	%(	 0 j/&D
`J
 @.A&Y!f Ug*XW2B,R
Z\[[[[[[]
Z\[[[[[[[[[[[[[[[[[[]
Figure 4.3:Localquestion accommodation
Thistypeofaccommodationcane.g.occurifaquestion whichwasraisedpreviously has
droppedoffthelocal QUDbuthasnotyetbeenresolvedandremainson ISSUES. Itshould
alsobenotedthatseveralaccommodationstepscanbetakenduringtheprocessingofa

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION169
singleutterance; forexample, ifanissuethatisintheplanbuthasnotyetbeenraisedis
answeredelliptically .
(rule 4.2)rule:accommodate Issues 2QUD
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
Thesecondcondition in(rule 4.2)checksthatthecontentoftheanswermovepickedout
bycondition 1 issemanticallyunderspecified. Thethirdcondition imposesaconstrain t
onlocalquestion accommodation,excluding shortanswerstoy/n-questions (\yes",\no",
\maybe"etc.).Theremaining conditions checkthattheanswer-contentisrelevanttoan
issuewhichisonissuesbutnotonqud. Thefirstoperationpushestheaccommo dated
question onqud,andthefinalupdateraisesthequestion tothetopofthestackofopen
issues.
4.6.3 Issueclarification
In IBi S2,useranswersareeitherpragmatically relevanttothequestion topmost on QUD,
ornotrelevantatall. Whenweaddmechanisms ofaccommodationtoallowforanswers
tounraised questions, itbecomesnecessary todealwithcaseswhereananswermaybe
potentiallyrelevanttoseveraldifferentquestions.
Semanticallyunderspecifiedanswersmay(butneednot)bepragmatically ambiguous, i.e.
itisnotclearwhatquestion theyprovideananswerto. Thiscanberesolvedbyasking
thespeakerwhatquestion sheintendedtoanswer(orequivalently,whichpropositionshe
wantedtoconvey).
Inthiscase,wecanusethesamestrategy asfornegativegrounding, i.e.whenapragmat-
icallyambiguousutterance istobeinterpreted thesystemraisesaquestion whoseanswer
willbeintegrated insteadoftheambiguousanswer. Forexample, \Paris"mayberelevant
toeitherthedestination cityquestion orthedeparture cityquestion. Whenthetheclari-
ficationquestion \Doyoumeanfrom Parisorto Paris?"israiseditisexpectedthatthe

170 CHAPTER 4. ADDRESSING UNRAISED ISSUES
userwillanswerthisquestion, whichmeansthattheambiguousanswernolongerneedsto
beintegrated andcanbethrownaway 8.
Inthiswayweseehowquestion accommodation,amended withamechanismforresolving
whichquestion toaccommo date,canbeusedtoresolvepragmatic ambiguities inuserinput.
Theaccommodationmechanismcanthusberegarded asarefinemen toftheaccountof
grounding ontheunderstanding levelputforwardin Chapter 3. Therulewhichselects
theissueclarification issueisshownin(rule 4.3).
(rule 4.3)rule:clarify Issue
class:selectaction
pre:8
>>><
>>>:in($/private/nim,usr-answer(A))
setof(C,in($/private/plan,findout( Q))and
$domain ::relevant(A,Q),QSet)
$$arity(QSet)>1
eff:8
><
>:!setof(?P,in(QSet,Q)and$domain ::combine(Q,A,P),Alt Q)
push(/ private/agenda,findout( Alt Q))
del(/private/nim,usr-answer(A))
Thefirstcondition picksouttheanswer-movefromthenimqueue. Thesecondandthird
conditions checkthatthereismorethanonequestion intheplantowhichtheanswer
isrelevant,byconstructing thesetofsuchquestions. Thefirstoperationconstructs the
alternativ e-question byapplying eachquestion inthesetconstructed incondition 2 tothe
answertogetapropositionandprefixing thequestion operator'?'toeachproposition
togetay/n-question. Thealternativ equestion isthissetofy/n-questions. Thesecond
operationpushestheactiontoraisethealternativ equestion ontheagenda,andthefinal
operationremovestheanswermovefromnim;thisismotivatedabove.
Asampledialogue withissueclarification isshownin(dialogue 4.2).
(dialogue 4.2)
S>Welcome tothetravelagency!
U>priceinformation please
S>Okay. Ineedsomeinformation. Howdoyouwanttotravel?
U>flightumparis
S>OK,byflight. Doyoumeanfromparisortoparis?
8IBi S3 onlyhandlesfullanswerstoclarification questions, i.e.\To Paris."or\From Paris.".Aslightly
moreadvancedsemanticswouldberequired tohandlecaseswheretheuseragaingivesanunderspecified
responsewhichresolvesthequestion, i.e.\To."or\From.".

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION171
Theuser'sutterance of\paris"isinterpreted asanswer(paris),whichisrelevanttotwo
questions intheplan:?x.destcity(x)and?x.deptcity(x).Because ofthis,theissue
accommodationrulein 1 willnotfireandtheanswerisnotintegrated. Thisallowsthe
clarify Issue ruletofireintheselection phase. Bycombiningeachofthesequestions
withthecontentoftheanswer(paris),andturningeachresulting propositionintoay/n-
question, thesetf?destcity(paris),?dest city(paris)gisobtained. Thissetalsoworks
asanalternativ e-question, whichisusedasthecontentoftheclarification question inthe
system's finalutterance in(4.6).
Notethattheseclarification questions aredynamically puttogether bythesystemand
thusdonotneedtobepre-programmed. Thismeansthattheapplication designer does
notevenneedtorealizethatanambiguityexists.
4.6.4 Dependentissueaccommodation:fromdomainresource to
ISSUES
Issueaccommodation,introducedabove,presupposesthatthereisacurrentplaninwhich
tolookforanappropriate question; this,inturn,presupposesthatthereissomeissue
underdiscussion whichtheplanismeanttodealwith. Butwhatifthereiscurrentlyno
plan?
Inthiscase,itmaybenecessary tolookinatthesetofstoreddomain-sp ecificdialogue
plans(orcomeupwithanewplan)totrytofigureoutwhichissuethelatestutterance
wasaddressing. Anappropriate planshouldcontainaquestion matchingsomeinformation
providedinthelatestutterance. Ifsuchaplanisfound,itispossiblethat,inaddition tothe
question answeredbythelatestutterance, afurtherissueshouldalsobeaccommo dated:
the\goal-issue" whichtheplaninquestion isaimedatdealingwith. Givenourdefinition
ofdependence betweenquestions in Section 2.8.2,thegoalissueisdependentontheissue
directlyaddressed, andhencewerefertothisasdependentissueaccommodation.
Dependentissueaccommodationisthustheprocessoffindinganappropriate background
issueandaplanfordealingwiththatissuewhichmakesthelatestutterance relevant,given
\normal" globalissueaccommodation. Thatis,dependentissueaccommodationisalways
followedbyglobalissueaccommodation. Dependentissueaccommodationapplieswhenno
issuesareunderdiscussion, andapreviously unraised question isansweredusingafullor
shortanswer(inthelattercase,globalissueaccommodationmustinturnbefollowedby
localquestion accommodation). Aschematic overviewofdependentissueaccommodation
isshownin Figure 4.4,andtheupdateruleisshownin(4.7).

172 CHAPTER 4. ADDRESSING UNRAISED ISSUES 
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
_a`D b. A&Y!$4C<=*",IYIG

I
@./&102%13!c

Y:d&)(	*2,e G
 @./&102%13!c

Y:d&)(	*2,D @



"!f Ug*XW2B,-G
F
I
 

h Q
 b 4 i 02<;&)(	%(	 0 j/&D
`J
 @.A&Y!f Ug*XW2B,R
Z\[[[[[[]
Z\[[[[[[[[[[[[[[[[[[]
DOMAIN
RESOURCE
Figure 4.4:Dependentissueaccommodation
(rule 4.4)rule:accommodate Dependent Issue
class:accommodate
pre:8
>>>>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>>>>:setof(A,$/private/nim/elem/snd=answer(A),Ans Set)
$$arity(Ans Set)>0
isempty($/private/plan)
$domain ::plan(Dep Q,Plan)
forall(in( Ans Set,A),in(Plan,findout( Q))and
$domain ::relevant(A,Q))
not($domain ::plan(Dep Q0,Plan 0)and Dep Q06=Dep Qand
forall(in( Answer Set,A),in(Plan 0,findout( Q))and
$domain ::relevant(A,Q)))
notin($/private/agenda,icm:und*int:usr *issue(Dep Q))
eff:8
>>>>>><
>>>>>>:push(/ shared/issues,Dep Q)
push(/ private/agenda,icm:accommo date:Dep Q)
push(/ private/agenda,icm:und*p os:usr*issue(Dep Q))
set(/private/plan,Plan)
push(/ private/agenda,icm:loadplan )
Thefirsttwoconditions construct asetofallnon-integrated answersandcheckthatthe
arityofthissetislargerthanzero,i.e.thatthereisatleastonenon-integrated answer.

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION173
Itshouldbenotedthatthisformulationoftherulereliesontheassumption thatall
unintegrated answershavebeenprovidedbytheuser. Thisistruefor IBi S3,sinceall
systemanswersareintegrated immediately andneverneedaccommodation. However,ina
morecomplex systemthismaynotalwaysbetrue;inthiscase,therulewouldneedsome
slightmodifications toonlypickoutusermoves.
Thethirdcondition checksthattheplanisempty. Theconsequence ofthisisthatde-
pendentissueaccommodationisnotavailablewhensomeplanisbeingexecuted, soifan
issueisbeingdealtwiththeonlywaytoraiseanewissueistodosoexplicitly .Webelieve
thisisareasonable restriction, butifdesireditcanbedisabled byremovingthecondition.
However,doingsomaygiveproblems incasespeechrecognition mistakenlyrecognizes an
answernotmatchingthecurrentplan;ifthisanswertriggersdependentaccommodation
thismayresultinconfusing utterances fromthesystem.
Thefourthandfifthconditions lookforaplaninthedomainresource towhichallnon-
integrated answersarerelevant. Thiscanberegarded asasimpleversionofplanrecog-
nition:givenanobservedsetofactions(useranswers),trytofindaplanandagoal(an
issue)suchthattheactionsfittheplan. Here,theuseranswersfittheplanbybeingrele-
vantanswerstoquestions intheplan(moreprecisely,questions suchthattheplanincludes
actionstoresolvethem).
Thefinalcondition checksthatthereisonlyoneplantowhichalltheanswersarerelevant.
Ifthereareseveralsuchplans,theaccommodationruleshouldnottrigger;instead, a
clarification question shouldberaisedbythesystem(see Section 4.6.5).
Theupdatespushthedependentissueonissues,loadstheplan,andpushestheappropri-
ate ICMmovesontheagenda:positivefeedbackconcerning theaccommo datedissue(\You
wanttoknowaboutprice.")andfeedbackindicating thatanewplanhasbeenloaded(\I
needsomeinformation"). Inaddition, ICMindicating accommodationisproduced(see
Section 4.7.1).
(dialogue 4.3)
S>Welcome tothetravelagency!
U>iwantaflight
get Latest Mo ves
backup Shared Usr
accommo date Dependent Issue

174 CHAPTER 4. ADDRESSING UNRAISED ISSUES
8
>>>><
>>>>:push(/ shared/issues,?C.price(C))
push(/ private/agenda,icm:accommo date:?C.price(C))
push(/ private/agenda,icm:und*p os:usr*issue(?C.price(C)))
set(/private/plan,stackset([findout(? D.how(D)),findout(?E.destcity(E)),:::]))
push(/ private/agenda,icm:loadplan )
accommo date Plan 2Issues©push(/ shared/issues,?A.how(A))
accommo date Issues 2QUD½push(/ shared/qud,?A.how(A))
raise(/ shared/issues,?A.how(A))
integrate Usr Answ er
downdate ISSUES
remove Findout
downdate QUD
backup Shared Sys
select Icm Other
select Icm Other
2
666666666666666666666666664 private=2
6666666666664 agenda=­­
icm:loadplan, icm:acc*p osffff
plan =*findout(?A.destcity(A))
findout(?B.deptcity(B))
findout(?C.month(C))
findout(?D.deptday(D))
findout(?E.class(E))
consult DB(? F.price(F))+
bel =:::
nim =:::3
7777777777775
shared =2
666666664 com =©how(plane)ª
issues =­
?G.price(G)ff
qud =hi
pm =­­greetffff
lu =2
4 speaker =usr
moves =­­answer(plane)ffff
score =13
53
7777777753
777777777777777777777777775
S>Alright. Youwanttoknowaboutprice.
U>
S>Ineedsomeinformation. Okay. Byflight. Whatcitydoyouwanttogo
to?
Thecurrentsolution hasanoptimistic strategy fordependentaccommodation:theissue
isassumed tobeunderdiscussion andthesystemgivesexplicitpositivefeedbackofthis
assumption. Itmaybearguedthatapessimistic strategy ismoreappropriate fordependent
accommodation;thiscanbeachievedbyreplacing thelistofupdatesin 4 withtheupdate

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION175
in(4.7).
(4.7)push(/ private/agenda,icm:und*int:usr *issue(D))
Thiswillprovideinterrogativ efeedbackfromthesystemconcerning whether thedependent
issueshouldbeopened,e.g.\Youwanttoknowaboutprice,isthatcorrect?". Iftheuser
givesapositiveresponsetothisfeedback,thesystemwillusethesameupdaterulesas
usualforintegrating theuser'sresponsetointerrogativ efeedback.
(dialogue 4.4)
S>Welcome tothetravelagency!
U>iwantaflight
get Latest Mo ves
backup Shared Usr
accommo date Dependent Issue©push(/ private/agenda,icm:und*int:usr *issue(?C.price(C)))
downdate QUD
backup Shared Sys
select Icm Und Neg
select Icm Other
S>flight. Idontquiteunderstand. Youwanttoknowaboutprice,is
thatcorrect?
get Latest Mo ves
integrate Other ICM
integrate Other ICM
integrate Und In t ICM
U>yes
get Latest Mo ves
integrate Pos Icm Answ er
find Plan
accommo date Plan 2Issues
accommo date Issues 2QUD
integrate Usr Answ er
downdate QUD

176 CHAPTER 4. ADDRESSING UNRAISED ISSUES
2
6666666666666666666666666666664 private=2
666666666666664 agenda=­­icm:loadplan, icm:und*int:usr *how(plane)ffff
plan =*findout(?A.how(A))
findout(?B.destcity(B))
findout(?C.deptcity(C))
findout(?D.month(D))
findout(?E.deptday(E))
findout(?F.class(F))
consult DB(? G.price(G))+
bel =fg
nim =hhii)3
777777777777775
shared =2
66666666664 com =fg
issues =¿?A.how(A)
?H.price(H)À
qud =hi
pm =­­icm:sem*p os:answer(plane),:::ffff
lu =2
4 speaker =usr
moves =oqueueansw er(yes)
score =13
53
777777777753
7777777777777777777777777777775
backup Shared Sys
select Icm Other
select Icm Other
S>Ineedsomeinformation. byflight,isthatcorrect?
4.6.5 Dependentissueclarification
Ifnoplanisloadedandoneorseveralnon-integrated answersarerelevanttoseveralplans,
aclarification question shouldberaisedbythesystemtofindoutwhichissuetheuser
wantsthesystemtodealwith. Thisisdonebytheselection rulein(rule 4.5).
(rule 4.5)rule:clarify Dep endent Issue
class:selectaction
pre:8
>>>>>>>>>>><
>>>>>>>>>>>:in($/private/nim,pair(usr,answer(A)))
setof(Q0,$domain ::plan(Q0,Plan)and
in(Plan,findout( Some Q))and
$domain ::relevant(A,Some Q),
QSet 0)
removeunifiables( QSet 0,QSet)
$$arity(QSet)>1
eff:(
!setof(Issue Q,in(QSet,I)and Issue Q=?issue(I),Alt Q)
push(/ private/agenda,findout( Alt Q))

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION177
Thefirstcondition checksifthereisatleastonenon-integrated useranswerleftafter
thesystemhasattempted tointegratethelatestuserutterance. Thesecondandthird
conditions constructs theset QSetofdependentissuesthatthenon-integrated answeris
indirectly relevantto(i.e.issuesforwhichthereisaplancontaininganactiontoresolve
aquestion towhichtheanswerisrelevant)9. Thefinalcondition checksthatthereismore
thanonesuchdependentissue.
Thefirstupdateconstructs analternativ e-question bypickingouteachquestion Iin QSet
andadding?issue( I)tothesetwhichconstitutes thealternativ e-question. Thefinal
updatepushesanactiontoresolvealternativ e-question ontheagenda.
Inthetravelagencydomain, anexample ofdependentissueclarification occursifthe
user'sfirstutterance is\to Paris",interpreted asanswer(destcity(paris)).Thisanswer
isrelevanttothequestion?x.destcity(x)whichoccursinboththeplanforaddressing
thepriceissueandthatforaddressing thevisaissue. Thisblocksthedependentissue
accommodationrule. Inthedialogue in(dialogue 4.5),thesysteminsteadraisesa
clarification question. Notethat IBi S3 heremakesuseofthefactthatanask-movecan
supplyananswertoaquestion concerning whichissuetopursue.
(dialogue 4.5)
S>Welcome tothetravelagency!
U>toparis
get Latest Mo ves
backup Shared Usr
downdate QUD
backup Shared Sys
clarify Dep endent Issue½
!setof(E,in(set([need visa,?D.price(D)]),F)and E=issue(F),G)
push(/ private/agenda,findout(G))
select Icm Und Neg
select Ask
S>toparis. Idontquiteunderstand. Doyoumeantoaskaboutvisaor
toaskaboutprice?
9Theremoveunifiables condition isusedtoremovemultipleoccurrences ofthesameissue. Notethat
theseoccurrences arenotidentical,sincetheymaydifferintheidentityofvariables. Onemayofcourse
arguewhether setsshouldhavethisproperty,butinthecurrent Trindi Kit implementationtheydo.

178 CHAPTER 4. ADDRESSING UNRAISED ISSUES
get Latest Mo ves
integrate Other ICM
integrate Other ICM
integrate Sys Ask
U>visa
get Latest Mo ves
backup Shared Usr
integrate Usr Ask
downdate ISSUES
find Plan
accommo date Plan 2Issues
integrate Usr Answ er
downdate QUD
S>Okay. Ineedsomeinformation. toparis,isthatcorrect?
4.6.6 Question reaccommodation
In IBi S1 and IBi S2 theuserhasalimitedabilitytoreraisepreviously resolvedissues;this
willtypically resultinthesystemgivingthesameansweragain. However,thiskindof
reraising isnotveryusefulsincetheuserisnotabletomodifyherownanswerstothe
system's previous questions.
Globalquestionreaccommodation(Issuereaccommodation)
Ingeneral,iftheuserprovidesanalternativ eresolution ofanissuewhichhasbeenprevi-
ouslyresolved,thistriggersareraising ofthatissue. Iftheprevious answerisincompatible
withthenewone,theoldanswerisremoved. Thisallowstheusertochangehis/hermind
duringthedialogue. Hereisanexample dialogue withthesystem:
(dialogue 4.6)
S>Welcome tothetravelagency!
U>priceinformation please
S>Youaskedaboutprice. Howdoyouwanttotravel?

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION179
U>aflight, aprilthefifth
S>byflight. inapril. thefifth. Okay. Whatcitydoyouwanttogo
to?
U>london
S>Okay.tolondon.
U>actually, iwanttogoonthefourth
S>thefourth. Whatcitydoyouwanttogofrom?
Initially,integration oftheanswerusingintegrate Usr Answ er(Section 3.6.6)willfail
sincethereisnomatchingquestion onissues. Thesystemwillthentryvariousaccom-
modationstrategies, including accommodationfrom/shared/com formulatedin(rule
4.6).
(rule 4.6)rule:accommodate Com 2Issues
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
Thisaccommodationrulelooksforananswer Aamongthemoveswhichhavenotyetbeen
integrated (firstcondition). Itthenlooksforapropositionamongthesharedcommitmen ts
established inthedialogue sofar(secondcondition) whichaccording tothesystem's domain
resource isanappropriate answertosomequestion forwhich Aisalsoananswer(thirdto
fifthconditions). Giventhatinthissimplesystemanswerscanonlyberelevanttoasingle
question 10,thisstrategy willbesuccessful inidentifyingcaseswherewehavetwoanswers
tothesamequestion. Asystemthatdealswithmorecomplex dialogues wherethisisnot
thecasewouldneedtokeeptrackofclosedissuesinaseparate listofclosedissues. Thus
theconditions willsucceedifthereisaquestion suchthatboththeuseranswerandastored
propositionarerelevantanswerstoit;intheexample dialogue above,\departure dateis
thefourth"and\departure dateisthefifth"arebothrelevantanswerstothequestion
\whichdaydoyouwanttotravel?".Ifsuchaquestion isfounditisaccommo datedto
issues,thatis,itbecomesanopenissueagain.
Whenaccommodate Com 2Issues hasbeensuccessfully applied,theretractrulein(rule
10Thatis,inthefullforminwhichtheyappearin$/shared/com.\Chicago" canbeananswerto
\Whichcitydoyouwanttogoto?"and\Whichcitydoyouwanttogofrom?"butwhenithasbeen
combinedwiththequestions theresultwillbe\destination(Chicago)" and\from(Chicago)" respectively
anditisthiswhichisenteredintothecommitmen ts.

180 CHAPTER 4. ADDRESSING UNRAISED ISSUES
4.7)willremovetheincompatible information fromthesystem's viewofsharedcommit-
mentsrepresentedin/shared/com .
(rule 4.7)rule:retract
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
Theconditions herearesimilartothosein(rule 4.6).Welookforanunintegrated
answer(firstcondition) whichisrelevanttoaquestion attheheadofthelistofopenissues
(thirdandfifthconditions) andforwhichthereisalreadyarelevantanswerintheshared
commitmen ts(secondandfourthconditions). Finally,wedetermine thattheresultof
combiningtheanswerwiththequestion (sixthcondition) isincompatible withtheanswer
alreadyfound(seventhcondition). Ifallthisistruewedeletetheanswerwhichiscurrently
inthesharedcommitmen ts. Thiswillfinallyallowthenewanswertobeintegrated bya
rulethatintegrates ananswerfromtheuser,andafurtherrulewillremovetheresolved
issuefrom QUD. Notethatthisruleisofclassintegrate. Asisindicated in Appendix B,it
istriedbeforeanyotherintegration rule,toavoidintegration ofconflicting information.
Notealsothatthe\incompatible" relationisdefinedasapartofthedomainresource, and
canthusbedomainspecific. Thesimplekindofrevision that IBi Scurrentlydealswith
isalsohandled bysomeform-based systems(although theyusuallydonotgivefeedback
indicating thatinformation hasbeenremovedorreplaced, as IBi Sdoes).Forexample,
Chu-Carroll (2000)achievesasimilarresultbyextracting parameter valuesfromthelatest
userutterance andsubsequen tly(ifpossible)copyingvaluesfromtheprevious formfor
anyparameters notspecifiedinthelatestutterance. Asimilarmechanismisreferredto
as\overlay"by Alexandersson and Becker(2000).Whilewearedealingonlywithvery
simplerevisionhere,therulein(rule 4.7)andthe\incompatible" relationcanbeseenas
placeholders foramoresophisticated mechanismofbeliefrevision.
Itisalsopossibletoremovetheoldanswerbydenyingit(asserting itsnegation) asin
(dialogue 4.7).
(dialogue 4.7)

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION181
S>Welcome tothetravelagency!
U>priceinformation foraflighttoparisonaprilthefifth
S>Youaskedaboutprice. byflight. toparis. inapril. thefifth.
Whatcitydoyouwanttogofrom?
U>actually, notthefifth
S>notthefifth. So,whatdaydoyouwanttoleave?
Inthiscase,thesystemwillexplicitly reraisetheissuetogetanewresponsefromthe
user. Again,thesystemwillusetherulein 25 andsignalreraising using"so,".Allthe
ruleswillbeappliedasintheprevious case,butthedeparture datequestion willnotbe
removedsinceitisnotresolvedbythegivenanswer. Eventually,thisleadstothesystem
reraising thequestion.
Reraising ofdependentquestions (dependentissuereaccommodation)
Insomecases,anissuemightbereraised whichinfluences theanswertoafurtherissue
thathasalsobeenresolved. Forexample, thechoiceofpriceclassforaflightinfluences the
priceoftheflight. Inthiscase,theinfluenced question alsoneedstobereaccommo dated
andansweredagain.
(dialogue 4.8)
S>Welcome tothetravelagency!
U>what'sthepriceofaflightfromlondontoparisaprilthefifth?
S>Youaskedaboutprice. byflight. fromlondon. toparis. inapril.
thefifth. Whatclassdidyouhaveinmind?
U>ascheapaspossible
S>cheap. Okay. Thepriceis 123 crowns.
U>actually, imightgoforbusiness class
S>firstclass. Okay. Concerning yourquestion aboutprice:Theprice
is 1234 crowns.
Therulethatachievesthereraising ofadependentquestion com-to-issuesaccommodation
isshownin(rule 4.8).

182 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(rule 4.8)rule:accommodate Com 2Issues Dep endent
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
Thisruleissimilarto 6 exceptthatislooksforaquestion whichdependsonthequestion
itfindscorrespondingtotheanswerprovidedbytheuser. Itputsbothquestion ontothe
listofopenissuesandplanstorespondtothedependentquestion. Thisrule,ascurrently
implemen ted,isspecifictotheparticular casetreatedinthesystem. Thereis,ofcourse,a
greatdealmoretosayaboutwhatitmeansforonequestion tobedependentonanother
andhowthesystemknowswhether itshouldrespondtodependentquestions orraisethem
withtheuser.
4.6.7 Openingupimplicitgrounding issues
In Chapter 3 weoutlined ageneralissue-based accountofgrounding, whereissuesofcon-
tact,perception, understanding andacceptance ofutterances mayberaisedandaddressed.
Partsofthisaccountwereimplemen tedin IBi S2,allowingthesysteme.g.toraiseunder-
standing questions regarding theuser'sinput(e.g.\To Paris,isthatcorrect?"). Thisis
acaseofexplicitly raisingtheunderstanding-question whichresultsinthisquestion being
underdiscussion.
Thesystemcouldalsoproducepositiveexplicitfeedback(e.g.\To Paris");thiskindof
feedbackdoesnotexplicitly raisetheunderstanding question, andthereisnoobligation
ontheusertorespondtoitbeforethedialogue canproceed. However,itcanbeargued
thatevenpositivefeedbackraisesgrounding-related issues,although notexplicitly .This
isgivensomesupportfromthefactthatitispossiblefortheusertoprotestagainstthe
system's feedbackincasethesystemgotsomething wrong.

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION183
According to Ginzburg, anassertion canbefollowedbyanyutterance addressing the
acceptance ofthisquestion asafact,e.g.bysaying\no!".Thisisthenregarded asa
shortanswertotheacceptance question; ineffect,arejection. Inthecaseofanassertion
addressing understanding (i.e.positiveunderstanding feedback),theacceptance question
canbeparaphrased \Isitcorrectthatyoumeant'to Paris'?".Thatis,theacceptance-
question regarding thesystem's understanding isexactlythesamequestion whichisraised
explicitly byaninterrogativ efeedbackutterance.
In IBi S,wehavechosennottorepresentacceptance-questions explicitly; however,inthe
caseofpositiveexplicitgrounding therearegoodreasonstodoso. Positivefeedbackhas
theadvantageofincreased efficiency compared tointerrogativ efeedback,butthedisad-
vantageisthattheuserisnotabletocorrectthesystem's interpretation. However,ifthe
positivefeedbackmoveimplicitly raisesthequestion whether thesystem's interpretation
wascorrect,wecanusethistoallowtheusertorejectfaultysysteminterpretations. Be-
sides,wealreadyhavemechanisms inplaceforrepresentinganddealingwithanswersto
theunderstanding-question.
Tomodelthefactthattheacceptance question regarding understanding isimplicitrather
thanexplicit, wepushitontothelocal QUDonly. Iftheuseraddresses it(e.g.bysaying
\no"),theimplicit issueis\openedup",i.e.itbecomesanopenissue;itispushedon
ISSUES.
(rule 4.9)rule:accommodate QUD2Issues
class:accommodate
pre:8
>>><
>>>:$/private/nim/elem/snd=answer(A)
in($/shared/qud,Q)
$domain ::relevant(A,Q)
notin($/shared/issues,Q)
eff:n
push(/ shared/issues,Q)
Therulein(rule 4.9)picksoutanon-integrated answer-movewhichisrelevant toa
question on QUDwhichisnotcurrentlyanopenissue,andpushesitonissues.
Tohandleintegration responsestopositiveunderstanding feedback,wealsoneedtomod-
ifytheintegrate Neg Icm Answ erruledescribedin Section 3.6.6. Asignifican tdifference
betweenpositiveandinterrogativ efeedbackin IBi Sisthattheformerisassociatedwith
cautiously optimistic grounding, whilethelatterisusedinthepessimistic grounding strat-
egy. Thismeansthatanegativeresponsetofeedbackontheunderstanding levelmustbe
handled differentlydependingonwhether thecontentinquestion hasbeenaddedtothe
dialogue gameboardornot. Specifically,ifthepositivefeedbackisrejected theoptimistic
grounding assumption mustberetracted.

184 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(rule 4.10) rule:integrate Neg Icm Answ er
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
Therulein(rule 4.10)issimilartothoseforintegrating \normal" useranswers(see Sec-
tion 3.6.6),becauseofthespecialnatureofgrounding issues,weincludeissuedowndating
intheruleratherthanaddingafurtherrulefordowndating issuesforthisspecialcase.
Thismeanstherulehastocheckthattheanswerresolvesthegrounding issue,ratherthan
merelycheckingthatitisrelevant;thisisdoneinthethirdcondition. Thecontentresult-
ingfromcombiningtheissueon QUDandtheansweriscomputed inthefifthcondition.
Finally,thesixthcondition checksthatthecontentisnot(und( DP*C))where DPisa DP
and Cisthecontentthatisbeinggrounded (orinthiscase,notgrounded).
Thesecondupdateremovesthegrounding question fromissues. Thethirdupdatefirst
checksif Chasbeenoptimistically grounded. Inthiscase,theoptimistic grounding as-
sumption regarding thegrounding of Cisretracted. Thisiswherethenewtmp/usr field,
containingrelevantpartsoftheinformation stateastheywerebeforethelatestuserutter-
ancewasoptimistically assumed tobegrounded, isused. If Chasnotbeenoptimistically
assumed tobegrounded, nothinginparticular needstobedone.
Thefourthupdateaddspositivefeedbackthatthesystemhasundersto odthat Cwasfalse.
Notethatnot(C)isnotaddedto/shared/com .Thereasonforthisisthatthenegated
propositionisnotsomething thattheuserintendedtoaddtothe DGB-itwassimplya
resultofamisunderstanding bythesystem.

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION185
Notealsothatthisfeedbackwillnotraiseagrounding issueaccording tothedefinition of
question-raising ICMin Section 3.7.1. Sincethecontentnot(C)hasnotbeenaddedto
theinformation state,thereisnopointindealingwithgrounding.
Thefinaltwoupdatesclearthenimqueue,whichmeansthatthesystemwilldisregard any
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
Whenintegrating theuser's\no"(anegativeresponsetosystem ICM),theanswer-moves
realizedintheutterance \flighttoparis"arediscarded;. Thesystemhastriedtomake
senseofitbuttheuserrejectedthisattempt. Atthispoint,thesystemsimplycannotdeal
withthemandratherthangettingstuckintryingtofigureoutwhattheusermeant,the
movesarethrownout.
Notethattheruleasimplemen tedisactually moregeneralthanwhatisneededfor(or
usedin)IBi S3. Sincethepartoftmpthatitbacktrackstodependsonthe DPvariable,
inprinciple itcouldbeusedforcaseswheretheusergivespositivefeedbackandthesystem
rejectsthisasmistaken.
Asampledialogue withanegativeresponsetoanimplicitgrounding question isshownin
(dialogue 4.10).
(dialogue 4.10)
S>Welcome tothetravelagency!
U>visainformation please(0.78)(useractually saidsomething else)
get Latest Mo ves
backup Shared Usr
integrate Usr Ask

186 CHAPTER 4. ADDRESSING UNRAISED ISSUES
find Plan
downdate QUD
backup Shared Sys
select Icm Other
select Icm Other
S>Okay. Youwanttoknowaboutprice.
get Latest Mo ves
integrate Other ICM
integrate Und P os ICM
2
666666666666666666666666666666666666664 private=2
6666666666666666666666664 agenda=­­
icm:loadplanffff
plan =*findout(?A.how(A))
findout(?B.destcity(B))
findout(?C.deptcity(C))
findout(?D.month(D))
findout(?E.deptday(E))
findout(?F.class(F))
consult DB(? G.price(G))+
bel =fg
tmp =2
66664 usr=2
66664 com =fg
qud =hi
issues =hi
agenda=hhii
plan =hi 3
777753
77775
nim =hhii 3
7777777777777777777777775
shared =2
666666664 com =fg
issues =­
?H.price(H)ff
qud =­
und(usr*issue(?I.price(I)))ff
pm =©ask(?H.price(H))ª
lu =2
4 speaker =sys
moves =½icm:und*p os:usr*issue(?I.price(I))
icm:acc*p os¾3
53
7777777753
777777777777777777777777777777777777775
U>no
get Latest Mo ves
accommo date QUD2Issues©
push(/ shared/issues,und(usr*issue(?A.price(A))))
integrate Neg Icm Answ er

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION187
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
downdate QUD
2
666666666666666666666666664 private=2
666666666666664 agenda=¿¿
icm:loadplan
icm:und*p os:usr*not(issue(? A.price(A)))ÀÀ
plan =hi
bel =fg
tmp =2
66664 usr=2
66664 com =fg
qud =hi
issues =hi
agenda=hhii
plan =hi 3
777753
77775
nim =hhii 3
777777777777775
shared =2
6666664 com =fg
issues =hi
qud =hi
pm =©
icm:und*p os:usr*issue(?A.price(A)),icm:acc*p osª
lu =·speaker =usr
moves =©answer(not(und(usr *issue(?A.price(A)))))ª¸3
77777753
777777777777777777777777775
backup Shared Sys
select Icm Other
S>Youdidnotaskaboutprice.
Feedbackforutterances realizingseveralmoves
Inthecasewhereauserutterance providesanswerstoseveralquestions (andperhaps
alsoasksaquestion), thestrategy wehavechosenistoproducefeedbackforeachmove
individually togivetheuserachancetocorrectmishearings ormisunderstandings. If
positivefeedbackregarding onepieceofinformation isrejected, theoptimistic assumption
isretracted bymodifyingtheinformation stateaccording tothe/private/tmp/usr saved
state. Iffeedbackregarding onepieceofinformation isaccepted, thisinformation should
notdisappearifalaterfeedbackutterance fromthesystemshouldberejected.

188 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(dialogue 4.11)
S>Welcome tothetravelagency!
U>priceinformation please
S>Okay. Ineedsomeinformation. Howdoyouwanttotravel?
U>aflighttoferris[0.78]
S>Okay.byflight.
U>yes
S>toparis.
U>no
S>nottoparis. So,whatcitydoyouwanttogoto?
Forexample, inthedialogue in(dialogue 4.11),theuseracceptsthesystem's feedback
\byflight",butrejects\toparis";however,theinformation thattheuserwantstotravel
byflightisretained.
Tohandlethis,eachtimepositivefeedbackisaccepted, thepartsofthe/private/tmp/usr
structure correspondingtotheshared fieldaremodified. Afurthermodification isthus
neededfortheintegrate Pos Icm Answ errulepreviously definedin Section 3.6.6.

4.6. VARIETIES OFQUESTION ACCOMMOD ATION ANDREACCOMMOD ATION189
(rule 4.11) rule:integrate Pos Icm Answ er
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
issuesinsteadofqud. Thefirsttwoupdatesarealsothesame. Thethirdupdateaddsthe
content Contentwhichisbeinggrounded totmp/usr (incase DPisusr,whichitalways
isin IBi S3).Thismeansthatiffuturefeedback(concerning thesameutterance) fromthe
systemisrejected, thesystemwillbacktracktoastatewhere Contentisintegrated. The
conditionals inthethirdandfourthupdatesreflectthefactthatquestions areintegrated
differentlyfrompropositions. Thefourthupdateissimilartothethirdupdateinthe
previous versionoftherule.
Implicitacceptance
Beforewemoveonthereisonemorethingtoconsider. Iftheuserdoesnotrejectthe
system's positivefeedbackconcerning apieceofinformation, thisisregarded asanimplicit
acceptance. Therefore, wealsoneedtoaddano Followuprule,forcaseswherepositive
systemfeedbackisnotrespondedtoatall(i.e.theuserdoesnottaketheturnoffered).

190 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(rule 4.12) rule:no Followup
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
Thefirstcondition istrueonlyiftheuserdidnotproduceanyutterance (thatthesystem
heard)duringherlatestturn 11. Thesecondcondition checksthatthemovesperformed in
theprevious utterance includes positiveunderstanding feedbackregarding Content. The
firstupdatesareidenticaltothethirdupdateintheintegrate Pos Icm Answ errulein
Section 4.6.7.
Belowisadialogue example involvingpositive,implicitpositive,andnegativefollowups
tosystemfeedback.
(dialogue 4.12)
S>Welcome tothetravelagency!
U>priceinformation please
S>Okay. Letssee. Howdoyouwanttotravel?
U>aflighttoparisinapril
S>Okay.byflight.
U>yes
S>toparis.
U>
S>inapril.
U>no
S>notinapril. Whatcitydoyouwanttogoto?
Implicitquestions andellipticalanswers
Inthecaseofimplicitacceptance questions in English(and Swedish)itappearsthatthey
canbeaddressed byshortanswers;however,wecannotassumethatallimplicit issues
canbeaddressed elliptically .Theuseof QUDforstoringimplicitissuesreliesonthefact
11See Section 3.6.6 foranexplanation of'TIMEDOUT'.

4.7. FURTHER IMPLEMENT ATION ISSUES 191
thatquestions on QUDhavenotnecessarily beenraisedexplicitly; however,questions on
QUDarealsobydefinition availableforresolution ofshortanswers. Torepresentimplicit
questions whichcannotbeaddressed elliptically ,afurtherlocaldatastructure forimplicit
questions underdiscussion wouldbeneeded.
4.7 Furtherimplementationissues
Inthissectionwedescribepartsoftheimplementationof IBi S3 whichhavenotbeen
discussed earlierinthischapter,andwhicharenotdirectlyreusedfrom IBi S2.
4.7.1 Dialogue moves
For IBi S3,onlyonedialogue movehasbeenadded:ICMindicating accommodationofa
dependentissue. In English, wehavechosen\alright,youwanttoknowabout:::"toindi-
catethatsomeinference hasbeenperformed, andthatithasbeensuccessful. Thischoice
isbasedontheintuitionthatthisindicates someprocessinference whichhasconcluded
successfully; thisshouldberegarded asapreliminary andtemporarysolution awaiting
furthercorpusandusabilitystudies.
²icm:accommo date:Q:Moveif Q:Question
4.7.2IBi S3 updatemodule
Updaterules
Themainadditions totheupdaterulecollection neededtohandleaccommodationand
reaccommodationweredescribedabovein Section 4.6.
Inthissection, wedescribechangesappliedtootherrulesfrom IBi S2 tofitwiththe
modifiedinformation stateusedby IBi S3.

192 CHAPTER 4. ADDRESSING UNRAISED ISSUES
Backinguptmp/usr
Thetmp/usr fieldcontainscopiesofpartsoftheinformation stateastheywerebefore
thelatestuserutterance wasintegrated. Iftheoptimistic assumption shouldturnoutto
bewrong,thetmp/usr fieldisusedtoundotheoptimistic grounding assumption without
theneedforcomplex revisionprocessing(see Section 4.6.7).
Thebackup Shared Usr in(4.8)iscalledeachtimeanutterance istobeintegrated and
storesthecurrentqud,issues,com,planandagendafields;theseareallpotentially
affectedbytheintegration ofthemovesinthelatestutterance, andarealsoimportantfor
determining whattodonext.
Thisbacktrackingmechanismonlyappliestodomain-levelcommunication; user ICMmoves
arealwaysoptimistically assumed tobecorrectly understo odandintegration alwayssuc-
ceeds. Since ICM\subdialogues", suchasthatin(dialogue 4.13)areusedtoestablish
thefactthataprevious userutterance wasmisundersto odbythesystem,itisimportant
thattmp/usr isnotoverwritten duringthesubdialogue. Forexample, thebackup Share-
d Usrruleshouldnottriggerbeforeintegrating theuser's\pardon" ortheuser'sanswer
\no"tothesystem ICM\byboat".
(dialogue 4.13)
S>Okay. Letssee. Howdoyouwanttotravel?
U>byboat[0.76](useractually saidsomething else)
S>Okay.byboat.
U>pardon?
S>Okay.byboat.
U>no
S>notbyboat. So,howdoyouwanttotravel?

4.7. FURTHER IMPLEMENT ATION ISSUES 193
(rule 4.13) rule:backup Shared Usr
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
Thefirstcondition checksthatthelatestspeakerwasindeedtheuser;ifnot,therule
shouldofcoursenottrigger. Thenextfourconditions areusedtopreventtriggering in
caseofan ICMsubdialog,i.e.iftheuserproducedan ICMmoveorrespondedtoonefrom
thesystem.(Notethatnomovemaycountasimplicit ICMiftheuserdoesnotrespondto
ICMfromthesystem;see Section 4.6.7).Thefifthcondition checksiftheuserutterance
containsananswerrelevanttoagrounding-question on QUD. Theeffectssimplycopythe
contentsoftmp/usr tothecorrespondingpathsintheinformation state.
Integration rulesandnim
In IBi S2,theintegration rulesinspectnimusingthecondition in(/private/nim,Moves).
Since Trindi Kit usesbacktrackingtofindinstantiationsofvariablesinconditions (see
Appendix A),thisresultsineachintegration rulelookingthroughthewholequeueofnon-
integrated moves. Thus,in IBi S2 theordering oftheintegration rulesdetermines which
moveisintegrated first. Thisisokayfordialogues withaverysimplestructure, butwhen
dialogues becomemorecomplex (e.g.becauseofaccommodation), theordering ofthe
movesbecomesmoreimportant.
Therefore, in IBi S3 allintegration rulesinspectonlythefirstmoveonthenimqueue,using
thecondition fst(/private/nim,Move)orsimilar. Incombination withthequeue-shifting
techniquedescribedin Section 4.7.2,thismeansthatthealgorithm triestointegratemoves
intheordertheywereperformed.

194 CHAPTER 4. ADDRESSING UNRAISED ISSUES
Updatealgorithm
Because ofthemorecomplex dialogues handled by IBi S3,theupdatealgorithm isabit
morecomplex thanthatfor IBi S2.
(4.8)1 ifnot($latestmoves==failed)
2 thenhget Latest Mo ves,
3 trybackup Shared Usr ,
4 tryirrelevant Followup,
5 repeath
6 repeat(hintegrate,
7 trydowndateissues,
8 tryremove Findout ,
9 tryloadplani,
10 orelseapplyshift(/private/nim))
11 untilfullyshifted($ /private/nim),
12 applyshift(/private/nim),
13 tryselectaction
14 accommodatei,
15 applycancelshift(/private/nim ),
16 repeatexecplan,
17 trydowndatequdi
18 elsehfailed Followuporelseunclear Followupi
Line 1 checksthattheinterpretation ofthelatestutterance wassuccessful (ofcourse,in
thecaseofsystemutterances thisisalwaystrue).Ifnot,thefailed Followupandun-
clear Followuprulesinline 18,describedin Section 3.6.8,aretried. Ifinterpretation
wassuccessful, thelatestmovesareincorporatedintheinformation stateproperbythe
get Latest Mo vesrule(see Section 3.6.7).Afterthisthebackup Shared Usr ruleistried;
itsconditions aresatisfied, therulewilltriggerandstoreacopyofrelevantpartsofthein-
formation stateincasethesystemmakesanoptimistic grounding assumption whichturns
outtobemistaken(see Section 4.7.2).Also,beforeintegration starts,theirrelevant Fol-
lowupruledescribedin Section 3.6.8 istriedtocatchcaseswhereasystemquestion has
beenignoredbytheuser.
Afterthis,aloopinvolvingintegration andaccommodationisexecuted untilnothingmore
canbeintegrated (i.e.untiltheloopcannolongerbeexecuted). Thebasicideaisthis:
firsttrytointegrateasmanymovesaspossiblebycyclingthrough thenimqueue;then,
ifaccommodationcanbeapplied, dothesamethingagain. Repeatthisuntilnothingcan
beintegrated andnoaccommodationispossible.

4.7. FURTHER IMPLEMENT ATION ISSUES 195
Thefirstpartofthisloopstartsinline 6 andisitselfaloopforcyclingthrough allnon-
integrated movesandtryingtointegratethem. Ifintegration succeeds, thealgorithm tries
toremoveanyresolvedissuesfromissuesandplan,andifnecessary loadanewplan
(e.g.ifanaskmovefromtheuserwasintegrated). Thenittriesintegration again. If
integration fails,thenimqueueisshiftedonestep,i.e.thetopmost elementisremoved
fromthetopandpushedtotheendofthequeue. Then,integration istriedagain. This
continuesuntilthequeuehasbeencompletely cycledthrough once,andallmoveshave
hadashotatbeingintegrated.
Afterthisloopisfinished, accommodationwillattempt toadjustthe/shared fieldso
thatanymovesstillnotintegrated maybeundersto odonthepragmatic level,andinte-
grated. However,weneedtoavoidaproblem thatarisesasaconsequence ofhavingthe
integration ruleshandlepragmatic understanding, acceptance, andintegration inasingle
step. Theproblem arisesifsomemoveisregarded asrelevant(i.e.understo odonthe
pragmatic level)butnotacceptable, orifarelevantmovehaslowreliabilityandshould
beverifiedbeforebeingintegrated. Inthiscase,accommodationshouldnotbetriedsince
thepurposeofaccommodationistounderstand someutterance onthepragmatic level,
andthishasalreadybeenachieved. Tosolvethisproblem, someactionselection rules(of
classselectaction)havebeenmovedfromtheselection moduletotheupdatemodule(for
alistoftheserules,see Appendix B).Beforetryingaccommodation,line 13 oftheupdate
algorithm thustriestoselectrejection movesandinterrogativ efeedbackmovestocatch
anymoveswhichhavealreadybeenundersto od.
Line 14 callstheaccommodationruleclass. Ifthissucceeds, thereisachancethatsome
movesthatcouldnotbeintegrated beforecannowbeintegrated, sotheloopstarting in
line 6 isrestarted. Whennothingcanbeintegrated andnothingcanbeaccommo dated,
thesequence startingatline 6 andendingatline 14 cannotbeexecuted, andconsequen tly
theloopstartedinline 5 willbefinished. Line 15 cancelsshiftingofthenimqueue(see
Section A.2.1).
Anyloadedplanisexecuted inline 16 byrepeatedlyapplying theexecplanruleclass
untilnomoreexecution ispossibleatthecurrentstageofthedialogue. Finally,QUDis
downdated.
Asanexample ofhowintegration andaccommodationinteract,inthedialogue in
(dialogue 4.14),\toparis"isintegrated beforeaccommodationistried,sotheonly
question availableforellipsisresolution of\paris"istheoneconcerning departure city.
(dialogue 4.14)
S>Welcome tothetravelagency!
U>pricelondontoparis[0.78]

196 CHAPTER 4. ADDRESSING UNRAISED ISSUES
S>Okay. Youwanttoknowaboutprice.
S>Ineedsomeinformation. toparis.
S>fromlondon.
S>Howdoyouwanttotravel?
Accommo dationruleordering Fortheaccommodateruleclass,theordering inwhich
thevariousaccommodationrulesaretriedmaybeimportantinsomecases. Theordering
usedin IBi S3 isshownin(4.9).
(4.9)accommodate
1.accommodate Issues 2QUD
2.accommodate QUD2Issues
3.accommodate Plan 2Issues
4.accommodate Com 2Issues
5.accommodate Com 2Issues Dep endent
6.accommodate Dependent Issue
Thisorderinwhichtotrytheaccommodationruleshasbeenchosenbasedonintuitions
abouthowaccessible questions aredependingonwheretheyareretrieved. Byexperiment-
ingwiththeordering, differentbehaviourscanbeobtained. Thecurrentordering should
beregarded asprovisional, andfindingthe\best"ordering isanobjectforfutureresearch.
Itmayalsosometimes benecessary todoclarification ifananswermatchesseveralques-
tionswhoseaccommodationruleshavethesameornearlythesamepriority;thishasnot
beenimplemen tedin IBi S3.
Possiblecriteriaforjudgingwhetheroneordering isbetterthananotherare(1)howreason-
abletheresulting behavioursare,(2)howefficienttheoverallprocessingbecomes,and(3)
howsimilartohumancognitiveprocessescorrespondingtoaccommodationtheprocessing
is(assuming question accommodationiscognitivelyplausible).
First,accommodationinvolvingonlyissuesandqudistried,sincethesearethecentral
structures fordealingwithquestions. Ifthisfails,accommodationfromthedialogue plan
istried;ifthisfails,reaccommodationfromcomisattempted. First\normal" reaccom-
modation,thendependentreaccommodation. Finally,dependentissueaccommodationis
tried;thisistriedlastsinceitfindsthequestion inthedomainresource ratherthanthe
information stateproper.

4.8. DISCUSSION 197
4.7.3 Selection module
Theselection moduleisalmostunchangedfrom IBi S2. Someminoradjustmen tshavebeen
madetoadapttherulestothechangesintheinformation statetype:thatobjectsinnim
arepairsof DPsandmoves,andthattmpisdividedintotwosubstructures.
4.8 Discussion
Inthissectionwediscusssomevariations on IBi S3,showsomeadditional \emergen t"
features, anddiscussvariousaspectsofquestion accommodation.
4.8.1 Phrasespottingandsyntaxinflexibledialogue
Asitturnsout,IBi S3 sometimes runsintotroubleiftheinterpreter recognizes several
answerstothesamequestion inanutterance. Whereas IBi S2 wouldsimplyintegratethe
firstanswerandignorethesecond, IBi S3 willtrytomakesenseofallthemovesinan
utterance, whichmayleadtoproblems iftheaccommodationrulesarenotdesigned to
coverthecaseathand.
Forexample, ifthesystemrecognizes \paristolondon" asafirstutterance inadialogue,
thesystemwilltrydependentissueaccommodation(see Section 4.6.4)andnotethatthe
setofanswers(answer(paris)andanswer(destcity(london) ))is(indirectly) relevantto
boththepriceissueandthevisaissue. Itmightseemthatthisiswrong,sincethetwo
answersareinfactrelevanttothesamequestion (regarding destination city)inthe\visa"
plan,whereas itisrelevanttotwoseparate questions (destination anddeparture city)in
the\price"plan,soitshouldbeindirectly relevantonlytothe\price"issue. Butin
general, onecannotrequirethatthetwoanswersmustbeanswerstodifferentquestions,
sincethesecondanswermaybeacorrection ofthefirst. Thismayofcoursebesignalled
moreclearly,asin\toparisuhnotolondon", butthecorrection signalsmaybeleftout,
inaudible, ornotrecognized.
Onewaytosolvethisproblem istosometimes lookforconstructions whichrealizemore
thanonemove,anddosome\cleaning up"intheinterpretation phasesothatthe DME
willnotgetintotrouble. Forexample, wecanaddalexicalentrylookingforphrases
oftheform\Xto Y"andinterpretthisas\from Xto Y",i.e.answer(deptcity(X))
andanswer(destcity(Y)).
Arelatedproblem occursiftheuserfirstchooses Gothenburgasdeparture cityandthen

198 CHAPTER 4. ADDRESSING UNRAISED ISSUES
says\notfromgothenburg london".Sinceplan-to-issues accommodationhasprece-
denceovercom-to-issues, \london" willbeintegrated firstbyaccommo datingthedes-
tination cityquestion, whichiswrong. Onesolution isofcoursetogivecom-to-issues
accommodationprecedence, butthenfor\parisfromlondon",\fromlondon"willfirst
beintegrated andthen\paris"willbeseenasarevisionofthedeparture city,whichis
alsowrong.
Asmentionedbeforein Section 4.7.2,theexactprecedence ordering betweenaccommo da-
tionrulesisatopicforfutureresearch,anditmaysometimes benecessary todoclarification
ifananswermatchesseveralquestions whoseaccommodationruleshavethesameornearly
thesamepriority. However,aneasiersolutionistoaddafurtherinterpretation rulesaying
that\not PX,Y"shouldbeinterpreted asaparaphrase of\not PX,PY".
Aslightlyirritating butnotveryserious\bug"in IBi Soccursifauserutterance contains
twoanswerstothesamequestion (e.g.\tokualalumpurtolondon"), andthefirstof
theseisaninvaliddatabase parameter. Thefirstanswerwillberejected, andappropriate
feedbackwillbeputontheagenda. Thesecondanswerwillthen(correctly) replacethe
firstanswerusingretraction, buttherejection feedbackconcerning thenowreplaced first
answerremains ontheagenda. Thismeansthatthesystemwillgivesomeirrelevant
information, namelythatthefirstanswerwasrejected. Thiscanbefixedtosomeextent
byinterpreting phrasesoftheform\PXPY"as\PY",i.e.thesecondpartisregarded as
acorrection ofthefirstpart. Similarly ,phrasesoftheform\PXno(P)Y",where\no"
isregarded asacorrection indicator andthesecond Pisoptional, canalsobeinterpreted
as\PY".Ingeneral,itisusefultodetectcorrections intheinterpretation phasetoavoid
potentiallyexpensiverevisions intheintegration phase.
Ofcourse,thesesimplefixeswillonlygetussofar,sincetheyonlycapture thevery
simplest cases. Forexample, wewouldnotbeabletonoticethatanutterance contains
twoanswerstothesamequestion unlesstheyareadjacent. Whatisreallyneededhereis
aproperparser(e.g.a HPSG-based parser)andgrammar.
Whatthisshowsus,then,isthattakingsyntaxintoaccountininterpretation becomes
increasingly importantwhenthedialogue managementbecomesmoreflexible. Thismight
notbeverysurprising, butbystartingoutwithverysimplekeywordspottingandkeeping
itaslongaspossible,wefindoutexactlywhereitbecomesinsufficien t. Hadweuseda
sophisticated parserfromtheoutset,wewouldnothavehadthisinsight.

4.8. DISCUSSION 199
4.8.2 Relaxing constrain tsusingdenialanddependentreaccom-
modation
Ininquiry-orienteddialogue itisoftenusefultobeabletorelaxconstrain tsonthedatabase
search,especiallyincaseswherenoresultisreturned fromthedatabase. Asitturns
out,existingaccommodationmechanisms in IBi S3 incombination withtheslightlymore
complex database resultformatwhichwasintroducedasanextension of IBi S2(see Section
2.12.4)providesawayofdoingexactlythis.
Theideaisthis:ifthesystemreturnsanemptyorotherwise unsatisfactory database result,
theusercanmodifytheinformation giventothesystembydenyingsomepartofit. This
triggersreaccommodationofthedependentissuethatthedatabase searchtriedtofindan
answerto,andthecorrespondingplanisreloaded. Sincesomeinformation isnowmissing,
thesystemwillagainaskforit;therestoftheactionsintheplanwillberemovedsincethe
questions havealreadybeenanswered. Byrejecting therepeatedquestion (e.g.bysaying
\Itdoesn'tmatter" or\Idon'tknow"),theusermakesthesystemsearchthedatabase
again,butthistimewithrelaxedconstrain ts.
(dialogue 4.15)
S>Welcome tothetravelagency!
U>aflighttoparisfromgothenburg inapril
S>Alright. Youwanttoknowaboutprice.
S>Letssee. Okay. Whatdaydoyouwanttoleave?
U>thefifth
S>Okay. Whatclassdidyouhaveinmind?
U>business class
$S>Okay. Sorry,thereisnothing matching yourrequest aboutprice.
U>okay,notbusiness classthen
S>Youwanttoknowaboutprice.
$S>Letssee. Okay. So,Whatclassdidyouhaveinmind?
U>itdoesntmatter
S>Thepriceis 7654 crowns. economy class.
Theexample in(dialogue 4.15)illustrates theprinciple. Tomakethisfeaturemore
useful,onewouldneedtobeabletogivedisjunctiv eanswers(\Iwanttoleaveonthe
twenty-firstorthetwenty-second"), specifyarangeofallowable\parameter values"(\I
wanttoleavebetweenthetwenty-firstandthetwenty-fifth"), andgiveanswerswhichare
unspecificinrelationtothequestion (\Iwanttogoto France"inresponseto\Whatcity
doyouwanttogoto").Ofcourse,thisisausefulfeaturealsowhenprovidinganswersin
theinitialdatabase queryspecification stage. Thisisanareaforfurtherimplementation.

200 CHAPTER 4. ADDRESSING UNRAISED ISSUES
Thenicethingaboutthisapproachtorelaxing constrain tsisthatitrequires nospecial
machinery,butitemerges asapossibilitygivenmechanisms whichareindependentlymo-
tivated.
4.8.3\Smart" interpretation
Thedialogues in(dialogue 4.16)and(dialogue 4.17)showhowtheintegration strategy
in IBi S2 isabletousealltheinformation providedinanutterance ascluesforhow
tointerpretunderspecifiedinformation. Theinterpretation of\paris"asdestination or
departure citydependsonwhatotherinformation isgivenintheutterance, specifically
whether destination ordeparture cityisspecifiedelsewhere intheutterance.
(dialogue 4.16)
U>priceinformation please
S>Okay. Letssee. Howdoyouwanttotravel?
U>parisfromlondon[0.78]
S>Okay.fromlondon.
S>toparis.
(dialogue 4.17)
U>priceinformation please
S>Okay. Letssee. Howdoyouwanttotravel?
U>paristolondon[0.78]
S>Okay.tolondon.
S>fromparis.
Thesampledialogue in(dialogue 4.18)showshowthesystemcanintegratesuccessive
hintsfromtheuseraboutwhatshewantstodo.
(dialogue 4.18)
S>Welcome tothetravelagency!
U>umiwouldliketogotoparis
S>toparis. Idontquiteunderstand. Doyoumeantoaskaboutvisaorto
askaboutprice?
U>umiwanttogobyflight
S>Alright. Youwanttoknowaboutprice.

4.8. DISCUSSION 201
4.8.4 Separating understanding, acceptance, andintegration
Theintegration rulesin IBi S3 performseveraltasks:contextualinterpretation (e.g.for
underspecifiedanswers),deciding whether toacceptorrejectamoveandtheircontents,
and(ifacceptance isdecidedon)integration ofthefulleffectsofthemove. Whilethis
wasagoodapproachin IBi S1 and IBi S2,in IBi S3 thisapproachsometimes obscures the
workingsofthesystemandmakerulesrathercomplex.
Analternativ eapproachwouldbetoimplemen tcontextualinterpretation, theaccep-
tance/rejection decision, andintegration asseparate ruleclasses. Thecontextualinter-
pretation ruleswouldtakemovesoffaqueueofmovesprovidedbytheinterpretation
module(correspondingtothecurrentnimfield);wecouldcallthisqueueofpossiblyun-
derspecifiedmoves SUM(Semantically Understo od Moves).Theresulting fullyspecified
movescouldthenbeaddedtoa PUM(Pragmatically Understo od Moves)queue,which
wouldserveasinputfortheacceptance/rejection decision rules. Rejected moveswould
beputona RM(Rejected Moves)queue,whichwouldlaterbeinspectedintheselection
phasetoproducesuitablefeedback. Accepted moveswouldbeaddedtoan AM(Accepted
Moves)stack,whichinturnwouldserveasinputtotheintegration rules. Whilethiswould
probably requirealargernumberofrulesandalsosomeadditional datastructures inthe
information state,thecomplexit yoftheindividual rulescouldbegreatlyreducedandthe
clarityoftheoverallprocessingwouldimprove. Itisalsolikelythatthiswouldleadtoa
lessbug-prone andtheoretically moresatisfying implementation.
4.8.5 Accommo dationandthespeaker'sownutterances
Inthischapterwehavebeenmainlyconcerned withissueaccommodationasawayof
interpreting utterances fromtheother DP(foradialogue system,theuser).Buthowdoes
accommodationrelatetothegeneration andintegration ofone'sownutterances? This
issuesdoesnotcomeupin IBi Ssincethesystemneverproducesutterances thatcanbe
expectedtorequireaccommodationonthepartoftheuser(e.g.endingalongdialogue
with\$100"ratherthan\Thepriceis$100").
Ginzburg allowsthespeakertoupdate QUDwithaquestion andthenaddressit. This
will(probably) requireaccommodationonthepartofthehearer. Thesequence ofevents
hereisroughlythefollowing(Sisthespeaker,Hthehearer):
²Spushes Qon QUD,thenaddresses Q
²Sintegrates A

202 CHAPTER 4. ADDRESSING UNRAISED ISSUES
²Haccommo dates Q,integrates A
However,wehavenotedabovein Section 3.3.4 thatthisseemsinconsisten twiththeview
of QUDassomething thatisassumed tobeshared. Possibly,onecouldhavea\fuzzier"
conceptof QUD(andperhapsthe DGBingeneral) thatleavessomefreedom ofmodifying
itprivately,aslongasthehearercanbeexpectedtoaccommo datethesemodifications.
Theotheralternativ eistoallowthespeakertogenerate utterances thatdonotexactly
matchthecurrentinformation state,andthenperformaccommodationtointegrateher
ownutterance. Inthiscase,thesequence ofeventsisinstead:
²Saddresses Q,believingthattheinformation statecanbeadjusted (usingaccom-
modation)soastomakethisutterance felicitous
²Sand Haccommo date Qandintegrate A
Whether thechoicebetweenthesetwoapproachesmakeanyrealdifference totheinternal
processingand/orexternal behaviourofthesystemremains afutureresearchissue. For
example, if QUDisupdatedwith Qbefore Aisproduced,andtheutterance realizing A
isinterrupted, should Qberemovedfrom QUD?
4.8.6 Accommo dationvs.normalintegration
Aswehaveseen,question accommodationallowsageneralized accountforhowanswers
areintegrated intotheinformation state,regardless ofthestatusofthecorresponding
question. Theaccommodationproceduremayalsohaveside-effects (e.g.loadinganew
dialogue plan)whichservetodrivethedialogue forward.
Insteadofgivingrulesforaccommodationandintegration separately ,onecoulddenythe
existence ofaccommodationandjustgivemorecomplex integration rules. Theintegration
ruleforshortanswersrequires thatthereisaquestion onthe QUDtowhichthelatest
moveisanappropriate answer,andtheaccommodationrulesareusedifnosuchquestion
canbefound. Thealternativ eistoskipthe QUDrequiremen t,thusincorporatingthe
accommodationmechanisms intotheintegration rule,whichwouldthensplitintoseveral
rules. Forexample, therewouldbeoneruleforintegrating answersbymatchingthemto
questions intheplandirectly.
Apartfromthetheoretical argumen tthatquestion accommodationprovidesageneraliza-
tionofthewayanswersareintegrated, therearealsopractical motivations. Inparticular,

4.9. SUMMAR Y 203
thefactthatseveralstepsofaccommodationmaybenecessary tointegrateasingleanswer
meansthatthetotalnumberofrulesforintegrating answerswouldbehigherifaccom-
modationwasnotused-onewouldneedatleastoneintegration ruleforeachpossible
combination ofaccommodationrules.
Afurtherargumen twhichisnotexplored inthisthesis(butsee Engdahl etal.,1999)is
thatquestion presuppositionandaccommodationinteractwithintra-sententialinformation
structure ininteresting andusefulways.
4.8.7 Dependentissueaccommodationin Voice XML?
Onaclosereadingofthe Voice XML specification (Mc Glashan etal.,2001),itmayap-
pearthat Voice XML offersamechanismsimilartodependentissueaccommodation 12. In
Voice XML, agrammar canhavescopeoverasingleslot,overaform,oroverawhole
document(containingseveralforms).Givenagrammar withdocumentscope(defining a
setofsentenceswhichthe Voice XML interpreter willlistenforduringthewholedialogue),
iftheusergivesinformation whichdoesnotmatchthecurrentlyactiveform,Voice XML
willjumptoaformmatchingtheinput 13. Thiscorrespondsroughlytothedependentissue
accommodationmechanismin IBi S. However,ifinputmatchesmorethanonetask(e.g.
\raisethevolume"couldmatchataskrelatedtothe TVoronerelatedtothe CDplayer),
Voice XML willnotaskwhichofthesetaskstheuserwantstoperformbutinsteadgoto
theoneitfindsfirst,regardless ofwhattheuserintended. Generally ,itishardtoseehow
clarification questions couldbehandled inageneralwayin Voice XML, sincetheydonot
belongtoaparticular form.
4.9 Summary
Toenablemoreflexibledialogue behaviour,wemadeadistinction betweenalocaland
aglobal QUD(referring tothelatteras\openissues",orjust\issues"). Thenotionsof
12Thisdiscussion isbasedonthe Voice XML specification ratherthanhands-on experienceof Voice XML.
Thismeansthatsomeunclarityremains aboutthecapabilities of Voice XML ingeneral, andindividual
implementationsof Voice XML serversinparticular. Forboththesereasons, thediscussion shouldbe
regarded astentativeandopenforrevision. However,itshouldalsobepointedoutthatitisfairly
clearwhatissupportedin Voice XML; mostoftheunclarities refertowhatispossible,butnotexplicitly
supported,in Voice XML. Ingeneral,itismoreimportanttoknowwhatissupportedbyastandard than
whatispossible,sincealmostanythingispossibleinanyprogramming environmen t(givenasufficient
numberofhacks).
13Although the Voice XML documentationdoesnotprovideanyexamples ofthiskindofbehaviour,it
appearstobepossible,atleastinprinciple.

204 CHAPTER 4. ADDRESSING UNRAISED ISSUES
question andissueaccommodationwerethenintroducedtoallowthesystemtobemore
flexibleinthewayutterances areinterpreted relativetothedialogue context. Question
accommodationallowsthesystemtounderstand answersaddressing issueswhichhavenot
yetbeenraised. Incasesofambiguity,whereananswermatchesseveralpossiblequestions,
clarification dialogues maybeneeded.

