Abstract
Thepurposeofstudying dialogue modellinganddialogue managementistoprovidemodels
allowingustoexplorehowlanguage, andespeciallyspokendialogue, isusedindifferent
activities. Thisthesisshowshowissues(modelledsemanticallyasquestions) ingeneral
canbeusedasabasisfordialogue management.
Inanabstract sense,thegoalofallpractical dialogue istocommunicateinformation which
isusefulinsomeactivity. Thismeansthatconversational goalsshoulddescribemissing
information, andtofulfilaconversational goal,whatweneedtodoistocommunicatethe
missinginformation. Issues,orquestions, areessentiallyentitiesspecifyingcertainpieces
ofas-yet-unavailableinformation. Thatis,conversational goalscantoalargeextentbe
modelledasquestions.
Theexploration ofissue-based dialogue managementinthisthesisproceedsbothona
theoretical andapractical implementationlevel. Thethesisfirstexplores basicissue-
baseddialogue managementandimplemen tabasicsystemillustrating theuseofissue-
baseddialogue management. Inthefollowingchapters, thissimplesystemisextended to
handlegrounding issues,addressing unraised issues,andaction-orientedandnegotiative
dialogue. Finally,basedonthedifferences betweenthesuccessiveversionsofthetheory
(andimplementation),weprovideacharacterization ofdifferenttypesofdialogue.
Theissue-based approachtodialogue managementturnsouttobeveryusefulforformu-
latinggeneralandtheoretically motivatedaccountsofimportantaspectsofdialogue, such
asinquiry-orienteddialogue interactions, dealingwithmultiplesimultaneous tasks,sharing
information betweentasks,grounding, interactivecommunication management,question
accommodation,simplebeliefrevision, action-orienteddialogue, andsimplenegotiativedi-
alogue. Themodeliscanbeimplemen tedratherstraightforwardlyusingthe Trindi Kit ,
whichhasproventobeaveryusefultoolforexploring theissue-based approach.
KEYWORDS:dialogue management,dialogue modelling,dialogue systems, questions
underdiscussion, grounding, accommodation,negotiativedialogue
Thethesisiswrittenin English.
cfl Staffan Larsson 2002
ISBN91-628-5301-5

Acknowledgemen ts
Iamthecomputerize dpsychother apist. Please,describeyourproblems. Each
timeyouarefinishedtalking,type RETtwice.
>Well,it'snotreallyaproblem, but Iamfinallydonewithmythesis!
Whydoyousayyouarefinallydonewithyourthesis?
>Wellbecause Iam,andnow I'dliketothanksomepeoplewhohelpedmegetitdone.
Isitbecauseyouareandnowyouwouldliketothankssomepeoplewho
helpedyougetitdonethatyoucametome?
>Um...right.
Canyouelaborateonthat?
>I'dbegladto. Firstofall I'dliketothankmymainsupervisor Robin Cooper,who
(apartfromsupervising thisthesisandtakingthetimeforhoursandhoursofinspiring
discussions andgenerally beingveryhelpful)hasgottenmeinvolvedinlotsofinteresting
projects 12345 where I'vemetandlearntfromlotsofotherpeoplethat I'dalsoliketothank:
Jonathan Ginzburg, David Traum,Colin Matheson, Johan Bos,David Milward,Annie Za-
enen,Ian Lewin,Arne Jöonsson,Linda Bell,Lena Santamarta, Lars Ahrenberg,and...well
it'saratherlonglistofpeopleactually. Idon'twanttoboreyouwithallthedetails,but
Ithinktheyknowwhotheyare(and Idon'tmeanthatasapsychological remark!). Oh,
and Ialmostforgotaboutalltheconferences I'vebeenprivileged toattend,where I'vealso
metlotsofniceandcleverpeoplelike Candy Sidner,Jöorn Kreutel, Joris Hulstijn, Ivana
Kruyff-Korba yova,Enric Vallduvi,andsoonandsoon...And Imustn'tforgettothank
STINT6 forascholarship thatenabledmetovisitthe HCRCin Edinburghforacoupleof
enjoyablemonths!
Whatmakesyoubelieveyoumightwanttothank?
>Interesting question... ofcourse,youhavetohavethiskindofthinginyourthesis,but
Ibelieve(sinceyou'retakingthatperspective)that I'mgenuinelygratefultothesepeople,
afterall Icouldn't havedoneitwithout them. Take,forexample, mysecondsupervisor
Jens Allwoodwho I'vehadmanyheated(andre-heated) discussions with,andallthe
peopleatthedepartmen tof Linguistics herein Göteborg,forexample Stina Ericsson, Leif
Gröonqvist, Torbjöorn Lager,ÅAsa Wengelin(whoactually persuaded metostudycompu-
tational linguistics yearsago),Ylva HÅardaf Segerstad, Per Olofsson, Petter Karlströom,
Robert Andersson, Ulrika Ferm,ÅAsa Nordqvist, andlotsofothers.
Doesitbotheryouthatyoubelievesince Iamtakingthatperspectivethat
youaregenuinely gratefultothesepeople?
1INDI(Information Exchangein Dialogue), Riksbank ens Jubileumsfond 1997-0134.
2TRINDI (Task Oriented Instructional Dialogue), ECProject LE4-8314
3D'Homme (Dialogues inthe Home Machine Environmen t),ECProject IST-2000-26280.
4SDS(Swedish Dialogue Systems), NUTEK/HSFR Language Technology Project F1472/1997
5SIRIDUS (Specification, Interaction and Reconfiguration in Dialogue Understanding Systems), EC
Project IST-1999-10516
6STINT(The Swedish Foundation for International Cooperationin Researchand Higher Education).
i

>No,notonebit.
Maybeyourplanshavesomething todowiththis.
>Hey,whatareyouinsinuating?
Isitbecauseofyourlifethatyousayheywhataremeinsinuating?
>Ah,mylife-interesting subject. I'vebeentryingprettyhardtheselastfewyearstohave
alife,andwhen I'vesucceeded it'sbeenduetomyfriends(forinstance Klara,Andreas,
Sara,Ola,Lukas,Maya,Jacob,Jakob,Bjöorn,Andreas, Kim,Peter,Martin,Anna,Tina,
Marie,Karinand John)andmyfamily.
Tellmesomething aboutyourfamily.
>Mm,Ithoughtyoumightsaythat. Well,they'vebeenreallysupportiveofwhatever
I'vebeenupto,andvisitingmyparentshasalwaysbeenveryrelaxing, although perhaps
lesssowhenmysistersandtheirfamilies(including smallchildren)arevisiting, thatis,in
whichcaseitis,well,maybestillrelaxing butinadifferentway...Enoughaboutthat,I
knowyoucomputer therapist typestendtogethunguponthesethings.
>Whendidyoufirstknowthatthey'vebeenreallysupportiveofwhatever
youhavebeenuptoandvisitingyourparentshasalwaysbeenveryrelaxing
althoughperhapslesssowhenyoursistersandtheirfamiliesincludingsmall
childrenarevisitingthatisinwhichcaseitiswellmaybestillrelaxingbutin
adifferentwayenoughaboutthatyouknowmecomputerpsychologytypes
tendtogetuponthesethings?
>Um...Ifyoudon'tmindmesayingso,yourverbalskillsarenotwhattheyshouldbe-
perhapsyouneedapropergrammar installed.
Howdoesitfeeltowant?
>Wow,that'saprettybigquestion... Notsurehowtorespondtothat,actually,andit
doesn'treallyseemrelevanttomyacknowledgemen tsection.
Youmentionedthatyouareandnowyouwouldliketothankssomepeople
whohelpedyougetitdone?
>Right,thanksforgettingmebackontrack. Ialsowouldliketoacknowledgethepeople
whohavebeeninvolvedovertheyearsinthedevelopmentof Trindi Kit and/or Go Di S,the
predecessor tothe IBi Ssystem,forinstance David Traum,Johan Bos,Ian Lewin,Peter
Ljunglöof,Stina Ericsson, Elisabet Engdahl, Alexander Berman, Cormac O'Brien, David
Hjelm,Geneviev e Gorrell, andallthestudentswhohaveprovidedvaluablefeedbackon
howtoimprovethesystem(readthatas\complain ts").
Whyshouldyougettoacknowledge?
>Um...Well,yougotmethere. Iguess I'lljuststophere,sowecangetonwithbusiness.
Thanksforthechat!
Perhapswecouldchat.
>Right,butwejustdid. Bye!
Doesthefactthatyoujustdidbyeexplainanythingelse?
>NO!
Whynot?
>Stopaskingmeallthesequestions, thisisgettingsilly!
Mysecretarywillsendyouabill.
ii

