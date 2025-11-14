Chapter 6
Conclusions andfuture researc h
6.1 Introduction
Inthisfinalchapter,wefirstsummarize theprevious chapters. Wewillthenusetheresults
toclassifyvariousdialogue typesandactivities, andsaysomething abouttherelationof
theissue-based modelto Groszand Sidner's (1986)accountofdialogue structure. Finally,
wediscussfutureresearchissues.
6.2 Summary
In Chapter 1,wepresentedtheaimofthisstudyandgavesomeinitialmotivationsfor
exploring theissue-based approachtodialogue management. Wethengaveabriefoverview
ofthethesisandtherelatedversionsofthe IBi Ssystem. Finally,wegaveaverybrief
introductiontothe Trindi Kit architecture andtheinformation stateapproachtodialogue
implemen tedtherein.
In Chapter 2,welaidthegroundw orkforfurtherexplorations ofissue-based dialogue
managementanditsimplementationinthe IBi Ssystem. Asastarting pointweused
Ginzburg's conceptof Questions Under Discussion, andweexplored theuseof QUDas
thebasisforthedialogue management(Dialogue Move Engine) componentofadialogue
system. Thebasicusesof QUDistomodelraisingandaddressing issuesindialogue,
including theresolution ofelliptical answers. Also,dialogue plansandasimplesemantics
wereintroducedandimplemen ted.
235

236 CHAPTER 6. CONCLUSIONS AND FUTURE RESEAR CH
In Chapter 3 wediscussed generaltypesandfeatures offeedbackasitappearsinhuman-
humandialogue. Next,wediscussed theconceptofgrounding fromaninformation state
updatepointofview,andintroducedtheconcepts ofoptimistic, cautious andpessimistic
grounding strategies. Wethenrelatedgrounding andfeedbacktodialogue systems, and
discussed theimplementationofapartial-co veragemodeloffeedbackrelatedtogrounding
in IBi S2. Thisallowsthesystemtoproduceandrespondtofeedbackconcerning issues
dealingwiththegrounding ofutterances.
In Chapter 4,wemadeadistinction betweenalocalandaglobal QUD(referring tothe
latteras\openissues",orjust\issues"). Thenotionsofquestion andissueaccommodation
werethenintroducedtoallowthesystemtobemoreflexibleinthewayutterances are
interpreted relativetothedialogue context. Question accommodationallowsthesystemto
understand answersaddressing issueswhichhavenotyetbeenraised. Incasesofambiguity,
whereananswermatchesseveralpossiblequestions, clarification dialogues maybeneeded.
In Chapter 5,wefirstextended theissue-based approachtoaction-orienteddialogue, and
implemen tedadialogue interfacetoa VCRwheredialogue planswerebasedonanexisting
menuinterface. Wethenproposedaviewofnegotiation asdiscussing severalalternativ e
solutions toanissueundernegotiation. Onourapproach,anissueundernegotiation is
representedasaquestion, e.g.whatflighttheuserwants. Ingeneral,thismeansviewing
problems asissuesandsolutions asanswers.
6.3 Dialoguetypology
Inthissection, wewillusesomedistinctions madeinprevious chaptersasabasisfor
classifying dialogues anddialogue segmentsalongvariousdimensions. Whilethesedi-
mensions cantosomeextentbeusedtoclassifydialogue systems according tothekinds
ofdialogues theycanhandle,theyarenotintendedasaclassification ofhuman-human
dialogues. Rather,theyshouldberegarded asdescribing propertiesofdialogue segments.
Aswehavepreviously stated,wemakeadistinction between Inquiry-orientedand Action-
orienteddialogue according towhether thedialogue concerns non-comm unicativeactions
tobeperformed bya DP. Usually,butnotnecessarily ,AODsubsumes IOD. Oneexample
of\pure"actionorienteddialogue, wherenoquestions areasked,is Wittgenstein's simple
\slab"gamein Wittgenstein (1953).Another example issimplevoicecommand systems.
AODand IODareshownwiththeircorrespondingdialogue movesandinformation state
componentsin Table 6.1.
Wecanalsoclassifydialogues according tothepresence orabsence ofgeneraldialogue
features suchasgrounding, question accommodation,andnegotiation. Thisisdonein

6.3. DIALOGUE TYPOLOGY 237
Dialogue type Moves IScomponents
IOD ask qud
answerissues
AOD request actions
confirm
Table 6.1:Dialogue types
Table 6.2. Whilegrounding andaccommodationisprobably presentinallhuman-human
dialogue, negotiation maybelessfrequent.
Feature Moves IScomponent
Grounding icm tmp,grounding issues
Accommo dationaccommodate X-
(tacit)
Negotiation propose Question²Set(Answ er)
Table 6.2:Dialogue features
Finally,wecanalsoclassifyactivities according tovariousaspectsofdialogue, asin Table
6.3. Notethatthisclassification isindependentofthatin Table 6.2. Webelievethat
dialogue inalltheseactivities maybenegotiativeornon-negotiative,andnegotiation may
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
Tutorial IODor AODcomplex ? tutor
Table 6.3:Activities
Wewillnowrelatethetaxonomyabovetothetaxonomies in Dahlböack(1997)and Allen
etal.(2001).Itshouldbestressed thatneither Allennot Dahlböackhavethesamegoals
withtheirclassifications aswedohere,andthoughsomeformulations mayappearcritical
theyaremainlyintendedtoclarifytherelationbetweentheseclassifications andours.

238 CHAPTER 6. CONCLUSIONS AND FUTURE RESEAR CH
6.3.1 Relation to Dahlböack'sdialogue taxonomy
Dahlböack(1997)taxonomizes dialogue according tosevencriteria:
²modality:spokenorwritten
²kindsofagents:humanorcomputer
²interaction: dialogue ormonologue
²context:spatial,temporal
²numberandtypeofpossible/sim ultaneous tasks
²dialogue-task distance: longorshort
²kindsofsharedknowledgeused:perceptual, linguistic, cultural
Ourtypologyappearstobeonadifferentlevelandisindependentofmanyof Dahlböack's
criteria, andbothcoverimportant(butforthemostpartdistinct) dimensions ofclassifi-
cation. Ingeneral, theinteraction betweenthedimensions coveredby Dahlböackandthe
onescoveredinourtypologyisaninteresting areaforfutureresearch.
Modalityisnotincluded inourtypology;however,IBi Sisabletousebothwrittenand
spokenlanguage. Regarding kindsofagents,wehaveofcoursebeendealingmainlywith
human-computer interaction; however,wehavebasedboththeoryandimplementationon
observationsofhuman-humandialogue.
Ourdialogue typologyshouldberegarded asprimarily concerning dialogue interaction;
however,aversionof Go Di S(thepredecessor of IBi S)hasbeenusedtoproducemonologue
outputfromadomainplanspecification whichwasalsousedforgenerating dialogue plans
(see Larssonand Zaenen,2000).
Wehavenotincluded aspectsofspatialandtemporalcontextinourtypology;forour
theoryandsystemwehavenotexplored theimpactofanyotherkindofcontextthan
(pre-stored information about)thedomain(activity)andthedialogue itself.
Regarding thenumberandtypeofpossibleand/orsimultaneous tasks,theuseoftheissues
andactionsstacksallows,atleastinprinciple, anarbitrary numberofsimultaneous tasks.
Sincethesimplest versionofourtheoryandsystemcanhandlethis,wehavenotusedthis
asadimension ofclassification.

6.3. DIALOGUE TYPOLOGY 239
Thedialogue-task distance dimension isperhapslessobviousthantheothers. Thisisbased
ontheobservationthatsomekindsofdialogue haveastructure closelycorresponding
tothetaskstructure (e.g.planning oradvisory dialogue), whilesomehavea\longer
distance" betweenthesetwostructures (e.g.information retrievaldialogue). Dahlböack
arguesthatfordialogues withashortdialogue-task distance, intention-based methodsfor
dialogue actrecognition isbothmoreusefulandeasierthanfordialogues withalong
dialogue-task distance. Forthelatter,surface-based actinterpretation iseasierandmore
appropriate, whereasintention-based methodsarelessusefulandmoredifficult. Regarding
thisdimension, wehavebeenmostlyconcerned withdialogues withalongdialogue-task
distance, andif Dahlböackisrightanintention-based andcontext-dependentinterpretation
modulewillbeneededwhenextending theissue-based approachtoe.g.collaborative
planning dialogue. Whilethismayaffecthowdialogue movesaredefined, webelieve
(although wecannotbesure)thatthesetofdialogue moveswehaveproposedinour
taxonomycanstillbemaintained.
Finally,regarding thekindsofsharedknowledgethatareused,ourtaxonomydoesnotsay
much. Wehavenotbeenconcerned withtheperceptual andcultural context,exceptto
theextentthattheseareencodedinthestaticdomainknowledgeresources. Theuseof
domain-sp ecificlexiconscanperhapsberegarded asasimplistic formoflinguistic context.
6.3.2 Relation to Allenet.al.'sdialogue classification
Theclassification by Allen et al.(2001)appearstobecloserinspirittotheoneproposed
here. Dialogues areclassified according tothedialogue managementtechnique(minimally)
required byadialogue systemcapableofhandling therespectivekindsofdialogue. Each
classisfurtherspecifiedbyexample tasks,adegreeoftaskcomplexit y(ranging fromleast
tomostcomplex), andasetofdialogue phenomena handled.
²finite-state script
{example task:long-distance calling
{dialogue phenomena: useranswersquestions
²frame-based
{example tasks:gettingtraintimetable information
{dialogue phenomena: useranswersquestions, simpleclarifications bysystem
²setsofcontexts
{example tasks:travelbookingagent

240 CHAPTER 6. CONCLUSIONS AND FUTURE RESEAR CH
{dialogue phenomena: shiftsbetweenpredetermined topics
²plan-based models
{example tasks:kitchendesignconsultan t
{dialogue phenomena: dynamically generated topicstructures, collaborativene-
gotiation subdialogues
²agent-basedmodels
{example tasks:disasterreliefmanagement
{dialogue phenomena: differentmodalities(e.g.plannedworldandactualworld)
Thefirstthingtonoteaboutthisclassification isthatitdoesnotdistinguish separate
dimensions ofclassification, butratherreduceseveraldimensions toone;thiskindof
simplification andgeneralization doesofcoursehaveitsmerits,butmayalsobeconfusing.
Regarding thetaxonomyoftechnologies usedinthisclassification, itappearsthatthe
closestcorrespondingdimensions inourtypologyisthedifferentkindsofinformation states
anddialogue movesusedforvariousdialogue types,dialogue phenomena, andactivities.
However,theclassifications arealsoquitedifferent;foronething,thefinite-state-based
andform-based techniques usuallydonotevenusedialogue moves. Bycontrast,our
classification reliesonspecifyingdialogue movesevenforverysimpledialogues. Wewill
notgointoadiscussion oftherelativemeritsofthesegroundsofclassification; sufficetosay
thatatheory-dep endentclassification (whichourstosomeextentis)allowsagreaterlevel
ofdetailintheclassification, butitsusefulness isofcoursedependentontheacceptance
ofthebasictheoretical assumptions thataremade.
Thefirsttwotechnologies listedby Allenet.al.werediscussed in Chapter 1,andthe
distinction betweenthemareprettymuchstandard. However,theclassification ofthe
remaining threetechnologies ismoreproblematic.
Regarding the\setsofcontexts"technology,furtherspecifiedastheuseofseveralforms,
itcanberegarded asambiguousbetweentheuseofseveralformsofthesametypeand
theuseofseveralformsofdifferenttypes. Theexample taskprovidedis\travelbooking
agent",ormorespecifically,itinerary booking. Thisseemstoindicate thattheintended
meaning of\setsofcontexts"istheuseofseveralformsofthesametype(e.g.oneforeach
legoftheitinerary). Inourtypologyofactivities in Table 6.3,thiswouldcorrespondtoa
dialogue withacomplex result. However,theuseofseveralformsofdifferenttypesseems
rathertothepossibilityofseveralsimultaneous tasks(e.g.askingaboutwhichchannelis
onwhileprogramming the VCR).

6.4. DIALOGUE STRUCTURE 241
Thelevelofplan-based technology isfurtherspecifiedas\interactivelyconstructing a
planwiththeuser"(Allen et al.,2001,p.30).Thisspecification thussayssomething
abouttheresultofthedialogue (aplan)andhowthisresultisconstructed (interactively).
Notethatthisisnotexactlywhatwereferredtoastheplan-based approachin Chapter
1;atleastinprinciple (andperhapsalsoinpractice; thisisanempirical issuerelatedto
Dahlböack'sconceptofdialogue-task distance) itappearstobepossibleforadialogue system
toengageinthiskindofdialogue evenifthesystemitselfdoesnotusecomplex planning
andplanrecognition (e.g.fordialogue actrecognition). Relating thistoourclassification
ofactivities, itappearsthattheplan-based levelcorrespondsroughlytodialogues with
complex results(plans)anddistributed decision rights(interactivit y).Asisindicated by
Table 6.3,thetechniquesneededtohandlethe\plan-based" levelwouldalsobeneeded
fore.g.explanatory andtutorialdialogue.
Finally,regarding thelevelofagent-basedtechnology,furtherspecifiedaspossiblyinvolving
execution andmonitoring ofoperations inadynamically changing world,itappearsthat
themaindifference totheplan-based modeliswhatwerefertoas(pro)activ enessofthe
external process.
Toconclude, itappearsfromthepointofviewofourtypologythattheclassification by
Allen et al.(2001)isbasedonamixofcriteria, including information statecomponents
(e.g.forms)butalsoactivitytype,resulttype,pro-activ enessofexternal process,decision
rights,anddialogue features suchasgrounding (\simple clarifications") andnegotiation
(\collaborativenegotiation subdialogues"). The AOD/IOD distinction appearsnottobe
included atall.
6.4 Dialoguestructure
Inthissectionwediscusstheimplications ofissue-based dialogue managementonthe
structure ofdialogue. Wediscussthedialogue modelof Groszand Sidner(1986),elaborated
in Groszand Sidner(1987),andrelateittotheissue-based model. Theauthorspresenta
theoryofdiscourse structure basedonthreestructural components:
²linguistic structure: utterances, phrases, clausesetc.
²intentionalstructure: intentions,relatedbydominance andsatisfaction-precedence
²attentionalstate:salientobjects,properties,relations anddiscourse intentions
Theintentionalstructure isrelatedtodialogue structure through Discourse Segment Pur-
poses(DSPs).Adialogue canbedividedintosegmentswhereeachsegmentisengaged

242 CHAPTER 6. CONCLUSIONS AND FUTURE RESEAR CH
inforthepurposeofsatisfying aparticular intention,designated asthe DSPofthatseg-
ment. Thisrelationisusedtoexplaintheclosecorrespondence betweentaskstructure and
dialogue structure observedincollaborativeplanning dialogue. Withregardtodialogue
management,itisclaimedthat\aconversational participantneedstorecognize the DSPs
andthedominance relationships betweentheminordertoprocesssubsequen tutterances
ofthediscourse" (Groszand Sidner,1987,p.418).Theauthorsalsosketchaprocess
modelbasedontheconceptofa Shared Plan,formalized intermsofindividual intentions
andmutualbeliefs.
Therearesomeinteresting butroughcorrespondences betweenthismodelandtheissue-
basedmodel,andthelattercanperhapsbeseen(atleasttosomeextent)asanalternativ e
(orcomplemen t)tothe Shared Plans formalization.
Thesimplest correspondence isthatbetweenthelinguistic structure andthelufield(and
perhapsalsotheinputvariable)intheissue-based model,although ourmodeloflinguistic
structure isextremely impoverished.
Intheissue-based model,DSPsroughlycorrespondtotheissuesand(in AOD)actions
fields,andshouldthusbeusefulforsegmentingdialogue inamannersimilarto Groszand
Sidner's. Sequencing ICM,which(amongotherthings)reflectchangesinissuescanthus
beregarded asindicating dialogue segmentshifts.
Thelocalfocusofattentionispartially modelledby QUD,although sofarourattentional
modellackse.g.arepresentationof\objectsunderdiscussion". Discourse intentionsseem
tocorrespondroughlytotheagendafield,andpossiblyalsotheplanfieldalthough the
latterismoreglobalinnature. Ofcourse,ourrepresentationofdialogue plansisquite
differentfromthatof Groszand Sidner,whouseamodallogicwithoperatorsforintentions.
Itshouldbenotedthattheintentionalstructure, modelledas Shared Plans, ispartofthe
sharedknowledge. Groszand Sidnerareprimarily interested indialogues aimedatthe
collaborativecreation andexecution ofthese Shared Plans, whichmeansthattheirmodel
doesnottriviallyextendtootherkindsofdialogue, e.g.simpleinquiry-orienteddialogue or
tutorialdialogue. Forthekindsofdialogue wehavedealtwithsofar,thekindofcomplex
representationsneededformodelling Shared Plans appearnottobeneeded. Theclosest
correspondence to Shared Plans inourmodelistheactionsfieldwhichcontainsdomain
actionstobeperformed byoneofthe DPs. Itcanbeexpectedthatwhentheissue-based
modelisextended tohandlecollaborativeplanning dialogue, thestructure oftheactions
fieldwillbecomemorecomplex andmoresimilarto Shared Plans.

6.5. FUTURE RESEAR CHAREAS 243
6.5 Futureresearchareas
Inthissection,webrieflymentionsomefutureareasforresearchusingtheissue-based
approachtodialogue management. Wealsomentionsomedesirable improvementsto
IBi S.
6.5.1 Developingtheissue-based approachtogrounding
Representationofutterances Starting from Ginzburg's grounding protocols,wehave
formalized andimplemen tedabasicversionofissue-based grounding andfeedback. How-
ever,someaspectsofthecurrentsolution arenotcompletely satisfactory ,anditappears
thatabettersolution couldbeobtained byexplicitly representingutterances invarious
stagesofgrounding toalargerextentthaninthecurrentsystem.
Grounding issues Also,toincrease thecoverageofthetheoryandtheabilities ofthe
systemitwouldbeusefultorepresentgrounding issuesexplicitly onseverallevelsofground-
ingtoalargerextentthaniscurrentlydone. Someofthepossiblegrounding issuesthat
couldberepresentedarethefollowing(Sisthespeaker,Aistheaddressee, uisanutterance
by S).
²Contactlevel
{Sand A:Do Ihavecontactwithother DP?
²Perception level
{S:Did Aperceiveucorrectly? Ifnot,whatdid Aperceive?
{A:Whatdid Ssay?Did Ssay X?Whichof X1;:::;Xndid Ssay?
{Sand A:Isugrounded ontheperception level?
²Semanticunderstanding level
{S:Did Aunderstand theliteralmeaning ofu?Ifnot,whatdoes Athink I
meant(literally)?
{A:Whatdoesumean(literally)? Doesumean X?Whichof X1;:::;Xndoes
umean?
{Sand A:Isugrounded onthesemanticunderstanding level?
²Pragmatic understanding level

244 CHAPTER 6. CONCLUSIONS AND FUTURE RESEAR CH
{S:Did Aunderstand thepragmatic meaning ofu?Ifnot,whatdoes Athink I
meant(pragmatically)?
{A:Whatdid Smeanbyumean,giventhecurrentcontext?Howisurelevant
inthecurrentcontext?Did Smean X?Whichof X1;:::;Xndid Smean?
{Sand A:Isugrounded onthepragmatic understanding level?
²Reaction level
{S:Will Aaccept(thecontentof)u?
{A:Should Iaccept(thecontentof)u?Ifuisanassertion, should Iacceptu
asafactoronlyasatopicfordiscussion? If Idon'tacceptu,howshould I
indicate this?Should Iacceptanalteredversionofu?Should Iacceptonlya
partofu?
Increased coverage Ouraccountofgrounding and ICMissofaronlypartialincover-
age;phenomena thatremaintobeaccountedforand/orimplemen tedincludeclarification
ellipsis,semanticambiguityresolution, collaborativecompletions andrepair,andturntak-
ing ICM. Whilewehaveincluded somerudimentarysequencing ICM,furtherinvestigations
oftheappropriateness andusefulness oftheseutterances areneeded;here,researchondis-
coursemarkers(e.g. Schiffrin,1987)andcuephrases(e.g. Groszand Sidner,1986,Polanyi
and Scha,1983,and Reichman-Adar, 1984)canbeofgreatuse. Wealsowanttoexplore
turntakinginasynchronousdialogue management,andhowthisrelatestoturntaking ICM.
Own Communication Managemen thassofarnotbeenhandled atall,andthisisclearly
anareawherethesystemcouldbeimprovedbothontheinterpretation andgeneration
side. Wehopethattheissue-based approachcouldhelpclarifytherelationbetween ICM
and OCMaspectsofgrounding-related utterances.
Methodsforchoosinggrounding and ICMstrategies Wehaveusedaverybasic
methodforchoosinggrounding and ICMstrategies; thiscouldbedevelopedtoinclude
context-related aspectsoftheutterance tobegrounded. Thisalsogoesforthestrategies
forchoosingbetweenseveralcompetinginterpretation hypothesesontheperception and
understanding levels.
Implicitissues Webelievethatthemodellingofimplicitissues,bothgrounding-related
andothers,canbeveryusefulforaccountingfortherelevanceofmanyutterances. We
therefore needtodevelopageneralwayofdealingwithimplicitquestions andtheaccom-
modationofthese. Webelievethatsuchanaccountshouldbebasedondynamic generation
andaccommodationofimplicitissueswhentheyareneeded,ratherthancalculating all
possibleimplicitissuesavailableatanystageofthedialogue.

6.5. FUTURE RESEAR CHAREAS 245
6.5.2 Otherdialogue andactivitytypes
Ofcourse,anobviouscontinuationoftheworkpresentedhereistocontinueextending the
coverageofissue-based dialogue managementtootherkindsofdialogues. Inthissection
wewilldiscusssomepossibilities.
Pro-activedevices Tohandledialogue withpro-activ edevices, itisnotsufficientto
modelthedeviceonlyasaresource, sincethelatterarebydefinition passive. Whatis
neededisamodulewhichisconnected totheactivedevice;wecancallsuchamodulean
actionmanager. Dialogue withpro-activ edeviceswillalsorequireasynchronous dialogue
processing,atleastonsomelevel. Thesimplest solution istocheckformessages fromthe
devicewhenthesystemhastheturn. Tohandlethis,itisprobably sufficienttohavethe
wholesystemexcepttheactionmanager runningasasingleprocess. However,itmayalso
benecessary forthesystemtointerrupttheuser(orindeeditself)inmid-turn, togivea
reportonthestateofsomeactionorplanbeingexecuted. Thisislikelytorequireamore
advancedasynchronous setup,whereseveralprocessesareneeded.
Complex results Wehavesofaronlybeendealingwithdialogues wherethe\result"
(answer,action)isnotverycomplex. Ine.g.itinerary information dialogue, theresultmay
beamorecomplex structure. Incollaborativeplanning dialogue theresultisapotentially
complex planwithseveralactionsrelatedinvariousways. Similarly ,explanatory dialogue
mayrequirerepresentationofcomplex explanations orproofs. Todealwithdialogue with
complex results,weneedtobeabletorepresentthesecomplex structures, andperhaps
alsotoincremen tallyconstruct thembysuccessiveadditions andmodifications. However,
webelievethattheessentialfeatures ofinquiry-oriented,action-oriented,andnegotiative
dialogue arethesameregardless ofwhether theresultsarecomplex orsimple.
Argumentation Tohandleargumen tation,whichismostlikelytoappearinnegotiative
dialogue, wehopetobeabletoexploitprevious workinthisarea,e.g. Mannand Thompson
(1983)and Asherand Lascarides (1998),andrelateittotheissue-based approach.
Useofobligations Traumand Allen(1994)proposeobligations asacentralsocial
attitude drivingdialogue. Forexample, if DPAasksaquestion Qto DPB,Bwillhave
anobligation toaddress Q;typically,thisobligation willthengiverisetoanintentionto
address Q. In IBi S,weinsteadadd Qto QUD(globalandlocal),andifthesystemcan
answeraquestion on QUDitwilldoso. Ithasbeennotedthatthejobdonebyobligations
and QUDoverlaptoalargeextent(Kreutel and Matheson, 1999),andinmanykinds

246 CHAPTER 6. CONCLUSIONS AND FUTURE RESEAR CH
ofdialogue thechoicebetween QUDandobligations willnotresultinanydifferences in
behaviour. However,therearealsodifferences between QUDandobligations.
Foronething,QUDdoesnotrepresentwhoraisedthequestion, orwhoshouldrespond
toit. Aninteresting question thenbecomes: giventhatweincludeaglobal QUDinour
information state,whendoesitbecomenecessary toalsoincludeobligations? Itappears
thatonetypeofdialogue where QUDonitsownisinsufficien tistutorialdialogue, where
thetutorasksthestudentaso-called \examquestion" towhichthetutoralreadyknows
thecorrectanswer. Giventhestrategy usedby IBi S,thesystemwouldraisethequestion
andthenimmediately answerit,whichisprobably notaverygoodteachingstrategy.
However,inmanyotherkindsofdialogues itappearsthatthestrategy ofansweringa
question regardless ofwhoanswereditisausefulstrategy. Forexample, ifa DPA(a
humanorperhapsarobotequippedwithvision)asksanother DPBwheresomeobjectis
locatedandthenfindstheobject,itappearsmorefelicitous for Atoanswerthequestion
(\Ah,thereitis!")thantowaitfor Btodoso. Moreimportantly,wehaveinthepreceding
chaptersdemonstrated severalusesofaglobal QUD(modellinggrounding issues,handling
issueaccommodation,representingissuesundernegotiation) whichitmayormaynot
bepossibletohandleusingobligations. Forthesereasons, weareinterested infurther
exploring thesimilarities, differences, andinteraction between QUDandobligations, and
possiblyextendtheissue-based dialogue modelbyaddingobligations, atleastformodelling
somecomplex kindsofdialogue.
Generalplanning Asimilarcaseappliestogeneralized planning. Wehavesofaronly
usedpre-scripted dialogue planswhichareusedinaflexiblewaybythedialogue manager to
enablesomedegreeofrudimentaryreplanning, butitcanbeexpectedthatforsufficiently
complex dialogues thenumberofdialogue plansthatareneededwillbecomesolargethat
pre-scripting isnolongerfeasible. Atthispoint,dynamic planning willbeneeded. Weare
interested infindingoutforwhichkindsofdialogues dynamic general-purp oseplanning
isneeded,andinintegrating dynamic planning intheissue-based approachtodialogue
management.
6.5.3 Semantics
Thesemanticscurrentlyusedin IBi Sisobviouslyverysimple,andintegrating theissue-
basedapproachtodialogue managementwithamorepowerfulsemanticsislikelytoim-
proveboththetheoretical depthofanalysis, especiallyregarding thesemanticsofquestions,
andtheperformance ofthesystem. Arelevantissueinthiscontextistheconnection be-
tweendialogue featuresandrequirementsonthesemanticrepresentationused-whendoes
morecomplex semanticsbecomenecessary?

6.5. FUTURE RESEAR CHAREAS 247
Specifically,wewouldliketoexploreandimplemen tsemanticsusingdependentrecord
types(Cooper,1998),andintegratethiswithissue-based dialogue management. One
reasonforthisisthatdependentrecordtypesappearstoprovideacomputationally sound
frameworkforimplemen tingideasfromsituation semantics;thelatterhasbeenusedby
Ginzburg informulatingthesemanticsofquestions onwhichtheissue-based approachto
dialogue managementisbased.
Itshouldbenotedthatthesystemitselfisindependentofwhichsemanticsisused;this
isratherafeatureofthedomain-sp ecificresources and(tosomeextent)theresource
interfaces. Addingamorepowerfulsemanticswilltherefore notrequireanysignifican t
modifications ofupdaterulesetc.
6.5.4 General inference
Whileupdaterulescanberegarded asspecialized (forward-chaining) inference rules,we
havesofarnotdealtwithgeneralinference andbackward-chaininginference. Inference
couldbeusefulevenindatabase searchdialogue toreasonaboutthebestwayofdealing
withsearchresultsintheformofconditionals (see Section 2.12.4). Oneideahereisto
introduceaprivateissue-structure representingquestions thatthesystemisinterested in
resolving; thiscouldberegarded asmodellingthe\wonder"attitude. Afindout( Q)action
ontheagendacouldthenresultin Qbeingaddedtoafield/private/wonder,whichcan
eitherleadtoadatabase search,backward-chainingreasoning fromavailableinformation,
oraskingtheuserforananswer. Asanexample ofbackward-chainingreasoning usingthe
\wonder"attitude, ifthesystembelievesp!randwondersabout?r,arulecouldadd?p
tothewonderfield;thisrulewouldthenimplemen tbackward-chainingmodusponens.
6.5.5 Naturallanguage inputandoutput
Parsingandgeneration In IBi Swehavesofarconcentratedondialogue management
andusedveryrudimentarymodulesforinterpretation andgeneration ofnaturallanguage.
Weneedtoexplorethepossibleuseofrobustparsingtechniques(seee.g. Milward,2000)
and\real"grammars. Itwouldalsobeusefultobeabletoautomatically generate speech
recognition grammars (whichareusuallyfinite-state) fromtheparsinggrammar. Using
thesamegrammar forparsingandgeneration wouldfurtherdecrease theamountofwork
neededforportingthesystemtoanewdomainorlanguage.
Dialoguemoveinterpretation Sincewehavebeendealingwithsimpledialogue intoy
domains, wehavesofarbeenabletogetawaywithdoingdialogue moveinterpretation

248 CHAPTER 6. CONCLUSIONS AND FUTURE RESEAR CH
independentlyofthedynamic context. Instead, contextdependentinterpretation isper-
formedbythedialogue moveengineasasubtaskofintegrating moves. Whilewebelieve
thatthisisagoodstrategy touseaslongasitworkswell,itmayeventuallybecomenec-
essarytobeabletorecognize indirectspeechacts(inourcase,indirectdialogue moves),
whichprobably requires someformofcontext-dependentintentionrecognition todecide
whatmovehasbeenperformed.
Focusintonation Oneareaofresearchthatwehavenotmentionedsofar,butwhere
theissue-based approachshowsgreatpromise, isthegeneration andinterpretation of
focusintonation withrespecttotheinformation state. Someworkwasdoneonthisinthe
TRINDI project(Engdahl etal.,1999),andiscurrentlybeingdevelopedfurtherinthe
followup SIRIDUS project.
Speechrecognition forflexibledialogue Oneproblem foranydialogue systemallow-
ingforuserinitiativeandflexibilityisthatalargerspeechrecognition lexiconisneeded,
whichnegativelyaffectsthequalityofspeechrecognition. Wewanttoexploretheuseof
theinformation state,andespecially QUD,forimprovingrecognition, e.g.byrunning a
\global" recognizer listening foranythingthatthesystemcanunderstand, anda\local"
recognizer, listening e.g.foranswerstoquestions on QUD,inparallel.
6.5.6 Applications andevaluation
Toproperlytesttheissue-based approachtodialogue management,webelieveitisnec-
essarytobuildfull-scale prototypeapplications andevaluatethesebasedoninteractions
withnaiveusers. Onepossiblesuchapplication is VCRcontrol;another islocaltravel
information.
Although wehavenotsaidmuchaboutithere,wehavepreviously explored variouswaysof
acquiring dialogue plansappropriate foragivendomainorapplication. Amongtheoptions
wehaveusedisdialogue distillation (see Larsson et al.,2000 b),conversionofdomainplans
todialogue plans(see Larsson, 2000),andconversionofmenuinterfacestodialogue plans.
Afurtheroptionwewanttoexploreistheuseof Voice XML (Mc Glashan etal.,2001)
dialogue specifications asabasisfordialogue plans. Wehopetobeabletoautomatically
orsemi-automatically convert Voice XML scriptsintocomplete domainandlexiconspec-
ifications for IBi S,whichwehopewouldallowtheuseofgeneraldialogue mechanisms
(e.g.grounding, accommodation,negotiation) toenableflexibledialogue givenfairlysim-
ple Voice XML scripts. Thiswoulddecrease theamountofworkonthepartofthedialogue

6.6. CONCLUSION 249
designer, andthusenablerapidprototyping.
6.6 Conclusion
Theissue-based approachtodialogue managementhasproventobeveryusefulforformu-
latinggeneralandtheoretically motivatedaccountsofimportantaspectsofdialogue, such
asinquiry-orienteddialogue interactions, dealingwithmultiplesimultaneous tasks,sharing
information betweentasks,grounding, interactivecommunication management,question
accommodation,simplebeliefrevision, action-orienteddialogue, andsimplenegotiative
dialogue. Themodelcanbeimplemen tedratherstraightforwardlyusingthe Trindi Kit ,
whichhasproventobeaveryusefultoolforexploring theissue-based approach. Some
aspectsoftheaccountaspresentedherecanbeimprovedon,e.g.byproperlydividing the
tasksofutterance understanding andintegration intoseparate rules,andimprovingthe
treatmen tofsemantics.
Toreallyshowthattheissue-based approachisaviablealternativ etomorecomplex
approachessuchastheplan-based approachasusede.g.inthe TRIPSsystem(Allenet
al.(2001)), weneedtoextendthecoverageoftheissue-based accounttoincludemore
complex typesofdialogue, involvinge.g.collaborativeplanning andreal-time monitoring
ofadynamic environmen t. Webelievethisisfeasible, andanexcitingfutureresearcharea.
Themodularityofthe IBi Ssystemenablesrapidprototypingofsimpleexperimentalap-
plications. Webelievethatitwillbepossibletoscaleupthemethodspresentedhereto
morerealisticapplications whichcanbeevaluatedonnaivesubjects.

250 CHAPTER 6. CONCLUSIONS AND FUTURE RESEAR CH

Bibliograph y
Alexandersson, Janand Becker,Tilman 2000. Overlayasthebasicoperationfordiscourse
processinginamultimodaldialogue system. In Proceedingsofthe IJCAIWorkshop on
Knowledgeand Reasoningin Practical Dialogue Systems.8{14.
Allen,J. F.and Perrault,C.1980. Analyzing intentioninutterances. Artificial Intelligence
15(3):143{178.
Allen,James F.;Byron,Donna K.;Dzikovska,Myroslava;Ferguson, George; Galescu,
Lucian;and Stent,Amanda 2001. Towardconversational human-computer interaction.
AIMagazine 22(4):27{37.
Allen,J. F.1987. Natural Language Understanding .Benjamin Cummings, Menlo Park,
CA.
Allwood,Jens;Nivre,Joakim; and Ahlsen,Elisabeth 1992. Onthesemanticsandprag-
maticsoflinguistic feedback. Journalof Semantics 9:1{26.
Allwood,Jens 1995. Anactivitybasedapproachtopragmatics. Technical Report(GPTL)
75,Gothenburg Papersin Theoretical Linguistics, Universityof Göteborg.
Asher,N.and Lascarides, A.1998. Thesemanticsandpragmatics ofpresupposition.
Journalof Semantics 15(3):239{299.
Aust,H.;Oerder,M.;Seide,F.;and Steinbiss,V.1994. Experiencewiththe Philips
automatic traintableinformation system. In Proc.ofthe 2 nd Workshop on Interactive
Voice Technologyfor Telecommunic ations Applications(IVTTA),Kyoto,Japan.67{72.
Barwise, J.and Perry,J.1983. Situations and Attitudes. The MITPress.
Berman, Alexander 2001. Asynchronous feedbackandturn-taking. ms.
Bohlin,Peter;Bos,Johan;Larsson, Staffan;Lewin,Ian;Matheson, Colin;and Milward,
David 1999. Surveyofexistinginteractivesystems. Technical Report Deliverable D1.3,
Trindi.
251

252 BIBLIOGRAPHY
Bos,Johanand Gabsdil, Malte 2000. First-order inference andtheinterpretation of
questions andanswers. In Poesioand Traum 2000.
Boye,J.;Larsson, S.;Lewin,I;Matheson, C.;Thomas, J.;and Bos,J.2001. Standards in
homeautomation andlanguage processing. Technical Report Deliverable D1.1,D'Homme.
Böauerle,Rainer;Reyle,Uwe;and Zimmermann, Thomas Ede,editors 2002. Presupposi-
tionsand Discourse. Current Researchinthe Semantics/Pragmatics Interface. Amster-
dam(Elsevier).
Carberry,S.1990. Plan Recognitionin Natural Language Dialogue. The MITPress,
Cambridge,MA.
Chu-Carroll, Jennifer 2000. Mimic:Anadaptivemixedinitiativespokendialogue system
forinformation queries. In Proceedingsofthe 6 th Conferenceon Applied Natural Language
Processing.97{104.
Clark,H. H.and Schaefer,E. F.1989 a. Contributing todiscourse. Cognitive Science
13:259{94.
Clark,Herbert H.and Schaefer,Edward F.1989 b. Contributing todiscourse. Cognitive
Science 13:259{294. Alsoappearsas Chapter 5 in Clark(1992).
Clark,Herbert H.1992. Arenasof Language Use. Universityof Chicago Press.
Clark,H. H.1996. Using Language. Cambridge University Press,Cambridge.
Cohen,P.and Levesque,H.1990. Intentionischoicewithcommitmen t. Artificial Intel-
ligence 42:213{261.
Cohen,P.1981. Theneedforreferentidentification asaplanned action. In Proceedings
ofthe 7 th International Joint Conferenceof Artificial Intelligence,Toronto.31{36.
Cooper,Robinand Ginzburg, Jonathan 2001. Resolving ellipsisinclarification. In Pro-
ceedingsofthe 39 thmeetingofthe Assocationfor Computational Linguistics, Toulouse.
236{243.
Cooper,Robinand Larsson, Staffan 2002. Accommo dationandreaccommodationin
dialogue. In Böauerle et al.2002.
Cooper,Robin;Engdahl, Elisabet;Larsson, Staffan; and Ericsson, Stina 2000. Accom-
modatingquestions andthenatureofqud. In Poesioand Traum 2000.57{61.
Cooper,Robin; Ericsson, Stina;Larsson, Staffan; and Lewin,Ian 2001. An
information stateupdateapproachtocollaborativenegotiation. In Köuhnlein,
Peter;Rieser, Hannes; and Zeevat,Henk,editors 2001,BI-DIALOG 2001|
Proceedingsofthe 5 th Workshop on Formal Semantics and Pragmatics of Dialogue,
http://www.uni-bielefeld.de/BIDIALOG .Zi F,Univ. Bielefeld. 270{9.

BIBLIOGRAPHY 253
Cooper,R.1998. Information states,attitudes anddependentrecordtypes. In Proceedings
of ITALLC-98 .
Core,Mark G.and Allen,James F.1997. Codingdialogues withthe DAMSLanno-
tationscheme. In Traum,David,editor 1997,Working Notes:AAAIFall Symposium
on Communic ative Actionin Humans and Machines ,Menlo Park,California. American
Associationfor Artificial Intelligence. 28{35.
Dahlböack,Nils 1997. Towardsadialogue taxonomy. In Maier,Elisabeth;Mast,Mar-
ion;and Luper Foy,Susann, editors 1997,Dialogue Processingin Spoken Language Sys-
tems,number 1236 in Springer Verlag Series LNAI-Lecture Notesin Artificial Intelligence.
Springer Verlag.
Di Eugenio, B.;Jordan,P. W.;Thomason, R. H.;and Moore,J. D.1998. Anempirical
investigation ofproposalsincollaborativedialogues. In Proceedingsof ACL{COLING 98:
36 th Annual Meetingofthe Associationof Computational Linguistics and 17 th Interna-
tional Conferenceon Computational Linguistics .325{329.
The DISCconsortium, 1999. Discdialogue engineering model. Technicalreport,DISC,
http://www.disc 2.dk/slds/.
Engdahl, Elisabet;Larsson, Staffan;and Bos,Johan 1999. Focus-ground articulation and
parallelism inadynamic modelofdialogue. Technical Report Deliverable D4.1,Trindi.
Fikes,R. E.and Nilsson, N. J.1971. STRIPS: Anewapproachtotheapplication of
theorem provingtoproblem solving. Artificial Intelligence 2:189{208.
Göardenfors, P.1988. Knowledgein Flux:Modelingthe Dynamic of Epistemic States. The
MITPress,Cambridge,MA.
Ginzburg, J.1994. Anupdatesemanticsfordialogue. Inal,H. Buntet,editor 1994,
Proceedingsofthe International Workshop on Computational Semantics .ITK. Tilburg.
111{120.
Ginzburg, J.1996. Interrogativ es:Questions, factsanddialogue. In The Handbookof
Contemp orary Semantic Theory. Blackwell,Oxford.
Ginzburg, J.1997. Structural mismatchindialogue. In Jaeger,G.and Benz,A,edi-
tors 1997,Proceedingsof Mun Dial 97,Technical Report 97-106. Universitaet Muenchen
Centrumfuer Informations- und Sprachverarbeitung,Muenchen.59{80.
Ginzburg, J.forth. Questions andthesemanticsofdialogue. Forthcoming book,partly
availablefromhttp://www.dcs.kcl.ac.uk/staff/ginzburg/papers.html .
Goffman, E.1976. Repliesandresponses. Language in Society 5:257{313.

254 BIBLIOGRAPHY
Grosz,B. J.and Sidner,C. L.1986. Attention,intention,andthestructure ofdiscourse.
Computational Linguistics 12(3):175{204.
Grosz,B. J.and Sidner,C. L.1987. Plansfordiscourse. In Symposiumon Intentions
and Plansin Communic ationand Discourse.
Grosz,B. J.and Sidner,C. L.1990. Plansfordiscourse. In Cohen,P. R.;Morgan, J.;and
Pollack,M. E.,editors 1990,Intentions in Communic ation. The MITPress,Cambridge,
MA.chapter 20,417{444.
Hulstijn, J.2000. Dialogue Modelsfor Inquiryand Transaction .Ph. D.Dissertation,
Universityof Twente.
Jennings, N.and Lesperance,Y,editors 2000. Proceedingsofthe 6 th International Work-
shopon Agent Theories,Architectures,and Languages (ATAL'1999) ,Springer Lecture
Notesin AI1757. Springer Verlag,Berlin.
Kaplan,D.1979. Dthat. In Cole,P.,editor 1979,Syntaxand Semantics v.9,Pragmatics .
Academic Press,New York.221{243.
Kreutel, Jornand Matheson, Colin 1999. Modellingquestions andassertions indialogue
usingobligations. In Van Kuppevelt et al.1999.
van Kuppevelt,Jan;van Leusen,Noor;van Rooy,Robert;and Zeevat,Henk,editors 1999.
Proceedingsof Amstelogue'99Workshop onthe Semantics and Pragmatics of Dialogue.
Larsson, Staffanand Traum,David 2000. Information stateanddialogue managementin
thetrindidialogue moveenginetoolkit. NLESpecial Issueon Best Practicein Spoken
Language Dialogue Systems Engineering 323{340.
Larsson, Staffanand Zaenen, Annie 2000. Documenttransformations andinformation
states. In Proceedingofthe 1 st Sig Dial Workshop, Hong Kong. ACL.112{120.
Larsson, Staffan;Ljunglöof,Peter;Cooper,Robin;Engdahl, Elisabet;and Ericsson, Stina
2000 a. Godis-anaccommo datingdialogue system. In Proceedingsof ANLP/NAA CL-
2000Workshop on Conversational System.
Larsson, Staffan; Santamarta, Lena;and Jöonsson,Arne 2000 b. Usingtheprocessof
distilling dialogues tounderstand dialogue systems. In Proceedingsof 6 th International
Conferenceon Spoken Language Processing(ICSLP2000/INTERSPEECH2000), Volume
III.374{377.
Larsson, Staffan 1998. Questions underdiscussion anddialogue moves. In Proceedingsof
the Twente Workshop on Language Technology.163{171.
Larsson, Staffan 2000. Frommanualtexttoinstructional dialogue: aninformation state
approach. In Poesioand Traum 2000.203{206.

BIBLIOGRAPHY 255
Lewin,Ian;Cooper,Robin;Ericsson, Stina;and Rupp,C. J.2000. Dialogue movesin
negotiativedialogues. Projectdeliverable 1.2,SIRIDUS.
Lewin,I.;Larsson, S.;Ericsson, S.;and Thomas, J.2001. Thed'homme deviceselection.
Technical Report Deliverable D5.1,D'Homme.
Lewis,D. K.1979. Scorekeepinginalanguage game. Journalof Philosophic al Logic
8:339{359.
Ljunglöof,Peter 2000. Formalizing thedialogue moveengine. In Proceedingsof Göotalog
2000 workshop onsemantics andpragmatics ofdialogue.207{210.
Mann,W. C.and Thompson, S. A.1983. Relational propositionsindiscourse. Technical
Report ISI/RR-83-115, USC,Information Sciences Institute.
Mc Glashan, S.;Burnett, D;Danielsen, P.;Ferrans,J.;Hunt,A.;Karam,G;Ladd,D.;
Lucas,B.;Porter,B.;and Rehor,K.2001. Voiceextensible markuplanguage (voicexml)
version 2.0. Technicalreport,W3C. W3CWorking Draft,23October 2001.
Microsoft, 2000. Universal Plugand Play Device Architecture Version 1.0. URL:
http://www.upnp.org/do wnload/UPn PD A1020000613.h tm.
Milward,D.2000. Distributing representationforrobustinterpretation ofdialogue ut-
terances. In Proceedingsofthe 38 th Annual Meetingofthe Associationof Computational
Linguistics, ACL-2000.133{141.
Moore,Johanna D.1994. Participatingin Explanatory Dialogues:Interpretingand
Respondingto Questions in Context. Acl-Mit Press Seriesin Natural Language Processing.
MITPress.
Poesio,Massimo and Traum,David R.1998. Towardsanaxiomatization ofdialogue acts.
In Proceedingsof Twendial'98, 13 th Twente Workshop on Language Technology:Formal
Semantics and Pragmatics of Dialogue.207{222.
Poesio,Massimo and Traum,David,editors 2000. Proceedingsof Göotalog 2000,number
00-5 in GPCL(Gothenburg Papers Computational Linguistics).
Polanyi,L.and Scha,R.1983. Ontherecursivestructure ofdiscourse. In Ehlich,K.and
Riemsdijk, H.van,editors 1983,Connectednessin Sentence,Discourseand Text. Tilburg
University.141{178.
Rao,A. S.and Georgeff, M. P.1991. Modelingrationalagentswithinabdi-architecture. In
Allen,James;Fikes,Richard;and Sandewall,Eric,editors 1991,Proceedingsofthe Second
International Conferenceon Principles of Knowledge Representation and Reasoning(KR-
91),Cambridge,MA.473{484.

256 BIBLIOGRAPHY
Reichman-Adar, R.1984. Extended man-mac hineinterface. Artificial Intelligence
22(2):157{218.
Sadek,M. D.1991. Dialogue actsarerational plans. In Proceedingsofthe ESCA/ETR
workshop onmulti-mo daldialogue.1{29.
vander Sandt,R. A.1992. Presuppositionprojectionasanaphora resolution. Journalof
Semantics 9(4):333{377.
San-Segundo, Ruben;Montero,Juan M.;Guitierrez, Juana M.;Gallardo, Ascension;
Romeral, Jose D.;and Pardo,Jose M.2001. Atelephone-based railwayinformation system
forspanish: Developmentofamethodologyforspokendialogue design. In Proceedingsof
the 2 nd SIGdial Workshop on Discourseand Dialogue.140{148.
Schiffrin,D.1987. Discourse Markers. Cambridge University Press,Cambridge.
Severinson Eklundh, Kerstin 1983. Thenotionoflanguage game{anaturalunitof
dialogue anddiscourse. Technical Report SIC5,Universityof Linköoping,Studiesin
Communication.
Sidner,Candace L.and Israel,David J.1981. Recognizing intendedmeaning andspeak-
ers'plans. In Proceedingsofthe Seventh International Joint Conferenceon Artificial
Intelligence,Vancouver,British Columbia. International Joint Committee on Artificial
Intelligence. 203{208.
Sidner,Candace L.1994 a. Anartificial discourse language forcollaborativenegotiation.
In Proceedingsoftheforteenth National Conferenceofthe American Associationfor Ar-
tificial Intelligence(AAAI-94) .814{819.
Sidner,Candace. L.1994 b. Negotiation incollaborativeactivity:Adiscourse analysis.
Knowledge-Based Systems 7(4):265{267.
Stalnaker,R.1979. Assertion. In Cole,P.,editor 1979,Syntaxand Semantics ,volume 9.
Academic Press.315{332.
Stenströom,Anna-Brita 1984. Questions and Responses. Lund Studiesin English: Number
68. Lund:CWKGleerup.
Sutton,S.and Kayser,E.1996. Thecslurapidprototyper:Version 1.8. Technicalreport,
Oregon Graduate Institute, CSLU.
Traum,D. R.and Allen,J. F.1994. Discourse obligations indialogue processing. In
Proc.ofthe 32 nd Annual Meetingofthe Associationfor Computational Linguistics ,New
Mexico. 1{8.
Traum,D. R.and Hinkelman,E. A.1992. Conversation actsintask-orientedspoken
dialogue. Computational Intelligence 8(3):575{599. Special Issueon Non-literal Language.

BIBLIOGRAPHY 257
Traum,D. R.1994. AComputational Theoryof Groundingin Natural Language Conver-
sation. Ph. D.Dissertation, Universityof Rochester,Departmentof Computer Science,
Rochester,NY.
Traum,David R.1996. Areactive-deliberativemodelofdialogue agency. In Möuller,J. P.;
Wooldridge, M. J.;and Jennings, N. R.,editors 1996,Intelligent Agents III|Proceedings
ofthe Third International Workshop on Agent Theories,Architectures,and Languages
(ATAL-96),Lecture Notesin Artificial Intelligence. Springer-V erlag,Heidelberg.151{
157.
Wittgenstein, Ludwig 1953. Philosophic al Investigations .Basil Blackwell Ltd.
Wooldridge, M.and Jennings, N. R.1995. Intelligentagents:Theoryandpractice. Knowl-
edge Engineering Review 10(2):115{152.

258 BIBLIOGRAPHY

Appendix A
Trindi Kit functionalit y
A.1Introduction
Inthisappendix,wegiveamoredetaileddescription ofsomepartsof Trindi Kit relevant
totheimplementationofthe IBISsystems. Thisdescription referstoversion 3.0 aof
Trindi Kit 1.
Apartfromthegeneralarchitecture definedin 1.5,the Trindi Kit provides,amongother
things,
²definitions ofdatatypes,forusein TISvariabledefinitions
²aformatfordefining datatypes
²methods(checks,queriesandupdates)foraccessing the TIS
²alanguage forspecifying TISupdaterules
²anupdatealgorithm language formodules
²acontrolalgorithm language forthecontroller,including concurren tcontrol
²simpledefaultmodulesforinput,interpretation, generation andoutput
²useofexternal resources
1Thelatestofficial versionof Trindi Kit isavailable fromthe Trindi Kit webpage,
www.ling.gu.se/projekt/trindi .Version 3.0 aisavailablefromwww.ling.gu.se/~sl/Thesis .
259

260 APPENDIX A. TRINDIKIT FUNCTIONALITY
Wewillfirstexplainhowdatatypesaredefined,andgivespecifications ofsomedatatypes
usedby IBIS. Wethenshowhowthesedefinitions relatetothesyntaxandsemanticsof
conditions, queriesandupdates. Wegoontoshowhowconditions, queriesandupdatesare
usedinformulatingupdaterules. Twoalgorithm specification languages, forcoordinating
updaterulesandmodules,respectively,arethenintroduced. Finally,wedescribesomeof
themodulesincluded inthe Trindi Kit package.
A.2Datatypes
Datatypes 2 areusedextensivelyinthe Trindi Kit architecture, mostimportantlyfor
modellingthe TIS. Datatypesprovideanaturalwayofformalizing information states.
The TISisspecifiedusingabstract datatypes,eachpermitting aspecificsetofqueriesto
inspectthetypeandoperations tochangeit.
The Trindi Kit providesanumberofdatatypedefinitions, towhichtheusermayaddher
own.
A.2.1 Datatypedefinition format
Adatatypedefinition mayincludethefollowing:
1.relations
2.functions
3.selectors
4.operations
Datatypesareimplemen tedintheformof Prologclauses,hererepresentedintheform
Head ClauseüBodyorsimply Head Clause.
2Analternativ etermis\(abstract) datastructure".

A.2. DATATYPES 261
Relations
Theargumen tsofarelationareobjects,andthedefinition oftherelationspecifiesbetween
whichobjectstherelationholds. Forexample, therelationinhastwoargumen ts,aset S
ofobjectsoftype Tandanobject Xoftype T,andholdsif Xisamemberof S.
Theheadclauseofarelationdefinition hastheformin(A.1).
(A.1)relation( Rel,[Arg 1;:::;Argn])
Asampledefinition ofarelationisisshownin(A.2).
(A.2)relation( <,[A;B])üA<B
Relations mayalsobeindirectly definedbyfunctions andselectors, aswillbeexplained
below.
Functions
Functions takeobjectsasargumen tsandreturnanewobject. Forexample, thefunction
fsttakesastack Softypestack(T)andgivesthetopmost element X(oftype T)ofthe
stack. Ifthestackisempty,theresultofthefunction isundefined; thatis,functions may
bepartial.
Theheadclauseofafunction definition hastheformin(A.3).
(A.3)function( Fun,[Arg 1;:::;Argn],Result)
Asampledefinition ofarelationisisshownin(A.4).
(A.4)function( arity,[set(Xs)],N)ülength(Xs;N).
Everyfunction correspondstoarelationaccording totheschemain(A.5).
(A.5)relation( Fun,[Arg 1;:::;Argn;Result])ü
function( Fun,[Arg 1;:::;Argn],Result)
Forexample, giventhefunction aritywealsohavearelationaritywhoseargumen tsisa
set Sandaninteger N;thisrelationholdsifthe Nistheresultofapplying arityto S,i.e.
if Nisthearityof S.

262 APPENDIX A. TRINDIKIT FUNCTIONALITY
Selectors
Selectors canberegarded asaspecialkindoffunctions whichcanbeappliedtocollections
ofobjects(i.e.objectscontainingotherobjects,e.g.sets,stacksandrecords) toselect
objectsinthecollection.
Theheadclauseofafunction definition hastheformin(A.6).
(A.6)selector( Sel,Coll,Obj,Coll With Hole,Hole)
Here,Collisacollection (e.g.astack),Objistheobjectin Collselected by Sel.
Coll With Holeisacopyof Collwith Objreplaced byaprologvariable Hole. Thereason
forthiswayofimplemen tingselectors israthertechnicalandwewillnotbepursued here.
Asampledefinition ofaselectorisisshownin(A.7).
(A.7)selector( fst,stack([Fstj Rest]),Fst,stack([Holej Rest]),Hole
)
Everyselectorcorrespondstoafunction according totheschemain(A.8).
(A.8)function( Sel,[Coll],Obj)ü
selector( Sel,Coll,Obj,Coll With Hole,Hole)
Forexample, giventheselectorfstwhichselectsanobject Objinastack S,wealsohave
afunction fstwhoseargumen tis Sandanwhoseresultis Obj. Theresultofapplying this
function to Sis Objif Objisthetopmost elementof S.
Sinceeachselectorcorrespondstoafunction andeachfunction correspondstoarelation,
itfollowsthateachselectorcorrespondstoarelation. Forexample, giventheselectorfst
whichselectsanobject Objinastack S,wealsohavearelation fstwhichholdsiffst
selects Objin S.
Operations
Operations takeaninputobjectand(optional) argumen tsandreturnanoutputobject.
Theobjectsin Trindi Kit areimmutable ,whichmeanstheycannotbechanged. What
operations doistoreplaceanobjectwithanotherobjectwhichistheresultofapplying
theoperationtotheoriginalobject.

A.2. DATATYPES 263
Theheadclauseofanoperationdefinition hastheformin(A.9).
(A.9)operation( Opr,Objin,[Arg 1;:::;Argn],Objout)
Asampledefinition ofanoperationisisshownin(A.10).
(A.10)operation( push,stack(Xs),[X],stack([Xlj Xs]))
Everyoperationcorrespondstoarelationaccording totheschemain(A.11).
(A.11)relation( Opr,[Objin,Arg 1;:::;Argn,Objout])ü
operation( Opr,Objin,[Arg 1;:::;Argn],Objout)
Forexample, giventheoperationpushwhichpushesanobject Xonastack Stack in,
resulting inastack Stack out,wealsohavearelationpushwhoseargumen tsare Stack in,
X,and Stack out. Thisrelationholdsif Stack outistheresultofpushing Xon Stack in.
Somedatatypesusedby IBi S
Inthissection,welistthedefinitions ofsomeofthedatatypesusedintheimplementation
of IBi S. Relations, functions, selectors andoperationsarehererepresentedastheyappear
inupdaterules,ratherthanhowtheyappearinthedatatypedefinitions. Therelation
betweentheserepresentationisthefollowing:
²Rel(Arg 1;:::;Argn)givenrelation( Rel,[Arg 1;:::;Argn])
²Fun(Arg 1;:::;Argn)givenrelation( Fun,[Arg 1;:::;Argn],Result)
²Coll=Selgivenselector( Sel,Coll,Obj,Coll With Hole,Hole)
²Opr(Arg 1;:::;Argn)givenrelation( Opr,Objin,[Arg 1;:::;Argn],Objout)
Relations aredescribedintermsoftruthconditions, i.e.whathastobetruefortherelation
tohold. Forfunctions, thereisadescription oftheresultofapplying thefunction toits
argumen ts. Forselectors, theselectedobjectisdescribed. Foroperations, thedescription
explains howtheoperationmodifiestheobjecttowhichitisapplied.
Someofthedescriptions belowarepartialinthesensethatnotallrelations, functions,
selectors andoperations areincluded. Wehavemainlyincluded thoseusedin IBi S.

264 APPENDIX A. TRINDIKIT FUNCTIONALITY
Set
Simpleunordered set.
type:set
rel:n
in(Set,X):Xisunifiable withanelementof Set
fun:n
arity(Set):thenumberofelements in Set
sel:n
Set/elem:anelement(member)of Set
opr:8
><
>:add(X):addsanelement X
del(X):deletesanelementunifiable with X,failsifnoelementisunifiable with X
extend( Set):addallelements of Set
Stack
Simplestack.
type:stack
rel:n
fst(Stack,X):Xisunifiable withthetopmostelementof Stack
fun:n
arity(Stack):thenumberofelements in Stack
sel:n
Set/fst:thetopmostelementof Set
opr:(
push(X):make Xthetopmostelement
pop:popthestack,i.e.removethetopmostelement
Openstack(\stackset")
Stackwithsomeset-likeproperties. Non-topmost elementscanbeaccessed. Openstacks
cannotcontaintwounifiable elements.
type:openstack
rel:(
fst(Stack,X):Xisunifiable withthetopmostelementof Stack
in(Stack,X):Xisunifiable withanelementof Set
fun:n
arity(Stack):thenumberofelements in Stack
sel:n
Set/fst:thetopmostelementof Set

A.2. DATATYPES 265
opr:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:push(X):ifnoelementisunifiable with X,make Xtopmost;
if Xisunifiable withanelement Y,make Ythetopmostelement
raise(X):makeanelementunifiable with Xthetopmostelement;
failsif Xisnotunifiable withanyelement
pop:popthestack,i.e.removethetopmostelement;
failsifthestackisempty
del(X):deletesanelementunifiable with X;
failsifnoelementisunifiable with X
Queue
FIFOqueue.
type:queue
rel:n
none 3
fun:n
arity(Queue):thenumberofelements in Queue
sel:(
Queue/fst:thefirst(closesttoendtop)elementof Set
Queue/lst:thelast(closesttotheend)elementof Set
opr:(
push(X):make Xthelastelement
pop:popthequeue,i.e.removethefirstelement
Open Queue
FIFOqueuewithsomeset-likepropertiesanda\shift"operation.
type:openqueue
rel:8
>>><
>>>:fst(Queue,X):Xisunifiable withthetopmostelementof Queue
in(Queue,X):Xisunifiable withanelementof Set
fullyshifted( Queue):Queuehasbeenshiftedonecycle,
i.e.allelements havebeenshiftedonce
fun:n
arity(Queue):thenumberofelements in Queue
sel:(
Queue/fst:thefirst(closesttoendtop)elementof Set
Queue/lst:thelast(closesttotheend)elementof Set

266 APPENDIX A. TRINDIKIT FUNCTIONALITY
opr:8
>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>:push(X):ifnoelementisunifiable with X,make Xthelastelement;
if Xisunifiable withanelement Y,make Ythelastelement
pop:popthequeue,i.e.removethefirstelement; failsifthestackisempty
del(X):deletesanelementunifiable with X;
failsifnoelementisunifiable with X
shift:popandpushfirstelementtotheend;
requiresshiftingenabled
initshift:initialize queueforshifting
cancelshift:disableshifting
pair
Simplepairofobjects,possiblyofdifferenttypes. Wewillsometimes usethenotation
Fst-Sndforpairs.
type:pair
rel:n
none
fun:n
none
sel:(
Pair/fst:thefirstelementof Pair
Pair/snd:thesecondelementof Pair
opr:(
setfst(X):setthefirstelementto X
setsnd(X):thesecondelementto X
record
Recursiverecordstructure.
type:record
rel:n
none
fun:n
none
sel:n
Record/Label:thevalueof Labelin Record
opr:n
addfield(Label;Obj):addafieldwithlabel Labelandvalue Obj

A.2. DATATYPES 267
Typeindependent
Apartfromthetype-specificrelations, functions, selectors andoperations, therearesome
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
>>>:set(Obj):thevariableissetto Obj
unset:thevariableisunset(settonil)
clear:thevalueofthevariableissettobeanemptyobjectoftype T
(onlyusefulforcollections)
Resource objects,types,andvariables
Eachresource mustbedefinedasaresourceobjectofacertaintype,aresourcetype. The
definition ofthistypecanberegarded asainterfacetowhateverinput/output facilities
areavailablefortheresource itself,enabling theresource tobeaccessed by Trindi Kit .
Resources arehookeduptothe TISusingresource interfacevariables, andthevalueofa
resource interfacevariableisaresource object.
Asampleinterfacetypedefinition foralexicon(muchliketheoneusedby IBi S)isshown
in(A.12).
(A.12) type:lexicon T
rel:8
>>><
>>>:inputform(Lexicon; Phrase;Moves):Phraseisinterpretedas
Movesby Lexicon
outputform(Lexicon; Move;Phrase):Moveisgeneratedas
Phraseby Lexicon
fun:n
(none)
sel:n
(none)
opr:n
(none)
Theremaybeseveralresources ofeachtype;forexample, theremaybelexiconsforseveral
languages whichallareofthetypelexicon T. Foreachobject,atypedeclaration suchas
thosein(A.13)isneeded.

268 APPENDIX A. TRINDIKIT FUNCTIONALITY
(A.13)lexicontravelenglish:lexicon T
lexicontravelswedish:lexicon T
lexiconvcrenglish:lexicon T
lexiconvcrswedish:lexicon T
Tohookuparesource tothe TIS,weneedaresource interfacevariabletypedeclaration
andanassignmen tofaresource objecttothatvariable,asshownin(A.14).(See Section
A.3.4 foranexplanation oftheassignmen tsyntax.)
(A.14) lexicon:lexicon T
lexicon :=lexicontravelenglish
Anoteonthedifference betweenmodulesandresources: Resources aredeclarativ eknowl-
edgesources, external totheinformation state,whichareusedinupdaterulesandal-
gorithms. Modules,ontheotherhand,areagentswhichinteractwiththeinformation
stateandarecalleduponbythecontroller. Ofcourse,thereisaproceduralelementto
allkindsofinformation search,whichmeansamongotherthingsthatonemustbecareful
nottoengageinextensivetime-consuming searches. Conversely,modulescanbedefined
declarativ elyandthushaveadeclarativ eelement. Thereisnosharpdistinction dictat-
ingthechoicebetweenresource ormodule;forexample, itispossibletohavetheparser
bearesource. However,itisimportanttoconsider theconsequences ofchoosingtosee
something asaresource ormodule.
A.3Methodsforaccessing the TIS
The TIScanbeaccessed inthreeways:conditions ,queries,andupdates. Checkingand
querying arewaystofindoutwhattheinformation stateislike,andtheycanbind Pro-
logvariables. Updateschangetheinformation state,butcannotbind Prologvariables.
Conditions aretrueorfalse,whereas queryandapply-calls failorsucceed.
A.3.1 Objects,functions, locations,andevaluation
Theinformation statein Trindi Kit consists ofvariables whosevaluesareobjectsof
differenttypes. Whenexplaining thesyntaxforconditions in Section A.3.2 wewilluse
Objasavariablerangingoverallobjects;forexample, Objcanbeastackoraninteger. TIS
variablesareevaluatedusingthevariableevaluation operator\$",whichcanberegarded
asafunction from TISvariablestoobjects. Thesyntaxrulefor Objallowingobjectsto
bespecifiedusingevaluation ofa TISvariable TISvarisshownin(A.15).

A.3. METHODS FORACCESSING THETIS 269
(A.15) Obj!$TISvar
Objectscanalsobespecifiedusingevaluation offunctions; thefunction evaluation operator
isdenoted \$$".Givenafunction Funtakingargumen ts Arg 1;:::;Argn,thesyntaxrule
in(A.16)allowsspecifyinganobjectbyapplying Funto Obj 1;:::;Objn.
(A.16) Obj!$$Fun(Obj 1;:::;Objn)
Byusingpaths,builtupbyselectors, itispossibleto\point"atanobjectembeddedatthe
correspondinglocationinsidea(complex) objectandinspectormanipulate it. Pathsthus
appearintwocontexts:inspection,wheretheyspecifyobjects,andmanipulation, where
theyspecifylocations.
Anobject Xcanbespecifiedbyacomplex objectandaselector Selpointingout Xinside
thecomplex object. Thesyntaxruleforpointingoutembeddedobjectsusingselectors is
shownin(A.17).
(A.17) Obj!Obj=Sel
Thisrecursivedefinition allowsselectors tobeiterativelyappliedtoobjects,usingexpres-
sionsoftheform Obj=Sel 1=Sel 2:::=Seln;thisisequivalentto(:::((Obj=Sel 1)=Sel 2):::
=Seln).
Another basicconceptin Trindi Kit isthatoflocationsinobjects. Thegeneralsyntax
forlocationsisshownin(A.18);here,Selisaselectorand Objisacomplex object(a
collection).
(A.18) Loc!Loc=Sel
Loc!TISvar
Again,therecursivedefinition allowsselectors tobeiterativelyapplied, usingexpressions
oftheform TISvar=Sel 1=Sel 2:::=Seln;thisisequivalentto(:::((TISvar=Sel 1)=Sel 2):::
=Seln).
Forexample, assumewehavea TISwheretheinformation stateproper(the ISvariable)
hasthetypegivenin(A.19)andthevaluegivenin(1.19.)(Thisexamples assumes there
aredefinitions ofthetypes Propositionand Topic.)
(A.19) is:"
beliefs :Set(Prop osition)
topics =Stack(Topic)#
(A.20) is="
beliefs =fhappy(sys),frustrated(usr) g
topics =htheweather,foreignpoliticsi#

270 APPENDIX A. TRINDIKIT FUNCTIONALITY
Then,thefollowingholds:
²thelocationpointedtobyis/topics containstheobjecthweather,foreignpolitics
i
²$is/topics/fst isequivalenttotheweather
²thelocation is/beliefs/elem contains(indeterministically) somememberoftheset
fhappy(sys),frustrated(usr) g
²htheweather,foreignpoliticsi/fstisequivalenttotheweather
²$$arity($is/beliefs )isequivalentto 2
Trindi Kit offersashortcut representationforpathsintheinformation stateproper:
²theobject$/Pathisequivalentto$is=Path
²thelocation /Pathisequivalenttois=Path
A.3.2 Conditions
Thebasicsyntaxrulesforconditions isshownin(A.21).Argumen ts(Argi;1·i·n)are
eitherobjectsor(ifallowedbytherelationdefinition) prologvariables.
(A.21)a. Cond!Rel(Arg 11;:::;Argn
e.g.fst($/topics ,Q)
b. Cond!Arg 1::Rel(Arg 2;:::;Argn)
e.g.$/shared/qud ::fst(Q)
c. Cond!Obj 1=Obj 2
Thisholdsif Obj 1 and Obj 2 areunifiable.
d. Cond!Obj 1==Obj 2
Thisholdsif Obj 1 and Obj 2 areidentical.
Givenconditions Cond,Cond 1 and Cond 2,thefollowingconstructs arealsopossible:
²Cond 1 and Cond 2
Thisistrueif Cond 1 istrueand Cond 2 istrue.

A.3. METHODS FORACCESSING THETIS 271
²Cond 1 or Cond 2
Thisistrueif Cond 1 istrueor Cond 2 istrue. Cond 1 willbetestedfirst,andonlyif
itisfalsewill Cond 2 betested.
²not Cond
Thisistrueif Condisfalse.
²forall(Cond 1,Cond 2)
Thisisequivalenttonot(Cond 1 and(not Cond 2)).
²setof(Obj,Cond,Obj Set)
Obj Setisthesetofobjects Objsatisfying Cond.
Conditions and First Order Logic
Intermsof First Order Logic(FOL),acondition canbeseenasaproposition(whichis
trueorfalseofthe TIS),existentiallyquantifiedoverall Prologvariablesoccuringinthe
condition -exceptforvariables occuringonlywithinthescopeofnegation oruniversal
quantification.
Anillustration isshownin(A.22)(C1(X),C2(X;Y)and C3(Y;Z)areconditions; X,Y
and Zare Prologvariables, andx;yandzarethecorresponding FOLvariables).
(A.22)(C1(X)and C2(X;Y)and C3(Y;Z))»
9 x;y;z(C1(x)^C2(x;y)^C3(y;z))
Negation
Whenevaluating \not Cond",some Prologvariablesappearingin Condmayalreadyhave
becomebound(whenevaluating aprevious check).Anypreviously boundvariablesap-
pearingin Condwillstillbeboundwhenevaluating "not Cond.
(A.23)(C1(X)and(not C2(X))and C3(Y;Z))»
9 x;y;z(C1(x))^:C2(x)^C3(y;z)
Anypreviously unboundvariablesappearingin Condwillnotbeboundbychecking\not
Cond".Theyareinterpreted asexistentiallyquantifiedwithinthescopeofthenegation,
asillustrated in(A.24).Anyoccurrences ofthesevariablesoccuringinfollowingconditions
willbeindependent,i.e.theycanberegarded asseparate variables.

272 APPENDIX A. TRINDIKIT FUNCTIONALITY
(A.24)(C1(X)and(not C2(X;Y))and C3(Y;Z))»
9 x;y;z(C1(x))^:9 y 0(C2(x;y 0))^C3(y;z)
Universalquantification
Thebindingbehaviourof Prologvariablesinsidethescopeof\forall"issimilartothatfor
\not",whichisnaturalsince\forall"isdefinedusing\not".
If X1;:::;Xnarevariablesin Cond 1 whicharenotpreviously bound,and Y1;:::;Ymare
variablesin Cond 2 whicharenotpreviously boundanddonotoccurin Cond 1,the FOL
interpretation isasshownin(A.25).
(A.25)forall(Cond 1;Condn)»
8 x 1;:::;xn(Cond 1!9 y 1;:::;ym(Cond 2))
Anypreviously boundvariables appearingin Cond 1 or Cond 2 willstillbeboundwhen
evaluating \forall(Cond 1;Cond 2)".Anypreviously unboundvariablesappearingin Cond 1
or Cond 2 willnotbeboundbychecking\forall(Cond 1;Cond 2)".Anyoccurrences ofthese
variablesoccuringinfollowingconditions willbeindependent,i.e.theycanberegarded
asseparate variables.
A.3.3 Queries
Queriesaresimilartoconditions inthattheydonotmodifytheinformation state;however,
theyarealsosimilartoupdatesinthattheydonotbacktrack,andiftheyfailtheyproduce
anerrormessage. Thesyntaxforqueriesisshownin(A.26).
(A.26) Query!!Cond
Forexample, aquery\!in($/topics ,Q)"willbind Qtothetopmost elementofthestack
in/topics .However,ifthestackisemptyanerrormessage willbereported.
A.3.4 Updates
Updatesmodify TIS,andifanupdatefails,anerrormessage isreported. Thebasicsyntax
forupdatesisshownin(A.27).

A.4. RULEDEFINITION FORMA T 273
(A.27)a. Update!Opr(Loc;Obj 1;:::;Objn)
e.g.push(/topics, sports)
b. Update!Loc::Obj 1;:::;Objn)
e.g./topics::push(sports)
c. Update!Loc:=Obj
Equivalenttoset(Loc;Obj).
Givenupdates Update,Update 1;:::;Update n,theconstructions in(A.28)arealsopossible.
(A.28)a. Update![Update 1;:::;Update n]
Execute Update 1;:::;Update ninsequence.
b. Update!ifdo(Cond,Update)
If Condholds,execute Update.
c. Update!ifthenelse(Cond,Update 1,Update 2)
If Condholds,execute Update 1;otherwise, execute Update 2.
d. Update!foralldo(Cond,Update)
(Seebelowforexplanation)
Itispossibletoapplyanoperationrepeatedlyusingasingleupdatecallwiththesyntax
\foralldo(Cond,Update)",where Condisacondition and Updateisanupdate.
Let X1;:::;Xnbeallunbound Prologvariablesin Cond(i.e.thosewhicharenotbound
whentheupdateisapplied). Now,theinterpretation of\foralldo(Cond,Update)"goes
asfollows:\Forallbindings of X1;:::;Xnwhichmake Condtrue,apply Update."
Asanexample, forall Asuchthat Aisintheset/beliefs ,(A.29)willpush Aonthe
stackat/topics .
(A.29)foralldo(in($ /beliefs ,A),push(/topics ,A))
A.4Ruledefinition format
Updaterulesarerulesforupdatingthe TIS. Theyconsistofarulename,aprecondition list,
andaneffectlist. Preconditions areconditions, andeffectscanbequeriesorupdate-calls.
Ifthepreconditions ofarulearetrueforthe TIS,thentheeffectsofthatrulecanbe
appliedtothe TIS. Rulemayalsobelongtoaclass.

274 APPENDIX A. TRINDIKIT FUNCTIONALITY
Theruledefinition formatisshownin(A.30).
(A.30) rule:Rule Name
class: Rule Class
pre:n
Precond List
eff:n
Effects List
Here,Precond List isalistofconditions and Effects List isalistofqueriesandupdates.
The Rule Classmaybeusedindefining DMEalgorithms (Section A.5).
Theprecondition list Cond 1;:::;Cond 2 inaruleisequivalenttoaconjunction \Cond 1
and:::and Condn".Anyvariablesthatbecomeboundwhilecheckingthepreconditions
willstillbeboundwhenexecuting theeffects.
A.4.1 Backtrackingandvariablebindinginrules
Whenaruleisappliedtothe TIS,thepreconditions willbeevaluatedintheorderthey
appear. Sinceconditions maybenondeterministic, conditions containing Prologvariables
mayhaveseveralpossibleresults. Forexample, checking\member(X)"onasetfa,b,cg
has X=a,X=band X=caspossibleresults.
Thefirsttimethischeckismade,thefirstsolution willbereturned, i.e. Xwillbecome
boundtoa. Ifalaterprecondition whichuses Xisnottruefor X=a,Trindi Kit willuse
Prolog's backtrackingfacilitytogobackandgetthesecondsolution X=b. Inthisway,the
Trindi Kit ruleinterpreter willtrytofindawaytobindthe Prologvariablesappearing
intheprecondition list 4 sothatallthepreconditions hold.
Oncethishassucceeded, theeffectsoftherulewillbeappliedusingthevariablebindings
obtained whencheckingthepreconditions. Continuingtheexample above,ifallprecon-
ditionssucceed with Xboundtoa,thisbindingwill\survive"totheeffectsandany
appearanceof Xintheeffectswillbeequivalenttoanappearanceofa.
A.4.2 Condition andoperationmacros
Inaddition totheconditions andoperationsprovidedbythedatatypedefinitions, itisalso
possibletowritemacros. Macrosdefinesequences ofconditions (forcondition macros)
4 apartfromthoseappearinginthescopeofanegation oruniversalquantification, see A.3.2 and A.3.2
respectively

A.5. THEDME-ADL LANGUA GE 275
oroperations (foroperationmacros).Likeconditions andoperations (butunlikerules),
macroscantakeargumen ts.
Macrosaredefinedbyassociatingamacrowithalistof TISconditions oralistof TIS
updates.
(A.31)macrocond(beliefandtopic(X),[in($/belief,X),in(
$/topic,X)])
(A.32)macroupdate(addtobeliefandtopic,[add(/belief,X),
push(/topic,X)])
A.4.3 Prologvariablesinthe TIS
Trindi Kit doesnotprohibit Prologvariablesaspartofthe TIS,i.e.objectscancontain
Prologvariables. Thishastheadvantagethatitispossibletohavepartially uninstan tiated
objects(non-groundtermsin Prologterminology) whichmaybecomefullyinstantiatedat
alaterpoint.
However,thisalsomakesitpossibleforchecksandqueriestotemporarilychangethe
information statebyunifying apartially instantiatedobjectinthe TISwithamorespecific
object. Forexample, ifthevalueofthe TISvariable latestmoveisask(?happy(X)),
checking$latestmove=ask(?happy(john))willhavetheeffectthatlatestmove
nowhasthevalueask(?happy(john)).
Ifthischeckispartofthepreconditions listofarule,andalaterprecondition fails,
Trindi Kit maybacktrackwhichmayresultin Xbecoming unboundagain. Thesebind-
ings\survive"withinthescopeofanupdateruleorasequence ofconditions. Afterthe
ruleorsequence ofchecksisdone,any Prologvariablesinthe TISwillagainbeunbound.
A.5The DME-ADL language
DME-ADL (Dialogue Move Engine Algorithm Definition Language) isalanguage forwrit-
ingalgorithms forupdatingthe TIS. Algorithms in DME-ADL areexpressions ofanyof
thefollowingkinds(Cisa TIScondition; R,Sand Tarealgorithms, Ruleisthenameof
anupdaterule,and Rule Classisaruleclass):

276 APPENDIX A. TRINDIKIT FUNCTIONALITY
1. Rule
applytheupdaterule Rule
2. Rule Class
applyanupdateruleofclass Rule Class;rulesaretriedintheordertheyaredeclared
3.[R1;:::;Rn]
execute R1;:::;Rninsequence
4.if Cthen Selse T
If Cistrueofthe TIS,execute S;otherwise, execute T
5.while Cdo R
while Cistrueofthe TIS,execute Rrepeatedly
6.repeat Runtil C
execute Rrepeatedlyuntil Cistrueofthe TIS
7.repeat R
execute Rrepeatedlyuntilitfails;reportnoerrorwhenitfails
8.repeat+R
execute Rrepeatedly,butatleastonce,untilitfails;reportnoerrorwhenitfails
9.try R
trytoexecute R;ifitfails,reportnoerror
10. Rorelse S
Trytoexecute R;ifitfails,reportnoerrorandexecute Sinstead
11.test C
if Cistrueofthe TIS,donothing; otherwise, haltexecution ofthecurrentalgorithm
12.apply Op
applyoperation Op
13. Sub Alg
executesubalgorithm Sub Alg
Subalgorithms aredeclared using),whichispreceded bythesubalgorithm nameand
followedbythealgorithm, asin(A.33).
(A.33)mainupdate)hgrounding ,
repeat+(integrate orelseaccommodate)i

A.6. THECONTR OL-ADL LANGUA GE 277
Asample DME-ADL algorithm isshownin(A.34).
(A.34)if$latestmoves==failed
thenrepeatrefill
elsehgrounding,
repeat+(integrate orelseaccommodate),
if$latestspeaker ==usr
thenhrepeatrefill,
trydatabasei
elsestore
i
A.6The Control-ADL language
Thecontrolalgorithm specifieswhether asystemshouldberuninserialorasynchronously .
Serialalgorithms aresimplerthanasynchronousones,andthesyntaxusedforasynchronous
algorithms subsumes thesyntaxforserialalgorithms. Since IBi Susesonlyserialcontrol,
wewillnotintroducethesyntaxforasynchronous controlhere.
A.6.1 Serialcontrolalgorithm syntax
Theserial Control-ADL language issimilartothe DME-ADL language, exceptthatitcalls
modulealgorithms insteadofrules,anditcanincludethe\printstate"instruction. Each
algorithm hasaname,andeachmodulemaydefineoneormorealgorithms.
Asampleserial Control-ADL algorithm isshownin(A.35).
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

278 APPENDIX A. TRINDIKIT FUNCTIONALITY
A.7Providedmodules
The Trindi Kit packageincludes acoupleofsimplemoduleswhichcanbeusedtoquickly
buildprototypesystems.
²inputsimpletext :asimplemodulewhichreadstextinputfromtheuserandstores
itinthe TIS
²outputsimpletext :asimpletextoutputmodule
²intpretsimple 1 :aninterpretation modulewhichusesalexiconofkeywordsand
phrasestointerpretuserutterances intermsofdialogue moves
²generatesimple 1 :ageneration modulewhichusesalexiconofmainlycanned
sentencestogenerate systemutterances frommoves
A.7.1 Simpletextinputmodule
Theinputmoduleinputsimpletext readsastring(untilnew-line) fromthekeyboard,
preceded bytheprintingofaninputprompt. Thesystemvariable inputisthensettobe
thevalueread.
A.7.2 Simpletextoutputmodule
Theoutputmoduleoutputsimpletext takesthestringinthesystemvariable output
andprintsitonthecomputer screen,preceded bytheprintingofanoutputprompt. The
contentsoftheoutput variableisthendeleted. Themodulealsomovesthecontentsof
thesystemvariable nextmovestothesystemvariable latestmoves. Finallyitsets
thesystemvariable latestspeaker tobethesystem.
A.7.3 Asimpleinterpretation module
Theinterpretation moduleinterpretsimple 1 takesastringoftext,turnsitintoase-
quenceofwords(a\sentence")andproducesasetofmoves. The\grammar" consists
ofpairings betweenlistswhoseelementsarewordsorsemanticallyconstrained variables.
Semanticconstrain tsareimplemen tedbyasetofsemanticcategories (location,month,

A.7. PROVIDED MODULES 279
meansoftransportetc.)andsynonymysets. Asynonymysetisasetofwordswhich
allareregarded ashavingthesamemeaning.
Thesimplest kindoflexicalentryisonewithoutvariables. Forexample, theword\hello"
isassumed torealizeagreetmove.:
(A.36)inputform([hello],greet)
Thefollowingrulesaysthataphraseconsisting oftheword\to"followedbyaphrase S
constitutes ananswermovewithcontentto(C)providedthatthelexicalsemanticsof S
is C,and Cisalocation .Thelexicalsemanticsofawordisimplemen tedbyacoupling
betweenasynsetandameaning; thelexicalsemanticsof Sis C,providedthat Sisa
memberofasynonymysetofwordswiththemeaning C.
(A.37)inputform([toj S],answer(to(C))ülexsem( S,C),loca-
tion(C).
Toputitsimply,theparsertriestodividethesentenceintoasequence ofphrases(found
inthelexicon), coveringasmanywordsaspossible.
A.7.4 Asimplegeneration module
Thegeneration modulegenerateoutputform takesasequence (list)ofmovesandout-
putsastring. Thegeneration grammar/lexicon isalistofpairsofmovetemplates and
strings.
(A.38)outputform(greet,"Welcometothetravelagency!" ).
Torealizealistof Moves,thegenerator looks,foreachmove,inthelexiconforthecor-
respondingoutputform(asastring),andthenappendsallthesestringstogether. The
outputstringsisappendedinthesameorderasthemoves.

280 APPENDIX A. TRINDIKIT FUNCTIONALITY

Appendix B
Rules andclasses
Thisappendixlistsruleclassesusedbythevariousversionsof IBi S. Rulesarelistedin
theordertheyaretriedwhenthecorrespondingruleclassiscalledinamodulealgorithm.
The IBi Ssystemsand Trindi Kit canbedownloaded from:
http://www.ling.gu.se/~sl/Thesis .
Thesizeofthesystemsrangefromapproximately 1,200 linesofcode(32 kbyte)for IBi S1
toabout 2,500 lines(75 kbyte)for IBi S4,excluding domain-sp ecificresources.
B.1IBi S1
B.1.1IBi S1 updatemodule
²grounding
{get Latest Mo ve(rule 3.1)(p.41)
²integrate
1.integrate Usr Ask (rule 3.3)(p.44)
2.integrate Sys Ask (rule 3.2)(p.43)
3.integrate Answ er(rule 3.4)(p.47)
4.integrate Greet (rule 3.6)(p.48)
5.integrate Sys Quit (rule 3.8)(p.49)
281

282 APPENDIX B. RULES AND CLASSES
6.integrate Usr Quit (rule 3.7)(p.48)
²downdatequd
1.downdate QUD (rule 3.5)(p.48)
2.downdate QUD2 (rule 3.16)(p.63)
²loadplan
1.recover Plan (rule 3.17)(p.64)
2.find Plan (rule 3.9)(p.49)
²execplan
1.remove Findout (rule 3.10)(p.50)
2.remove Raise (rule 3.19)(p.66)
3.execconsult DB (rule 3.11)(p.50)
B.1.2IBi S1 selectmodule
²selectaction
1.select Resp ond(rule 3.14)(p.53)
2.select From Plan (rule 3.12)(p.51)
3.reraise Issue (rule 3.18)(p.65)
²selectmove
1.select Answ er(rule 3.15)(p.54)
2.select Ask (rule 3.13)(p.52)
3.select Other
B.2IBi S2
B.2.1IBi S2 updatemodule
²grounding
{get Latest Mo ves(rule 4.16)(p.130)

B.2. IBIS2 283
²integrate
1.integrate Usr Ask (rule 4.1)(p.110)
2.integrate Sys Ask (rule 4.18)(p.132)
3.integrate Neg Icm Answ er(rule 4.7)(p.115)
4.integrate Pos Icm Answ er(rule 4.8)(p.116)
5.integrate Usr Answ er(rule 4.4)(p.113)
6.integrate Sys Answ er(rule 4.19)(p.132)
7.integrate Und In t ICM (rule 4.6)(p.115)
8.integrate Usr P er Neg ICM (rule 4.20)(p.133)
9.integrate Usr Acc Neg ICM (rule 4.21)(p.135)
10.integrate Other ICM (rule 4.10)(p.121)
11.integrate Greet
12.integrate Sys Quit
13.integrate Usr Quit
14.integrate No Mo ve
²downdatequd
{downdate QUD
{downdate QUD2
²loadplan
1.recover Plan (rule 4.24)(p.143)
2.find Plan (rule 4.23)(p.143)
²execplan
1.remove Findout
2.execconsult DB
²(none)
{irrelevant Followup(rule 4.22)(p.141)
{unclear Followup

284 APPENDIX B. RULES AND CLASSES
B.2.2IBi S2 selectmodule
²selectaction
1.reject Issue (rule 4.15)(p.129)
2.reject Prop (rule 4.14)(p.127)
3.select Icm Und In t Ask(rule 4.3)(p.112)
4.select Icm Und In t Answer(rule 4.5)(p.114)
5.select Resp ond(rule 4.26)(p.147)
6.select From Plan
7.reraise Issue (rule 4.25)(p.144)
²selecticm
1.select Icm Con Neg (rule 4.9)(p.120)
2.select Icm P er Neg (rule 4.11)(p.121)
3.select Icm Sem Neg (rule 4.12)(p.122)
4.select Icm Und Neg (rule 4.13)(p.123)
5.select Icm Other (rule 4.2)(p.111)
²selectmove
1.select Answ er(rule 4.27)(p.147)
2.select Ask
3.select Other
4.select Icm Other (rule 4.2)(p.111)
²(none)
{backup Shared (rule 4.17)(p.131)
B.3IBi S3
B.3.1IBi S3 updatemodule
²grounding
{get Latest Mo ves

B.3. IBIS3 285
²integrate
1.retract (rule 5.7)(p.180)
2.integrate Usr Ask
3.integrate Sys Ask
4.integrate Neg Icm Answ er(rule 5.10)(p.184)
5.integrate Pos Icm Answ er(rule 5.11)(p.189)
6.integrate Usr Answ er
7.integrate Sys Answ er
8.integrate Accommo dation ICM
9.integrate Und P os ICM
10.integrate Und In t ICM
11.integrate Usr P er Neg ICM
12.integrate Usr Acc Neg ICM
13.integrate Other ICM
14.integrate Greet
15.integrate Sys Quit
16.integrate Usr Quit
17.integrate No Mo ve
²accommodate
1.accommodate Issues 2QUD (rule 5.2)(p.169)
2.accommodate QUD2Issues (rule 5.9)(p.183)
3.accommodate Plan 2Issues (rule 5.1)(p.166)
4.accommodate Com 2Issues (rule 5.6)(p.179)
5.accommodate Com 2Issues Dep endent(rule 5.8)(p.182)
6.accommodate Dependent Issue (rule 5.4)(p.172)
²downdateissues
{downdate ISSUES
{downdate ISSUES2 (similartodowndate QUD2 in IBi S1)
²downdatequd
{downdate QUD

286 APPENDIX B. RULES AND CLASSES
²loadplan
1.recover Plan
2.find Plan
²execplan
1.remove Findout
2.execconsult DB
²selectaction
1.select Icm Und In t Ask
2.select Icm Und In t Answer
3.select Icm Und In t Request
4.reject Issue
5.reject Action
6.reject Prop
²none
{irrelevant Followup
{unclear Followup
{failed Followup
{no Followup(rule 5.12)(p.190)
{backup Shared Usr (rule 5.13)(p.193)
B.3.2IBi S3 selectmodule
²selectaction
1.clarify Issue (rule 5.3)(p.170)
2.clarify Dep endent Issue (rule 5.5)(p.176)
3.select Resp ond
4.select From Plan
5.reraise Issue
²selecticm
1.select Icm Con Neg

B.4. IBIS4 287
2.select Icm P er Neg
3.select Icm Sem Neg
4.select Icm Und Neg
5.select Icm Other
²selectmove
1.select Quit
2.select Answ er
3.select Ask
4.select Greet
5.select Icm Other
²none
{backup Shared Sys
B.4IBi S4
B.4.1IBi S4 updatemodule
²grounding
{get Latest Mo ves
²integrate
1.retract
2.integrate Usr Ask
3.integrate Sys Ask
4.integrate Usr Request (rule 6.1)(p.216)
5.integrate Confirm (rule 6.6)(p.218)
6.integrate Neg Icm Answ er
7.integrate Pos Icm Answ er
8.integrate Usr Answ er
9.integrate Sys Answ er
10.integrate Accommo dation ICM

288 APPENDIX B. RULES AND CLASSES
11.integrate Und P os ICM
12.integrate Und In t ICM
13.integrate Usr P er Neg ICM
14.integrate Usr Acc Neg ICM
15.integrate Other ICM
16.integrate Greet
17.integrate Sys Quit
18.integrate Usr Quit
19.integrate No Mo ve
²accommodate
1.accommodate Issues 2QUD
2.accommodate QUD2Issues
3.accommodate Plan 2Issues
4.accommodate Com 2Issues
5.accommodate Com 2Issues Dep endent
6.accommodate Dependent Issue
7.accommodate Action (rule 6.8)(p.221)
²downdateissues
1.downdate ISSUES
2.downdate ISSUES2
3.downdate ISSUES3 (downdates resolvedaction-issue)
4.downdate Actions (rule 6.7)(p.218)
²downdatequd
{downdate QUD
²loadplan
1.find Plan
2.find Action Plan
²execplan
1.recover Plan
2.recover Action Plan

B.4. IBIS4 289
3.remove Findout
4.execconsult DB
5.execdevget
6.execdevset
7.execdevdo(rule 6.3)(p.217)
8.execdevquery
²selectaction
1.select Icm Und In t Ask
2.select Icm Und In t Answer
3.select Icm Und In t Request
4.reject Issue
5.reject Prop
6.reject Action (rule 6.2)(p.216)
²(none)
{backup Shared Usr
{irrelevant Followup
{irrelevant Followup
{unclear Followup
{failed Followup
{no Followup
{decline Prop
B.4.2IBi S4 selectmodule
²selectaction
1.clarify Issue
2.clarify Issue Action (rule 6.9)(p.221)
3.select Confirm Action (rule 6.4)(p.217)
4.select Resp ond
5.reraise Issue
6.select From Plan

290 APPENDIX B. RULES AND CLASSES
²selecticm
1.select Icm Con Neg
2.select Icm P er Neg
3.select Icm Sem Neg
4.select Icm Und Neg
5.select Icm Other
²selectmove
1.select Quit
2.select Answ er
3.select Ask
4.select Confirm (rule 6.5)(p.217)
5.select Greet
6.select Icm Other
²(none)
{backup Shared Sys