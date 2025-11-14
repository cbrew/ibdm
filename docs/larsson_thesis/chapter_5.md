Chapter 5
Action-orientedandnegotiative
dialogue
5.1 Introduction
Inthischapter,weextendtheissue-based approachtosimpleaction-orientedandnego-
tiativedialogue. First,wedealwithaction-orienteddialogue (AOD),whichinvolves DPs
performing non-comm unicativeactionssuchase.g.addingaprogram toa VCRorreserv-
ingticketsinatravelagency. Weextendthe IBi Ssystemtohandleasimplekindof AOD.
Inaddition toissuesandquestions underdiscussion, thissystemalsohastokeeptrackof
actions. Usually,itisusefulforan AODsystemtoalsohandle IOD.
Theconceptofissueaccommodationisextended toactionaccommodation. Wealsoshow
howmultiplesimultaneous plansmaybeusedtoenablemorecomplex dialogue structures,
andhowmultipleplansinteractwithactionsandissues. Weshowhowdialogue plans
maybeconstructed frommenus,andillustrate menu-based AODwithexamples froman
implementationofamenu-based VCRinterface.
Next,weturntonegotiativedialogue, anddescribeanissue-based accountofasimplekind
ofcollaborativenegotiativedialogue. Wealsosketchaformalization ofthisaccountand
discussitsimplementationin IBi S.
205

206 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
5.2 Issuesandactionsinaction-orienteddialogue
In IBi S3,eachdialogue planwasaimedatresolving aspecificissue. Ingeneral,ofcourse,
notalldialogue isaimedatresolving issues;oftenitisaimedtowardstheperformance of
some(non-comm unicative)action. Forexample, turningonoroffthelightsinaroom,
addingaprogram toa VCR,callingsomebodyup,ormakingareservationinatravel
agency. Actionorienteddialogue ingeneralplacesobligations on DPstoperformactions,
eitherduringthedialogue orafter. Forexample, bookingaticketinvolvesanobligation
ontheclerktosendatickettothecustomer, andonthecustomer topayfortheticket.
Requesting a VCRmanager toaddaprogram putsanobligation onthemanager addthe
program tothe VCRtimerrecording memory bank.
Wewillbedealingwithasimplekindof AOD,whereeachactioncanonlybeperformed
byoneofthe DPs,similartoourassumptions regarding issues. Thisallowsasimple
representationofactionsthatdoesnottakeintoaccountwhohastheobligation toperform
eachaction. Sincewearegivingexamples fromadevicecontroldomain(VCRcontrol),
wewillinfactonlydealwiththecasewhereallactionsareperformed bythesystem 1.
Previous workwith Go Di S,thepredecessor of IBi S,hasalsoaddressed thecasewherethe
userperformsalltheactions(Larsson, 2000,Larssonand Zaenen,2000).
5.3 Extending IBi Stohandleactionorienteddialogue
Inthissection,wedescribeadditions totheinformation state,semantics,anddialogue
moves. Updateruleswillbediscussed in Section 5.6.
5.3.1 Enhancing theinformation state
Inthissection,weshowhowthe IBi Sinformation stateneedstobemodifiedtohandle
Action Oriented Dialogue. Thenewinformation statetypeisshownin Figure 5.1.
Theonlyaddition istheactionsfieldwhichhasbeenaddedto/shared and/pri-
vate/tmp. Weassumetheactionsstackisanopenstack,whichisthesamestructure
thatweuseforissues.
1Ofcourse,eveninthissimpledomainitcannotreallybeassumed generally thatthesystemperforms
alltheactions; onecouldwellimagine a VCRcontroldialogue systemwhich,forexample, requests the
usertoinsertatapeintothe VCR.

5.3. EXTENDING IBISTOHANDLE ACTION ORIENTED DIALOGUE 207
2
66666666666666666666666664 private:2
666666664 agenda:Open Queue(Action)
plan :Open Stack(Plan Construct)
bel :Set(Prop)
tmp :"
usr:Tmp
sys:Tmp#
nim :Open Queue(P air(DP,Move))3
777777775
shared :2
666666666664 com :Set(Prop)
issues :Open Stack(Question)
actions :Open Stack(Action)
qud :Open Stack(Question)
pm :Open Queue(Mo ve)
lu :"
speaker :Participan t
moves:Set(Move)#3
7777777777753
77777777777777777777777775
Tmp=2
666666664 com :Set(Prop)
issues :Open Stack(Question)
actions :Open Stack(Action)
qud :Open Stack(Question)
agenda:Open Queue(Action)
plan :Open Stack(Plan Construct)3
777777775
Figure 5.1:IBi S4Information Statetype
Semantics
Tohandleaction AODweneedtoextendoursemantics. Giventhatff:Action,wehave
²action( ff):Proposition
²done(ff):Proposition
Roughparaphrases ofthesepropositionsare\action ffshouldbeperformed (byany DP
whocanperformff)",and\action ffhasbeensuccessfully performed", respectively.
Actionsandpostconditions
Thesetofactionsthatcanberequested dependsonthedomain; forexample, inthetravel
bookingdomainoneactionwouldbemakereservation ,andanexample fromthe VCR

208 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
controldomainisvcraddprogram. Fordialogues wherethetheuserrequests actionsto
beperformed bythesystem,eachsuchaction(whichwemayrefertoasagoal-action )is
associatedwithadialogue plan.
Indevicecontroldialogue, thereisalsoanadditional kindofactions,namelythosethat
arespecifiedbythedeviceitself;werefertotheseasdeviceactions. Wewillalsogeneralize
overdeviceactionsusingthe UPn Pprotocol(\Universal Plug'n'Pla y",Microsoft, 2000,
Boye et al.,2001,Lewin et al.,2001);thisrequires afurthertypeofupnpactionwhose
argumen tsisadeviceandadeviceaction. Thisallowsustoaccessmultipledevicesdefined
usingacommon interface. Thiswillbefurtherclarified in Section 5.4.1.
Deviceactionsand UPn Pactionscanbethoughtofasatomicactions,whereasgoalactions
aremorecomplex; specifically,theexecution ofasinglegoalaction(e.g.turningoffallthe
lightsinaroom)mayinvolvetheexecution ofseveraldeviceactions(e.g.turningoffeach
individual light).
Inaddition todomain-sp ecificgoalactionsanddeviceactions,westillhavetheissue-related
actionsfindout,raiseandrespondintroducedin Chapter 2,andthesetofdialogue moves.
Forissues,theresolvesrelationprovidedawaytodecidewhenanissuehasbeensuccess-
fullyperformed andshouldbepoppedoffthe/shared/issues stack. Foractions, we
insteadneedtodefinepostconditions whicharedefinedasrelations betweenactionsand
propositionsinthedomainresource; thesecanthenbeusedwhentodetermine whenan
actioncanberemovedfrom/shared/a ctions.
5.3.2 Dialogue moves
Inaddition tothedialogue movesintroducedin Chapters 2 and 3,IBi S4 usesthefollowing
twomoves:
²request( ff),whereff:Action
²confirm( ff),whereff:Action
Thesetwomovesaresufficientforactivities whereactionsareperformed instantlyornear-
instantly,andalwayssucceed. Iftheserequirementsarenotfulfilled, theconfirmmovecan
bereplaced byorcomplemen tedwithamoregeneralreport(ff,Status)movewhichreports
onthestatusofactionff. Possiblevaluesof Statuscouldbedone,failed,pending,initiated
etc.;report(ff,done)wouldcorrespondtoconfirm( ff).

5.4. INTERA CTING WITH MENU-BASED DEVICES 209
5.4 Interacting withmenu-baseddevices
Asasamplesubtypeofactionorienteddialogue wewillexploremenu-based AOD. While
menuinterfacesareubiquitous inmoderntechnology theyareoftentediousandfrustrat-
ing. Themechanisms ofaccommodationintroducedin Chapter 4 offersthepossibilityof
allowingtheusertopresentseveralpiecesofrelevantinformation atonetimeortopresent
information intheorderinwhichtheuserfindsmostnatural. Thismeansthatuserscan
usetheirownconception oftheknowledgespaceandnotbelockedtothatofthedesigner
ofthemenusystem.
First,wedescribeageneralmethodforconnecting devicesto IBi S,andthenweshowhow
menuinterfacescanbeconvertedintodialogue plansusingasimpleconversionschema.
5.4.1 Connecting devicesto IBi S
Figure 5.2:Connecting devicesto IBi S
Inthissectionwedescribebrieflyhow IBi Scaninteractwithdevicesusingthe UPn P
protocol. In Figure 5.2,weseeanimpression ofhowvariousdevicescanbeconnected to

210 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
IBi S. Wewillmainlybedealingwithdevicesthatcanbemodelledasresources, i.e.that
arepassive(orreactive)inthesensethattheycannotsendoutinformation unlessqueried
bysomeothermodule. Ofcourse,manydevicesarenotpassiveinthissensebutrather
active(orpro-active),e.g.burglaralarmsorrobots. Tohandleactivedevices,wewould
needtobuilda Trindi Kit modulewhichcouldwriteinformation toadesignated partof
theinformation statebasedonsignalsfromthedevice;thisinformation couldthentrigger
variousprocessesinothermodules. Still,evenforanactivedevicethesolution wepresent
herewouldbeveryuseful;minimally ,wewouldonlyneedtoaddamodulewhichsetsaflag
intheinformation statewheneverthedeviceindicates thatsomething needstobetaken
careof,triggering othermodulestoquerythedeviceaboutexactlywhathashappened.
Tobeabletohookuppassive UPn Pdevicesto IBi S,weneedthefollowing:
1.devicehandlerresources whichcommunicatedirectlywiththedeviceitself;thedevice
handlers canbesaidtorepresentthedevicein IBi S;
2.aresource typefor UPn Pdevices,specifyinghowdevicesmaybeaccessed asobjects
ofthistype;
3.aresource interfacevariabletothe TISwhosevaluesareofthe UPn Presource type;
thisvariablehooksupdevicestothe TIS;
4.planconstructs forinteracting withdevices, andupdaterulesforexecuting these
planconstructs;
5.dialogue plansforinteracting withdevices.
UPn Pdevicehandlers
Thedevicehandlermediates communication between IBi Sandthedeviceitself,andcan
besaidtorepresentthedevicefor IBi S. Weassumethateachspecificdevicehasaunique
ID,andisaccessed viaaseparate devicehandlerprocess. Adevicehandlerisbuiltfor
acertaindevicetype(e.g.the Panasonic NV-SD200 VCR),andeachdeviceofthattype
needstobeconnected toaprocessrunningthedevicehandler, inordertobeaccessed by
IBi S.
For UPn Pdevices, thedevicehandlercontainsaspecification partlyderivablefromthe
UPn Pspecifications, butmadereadable for IBi S(i.e.convertedfrom XMLtoprolog).
Thedevicehandlerdoesthefollowing:
²specifiesasetofactionsandassociatedargumen ts

5.4. INTERA CTING WITH MENU-BASED DEVICES 211
²specifiesasetofvariables, theirrangeofallowedvalues,and(optionally) theirdefault
value
²routines forsettingandreading variables (devsetanddevget),forperforming
queries(devquery),andforexecuting actions(devdo)
²accesses thedevicesim ulation
The UPn Presourceinterface
Inordertohookupadeviceto IBi Soneneedstodefineanabstract datatypefordevices
anddeclareasetofconditions andoperations onthatdatatype. For IBi S,weimplemen t
agenericresource interfaceintheformofanabstract datatypefor UPn Pdevices.
In UPn P,adeviceisdefinedintermsof
²asetofvariables
²asetofactionswithoptional argumen ts
Inaddition togettingthevalueofavariable,settingavariabletoanewvalue,andissuing
acommand, wealsoaddtheoptionofdefiningqueriestothedevice. Thesequeriesallow
morecomplex conditions tobechecked,e.g.whether twovariableshavethesamevalue.
Basedonthiswedefinethedatatypeupnpdevasin(5.1);here,Varisadevicevariable;
Valisthevalueofadevicevariable, Queryisaquestion, Answerisaproposition, ffdevis
adeviceaction,and Prop Setisasetofpropositions.
(5.1) type:upnpdev
rel:(
devget(Var;Val)
devquery(Query,Answer)
op:(
devset(Var,Val)
devdo(ffdev,Prop Set)
Deviceactionsmayhaveoneormoreparameters; forexample, inthe VCRcontroldomain
thereisanaction Add Program whichtakesparameters specifyingdate,program number,
starttime,andendtime. The Prop Setargumen tofdevdoisasetofpropositions, some
ofwhichmayserveasargumen tstoffdev. Intheresource interfacedefinition, thissetis
searchedbythedeviceinterfaceforargumen ts. Thismeansthat Prop Setisnottheexact
setofargumen tsneededforffdev;rather,itisarepositoryofpotentialargumen ts.

212 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Therelationbetween UPn Pactions,deviceactions,anddeviceoperations isexemplified
below:
²devdo(myvcr,Add Program) isa UPn Paction,whichmayappearinaplan
²Add Program isadeviceaction
²devdo(Add Program, fchanneltostore(1),starttimetostore(13:45), :::g)
isadeviceupdateoperation
Inaddition tothedatatypedefinition, onecandefineobjectstobeofthatdatatype. For
eachdevicethatthesystemshouldrecognize, thedevice IDshouldbedeclared tobeof
typeupnpdev.
5.4.2 Frommenutodialogue plan
Havingdescribeageneralmethodforconnecting devicesto IBi S,wewillnowshowhow
menuinterfacescanbeconvertedintodialogue plansusingasimpleconversionschema.
Weassumemenuinterfacesconsistof(atleast)thefollowingelements:
²multi-choic elists,wheretheuserspecifiesoneofseveralchoices
²dialoguewindows,wheretheuserentersrequested information usingthekeyboard
²tick-box,whichtheusercanselectorde-select
²pop-upmessages confirming actionsperformed system
Thecorrespondence betweenmenuelementsandplanconstructs isshownin Table 5.1.
Regarding confirmations, weprovideageneralsolution forconfirming actionsin Section
5.6.3. Confirmations thusdonotneedtobeincluded intheplan.
5.4.3 Extending theresolvesrelationformenu-based AOD
Inmenu-based AOD,thesystemmayaskanalternativ e-question aboutwhichactionthe
userwantsthesystemtoperform. Theusermaythenanswerbychoosingoneofthelisted

5.5. IMPLEMENT ATION OFTHEVCRCONTR OLDOMAIN 213
Menuconstruct Planconstruct
multi-choicelist actiontoresolvealternativ equestion aboutaction
hff 1;ff 2;:::;ffni findout(n
?action( ff 1),...,?action( ffn)o
)
tick-boxorequivalent actiontoresolvey/n-question
+/-P findout(? P)
dialogue window actiontoresolvewh-question
parameter= findout(? x:parameter(x))
pop-upmessage confirming ffconfirm( ff)
Table 5.1:Conversionofmenusintodialogue plans
alternatives. However,iftheuserselectsanactionwhichisnotinthelistedalternatives
butfurtherdowninthehierarchyofactions,thisshouldalsoberegarded asasananswer
thatresolvesthesystem's question. Tohandlethis,weneedtoextendthedefinition ofthe
resolvesrelation(see Section 2.4.6).
(5.2)action( ff)resolves f?action( ff 1),:::,?action( ffn)gif
²ff=ffior
²ffidominates ff(1·i·n)
Thedominates relationisdefinedrecursivelyasin(5.3).
(5.3)ffdominates ff 0 if
²thereisaplan Pforffsuchthat Pincludesfindout( Alt Q)
and?action( ff)2Alt Q,or
²ffdominates someactionff 00 andff 00 dominates ff 0
Theideais,then,thatdomination reflectsthemenustructure sothatanactiondominates
anyactionsbelowitinthemenu.
5.5 Implemen tationofthe VCRcontroldomain
AVCRmenusection
Westartfromasectionofthemenustructure fora VCRasshownin(5.4).

214 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
(5.4)²toplevel:hchange-pla y-status, change-channel, timer-
recording, :::i
{changeplaystatus:hplay,stop,:::i
{changechannel
¤new-channel=
¤confirmnewchannel
{timerrecording:hadd-program, delete-programi
¤addprogram
¢channel-to-store =
¢date-to-store =
¢start-time-to-store =
¢end-time-to-store =
¢confirmprogram added
¤deleteprogram
¢displayexistingprograms
¢program-to-delete:
¢confirmprogram deleted
{change-settings:hset-clock,:::i
Dialogueplansfor VCRcontrol
Usingtheconversionschemain Table 5.1 wecanconvertthemenustructures in(5.4)into
dialogue plansasthoseshownin(5.5).

5.6. UPDATERULES AND DIALOGUE EXAMPLES 215
(5.5)a.action :vcrtop
plan:h
raise(?x.action( x))
findout(8
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
plan:findout((
?action(vcraddprogram),
?action(vcrdeleteprogram))
)
post:done(vcraddprogram) or
done(vcrdeleteprogram)
c.action :vcraddprogram
plan:h
findout(?x.channeltostore(x))
findout(?x.datetostore(x))
findout(?x.starttimetostore(x))
findout(?x.stoptimetostore(x))
devdo(vcr,'Add Program')
i
post:done('Add Program')
5.6 Updaterulesanddialogueexamples
Inthissectionweshowhowupdaterulesforactionorienteddialogue havebeenimple-
mentedin IBi S4,andgiveexamples ofdialogues fromthe VCRcontroldomain.
5.6.1 Integrating andrejecting requests
First,weintroduceupdaterulesforintegrating requestmoves. Sincewearelimiting
thisimplementationtodomains wherethesystemperformsalltheactions, wewillnot
providerulesforintegrating requests fromthesystemtotheuser;however,thesecould
bestraightforwardlyimplemen tedsincetherelation betweensystemrequests anduser
requests isverysimilartotherelationbetweensystemanduseraskmoves.

216 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Theruleforintegrating userrequests isshownin(rule 5.1).
(rule 5.1)rule:integrate Usr Request
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
Thisruleissimilartothatforintegrating useraskmoves(see Section 3.6.6);insteadof
pushinganissue Qon ISSUESand QUD,andpushingrespond(Q)ontheagenda,thisrule
pushestherequested action Aon/shared/a ctionsand/private/agenda.
Asforuseraskmoveswealsoneedtodealwiththecasewherethesystemmustrejectan
actionsinceitdoesnothaveaplanfordealingwithit. Thisruleisshownin(rule 5.2).
(rule 5.2)rule:reject Action
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
5.6.2 Executing deviceactions
Theupdateruleforexecuting thedevdodeviceactionisshownin(rule 5.3).

5.6. UPDATERULES AND DIALOGUE EXAMPLES 217
(rule 5.3)rule:execdevdo
class:execplan
pre:n
fst($/private/plan,devdo(Dev,Adev))
eff:8
>>><
>>>:pop(/private/plan)
!$/shared/com=Prop Set
devices /Dev::devdo(Prop Set,Adev)
add(/private/bel,done(Adev))
Thecondition looksforadevdoupnpactionintheplan,withargumen ts Dev,thedevice
pathname,and Adev,thedeviceaction. Theupdatespoptheactionofftheplan,and
appliesthecorrespondingupdatedevdo(Prop Set,Adev)tothedevice Dev. Finally,the
propositiondone(Adev)isaddedthetheprivatebeliefs.
Inaddition, wehaveimplemen tedrulesforexecuting thedevget,devsetanddevquery
actions.
5.6.3 Selecting andintegrating confirm-moves
Theselection rulefortheconfirmactionisshownin(rule 5.4).
(rule 5.4)rule:select Confirm Action
class:selectaction
pre:8
>>><
>>>:fst($/shared/actions,A)
$domain ::postcond( A,PC)
in($/private/bel,PC)
notin($/shared/com,PC)
eff:n
push(/ private/agenda,confirm( A))
Theconditions inthisrulecheckthatthethereisanactionin/shared/a ctionswhose
postcondition isbelievedbythesystemtobetrue,however,thisisnotyetsharedinfor-
mation. Ifthisistrue,aconfirmactionispushedontheagenda. Eventually,thisaction
(whichalsoisadialogue move)ismovedtonextmovesby(rule 5.5).
(rule 5.5)rule:select Confirm
class:selectmove
pre:n
fst($/private/agenda,confirm( A))
eff:(
push(nextmoves,confirm( A))
pop(/private/agenda)

218 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Whentheconfirmation movehasbeenmade,itisintegrated bytherulein(rule 5.6).
(rule 5.6)rule:integrate Confirm
class:integrate
pre:n
$/private/nim/fst/snd=confirm( A)
eff:(
pop(/private/nim)
add(/shared/com,done(A))
Thisruleaddsthepropositiondone(A)tothesharedcommitmen tswhichenablesthe
downdate Actions rulein(rule 5.7)totrigger.
(rule 5.7)rule:downdate Actions
class:downdateissues
pre:8
><
>:fst($/shared/actions,A)
$domain ::postcond( A,PC)
in($/shared/com,PC)
eff:n
pop(/shared/actions)
Thisruleremovesanaction Awhosepostcondition isjointlybelievedtobetruefrom
actions 2.
5.6.4 Dialogue example: menutraversalandmultiplethreads
In(dialogue 5.1)weshowasampledialogue interaction withthemenu-based VCR
application. Itshowsbothmenutraversalandaccommodation,aswellasdealingwith
multipletasks(issuesandactions).
(dialogue 5.1)
S>Welcome tothe VCRmanager!
S>Letssee. Whatcan Idoforyou?
U>
2Notethatdone(ff)istrivially apostcondition foranyactionff.

5.6. UPDATERULES AND DIALOGUE EXAMPLES 219
$S>Doyouwanttochangeplaystatus,changechannel ,gototimer
recording orgotosettings?
U>gototimerrecording
$S>Okay. Letssee. Doyouwanttoaddaprogram ordeleteaprogram?
U>addaprogram today
S>Okay. Letssee. Whatchannel doyouwant?
U>whatchannel isonnow
2
66666666666666666666664 private=2
66664 agenda=­­
icm:acc*p osffff
plan =hi
bel =©
currentchannel(1)ª
tmp =:::
nim =hhii 3
77775
shared =2
6666666666664 com =©
datetostore(today)ª
actions =*vcraddprogram
vcrtimerrecording
vcrtop+
issues =­?E.currentchannel(E)ff
qud =hi
pm =©
ask(?A.channeltostore(A)),icm:loadplan, icm:acc*p osª
lu =·speaker =usr
moves =©
ask(?E.currentchannel(E))ª¸3
77777777777753
77777777777777777777775
S>Okay. Thecurrent channel is 1
S>Returning toaddaprogram. Whatchannel doyouwant?
U>one
S>Okay. Whattimedoyouwanttostartrecording?
U>stopthevcr
deviceresourceissuescommand todevice:[UPn P]Stop
S>Okay. The VCRisnowstopped.
S>Returning toaddaprogram. Whattimedoyouwanttostartrecording?
U>twelvethirty

220 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
S>Okay. Whattimedoyouwanttostoprecording?
U>twofifteen
deviceresourceissuescommand todevice:[UPn P]Add Program(1,to day,1230,215)
S>Okay. Theprogram hasbeenadded.
S>Returning totimerrecording. Doyouwanttoaddaprogram ordeletea
program?
N. B.:Inthisdialogue, theuser'squestion \Whatchannelisonnow"isregarded asan
irrelevantfollowupto\Whatchanneldoyouwant?".Tochangethisonecouldadda
dependency betweenthesequestions tothedomainresource (see Section 2.8.2),asin(5.6).
(5.6)depends(?x.channeltoadd(x),?x.currentchannel( x)))
5.6.5 Actionaccommodationandclarification
Wealsoimplemen tanaction-related counterparttotheruleaccommodate Dependen-
t Issuepresentedin Section 4.6.4. Thisallowstheusertoprovideparameters forsome
actionwithoutmakinganexplicitrequest.

5.6. UPDATERULES AND DIALOGUE EXAMPLES 221
(rule 5.8)rule:accommodate Action
class:accommodate
pre:8
>>>>>>>>>>>>>>>>>><
>>>>>>>>>>>>>>>>>>:setof(A,$/private/nim/elem/snd=answer(A),Ans Set)
$$arity(Ans Set)>0
$domain ::plan(Action,Plan)
$domain ::action(Action)
forall(in( Ans Set,A),in(Plan,findout( Q))and
$domain ::relevant(A,Q))
not$domain ::plan(Action 0,Plan 0)and Action 06=Actionand
forall(in( Ans Set,A),in(Plan 0,findout( Q))and
$domain ::relevant(A,Q))
notin($/private/agenda,icm:und*int:usr *action( Action))
eff:8
>>>>>><
>>>>>>:push(/ shared/actions,Action)
push(/ private/agenda,icm:accommo date:Action)
push(/ private/agenda,icm:und*p os:usr*action( action))
set(/private/plan,Plan)
push(/ private/agenda,icm:loadplan )
Thisruleisverysimilartotheaccommodate Dependent Issue(see Section 4.6.4),except
thatitaccommo datesadependentactionratherthanadependentissue.
Ifthesystemfindsseveralactionsmatchingtheinformation givenbytheuser,aclarification
question israised. Thisisagainsimilartothebehaviourforissuesdescribedin Section
4.6.5;infact,therulebelowreplaces thepreviousclarify Dep endent Issuerule.
(rule 5.9)rule:clarify Issue Action
class:selectaction
pre:8
>>>>>><
>>>>>>:in($/private/nim,pair(usr,answer(A)))
setof(Action,$domain ::depends(ff,Q)and
$domain ::relevant(A,Q),Action S et)
removeunifiables( Actions,Actions 0)
$$arity(Actions 0)>1
eff:8
>>>>>>>>>>>>><
>>>>>>>>>>>>>:!setof(?Issue Prop,in(Actions 0,Issue 0)and
not$domain ::action(Issue 0)and
Issue Prop=issue(Issue 0),Issue Questions )
!setof(?Action P rop,in(Actions 0,Action 0)and
$domain ::action(Action 0)and
Action P rop=action(Action),Action Questions )
!union(Issue Questions ,Action Questions ,Alt Q)
push(/ private/agenda,findout( Alt Q))

222 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Thepreconditions checkthatthereismorethanoneplan(forperforming actionsorresolv-
ingissues)towhichallanswersin/private/nim arerelevant. Thefirstupdatecreates
analternativ equestion regarding allissueswhichthenon-integrated answersarerelevant
to,andthesecondupdatedoesthesameforactions. Thethirdupdatejoinsthesetwo
alternativ e-questions (setsofy/n-questions) intoasingley/n-question, whichisaddedto
theagendabythefinalupdate.
5.6.6 Dialogue examples: actionaccommodationandclarifica-
tion
Thedialogue in(dialogue 5.2)demonstrates actionaccommodation,andthedialogue in
(dialogue 5.3)demonstrates aclarification question bythesystem.
(dialogue 5.2)
S>Welcome tothe VCRmanager!
S>Letssee. Whatcan Idoforyou?
U>todayfromfivethirtyonchannel one
S>Alright. addaprogram.
S>Letssee. Okay. Whattimedoyouwanttostoprecording?
(dialogue 5.3)
S>Welcome tothe VCRmanager!
S>Letssee. Whatcan Idoforyou?
U>sixthirty
$S>sixthirty. Idontquiteunderstand. Doyouwanttoaddaprogram
orsettheclock?
U>addaprogram
$S>Okay. Letssee. Doyouwanttorecordfromsixthirtyoruntil
sixthirty?
U>fromsixthirty
S>Okay. Whatchannel doyouwant?

5.7. ISSUES UNDER NEGOTIA TION INNEGOTIA TIVE DIALOGUE 223
5.7 Issuesundernegotiation innegotiativedialogue
Wewillnowturntonegotiativedialogue, anddescribeanissue-based accountofasimple
kindofcollaborativenegotiativedialogue. Wealsosketchaformalization ofthisaccount
anddiscussitsimplementationin IBi S.
Westartfromaprevious formalaccountofnegotiativedialogue (Sidner, 1994 a)andargue
foraslightlydifferentideaofwhatnegotiativedialogue is. Wewanttomakeadistinc-
tionbetweentheprocessofaccepting anutterance anditscontent,whichappliestoall
utterances, andaconcept ofnegotiation defined, roughly,asadiscussion ofseveralal-
ternativesolutions tosomeproblem. Thislatteraccountisformulatedintermsof Issues
Under Negotiation (IUN),representingthequestion orproblem toberesolved,andaset
ofalternativ eanswers,representingtheproposedsolutions.
First,wewillgiveabriefreviewof Sidner's theoryanddiscussitsmeritsanddrawbacks 3.
Wethenprovideanalternativ eaccountbasedontheconceptof Issues Under Negotiation.
Weexplainhow IUNcanbeaddedto IBi S,andgiveaninformation stateanalysis ofa
simplenegotiativedialogue.
5.7.1 Sidner's theoryofnegotiativedialogue
Asthetitleofthepapersays,Sidner's (1994 a)theoryisformulatedas\anartificial dis-
courselanguage forcollaborativenegotiation". Thislanguage consistsofasetofmessages
(ormessage types)withpropositional contents(\beliefs"). Theeffectsofanagenttrans-
mittingthesemessages toanotheragentisformulatedintermsofthe\stateofcommunica-
tion"afterthemessage hasbeenreceived. Thestateofcommunication includes individual
beliefsandintentions,mutualbeliefs,andtwostacksfor Open Beliefsand Rejected Beliefs.
Someofthecentralmessages are
²Propose For Accept (PFAagt 1 beliefagt 2):agt 1 expresses belieftoagt 2.
²Reject(RJagt 1 beliefagt 2):agt 1 doesnotbelievebelief,whichhasbeen
offeredasaproposal
²Accept Prop osal(APagt 1 beliefagt 2):agt 1 andagt 2 nowholdbeliefasa
mutualbelief
3Anin-depth description of Sidner's accountanditsrelationtothe Go Di Ssystem,including arefor-
mulationof Sidner's artificial negotiation language intermsof Go Di Sinformation stateupdates,canbe
foundin Cooper et al.(2001).

224 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
²Counter(COagt 1 belief 1 agt 2 belief 2) :Without rejecting belief 1,agt 1 of-
fersbelief 2 toagt 2
Inaddition, therearethreekindsofacknowledgemen tmessages, themostimportantbeing
Acknowledge Receipt (ARagt 1 beliefagt 2),whichmayoccuraftera Propose For-
Acceptmessage andresultsinbeliefbeingpushedonthestackfor Open Beliefs. Ac-
knowledgemen tindicates thataprevious message fromagt 2 aboutbeliefhasbeenheard;
theagentswillnotholdbeliefasamutualbeliefuntilan Accept Prop osalmessage has
beensent.
Whilewewillnotgiveadetailed analysis oftheeffectsofeachofthesemessages, some
observationsareimportantforthepurposesofthispaper. Specifically,acounter-proposal
(COagt 1 belief 1 agt 2 belief 2) isanalyzed asacompositemessage consisting oftwo
PFAmessages withpropositional contents. Thefirstproposedpropositionisbelief 2
(the\new"proposal),andthesecondis(Supports (Notbelief 1) belief 2) ,i.e.that
belief 2 supportsthenegation ofbelief 1 (the\old"proposal).Exactlywhatismeant
by\supports"hereisleftunspecified,butperhapslogicalentailmentisatleastasimple
kindofsupport.
²(PFAagt 1 belief 2 agt 2)
²(PFAagt 1(Supports (Notbelief 1) belief 2) agt 2)
Sidner'sanalysisofproposalsisonlyconcerned withpropositional contents. ARequest for
actionismodelledasaproposalwhosecontentisoftheform(Should-Do Agt Action).
Aquestion isaproposalfortheactiontoprovidecertaininformation. Thisbringsusto
ourfirstproblem with Sidner's account.
Problem 1:Negotiation vs.utterance acceptance
In Sidner's theory,alldialogue isnegotiativeinthesensethatallutterances (exceptac-
ceptances, rejections, andacknowledgemen ts)areseenasproposals. Thisiscorrectif
weconsider negotiation aspossiblyconcerning meta-asp ectsofthedialogue. Sinceany
utterance (content)canberejected, allutterances canindeedbeseenasproposals.
Soinonesenseof\negotiative",alldialogue isnegotiativesinceassertions (andquestions,
instructions etc.)canberejected oraccepted aspartofthegrounding process. Butsome
dialogues arenegotiativeinanothersense,inthattheycontainexplicitly discussions about
differentsolutions toaproblem. Negotiation, onthisview,isdistinctfromgrounding.

5.7. ISSUES UNDER NEGOTIA TION INNEGOTIA TIVE DIALOGUE 225
Thereisthusastronger senseofnegotiation whichisnotpresentinalldialogue. A
minimumrequiremen tonnegotiation inthisstronger sensecouldbethatseveralalternativ e
solutions (answers)toaproblem (question orissue)canbediscussed andcompared before
asolutionisfinallysettledon. Sidnerisawareofthisaspectofnegotiation, andnotesthat
\maintainingmorethanoneopenproposalisacommon featureofhumandiscourses and
negotiations." Whatwewanttodoistofindawayofcapturing thispropertyindependently
ofgrounding andofotheraspectsofnegotiation, anduseitasaminimal requiremen ton
anydialogue thatistoberegarded asnegotiative.
Onourview,proposal-movesaremovesonthesamelevelasotherdialogue moves:greet-
ings,questions, answersetc.,andcanthusbeaccepted orrejectedonthegrounding level.
Accepting aproposal-moveonthegrounding levelmerelymeansaccepting thecontent
ofthemoveasaproposal,i.e.asapotentialanswertoaquestion. Thisisdifferent
fromaccepting theproposedalternativ eastheactualsolution toaproblem (answertoa
question).
Togiveaconcrete example ofthesedifferentconcepts ofnegotiativit y,wecancompare the
dialogues in Examples (5.5)and(5.6).
(5.7)A:Todayis January 6 th.
proposeproposition
B(alt.1):Uhuh
acceptproposition
B(alt.2):No,it'snot!
rejectproposition
(5.8)S:wheredoyouwanttogo?
askquestion
U:flightstoparisonseptember 13 please
answerquestion
S:thereisoneflightat 07:45 andoneat 12:00
proposealternatives, giveinformation aboutalternatives
U:whatairlineisthe 12:00 one
askquestion
S:the 12:00 flightisan SASflight
answerquestion
U:I'lltakethe 7:45 flightplease
acceptalternative, answerquestion \whichflight?"
Thetypenegotiation in(5.7)concerns acceptance-levelgrounding oftheutterance andits
content. Bycontrast,thetypeofnegotiation in(5.8)concerns domain-levelissuesrather
thansomeaspectofgrounding.

226 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
Problem 2:Alternativ esandcounterproposals
Whenanalyzing atravelagencydialogue (Sidner,1994 b),thetravelagent'ssuccessivepro-
posalsofflightsareseenascounterproposalstohisownprevious proposals,eachmodelled
asaproposition. Thedifference betweenproposalsandcounterproposalsisthatthelatter
notonlymakeanewproposalbutalsoproposesthepropositionthatthenewproposal
conflicts withtheprevious proposal(bysupportingthenegation oftheprevious proposal).
Thiscanbeseenasanattempt by Sidnertoestablish theconnection betweenthetwo
proposalsassomehowconcerning thesameissue.
Thisanalysis isproblematic inthatitexcludes caseswherealternativesarenotmutually
exclusive,whichisnaturalwhene.g.bookingaflight(sincetheuserpresumably onlywant
oneflight)butnote.g.whenbuyinga CD(sincetheusermaywanttobuymorethanone).
Also,itseemsoddtomakecounterproposalstoyourownprevious proposals,especially
sincemakingaproposalcommits youtointendingtheaddressee toacceptthatproposal
ratherthanyourprevious ones. Inmanycases(including thetravelagencydomain) it
seemsthattheagentmayoftenbequiteindifferen ttowhichflighttheuserselects. Travel
agentsmayoftenmakeseveralproposalsinoneutterance, e.g.\Thereisoneflightat 7:45
andanotheroneat 12:00",inwhichcaseitdoesnotmakesensetosee\oneat 12:00"as
acounterproposalas Sidnerdefinesthem.
Wedonotwanttousetheterm\counterproposal"inthesecases;whatweneedissome
wayofproposingalternativeswithoutseeingthemascounterproposals. Thebasicproblem
seemstobethatwhenseveralproposalsare\onthetable"atonce,oneneedssomeway
ofrepresentingthefactthattheyarenotindependentofeachother. Sidnerdoesthis
byaddingpropositionsoftheform(Supports (Notbelief 1) belief 2) toshowthat
belief 1 andbelief 2 arenotindependent;however,thispropositionnotonlyclaimsthat
thepropositionsaresomehowdependent,butalsothattheyare(logically orrhetorically)
mutuallyexclusive. Inourview,thisindicates aneedforatheoryofnegotiation which
makesitpossibletorepresentseveralalternativesassomehowconcerningthesameissue,
independentlyofrhetorical orlogicalrelations betweenthealternatives. Negotiation, in
ourview,shouldnotingeneralbeseenintermsofproposalsandcounterproposals,butin
termsofproposingandchoosingbetweenseveralalternatives.
5.7.2 Negotiation asdiscussing alternatives
Inthissection,wewillattempt toprovideamoredetailed description ofnegotiativedi-
alogue. Clearly,negotiation isatypeofproblem-solving (Di Eugenio etal.,1998).We
definenegotiativedialogue morespecifically tobedialoguewhere DPsdiscussseveralal-
ternative solutions toaproblem(issue)beforechoosingone(orseveral)ofthem. Inline

5.7. ISSUES UNDER NEGOTIA TION INNEGOTIA TIVE DIALOGUE 227
withourissue-based approachtodialogue management,weproposetomodelnegotiable
problems (issues)semanticallyasquestions andalternativesolutions asalternativ eanswers
toaquestion.
Wealsoproposetokeeptrackofissuesundernegotiation andtheanswersbeingconsidered
aspotentialsolutions toeachissueinthe/shared/issues field,representedasquestions
associatedwithsetsofanswers.
Degreesofnegotiativit y
Starting fromthisdefinition, wecandistinguish betweenfullynegotiativedialogue and
semi-negotiativedialogue (seealso Section 2.1.2).Innon-negotiativedialogue, onlyone
alternativ ecanbediscussed. Insemi-negotiativedialogue, anewalternativ ecanbeintro-
ducedbyrevising parameters oftheprevious alternativ e;however,previous alternatives
arenotretained. Finally,innegotiativedialogue: severalalternativescanbeintroduced,
andoldalternativesareretained andcanbereturned to.
Semi-negotiativeinformation-orienteddialogue doesnotrequirekeepingtrackofseveral
alternatives. Allthatisrequired isthatinformation isrevisable, andthatnewdatabase
queriescanbeformedfromoldonesbyreplacing somepieceofinformation. Thisproperty
isimplemen tedinalimitedwayforexample inthe Swedishrailwayinformation system(a
variantofthe Philipssystemdescribedin Aust et al.,1994),whichafterprovidinginfor-
mationaboutatripwillasktheuser\Doyouwantanearlierorlatertrain?". Thisallows
theusertomodifytheprevious query(although inaverylimitedway)andgetinforma-
tionaboutfurtheralternatives. However,itisnotpossibletocompare thealternatives
byaskingquestions aboutthem;indeed,thereisnosignthatinformation aboutprevious
alternativesisretained inthesystem. Theimplementationofreaccommodationin IBi S3
(Section 4.6.6)alsoallowedsemi-negotiativedialogue inthissense.
Factorsinfluencing negotiation
Thereareanumberofaspectsofthedialogue situation whichaffectthecomplexit yof
negotiativedialogues, andallowsfurthersub-classification ofthem. Thissub-classification
allowsustopickoutasubspeciesofnegotiativedialogue toimplemen t.
Onourdefinition, negotiation doesnotrequireconflicting goalsorinterests,andforthis
reasonitmaynotcorrespondperfectlytotheeverydayuseoftheword\negotiation".
However,wefeelitisusefultokeepcollaborativity(i.e.lackofconflicting goals)asa
separate dimension fromnegotiation. Also,itiscommon practice inotherfieldsdealing

228 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
withnegotiation (e.g.gametheory,economy)toincludecollaborativenegotiation (cf.
Lewin et al.,2000).
Asecondfactorinfluencing negotiation isthedistribution ofinformation between DPs. In
someactivities, information maybesymmetrically distributed, i.e. DPshaveroughlythe
samekindofinformation, andalsothesamekindofinformation needs(questions they
wantanswered).Thisisthecasee.g.inthe Coconut(Di Eugenio etal.,1998)dialogues
where DPseachhaveanamountofmoneyandtheyhavetodecidejointlyonanumberof
furniture itemstopurchase. Inotheractivities, suchasatravelagency,theinformation
andinformation needsofthe DPsisasymmetrically distributed. Thecustomer hasaccess
toinformation aboutherdestination, approximatetimeoftraveletc.,andwantstoknow
e.g.exactflighttimesandprices. Thetravelagenthasaccesstoadatabase offlight
information, butneedstoknowwhenthecustomer wantstoleave,whereshewantsto
travel,etc.
Athirdvariableiswhether DPsmustcommitjointly(asine.g.the Coconutdialogues)
orone DPcanmakethecommitmen tbyherself(ase.g.inflightbooking).Inthelatter
case,theacceptance ofoneofthealternativescanbemodelledasananswertoan IUN
bythe DPresponsibleforthecommitmen t,without theneedforanexplicitagreemen t
fromtheother DP. Intheformercase,asimilaranalysis ispossible,buthereitismore
likelythatanexplicitexpression ofagreemen tisneededfromboth DPs. Thisvariable
mayperhapsbereferredtoas\distribution ofdecision rights".Insomedialogues (such
asticketbooking)one DPhasthedecision rightsforallnegotiable issues;inthiscase
thereisnoneedforexplicitly representingdecision rights. However,ifdecision rightsare
distributed differentlyfordifferentissues,anexplicitrepresentationofrightsisneeded.
Ticketbookingdialogue, anddialogue inotherdomains withcleardifferences ininformation
anddecision-righ tdistribution betweenroles,hastheadvantageofmakingdialogue move
interpretation easiersincethepresence ofacertainbitsofinformation inanutterance
together withknowledgeabouttheroleofthespeakerandtherole-related information
distribution oftencanbeusedtodetermine dialogue movetype. Forexample, anutterance
containingthephrase\to Paris"spokenbyacustomer inatravelagencyislikelytobe
intendedtoprovideinformation aboutthecustomer's desireddestination.
5.7.3 Issues Under Negotiation (IUN)
Inthissectionwediscussthenotionof Issues Under Negotiation representedbyquestions,
andhowproposalsrelatetosuchissues. Wealsodiscusshowthisapproachdiffersfrom
Sidner's.

5.7. ISSUES UNDER NEGOTIA TION INNEGOTIA TIVE DIALOGUE 229
Negotiable issuesandactivity
Whichissuesarenegotiable dependsontheactivity. Forexample, itisusuallynotthe
casethatthenameofa DPisanegotiable issue;thisiswhyitwouldperhapsseem
counterintuitivetoviewanintroduction(\Hi,mynameis NN")asaproposal(asisdone
in Sidner,1994 b).However,itcannotberuledoutthatthereissomeactivitywhereeven
thismaybecomeamatterofnegotiation. Also,itisusuallypossibleinprinciple tomake
anyissueintoanegotiable issue,e.g.byraisingdoubtsaboutaprevious answer(see
Section 5.8.2).
Alternativ esasanswersto Issues Under Negotiation
Giventhatweanalyze Issues Under Negotiation asquestions, itisnaturaltoanalyzethe
alternativesolutions tothisissueaspotentialanswers. Onthisview,aproposalhasthe
effectofaddinganalternativ eanswertothesetofalternativ eanswerstoan IUN. Fora DP
withdecision rightsoveran IUN,givingananswertothis IUNisequivalenttoaccepting
oneofthepotentialanswersastheactualanswer. Thatis,an IUNisresolvedwhenan
alternativ eanswerisaccepted.
Hereweseehowourconceptofacceptance differsfrom Sidner. Onourviewaproposed
alternativ ecanbeaccepted intwodifferentways:asaproposal,orastheanswertoan IUN.
Accepting aproposalmoveasaddinganalternativ ecorrespondstometa-levelacceptance.
However,accepting analternativ eastheanswertoan IUNisdifferentfromaccepting an
utterance. Giventheoptimistic approachtoacceptance, allproposalswillbeassumed to
beaccepted asproposals;however,ittakesananswer-movetogettheproposedalternativ e
accepted asthesolution toaproblem.
Semantics
Torepresentissuesundernegotiation, wewillusepairsofquestions (usuallywh-questions
butpossiblyalsoy/n-questions) andsetsofproposedanswers. Thisisinfactanalter-
nativerepresentationofalternativ e-questions tothatwhichwehaveusedpreviously .The
additional semanticrepresentationisshownin(5.9).
(5.9)Q²Ans Set:Alt Qif Q:WHQ(or Q:YNQ)and Ans Set:
Set(Short Ans)

230 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
5.7.4 Anexample
Inthe(invented)example in Figure 5.3,thequestion onissuesis?x:desiredflight(x),
i.e.\Whichflightdoestheuserwant?".Theusersupplies information aboutherdesired
destination anddeparture date;thisutterance isinterpreted asasetofanswer-movesby
thesystemsinceitprovidesanswerstoquestions thatthesystemhasaskedorwasgoingto
ask. Asaresponsetothis,thesystemperformsadatabase searchwhichreturnstwoflights
f 1 andf 2 matchingthespecification, andstoresthedatabase resultsin/private/bel.
Thesystemthenproposestheseflightsasanswerstothecurrent IUN. Thesystemalso
supplies someinformation aboutthem. Asaresult,the IUNisnowassociatedwithtwo
alternativ eanswers,f 1 andf 2. Finally,theuserprovidesananswertothecurrent IUN,
therebyaccepting oneofthesealternativesastheflightshewantstotake.
Thisdialogue doesnotincludeanydiscussion orcomparison ofalternatives,butitcould
easilybeextended tocovere.g.thedialogue in(5.8).
5.8 Discussion
5.8.1 Negotiation ininquiry-orienteddialogue
Themodelpresentedhereisnotcommitted totheviewthatnegotiation onlytakesplace
inthecontextofcollaborativeplanning, orevenaction-orienteddialogue. Inthesenseof
negotiativedialogue usedhere,i.e.dialogue involvingseveralalternativesolutions tosome
problem, negotiation mayalsoconcernmattersoffact. Thiscanbeusefule.g.intutorial
dialogue whereatutorasksaquestion, givessomealternativ eanswers,andthestudent's
taskistoreasonaboutthedifferentalternativesanddecideononeofthem. Inthetravel
agencydomain, itisoftennotnecessary toexplicitly represente.g.thatdeciding ona
flightisaprecondition ofageneralplanfortravelling;instead,wecanrepresentitsimply
asafactconcerning whichflighttheuserwantstotake.
Arelatedpointisthatcollaborativeplanning dialogue isnotnecessarily action-oriented
dialogue, sincetheactivityofplanning maybedirected atcomingupwithanabstract plan
regardless ofwhoactually performstheactionsintheplan. Onlywhensome DPbecomes
obligedtocarryoutsomepartoftheplandoesthedialogue becomewhatwerefertoas
anaction-orienteddialogue.

5.8. DISCUSSION 231
A>flights toparis,june 13
answer(desireddestcity(paris))
answer(desireddeptdate(13/5) )
B>OK,there's oneflightleaving at 07:45 andoneat 12:00
propose(f 1)
propose(f 2)
inform(depttime(f 1,07:45) )
inform(depttime(f 2,12:00) )
2
66666666666666666666666666664 private=2
6666664 agenda=hfindout(?x:desiredflight(x))i
plan =hfindout(?x:credit-card-no( x))
update DB(add reservation)i
bel =8
<
:flight(f 1)
depttime(f 1,0745)
...9
=
;3
7777775
shared =2
66666666666666664 com =8
>><
>>:depttime(f 1,0745)
depttime(f 2,1200)
desireddestcity(paris)
desireddeptdate(13/5) :::9
>>=
>>;
issues =h?x:desiredflight(x)²©
f 1,f 2ª
i
actions =hbookticketi
xsqud=hi
lu =2
664 speaker =sys
moves =8
<
:propose(f 1)
propose(f 2)
:::9
=
;3
7753
777777777777777753
77777777777777777777777777775
A>I'lltakethe 07:45 one
answer(desiredflight(X)&depttime(X,07:45))
(aftercontextualinterpretation: answer(desiredflight(f 1)))
2
666666666666666666666666664 private=2
66664 agenda=hfindout(?x:credit-card-no( x))i
plan =hupdate DB(add reservation)i
bel =8
<
:flight(f 1)
depttime(f 1,0745)
...9
=
;3
77775
shared =2
66666666666666664 com =8
>>>><
>>>>:desiredflight(f 1)
depttime(f 1,0745)
depttime(f 2,1200)
desireddestcity(paris)
desireddeptdate(13/5) :::9
>>>>=
>>>>;
issues =hi
actions =hbookticketi
qud =hi
lu =2
4 speaker =sys
moves =½
answer(desiredflight(f 1)
:::¾3
53
777777777777777753
777777777777777777777777775
Figure 5.3:Example dialogue

232 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
5.8.2 Rejection, negotiation anddownshifting
Inthecontextofdiscussing referentidentification ininstructional assemblydialogues,
Cohen(1981)makesananalogy betweenshiftsindialogue strategy andshiftinggears
whendrivingacar. Inadialogue inhighgear,thespeakerintroducesseveralsubgoals
ineachutterance, whereas fewergoalsareintroducedinlow-geardialogue. Thetypeof
subgoals discussed by Cohenaremainlyidentifyingareferent,requests topickupobjects,
andrequesting anassemblyaction. Aslongasthedialogue proceedssmoothlyandthe
hearerisabletocorrectly identifyreferentsandcarryoutactions, thespeakerrequests
assemblyactionsandexpectsthehearertobeabletoidentifyandpickuptheobjects
referredtowithoutexplicitrequests forthis. However,whenthisfailsandthehearerfails
toidentifyareferent,thespeakermayshiftintoalowergear(downshift) andmakeexplicit
requests foridentification ofreferents. Atalaterstage,thespeakermayshifttoahigher
gearandrequestthehearertopickupanobjectandthentoperformanassemblyaction.
Finally,thespeakermayreturntotheinitialgearandonlymakerequests forassembly
actions.
Severinsson (1983)viewstotheprocessofdownshifting asmakinglatentsubgames into
explicitsubgames. Inthecasementionedabove,thegoalsofthelatentsubgames are(1)
togetthehearertoidentifyareferent,and(2)forthehearertopickuptheobjectreferred
to. Inhighgear,thesesubgames arelatentinthesensethattheydonotgiverisetoany
utterances (dialogue moves).Whenthelatentsubgames becomeexplicit, theprocessthat
waspreviously carriedoutsilentlyisinsteadcarriedoutusingutterances.
Thisviewfitswellwiththeconceptoftacitmovesintroducedin Section 4.4.2. Updatesfor
latentreferentidentification andutterance acceptance canberegarded astacitmoves(or
games)correspondingtoexplicitreferentidentification ornegotiation subdialogues, similar
tothewaythatquestion accommodationupdatesaretacitmovescorrespondingtotheask
dialogue moves.
Boththesenotions, shiftinggearsindialogue andlatentsubgames, areusefulforshedding
lightontherelationbetweennegotiativedialogue andutterance acceptance. Firstly,the
notionsofoptimism andpessimism regarding grounding strategies seemintimately related
tothenotionofgears,bothmetaphorically andfactually. Metaphorically ,wemaysaythat
anoptimistic driverwilluseahighergearthanapessimistic one;onlywhensheencounters
abumpyroadwillsheshiftintolowergear(thustakingamorepessimistic approach).
Later,whentheroadbecomessmoother,shemayagainresumeheroptimistic strategy
anduseahighergear. Similarly ,speakerscanbeexpectedtoswitchbetweenhigherand
lowergears,andbetweenoptimistic andpessimistic grounding strategies regarding the
grounding oftheirutterances. Thusweclaimthatthenotionofshiftinggearsisapplicable
notonlytoreferentidentification, butalsotoothergrounding relatedgames,including
utterance acceptance.

5.9. SUMMAR Y 233
In Chapter 3,wetalkedaboutoptimism andpessimism inregardtogrounding onthe
acceptance level;wenowaddthat DPsmayshiftgearsregarding grounding ontheaccep-
tancelevel. Inadialogue inhighgear,thespeakeroptimistically assumes thehearerto
acceptherutterances. However,shouldthespeakerrejectsomeutterance, thedialogue is
downshifted andthelatentuptakesubgame becomesexplicit. Wewouldclaim(contrary
to Sidner)thatitisonlywhenthedialogue isdownshifted inthissensethatmovessuchas
questions andassertions shouldberegarded asproposals. Atthisstage,DPsmayintroduce
alternativestotheproposal,andtheymayarguefororagainstproposals.
Theconceptofdownshiftisrelatedto Ginzburg's casewhereaproposition pisrejected
asafactbut?pisaccepted asaquestion fordiscussion. Thisappearstobeapotential
caseofdownshifting whichcouldbemodelledbyregarding?p²fyes,nogasanissue
undernegotiation. Inaddition, alterations ofpmaybeproposed,roughlycorresponding
to Clark's\cooperativealterations". Itappearsthiscanbemodelledasanissueunder
negotiation ?x.px²fa;b;:::g(wherepxisthepropositionpwithsomeargumen tareplaced
byx,andthusp=px(a)).Thealterations arethenrepresentedasalternativesb;:::toa.
Thus,ifaquestion qhasbeenraisedinadialogue andifananswerarelevanttoqis
rejected(onthegrounding level),qmaybecomenegotiable (dependingontheactivity).If
so,the DPwhorejected amayproposeanalternativ eanswera 0 toq. Itisthenpossible
forthe DPstostarta(probably argumen tative)negotiation regarding whichofaanda 0,
orperhapssomeotheranswer,shouldbeaccepted astheanswertoq. Wethusbelieve
thatdownshifting ofdialogue fromoptimistic acceptance tonegotiation canshedlighton
variousgrounding-related phenomena, e.g.alterations (see Section 3.2.1),andtherelation
betweengrounding andnegotiation.
5.9 Summary
Firstly,weextended theissue-based approachtoaction-orienteddialogue, andimplemen ted
adialogue interfacetoa VCRwheredialogue planswerebasedonanexisting menuin-
terface. Wemodifiedtheinformation statebyaddingafield/shared/a ctions,and
alsoaddedtwonewdialogue movesspecificto AODrequestandconfirm. Wealsoimple-
mentedupdaterulesin IBi Stohandleintegration andselection ofthesemoves,aswellas
interaction withadevice,andalsoprovidedanadditional accommodationruleforactions.
Secondly ,weproposedaviewofnegotiation asdiscussing severalalternativesolutions to
anissueundernegotiation. Onourapproach,anissueundernegotiation isrepresentedas
aquestion, e.g.whatflighttheuserwants. Ingeneral, thismeansviewingproblems as
issuesandsolutions asanswers. Thisapproachhasseveraladvantages. Firstly,itprovides
astraightforwardanintuitivelysoundwayofcapturing theideathatnegotiativedialogue

234 CHAPTER 5. ACTION-ORIENTED AND NEGOTIA TIVE DIALOGUE
involvesseveralalternativesolutions tosomeissueorproblem, andthatproposalsintroduce
suchalternatives. Secondly ,itdistinguishes twotypesofnegotiation (grounding-related
negotiation andnegotiation ofissues)andclarifiestherelationbetweenthem.

