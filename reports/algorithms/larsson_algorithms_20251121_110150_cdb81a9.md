# Algorithms Extracted from Larsson_Tesis.pdf

Total algorithms found: 198

---

## Algorithm 1: Procedure/Rule in 1.1 The aim of this study

**Section:** 1.1 The aim of this study
**Page:** 23

**Algorithm:**

```
Chapter 1
Introduction
1.1 The aim of this study
The primary aim of this study is to explore issue-based dialogue management, an ap-
proach to dialogue management and dialogue modelling which regards issues, modelled
semantically as questions, as a primary organizing and motivating force in dialogue.
This exploration will proceed both on a theoretical and a practical implementation level.
Starting from a basic account of issue-based dialogue management, we gradually extend
the coverage of the theory and the implementation to more complex types of dialogue. A
secondary aim is to exploit the difierences between the successive versions of the theory
(and implementation) to provide a formal characterization of difierent types of dialogue.
We will only be concerned with what Allen et al. (2001) refer to as practical dialogue, i.e.
dialogue focused on accomplishing a concrete task.
Our general strategy for reaching these goals will be to try as far as possible to \keep things
simple"; that is, for each type of dialogue we try to give an account that handles exactly
those phenomena appearing in that type of dialogue. However, we also want to keep things
fairly general, to enable reuse of components of a simple version in a more complex version
of the theory and implementation.
In this chapter, we will flrst motivate exploring the issue-based approach to dialogue man-
agement. We will then give an outline of this thesis and give brief descriptions of the
implementations. Finally, we will introduce the TrindiKit, a toolkit for building and
experimenting with dialogue systems, which has been used for the implementations.
1
```

---

## Algorithm 2: Procedure/Rule in 2.1. INTRODUCTION 17

**Section:** 2.1. INTRODUCTION 17
**Page:** 39

**Algorithm:**

```
2.1. INTRODUCTION 17
It is useful, however, to have a concept of inquiry-oriented dialogue which does not include
giving orders or instructions to perform actions changing the state of the world (rather
than just changing the information states of DPs), or indeed any utterance resulting in a
DP having an obligation or commitment to perform some action. However, it must also
be remembered that utterances are also actions, and DPs can be obliged to perform them;
for example, a question can be said to introduce an obligation on the hearer to respond to
that question. So we still want to allow utterances which result in obligations to perform
communicative actions that are part of the dialogue2. Of course, the same applies to these
obliged actions themselves. In efiect, this deflnitions serves to exclude orders, instructions
etc. from information-oriented dialogue.
Withthismotivation, thetermInquiryOrientedDialogue, orIOD,willhenceforthbetaken
to refer to any dialogue whose sole purpose is the transference of information, and which
does not involve any DP assuming (or trying to make another DP assume) commitments
or obligations concerning any non-communicative actions outside the dialogue.
Hulstijn (2000) deflnes the dialogue game of inquiry in the following way:
The dialogue game of inquiry is deflned as the exchange of information between
two participants: an inquirer and an expert (...). The inquirer has a certain
information need. Her goal in the game is to ask questions in the domain in
order to satisfy her information need. The expert has access to a database
about the domain. His goal is to answer questions. (...) [T]he expert may ask
questions too. (Hulstijn, 2000 p. 66)
Here, tworolesareintroduced: inquirerandexpert. Thisconceptisparticularlywellsuited
for dialogue systems for database search, which happens to be the type of dialogue we will
initially be exploring. In a dialogue system setting, the system is typically the expert and
the user is the inquirer.
Initially, we will be dealing only with a subtype of inquiry-oriented dialogue, namely non-
negotiative IOD. Negotiative dialogue here refers to, roughly, dialogue where DPs can
discuss and compare several difierent alternative solutions to a problem. Non-negotiative
dialogue is su–cient when database searches can be expected to return only a single result
(rather than e.g. a table). Obviously this is insu–cient for dealing with many information-
seeking domains and applications. In Chapter 4 we will be able to handle semi-negotiative
dialogue, where several alternatives can be introduced in the dialogue; however, the intro-
duction of a new alternative will always remove the previous alternative which thus cannot
be returned to unless reintroduced \from scratch".
2The reservation that the obliged actions are part of the dialogue is meant to exclude utterances which
impose an obligation to perform a communicative action directed at some agent who is not a DP, e.g.
\Tell Martha to go home".
```

---

## Algorithm 3: Procedure/Rule in 2.3.2 Simplifying assumptions

**Section:** 2.3.2 Simplifying assumptions
**Page:** 44

**Algorithm:**

```
22 CHAPTER 2. BASIC ISSUE-BASED DIALOGUE MANAGEMENT
(2.2) repeat h select
if not is empty($next moves)
then h generate
output
update i
test( $program state == run )
input
interpret
update i
The IBiS system uses modules included in the TrindiKit package for input, interpre-
tation, generation and output. The interpretation and generation modules are described
in Section A.7. The update and selection modules are described in Sections 2.8 and 2.9,
respectively.
Turntaking is regulated by the following principle: if select flnds a move to perform, the
system will generate a string and output it to the user. The TIS is then updated, and
provided the program state variable is still set to run, the system reads input from the
user, interprets it, and again updates the TIS. This means that if select flnds no move to
perform, the turn will be handed over to the user.
2.3.2 Simplifying assumptions
For our initial system, we will make some simplifying assumptions, which in efiect will pro-
vide us with a system that only handles a limited range of dialogue phenomena. Later, we
will remove some of these limitations and extend the implementation correspondingly. The
simplifying assumptions will make it easier to formulate a simple basic set of information
state update rules.
† All utterances are understood and accepted. This assumption will be removed in
Section 3.
† Utterance interpretation does not involve the identiflcation of referents, and referents
are not represented in the information state. This assumption will be removed in
Chapter 5.
† Complex semantic representation is not needed for simple kinds of dialogue. This
assumption will not be removed; however, it is clear that a more complex semantic
analysis involving e.g. quantiflcation, temporality, and modality would be required
```

---

## Algorithm 4: Procedure/Rule in 2.4.3 Questions

**Section:** 2.4.3 Questions
**Page:** 48

**Algorithm:**

```
26 CHAPTER 2. BASIC ISSUE-BASED DIALOGUE MANAGEMENT
want to go to Paris" could normally be represented semantically as e.g. want(user, go-
to(user, paris) ) or want(u, go-to(u,p)) & city(p) & name(p, paris) & user(u).
We will be using a reduced semantic representation with a coarser, domain-dependent
level of granularity; for example, the above example will be rendered as dest-city(paris).
This reduced representation is in part a consequence of the use of keyword-spotting in
interpreting utterances, but can arguably also be regarded as a re(cid:176)ection of the level of
semantic granularity inherent in the underlying domain task. As an example of the latter,
in a travel agency domain there is no point in representing the fact that it is the user (or
customer) rather than the system (or clerk) who is going to Paris; it is implicitly assumed
that this is always the case.
As a consequence of using reduced semantics, it will be useful to allow 0-ary predicates,
e.g. return, meaning \the user wants a return ticket". 0-ary predicates can of course
appear in non-reduced semantics as well, e.g. in the representation of \It’s raining" in a
non-temporal logic as e.g. rain. (Of course, non-temporal logic can also be argued to be
a kind of reduced semantic representation.)
The advantage of this semantic representation is that the speciflcation of domain-speciflc
semantics becomes simpler, and that unnecessary \semantic clutter" is avoided. On the
other hand, it severely restricts the possibility of providing generic semantic analyses that
can be extended to other domains.
If the database search for an answer to a question q fails the resulting proposition is fail(q).
We have chosen this representation because it provides a concise way of encoding a failure
to flnd an answer to q in the database.
2.4.3 Questions
Threetypesofquestionsarehandledby IBiS:y/n-questions, wh-questions, andalternative
questions. Here we describe how these are represented on a semantic level; the syntactic
realization is deflned in the lexicon.
† y/n-questionsarepropositionsprecededbyaquestionmark,e.g. ?dest-city(london)
(\Do you want to go to London?")
† wh-questions are lambda-abstracts of propositions, with the lambda replaced by a
question mark, e.g. ?x.dest-city(x) (\Where do you want to go?")
† alternative questions are sets of y/n-questions, e.g. f?dest-city(london), ?dest-
city(paris)g (\Do you want to go to London or do you want to go to Paris?")
```

---

## Algorithm 5: Procedure/Rule in 2.6.1 Domain plans and dialogue plans

**Section:** 2.6.1 Domain plans and dialogue plans
**Page:** 55

**Algorithm:**

```
2.6. REPRESENTING DIALOGUE PLANS IN IBIS1 33
\Give me price information!", \I want to know about price.", \I want price information."
and \price information" are all interpreted ask ask(?x.price(x)). For a description of how
this interpretation works, see Section A.7.3.
Ofcourse, partofthereasonthatthisapproachworksisthatweareoperatinginsimpledo-
mains and activities which can be fairly well covered by a keyword-spotting interpretation
module. However, the approach could well be improved by adding a more complex kind of
grammar (e.g. HPSG), thus enabling the system to take syntactic features of utterances
into account, while still using an activity-based classiflcation. Whether activity-dependent
classiflcation of moves is a viable alternative to intention- and structure-based classiflcation
in general is an issue we will return to in Chapter 6. One hypothesis worth exploring is to
what extent traditional speech acts can be replaced by a combination of activity-related
dialogue moves (to update IS and decide on future moves) and syntactic sentence modes
(to decide on the surface form of future moves).
2.6 Representing dialogue plans in IBiS1
In this section we introduce the concept of dialogue plans, and show how these are rep-
resented in IBiS1. In later chapters, the plan formalism will be extended to handle more
powerful constructions.
2.6.1 Domain plans and dialogue plans
In our implementation, the domain knowledge resource contains, among other things, a set
of dialogue plans which contain information about what the system should do in order to
achieve its goals.
In plan-based dialogue management (e.g. Allen and Perrault, 1980), it has been assumed
thatgeneralplannersandplanrecognizersshouldbeusedtoproducecooperativebehaviour
from dialogue systems. On this account, the system is assumed to have access to a library
of domain plans, and by recognizing the domain plan of the user, the system can produce
cooperative behaviour such as supplying information which the user might need to execute
her plan. On this approach, plans for carrying out dialogues are not represented explicitly;
instead, the system is continually inspecting (and perhaps modifying) domain plans to
determine what dialogue moves need to be performed.
Our approach is instead to directly represent ready-made plans for engaging in coopera-
tive dialogue and producing cooperative behaviour (such as answering questions) which
```

---

## Algorithm 6: rule 2 .1) rule: getLatestMove

**Section:** 3. B provides a response u that addresses q
**Page:** 63

**Context Before:**
> 2.8. IBIS1 UPDATE MODULE 41
(...

**Algorithm:**

```
rule 2.1) rule: getLatestMove
class: grounding
$latest moves=Moves
pre:
$latest speaker=DP
(
/shared/lu/moves := Moves
eff:
/shared/lu/speaker := DP
(
This rule copies the information about the latest utterance from the latest moves and
latest speaker to the /shared/lu fleld. The flrst condition picks out the (singleton)
set of moves stored by the interpretation module, and the second condition gets the value
of the latest speaker variable. The updates set the values of the two subflelds of the
/shared/lu record correspondingly.
```

**Context After:**
> 2.8.2 Raising issues: the ask move
Before we explain the rules used by IBiS1 for dealing with the ask move, we will review
Ginzburg’s protocols for querying and assertion on which the rules are based....

---

## Algorithm 7: rule 2 .2) or the user (rule 2.3.)

**Section:** 2. Conveys a question on which q depends
**Page:** 65

**Context Before:**
> c utterance is one that either
1. Conveys information ABOUT q or
2. Conveys a question on which q depends
WehavenotimplementedthisrelationdirectlyinIBiS,howeverbothrelevance(ourversion
of ’ABOUT’) and...

**Algorithm:**

```
rule 2.2) or the user (rule 2.3.)
(rule 2.2) rule: integrateSysAsk
class: integrate
$/shared/lu/speaker==sys
pre:
in($/shared/lu/moves, ask(Q))
(
eff: push(/shared/qud, Q)
n
The conditions of the rule in (2.14) checks that the latest speaker is sys and that the latest
move was an ask move with content Q. The update pushes Q on /shared/qud.
```

---

## Algorithm 8: rule 2 .3.)

**Section:** 2. Conveys a question on which q depends
**Page:** 65

**Context Before:**
> either
1. Conveys information ABOUT q or
2. Conveys a question on which q depends
WehavenotimplementedthisrelationdirectlyinIBiS,howeverbothrelevance(ourversion
of ’ABOUT’) and dependence are deflned....

**Algorithm:**

```
rule 2.3.)
(rule 2.2) rule: integrateSysAsk
class: integrate
$/shared/lu/speaker==sys
pre:
in($/shared/lu/moves, ask(Q))
(
eff: push(/shared/qud, Q)
n
The conditions of the rule in (2.14) checks that the latest speaker is sys and that the latest
move was an ask move with content Q. The update pushes Q on /shared/qud.
```

---

## Algorithm 9: rule 2 .2) rule: integrateSysAsk

**Section:** 2. Conveys a question on which q depends
**Page:** 65

**Context Before:**
> onveys information ABOUT q or
2. Conveys a question on which q depends
WehavenotimplementedthisrelationdirectlyinIBiS,howeverbothrelevance(ourversion
of ’ABOUT’) and dependence are deflned.
Integratin...

**Algorithm:**

```
rule 2.2) rule: integrateSysAsk
class: integrate
$/shared/lu/speaker==sys
pre:
in($/shared/lu/moves, ask(Q))
(
eff: push(/shared/qud, Q)
n
The conditions of the rule in (2.14) checks that the latest speaker is sys and that the latest
move was an ask move with content Q. The update pushes Q on /shared/qud.
```

---

## Algorithm 10: rule 2 .3) rule: integrateUsrAsk

**Section:** 2. Conveys a question on which q depends
**Page:** 66

**Context Before:**
> 44 CHAPTER 2. BASIC ISSUE-BASED DIALOGUE MANAGEMENT
(...

**Algorithm:**

```
rule 2.3) rule: integrateUsrAsk
class: integrate
$/shared/lu/speaker==usr
pre:
in($/shared/lu/moves, ask(Q))
(
push(/shared/qud, Q)
eff:
push(/private/agenda, respond(Q))
(
The update rule in (rule 2.3) for integrating user queries is slightly difierent: if the user
```

**Context After:**
> asks a question q, the system will also push respond(q) on the agenda. This does not
happen if the system asks the question, since it is the user who is expected to answer this
question.
Eventually, t...

---

## Algorithm 11: rule 2 .3) for integrating user queries is slightly difierent: if the user

**Section:** 2. Conveys a question on which q depends
**Page:** 66

**Context Before:**
> 44 CHAPTER 2. BASIC ISSUE-BASED DIALOGUE MANAGEMENT
(rule 2.3) rule: integrateUsrAsk
class: integrate
$/shared/lu/speaker==usr
pre:
in($/shared/lu/moves, ask(Q))
(
push(/shared/qud, Q)
eff:
push(/priv...

**Algorithm:**

```
rule 2.3) for integrating user queries is slightly difierent: if the user
asks a question q, the system will also push respond(q) on the agenda. This does not
happen if the system asks the question, since it is the user who is expected to answer this
question.
Eventually, the flndPlan (see Section 2.8.6) rule will load the appropriate plan for dealing
with Q. This assumes that for any user question that the system is able to interpret, there
is a plan for dealing with that question. If this were not the case, IBiS would somehow
have to reject Q; in Chapter 3 we will discuss this further.
Reasons for answering questions
The solution of pushing respond(Q) on the agenda when integrating a user ask(Q) move is
nottheonlypossibleoption. Itcanbeseenasasimple\intention-based"strategyinvolving
minimal reasoning; \If the user asked q, I’m going to respond to q". Alternatively, one
could opt for a more indirect link between the user asking a question and the system
intending to respond to it.
One such indirect approach is to not push respond(Q) on the agenda when integrating a
user ask(Q) move, but only push Q on QUD7. A separate rule would then push respond(Q)
on the agenda given that Q is on QUD and the system has a plan for responding to Q.
This reasoning behind this rule could be paraphrased roughly as \If q is under discussion
and I know a way of dealing with q, I should try to respond to q". On this approach,
it would be assumed that DPs do not care about who asked a question; they will simply
attempt to answer any question that is under discussion, regardless of who raised it.
A second indirect approach is to assume that asking a question introduces obligations on
the addressee. This \obligation-based approach" would require representing obligations as
part of the shared information. For an obligation-based account of dialogue, see Traum
(1996); for a comparison of QUD-based and obligation-based approaches, see Kreutel and
7If the system can understand user questions which it cannot respond to (which IBiS1 does not), the
integration rulefor userask moves would still needto checkthat thereisa plan fordealing with Q, orelse
reject Q; issue rejection is discussed further in Chapter 3.
```

---

## Algorithm 12: rule 2 .4) rule: integrateAnswer

**Section:** 2.8.4 Downdating QUD
**Page:** 69

**Context Before:**
> 2.8. IBIS1 UPDATE MODULE 47
(...

**Algorithm:**

```
rule 2.4) rule: integrateAnswer
class: integrate
in($/shared/lu/moves, answer(A))
pre: fst($/shared/qud, Q)
8
>< $domain :: relevant(A, Q)
! $domain :: combine(Q, A, P)
eff:
>:
add(/shared/com, P)
(
The flrst condition checks that the latest move was an answer move with content A, and
the next two conditions check that A is relevant to some question Q topmost on QUD.
The flrst updates combines Q and A to form a proposition P according to the deflnition
in Section 2.4.7. Finally, P is added to the shared commitments.
```

**Context After:**
> 2.8.4 Downdating QUD
QUD downdating principle
Ginzburg’s \QUD downdating principle" goes as follows:
Assume q is currently maximal in A’s QUD, and that there exists a p in A’s
FACTS such that p is goa...

---

## Algorithm 13: rule 2 .5) rule: downdateQUD

**Section:** 2.8.5 Integrating greet and quit moves
**Page:** 70

**Context Before:**
> 48 CHAPTER 2. BASIC ISSUE-BASED DIALOGUE MANAGEMENT
(...

**Algorithm:**

```
rule 2.5) rule: downdateQUD
class: downdate qud
fst($/shared/qud, Q)
pre: in($/shared/com, P)
8
>< $domain :: resolves(P, Q)
eff: >: pop(/shared/qud)
n
The paraphrase of this rule is straightforward and is left as an exercise to the reader.
This rule is perhaps ine–cient in the sense that it may require checking all propositions in
/shared/com every time the update algorithm is executed. However, in the systems we
are concerned with the number of propositions is not very high, and in addition we favour
clarity and simplicity in the implementation over e–ciency.
```

**Context After:**
> 2.8.5 Integrating greet and quit moves
InIBiS1greetingshavenoefiectontheinformationstate. Theruleforintegratinggreetings
is shown in (rule 2.6).
(rule 2.6) rule: integrateGreet
class: integrate
pre: i...

---

## Algorithm 14: rule 2 .6).

**Section:** 2.8.5 Integrating greet and quit moves
**Page:** 70

**Context Before:**
> is left as an exercise to the reader.
This rule is perhaps ine–cient in the sense that it may require checking all propositions in
/shared/com every time the update algorithm is executed. However, in ...

**Algorithm:**

```
rule 2.6).
(rule 2.6) rule: integrateGreet
class: integrate
pre: in($/shared/lu/moves, greet)
eff: fn
The update rules for integrating quit moves performed by the user or system are shown in
(rule 2.7) and (rule 2.8,) respectively.
(rule 2.7) rule: integrateUsrQuit
class: integrate
$/shared/lu/speaker==usr
pre:
in($/shared/lu/moves, quit)
(
eff: push(/private/agenda, quit)
n
If the quit move is performed by the user, the efiect is that the system puts quit on the
agenda so that it gets to say \Goodbye" to the user before the dialogue ends.
```

---

## Algorithm 15: rule 2 .6) rule: integrateGreet

**Section:** 2.8.5 Integrating greet and quit moves
**Page:** 70

**Context Before:**
> an exercise to the reader.
This rule is perhaps ine–cient in the sense that it may require checking all propositions in
/shared/com every time the update algorithm is executed. However, in the systems...

**Algorithm:**

```
rule 2.6) rule: integrateGreet
class: integrate
pre: in($/shared/lu/moves, greet)
eff: fn
The update rules for integrating quit moves performed by the user or system are shown in
(rule 2.7) and (rule 2.8,) respectively.
(rule 2.7) rule: integrateUsrQuit
class: integrate
$/shared/lu/speaker==usr
pre:
in($/shared/lu/moves, quit)
(
eff: push(/private/agenda, quit)
n
If the quit move is performed by the user, the efiect is that the system puts quit on the
agenda so that it gets to say \Goodbye" to the user before the dialogue ends.
```

---

## Algorithm 16: rule 2 .7) and (rule 2.8,) respectively.

**Section:** 2.8.5 Integrating greet and quit moves
**Page:** 70

**Context Before:**
> ever, in the systems we
are concerned with the number of propositions is not very high, and in addition we favour
clarity and simplicity in the implementation over e–ciency.
2.8.5 Integrating greet an...

**Algorithm:**

```
rule 2.7) and (rule 2.8,) respectively.
(rule 2.7) rule: integrateUsrQuit
class: integrate
$/shared/lu/speaker==usr
pre:
in($/shared/lu/moves, quit)
(
eff: push(/private/agenda, quit)
n
If the quit move is performed by the user, the efiect is that the system puts quit on the
agenda so that it gets to say \Goodbye" to the user before the dialogue ends.
```

---

## Algorithm 17: rule 2 .8,) respectively.

**Section:** 2.8.5 Integrating greet and quit moves
**Page:** 70

**Context Before:**
> stems we
are concerned with the number of propositions is not very high, and in addition we favour
clarity and simplicity in the implementation over e–ciency.
2.8.5 Integrating greet and quit moves
In...

**Algorithm:**

```
rule 2.8,) respectively.
(rule 2.7) rule: integrateUsrQuit
class: integrate
$/shared/lu/speaker==usr
pre:
in($/shared/lu/moves, quit)
(
eff: push(/private/agenda, quit)
n
If the quit move is performed by the user, the efiect is that the system puts quit on the
agenda so that it gets to say \Goodbye" to the user before the dialogue ends.
```

---

## Algorithm 18: rule 2 .7) rule: integrateUsrQuit

**Section:** 2.8.5 Integrating greet and quit moves
**Page:** 70

**Context Before:**
> h the number of propositions is not very high, and in addition we favour
clarity and simplicity in the implementation over e–ciency.
2.8.5 Integrating greet and quit moves
InIBiS1greetingshavenoefiect...

**Algorithm:**

```
rule 2.7) rule: integrateUsrQuit
class: integrate
$/shared/lu/speaker==usr
pre:
in($/shared/lu/moves, quit)
(
eff: push(/private/agenda, quit)
n
If the quit move is performed by the user, the efiect is that the system puts quit on the
agenda so that it gets to say \Goodbye" to the user before the dialogue ends.
```

---

## Algorithm 19: rule 2 .8) rule: integrateSysQuit

**Section:** 2.8.6 Managing the plan
**Page:** 71

**Context Before:**
> 2.8. IBIS1 UPDATE MODULE 49
(...

**Algorithm:**

```
rule 2.8) rule: integrateSysQuit
class: integrate
$/shared/lu/speaker==sys
pre:
in($/shared/lu/moves, quit)
(
eff: program state := quit
n
Integrating a quit move performed by the system causes the program state variable to
be set to quit. This will eventually cause the program to halt.
The greet move does not have any efiect on the information state, and thus no update rule
is needed to integrate it.
```

**Context After:**
> 2.8.6 Managing the plan
The dialogue plans are interpreted by a class of update rules called exec plan. When a
plan has been entered into the /private/plan fleld, it is processed incrementally by the
...

---

## Algorithm 20: rule 2 .9) to trigger and load a plan for dealing with Q.

**Section:** 2.8.6 Managing the plan
**Page:** 71

**Context Before:**
> ect on the information state, and thus no update rule
is needed to integrate it.
2.8.6 Managing the plan
The dialogue plans are interpreted by a class of update rules called exec plan. When a
plan has...

**Algorithm:**

```
rule 2.9) to trigger and load a plan for dealing with Q.
(rule 2.9) rule: flndPlan
class: flnd plan
fst($/private/agenda, respond(Q))
pre: $domain :: plan(Q, Plan)
8
>< not in($/private/bel, P) and $domain :: resolves(P, Q)
pop(/private/agenda)
eff:
>:
set(/private/plan, Plan)
(
The flrst two conditions check that there is an action respond(Q) on the agenda and that
the system has a plan for dealing with Q. The third condition checks that the system does
not already know an answer to Q (if it does, the system should instead respond to Q). If
these conditions hold, the updates pop respond(Q) ofi the agenda and load the plan.
```

---

## Algorithm 21: rule 2 .9) rule: flndPlan

**Section:** 2.8.6 Managing the plan
**Page:** 71

**Context Before:**
> eeded to integrate it.
2.8.6 Managing the plan
The dialogue plans are interpreted by a class of update rules called exec plan. When a
plan has been entered into the /private/plan fleld, it is processe...

**Algorithm:**

```
rule 2.9) rule: flndPlan
class: flnd plan
fst($/private/agenda, respond(Q))
pre: $domain :: plan(Q, Plan)
8
>< not in($/private/bel, P) and $domain :: resolves(P, Q)
pop(/private/agenda)
eff:
>:
set(/private/plan, Plan)
(
The flrst two conditions check that there is an action respond(Q) on the agenda and that
the system has a plan for dealing with Q. The third condition checks that the system does
not already know an answer to Q (if it does, the system should instead respond to Q). If
these conditions hold, the updates pop respond(Q) ofi the agenda and load the plan.
```

---

## Algorithm 22: rule 2 .10).

**Section:** 2.8.6 Managing the plan
**Page:** 72

**Context Before:**
> BASED DIALOGUE MANAGEMENT
Executing the plan
Ginzburg provides a dialogue-level appropriateness condition for querying:
A question q can be successfully posed by A only if there does not exist a fact ...

**Algorithm:**

```
rule 2.10).
(rule 2.10) rule: removeFindout
class: exec plan
fst($/private/plan, flndout(Q))
pre: in($/shared/com, P)
8
>< $domain :: resolves(P, Q)
eff: >: pop(/private/plan)
n
This rule removes a flndout(Q) action from the plan in case there is a resolving proposition
P in /shared/com.
If there is a consultDB action topmost on the plan, (rule 2.11) will trigger a database
```

**Context After:**
> search .
(rule 2.11) rule: exec consultDB
class: exec plan
pre: fst($/private/plan, consultDB(Q))
n ! $/shared/com=B
! $database :: consultDB(Q, B, C)
eff: 8
>>>< add(/private/bel, C)
pop(/private/pla...

---

## Algorithm 23: rule 2 .10) rule: removeFindout

**Section:** 2.8.6 Managing the plan
**Page:** 72

**Context Before:**
> E MANAGEMENT
Executing the plan
Ginzburg provides a dialogue-level appropriateness condition for querying:
A question q can be successfully posed by A only if there does not exist a fact ¿
such that ¿...

**Algorithm:**

```
rule 2.10) rule: removeFindout
class: exec plan
fst($/private/plan, flndout(Q))
pre: in($/shared/com, P)
8
>< $domain :: resolves(P, Q)
eff: >: pop(/private/plan)
n
This rule removes a flndout(Q) action from the plan in case there is a resolving proposition
P in /shared/com.
If there is a consultDB action topmost on the plan, (rule 2.11) will trigger a database
```

**Context After:**
> search .
(rule 2.11) rule: exec consultDB
class: exec plan
pre: fst($/private/plan, consultDB(Q))
n ! $/shared/com=B
! $database :: consultDB(Q, B, C)
eff: 8
>>>< add(/private/bel, C)
pop(/private/pla...

---

## Algorithm 24: rule 2 .11) will trigger a database

**Section:** 2.8.6 Managing the plan
**Page:** 72

**Context Before:**
> answer is already
shared. On an individual level, each DP should make sure to not ask such questions. In
IBiS1, this will be guaranteed by the removeFindout (rule 2.10).
(rule 2.10) rule: removeFindou...

**Algorithm:**

```
rule 2.11) will trigger a database
search .
(rule 2.11) rule: exec consultDB
class: exec plan
pre: fst($/private/plan, consultDB(Q))
n ! $/shared/com=B
! $database :: consultDB(Q, B, C)
eff: 8
>>>< add(/private/bel, C)
pop(/private/plan)
>>>:
This rule takes all the propositions in /shared/com and given this looks up the answer
to q in the database. The resulting proposition is stored in /private/bel.
```

---

## Algorithm 25: rule 2 .11) rule: exec consultDB

**Section:** 2.8.6 Managing the plan
**Page:** 72

**Context Before:**
> vel, each DP should make sure to not ask such questions. In
IBiS1, this will be guaranteed by the removeFindout (rule 2.10).
(rule 2.10) rule: removeFindout
class: exec plan
fst($/private/plan, flndou...

**Algorithm:**

```
rule 2.11) rule: exec consultDB
class: exec plan
pre: fst($/private/plan, consultDB(Q))
n ! $/shared/com=B
! $database :: consultDB(Q, B, C)
eff: 8
>>>< add(/private/bel, C)
pop(/private/plan)
>>>:
This rule takes all the propositions in /shared/com and given this looks up the answer
to q in the database. The resulting proposition is stored in /private/bel.
```

---

## Algorithm 26: rule 2 .12).

**Section:** 2.9.1 Selecting an action from the plan
**Page:** 73

**Context Before:**
> an be executed.
2.9 IBiS1 selection module
The task of the selection module in IBiS1 is to determine the next move to be performed
by the system. In IBiS1, this is a fairly trivial task, involving two...

**Algorithm:**

```
rule 2.12).
(rule 2.12) rule: selectFromPlan
class: select action
is empty($/private/agenda)
pre:
fst($/private/plan, Action)
(
eff: push(/private/agenda, Action)
n
```

---

## Algorithm 27: rule 2 .12) rule: selectFromPlan

**Section:** 2.9.1 Selecting an action from the plan
**Page:** 73

**Context Before:**
> d.
2.9 IBiS1 selection module
The task of the selection module in IBiS1 is to determine the next move to be performed
by the system. In IBiS1, this is a fairly trivial task, involving two parts: flrst...

**Algorithm:**

```
rule 2.12) rule: selectFromPlan
class: select action
is empty($/private/agenda)
pre:
fst($/private/plan, Action)
(
eff: push(/private/agenda, Action)
n
```

---

## Algorithm 28: rule 2 .13).

**Section:** 2.9.2 Selecting the ask move
**Page:** 74

**Context Before:**
> ny question q which is part of the plan
1
(by virtue of a flndout action) will be such that it in(cid:176)uences q ; indeed, this is exactly the
1
deflnition of in(cid:176)uences that we assume (see S...

**Algorithm:**

```
rule 2.13).
(rule 2.13) rule: selectAsk
class: select move
fst($/private/agenda, flndout(Q)) or fst($/private/agenda,
pre:
raise(Q))
(
add(next moves, ask(Q))
eff:
if do(fst($/private/plan, raise(A)), pop(/private/plan))
(
```

---

## Algorithm 29: rule 2 .13) rule: selectAsk

**Section:** 2.9.2 Selecting the ask move
**Page:** 74

**Context Before:**
> which is part of the plan
1
(by virtue of a flndout action) will be such that it in(cid:176)uences q ; indeed, this is exactly the
1
deflnition of in(cid:176)uences that we assume (see Section 2.8.2)....

**Algorithm:**

```
rule 2.13) rule: selectAsk
class: select move
fst($/private/agenda, flndout(Q)) or fst($/private/agenda,
pre:
raise(Q))
(
add(next moves, ask(Q))
eff:
if do(fst($/private/plan, raise(A)), pop(/private/plan))
(
```

---

## Algorithm 30: rule 2 .14).

**Section:** 2.9.3 Selecting to respond to a question
**Page:** 75

**Context Before:**
> ed in Section 2.8.4
guarantees that resolved issues are removed from QUD.
We divide the selection of an answer move into two steps: flrst, the selection of a respond
action and second, the selection o...

**Algorithm:**

```
rule 2.14).
(rule 2.14) rule: selectRespond
class: select action
is empty($/private/agenda)
is empty($/private/plan)
8
pre:
>>>>>>>>< f
in
st
(
(
$
$
/
/
p
s
r
h
i
a
v
r
at
ed
e/
/
b
q
e
u
l
d
,
,
P
Q
)
)
not in($/shared/com, P)
eff:
>>>>>>>>:
p
$
u
d
s
o
h(
m
/
a
p
i
r
n
iv
:
a
:
t
re
e
l
/
e
a
va
g
n
e
t
n
(P
da
,
,
Q
r
)
espond(Q))
n
The flrst two conditions check that there is nothing else that currently needs to be done.
The remaining conditions check that some question Q is topmost on QUD, the system
knows a relevant answer P to Q which is not yet shared.
```

---

## Algorithm 31: rule 2 .14) rule: selectRespond

**Section:** 2.9.3 Selecting to respond to a question
**Page:** 75

**Context Before:**
> 2.8.4
guarantees that resolved issues are removed from QUD.
We divide the selection of an answer move into two steps: flrst, the selection of a respond
action and second, the selection of an answer mo...

**Algorithm:**

```
rule 2.14) rule: selectRespond
class: select action
is empty($/private/agenda)
is empty($/private/plan)
8
pre:
>>>>>>>>< f
in
st
(
(
$
$
/
/
p
s
r
h
i
a
v
r
at
ed
e/
/
b
q
e
u
l
d
,
,
P
Q
)
)
not in($/shared/com, P)
eff:
>>>>>>>>:
p
$
u
d
s
o
h(
m
/
a
p
i
r
n
iv
:
a
:
t
re
e
l
/
e
a
va
g
n
e
t
n
(P
da
,
,
Q
r
)
espond(Q))
n
The flrst two conditions check that there is nothing else that currently needs to be done.
The remaining conditions check that some question Q is topmost on QUD, the system
knows a relevant answer P to Q which is not yet shared.
```

---

## Algorithm 32: rule 2 .15) rule: selectAnswer

**Section:** 2.9.4 Selecting the answer move
**Page:** 76

**Context Before:**
> from his QUD as well. This rule
also has the nice (but perhaps not extremely useful) feature that it would cover rhetorical
questions as well as ordinary ones (however, this would require selection ru...

**Algorithm:**

```
rule 2.15) rule: selectAnswer
class: select move
fst($/private/agenda, respond(Q))
in($/private/bel, P)
pre: 8
>>>< not in($/shared/com, P)
$domain :: relevant(”A, Q)
eff:
>>>:
add(next moves, answer(P))
n
Again, it may be argued that it is ine–cient to have to check the same conditions twice in
the case where selectAnswer is preceded by selectRespond. However, as we mentioned
above the respond action may also have been pushed on the agenda when integrating a
user ask move, and in this case the conditions need to be checked.
```

---

## Algorithm 33: Procedure/Rule in 2.11 Sample dialogue with IBiS1

**Section:** 2.11 Sample dialogue with IBiS1
**Page:** 80

**Algorithm:**

```
58 CHAPTER 2. BASIC ISSUE-BASED DIALOGUE MANAGEMENT
2.10.3 Database resource
The database for the travel agency domain contains information about the price of trips,
and information about visa regulations. If there is no database entry matching the infor-
mation specifled in the query q, the database will return a fail(q) message.
2.11 Sample dialogue with IBiS1
In this section we show a sample interaction with IBiS1. For the examples we have used
text-based input and output, but the system can also use speech. In this flrst dialogue we
show some update rules including their efiects, information states, and utterances.
(dialogue 2.2)
selectOther
add(next moves, greet)
'
S> Welcome to the travel agency!
getLatestMove
set(/shared/lu/moves, set([greet]))
set(/shared/lu/speaker, sys)
‰
integrateGreet
agenda = hi
private = plan = hi
2 2 3 3
bel = fg
6 4 com = fg 5 7
6 7
6 qud = hi 7
6 shared = 2 3 7
6 speaker = sys 7
6 lu = 7
6 6 moves = greet 7 7
6 6 • ‚ 7 7
4 4 5 5
' “
latest speaker = sys
latest moves = greet
2 3
next moves = fg
' “
6 program state = run 7
6 7
6 lexicon = lexicon travel english 7
6 7
6 domain = domain travel 7
6 7
6 database = database travel 7
6 7
4 5
U> price information please
```

---

## Algorithm 34: rule 2 .16) would need to

**Section:** 2.12. DISCUSSION 63
**Page:** 85

**Context Before:**
> ), the system will proceed to ask the alt-question. However, if the user addresses the
wh-questiontheflndoutactionwillbepoppedofitheplansincethealt-questionhasalready
been resolved.
One way of impleme...

**Algorithm:**

```
rule 2.16) would need to
be added (note that this rule requires QUD to be an open stack).
(rule 2.16) rule: downdateQUD2
class: downdate qud
in($/shared/qud, IssueQ)
pre: fst($/shared/qud, Q)
8
>< $domain :: resolves(Q, IssueQ)
eff: >: del(/shared/qud, IssueQ)
n
We also need to deflne resolvedness conditions for issue-questions (for example, an issue-
question cannot be resolved by an issue-question). In addition, rules for removing flndout
and raise actions from the plan based on the contents of QUD would need to be added.
```

---

## Algorithm 35: rule 2 .16) rule: downdateQUD2

**Section:** 2.12. DISCUSSION 63
**Page:** 85

**Context Before:**
> uestiontheflndoutactionwillbepoppedofitheplansincethealt-questionhasalready
been resolved.
One way of implementing this is to have rules which remove actions and questions which
concern what issue to ...

**Algorithm:**

```
rule 2.16) rule: downdateQUD2
class: downdate qud
in($/shared/qud, IssueQ)
pre: fst($/shared/qud, Q)
8
>< $domain :: resolves(Q, IssueQ)
eff: >: del(/shared/qud, IssueQ)
n
We also need to deflne resolvedness conditions for issue-questions (for example, an issue-
question cannot be resolved by an issue-question). In addition, rules for removing flndout
and raise actions from the plan based on the contents of QUD would need to be added.
```

---

## Algorithm 36: rule 2 .17) will pick up any question Q lying around on QUD

**Section:** 2.12.3 Reraising issues and sharing information
**Page:** 86

**Context Before:**
> the resources are set up to handle,
as long as each issue is resolved before moving on to the next one. If the user asks q and
then asks q0 before q has been resolved, IBiS1 will forget its plan for d...

**Algorithm:**

```
rule 2.17) will pick up any question Q lying around on QUD
when the plan and agenda is empty, check if there is a plan for resolving it, and if so load
this plan.
(rule 2.17) rule: recoverPlan
class: exec plan
fst($/shared/qud, Q)
is empty($/private/agenda)
pre: 8
>>>< is empty($/private/plan)
$domain :: plan(Q, Plan)
eff:
>>>:
set(/private/plan, Plan)
n
However, this solution has a problem. If, when dealing with a question q, the system
asks a question q and the user does not answer this question but instead raises a new
u
question q , both q and q will remain on QUD when q has been resolved. Now, if the
1 u 1
user simply answers q immediately after q has been resolved, everything is flne and the
u 1
system will reload the plan for dealing with q. However, if the user does not answer q ,
u
```

---

## Algorithm 37: rule 2 .17) rule: recoverPlan

**Section:** 2.12.3 Reraising issues and sharing information
**Page:** 86

**Context Before:**
> ved, IBiS1 will forget its plan for dealing with q and
instead load the plan for dealing with q0. When q0 has been resolved, IBiS1 will wait for
a new question from the user. However, q is still on QU...

**Algorithm:**

```
rule 2.17) rule: recoverPlan
class: exec plan
fst($/shared/qud, Q)
is empty($/private/agenda)
pre: 8
>>>< is empty($/private/plan)
$domain :: plan(Q, Plan)
eff:
>>>:
set(/private/plan, Plan)
n
However, this solution has a problem. If, when dealing with a question q, the system
asks a question q and the user does not answer this question but instead raises a new
u
question q , both q and q will remain on QUD when q has been resolved. Now, if the
1 u 1
user simply answers q immediately after q has been resolved, everything is flne and the
u 1
system will reload the plan for dealing with q. However, if the user does not answer q ,
u
```

---

## Algorithm 38: rule 2 .18) rule: reraiseIssue

**Section:** 2.12. DISCUSSION 65
**Page:** 87

**Context Before:**
> 2.12. DISCUSSION 65
this question will be topmost on QUD and block recoverPlan from triggering. Because of
the simple structure of QUD, IBiS1 sees no reason to ask q again; after all, it is already
u
...

**Algorithm:**

```
rule 2.18) rule: reraiseIssue
class: select action
fst($/shared/qud, Q)
pre:
not $domain :: plan(Q, SomePlan)
(
eff: push(/private/agenda, raise(A))
n
Issues are divided up between those for which the system has an associated plan in its
domain resource and those for which it does not. For example, the \price issue" is one for
which there is a plan: the system has to ask where the user wants to go, where from, when
etc. However, there is no plan associated with the question of where the user wants to go
from. This question is simply part of the plan for the price issue. Thus, when the system
flnds this question in the list of open issues (the flrst condition of this rule) and it flnds
that it does not have a plan for this issue (the second condition), it plans to reraise the
question.
Two furthermodiflcationsareneededtomakethisworksmoothly. Firstly, whenaquestion
is reraised that was previously on QUD, the simple stack structure of QUD will result in
two instances of the same question being topmost on QUD. One way of solving this is to
change the datatype of /shared/qud into an \open stack" or \stackset"; this datatype
can be regarded as a mix of a stack and a set. The property of open stacks relevant to our
problem is that when some element x is pushed on a stack which already contains x (or
an element uniflable with x), the resulting open stack will contain a single instance of x,
which is also topmost on the open stack.
Secondly, we need a rule for removing raise(Q) actions from the plan in case Q has already
been resolved; this rule is similar to the removeFindout rule described in Section 2.8.6.
```

---

## Algorithm 39: rule 2 .19) rule: removeRaise

**Section:** 2.12. DISCUSSION 65
**Page:** 88

**Context Before:**
> 66 CHAPTER 2. BASIC ISSUE-BASED DIALOGUE MANAGEMENT
(...

**Algorithm:**

```
rule 2.19) rule: removeRaise
class: exec plan
fst($/private/plan, raise(A))
pre: in($/shared/com, B)
8
>< $domain :: resolves(B, A)
eff: >: pop(/private/plan)
n
This rule is needed to avoid asking the same question twice in case it is flrst reraised and
then also included in a recovered plan.
A sample dialogue involving the system reraising an issue and recovering a plan is shown
in (dialogue 2.4). Incidentally, this dialogue also demonstrates information sharing be-
tween dialogue plans; when the user asks about visa, the system already knows what the
destination city is andthusdoes not ask thisagain. By contrast, in VoiceXML (McGlashan
et al., 2001), user-initiated subdialogues will cause previous dialogue to be forgotten. Only
if there is a pre-scripted, system-initiated transition from one form to another can the
previous dialogue be resumed after the subdialogue has been completed9.
(dialogue 2.4)
S> Welcome to the travel agency!
U> price information please
S> How do you want to travel?
U> plane
S> What city do you want to go to?
U> paris
S> What city do you want to go from?
U> do i need a visa
getLatestMove
9Information sharing in VoiceXML is only possible in the case where a form F calls another form F .
1 2
WhenF isflnishedandcontrolispassedbacktoF , informationmaybesentfromF toF . Information
2 1 2 1
sharing is not supported e.g. in cases where user initiative leads to the adoption of F while F is being
2 1
executed.
```

---

## Algorithm 40: Procedure/Rule in 2.12.5 Additional plan constructs

**Section:** 2.12.5 Additional plan constructs
**Page:** 92

**Algorithm:**

```
70 CHAPTER 2. BASIC ISSUE-BASED DIALOGUE MANAGEMENT
S> What city do you want to go from?
U> london
S> What month do you want to leave?
U> april
S> What day do you want to leave?
U> fifth
S> What class did you have in mind?
U>
S> The price is 7654 crowns, economy class. The price is 456 crowns,
business class.
A further possibility (that has not been implemented) is that the user provides a relevant
but not resolving answer to one or more questions raised by the system, e.g. by providing
a destination country when asked for a destination city. In this case, either the less speciflc
answer must match some other parameter in the database (e.g. if destination countries
are included in addition to destination cities), or some inference must be performed. This
inference may result in a disjunction of answers specifying parameters which are in the
database, e.g. the disjunction of all available destination cities in some specifled country.
This disjunction can then be used to search the database. Further database variations
include requesting answers to more that one question at a time (e.g. \I want information
about price information and departure dates for (cid:176)ights to Paris in April.").
2.12.5 Additional plan constructs
In IBiS1 we have used a very basic set of plan constructs. However, it is fairly straight-
forward to add new constructs, by adding new objects of type PlanConstruct and update
rules (of the class exec plan) for dealing with them. Some more complex constructs which
are not used here but have been used in GoDiS, the predecessor of IBiS (see e.g. Larsson
and Zaenen, 2000), are listed below, with brief explanations of what the corresponding
update rules do.
† if then(P, C) where P : proposition and C : PlanConstruct; if P is in /private/bel
or /shared/com, then replace if then(P, C) with C ; otherwise, delete it
1
† if then else(P, C , C ) where P : proposition and C : PlanConstruct and C :
1 2 1 2
PlanConstruct; if P is in /private/bel or /shared/com, then replace if then(P,
C) with C ; otherwise, replace it by C
1 2
† exec(fi), where fi : Action is an action such that there is a plan ƒ for doing fi; replace
exec(fi) with ƒ (see Chapter 5 for a discussion of action-related plans)
```

---

## Algorithm 41: Procedure/Rule in 2.12.6 Questions and answers vs. slots and flllers

**Section:** 2.12.6 Questions and answers vs. slots and flllers
**Page:** 93

**Algorithm:**

```
2.12. DISCUSSION 71
† hC ;:::;C i where C : PlanConstruct (1 • i • n); prepend C ;:::;C to the
1 n i 1 n
/private/plan fleld.
Theseconstructsaddconsiderablytotheversatilityofdialogueplans, andallowe.g. asking
whether the user wants a return trip (formalized e.g. as a question ?return), and ask
appropriate questions (return date etc.) only if the users gives a positive response (i.e. if
the proposition return is in /shared/com). A dialogue plan for accomplishing this is
shown in (2.23).
(2.23) issue : ?x.price(x)
plan: h
flndout(?x:means of transport(x)),
flndout(?x:dest city(x)),
flndout(?x:depart-city(x)),
flndout(?x:depart-month(x)),
flndout(?x:depart-day(x)),
flndout(?x:class(x)),
flndout(?return),
if then( return, h flndout(?x:return-month(x)),
flndout(?x:return-day(x)) i ),
consultDB(?x:price(x))
i
2.12.6 Questions and answers vs. slots and flllers
In principle, a slot in a form can be seen as a question, and a flller can be seen as an answer
to that question. The result, a slot-flller pair, is the equivalent of a proposition. If the
value of a slot is binary (0/1 or yes/no), the slot corresponds to a y/n-question; otherwise,
it corresponds to a wh- or alternative question.
For example, in a travel agency setting a form-based system might have a form containing
a slot dest-city for the destination city; this would correspond to a question represented
in lambda-calculus as ?x:dest-city(X) (\What is the destination city?"). A flller for this
would be e.g. paris, which would also constitute an answer to the question. The slot-
flller pair dest-city=paris would then correspond to the FOL proposition resulting from
applying the question to the answer, dest-city(paris).
But there are also important difierences between form-based and issue-based dialogue
management. For example, a single answer may be relevant to questions in several plans.
This enables information-sharing between plans, i.e. when executing a plan the system
```

---

## Algorithm 42: Procedure/Rule in 3.1.1 Dialogue examples

**Section:** 3.1.1 Dialogue examples
**Page:** 98

**Algorithm:**

```
76 CHAPTER 3. GROUNDING ISSUES
3.1.1 Dialogue examples
The human-human dialogue excerpt1 in (3.1) shows two common kinds of feedback. J’s
\mm" shows that J (thinks that he) understood P’s previous utterance; P’s \pardon"
shows that P was not able to hear J’s previous utterance. The example also includes a
hesitation sound (\um") from J. (P is a customer and J a travel agent.)
(3.1) P : o˜m (.) (cid:176)yg ti paris
um (.) (cid:176)ight to paris
J : mm (.) ska du ha en returbiljett
mm (.) do you want a return ticket
P : va sa du
pardon
J : ska du ha en tur”a retur
do you want a round trip
The feedback in (3.1) consisted of conventionalized feedback words (\mm", \pardon").
However, feedback may also be more explicit and repeat the central content of the previous
utterance, as K’s second feedback utterance in (3.2).
(3.2) B : ja ska va framme i [ go˜teborg ] e e ungefa˜r vi nietiden om
1 1
de flnns n”a tidit [ morgon(cid:176)yg ]
2 2
I need to be in Gothenburg er er around nine if there is an early
morning (cid:176)ight
K : [ m ]
1 1
m
K : [ vi ] nietiden m vi ska se
2 2
Around nine m let’s see
The function of an utterance answering a question is not primarily to give feedback, but
rather to provide task-related information. However, an answer also shows that the pre-
vious question was understood and integrated. Example (3.3) shows that feedback is
sometimes given in reaction to a question before the question is answered.
(3.3) J : sen m”aste du ha e s”an da˜r intenationellt studentkort ocks”a
ha du de
then you need one of those international student cards do you
have that
P : mm na˜
mm no
1Exceptwherenoted,thehuman-humandialoguesinthischapterhavebeencollectedbytheUniversity
ofLundaspartoftheSDSproject. WequotetranscriptionsdoneinG˜oteborgaspartofthesameproject.
The (.) symbol indicates a pause.
```

---

## Algorithm 43: Procedure/Rule in 3.2.3 Allwood: Interactive Communication Management

**Section:** 3.2.3 Allwood: Interactive Communication Management
**Page:** 105

**Algorithm:**

```
3.2. BACKGROUND 83
For clarity, we reproduce the full protocol in a more schematic way:
try to flnd an answer resolving q (u) = ?x.content(u, x)
content
† no answer found ! push q (u) on QUD, produce q (u)-speciflc utterance
content content
† answer c found !
{ c is a question ! consider q (c) = ?MAX-QUD(c)
accept
⁄ decide on \no" ! push q (c) on QUD, produce q (c)-speciflc utter-
accept accept
ance [reject c]
⁄ decide on \yes" ! push c on QUD, produce c-speciflc utterance [accept c]
{ c is a proposition ! consider q (?c)
accept
⁄ no ! push q (?c) on QUD, produce q (?c)-speciflc utterance [reject
accept accept
?c as topic for discussion]
⁄ yes ! consider ?c [accept ?c as topic for discussion]
¢ no ! push ?c on QUD, produce ?c-speciflc utterance [reject c as fact]
¢ yes ! add c to FACTS [accept c as fact]
Note that there are a number of decisions that need to be made by B, and for each of these
decisions there is the possibility of rejecting u on the corresponding level. For a question,
there is only one way of rejecting it (once the content question has been resolved): to reject
it as a question under discussion. This amounts to refusing to discuss the question. For
a proposition p, there are two difierent ways of rejecting it. Firstly, one may reject the
issue \whether p" completely; this amounts to refusing to discuss whether p is true or not.
Alternatively, one may accept \whether p" for discussion but reject p as a fact.
3.2.3 Allwood: Interactive Communication Management
Allwood(1995)usestheconceptof\InteractiveCommunicationManagement"todesignate
all communication dealing with the management of dialogue interaction. This includes
feedback but also sequencing and turn management. Sequencing \concerns the mecha-
nisms, whereby a dialogue is structured into sequences, subactivities, topics etc. ...".
Here, we will use the term ICM as a general term for coordination of the common ground,
which in an information state update approach comes to mean explicit signals enabling
coordination of updates to the common ground. While feedback is associated with speciflc
utterances, ICM in general does not need to concern any speciflc utterance.
```

---

## Algorithm 44: Procedure/Rule in 3.3.1 Levels of action in dialogue

**Section:** 3.3.1 Levels of action in dialogue
**Page:** 106

**Algorithm:**

```
84 CHAPTER 3. GROUNDING ISSUES
As will be seen below, we will also be making use of various other parts of Allwood’s
\activity-based pragmatics" (Allwood, 1995), including Allwood’s action level terminol-
ogy, the concept of Own Communication Management (OCM), and various distinctions
concerning ICM.
3.3 Preliminary discussion
In the previous section we have seen examples of difierent ways of accounting for grounding
and feedback. We feel that they all ofier useful insights, and that they together can serve
as a basis for our further explorations.
Therefore, in this section we will discuss the accounts presented in Section 3.2, relate them
to each other, and establish some basic principles and terminological conventions.
3.3.1 Levels of action in dialogue
Both Allwood (1995) and Clark (1996) distinguish four levels of action involved in com-
munication (S is the speaker of utterance u, H is the hearer/addressee). They use slightly
difierent terminologies; here we use Allwood’s terminology and add Clark’s (and, for the
reaction level, also Ginzburg’s) corresponding terms in parenthesis. The deflnitions are
mainly derived from Allwood.
† Reaction (acceptance, consideration): whether H has integrated (the content of) u
† Understanding (recognition): whether H understands u
† Perception (identiflcation): whether H perceives u
† Contact (attention): whether H and S have contact, i.e. if they have established a
channel of communication
These levels of action are involved in all dialogue, and to the extent that contact, per-
ception, understanding and acceptance can be said to be negotiated, all human-human
dialogue has an element of negotiation built in. Note that the above list of levels is formu-
lated in terms of the hearer’s perspective.
Giventhatgroundingisconcernedwithalllevels,itfollowsthatfouraspectsofanutterance
u in a dialogue between H and S can in principle be represented in the common ground,
one for each action level:
```

---

## Algorithm 45: Procedure/Rule in 3.4.1 Classifying explicit feedback

**Section:** 3.4.1 Classifying explicit feedback
**Page:** 112

**Algorithm:**

```
90 CHAPTER 3. GROUNDING ISSUES
haviourinthissenseincludesaskingandansweringtask-levelquestions,givinginstructions,
etc. (cf. the \Core Speech Acts" of Poesio and Traum, 1998). Answering a domain-level
question (e.g. saying \Paris" in response to \What city do you want to go to?") certainly
involves aspects of grounding and acceptance, since it shows that the question was under-
stood and accepted. However, the primary function of a domain-level answer is to resolve
the question, not to show that it was understood and accepted.
A single utterance may include both feedback and domain-level information. Clark talks
about communication of these two types of information as belonging to difierent \tracks":
domain-level information is on track 1 while feedback, and grounding-related communica-
tion in general, is on track 2.
In this section we will attempt to give an overview of various aspects of feedback. We will
return to sequencing ICM in Section 3.6.9.
3.4.1 Classifying explicit feedback
To get an overview of the range of explicit feedback behaviour that exists in human-human
dialogue, we will classify feedback according to four criteria. We will assume that DP S
has just uttered or is uttering u to DP H, when the feedback utterance f (uttered by H
to S) occurs.
† level of action / basic communicative function (contact, perception, understanding,
reaction / acceptance)
† polarity (positive / negative): whether f indicates contact / perception / under-
standing / acceptance or lack thereof
† eliciting / non-eliciting: whether f is intended to evoke a response (e.g. a reformu-
lation or a reason to accept some content)
† form of f: single word, repetition etc.
† content of f: object-level or meta-level
The action level criterion has been explained above; the others will be explained presently.
The criteria of basic communicative function, polarity, eliciting/non-eliciting, and surface
form are all derived from Allwood et al. (1992) and Allwood (1995).
```

---

## Algorithm 46: Procedure/Rule in 3.5.3 The cautious strategy

**Section:** 3.5.3 The cautious strategy
**Page:** 119

**Algorithm:**

```
3.5. UPDATE STRATEGIES FOR GROUNDING 97
surface form of the utterance; to assume grounding on the understanding level is to update
the common ground with a semantic representation of the utterance. Finally, to assume
an utterance has been grounded on the acceptance level is to update the common ground
with the intended efiects of the utterance (e.g. pushing a question on QUD). Thus, the
grounding assumption can be divided into four independent assumptions, one for each of
these levels; we will concentrate on the understanding and integration levels.
The independence of these assumptions means e.g. that it is possible to make an optimistic
assumptionaboutunderstandingbutapessimisticoneaboutacceptance. Thiswouldmean
assumingthatanutterancewasunderstoodassoonasitwasuttered, butrequiringpositive
evidence before it is assumed to be accepted.
3.5.3 The cautious strategy
Clark seems to assume that once an utterance has been grounded, there is no turning back;
the grounding assumption cannot be undone. That is, the moment information about an
utterance is added to the common ground there is no way (short of general strategies for
beliefrevision)ofunderstandingnegativefeedbackandreacttoitbymodifyingorremoving
the grounded material.
However, we believe that there is a difierence between assuming an utterance as grounded
(added to the common ground) and giving up the possibility of modifying or correcting
the grounded material. This opens up a new kind of grounding strategy not included in
Clark’s account: the cautious strategy.
For a DP using a cautious strategy, it is possible to assume an utterance as being grounded,
while still being able to understand and react appropriately to negative feedback. This
requires (1) that negative feedback, which is often underspecifled in the sense that it does
not explicitly identify which part of an utterance it concerns, can be correctly interpreted,
and (2) that the DP can revise the common ground in a way which undoes all efiects of
the erroneous assumption that the utterance was grounded. A simple example is shown in
(3.12).
(3.12) A : Do I need a visa?
A optimistically assumes that \does A need a visa?" is now
under discussion.
B : Pardon?
A correctly interprets B’s utterance as negative feedback (proba-
bly on the perception level) regarding the previous utterance, and
retracts the assumption that \does A need a visa?" is on QUD.
```

---

## Algorithm 47: procedure in human-human

**Section:** 3.6.3 Issue-based grounding in IBiS
**Page:** 122

**Context Before:**
> stinction is what we have here referred to as polarity: \explicit" veriflcation
is neutral (and eliciting and interrogative) whereas \implicit" veriflcation is positive.
Given that veriflcation is a r...

**Algorithm:**

```
procedure in human-human
dialogue. Second, because it only involves part of the full spectrum of feedback behaviour,
excluding e.g. acceptance-related feedback behaviour.
```

**Context After:**
> 3.6.3 Issue-based grounding in IBiS
In this section we outline a (partially) issue-based account of grounding in terms of infor-
mation state updates, inspired by Ginzburg’s account of content questio...

---

## Algorithm 48: rule 3 .1).

**Section:** 3.6.6 Grounding of user utterances in IBiS2
**Page:** 132

**Context Before:**
> 110 CHAPTER 3. GROUNDING ISSUES
In addition to being checked for relevance, contentful moves are checked for integratability
(acceptability) and if these conditions are not fulfllled the move will not...

**Algorithm:**

```
rule 3.1).
(rule 3.1) rule: integrateUsrAsk
class: integrate
$/shared/lu/speaker==usr
fst($/private/nim, ask(Q))
8
pre: >>>>>><
S
$s
c
c
o
o
re
re
>
=
0
S
.7
core
$domain :: plan(Q, Plan)
>>>>>>:
1 pop(/private/nim)
2 push(/private/agenda, icm:acc*pos)
8
eff:
>>>>>>>>>>>>>>><
5
3
4
i
a
i
f
f
p
d
d
d
u
d
o
o
s
(
h
(
(
/
i
S
s
(
n
/
h
c
(
p
o
a
$
r
r
/
r
e
s
i
e
v
h
•
d
a
a
t
/
r
0
l
e
.
e
u
9
/
d
,
/
a
/
m
g
q
e
o
u
n
v
d
d
e
,
a
s
Q
,
,
a
)
ic
s
m
a
k
n
(
:
Q
d
un
)
n
)
d
o
*
t
po
fs
s
t
:u
($
sr
/
*
s
i
h
ss
a
u
r
e(
e
Q
d
)
/
)
q
)
ud, Q),
push(/private/agenda, icm:reraise:Q))
>>>>>>>>>>>>>>>:
6
7
p
p
u
u
s
s
h
h
(
(
/
/
s
p
h
r
a
iv
r
a
e
t
d
e
/
/
q
a
u
g
d
e
,
n
Q
da
)
, respond(Q))
The flrst two conditions picks out a user ask move on nim. The third and fourth con-
ditions check the recognition score of the utterance and if it is higher than 0.7 (T ), the
2
rule proceeds to check for acceptability. If the score is too low, the move should not be
optimistically integrated; instead, a pessimistic grounding strategy should be applied and
interrogative feedback selected (see below).
The flfth condition checks for acceptability, i.e. that the system is able to deal with this
question, i.e. that there is a corresponding plan in the domain resource. If not, the
integration rule will not trigger and the ask move will remain on nim until the selection
phase, where it will give rise to an issue rejection (see Section 3.6.6).
The flrst update pops the integrated move ofi nim. In update 2, positive integration
feedback is added to the agenda, to indicate that the system can integrate the ask-move.
Update 3 adds the move to /shared/lu/moves, thereby re(cid:176)ecting the optimistic ground-
ing assumption on the understanding level. In update 4, positive understanding feedback
is selected unless the score is higher than 0.9 (T ).
1
```

---

## Algorithm 49: rule 3 .1) rule: integrateUsrAsk

**Section:** 3.6.6 Grounding of user utterances in IBiS2
**Page:** 132

**Context Before:**
> 110 CHAPTER 3. GROUNDING ISSUES
In addition to being checked for relevance, contentful moves are checked for integratability
(acceptability) and if these conditions are not fulfllled the move will not...

**Algorithm:**

```
rule 3.1) rule: integrateUsrAsk
class: integrate
$/shared/lu/speaker==usr
fst($/private/nim, ask(Q))
8
pre: >>>>>><
S
$s
c
c
o
o
re
re
>
=
0
S
.7
core
$domain :: plan(Q, Plan)
>>>>>>:
1 pop(/private/nim)
2 push(/private/agenda, icm:acc*pos)
8
eff:
>>>>>>>>>>>>>>><
5
3
4
i
a
i
f
f
p
d
d
d
u
d
o
o
s
(
h
(
(
/
i
S
s
(
n
/
h
c
(
p
o
a
$
r
r
/
r
e
s
i
e
v
h
•
d
a
a
t
/
r
0
l
e
.
e
u
9
/
d
,
/
a
/
m
g
q
e
o
u
n
v
d
d
e
,
a
s
Q
,
,
a
)
ic
s
m
a
k
n
(
:
Q
d
un
)
n
)
d
o
*
t
po
fs
s
t
:u
($
sr
/
*
s
i
h
ss
a
u
r
e(
e
Q
d
)
/
)
q
)
ud, Q),
push(/private/agenda, icm:reraise:Q))
>>>>>>>>>>>>>>>:
6
7
p
p
u
u
s
s
h
h
(
(
/
/
s
p
h
r
a
iv
r
a
e
t
d
e
/
/
q
a
u
g
d
e
,
n
Q
da
)
, respond(Q))
The flrst two conditions picks out a user ask move on nim. The third and fourth con-
ditions check the recognition score of the utterance and if it is higher than 0.7 (T ), the
2
rule proceeds to check for acceptability. If the score is too low, the move should not be
optimistically integrated; instead, a pessimistic grounding strategy should be applied and
interrogative feedback selected (see below).
The flfth condition checks for acceptability, i.e. that the system is able to deal with this
question, i.e. that there is a corresponding plan in the domain resource. If not, the
integration rule will not trigger and the ask move will remain on nim until the selection
phase, where it will give rise to an issue rejection (see Section 3.6.6).
The flrst update pops the integrated move ofi nim. In update 2, positive integration
feedback is added to the agenda, to indicate that the system can integrate the ask-move.
Update 3 adds the move to /shared/lu/moves, thereby re(cid:176)ecting the optimistic ground-
ing assumption on the understanding level. In update 4, positive understanding feedback
is selected unless the score is higher than 0.9 (T ).
1
```

---

## Algorithm 50: rule 3 .2).

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 111
**Page:** 133

**Context Before:**
> arded as a
shortcut for reasoning about obligations and intentions; when accepting a user question,
thus accepting the obligation to try to respond to it, the system will automatically intend
to respo...

**Algorithm:**

```
rule 3.2).
(rule 3.2) rule: selectIcmOther
class: select icm
in($/private/agenda, icm:A)
pre:
not in($next moves, B) and B=ask(C)
(
push(next moves, icm:A)
eff:
del(/private/agenda, icm:A)
(
Dialogue example: integrating user ask-move The dialogue below shows how a user
ask move with a score of 0.76 is successfully integrated, and positive understanding and
acceptance feedback is produced.
(dialogue 3.3)
S> Welcome to the travel agency!
U> price information please [0.76]
getLatestMoves
set(/private/nim, oqueue([ask(?A.price(A))]))
set(/shared/lu/speaker, usr)
8
clear(/shared/lu/moves)
>><
set(/shared/pm, set([greet]))
integrateUsrAsk
>>:
```

---

## Algorithm 51: rule 3 .2) rule: selectIcmOther

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 111
**Page:** 133

**Context Before:**
> hortcut for reasoning about obligations and intentions; when accepting a user question,
thus accepting the obligation to try to respond to it, the system will automatically intend
to respond to it.
De...

**Algorithm:**

```
rule 3.2) rule: selectIcmOther
class: select icm
in($/private/agenda, icm:A)
pre:
not in($next moves, B) and B=ask(C)
(
push(next moves, icm:A)
eff:
del(/private/agenda, icm:A)
(
Dialogue example: integrating user ask-move The dialogue below shows how a user
ask move with a score of 0.76 is successfully integrated, and positive understanding and
acceptance feedback is produced.
(dialogue 3.3)
S> Welcome to the travel agency!
U> price information please [0.76]
getLatestMoves
set(/private/nim, oqueue([ask(?A.price(A))]))
set(/shared/lu/speaker, usr)
8
clear(/shared/lu/moves)
>><
set(/shared/pm, set([greet]))
integrateUsrAsk
>>:
```

---

## Algorithm 52: rule 3 .3).

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 111
**Page:** 134

**Context Before:**
> next moves, icm:acc*pos)
del(/private/agenda, icm:acc*pos)
‰
selectIcmOther
push(next moves, icm:und*pos:usr*issue(?A.price(A)))
del(/private/agenda, icm:und*pos:usr*issue(?A.price(A)))
‰
selectIcmOth...

**Algorithm:**

```
rule 3.3).
(rule 3.3) rule: selectIcmUndIntAsk
class: select icm
$/shared/lu/speaker==usr
pre: fst($/private/nim, ask(Q))
8
>< $score • 0.7
pop(/private/nim)
eff:
>:
push(next moves, icm:und*int:usr*issue(Q))
(
```

---

## Algorithm 53: rule 3 .3) rule: selectIcmUndIntAsk

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 111
**Page:** 134

**Context Before:**
> icm:acc*pos)
del(/private/agenda, icm:acc*pos)
‰
selectIcmOther
push(next moves, icm:und*pos:usr*issue(?A.price(A)))
del(/private/agenda, icm:und*pos:usr*issue(?A.price(A)))
‰
selectIcmOther
selectAsk...

**Algorithm:**

```
rule 3.3) rule: selectIcmUndIntAsk
class: select icm
$/shared/lu/speaker==usr
pre: fst($/private/nim, ask(Q))
8
>< $score • 0.7
pop(/private/nim)
eff:
>:
push(next moves, icm:und*int:usr*issue(Q))
(
```

---

## Algorithm 54: rule 3 .4) is similar to that for ask moves, except that answers are checked for relevance

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 113
**Page:** 135

**Context Before:**
> ead, we follow the general
philosophy of IBiS of trying to keep our representation as simple as possible as long as
it works. The interrogative feedback selected in the second update will, in a sense,...

**Algorithm:**

```
rule 3.4) is similar to that for ask moves, except that answers are checked for relevance
as well as reliability and acceptability.
(rule 3.4) rule: integrateUsrAnswer
class: integrate
1 fst($/private/nim, answer(A))
2 $/shared/lu/speaker==usr
8
pre:
>>>>>>>>>>>>><
5
4
3
f
S
!
s
c
t
$
(
o
s
$
r
c
/
e
o
s
>
r
h
e
a
0
=
r
.7
e
S
d
co
/
r
q
e
ud, Q)
6 $domain :: relevant(A, Q)
>>>>>>>>>>>>>:
1
7
8
p
$
$
o
d
d
p
a
o
(
t
m
/
a
p
a
b
r
i
a
n
iv
s
:
a
e
:
t
:
c
e
:
o
/
m
v
n
a
b
i
l
m
i
i
d
n
)
D
e(
B
Q
p
,
a
A
ra
,
m
P
e
)
ter(P) or P=not(X)
2 add(/shared/lu/moves, answer(P))
8
eff:
>>>>>>>>< 3
4
p
if
u
d
s
o
h
(
(
S
/p
co
r
r
iv
e
a
•
te
0
/
.9
ag
a
e
n
n
d
d
A
a,
6=
ic
y
m
es
:a
a
c
n
c*
d
p
A
os)
6= no,
push(/private/agenda, icm:und*pos:usr*P))
>>>>>>>>: 5 add(/shared/com, P)
Conditions 1-4 are similar to those for the integrateUsrAsk rule. The relevance of the
content of the answer to a question on QUD is checked in condition 6.
The acceptability condition in the condition 8 makes sure that the propositional content
resulting from combining the question topmost on QUD with the content of the answer-
move is either
† a valid database parameter, or
† a negated proposition
```

---

## Algorithm 55: rule 3 .4) rule: integrateUsrAnswer

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 113
**Page:** 135

**Context Before:**
> errogative feedback selected in the second update will, in a sense, take
over the function of the original move; if the feedback is answered positively, the end result
will be the same as if the ask m...

**Algorithm:**

```
rule 3.4) rule: integrateUsrAnswer
class: integrate
1 fst($/private/nim, answer(A))
2 $/shared/lu/speaker==usr
8
pre:
>>>>>>>>>>>>><
5
4
3
f
S
!
s
c
t
$
(
o
s
$
r
c
/
e
o
s
>
r
h
e
a
0
=
r
.7
e
S
d
co
/
r
q
e
ud, Q)
6 $domain :: relevant(A, Q)
>>>>>>>>>>>>>:
1
7
8
p
$
$
o
d
d
p
a
o
(
t
m
/
a
p
a
b
r
i
a
n
iv
s
:
a
e
:
t
:
c
e
:
o
/
m
v
n
a
b
i
l
m
i
i
d
n
)
D
e(
B
Q
p
,
a
A
ra
,
m
P
e
)
ter(P) or P=not(X)
2 add(/shared/lu/moves, answer(P))
8
eff:
>>>>>>>>< 3
4
p
if
u
d
s
o
h
(
(
S
/p
co
r
r
iv
e
a
•
te
0
/
.9
ag
a
e
n
n
d
d
A
a,
6=
ic
y
m
es
:a
a
c
n
c*
d
p
A
os)
6= no,
push(/private/agenda, icm:und*pos:usr*P))
>>>>>>>>: 5 add(/shared/com, P)
Conditions 1-4 are similar to those for the integrateUsrAsk rule. The relevance of the
content of the answer to a question on QUD is checked in condition 6.
The acceptability condition in the condition 8 makes sure that the propositional content
resulting from combining the question topmost on QUD with the content of the answer-
move is either
† a valid database parameter, or
† a negated proposition
```

---

## Algorithm 56: rule 3 .5).

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 113
**Page:** 136

**Context Before:**
> n
that these are easily recognized; if this is not the case, their special status should be
removed. Finally, update 5 adds the proposition resulting from combining the question on
QUD with the conten...

**Algorithm:**

```
rule 3.5).
(If the question is not acceptable it will instead be rejected; see Section 3.6.6).
(rule 3.5) rule: selectIcmUndIntAnswer
class: select icm
fst($/private/nim, answer(A))
$/shared/lu/speaker==usr
8
pre:
>>>>>>>>< $
fs
s
t
c
($
o
/
r
s
e
ha
•
re
0.
d
7
/qud, B)
$domain :: relevant(A, B)
eff:
>>>>>>>>:
p
$
o
d
p
o
(
m
/p
a
r
in
iva
::
t
c
e
o
/
m
n
b
im
in
)
e(B, A, C)
push(next moves, icm:und*int:usr*C)
(
The conditions check that there is a user answer move on nim whose content is relevant
to and combines with a question on QUD, and that the recognition score was less than or
equal to 0.7. If these conditions are true, the move is popped ofi nim and interrogative
understanding feedback is selected.
Integrating and responding to interrogative feedback
Integrating interrogative understanding feedback As explained in Section 3.6.3,
Interrogative feedback raises understanding questions. This is re(cid:176)ected in (rule 3.6).
```

---

## Algorithm 57: rule 3 .5) rule: selectIcmUndIntAnswer

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 113
**Page:** 136

**Context Before:**
> ved. Finally, update 5 adds the proposition resulting from combining the question on
QUD with the content of the answer move to the shared commitments.
Interrogative understanding feedback for user as...

**Algorithm:**

```
rule 3.5) rule: selectIcmUndIntAnswer
class: select icm
fst($/private/nim, answer(A))
$/shared/lu/speaker==usr
8
pre:
>>>>>>>>< $
fs
s
t
c
($
o
/
r
s
e
ha
•
re
0.
d
7
/qud, B)
$domain :: relevant(A, B)
eff:
>>>>>>>>:
p
$
o
d
p
o
(
m
/p
a
r
in
iva
::
t
c
e
o
/
m
n
b
im
in
)
e(B, A, C)
push(next moves, icm:und*int:usr*C)
(
The conditions check that there is a user answer move on nim whose content is relevant
to and combines with a question on QUD, and that the recognition score was less than or
equal to 0.7. If these conditions are true, the move is popped ofi nim and interrogative
understanding feedback is selected.
Integrating and responding to interrogative feedback
Integrating interrogative understanding feedback As explained in Section 3.6.3,
Interrogative feedback raises understanding questions. This is re(cid:176)ected in (rule 3.6).
```

---

## Algorithm 58: rule 3 .6) rule: integrateUndIntICM

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 115
**Page:** 137

**Context Before:**
> 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 115
(...

**Algorithm:**

```
rule 3.6) rule: integrateUndIntICM
class: integrate
pre: fst($/private/nim, icm:und*int:DP*C)
n pop(/private/nim)
eff: add(/shared/lu/moves, icm:und*int:DP*C)
8
>< push(/shared/qud, und(DP*C))
>:
The condition simply checks that there is an icm:und*int:DP*C move on nim, which is
then popped ofi by the flrst update and added to /shared/lu/moves by the second
update. The third update pushes the understanding question ?und(DP*C) on QUD.
Integrating positive answer to understanding-question When the system raises
an understanding question (e.g. by saying \To Paris, is that correct?"), the user can either
say \yes" or \no". (The case where the user does not give a relevant answer to the inter-
rogative feedback is treated in Section 3.6.8). In IBiS2, we do not represent propositions
related to the understanding of utterances in the same way as other propositions (which
are stored in /shared/com). Therefore, special rules are needed for dealing with answers
to understanding-questions.
The rule for integrating a negative answer to an understanding-question is shown in (rule
3.7).
(rule 3.7) rule: integrateNegIcmAnswer
```

**Context After:**
> class: integrate
fst($/private/nim, answer(no))
pre:
fst($/shared/qud, und(DP*C))
(
pop(/private/nim)
add(/shared/lu/moves, answer(und(DP*C)))
eff: 8
>>>< pop(/shared/qud)
push(/private/agenda, icm:un...

---

## Algorithm 59: 3 .7).

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 115
**Page:** 137

**Context Before:**
> rect?"), the user can either
say \yes" or \no". (The case where the user does not give a relevant answer to the inter-
rogative feedback is treated in Section 3.6.8). In IBiS2, we do not represent pro...

**Algorithm:**

```
rule
3.7).
(rule 3.7) rule: integrateNegIcmAnswer
class: integrate
fst($/private/nim, answer(no))
pre:
fst($/shared/qud, und(DP*C))
(
pop(/private/nim)
add(/shared/lu/moves, answer(und(DP*C)))
eff: 8
>>>< pop(/shared/qud)
push(/private/agenda, icm:und*pos:DP*not(C))
>>>:
The conditions check that there’s an answer(yes) move on nim and an understanding-
question on QUD. The flrst three updates establish the move as shared and pop the
understanding-question ofi QUD. Finally, positive feedback is selected to indicate that
the system has understood that the assumed interpretation C was incorrect.
Integrating positive answer to understanding question The rule for integrating a
positive answer to an understanding-question is shown in (rule 3.8).
```

---

## Algorithm 60: rule 3 .7) rule: integrateNegIcmAnswer

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 115
**Page:** 137

**Context Before:**
> user can either
say \yes" or \no". (The case where the user does not give a relevant answer to the inter-
rogative feedback is treated in Section 3.6.8). In IBiS2, we do not represent propositions
rel...

**Algorithm:**

```
rule 3.7) rule: integrateNegIcmAnswer
class: integrate
fst($/private/nim, answer(no))
pre:
fst($/shared/qud, und(DP*C))
(
pop(/private/nim)
add(/shared/lu/moves, answer(und(DP*C)))
eff: 8
>>>< pop(/shared/qud)
push(/private/agenda, icm:und*pos:DP*not(C))
>>>:
The conditions check that there’s an answer(yes) move on nim and an understanding-
question on QUD. The flrst three updates establish the move as shared and pop the
understanding-question ofi QUD. Finally, positive feedback is selected to indicate that
the system has understood that the assumed interpretation C was incorrect.
Integrating positive answer to understanding question The rule for integrating a
positive answer to an understanding-question is shown in (rule 3.8).
```

---

## Algorithm 61: rule 3 .8) rule: integratePosIcmAnswer

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 115
**Page:** 138

**Context Before:**
> 116 CHAPTER 3. GROUNDING ISSUES
(...

**Algorithm:**

```
rule 3.8) rule: integratePosIcmAnswer
class: integrate
fst($/private/nim, answer(yes))
pre:
fst($/shared/qud, und(DP*Content))
(
pop(/private/nim)
add(/shared/lu/moves, answer(und(DP*Content)))
8
eff:
>>>>>>>>>>><
i
p
f
o
t
p
p
h
(
u
e
/
n
s
s
h
h
e
(
a
l
/
s
r
s
e
h
(
e
C
a
d
o
r
/
n
q
e
t
d
u
e
/
d
n
q
t
)
=
ud
is
,
su
Q
e(
)
Q), [
push(/private/agenda, respond(Q)) ],
>>>>>>>>>>>:
add(/shared/com, Content))
The conditions and the flrst three updates are similar to those in the integrateNegIc-
mAnswer rule. The flnal (conditionalized) update integrates the content C. If the \orig-
inal" move (the move which caused the interrogative feedback to be produced in the flrst
place) was ask, C will be a proposition issue(Q). Consequently, integrating this propo-
sitions has the same efiects as integrating an ask-move: pushing the question Q on QUD
and pushing the action respond(Q) on the agenda. If the proposition is not of this type, it
is simply added to /shared/com.
Dialogue example: positive and negative response to interrogative feedback In
the following dialogue, the system produces interrogative understanding feedback for two
user utterances, one containing an ask move and the other containing an answer move. The
flrst interrogative feedback is answered positively and the second negatively.
(dialogue 3.4)
U> price information please [0.65]
getLatestMoves
agenda = hhii
private = plan = hi
2 2 3 3
nim = ask(?A.price(A))
6 4 com = fg 5 7
6 ›› fifi 7
6 qud = hi 7
6 shared = 2 3 7
6 speaker = usr 7
6 lu = 7
6 6 moves = fg 7 7
6 6 • ‚ 7 7
4 4 5 5
backupShared
selectIcmUndIntAsk
pop(/private/nim)
push(/private/agenda, icm:und*int:usr*issue(?A.price(A)))
‰
```

---

## Algorithm 62: rule 3 .9).

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 119
**Page:** 142

**Context Before:**
> n the
perception level, e.g. \I didn’t hear what you said.".
We have conflgured the input module to set the input variable to ‘TIMED OUT’ if nothing
is detected, and to ‘FAIL’ if something unrecogniza...

**Algorithm:**

```
rule 3.9).
(rule 3.9) rule: selectIcmConNeg
class: select icm
$input= ‘TIMED OUT’
pre: is empty($next moves)
8
>< is empty($/private/agenda)
eff: >: push(next moves, icm:con*neg)
n
Unless the system has something else to do, this will trigger negative contact ICM by the
system, realisede.g. as\Ididn’thearanythingfromyou.". Thepurposeofthisisprimarily
to indicate to the user that nothing was heard, but perhaps also to elicit some response
from the user to show that she is still there. Admittedly, this is a rather undeveloped
aspect of ICM in the current IBiS implementation, and alternative strategies could be
explored. For example, the system could increase the timeout span successively instead of
repeating negative contact ICM every flve seconds. Other formulations with more focus on
the eliciting function could also be considered, e.g. \Are you there?" or simply \Hello?".
The second and third condition check that nothing is on the agenda or in next moves.
The motivation for this is that there is no reason to address contact explicitly in this case,
since any utterance from the system implicitly tries to establish contact.
Default ICM integration rule Since contact is not explicitly represented in the infor-
mation state proper, integration of negative system contact ICM moves have no speciflc
efiect on the information state, and are therefore integrated by the default ICM integration
rule shown in (rule 3.10). Unless an ICM move has a speciflc integration rule deflned for
```

**Context After:**
> it, it will be integrated by this rule....

---

## Algorithm 63: rule 3 .9) rule: selectIcmConNeg

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 119
**Page:** 142

**Context Before:**
> tion level, e.g. \I didn’t hear what you said.".
We have conflgured the input module to set the input variable to ‘TIMED OUT’ if nothing
is detected, and to ‘FAIL’ if something unrecognizable was dete...

**Algorithm:**

```
rule 3.9) rule: selectIcmConNeg
class: select icm
$input= ‘TIMED OUT’
pre: is empty($next moves)
8
>< is empty($/private/agenda)
eff: >: push(next moves, icm:con*neg)
n
Unless the system has something else to do, this will trigger negative contact ICM by the
system, realisede.g. as\Ididn’thearanythingfromyou.". Thepurposeofthisisprimarily
to indicate to the user that nothing was heard, but perhaps also to elicit some response
from the user to show that she is still there. Admittedly, this is a rather undeveloped
aspect of ICM in the current IBiS implementation, and alternative strategies could be
explored. For example, the system could increase the timeout span successively instead of
repeating negative contact ICM every flve seconds. Other formulations with more focus on
the eliciting function could also be considered, e.g. \Are you there?" or simply \Hello?".
The second and third condition check that nothing is on the agenda or in next moves.
The motivation for this is that there is no reason to address contact explicitly in this case,
since any utterance from the system implicitly tries to establish contact.
Default ICM integration rule Since contact is not explicitly represented in the infor-
mation state proper, integration of negative system contact ICM moves have no speciflc
efiect on the information state, and are therefore integrated by the default ICM integration
rule shown in (rule 3.10). Unless an ICM move has a speciflc integration rule deflned for
```

**Context After:**
> it, it will be integrated by this rule....

---

## Algorithm 64: rule 3 .10). Unless an ICM move has a speciflc integration rule deflned for

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 119
**Page:** 142

**Context Before:**
> that nothing is on the agenda or in next moves.
The motivation for this is that there is no reason to address contact explicitly in this case,
since any utterance from the system implicitly tries to e...

**Algorithm:**

```
rule 3.10). Unless an ICM move has a speciflc integration rule deflned for
it, it will be integrated by this rule.
```

---

## Algorithm 65: rule 3 .10) rule: integrateOtherICM

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 121
**Page:** 143

**Context Before:**
> 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 121
(...

**Algorithm:**

```
rule 3.10) rule: integrateOtherICM
class: integrate
pre: fst($/private/nim, icm:A)
n pop(/private/nim)
eff:
add(/shared/lu/moves, icm:A)
(
The condition and updates in this rule are straightforward.
Negative system perception feedback If the speech recognizer gets some input from
the user but is not able to reliably flgure out what was said (the recognition score may be
too low), the input variable gets set to ‘FAIL’. This will trigger negative perception ICM,
e.g. \I didn’t hear what you said".
(rule 3.11) rule: selectIcmPerNeg
```

**Context After:**
> class: select icm
$input=’FAIL’
pre:
not in($next moves, icm:per*neg)
(
eff: push(next moves, icm:per*neg)
n
The purpose of the second condition is to prevent selecting negative perception feedback
mo...

---

## Algorithm 66: rule 3 .11) rule: selectIcmPerNeg

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 121
**Page:** 143

**Context Before:**
> le 3.10) rule: integrateOtherICM
class: integrate
pre: fst($/private/nim, icm:A)
n pop(/private/nim)
eff:
add(/shared/lu/moves, icm:A)
(
The condition and updates in this rule are straightforward.
Neg...

**Algorithm:**

```
rule 3.11) rule: selectIcmPerNeg
class: select icm
$input=’FAIL’
pre:
not in($next moves, icm:per*neg)
(
eff: push(next moves, icm:per*neg)
n
The purpose of the second condition is to prevent selecting negative perception feedback
more than once in the selection phase. As with negative system contact feedback, negative
system perception feedback is integrated by the integrateOtherICM rule.
Negative understanding level feedback
Negative feedback can concern either of the two sublevels of the understanding level: se-
mantic and pragmatic understanding.
Negative system semantic understanding feedback If some input is recognized
by the recognition module, the interpretation module will try to flnd an interpretation
of the input. If this fails, the latest moves gets set to failed which triggers selection
of negative semantic understanding feedback (e.g. \I don’t understand"). In addition,
positive perception feedback (e.g. \I heard ‘perish’ ") is produced to indicate to the user
what the system thought she said.
```

---

## Algorithm 67: rule 3 .12) rule: selectIcmSemNeg

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 121
**Page:** 144

**Context Before:**
> 122 CHAPTER 3. GROUNDING ISSUES
This will only occur if the recognition lexicon covers sentences not covered by the inter-
pretation lexicon.
(...

**Algorithm:**

```
rule 3.12) rule: selectIcmSemNeg
class: select icm
$latest moves=failed
pre: $input=String
8
>< not in($next moves, icm:sem*neg)
push(next moves, icm:per*pos:String)
eff:
>:
push(next moves, icm:sem*neg)
(
The purpose of the third condition is to prevent negative semantic understanding feedback
from being selected more than one time. Since only one string is recognized per turn,
there is never any reason to apply the rule more than once; and if anything at all can be
interpreted, the rule will not trigger at all even if some material was not used in interpreta-
tion. In a system with a wide-coverage recognizer and a more sophisticated interpretation
module, one may consider producing negative semantic understanding feedback for any
material which cannot be interpreted (e.g. \I understand that you want to go to Paris,
but I don’t understand what you mean by ‘Londres’.").
The flrst update in this rule selects positive perception ICM to show the user what the
system heard. The second update selects negative semantic understanding ICM.
Negative system pragmatic understanding feedback The system will try to inte-
grate the moves according to the rules above in Section 3.6.7. If this fails (if there are still
moves which have not been integrated), the rule in (rule 3.13) will be triggered and a
```

**Context After:**
> icm:und*neg-move will be selected by the system. However, if the reason that the move was
not integrated is that it had a low score or was not acceptable to the system, interrogative
understanding fee...

---

## Algorithm 68: rule 3 .13) will be triggered and a

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 121
**Page:** 144

**Context Before:**
> ted (e.g. \I understand that you want to go to Paris,
but I don’t understand what you mean by ‘Londres’.").
The flrst update in this rule selects positive perception ICM to show the user what the
syst...

**Algorithm:**

```
rule 3.13) will be triggered and a
icm:und*neg-move will be selected by the system. However, if the reason that the move was
not integrated is that it had a low score or was not acceptable to the system, interrogative
understanding feedback (Section 3.6.6) or negative acceptance feedback (Section 3.6.6),
respectively, will instead be selected and the move will be popped ofi nim before the rule
in (rule 3.13) is tried.
In IBiS, only ask-moves can be irrelevant. Other moves, including ask, do not have any
relevance requirements. This means that answer moves are the only moves that can fail
to be understood on the pragmatic level, given that they have been understood on the
semantic level. Also, for an utterance to be completely irrelevant, no part of it must have
been integrated. For these reasons, the rule in (rule 3.13) will trigger only if no move
```

**Context After:**
> in the latest utterance was integrated, and the utterance was interpreted as containing at
least one answer-move....

---

## Algorithm 69: rule 3 .13) is tried.

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 121
**Page:** 144

**Context Before:**
> ction 3.6.7. If this fails (if there are still
moves which have not been integrated), the rule in (rule 3.13) will be triggered and a
icm:und*neg-move will be selected by the system. However, if the r...

**Algorithm:**

```
rule 3.13) is tried.
In IBiS, only ask-moves can be irrelevant. Other moves, including ask, do not have any
relevance requirements. This means that answer moves are the only moves that can fail
to be understood on the pragmatic level, given that they have been understood on the
semantic level. Also, for an utterance to be completely irrelevant, no part of it must have
been integrated. For these reasons, the rule in (rule 3.13) will trigger only if no move
in the latest utterance was integrated, and the utterance was interpreted as containing at
least one answer-move.
```

---

## Algorithm 70: rule 3 .13) will trigger only if no move

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 121
**Page:** 144

**Context Before:**
> ill instead be selected and the move will be popped ofi nim before the rule
in (rule 3.13) is tried.
In IBiS, only ask-moves can be irrelevant. Other moves, including ask, do not have any
relevance re...

**Algorithm:**

```
rule 3.13) will trigger only if no move
in the latest utterance was integrated, and the utterance was interpreted as containing at
least one answer-move.
```

---

## Algorithm 71: rule 3 .13) rule: selectIcmUndNeg

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 123
**Page:** 145

**Context Before:**
> 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 123
(...

**Algorithm:**

```
rule 3.13) rule: selectIcmUndNeg
class: select icm
not in($next moves, icm:und*neg)
in($latest moves, answer(A))
8
pre:
>>>>>>>>< fora
$
l
/
l(
p
$
r
l
i
a
v
t
a
e
t
s
e
t
/n
m
im
ov
/e
e
l
s
e
/e
m
l
=
e
M
m=
ov
M
e)
ove,
forall($latest moves/elem=answer(A0),
>>>>>>>>:
fora
n
l
o
l
t
d
f
o
s
(
t
$
(
l
$
a
/s
t
h
e
a
st
re
m
d
o
/q
ve
u
s
d
/
,
e
D
le
)
m
an
=
d
M
$
o
d
v
o
e
m
,
ain :: relevant(A0, Q))
eff: push(next moves, icm:sem*pos:Move))
8
>< push(next moves, icm:und*neg)
>:
The flrst rule checks that negative pragmatic understanding feedback has not already been
selected. The second condition checks that the latest utterance contained an answer move,
and the third checks that none of the moves performed in the latest utterance has been
integrated; all moves in latest moves are still on nim. Finally, the fourth condition
checks that no answer is relevant to any question on QUD.
Theflrstupdateselectspositivefeedbackonthesemanticunderstandinglevelforeachmove
performed in the latest utterance, to show that the utterance was at least understood to
some extent. The second update selects negative feedback and pushes it on next moves.
The system is thus able to make a distinction between utterances it cannot interpret (and
thus not ground), and utterances that it can interpret and ground but not integrate. The
rule in (3.15) triggers when integration fails because the system cannot see the relevance
of the user utterance in the current dialogue context. Negative pragmatic understanding
feedback is currently realized as \I don’t quite understand"; the idea is to indicate that
the utterance was almost fully understood, but not quite. Again, it can be argued what
the best realization is.
Dialogue example: negative system contact, perception, and understanding
feedback In this dialogue, we see examples of negative system feedback on the contact,
perception, and understanding (both semantic and pragmatic) levels. (Since this dialogue
uses the text-based input module, we have simulated timeout and recognition failure.)
(dialogue 3.5)
S> Welcome to the travel agency!
U> ’TIMED_OUT’
```

---

## Algorithm 72: rule 3 .14) rule: rejectProp

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 127
**Page:** 149

**Context Before:**
> 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 127
(...

**Algorithm:**

```
rule 3.14) rule: rejectProp
class: select action
in($/private/nim, answer(A))
$/shared/lu/speaker=usr
8
pre:
>>>>>>>>< f
$
s
d
t(
o
$
m
/s
a
h
in
ar
::
ed
re
/
l
q
ev
u
a
d
n
,
t(
Q
A
)
, Q)
$domain :: combine(Q, A, P)
>>>>>>>>:
d
n
e
o
l
t
(/
$
p
d
r
a
i
t
v
a
a
b
t
a
e
s
/
e
ni
:
m
:
,
v
a
a
n
li
s
d
w
D
e
B
r(
p
A
a
)
r
)
ameter(P)
eff: push(/private/agenda, icm:und*pos:usr*P)
8
>< push(/private/agenda, icm:acc*neg:P)
>:
The flrst flve conditions are identical to those for the rule for integrating user answers,
integrateUsrAnswer (Section 3.6.6). The flnal condition checks that the proposition P,
resulting from combining a question on QUD with the content of the answer move, is not
a valid database parameter. The updates remove the move from nim and selects positive
understanding feedback to show what the system understood, and negative acceptance
feedback.
Of course, it is not optimally e–cient that the same sequence of conditions is checked by
several difierent rules; an alternative approach would be to let one rule determine e.g. how
an answer move is relevant, combine it with a question on QUD, and store the result in
a datastructure containing pragmatically interpreted material. This datastructure could
then be inspected by both integration and rejection rules. (See also Section 6.5.1.)
Dialogue example: system proposition rejection In the following dialogue, we il-
lustrate system rejection of the proposition that the means of transport to search for will
be train. A motivation is also given by the system, i.e. that \train" is not available as a
means of transport in the database.
(dialogue 3.8)
S> Okay. I need some information. How do you want to travel?
getLatestMoves
integrateOtherICM
integrateOtherICM
integrateSysAsk
U> train please
```

---

## Algorithm 73: rule 3 .15) rule: rejectIssue

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 129
**Page:** 151

**Context Before:**
> 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 129
In case the system has interpreted a user utterance as an ask-move with content q, but the
system does not have a plan for dealing with q, the syste...

**Algorithm:**

```
rule 3.15) rule: rejectIssue
class: select action
in($/private/nim, ask(Q))
pre: $/shared/lu/speaker=usr
8
>< not $domain :: plan(Q, Plan)
del(/private/nim, ask(Q))
>:
eff: push(/private/agenda, icm:und*pos:usr*issue(Q))
8
>< push(/private/agenda, icm:acc*neg:issue(Q))
>:
The rule is similar to the rejectProp rule. The third condition checks that there is no
plan for dealing with the question Q.
Dialogue example: system issue rejection In the following dialogue, the user’s re-
quest for information about connecting (cid:176)ights is rejected on the grounds that the system
does not know how to address that issue.
(dialogue 3.9)
S> Okay. The price is 123 crowns.
U> what about connecting flights
getLatestMoves
backupShared
rejectIssue
del(/private/nim, ask(?A.con (cid:176)ight(A)))
push(/private/agenda, )
8
push(/private/agenda, icm:acc*neg:issue(?A.con (cid:176)ight(A)))
<
selectIcmOther
: push(next moves, icm:und*pos:usr*issue(?A.con (cid:176)ight(A)))
del(/private/agenda, icm:und*pos:usr*issue(?A.con (cid:176)ight(A)))
‰
selectIcmOther
push(next moves, icm:acc*neg:issue(?A.con (cid:176)ight(A)))
del(/private/agenda, icm:acc*neg:issue(?A.con (cid:176)ight(A)))
‰
S> You asked about connecting flights. Sorry, I cannot answer questions
```

---

## Algorithm 74: rule 3 .16).

**Section:** 3.6.7 Grounding of system utterances in IBiS2
**Page:** 152

**Context Before:**
> has been implemented in IBiS2. We flrst present basic update rules re(cid:176)ecting the
cautious strategy. We then present integration rules for the \core" system dialogue moves
(ask and answer), and...

**Algorithm:**

```
rule 3.16).
(rule 3.16) rule: getLatestMoves
class: grounding
$latest moves=Moves
pre: $latest speaker=DP
8
>< $/shared/lu/moves=PrevMoves
set(/private/nim, Moves)
>:
set(/shared/lu/speaker, DP)
eff: 8
>>>< clear(/shared/lu/moves)
set(/shared/pm, PrevMoves)
>>>:
The rule loads information regarding the latest utterance performed into nim and copies
the previously grounded moves (in /shared/lu/moves) to the /shared/pm fleld. Note
that this rule has changed signiflcantly compared to IBiS1; no optimistic assumption
about understanding of the latest utterance is made here. Instead of putting the latest
moves in /shared/lu/moves, which would be to assume that they have been mutually
```

---

## Algorithm 75: rule 3 .16) rule: getLatestMoves

**Section:** 3.6.7 Grounding of system utterances in IBiS2
**Page:** 152

**Context Before:**
> emented in IBiS2. We flrst present basic update rules re(cid:176)ecting the
cautious strategy. We then present integration rules for the \core" system dialogue moves
(ask and answer), and describe the...

**Algorithm:**

```
rule 3.16) rule: getLatestMoves
class: grounding
$latest moves=Moves
pre: $latest speaker=DP
8
>< $/shared/lu/moves=PrevMoves
set(/private/nim, Moves)
>:
set(/shared/lu/speaker, DP)
eff: 8
>>>< clear(/shared/lu/moves)
set(/shared/pm, PrevMoves)
>>>:
The rule loads information regarding the latest utterance performed into nim and copies
the previously grounded moves (in /shared/lu/moves) to the /shared/pm fleld. Note
that this rule has changed signiflcantly compared to IBiS1; no optimistic assumption
about understanding of the latest utterance is made here. Instead of putting the latest
moves in /shared/lu/moves, which would be to assume that they have been mutually
```

---

## Algorithm 76: rule 3 .17) copies relevant parts of the IS to the

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 131
**Page:** 153

**Context Before:**
> 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 131
understood, IBiS2 clears /shared/lu/moves so that moves can be added when they are
actually integrated; only then are they assumed to be understood....

**Algorithm:**

```
rule 3.17) copies relevant parts of the IS to the
tmp fleld. This makes it possible to backtrack to a previous state, should the optimistic
grounding assumptions concerning a system move turn out to be mistaken. This means
thatanyoptimisticupdatesassociatedwithintegrationofsystemmovesarenowcautiously
optimistic.
(rule 3.17) rule: backupShared
class: none
pre: f
/private/tmp/qud := $/shared/qud
/private/tmp/com := $/shared/com
eff: 8
>>>< /private/tmp/agenda := $/private/agenda
/private/tmp/plan := $/private/plan
>>>:
There are no conditions on this rule. It is executed at the start of the selection algorithm
described in Section 3.7, and is thus only called before system utterances.
Cautiously optimistic integration of system moves
For system ask and answer moves, the integration rules are similar to those in IBiS1;
however, rather than picking out moves from /shared/lu/moves, IBiS2 picks moves
from /private/nim and adds them to /shared/lu/moves, thereby assuming grounding
ontheunderstandinglevel, onlyinconnectionwithintegration. Sinceoptimisticgrounding
is assumed for system moves, it would be okay to handle them the same way we did
in IBiS1; however, user moves are no longer (always) optimistically grounded, and we
have chosen to give a uniform treatment to all moves. Since in IBiS system moves are
always successfully integrated, however, there is no real difierence between the way they
are handled in IBiS1 and IBiS2.
```

---

## Algorithm 77: rule 3 .17) rule: backupShared

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 131
**Page:** 153

**Context Before:**
> ly integrated; only then are they assumed to be understood.
Saving previous state before integration Before selecting, producing, and integrat-
ing a new system utterance, the rule in (rule 3.17) copi...

**Algorithm:**

```
rule 3.17) rule: backupShared
class: none
pre: f
/private/tmp/qud := $/shared/qud
/private/tmp/com := $/shared/com
eff: 8
>>>< /private/tmp/agenda := $/private/agenda
/private/tmp/plan := $/private/plan
>>>:
There are no conditions on this rule. It is executed at the start of the selection algorithm
described in Section 3.7, and is thus only called before system utterances.
Cautiously optimistic integration of system moves
For system ask and answer moves, the integration rules are similar to those in IBiS1;
however, rather than picking out moves from /shared/lu/moves, IBiS2 picks moves
from /private/nim and adds them to /shared/lu/moves, thereby assuming grounding
ontheunderstandinglevel, onlyinconnectionwithintegration. Sinceoptimisticgrounding
is assumed for system moves, it would be okay to handle them the same way we did
in IBiS1; however, user moves are no longer (always) optimistically grounded, and we
have chosen to give a uniform treatment to all moves. Since in IBiS system moves are
always successfully integrated, however, there is no real difierence between the way they
are handled in IBiS1 and IBiS2.
```

---

## Algorithm 78: rule 3 .18) rule: integrateSysAsk

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 131
**Page:** 154

**Context Before:**
> 132 CHAPTER 3. GROUNDING ISSUES
(...

**Algorithm:**

```
rule 3.18) rule: integrateSysAsk
class: integrate
$/shared/lu/speaker==sys
pre:
fst($/private/nim, ask(A))
(
pop(/private/nim)
eff: add(/shared/lu/moves, ask(A))
8
>< push(/shared/qud, A)
>:
(rule 3.19) rule: integrateSysAnswer
```

**Context After:**
> class: integrate
fst($/private/nim, answer(A))
$/shared/lu/speaker==sys
8
pre: >>>>>><
f
$
s
d
t(
o
$
m
/s
a
h
in
ar
::
ed
pr
/
o
q
p
u
o
d
si
,
ti
B
on
)
(A)
$domain :: relevant(A, B)
>>>>>>:
pop(/pr...

---

## Algorithm 79: rule 3 .19) rule: integrateSysAnswer

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 131
**Page:** 154

**Context Before:**
> 132 CHAPTER 3. GROUNDING ISSUES
(rule 3.18) rule: integrateSysAsk
class: integrate
$/shared/lu/speaker==sys
pre:
fst($/private/nim, ask(A))
(
pop(/private/nim)
eff: add(/shared/lu/moves, ask(A))
8
>< ...

**Algorithm:**

```
rule 3.19) rule: integrateSysAnswer
class: integrate
fst($/private/nim, answer(A))
$/shared/lu/speaker==sys
8
pre: >>>>>><
f
$
s
d
t(
o
$
m
/s
a
h
in
ar
::
ed
pr
/
o
q
p
u
o
d
si
,
ti
B
on
)
(A)
$domain :: relevant(A, B)
>>>>>>:
pop(/private/nim)
eff: add(/shared/lu/moves, answer(A))
8
>< add(/shared/com, A)
>:
One complication is that in IBiS2, several moves may be performed in a single utter-
ance. To keep track of which utterances have been integrated, the /private/nim stack
of non-integrated moves is popped for each move that gets integrated. Note also that
each integrated (and thus understood) move is added to /shared/lu/moves (whereas in
IBiS1 this was done at the start of the update cycle).
The cautiously optimistic acceptance assumptions built into these rules can be retracted
on integration of negative user perception feedback, as explained in Section 3.6.6, or on
negative user integration feedback, as show in Section 3.6.7. Dialogue examples involving
the rules shown above will be given in these sections.
User feedback to system utterances
In this section we review user feedback to system utterances and how these afiect the
optimistic grounding assumptions.
Negative user perception feedback If the system makes an utterance, it will assume
itisgroundedandaccepted. Iftheuserindicatesthatshedidnotunderstandtheutterance,
the rule in (rule 3.20) makes it possible to retract the efiects of the system’s latest move,
```

**Context After:**
> thus cancelling the assumptions of grounding and acceptance....

---

## Algorithm 80: rule 3 .20) makes it possible to retract the efiects of the system’s latest move,

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 131
**Page:** 154

**Context Before:**
> in Section 3.6.6, or on
negative user integration feedback, as show in Section 3.6.7. Dialogue examples involving
the rules shown above will be given in these sections.
User feedback to system utteran...

**Algorithm:**

```
rule 3.20) makes it possible to retract the efiects of the system’s latest move,
thus cancelling the assumptions of grounding and acceptance.
```

---

## Algorithm 81: rule 3 .20) rule: integrateUsrPerNegICM

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 133
**Page:** 155

**Context Before:**
> 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 133
(...

**Algorithm:**

```
rule 3.20) rule: integrateUsrPerNegICM
class: integrate
$/shared/lu/speaker==usr
pre:
fst($/private/nim, icm:per*neg)
(
pop(/private/nim)
/shared/qud := $/private/tmp/qud
8
eff: >>>>>>< /
/
s
p
h
r
a
iv
r
a
e
t
d
e
/
/
c
a
o
g
m
en
:=
da
$/
:=
pr
$
i
/
v
p
a
r
t
i
e
v
/
a
t
t
m
e
p
/t
/c
m
o
p
m
/agenda
/private/plan := $/private/tmp/plan
>>>>>>:
The four last updates revert the com, qud, plan and agenda flelds to the values stored
in /private/tmp.
Dialogue example: negative user perception feedback This dialogue shows how
IBiS2 is able to react to negative user perception feedback (e.g. \pardon") by retracting
theoptimisticgroundingassumptionbybacktrackingrelevantpartsof sharedtothestate
in /private/tmp/sys, stored before the system utterance was generated. Also, the plan
and agenda are backtracked to enable the system to continue the dialogue properly.
(dialogue 3.10)
S>Okay. You asked about price. I need some information. How do you want
to travel?
getLatestMoves
integrateOtherICM
integrateOtherICM
integrateOtherICM
integrateSysAsk
```

---

## Algorithm 82: rule 3 .21) allows the user to reject a system

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 135
**Page:** 157

**Context Before:**
> 6 consultDB(?H.price(H)) 7 7
6 6 7 7
6 6 bel = fg 7 7
6 6 7 7
6 6 tmp = ::: 7 7
6 6 7 7
6 6 nim = hhii 7 7
6 6 7 7
6 4 com = fg 5 7
6 7
6 qud = ?A.price(A) 7
6 2 3 7
6 shared = speaker = usr 7
6 lu = ...

**Algorithm:**

```
rule 3.21) allows the user to reject a system
question (by indicating inability to answer, i.e. by uttering \I don’t know" or similar). If
this is done, the optimistic grounding update is retracted by restoring the shared parts
stored in nim, i.e. qud and com, to their previous states.
(rule 3.21) rule: integrateUsrAccNegICM
class: integrate
$/shared/lu/speaker==usr
pre: fst($/private/nim, icm:acc*neg:issue)
8
>< in($/shared/pm, ask(Q))
pop(/private/nim)
>:
add(/shared/lu/moves, icm:acc*neg:issue)
eff: 8
>>>< /shared/qud := $/private/tmp/qud
/shared/com := $/private/tmp/com
>>>:
```

---

## Algorithm 83: rule 3 .21) rule: integrateUsrAccNegICM

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 135
**Page:** 157

**Context Before:**
> 5
backupShared
selectFromPlan
selectIcmOther
selectIcmOther
selectIcmOther
selectAsk
S>Okay. You asked about price. I need some information. How do you want
to travel?
Explicit user issue rejection Th...

**Algorithm:**

```
rule 3.21) rule: integrateUsrAccNegICM
class: integrate
$/shared/lu/speaker==usr
pre: fst($/private/nim, icm:acc*neg:issue)
8
>< in($/shared/pm, ask(Q))
pop(/private/nim)
>:
add(/shared/lu/moves, icm:acc*neg:issue)
eff: 8
>>>< /shared/qud := $/private/tmp/qud
/shared/com := $/private/tmp/com
>>>:
```

---

## Algorithm 84: rule 3 .22) rule: irrelevantFollowup

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 141
**Page:** 163

**Context Before:**
> followups to system ask moves as implicit
rejections. However, this choice is not obvious and is a further topic for future research.
Implicit user rejection of issue
If an irrelevant followup is dete...

**Algorithm:**

```
rule 3.22) rule: irrelevantFollowup
class: none
1 $/private/nim=Moves
2 $/shared/lu/speaker==usr
8
pre:
>>>>>>>>>>>>><
5
4
3
P
i
n
n
o
r
(
t
$
e
/
v
A
s
M
/
h
e
a
o
l
v
r
e
e
e
m
=
d
=
a
/
s
i
p
k
c
m
m
(Q
,
:
)
P
o
r
r
evMove)
( PrevMove=icm:und*int:DP*C and Q=und(DP*C) )
eff:
>>>>>>>>>>>>>:
/
7
6
s
n
n
h
o
o
a
t
t
r
A
M
ed
/
o
e
/
v
l
q
e
e
u
s
m
/
d
e
=
:
l
=
a
e
n
m
s
$
w
=
/p
e
a
r
r
s
(
k
i
A
v
(
)
Q
at
a
0)
n
e
d
a
/
n
t
$
d
m
d
p
$
o
/
d
m
q
o
a
u
m
i
d
n
ai
:
n
: r
::
el
d
ev
e
a
p
n
e
t
n
(
d
A
s
,
(Q
Q
,
)
Q0)
/shared/com := $/private/tmp/com
(
(Sincethisruleiscalled\byname"fromtheupdatealgorithm,thereisnoneedforincluding
it in a rule class.) Condition 3 checks that no ICM was included in the latest move.
Condition 4 and 5 tries to flnd a question Q raised by the previous move, possibly an
understanding-question. Note here that we do not check QUD; in IBiS2, questions remain
on QUD only for one turn but it may be the case that we want questions to remain on
QUD over several turns. What we are interested here is thus not which questions are on
QUD but which questions were raised by the previous utterance, and this is the reason
for looking in pm rather than qud. Conditions 6 and 7 check that no move performed in
the latest utterance is relevant to Q, neither by answering it nor by asking a question on
which Q depends. The updates are similar to those for integration of negative acceptance
feedback (Section 3.6.7).
```

---

## Algorithm 85: rule 3 .23) rule: flndPlan

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 143
**Page:** 165

**Context Before:**
> 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 143
(...

**Algorithm:**

```
rule 3.23) rule: flndPlan
class: load plan
in($/private/agenda, respond(Q))
pre: $domain :: plan(Q, Plan)
8
>< not in($/private/bel, P) and $domain :: resolves(P, Q)
del(/private/agenda, respond(Q))
>:
eff: set(/private/plan, Plan)
8
>< push(/private/agenda, icm:loadplan))
>:
This rule is identical to that in IBiS1 (Section 2.8.6), expect for the flnal update which
pushes the icm:loadplan move on the agenda.
Reraising issues
System reraising of issue associated with plan If the user raises a question Q and
then raises Q0 before Q has been resolved, the system should return to dealing with Q once
Q0 is resolved; this was described in Section 3.6.9. The recoverPlan rule in IBiS2, shown
in (3.20), is almost identical to the one in IBiS1, except that ICM is produced to indicate
that an issue (q1) is being reraised. This ICM is formalized as icm:reraise:q where q is the
question being reraised, and expressed e.g. as \Returning to the issue of price".
(rule 3.24) rule: recoverPlan
```

**Context After:**
> class: load plan
in($/shared/qud, Q)
is empty($/private/agenda)
8
pre: >>>>>>< i
$
s
d
e
o
m
m
p
a
t
i
y
n
($
:
/
:
p
p
r
la
iv
n
a
(Q
te
,
/
P
p
l
l
a
a
n
n
)
)
not in($/private/bel, P) and $domain :...

---

## Algorithm 86: rule 3 .24) rule: recoverPlan

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 143
**Page:** 165

**Context Before:**
> ated with plan If the user raises a question Q and
then raises Q0 before Q has been resolved, the system should return to dealing with Q once
Q0 is resolved; this was described in Section 3.6.9. The r...

**Algorithm:**

```
rule 3.24) rule: recoverPlan
class: load plan
in($/shared/qud, Q)
is empty($/private/agenda)
8
pre: >>>>>>< i
$
s
d
e
o
m
m
p
a
t
i
y
n
($
:
/
:
p
p
r
la
iv
n
a
(Q
te
,
/
P
p
l
l
a
a
n
n
)
)
not in($/private/bel, P) and $domain :: resolves(P, Q)
>>>>>>:
set(/private/plan, Plan)
eff: push(/private/agenda, icm:reraise:Q)
8
>< push(/private/agenda, icm:loadplan))
>:
Issuereraising byuser Inthecasewheretheuserreraisesanopenissue,anicm:reraise:Q
move is selected by the integrateUsrAsk described in Section 3.6.6.
System reraising of issue not associated with plan The IBiS1 reraiseIssue rule
described in Section 2.12.3 reraises any questions on QUD which are not associated with
```

---

## Algorithm 87: rule 3 .25) rule: reraiseIssue

**Section:** 3.6. FEEDBACK AND GROUNDING STRATEGIES FOR IBIS 143
**Page:** 166

**Context Before:**
> 144 CHAPTER 3. GROUNDING ISSUES
any plan (i.e. which have been raised previously by the system). In this case it is again
helpful to indicate that the system is aware that the issue is being reraised....

**Algorithm:**

```
rule 3.25) rule: reraiseIssue
class: select action
fst($/shared/issues, Q)
pre:
not $domain :: plan(Q, P)
(
push(/private/agenda, icm:reraise)
eff:
push(/private/agenda, raise(Q))
(
The conditions of this rule checks that there is a question Q on issues for which the system
has no plan, i.e. one that the system needs to ask the user.
The flrst update adds an icm:reraise (without an argument) to signal that it is reraising
a question; this is currently generated as preflxing \so" to the next ask move, which is
an ordinary raising of the question (placed on the agenda by the second update in the
rule). In a more sophisticated implementation one could consider abbreviating the original
raising of the question to make an appropriate reraising, e.g. \So, from what city?" But
we do not have a general method for doing that yet, even in these simple dialogues. To
do it properly would probably require more detailed syntactic and semantic analysis of
contributions than we currently have in IBiS.
Dialogue example: user and system reraising (dialogue 3.12) is an example of a
dialogue where the user reraises an issue which was previously raised but not resolved.
Also subsequently the system reraises an issue which is relevant for addressing the issue
that the user reraised. In order to address the issue of price the system needs to get
information from the user concerning where she wishes to travel from.
(dialogue 3.12)
S> Welcome to the travel agency!
U> price information please
S> Okay. Lets see. How do you want to travel?
U> a flight
S> Okay. What city do you want to go to?
U> paris
S> Okay. What city do you want to go from?
```

---

## Algorithm 88: rule 3 .26), does not require the agenda

**Section:** 3.7.2 Selection module
**Page:** 168

**Context Before:**
> grate all
moves in /private/nim. If the user asked a question, the appropriate plan will be loaded
by line 5. Any loaded plan is executed by applying the exec plan rule class until no more
execution i...

**Algorithm:**

```
rule 3.26), does not require the agenda
to be empty, but only that the respond action has not already been selected, and thus it
allows several moves to be selected per turn.
```

---

## Algorithm 89: rule 3 .26) rule: selectRespond

**Section:** 3.7. FURTHER IMPLEMENTATION ISSUES 147
**Page:** 169

**Context Before:**
> 3.7. FURTHER IMPLEMENTATION ISSUES 147
(...

**Algorithm:**

```
rule 3.26) rule: selectRespond
class: select action
is empty($/private/plan)
fst($/shared/qud, A)
8
pre:
>>>>>>>>< i
n
n
o
(
t
$/
in
p
(
r
$
i
/
v
s
a
h
t
a
e
r
/
e
b
d
e
/
l
c
,
o
B
m
)
, B)
$domain :: resolves(B, A)
eff:
>>>>>>>>:
p
n
u
o
s
t
h
i
(
n
/
(
p
$
r
/
i
p
v
r
a
i
t
v
e
a
/
t
a
e
g
/
e
a
n
g
d
e
a
n
,
d
r
a
e
,
sp
re
o
s
n
p
d
o
(
n
A
d
)
(
)
A))
n
Similarly, the move selection rules in IBiS2 are repeatedly applied, popping actions ofi the
agenda queue and pushing the corresponding moves on next moves. As an example,
the selectAnswer rule is shown in (rule 3.27).
```

**Context After:**
> (rule 3.27) rule: selectAnswer
class: select move
fst($/private/agenda, respond(A))
in($/private/bel, B)
pre: 8
>>>< not in($/shared/com, B)
$domain :: resolves(B, A)
eff:
>>>:
push(next moves, answer...

---

## Algorithm 90: rule 3 .27).

**Section:** 3.7. FURTHER IMPLEMENTATION ISSUES 147
**Page:** 169

**Context Before:**
> /plan)
fst($/shared/qud, A)
8
pre:
>>>>>>>>< i
n
n
o
(
t
$/
in
p
(
r
$
i
/
v
s
a
h
t
a
e
r
/
e
b
d
e
/
l
c
,
o
B
m
)
, B)
$domain :: resolves(B, A)
eff:
>>>>>>>>:
p
n
u
o
s
t
h
i
(
n
/
(
p
$
r
/
i
p
v...

**Algorithm:**

```
rule 3.27).
(rule 3.27) rule: selectAnswer
class: select move
fst($/private/agenda, respond(A))
in($/private/bel, B)
pre: 8
>>>< not in($/shared/com, B)
$domain :: resolves(B, A)
eff:
>>>:
push(next moves, answer(B))
pop(/private/agenda)
(
The selection algorithm for IBiS2 is shown in (3.21).
(3.21) h backupShared,
if not in($/private/agenda, A) and q raising action(A)
then try select action,
repeat ( select icm orelse select move ) i
The select action rule class selects actions and places them on the agenda, whereas
the select move and select icm rule classes selects agenda items and places them on
next moves. Before selection, the backupShared (Section 3.6.7) is applied to copy
relevant parts of the information state to /private/nim.
The basic strategy for selection in IBiS is that only one question should be raised by the
system in each utterance. The IBiS2 selection algorithm flrst checks if some question-
raising action is already on the agenda; if not, it tries to select a new action. Then, it
selects moves and ICM repeatedly until nothing more can be selected.
```

---

## Algorithm 91: rule 3 .27) rule: selectAnswer

**Section:** 3.7. FURTHER IMPLEMENTATION ISSUES 147
**Page:** 169

**Context Before:**
> shared/qud, A)
8
pre:
>>>>>>>>< i
n
n
o
(
t
$/
in
p
(
r
$
i
/
v
s
a
h
t
a
e
r
/
e
b
d
e
/
l
c
,
o
B
m
)
, B)
$domain :: resolves(B, A)
eff:
>>>>>>>>:
p
n
u
o
s
t
h
i
(
n
/
(
p
$
r
/
i
p
v
r
a
i
t
v
e
...

**Algorithm:**

```
rule 3.27) rule: selectAnswer
class: select move
fst($/private/agenda, respond(A))
in($/private/bel, B)
pre: 8
>>>< not in($/shared/com, B)
$domain :: resolves(B, A)
eff:
>>>:
push(next moves, answer(B))
pop(/private/agenda)
(
The selection algorithm for IBiS2 is shown in (3.21).
(3.21) h backupShared,
if not in($/private/agenda, A) and q raising action(A)
then try select action,
repeat ( select icm orelse select move ) i
The select action rule class selects actions and places them on the agenda, whereas
the select move and select icm rule classes selects agenda items and places them on
next moves. Before selection, the backupShared (Section 3.6.7) is applied to copy
relevant parts of the information state to /private/nim.
The basic strategy for selection in IBiS is that only one question should be raised by the
system in each utterance. The IBiS2 selection algorithm flrst checks if some question-
raising action is already on the agenda; if not, it tries to select a new action. Then, it
selects moves and ICM repeatedly until nothing more can be selected.
```

---

## Algorithm 92: rule 4 .1) flrst checks whether a question which

**Section:** 4.6.1 Issue accommodation: from dialogue plan to ISSUES
**Page:** 187

**Context Before:**
> 9 *2 (cid:27) :; &=
KE MO N
KE MO NS R !$ UV *X W2 (cid:25)Y ,
(cid:30)(cid:5) (cid:25)Y :d &) ((cid:9)*2 (cid:27)(cid:26) , (cid:30)(cid:5) (cid:25)Y :d &) ((cid:9)*2 (cid:27)(cid:26) ,
*X W2 (cid:25...

**Algorithm:**

```
rule 4.1) flrst checks whether a question which
matches the answer occurs in the current dialogue plan (provided there is one). A question
matches an answer if the answer is relevant to, or (in Ginzburg’s terminology) about the
question. If such a question can be found, it can be assumed that this is now an open
issue. Accommodating this amounts to pushing the question on the ISSUES stack.
5Since the current plan is presumably being carried out in order to deal with some open issue, we may
regard the utterance as indirectly relevant to some open issue (via the plan).
```

---

## Algorithm 93: rule 4 .1) rule: accommodatePlan2Issues

**Section:** 4.6.1 Issue accommodation: from dialogue plan to ISSUES
**Page:** 188

**Context Before:**
> 166 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(...

**Algorithm:**

```
rule 4.1) rule: accommodatePlan2Issues
class: accommodate
$/private/nim/elem/snd = answer(A)
not $lexicon :: yn answer(A)
8
pre:
>>>>>>>>>>>>><
$
$
in
d
d
(
o
o
$/
m
m
p
a
a
r
i
i
i
n
n
va
:
:
:
:
te
d
re
/
e
l
f
p
e
a
v
l
u
a
a
l
n
t
n
t
,
q
(A
u
fl
e
n
,
s
d
Q
t
o
io
)
u
n
t(
(
Q
Q
)
)
)
or
not ( in($/private/plan, flndout(Q0))
eff:
>>>>>>>>>>>>>:
push(/sha
a
a
r
n
n
e
d
d
d
Q
$
/
d
i
6=
s
o
s
m
u
C
a
e
i
s
n
, B
::
)
relevant(A, Q0) )
n
The flrst condition picks out a non-integrated answer move with content A. The second
condition checks that A is not a y/n answer (e.g. yes, no, maybe etc.), and thus im-
plements an assumption that such answers cannot trigger question accommodation, since
they are too ambiguous6. The third and fourth conditions check if there is a flndout action
with content Q in the currently loaded plan, such that A is relevant to Q. The flnal con-
dition checks that there is no other question in the plan that the answer is relevant to, or
alternatively that Q has the status of a default question. If this condition does not hold, a
clariflcation question should be raised by the system; this is described in Section 4.6.3. The
\default question" option allows encoding of the fact that one issue may be signiflcantly
more salient in a certain domain. For example, in a travel agency setting the destination
city may be regarded as more salient than the departure city question. If this is encoded
as a default question, then if the user says simply \Paris" it is interpreted as answering
the destination city question; no clariflcation is triggered7
Example dialogue: issue accommodation The dialogue in (dialogue 4.1) illus-
trates accommodation of the question ?C.class(C) from the plan to the stack of open
issues.
(dialogue 4.1)
6However,ingeneralonecannotruleoutthepossibilitythaty/n answerscantriggeraccommodationin
severelyrestricteddomains. Theassumptionthatthiscannothappencanberegardedasaverysimplifled
version of a constraint on the number of questions which an answer may be relevant without making
question accommodation infeasible.
7The normal grounding mechanisms should of course enable correction of this assumption. In IBiS3
the choice of grounding strategy depends solely on the recognition score which means that a high-scoring
answermaybeinterpretedasananswertoadefaultquestionandnotreceiveanyexplicitfeedback. Thisis
onecasewhichindicatesaneedfortakingmorefactorsintoaccountwhenchoosingfeedbackandgrounding
strategy.
```

---

## Algorithm 94: Procedure/Rule in 4.6.2 Local question accommodation: from ISSUES to QUD

**Section:** 4.6.2 Local question accommodation: from ISSUES to QUD
**Page:** 190

**Algorithm:**

```
168 CHAPTER 4. ADDRESSING UNRAISED ISSUES
agenda = icm:acc*pos
flndout(?A.dept day(A))
2 2 plan = ›› fifi 3 3
private = consultDB(?B.price(B))
¿ (cid:192)
6 6 bel = fg 7 7
6 6 7 7
6 6 nim = hhii 7 7
6 6 7 7
6 4 class(economy) 5 7
6 7
6 month(april) 7
6 2 8 9 3 7
6
6
6 6
com = >>>><
d
d
e
e
p
st
t
c
c
i
i
t
t
y
y
(
(
p
lo
a
n
ri
d
s
o
)
n)
>>>>=
7
7
7
7
6 6 7 7
6 6 how(plane) 7 7
6 6
6
6
shared = 6 6
6
6
i
q
s
u
su
d
es
=
=
h
>>>>:i ?D.price(D) >>>>; 7 7
7
7
7 7
7
7
6 6 › fi 7 7
6 6 pm = icm:acc*pos, icm:loadplan, ask(?C.month(C)) 7 7
6 6 7 7
6 6 speaker = usr 7 7
6 6 ›› fifi 7 7
6 6 lu = moves = answer(april), answer(class(economy)) 7 7
6 6 2 3 7 7
6 6 score = 1 7 7
6 6 ›› fifi 7 7
4 4 4 5 5 5
S> Okay. What day do you want to leave?
4.6.2 Local question accommodation: from ISSUES to QUD
If a move with underspecifled content is made which does not match any question on the
QUD, the closest place to look for such a question is ISSUES, and if it can be found there
it should be pushed on the local QUD to enable ellipsis resolution. As a side-efiect, the
question has now been brought into focus and should, if it is not topmost on the open
issues stack, be raised to the top of open issues. A schematic overview of local question
accommodation is shown in Figure 4.3.
(cid:0)(cid:1)
(cid:1)
(cid:1) (cid:1)
(cid:1) (cid:1)
(cid:1)
(cid:1)
(cid:1) (cid:1) (cid:1) (cid:1)
(cid:1)
(cid:1)
(cid:1) (cid:1) (cid:1) (cid:1)
(cid:2)
(cid:3)(cid:5)
I>
(cid:4)(cid:7)
^
(cid:6)(cid:9)(cid:8)(cid:11)
(cid:10)(cid:18) (cid:4)(cid:7)
(cid:10)(cid:11) (cid:12)(cid:14)
(cid:13)(cid:5)
(cid:13)
(cid:20)
(cid:15)
(cid:15)
(cid:0)(cid:1)
(cid:1)
(cid:1) (cid:1)
(cid:1) (cid:1)
(cid:2)
(cid:0)(cid:1)
(cid:1)
(cid:1) (cid:1) (cid:1) (cid:1)
(cid:2)
(cid:10)(cid:17) (cid:16)(cid:18) (cid:13)(cid:5)
(cid:3) -" (cid:10)(cid:17)
?(cid:14) (cid:13)(cid:5) -
(cid:12)(cid:7) DE (cid:3) (cid:19)(cid:18) (cid:6)T D
_a ‘ D
(cid:6) IY I(cid:31) G e (cid:20)
G
(cid:3)(cid:26) D
-
G
(cid:19)(cid:17)
(cid:19)
(cid:13)
(cid:20)(cid:7)
I
(cid:10)
(cid:15)b
(cid:15)@ (cid:15)@
(cid:15)@
(cid:15)
(cid:15)(cid:22)
(cid:15)(cid:22)
(cid:15)@
(cid:15) (cid:15)(cid:22)
.A
(cid:21)(cid:24) (cid:21)(cid:24)
(cid:21)(cid:24)
F
(cid:21)(cid:24) (cid:23)(cid:26) (cid:25)(cid:28) (cid:27)(cid:14) (cid:29)(cid:24) (cid:30)(cid:5) (cid:25)(cid:31) (cid:30) (cid:25)"
(cid:21)(cid:24) (cid:23)(cid:26) (cid:25)(cid:28) (cid:27)(cid:26) ./ &1 02 %1 3(cid:7) !$
.A (cid:25)> &B !$ 4C <= *" (cid:23)(cid:26) ,
(cid:4) (cid:15)L
FH GJ I (cid:15)L I’ PQ I (cid:21)(cid:24) (cid:23)(cid:26) (cid:25)(cid:28) (cid:27)(cid:14) (cid:29)(cid:24) (cid:30)(cid:5) (cid:25)(cid:31) (cid:30) (cid:25)"
(cid:25)(cid:31) &Y !$ 4C <= *" (cid:23)(cid:26) ,
(cid:23)(cid:14) (cid:25)(cid:31) (cid:27)(cid:26) ./ &1 02 %1 3(cid:7) !c (cid:29)(cid:24) (cid:23)(cid:14) (cid:25)(cid:31) (cid:27)(cid:26) ./ &1 02 %1 3(cid:7) !c (cid:29)(cid:24)
(cid:23)(cid:14) (cid:25)(cid:31) (cid:27)(cid:14) (cid:29)(cid:24) (cid:30)(cid:5) (cid:25)(cid:28) (cid:30)(cid:5) (cid:25)" !f Ug
(cid:3) (cid:13)(cid:5) (cid:10)(cid:17) hQ (cid:13)(cid:5) (cid:4)
I
‘ D (cid:8)J (cid:13)
!$ #(cid:24) %’ &) (+*" (cid:27)(cid:26) ,
46 5702 (cid:27)(cid:14) 89 *2 (cid:27) :; &=
KE MO N
KE MO NS R !$ UV *X W2 (cid:25)Y ,
(cid:30)(cid:5) (cid:25)Y :d &) ((cid:9)*2 (cid:27)(cid:26) , (cid:30)(cid:5) (cid:25)Y :d &) ((cid:9)*2 (cid:27)(cid:26) ,
*X W2 (cid:25)B ,
(cid:15)b 4i 02 <; &) ((cid:9)%(cid:31)
(cid:15)@ .A (cid:25)(cid:31) &Y !f Ug
<) (cid:30)
((cid:9)(cid:23)
*X W2
%>
0j
(cid:25)B
&1
(cid:27)/
,
,
&
Z\[
[
[ [
[ [
]
R
Z\[
[
[ [ [ [
]
Z\[
[
[ [
[ [
[
[
[ [ [ [
[
[
[ [ [ [
]
Figure 4.3: Local question accommodation
This type of accommodation can e.g. occur if a question which was raised previously has
dropped ofi the local QUD but has not yet been resolved and remains on ISSUES. It should
also be noted that several accommodation steps can be taken during the processing of a
```

---

## Algorithm 95: rule 4 .2) rule: accommodateIssues2QUD

**Section:** 4.6.3 Issue clariflcation
**Page:** 191

**Context Before:**
> 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION169
single utterance; for example, if an issue that is in the plan but has not yet been raised is
answered elliptically.
(...

**Algorithm:**

```
rule 4.2) rule: accommodateIssues2QUD
class: accommodate
$/private/nim/elem=usr-answer(A)
$domain :: short answer(A)
8
pre:
>>>>>>>><
i
n
n
o
(
t
$/
$
s
l
h
e
a
x
r
ic
e
o
d
n
/i
:
s
:
su
yn
es
a
,
n
Q
sw
)
er(A)
not in($/shared/qud, Q)
eff:
>>>>>>>>:
p
$
u
d
s
o
h
m
(/
a
s
i
h
n
a
:
r
:
e
r
d
el
/
e
q
va
u
n
d
t
,
(A
Q
,
)
Q)
raise(/shared/issues, Q)
(
The second condition in (rule 4.2) checks that the content of the answer move picked out
```

**Context After:**
> by condition 1 is semantically underspecifled. The third condition imposes a constraint
on local question accommodation, excluding short answers to y/n-questions (\yes", \no",
\maybe" etc.). The remai...

---

## Algorithm 96: rule 4 .2) checks that the content of the answer move picked out

**Section:** 4.6.3 Issue clariflcation
**Page:** 191

**Context Before:**
> single utterance; for example, if an issue that is in the plan but has not yet been raised is
answered elliptically.
(rule 4.2) rule: accommodateIssues2QUD
class: accommodate
$/private/nim/elem=usr-an...

**Algorithm:**

```
rule 4.2) checks that the content of the answer move picked out
by condition 1 is semantically underspecifled. The third condition imposes a constraint
on local question accommodation, excluding short answers to y/n-questions (\yes", \no",
\maybe" etc.). The remaining conditions check that the answer-content is relevant to an
issue which is on issues but not on qud. The flrst operation pushes the accommodated
question on qud, and the flnal update raises the question to the top of the stack of open
issues.
```

**Context After:**
> 4.6.3 Issue clariflcation
In IBiS2, user answers are either pragmatically relevant to the question topmost on QUD,
or not relevant at all. When we add mechanisms of accommodation to allow for answers
...

---

## Algorithm 97: rule 4 .3).

**Section:** 4.6.3 Issue clariflcation
**Page:** 192

**Context Before:**
> will answer this question, which means that the ambiguous answer no longer needs to
be integrated and can be thrown away8.
In this way we see how question accommodation, amended with a mechanism for r...

**Algorithm:**

```
rule 4.3).
(rule 4.3) rule: clarifyIssue
class: select action
in($/private/nim, usr-answer(A))
setof(C, in($/private/plan, flndout(Q)) and
pre: 8
>>>< $domain :: relevant(A, Q), QSet)
$$arity(QSet) > 1
>>>: ! setof(?P, in(QSet, Q) and $domain :: combine(Q, A, P), AltQ)
eff: push(/private/agenda, flndout(AltQ))
8
>< del(/private/nim, usr-answer(A))
>:
The flrst condition picks out the answer-move from the nim queue. The second and third
conditions check that there is more than one question in the plan to which the answer
is relevant, by constructing the set of such questions. The flrst operation constructs the
alternative-question by applying each question in the set constructed in condition 2 to the
answer to get a proposition and preflxing the question operator ’?’ to each proposition
to get a y/n-question. The alternative question is this set of y/n-questions. The second
operation pushes the action to raise the alternative question on the agenda, and the flnal
operation removes the answer move from nim; this is motivated above.
A sample dialogue with issue clariflcation is shown in (dialogue 4.2).
(dialogue 4.2)
S> Welcome to the travel agency!
U> price information please
S> Okay. I need some information. How do you want to travel?
U> flight um paris
S> OK, by flight. Do you mean from paris or to paris?
8IBiS3onlyhandlesfullanswerstoclariflcationquestions,i.e. \ToParis." or\FromParis.". Aslightly
more advanced semantics would be required to handle cases where the user again gives an underspecifled
response which resolves the question, i.e. \To." or \From.".
```

---

## Algorithm 98: rule 4 .3) rule: clarifyIssue

**Section:** 4.6.3 Issue clariflcation
**Page:** 192

**Context Before:**
> this question, which means that the ambiguous answer no longer needs to
be integrated and can be thrown away8.
In this way we see how question accommodation, amended with a mechanism for resolving
whi...

**Algorithm:**

```
rule 4.3) rule: clarifyIssue
class: select action
in($/private/nim, usr-answer(A))
setof(C, in($/private/plan, flndout(Q)) and
pre: 8
>>>< $domain :: relevant(A, Q), QSet)
$$arity(QSet) > 1
>>>: ! setof(?P, in(QSet, Q) and $domain :: combine(Q, A, P), AltQ)
eff: push(/private/agenda, flndout(AltQ))
8
>< del(/private/nim, usr-answer(A))
>:
The flrst condition picks out the answer-move from the nim queue. The second and third
conditions check that there is more than one question in the plan to which the answer
is relevant, by constructing the set of such questions. The flrst operation constructs the
alternative-question by applying each question in the set constructed in condition 2 to the
answer to get a proposition and preflxing the question operator ’?’ to each proposition
to get a y/n-question. The alternative question is this set of y/n-questions. The second
operation pushes the action to raise the alternative question on the agenda, and the flnal
operation removes the answer move from nim; this is motivated above.
A sample dialogue with issue clariflcation is shown in (dialogue 4.2).
(dialogue 4.2)
S> Welcome to the travel agency!
U> price information please
S> Okay. I need some information. How do you want to travel?
U> flight um paris
S> OK, by flight. Do you mean from paris or to paris?
8IBiS3onlyhandlesfullanswerstoclariflcationquestions,i.e. \ToParis." or\FromParis.". Aslightly
more advanced semantics would be required to handle cases where the user again gives an underspecifled
response which resolves the question, i.e. \To." or \From.".
```

---

## Algorithm 99: rule 4 .4) rule: accommodateDependentIssue

**Section:** 4.6.4 Dependent issue accommodation: from domain resource to
**Page:** 194

**Context Before:**
> 27)(cid:14) 89 *2 (cid:27) :; &=
KE MO N
KE MO NS R !$ UV *X W2 (cid:25)Y ,
(cid:30)(cid:5) (cid:25)Y :d &) ((cid:9)*2 (cid:27)(cid:26) , (cid:30)(cid:5) (cid:25)Y :d &) ((cid:9)*2 (cid:27)(cid:26) ,
...

**Algorithm:**

```
rule 4.4) rule: accommodateDependentIssue
class: accommodate
setof(A, $/private/nim/elem/snd=answer(A), AnsSet)
$$arity(AnsSet) > 0
8
pre:
>>>>>>>>>>>>>>>>>>< i
$
f
s
o
d
r
e
o
a
$
m
l
m
d
l(
p
o
a
i
t
n
m
i
y
(
n
(
A
a
$
:
i
n
/
:
n
p
s
p
S
r
:
l
:
a
i
e
v
r
n
t
e
a
,
(
l
D
t
A
ev
e
)
e
a
/
,
p
n
p
i
Q
n
t
l
(
,
(
a
A
P
P
n
,
l
l
)
a
Q
a
n
n
)
,
)
)
flndout(Q)) and
not ( $domain :: plan(DepQ0, Plan0) and DepQ0 6= DepQ and
>>>>>>>>>>>>>>>>>>:
p
n
u
o
s
t
f
h
o
i
(
n
r
/
a
(
$
s
$
l
d
l
h
/
(
o
a
i
p
n
m
r
r
(A
i
a
e
v
d
i
n
a
n
/
s
t
i
w
:
e
s
:
s
e
/
r
u
r
a
e
S
e
g
le
s
e
e
v
,
t
n
a
,
D
n
d
A
t
e
a
(
)
p
A
,
,
Q
i
i
,
c
n
)
m
Q
(P
:
)
u
)
l
n
a
)
d
n
*
0,
in
fl
t
n
:u
d
s
o
r
u
*
t
is
(
s
Q
u
)
e
)
(D
an
e
d
pQ))
push(/private/agenda, icm:accommodate:DepQ)
8
eff: >>>>>><
s
p
e
u
t
s
(
h
/
(
p
/
r
p
i
r
v
i
a
v
t
a
e
t
/
e
p
/
l
a
a
g
n
e
,
n
P
d
l
a
a
,
n
i
)
cm:und*pos:usr*issue(DepQ))
push(/private/agenda, icm:loadplan)
>>>>>>:
The flrst two conditions construct a set of all non-integrated answers and check that the
arity of this set is larger than zero, i.e. that there is at least one non-integrated answer.
```

---

## Algorithm 100: rule 4 .5).

**Section:** 4.6.5 Dependent issue clariflcation
**Page:** 198

**Context Before:**
> 7
6 6 ›› fifi 7 7
6 6 lu = moves = oqueueanswer(yes) 7 7
6 6 2 3 7 7
6 6 score = 1 7 7
6 6 7 7
4 4 4 5 5 5
backupSharedSys
selectIcmOther
selectIcmOther
S> I need some information. by flight , is that...

**Algorithm:**

```
rule 4.5).
(rule 4.5) rule: clarifyDependentIssue
class: select action
in($/private/nim, pair(usr, answer(A)))
setof(Q0, $domain :: plan(Q0, Plan) and
8
pre:
>>>>>>>>>>><
QS
i
$
e
n
d
t
(
0
o
)
P
m
la
a
n
i
,
n
fl
:
n
:
d
r
o
e
u
le
t(
v
S
an
o
t
m
(A
eQ
, S
))
o
a
m
n
e
d
Q),
remove uniflables(QSet0, QSet)
eff:
>>>>>>>>>>>:
!
$$
se
a
t
r
o
it
f
y
(I
(Q
ss
S
u
e
e
t
Q
)
,
>
in
1
(QSet, I) and IssueQ=?issue(I), AltQ)
push(/private/agenda, flndout(AltQ))
(
```

---

## Algorithm 101: rule 4 .5) rule: clarifyDependentIssue

**Section:** 4.6.5 Dependent issue clariflcation
**Page:** 198

**Context Before:**
> fi 7 7
6 6 lu = moves = oqueueanswer(yes) 7 7
6 6 2 3 7 7
6 6 score = 1 7 7
6 6 7 7
4 4 4 5 5 5
backupSharedSys
selectIcmOther
selectIcmOther
S> I need some information. by flight , is that correct?
4...

**Algorithm:**

```
rule 4.5) rule: clarifyDependentIssue
class: select action
in($/private/nim, pair(usr, answer(A)))
setof(Q0, $domain :: plan(Q0, Plan) and
8
pre:
>>>>>>>>>>><
QS
i
$
e
n
d
t
(
0
o
)
P
m
la
a
n
i
,
n
fl
:
n
:
d
r
o
e
u
le
t(
v
S
an
o
t
m
(A
eQ
, S
))
o
a
m
n
e
d
Q),
remove uniflables(QSet0, QSet)
eff:
>>>>>>>>>>>:
!
$$
se
a
t
r
o
it
f
y
(I
(Q
ss
S
u
e
e
t
Q
)
,
>
in
1
(QSet, I) and IssueQ=?issue(I), AltQ)
push(/private/agenda, flndout(AltQ))
(
```

---

## Algorithm 102: 4 .6).

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION179
**Page:** 201

**Context Before:**
> ATIONANDREACCOMMODATION179
U> a flight, april the fifth
S> by flight. in april. the fifth. Okay. What city do you want to go
to?
U> london
S> Okay. to london.
U> actually, i want to go on the fourth
S...

**Algorithm:**

```
rule
4.6).
(rule 4.6) rule: accommodateCom2Issues
class: accommodate
$/private/nim/elem/snd=answer(A)
in($/shared/com, P)
8
pre: >>>>>><
$
$
d
d
o
o
m
m
a
a
i
i
n
n
:
:
:
:
r
q
e
u
l
e
e
s
v
t
a
i
n
o
t
n
(
(
A
Q
,
)
Q)
$domain :: relevant(P, Q)
eff:
>>>>>>:
push(/shared/issues, Q)
n
This accommodation rule looks for an answer A among the moves which have not yet been
integrated (flrst condition). It then looks for a proposition among the shared commitments
establishedinthedialoguesofar(secondcondition)whichaccordingtothesystem’sdomain
resource is an appropriate answer to some question for which A is also an answer (third to
flfth conditions). Given that in this simple system answers can only be relevant to a single
question10, this strategy will be successful in identifying cases where we have two answers
to the same question. A system that deals with more complex dialogues where this is not
the case would need to keep track of closed issues in a separate list of closed issues. Thus
theconditionswillsucceedifthereisaquestionsuchthatboththeuseranswerandastored
proposition are relevant answers to it; in the example dialogue above, \departure date is
the fourth" and \departure date is the flfth" are both relevant answers to the question
\which day do you want to travel?". If such a question is found it is accommodated to
issues, that is, it becomes an open issue again.
WhenaccommodateCom2Issueshasbeensuccessfullyapplied, theretractrulein(rule
10That is, in the full form in which they appear in $/shared/com. \Chicago" can be an answer to
\Which city do you want to go to?" and \Which city do you want to go from?" but when it has been
combined with the questions the result will be \destination(Chicago)" and \from(Chicago)" respectively
and it is this which is entered into the commitments.
```

---

## Algorithm 103: rule 4 .6) rule: accommodateCom2Issues

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION179
**Page:** 201

**Context Before:**
> COMMODATION179
U> a flight, april the fifth
S> by flight. in april. the fifth. Okay. What city do you want to go
to?
U> london
S> Okay. to london.
U> actually, i want to go on the fourth
S> the fourth...

**Algorithm:**

```
rule 4.6) rule: accommodateCom2Issues
class: accommodate
$/private/nim/elem/snd=answer(A)
in($/shared/com, P)
8
pre: >>>>>><
$
$
d
d
o
o
m
m
a
a
i
i
n
n
:
:
:
:
r
q
e
u
l
e
e
s
v
t
a
i
n
o
t
n
(
(
A
Q
,
)
Q)
$domain :: relevant(P, Q)
eff:
>>>>>>:
push(/shared/issues, Q)
n
This accommodation rule looks for an answer A among the moves which have not yet been
integrated (flrst condition). It then looks for a proposition among the shared commitments
establishedinthedialoguesofar(secondcondition)whichaccordingtothesystem’sdomain
resource is an appropriate answer to some question for which A is also an answer (third to
flfth conditions). Given that in this simple system answers can only be relevant to a single
question10, this strategy will be successful in identifying cases where we have two answers
to the same question. A system that deals with more complex dialogues where this is not
the case would need to keep track of closed issues in a separate list of closed issues. Thus
theconditionswillsucceedifthereisaquestionsuchthatboththeuseranswerandastored
proposition are relevant answers to it; in the example dialogue above, \departure date is
the fourth" and \departure date is the flfth" are both relevant answers to the question
\which day do you want to travel?". If such a question is found it is accommodated to
issues, that is, it becomes an open issue again.
WhenaccommodateCom2Issueshasbeensuccessfullyapplied, theretractrulein(rule
10That is, in the full form in which they appear in $/shared/com. \Chicago" can be an answer to
\Which city do you want to go to?" and \Which city do you want to go from?" but when it has been
combined with the questions the result will be \destination(Chicago)" and \from(Chicago)" respectively
and it is this which is entered into the commitments.
```

---

## Algorithm 104: 10 That is, in the full form in which they appear in $/shared/com. \Chicago" can be an answer to

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION179
**Page:** 201

**Context Before:**
> a separate list of closed issues. Thus
theconditionswillsucceedifthereisaquestionsuchthatboththeuseranswerandastored
proposition are relevant answers to it; in the example dialogue above, \departure d...

**Algorithm:**

```
rule
10That is, in the full form in which they appear in $/shared/com. \Chicago" can be an answer to
\Which city do you want to go to?" and \Which city do you want to go from?" but when it has been
combined with the questions the result will be \destination(Chicago)" and \from(Chicago)" respectively
and it is this which is entered into the commitments.
```

---

## Algorithm 105: rule 4 .7) rule: retract

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION179
**Page:** 202

**Context Before:**
> 180 CHAPTER 4. ADDRESSING UNRAISED ISSUES
4.7) will remove the incompatible information from the system’s view of shared commit-
ments represented in /shared/com.
(...

**Algorithm:**

```
rule 4.7) rule: retract
class: integrate
$/private/nim/elem/snd=answer(A)
in($/shared/com, P0)
8
pre:
>>>>>>>>>>><
$
$
fs
d
d
t(
o
o
$
m
m
/s
a
a
h
i
i
n
n
ar
:
:
:
:
ed
r
r
e
e
/
l
l
i
e
e
s
v
v
s
a
a
u
n
n
e
t
t
(
(
s
P
A
,
,
Q
,
Q
Q
)
)
)
$domain :: combine(Q, A, P)
eff:
>>>>>>>>>>>:
d
$
e
d
l(
o
/
m
sh
a
a
in
re
::
d/
in
c
c
o
o
m
m
,
p
P
at
0
i
)
ble(P, P0)
n
The conditions here are similar to those in (rule 4.6). We look for an unintegrated
```

**Context After:**
> answer (flrst condition) which is relevant to a question at the head of the list of open issues
(third and flfth conditions) and for which there is already a relevant answer in the shared
commitments ...

---

## Algorithm 106: rule 4 .6). We look for an unintegrated

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION179
**Page:** 202

**Context Before:**
> information from the system’s view of shared commit-
ments represented in /shared/com.
(rule 4.7) rule: retract
class: integrate
$/private/nim/elem/snd=answer(A)
in($/shared/com, P0)
8
pre:
>>>>>>>>>>...

**Algorithm:**

```
rule 4.6). We look for an unintegrated
answer (flrst condition) which is relevant to a question at the head of the list of open issues
(third and flfth conditions) and for which there is already a relevant answer in the shared
commitments (second and fourth conditions). Finally, we determine that the result of
combining the answer with the question (sixth condition) is incompatible with the answer
already found (seventh condition). If all this is true we delete the answer which is currently
in the shared commitments. This will flnally allow the new answer to be integrated by a
rule that integrates an answer from the user, and a further rule will remove the resolved
issue from QUD. Note that this rule is of class integrate. As is indicated in Appendix B, it
is tried before any other integration rule, to avoid integration of con(cid:176)icting information.
Note also that the \incompatible" relation is deflned as a part of the domain resource, and
can thus be domain speciflc. The simple kind of revision that IBiS currently deals with
is also handled by some form-based systems (although they usually do not give feedback
indicating that information has been removed or replaced, as IBiS does). For example,
Chu-Carroll (2000) achieves a similar result by extracting parameter values from the latest
user utterance and subsequently (if possible) copying values from the previous form for
any parameters not specifled in the latest utterance. A similar mechanism is referred to
as \overlay" by Alexandersson and Becker (2000). While we are dealing only with very
simple revision here, the rule in (rule 4.7) and the \incompatible" relation can be seen as
```

**Context After:**
> placeholders for a more sophisticated mechanism of belief revision.
It is also possible to remove the old answer by denying it (asserting its negation) as in
(dialogue 4.7).
(dialogue 4.7)...

---

## Algorithm 107: rule 4 .7) and the \incompatible" relation can be seen as

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION179
**Page:** 202

**Context Before:**
> lly do not give feedback
indicating that information has been removed or replaced, as IBiS does). For example,
Chu-Carroll (2000) achieves a similar result by extracting parameter values from the late...

**Algorithm:**

```
rule 4.7) and the \incompatible" relation can be seen as
placeholders for a more sophisticated mechanism of belief revision.
It is also possible to remove the old answer by denying it (asserting its negation) as in
(dialogue 4.7).
(dialogue 4.7)
```

---

## Algorithm 108: rule 4 .8) rule: accommodateCom2IssuesDependent

**Section:** 4.6.7 Opening up implicit grounding issues
**Page:** 204

**Context Before:**
> 182 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(...

**Algorithm:**

```
rule 4.8) rule: accommodateCom2IssuesDependent
class: accommodate
$/private/nim/elem/snd=answer(A)
in($/shared/com, P)
8
pre:
>>>>>>>>>>>>>>><
$
$
i
$
s
d
d
d
e
o
o
o
m
m
m
m
p
a
a
a
t
i
i
i
y
n
n
n
($
:
:
:
/
:
:
:
s
r
r
q
h
e
e
u
a
l
l
e
e
e
r
s
v
v
t
a
a
e
i
n
n
o
d
t
t
n
/
(
(
(
i
P
A
Q
ss
,
,
)
u
Q
Q
e
)
)
s)
$domain :: depends(Q0, Q)
>>>>>>>>>>>>>>>:
d
$
in
e
d
(
l
o
(
$
/
/
m
p
s
a
r
h
i
i
a
n
v
r
a
:
e
t
:
d
e
r
/
e
/
c
l
b
e
o
e
va
l
m
n
,
,
t
P
(
P
P
0)
0)
0, Q0)
del(/shared/com, P0)
8
eff: >>>>>><
p
p
u
u
s
s
h
h
(
(
/
/
s
s
h
h
a
a
r
r
e
e
d
d
/
/
i
i
s
s
s
s
u
u
e
e
s
s
,
,
Q
Q
)
0)
push(/private/agenda, respond(Q0))
>>>>>>:
This rule is similar to 6 except that is looks for a question which depends on the question
it flnds corresponding to the answer provided by the user. It puts both question onto the
list of open issues and plans to respond to the dependent question. This rule, as currently
implemented, is speciflc to the particular case treated in the system. There is, of course, a
great deal more to say about what it means for one question to be dependent on another
and how the system knows whether it should respond to dependent questions or raise them
with the user.
```

**Context After:**
> 4.6.7 Opening up implicit grounding issues
In Chapter 3 we outlined a general issue-based account of grounding, where issues of con-
tact, perception, understanding and acceptance of utterances may be...

---

## Algorithm 109: rule 4 .9) rule: accommodateQUD2Issues

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION183
**Page:** 205

**Context Before:**
> erpretation
was correct, we can use this to allow the user to reject faulty system interpretations. Be-
sides, we already have mechanisms in place for representing and dealing with answers to
the unde...

**Algorithm:**

```
rule 4.9) rule: accommodateQUD2Issues
class: accommodate
$/private/nim/elem/snd=answer(A)
in($/shared/qud, Q)
pre: 8
>>>< $domain :: relevant(A, Q)
not in($/shared/issues, Q)
eff:
>>>:
push(/shared/issues, Q)
n
The rule in (rule 4.9) picks out a non-integrated answer-move which is relevant to a
```

**Context After:**
> question on QUD which is not currently an open issue, and pushes it on issues.
To handle integration responses to positive understanding feedback, we also need to mod-
ify the integrateNegIcmAnswer ru...

---

## Algorithm 110: rule 4 .9) picks out a non-integrated answer-move which is relevant to a

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION183
**Page:** 205

**Context Before:**
> odel the fact that the acceptance question regarding understanding is implicit rather
than explicit, we push it onto the local QUD only. If the user addresses it (e.g. by saying
\no"), the implicit is...

**Algorithm:**

```
rule 4.9) picks out a non-integrated answer-move which is relevant to a
question on QUD which is not currently an open issue, and pushes it on issues.
To handle integration responses to positive understanding feedback, we also need to mod-
ify the integrateNegIcmAnswer rule described in Section 3.6.6. A signiflcant difierence
between positive and interrogative feedback in IBiS is that the former is associated with
cautiously optimistic grounding, while the latter is used in the pessimistic grounding strat-
egy. This means that a negative response to feedback on the understanding level must be
handled difierently depending on whether the content in question has been added to the
dialogue gameboard or not. Speciflcally, if the positive feedback is rejected the optimistic
grounding assumption must be retracted.
```

---

## Algorithm 111: rule 4 .10) rule: integrateNegIcmAnswer

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION183
**Page:** 206

**Context Before:**
> 184 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(...

**Algorithm:**

```
rule 4.10) rule: integrateNegIcmAnswer
class: integrate
$/private/nim/fst/snd=answer(A)
fst($/shared/issues, Q)
8
pre:
>>>>>>>>< $
fs
d
t(
o
$
m
/s
a
h
in
ar
::
ed
re
/
s
q
o
u
lv
d
es
,
(
Q
A
)
, Q)
$domain :: combine(Q, A, P)
>>>>>>>>:
p
P
o
=
p(
n
/
o
p
t(
r
u
i
n
v
d
a
(
t
D
e
P
/n
*
i
C
m
)
)
)
pop(/shared/issues)
8
eff:
>>>>>>>>>>>>>>>>>>>>>>>< if d
/
/
/
C
o
s
s
s
(
=
h
h
h
in
i
a
a
a
s
(
s
r
r
r
$
u
/
e
e
e
e
s
d
d
d
(
h
Q
/
/
/
a
i
q
c
0
s
)
r
o
u
s
e
a
u
m
d
n
d
e
d
:
/
:
s
=
=
c
i
:
n
o
=
$
$
(
m
/
/
$
$
p
p
/
,
/
r
s
r
C
p
h
i
i
v
r
)
v
a
a
a
i
o
r
v
t
t
r
e
a
e
e
d
t
/
/
e
/
t
t
i
/
m
m
s
t
s
p
p
m
u
/
/
e
p
D
D
s
/
P
,
P
D
Q
/
/
P
q
c
0)
/
u
o
,
i
d
s
m
[
sues
/private/agenda := $/private/tmp/DP/agenda
>>>>>>>>>>>>>>>>>>>>>>>:
i
p
c
n
l
u
e
it
s
a
/
h
r
p
s
(
(
h
r
/
/
i
p
p
i
f
v
t
r
r
(
a
i
i
/
t
v
v
p
a
a
e
r
t
t
/
i
p
e
e
v
l
a
/
/
a
n
a
t
n
g
i
e
m
/
e
:
)
n
=
n
i
d
m
$
a
)
/
,
p
i
r
cm
iv
:
a
u
t
nd
e
*
/
p
t
o
m
s:
p
D
/D
P*
P
n
/
o
p
t(
l
C
a
)
n
)
])
The rule in (rule 4.10) is similar to those for integrating \normal" user answers (see Sec-
```

**Context After:**
> tion 3.6.6), because of the special nature of grounding issues, we include issue downdating
in the rule rather than adding a further rule for downdating issues for this special case.
This means the ru...

---

## Algorithm 112: rule 4 .10) is similar to those for integrating \normal" user answers (see Sec-

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION183
**Page:** 206

**Context Before:**
> o
=
$
$
(
m
/
/
$
$
p
p
/
,
/
r
s
r
C
p
h
i
i
v
r
)
v
a
a
a
i
o
r
v
t
t
r
e
a
e
e
d
t
/
/
e
/
t
t
i
/
m
m
s
t
s
p
p
m
u
/
/
e
p
D
D
s
/
P
,
P
D
Q
/
/
P
q
c
0)
/
u
o
,
i
d
s
m
[
sues
/private/agenda :=...

**Algorithm:**

```
rule 4.10) is similar to those for integrating \normal" user answers (see Sec-
tion 3.6.6), because of the special nature of grounding issues, we include issue downdating
in the rule rather than adding a further rule for downdating issues for this special case.
This means the rule has to check that the answer resolves the grounding issue, rather than
merely checking that it is relevant; this is done in the third condition. The content result-
ing from combining the issue on QUD and the answer is computed in the flfth condition.
Finally, the sixth condition checks that the content is not(und(DP*C)) where DP is a DP
and C is the content that is being grounded (or in this case, not grounded).
The second update removes the grounding question from issues. The third update flrst
checks if C has been optimistically grounded. In this case, the optimistic grounding as-
sumption regarding the grounding of C is retracted. This is where the new tmp/usr fleld,
containing relevant parts of the information state as they were before the latest user utter-
ance was optimistically assumed to be grounded, is used. If C has not been optimistically
assumed to be grounded, nothing in particular needs to be done.
The fourth update adds positive feedback that the system has understood that C was false.
Note that not(C) is not added to /shared/com. The reason for this is that the negated
proposition is not something that the user intended to add to the DGB - it was simply a
result of a misunderstanding by the system.
```

---

## Algorithm 113: Procedure/Rule in 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION187

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION187
**Page:** 209

**Algorithm:**

```
4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION187
pop(/private/nim)
pop(/shared/issues)
8
if do(in($/shared/com, issue(?A.price(A))) or
>>>>>>>>>>>>>>>>>><
/
/
/
/
is
s
p
s
s
s
h
h
h
u
r
e
a
a
a
iv
(
r
r
r
?
a
e
e
e
A
t
d
d
d
.
e
p
/
/
/
/
r
c
i
q
a
i
s
c
o
u
s
g
e
u
m
d
(
e
A
e
n
:
:
s
)
=
=
d
)
:
a
=
=
$
$
i
/
:
/
s
=
$
p
s
p
u
/
r
r
$
e
p
i
i
(
/
v
r
v
D
p
a
a
iv
r
t
t
)
a
i
e
e
a
v
t
/
/
n
a
e
t
t
d
t
/
m
m
e
t
i
p
n
p
/
m
/
t
(
/
p
$
u
u
m
/
/
s
s
p
s
u
r
r
h
/
s
/
/
u
a
r
q
c
s
/
r
u
o
r
i
e
d
s
m
/
d
s
a
u
/
g
i
e
s
e
s
s
n
u
d
e
a
s, D), [
/private/plan := $/private/tmp/usr/plan ])
>>>>>>>>>>>>>>>>>>:
dow
p
i
c
n
l
u
n
e
it
s
a
d
h
r
s
a
(
(
h
/
/
t
i
e
p
p
ft
Q
r
r
(
i
i
/
U
v
v
p
a
a
r
D
t
t
i
e
e
v
/
/
a
n
a
t
g
i
e
m
/
e
)
n
n
i
d
m
a
)
, icm:und*pos:usr*not(issue(?A.price(A))))
icm:loadplan
agenda =
icm:und*pos:usr*not(issue(?A.price(A)))
2 2 ¿¿ (cid:192)(cid:192) 3 3
plan = hi
6 6 bel = fg 7 7
6 6 7 7
6 6 com = fg 7 7
6 private = 6 7 7
6 6 qud = hi 7 7
6 6 2 2 3 3 7 7
6 6 tmp = usr = issues = hi 7 7
6 6 7 7
6 6 6 6 agenda = hhii 7 7 7 7
6 6 6 6 7 7 7 7
6 6 6 6 plan = hi 7 7 7 7
6 6 6 6 7 7 7 7
6 6 nim = h4hii 4 5 5 7 7
6 6 7 7
6 4 com = fg 5 7
6 7
6 issues = hi 7
6 2 3 7
6 qud = hi 7
6 shared = 7
6 6 pm = icm:und*pos:usr*issue(?A.price(A)), icm:acc*pos 7 7
6 6 7 7
6 6 speaker = usr 7 7
6 6 lu = ' “ 7 7
6 6 moves = answer(not(und(usr*issue(?A.price(A))))) 7 7
6 6 • ‚ 7 7
4 4 5 5
' “
backupSharedSys
selectIcmOther
S> You did not ask about price.
Feedback for utterances realizing several moves
In the case where a user utterance provides answers to several questions (and perhaps
also asks a question), the strategy we have chosen is to produce feedback for each move
individually to give the user a chance to correct mishearings or misunderstandings. If
positive feedback regarding one piece of information is rejected, the optimistic assumption
isretractedbymodifyingtheinformationstateaccordingtothe/private/tmp/usrsaved
state. If feedback regarding one piece of information is accepted, this information should
not disappear if a later feedback utterance from the system should be rejected.
```

---

## Algorithm 114: rule 4 .11) rule: integratePosIcmAnswer

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION189
**Page:** 211

**Context Before:**
> 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION189
(...

**Algorithm:**

```
rule 4.11) rule: integratePosIcmAnswer
class: integrate
$/private/nim/fst/snd=answer(A)
fst($/shared/issues, Q)
8
pre:
>>>>>>>>< $
fs
d
t(
o
$
m
/s
a
h
in
ar
::
ed
re
/
s
q
o
u
lv
d
es
,
(
Q
A
)
, Q)
$domain :: combine(Q, A, P)
>>>>>>>>:
p
P
o
=
p(
u
/
n
p
d
r
(D
iv
P
at
*
e
C
/
o
n
n
i
t
m
en
)
t)
pop(/shared/issues)
8
eff:
>>>>>>>>>>>>>>>>>>>>>>>>>>><
i
i
f
f t
d
a
p
p
p
h
o
d
u
u
u
e
(
n
d
n
s
s
s
h
h
h
(
o
e
/
(
(
(
t
l
/
/
/
p
s
(
p
p
p
e
r
(
r
r
r
i
i
n
C
v
i
i
i
(
v
v
v
a
o
$
a
a
a
t
n
/
t
t
t
e
t
s
e
e
e
e
h
/
n
/
/
/
t
a
t
t
t
t
m
r
=
m
m
m
e
p
is
p
p
p
d
/
s
/
/
/
D
u
/
D
D
D
e
c
P
(
o
P
P
P
Q
/
m
/
/
/
c
0)
a
i
q
,
o
,
s
g
u
C
s
m
[
u
e
d
o
,
n
e
,
n
C
s
d
Q
te
,
o
a
0
n
n
Q
)
,
t
t
r
)
0
e
)
e
n
o
s
t
p
r
)
o
)
nd(Q0)) ],
Content=issue(Q0) and in($/shared/issues, Q0) ),
>>>>>>>>>>>>>>>>>>>>>>>>>>>:
a
if
d
t
d
p
p
p
h
(
u
u
u
e
/
n
s
s
s
s
h
h
h
h
e
(
(
(
a
l
/
/
/
s
r
p
s
s
e
h
h
(
e
r
C
a
a
d
iv
o
r
r
/
a
n
c
e
e
t
t
o
d
d
e
e
m
/
/
n
/
i
q
t
a
,
s
=
u
s
g
C
u
d
i
e
s
o
e
,
s
n
n
u
s
Q
d
t
e
,
e
(
a
0
Q
n
)
Q
,
t
0
0
)
r
)
)
e
)
,
)
sp
[
ond(Q0)) ],
The conditions are similar to those of the previous version of the rule, except for inspecting
issues instead of qud. The flrst two updates are also the same. The third update adds the
content Content which is being grounded to tmp/usr (in case DP is usr, which it always
is in IBiS3). This means that if future feedback (concerning the same utterance) from the
system is rejected, the system will backtrack to a state where Content is integrated. The
conditionals in the third and fourth updates re(cid:176)ect the fact that questions are integrated
difierently from propositions. The fourth update is similar to the third update in the
previous version of the rule.
Implicit acceptance
Before we move on there is one more thing to consider. If the user does not reject the
system’s positive feedback concerning a piece of information, this is regarded as an implicit
acceptance. Therefore, we also need to add a noFollowup rule, for cases where positive
system feedback is not responded to at all (i.e. the user does not take the turn ofiered).
```

---

## Algorithm 115: rule 4 .12) rule: noFollowup

**Section:** 4.6. VARIETIESOFQUESTIONACCOMMODATIONANDREACCOMMODATION189
**Page:** 212

**Context Before:**
> 190 CHAPTER 4. ADDRESSING UNRAISED ISSUES
(...

**Algorithm:**

```
rule 4.12) rule: noFollowup
class: (none)
$input, ’TIMED OUT’
pre:
in($/shared/pm, icm:und*pos:usr*Content)
(
if then else(Content=issue(Q), [
push(/private/tmp/usr/qud, Q)
8
eff: >>>>>>< p
p
u
u
s
s
h
h
(
(
/
/
p
p
r
r
i
i
v
v
a
a
t
t
e
e
/
/
t
t
m
m
p
p
/
/
u
u
s
s
r
r
/
/
i
a
s
g
su
en
es
d
,
a
Q
, r
)
espond(Q)) ],
add(/private/tmp/usr/com, Content))
>>>>>>:
The flrst condition is true only if the user did not produce any utterance (that the system
heard) during her latest turn11. The second condition checks that the moves performed in
the previous utterance includes positive understanding feedback regarding Content. The
flrst updates are identical to the third update in the integratePosIcmAnswer rule in
Section 4.6.7.
Below is a dialogue example involving positive, implicit positive, and negative followups
to system feedback.
(dialogue 4.12)
S> Welcome to the travel agency!
U> price information please
S> Okay. Lets see. How do you want to travel?
U> a flight to paris in april
S> Okay. by flight.
U> yes
S> to paris.
U>
S> in april.
U> no
S> not in april. What city do you want to go to?
Implicit questions and elliptical answers
In the case of implicit acceptance questions in English (and Swedish) it appears that they
can be addressed by short answers; however, we cannot assume that all implicit issues
can be addressed elliptically. The use of QUD for storing implicit issues relies on the fact
11See Section 3.6.6 for an explanation of ’TIMED OUT’.
```

---

## Algorithm 116: rule 4 .13) rule: backupSharedUsr

**Section:** 4.7. FURTHER IMPLEMENTATION ISSUES 193
**Page:** 215

**Context Before:**
> 4.7. FURTHER IMPLEMENTATION ISSUES 193
(...

**Algorithm:**

```
rule 4.13) rule: backupSharedUsr
class: (none)
$latest speaker=usr
$latest moves=Moves
8
pre:
>>>>>>>>>>><
n
n
n
o
o
o
t
t
t
i
i
(
n
n
f
(
(
s
M
M
t($
o
o
/
v
v
s
e
e
h
s
s
,
,
a
n
i
r
c
o
m
ed
m
:X
/
o
q
)
v
u
e)
d, und(usr*C)) and
in(A, answer(D)) and
>>>>>>>>>>>:
/pr
$
i
d
va
o
t
m
e
a
/
i
t
n
m
:
p
:
/
r
u
el
s
e
r
v
/
a
q
nt
u
(
d
D,
:=
un
$
d
/
(
s
u
h
sr
a
*
r
C
e
)
d
))
/qud
/private/tmp/usr/issues := $/shared/issues
8
eff: >>>>>>< /
/
p
p
r
r
i
i
v
v
a
a
t
t
e
e
/
/
t
t
m
m
p
p
/
/
u
u
s
s
r
r
/
/
c
a
o
g
m
en
:
d
=
a
$
:
/
=
sh
$
a
/p
r
r
e
i
d
v
/
a
c
t
o
e
m
/agenda
/private/tmp/usr/plan := $/private/plan
>>>>>>:
The flrst condition checks that the latest speaker was indeed the user; if not, the rule
should of course not trigger. The next four conditions are used to prevent triggering in
case of an ICM subdialog, i.e. if the user produced an ICM move or responded to one from
the system. (Note that no move may count as implicit ICM if the user does not respond to
ICM from the system; see Section 4.6.7). The flfth condition checks if the user utterance
contains an answer relevant to a grounding-question on QUD. The efiects simply copy the
contents of tmp/usr to the corresponding paths in the information state.
Integration rules and nim
In IBiS2, the integration rules inspect nim using the condition in(/private/nim, Moves).
Since TrindiKit uses backtracking to flnd instantiations of variables in conditions (see
Appendix A), this results in each integration rule looking through the whole queue of non-
integrated moves. Thus, in IBiS2 the ordering of the integration rules determines which
move is integrated flrst. This is okay for dialogues with a very simple structure, but when
dialogues become more complex (e.g. because of accommodation), the ordering of the
moves becomes more important.
Therefore, in IBiS3 all integration rules inspect only the flrst move on the nim queue, using
theconditionfst(/private/nim, Move)orsimilar. Incombinationwiththequeue-shifting
technique described in Section 4.7.2, this means that the algorithm tries to integrate moves
in the order they were performed.
```

---

## Algorithm 117: Procedure/Rule in 4.8.1 Phrase spotting and syntax in (cid:176)exible dialogue

**Section:** 4.8.1 Phrase spotting and syntax in (cid:176)exible dialogue
**Page:** 219

**Algorithm:**

```
4.8. DISCUSSION 197
4.7.3 Selection module
The selection module is almost unchanged from IBiS2. Some minor adjustments have been
made to adapt the rules to the changes in the information state type: that objects in nim
are pairs of DPs and moves, and that tmp is divided into two substructures.
4.8 Discussion
In this section we discuss some variations on IBiS3, show some additional \emergent"
features, and discuss various aspects of question accommodation.
4.8.1 Phrase spotting and syntax in (cid:176)exible dialogue
As it turns out, IBiS3 sometimes runs into trouble if the interpreter recognizes several
answers to the same question in an utterance. Whereas IBiS2 would simply integrate the
flrst answer and ignore the second, IBiS3 will try to make sense of all the moves in an
utterance, which may lead to problems if the accommodation rules are not designed to
cover the case at hand.
For example, if the system recognizes \paris to london" as a flrst utterance in a dialogue,
the system will try dependent issue accommodation (see Section 4.6.4) and note that the
set of answers (answer(paris) and answer(dest city(london))) is (indirectly) relevant to
both the price issue and the visa issue. It might seem that this is wrong, since the two
answers are in fact relevant to the same question (regarding destination city) in the \visa"
plan, whereas it is relevant to two separate questions (destination and departure city) in
the \price" plan, so it should be indirectly relevant only to the \price" issue. But in
general, one cannot require that the two answers must be answers to difierent questions,
since the second answer may be a correction of the flrst. This may of course be signalled
more clearly, as in \to paris uh no to london", but the correction signals may be left out,
inaudible, or not recognized.
One way to solve this problem is to sometimes look for constructions which realize more
than one move, and do some \cleaning up" in the interpretation phase so that the DME
will not get into trouble. For example, we can add a lexical entry looking for phrases
of the form \X to Y" and interpret this as \from X to Y", i.e. answer(dept city(X))
andanswer(dest city(Y)).
A related problem occurs if the user flrst chooses Gothenburg as departure city and then
```

---

## Algorithm 118: procedure may also have side-efiects (e.g. loading a new

**Section:** 4.8.6 Accommodation vs. normal integration
**Page:** 224

**Context Before:**
> ny real difierence to the internal
processing and/or external behaviour of the system remains a future research issue. For
example, if QUD is updated with Q before A is produced, and the utterance rea...

**Algorithm:**

```
procedure may also have side-efiects (e.g. loading a new
dialogue plan) which serve to drive the dialogue forward.
Instead of giving rules for accommodation and integration separately, one could deny the
existence of accommodation and just give more complex integration rules. The integration
rule for short answers requires that there is a question on the QUD to which the latest
move is an appropriate answer, and the accommodation rules are used if no such question
can be found. The alternative is to skip the QUD requirement, thus incorporating the
accommodation mechanisms into the integration rule, which would then split into several
rules. For example, there would be one rule for integrating answers by matching them to
questions in the plan directly.
Apart from the theoretical argument that question accommodation provides a generaliza-
tion of the way answers are integrated, there are also practical motivations. In particular,
```

---

## Algorithm 119: Procedure/Rule in 4.9 Summary

**Section:** 4.9 Summary
**Page:** 225

**Algorithm:**

```
4.9. SUMMARY 203
the fact that several steps of accommodation may be necessary to integrate a single answer
means that the total number of rules for integrating answers would be higher if accom-
modation was not used - one would need at least one integration rule for each possible
combination of accommodation rules.
A further argument which is not explored in this thesis (but see Engdahl et al., 1999) is
thatquestionpresuppositionandaccommodationinteractwithintra-sententialinformation
structure in interesting and useful ways.
4.8.7 Dependent issue accommodation in VoiceXML?
On a close reading of the VoiceXML speciflcation (McGlashan et al., 2001), it may ap-
pear that VoiceXML ofiers a mechanism similar to dependent issue accommodation12. In
VoiceXML, a grammar can have scope over a single slot, over a form, or over a whole
document (containing several forms). Given a grammar with document scope (deflning a
set of sentences which the VoiceXML interpreter will listen for during the whole dialogue),
if the user gives information which does not match the currently active form, VoiceXML
will jump to a form matching the input13. This corresponds roughly to the dependent issue
accommodation mechanism in IBiS . However, if input matches more than one task (e.g.
\raise the volume" could match a task related to the TV or one related to the CD player),
VoiceXML will not ask which of these tasks the user wants to perform but instead go to
the one it flnds flrst, regardless of what the user intended. Generally, it is hard to see how
clariflcation questions could be handled in a general way in VoiceXML, since they do not
belong to a particular form.
4.9 Summary
To enable more (cid:176)exible dialogue behaviour, we made a distinction between a local and
a global QUD (referring to the latter as \open issues", or just \issues"). The notions of
12ThisdiscussionisbasedontheVoiceXMLspeciflcationratherthanhands-onexperienceofVoiceXML.
This means that some unclarity remains about the capabilities of VoiceXML in general, and individual
implementations of VoiceXML servers in particular. For both these reasons, the discussion should be
regarded as tentative and open for revision. However, it should also be pointed out that it is fairly
clear what is supported in VoiceXML; most of the unclarities refer to what is possible, but not explicitly
supported, in VoiceXML. In general, it is more important to know what is supported by a standard than
what is possible, since almost anything is possible in any programming environment (given a su–cient
number of hacks).
13Although the VoiceXML documentation does not provide any examples of this kind of behaviour, it
appears to be possible, at least in principle.
```

---

## Algorithm 120: rule 5 .1).

**Section:** 5.6.2 Executing device actions
**Page:** 238

**Context Before:**
> 216 CHAPTER 5. ACTION-ORIENTED AND NEGOTIATIVE DIALOGUE
The rule for integrating user requests is shown in (...

**Algorithm:**

```
rule 5.1).
(rule 5.1) rule: integrateUsrRequest
class: integrate
$/private/nim/fst/snd=request(A)
$/shared/lu/speaker==usr
8
pre: >>>>>><
S
$s
c
c
o
o
re
re
>
=
0
S
.7
core
$domain :: plan(A, Plan)
>>>>>>:
pop(/private/nim)
add(/shared/lu/moves, request(A))
8
eff:
>>>>>>>>>>>< p
if
u
d
s
p
o
h
u
(
(
S
s
/
h
p
c
(
o
r
/
r
i
p
v
e
r
a
•
i
t
v
e
a
0
/
t
.9
a
e
,
g
/
e
a
n
g
d
e
a
n
,
d
i
a
cm
, i
:
c
a
m
cc
:u
*
n
p
d
o
*
s)
pos:usr*action(A)))
push(/shared/actions, A)
>>>>>>>>>>>:
push(/private/agenda, A)
This rule is similar to that for integrating user ask moves (see Section 3.6.6); instead of
pushing an issue Q on ISSUES and QUD, and pushing respond(Q) on the agenda, this rule
pushes the requested action A on /shared/actions and /private/agenda.
As for user ask moves we also need to deal with the case where the system must reject an
action since it does not have a plan for dealing with it. This rule is shown in (rule 5.2).
```

**Context After:**
> (rule 5.2) rule: rejectAction
class: select action
in($/private/nim, request(A))
pre: $/shared/lu/speaker=usr
8
>< not $domain :: plan(A, Plan)
del(/private/nim, request(A))
>:
eff: push(/private/agen...

---

## Algorithm 121: rule 5 .1) rule: integrateUsrRequest

**Section:** 5.6.2 Executing device actions
**Page:** 238

**Context Before:**
> 216 CHAPTER 5. ACTION-ORIENTED AND NEGOTIATIVE DIALOGUE
The rule for integrating user requests is shown in (rule 5.1).
(...

**Algorithm:**

```
rule 5.1) rule: integrateUsrRequest
class: integrate
$/private/nim/fst/snd=request(A)
$/shared/lu/speaker==usr
8
pre: >>>>>><
S
$s
c
c
o
o
re
re
>
=
0
S
.7
core
$domain :: plan(A, Plan)
>>>>>>:
pop(/private/nim)
add(/shared/lu/moves, request(A))
8
eff:
>>>>>>>>>>>< p
if
u
d
s
p
o
h
u
(
(
S
s
/
h
p
c
(
o
r
/
r
i
p
v
e
r
a
•
i
t
v
e
a
0
/
t
.9
a
e
,
g
/
e
a
n
g
d
e
a
n
,
d
i
a
cm
, i
:
c
a
m
cc
:u
*
n
p
d
o
*
s)
pos:usr*action(A)))
push(/shared/actions, A)
>>>>>>>>>>>:
push(/private/agenda, A)
This rule is similar to that for integrating user ask moves (see Section 3.6.6); instead of
pushing an issue Q on ISSUES and QUD, and pushing respond(Q) on the agenda, this rule
pushes the requested action A on /shared/actions and /private/agenda.
As for user ask moves we also need to deal with the case where the system must reject an
action since it does not have a plan for dealing with it. This rule is shown in (rule 5.2).
```

**Context After:**
> (rule 5.2) rule: rejectAction
class: select action
in($/private/nim, request(A))
pre: $/shared/lu/speaker=usr
8
>< not $domain :: plan(A, Plan)
del(/private/nim, request(A))
>:
eff: push(/private/agen...

---

## Algorithm 122: rule 5 .2).

**Section:** 5.6.2 Executing device actions
**Page:** 238

**Context Before:**
> os:usr*action(A)))
push(/shared/actions, A)
>>>>>>>>>>>:
push(/private/agenda, A)
This rule is similar to that for integrating user ask moves (see Section 3.6.6); instead of
pushing an issue Q on ISSU...

**Algorithm:**

```
rule 5.2).
(rule 5.2) rule: rejectAction
class: select action
in($/private/nim, request(A))
pre: $/shared/lu/speaker=usr
8
>< not $domain :: plan(A, Plan)
del(/private/nim, request(A))
>:
eff: push(/private/agenda, icm:und*pos:usr*action(A))
8
>< push(/private/agenda, icm:acc*neg:action(A))
>:
```

**Context After:**
> 5.6.2 Executing device actions
The update rule for executing the dev do device action is shown in (rule 5.3)....

---

## Algorithm 123: rule 5 .2) rule: rejectAction

**Section:** 5.6.2 Executing device actions
**Page:** 238

**Context Before:**
> n(A)))
push(/shared/actions, A)
>>>>>>>>>>>:
push(/private/agenda, A)
This rule is similar to that for integrating user ask moves (see Section 3.6.6); instead of
pushing an issue Q on ISSUES and QUD, ...

**Algorithm:**

```
rule 5.2) rule: rejectAction
class: select action
in($/private/nim, request(A))
pre: $/shared/lu/speaker=usr
8
>< not $domain :: plan(A, Plan)
del(/private/nim, request(A))
>:
eff: push(/private/agenda, icm:und*pos:usr*action(A))
8
>< push(/private/agenda, icm:acc*neg:action(A))
>:
```

**Context After:**
> 5.6.2 Executing device actions
The update rule for executing the dev do device action is shown in (rule 5.3)....

---

## Algorithm 124: rule 5 .3) rule: exec dev do

**Section:** 5.6.3 Selecting and integrating conflrm-moves
**Page:** 239

**Context Before:**
> 5.6. UPDATE RULES AND DIALOGUE EXAMPLES 217
(...

**Algorithm:**

```
rule 5.3) rule: exec dev do
class: exec plan
pre: fst($/private/plan, dev do(Dev, A ))
dev
n pop(/private/plan)
! $/shared/com=PropSet
eff: 8
>>>< devices/Dev :: dev do(PropSet, A
dev
)
add(/private/bel, done(A ))
dev
>>>:
The condition looks for a dev do upnp action in the plan, with arguments Dev, the device
path name, and A , the device action. The updates pop the action ofi the plan, and
dev
applies the corresponding update dev do(PropSet, A ) to the device Dev. Finally, the
dev
proposition done(A ) is added the the private beliefs.
dev
In addition, we have implemented rules for executing the dev get, dev set and dev query
actions.
```

**Context After:**
> 5.6.3 Selecting and integrating conflrm-moves
The selection rule for the conflrm action is shown in (rule 5.4).
(rule 5.4) rule: selectConflrmAction
class: select action
fst($/shared/actions, A)
$doma...

---

## Algorithm 125: rule 5 .4).

**Section:** 5.6.3 Selecting and integrating conflrm-moves
**Page:** 239

**Context Before:**
> r a dev do upnp action in the plan, with arguments Dev, the device
path name, and A , the device action. The updates pop the action ofi the plan, and
dev
applies the corresponding update dev do(PropSe...

**Algorithm:**

```
rule 5.4).
(rule 5.4) rule: selectConflrmAction
class: select action
fst($/shared/actions, A)
$domain :: postcond(A, PC)
pre: 8
>>>< in($/private/bel, PC)
not in($/shared/com, PC)
eff:
>>>:
push(/private/agenda, conflrm(A))
n
The conditions in this rule check that the there is an action in /shared/actions whose
postcondition is believed by the system to be true, however, this is not yet shared infor-
mation. If this is true, a conflrm action is pushed on the agenda. Eventually, this action
(which also is a dialogue move) is moved to next moves by (rule 5.5).
```

**Context After:**
> (rule 5.5) rule: selectConflrm
class: select move
pre: fst($/private/agenda, conflrm(A))
n push(next moves, conflrm(A))
eff:
pop(/private/agenda)
(...

---

## Algorithm 126: rule 5 .4) rule: selectConflrmAction

**Section:** 5.6.3 Selecting and integrating conflrm-moves
**Page:** 239

**Context Before:**
> pnp action in the plan, with arguments Dev, the device
path name, and A , the device action. The updates pop the action ofi the plan, and
dev
applies the corresponding update dev do(PropSet, A ) to th...

**Algorithm:**

```
rule 5.4) rule: selectConflrmAction
class: select action
fst($/shared/actions, A)
$domain :: postcond(A, PC)
pre: 8
>>>< in($/private/bel, PC)
not in($/shared/com, PC)
eff:
>>>:
push(/private/agenda, conflrm(A))
n
The conditions in this rule check that the there is an action in /shared/actions whose
postcondition is believed by the system to be true, however, this is not yet shared infor-
mation. If this is true, a conflrm action is pushed on the agenda. Eventually, this action
(which also is a dialogue move) is moved to next moves by (rule 5.5).
```

**Context After:**
> (rule 5.5) rule: selectConflrm
class: select move
pre: fst($/private/agenda, conflrm(A))
n push(next moves, conflrm(A))
eff:
pop(/private/agenda)
(...

---

## Algorithm 127: rule 5 .5).

**Section:** 5.6.3 Selecting and integrating conflrm-moves
**Page:** 239

**Context Before:**
> select action
fst($/shared/actions, A)
$domain :: postcond(A, PC)
pre: 8
>>>< in($/private/bel, PC)
not in($/shared/com, PC)
eff:
>>>:
push(/private/agenda, conflrm(A))
n
The conditions in this rule c...

**Algorithm:**

```
rule 5.5).
(rule 5.5) rule: selectConflrm
class: select move
pre: fst($/private/agenda, conflrm(A))
n push(next moves, conflrm(A))
eff:
pop(/private/agenda)
(
```

---

## Algorithm 128: rule 5 .5) rule: selectConflrm

**Section:** 5.6.3 Selecting and integrating conflrm-moves
**Page:** 239

**Context Before:**
> on
fst($/shared/actions, A)
$domain :: postcond(A, PC)
pre: 8
>>>< in($/private/bel, PC)
not in($/shared/com, PC)
eff:
>>>:
push(/private/agenda, conflrm(A))
n
The conditions in this rule check that t...

**Algorithm:**

```
rule 5.5) rule: selectConflrm
class: select move
pre: fst($/private/agenda, conflrm(A))
n push(next moves, conflrm(A))
eff:
pop(/private/agenda)
(
```

---

## Algorithm 129: rule 5 .6).

**Section:** 5.6.4 Dialogue example: menu traversal and multiple threads
**Page:** 240

**Context Before:**
> 218 CHAPTER 5. ACTION-ORIENTED AND NEGOTIATIVE DIALOGUE
When the conflrmation move has been made, it is integrated by the rule in (...

**Algorithm:**

```
rule 5.6).
(rule 5.6) rule: integrateConflrm
class: integrate
pre: $/private/nim/fst/snd=conflrm(A)
n pop(/private/nim)
eff:
add(/shared/com, done(A))
(
This rule adds the proposition done(A) to the shared commitments which enables the
downdateActions rule in (rule 5.7) to trigger.
(rule 5.7) rule: downdateActions
```

**Context After:**
> class: downdate issues
fst($/shared/actions, A)
pre: $domain :: postcond(A, PC)
8
>< in($/shared/com, PC )
eff: >: pop(/shared/actions)
n
This rule removes an action A whose postcondition is jointly b...

---

## Algorithm 130: rule 5 .6) rule: integrateConflrm

**Section:** 5.6.4 Dialogue example: menu traversal and multiple threads
**Page:** 240

**Context Before:**
> 218 CHAPTER 5. ACTION-ORIENTED AND NEGOTIATIVE DIALOGUE
When the conflrmation move has been made, it is integrated by the rule in (rule 5.6).
(...

**Algorithm:**

```
rule 5.6) rule: integrateConflrm
class: integrate
pre: $/private/nim/fst/snd=conflrm(A)
n pop(/private/nim)
eff:
add(/shared/com, done(A))
(
This rule adds the proposition done(A) to the shared commitments which enables the
downdateActions rule in (rule 5.7) to trigger.
(rule 5.7) rule: downdateActions
class: downdate issues
fst($/shared/actions, A)
pre: $domain :: postcond(A, PC)
8
>< in($/shared/com, PC )
eff: >: pop(/shared/actions)
n
This rule removes an action A whose postcondition is jointly believed to be true from
actions2.
```

**Context After:**
> 5.6.4 Dialogue example: menu traversal and multiple threads
In (dialogue 5.1) we show a sample dialogue interaction with the menu-based VCR
application. It shows both menu traversal and accommodation,...

---

## Algorithm 131: rule 5 .7) to trigger.

**Section:** 5.6.4 Dialogue example: menu traversal and multiple threads
**Page:** 240

**Context Before:**
> 218 CHAPTER 5. ACTION-ORIENTED AND NEGOTIATIVE DIALOGUE
When the conflrmation move has been made, it is integrated by the rule in (rule 5.6).
(rule 5.6) rule: integrateConflrm
class: integrate
pre: $/...

**Algorithm:**

```
rule 5.7) to trigger.
(rule 5.7) rule: downdateActions
class: downdate issues
fst($/shared/actions, A)
pre: $domain :: postcond(A, PC)
8
>< in($/shared/com, PC )
eff: >: pop(/shared/actions)
n
This rule removes an action A whose postcondition is jointly believed to be true from
actions2.
```

**Context After:**
> 5.6.4 Dialogue example: menu traversal and multiple threads
In (dialogue 5.1) we show a sample dialogue interaction with the menu-based VCR
application. It shows both menu traversal and accommodation,...

---

## Algorithm 132: rule 5 .7) rule: downdateActions

**Section:** 5.6.4 Dialogue example: menu traversal and multiple threads
**Page:** 240

**Context Before:**
> 218 CHAPTER 5. ACTION-ORIENTED AND NEGOTIATIVE DIALOGUE
When the conflrmation move has been made, it is integrated by the rule in (rule 5.6).
(rule 5.6) rule: integrateConflrm
class: integrate
pre: $/...

**Algorithm:**

```
rule 5.7) rule: downdateActions
class: downdate issues
fst($/shared/actions, A)
pre: $domain :: postcond(A, PC)
8
>< in($/shared/com, PC )
eff: >: pop(/shared/actions)
n
This rule removes an action A whose postcondition is jointly believed to be true from
actions2.
```

**Context After:**
> 5.6.4 Dialogue example: menu traversal and multiple threads
In (dialogue 5.1) we show a sample dialogue interaction with the menu-based VCR
application. It shows both menu traversal and accommodation,...

---

## Algorithm 133: rule 5 .8) rule: accommodateAction

**Section:** 5.6. UPDATE RULES AND DIALOGUE EXAMPLES 221
**Page:** 243

**Context Before:**
> 5.6. UPDATE RULES AND DIALOGUE EXAMPLES 221
(...

**Algorithm:**

```
rule 5.8) rule: accommodateAction
class: accommodate
setof(A, $/private/nim/elem/snd=answer(A), AnsSet)
$$arity(AnsSet) > 0
8
pre:
>>>>>>>>>>>>>>>>>><
$
$
fo
d
d
r
o
o
a
$
l
m
m
d
l(
o
a
a
in
m
i
i
(
n
n
A
a
:
:
i
n
:
:
n
s
a
p
S
:
c
l
:
a
e
t
r
i
n
t
o
e
,
(
n
l
A
A
e
(
v
c
A
)
a
t
,
c
i
n
i
o
t
n
t
i
n
(
(
o
A
,
P
n
P
,
)
la
Q
l
n
a
)
n
,
)
)
flndout(Q)) and
not $domain :: plan(Action0, Plan0) and Action06=Action and
>>>>>>>>>>>>>>>>>>:
p
n
u
o
s
t
f
$
h
o
i
d
(
n
r
/
o
a
(
s
$
l
m
l
h
/
(
a
a
i
p
n
i
r
r
(
n
A
i
e
v
:
d
n
a
:
/
s
t
r
a
S
e
e
c
l
e
/
e
t
t
a
v
,
i
a
g
o
A
n
e
n
t
)
n
(
,
s
A
d
,
in
a
,
A
(
,
Q
P
ct
i
)
c
l
i
)
a
m
o
n
n
:u
0
)
,
n
fl
d
n
*
d
in
o
t
u
:u
t(
s
Q
r*
)
a
)
c
a
ti
n
o
d
n(Action))
push(/private/agenda, icm:accommodate:Action)
8
eff: >>>>>>< p
se
u
t
s
(
h
/
(
p
/
r
p
i
r
v
i
a
v
t
a
e
t
/
e
p
/
l
a
a
g
n
e
,
n
P
d
l
a
a
,
n
i
)
cm:und*pos:usr*action(action))
push(/private/agenda, icm:loadplan)
>>>>>>:
ThisruleisverysimilartotheaccommodateDependentIssue(seeSection4.6.4), except
that it accommodates a dependent action rather than a dependent issue.
Ifthesystemflndsseveralactionsmatchingtheinformationgivenbytheuser,aclariflcation
question is raised. This is again similar to the behaviour for issues described in Section
4.6.5; in fact, the rule below replaces the previous clarifyDependentIssue rule.
(rule 5.9) rule: clarifyIssueAction
```

**Context After:**
> class: select action
in($/private/nim, pair(usr, answer(A)))
setof(Action, $domain :: depends(fi, Q) and
8
pre: >>>>>><
rem
$
o
d
v
o
e
m
u
a
n
i
i
n
fla
:
b
:
le
re
s(
le
A
v
c
a
t
n
i
t
o
(
n
A
s
,
...

---

## Algorithm 134: rule 5 .9) rule: clarifyIssueAction

**Section:** 5.6. UPDATE RULES AND DIALOGUE EXAMPLES 221
**Page:** 243

**Context Before:**
> ,
n
P
d
l
a
a
,
n
i
)
cm:und*pos:usr*action(action))
push(/private/agenda, icm:loadplan)
>>>>>>:
ThisruleisverysimilartotheaccommodateDependentIssue(seeSection4.6.4), except
that it accommodates a dep...

**Algorithm:**

```
rule 5.9) rule: clarifyIssueAction
class: select action
in($/private/nim, pair(usr, answer(A)))
setof(Action, $domain :: depends(fi, Q) and
8
pre: >>>>>><
rem
$
o
d
v
o
e
m
u
a
n
i
i
n
fla
:
b
:
le
re
s(
le
A
v
c
a
t
n
i
t
o
(
n
A
s
,
,
Q
Ac
),
ti
A
on
ct
s
i
0
o
)
nSet)
$$arity(Actions0) > 1
>>>>>>:
! setof(?IssueProp, in(Actions0, Issue0) and
not $domain :: action(Issue0) and
8
eff:
>>>>>>>>>>>>><
! se
I
$
t
d
s
o
s
f
o
(
u
m
?
e
A
P
a
c
i
r
t
n
o
io
p
:
n
:
=
P
a
is
c
r
s
t
o
u
i
p
e
o
(
,
n
I
i
(
n
s
A
s
(
c
u
A
t
e
i
c
0
o
t
)
n
i
,
o
0
I
n
)
s
s
a
s
0
n
,
u
d
A
eQ
ct
u
i
e
o
s
n
t
0
i
)
o
a
n
n
s
d
)
ActionProp=action(Action), ActionQuestions)
>>>>>>>>>>>>>:
p
!
u
u
s
n
h
i
(
o
/
n
p
(
r
Is
iv
s
a
u
t
eQ
e/
u
a
e
g
st
e
i
n
on
d
s
a
,
,
A
fl
c
n
t
d
i
o
on
ut
Q
(A
ue
lt
s
Q
ti
)
o
)
ns, AltQ)
```

---

## Algorithm 135: Procedure/Rule in 5.8.2 Rejection, negotiation and downshifting

**Section:** 5.8.2 Rejection, negotiation and downshifting
**Page:** 254

**Algorithm:**

```
232 CHAPTER 5. ACTION-ORIENTED AND NEGOTIATIVE DIALOGUE
5.8.2 Rejection, negotiation and downshifting
In the context of discussing referent identiflcation in instructional assembly dialogues,
Cohen (1981) makes an analogy between shifts in dialogue strategy and shifting gears
when driving a car. In a dialogue in high gear, the speaker introduces several subgoals
in each utterance, whereas fewer goals are introduced in low-gear dialogue. The type of
subgoals discussed by Cohen are mainly identifying a referent, requests to pick up objects,
and requesting an assembly action. As long as the dialogue proceeds smoothly and the
hearer is able to correctly identify referents and carry out actions, the speaker requests
assembly actions and expects the hearer to be able to identify and pick up the objects
referred to without explicit requests for this. However, when this fails and the hearer fails
to identify a referent, the speaker may shift into a lower gear (downshift) and make explicit
requests for identiflcation of referents. At a later stage, the speaker may shift to a higher
gear and request the hearer to pick up an object and then to perform an assembly action.
Finally, the speaker may return to the initial gear and only make requests for assembly
actions.
Severinsson (1983) views to the process of downshifting as making latent subgames into
explicit subgames. In the case mentioned above, the goals of the latent subgames are (1)
to get the hearer to identify a referent, and (2) for the hearer to pick up the object referred
to. In high gear, these subgames are latent in the sense that they do not give rise to any
utterances (dialogue moves). When the latent subgames become explicit, the process that
was previously carried out silently is instead carried out using utterances.
This view flts well with the concept of tacit moves introduced in Section 4.4.2. Updates for
latent referent identiflcation and utterance acceptance can be regarded as tacit moves (or
games) corresponding to explicit referent identiflcation or negotiation subdialogues, similar
to the way that question accommodation updates are tacit moves corresponding to the ask
dialogue moves.
Both these notions, shifting gears in dialogue and latent subgames, are useful for shedding
light on the relation between negotiative dialogue and utterance acceptance. Firstly, the
notions of optimism and pessimism regarding grounding strategies seem intimately related
to the notion of gears, both metaphorically and factually. Metaphorically, we may say that
an optimistic driver will use a higher gear than a pessimistic one; only when she encounters
a bumpy road will she shift into lower gear (thus taking a more pessimistic approach).
Later, when the road becomes smoother, she may again resume her optimistic strategy
and use a higher gear. Similarly, speakers can be expected to switch between higher and
lower gears, and between optimistic and pessimistic grounding strategies regarding the
grounding of their utterances. Thus we claim that the notion of shifting gears is applicable
not only to referent identiflcation, but also to other grounding related games, including
utterance acceptance.
```

---

## Algorithm 136: 1 n

**Section:** 68. Lund : CWK Gleerup.
**Page:** 291

**Context Before:**
> A.3. METHODS FOR ACCESSING THE TIS 269
(A.15) Obj ! $TISvar
Objectscanalsobespecifledusingevaluationoffunctions; thefunctionevaluationoperator
is denoted \$$". Given a function Fun taking arguments Ar...

**Algorithm:**

```
rule
1 n
in (A.16) allows specifying an object by applying Fun to Obj ;:::;Obj .
1 n
(A.16) Obj ! $$Fun(Obj ;:::;Obj )
1 n
By using paths, built up by selectors, it is possible to \point" at an object embedded at the
corresponding location inside a (complex) object and inspect or manipulate it. Paths thus
appear in two contexts: inspection, where they specify objects, and manipulation, where
they specify locations.
An object X can be specifled by a complex object and a selector Sel pointing out X inside
the complex object. The syntax rule for pointing out embedded objects using selectors is
shown in (A.17).
(A.17) Obj ! Obj=Sel
This recursive deflnition allows selectors to be iteratively applied to objects, using expres-
sions of the form Obj=Sel =Sel :::=Sel ; this is equivalent to (:::((Obj=Sel )=Sel ):::
1 2 n 1 2
=Sel ).
n
Another basic concept in TrindiKit is that of locations in objects. The general syntax
for locations is shown in (A.18); here, Sel is a selector and Obj is a complex object (a
collection).
(A.18) Loc ! Loc=Sel
Loc ! TISvar
Again, the recursive deflnition allows selectors to be iteratively applied, using expressions
of the form TISvar=Sel =Sel :::=Sel ; this is equivalent to (:::((TISvar=Sel )=Sel ):::
1 2 n 1 2
=Sel ).
n
For example, assume we have a TIS where the information state proper (the IS variable)
has the type given in (A.19) and the value given in (1.19.) (This examples assumes there
are deflnitions of the types Proposition and Topic.)
beliefs : Set(Proposition)
(A.19) is :
topics = Stack(Topic)
" #
beliefs = f happy(sys), frustrated(usr) g
(A.20) is =
topics = h the weather, foreign politics i
" #
```

---

## Algorithm 137: Procedure/Rule in 13. SubAlg

**Section:** 13. SubAlg
**Page:** 298

**Algorithm:**

```
276 APPENDIX A. TRINDIKIT FUNCTIONALITY
1. Rule
apply the update rule Rule
2. RuleClass
apply an update rule of class RuleClass; rules are tried in the order they are declared
3. [R ;:::;R ]
1 n
execute R ;:::;R in sequence
1 n
4. if C then S else T
If C is true of the TIS, execute S; otherwise, execute T
5. while C do R
while C is true of the TIS, execute R repeatedly
6. repeat R until C
execute R repeatedly until C is true of the TIS
7. repeat R
execute R repeatedly until it fails; report no error when it fails
8. repeat+ R
execute R repeatedly, but at least once, until it fails; report no error when it fails
9. try R
try to execute R; if it fails, report no error
10. R orelse S
Try to execute R; if it fails, report no error and execute S instead
11. test C
if C is true of the TIS, do nothing; otherwise, halt execution of the current algorithm
12. apply Op
apply operation Op
13. SubAlg
execute subalgorithm SubAlg
Subalgorithms are declared using ), which is preceded by the subalgorithm name and
followed by the algorithm, as in (A.33).
(A.33) main update ) h grounding,
repeat+ ( integrate orelse accommodate ) i
```

---

## Algorithm 138: rule 3 .1) (p. 41)

**Section:** 13. SubAlg
**Page:** 303

**Context Before:**
> ppendix lists rule classes used by the various versions of IBiS. Rules are listed in
the order they are tried when the corresponding rule class is called in a module algorithm.
The IBiS systems and Tr...

**Algorithm:**

```
rule 3.1) (p. 41)
† integrate
1. integrateUsrAsk (rule 3.3) (p. 44)
2. integrateSysAsk (rule 3.2) (p. 43)
3. integrateAnswer (rule 3.4) (p. 47)
4. integrateGreet (rule 3.6) (p. 48)
5. integrateSysQuit (rule 3.8) (p. 49)
281
```

---

## Algorithm 139: rule 3 .3) (p. 44)

**Section:** 13. SubAlg
**Page:** 303

**Context Before:**
> sions of IBiS. Rules are listed in
the order they are tried when the corresponding rule class is called in a module algorithm.
The IBiS systems and TrindiKit can be downloaded from:
http://www.ling.gu...

**Algorithm:**

```
rule 3.3) (p. 44)
2. integrateSysAsk (rule 3.2) (p. 43)
3. integrateAnswer (rule 3.4) (p. 47)
4. integrateGreet (rule 3.6) (p. 48)
5. integrateSysQuit (rule 3.8) (p. 49)
281
```

---

## Algorithm 140: rule 3 .2) (p. 43)

**Section:** 13. SubAlg
**Page:** 303

**Context Before:**
> order they are tried when the corresponding rule class is called in a module algorithm.
The IBiS systems and TrindiKit can be downloaded from:
http://www.ling.gu.se/~sl/Thesis.
The size of the systems...

**Algorithm:**

```
rule 3.2) (p. 43)
3. integrateAnswer (rule 3.4) (p. 47)
4. integrateGreet (rule 3.6) (p. 48)
5. integrateSysQuit (rule 3.8) (p. 49)
281
```

---

## Algorithm 141: rule 3 .7) (p. 48)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (...

**Algorithm:**

```
rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p. 64)
2. flndPlan (rule 3.9) (p. 49)
† exec plan
1. removeFindout (rule 3.10) (p. 50)
2. removeRaise (rule 3.19) (p. 66)
3. exec consultDB (rule 3.11) (p. 50)
```

**Context After:**
> B.1.2 IBiS1 select module
† select action
1. selectRespond (rule 3.14) (p. 53)
2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 5...

---

## Algorithm 142: rule 3 .5) (p. 48)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (...

**Algorithm:**

```
rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p. 64)
2. flndPlan (rule 3.9) (p. 49)
† exec plan
1. removeFindout (rule 3.10) (p. 50)
2. removeRaise (rule 3.19) (p. 66)
3. exec consultDB (rule 3.11) (p. 50)
B.1.2 IBiS1 select module
† select action
1. selectRespond (rule 3.14) (p. 53)
```

**Context After:**
> 2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update...

---

## Algorithm 143: rule 3 .16) (p. 63)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (...

**Algorithm:**

```
rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p. 64)
2. flndPlan (rule 3.9) (p. 49)
† exec plan
1. removeFindout (rule 3.10) (p. 50)
2. removeRaise (rule 3.19) (p. 66)
3. exec consultDB (rule 3.11) (p. 50)
B.1.2 IBiS1 select module
† select action
1. selectRespond (rule 3.14) (p. 53)
```

**Context After:**
> 2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update...

---

## Algorithm 144: rule 3 .17) (p. 64)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (...

**Algorithm:**

```
rule 3.17) (p. 64)
2. flndPlan (rule 3.9) (p. 49)
† exec plan
1. removeFindout (rule 3.10) (p. 50)
2. removeRaise (rule 3.19) (p. 66)
3. exec consultDB (rule 3.11) (p. 50)
B.1.2 IBiS1 select module
† select action
1. selectRespond (rule 3.14) (p. 53)
2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
```

**Context After:**
> † select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)...

---

## Algorithm 145: rule 3 .9) (p. 49)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p....

**Algorithm:**

```
rule 3.9) (p. 49)
† exec plan
1. removeFindout (rule 3.10) (p. 50)
2. removeRaise (rule 3.19) (p. 66)
3. exec consultDB (rule 3.11) (p. 50)
B.1.2 IBiS1 select module
† select action
1. selectRespond (rule 3.14) (p. 53)
2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
```

**Context After:**
> 2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)...

---

## Algorithm 146: rule 3 .10) (p. 50)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p....

**Algorithm:**

```
rule 3.10) (p. 50)
2. removeRaise (rule 3.19) (p. 66)
3. exec consultDB (rule 3.11) (p. 50)
B.1.2 IBiS1 select module
† select action
1. selectRespond (rule 3.14) (p. 53)
2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
```

**Context After:**
> 3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)...

---

## Algorithm 147: rule 3 .19) (p. 66)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p....

**Algorithm:**

```
rule 3.19) (p. 66)
3. exec consultDB (rule 3.11) (p. 50)
B.1.2 IBiS1 select module
† select action
1. selectRespond (rule 3.14) (p. 53)
2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)
```

---

## Algorithm 148: rule 3 .11) (p. 50)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p....

**Algorithm:**

```
rule 3.11) (p. 50)
B.1.2 IBiS1 select module
† select action
1. selectRespond (rule 3.14) (p. 53)
2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)
```

---

## Algorithm 149: rule 3 .14) (p. 53)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p....

**Algorithm:**

```
rule 3.14) (p. 53)
2. selectFromPlan (rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)
```

---

## Algorithm 150: rule 3 .12) (p. 51)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p....

**Algorithm:**

```
rule 3.12) (p. 51)
3. reraiseIssue (rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)
```

---

## Algorithm 151: rule 3 .18) (p. 65)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> 282 APPENDIX B. RULES AND CLASSES
6. integrateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p....

**Algorithm:**

```
rule 3.18) (p. 65)
† select move
1. selectAnswer (rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)
```

---

## Algorithm 152: rule 3 .15) (p. 54)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> rateUsrQuit (rule 3.7) (p. 48)
† downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p. 64)
2. flndPlan (rule 3.9) (p. 49)
† exec...

**Algorithm:**

```
rule 3.15) (p. 54)
2. selectAsk (rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)
```

---

## Algorithm 153: rule 3 .13) (p. 52)

**Section:** 13. SubAlg
**Page:** 304

**Context Before:**
> downdate qud
1. downdateQUD (rule 3.5) (p. 48)
2. downdateQUD2 (rule 3.16) (p. 63)
† load plan
1. recoverPlan (rule 3.17) (p. 64)
2. flndPlan (rule 3.9) (p. 49)
† exec plan
1. removeFindout (rule 3.10...

**Algorithm:**

```
rule 3.13) (p. 52)
3. selectOther
B.2 IBiS2
B.2.1 IBiS2 update module
† grounding
{ getLatestMoves (rule 4.16) (p. 130)
```

---

## Algorithm 154: rule 4 .1) (p. 110)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (...

**Algorithm:**

```
rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. integrateUsrAnswer (rule 4.4) (p. 113)
6. integrateSysAnswer (rule 4.19) (p. 132)
7. integrateUndIntICM (rule 4.6) (p. 115)
8. integrateUsrPerNegICM (rule 4.20) (p. 133)
9. integrateUsrAccNegICM (rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 155: rule 4 .18) (p. 132)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (...

**Algorithm:**

```
rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. integrateUsrAnswer (rule 4.4) (p. 113)
6. integrateSysAnswer (rule 4.19) (p. 132)
7. integrateUndIntICM (rule 4.6) (p. 115)
8. integrateUsrPerNegICM (rule 4.20) (p. 133)
9. integrateUsrAccNegICM (rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 156: rule 4 .7) (p. 115)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (...

**Algorithm:**

```
rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. integrateUsrAnswer (rule 4.4) (p. 113)
6. integrateSysAnswer (rule 4.19) (p. 132)
7. integrateUndIntICM (rule 4.6) (p. 115)
8. integrateUsrPerNegICM (rule 4.20) (p. 133)
9. integrateUsrAccNegICM (rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 157: rule 4 .8) (p. 116)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (...

**Algorithm:**

```
rule 4.8) (p. 116)
5. integrateUsrAnswer (rule 4.4) (p. 113)
6. integrateSysAnswer (rule 4.19) (p. 132)
7. integrateUndIntICM (rule 4.6) (p. 115)
8. integrateUsrPerNegICM (rule 4.20) (p. 133)
9. integrateUsrAccNegICM (rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 158: rule 4 .4) (p. 113)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. i...

**Algorithm:**

```
rule 4.4) (p. 113)
6. integrateSysAnswer (rule 4.19) (p. 132)
7. integrateUndIntICM (rule 4.6) (p. 115)
8. integrateUsrPerNegICM (rule 4.20) (p. 133)
9. integrateUsrAccNegICM (rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 159: rule 4 .19) (p. 132)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. i...

**Algorithm:**

```
rule 4.19) (p. 132)
7. integrateUndIntICM (rule 4.6) (p. 115)
8. integrateUsrPerNegICM (rule 4.20) (p. 133)
9. integrateUsrAccNegICM (rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 160: rule 4 .6) (p. 115)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. i...

**Algorithm:**

```
rule 4.6) (p. 115)
8. integrateUsrPerNegICM (rule 4.20) (p. 133)
9. integrateUsrAccNegICM (rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 161: rule 4 .20) (p. 133)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. i...

**Algorithm:**

```
rule 4.20) (p. 133)
9. integrateUsrAccNegICM (rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 162: rule 4 .21) (p. 135)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. i...

**Algorithm:**

```
rule 4.21) (p. 135)
10. integrateOtherICM (rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
```

**Context After:**
> 2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 163: rule 4 .10) (p. 121)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> B.2. IBIS2 283
† integrate
1. integrateUsrAsk (rule 4.1) (p. 110)
2. integrateSysAsk (rule 4.18) (p. 132)
3. integrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. i...

**Algorithm:**

```
rule 4.10) (p. 121)
11. integrateGreet
12. integrateSysQuit
13. integrateUsrQuit
14. integrateNoMove
† downdate qud
{ downdateQUD
{ downdateQUD2
† load plan
1. recoverPlan (rule 4.24) (p. 143)
2. flndPlan (rule 4.23) (p. 143)
```

**Context After:**
> † exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup...

---

## Algorithm 164: rule 4 .24) (p. 143)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> tegrateNegIcmAnswer (rule 4.7) (p. 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. integrateUsrAnswer (rule 4.4) (p. 113)
6. integrateSysAnswer (rule 4.19) (p. 132)
7. integrateUndIntICM (rule 4....

**Algorithm:**

```
rule 4.24) (p. 143)
2. flndPlan (rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup
```

---

## Algorithm 165: rule 4 .23) (p. 143)

**Section:** 13. SubAlg
**Page:** 305

**Context Before:**
> . 115)
4. integratePosIcmAnswer (rule 4.8) (p. 116)
5. integrateUsrAnswer (rule 4.4) (p. 113)
6. integrateSysAnswer (rule 4.19) (p. 132)
7. integrateUndIntICM (rule 4.6) (p. 115)
8. integrateUsrPerNeg...

**Algorithm:**

```
rule 4.23) (p. 143)
† exec plan
1. removeFindout
2. exec consultDB
† (none)
{ irrelevantFollowup (rule 4.22) (p. 141)
{ unclearFollowup
```

---

## Algorithm 166: rule 4 .15) (p. 129)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (...

**Algorithm:**

```
rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIcmUndIntAnswer (rule 4.5) (p. 114)
5. selectRespond (rule 4.26) (p. 147)
6. selectFromPlan
7. reraiseIssue (rule 4.25) (p. 144)
† select icm
1. selectIcmConNeg (rule 4.9) (p. 120)
2. selectIcmPerNeg (rule 4.11) (p. 121)
3. selectIcmSemNeg (rule 4.12) (p. 122)
```

**Context After:**
> 4. selectIcmUndNeg (rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (no...

---

## Algorithm 167: rule 4 .14) (p. 127)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (...

**Algorithm:**

```
rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIcmUndIntAnswer (rule 4.5) (p. 114)
5. selectRespond (rule 4.26) (p. 147)
6. selectFromPlan
7. reraiseIssue (rule 4.25) (p. 144)
† select icm
1. selectIcmConNeg (rule 4.9) (p. 120)
2. selectIcmPerNeg (rule 4.11) (p. 121)
3. selectIcmSemNeg (rule 4.12) (p. 122)
4. selectIcmUndNeg (rule 4.13) (p. 123)
```

**Context After:**
> 5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
...

---

## Algorithm 168: rule 4 .3) (p. 112)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (...

**Algorithm:**

```
rule 4.3) (p. 112)
4. selectIcmUndIntAnswer (rule 4.5) (p. 114)
5. selectRespond (rule 4.26) (p. 147)
6. selectFromPlan
7. reraiseIssue (rule 4.25) (p. 144)
† select icm
1. selectIcmConNeg (rule 4.9) (p. 120)
2. selectIcmPerNeg (rule 4.11) (p. 121)
3. selectIcmSemNeg (rule 4.12) (p. 122)
4. selectIcmUndNeg (rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
```

**Context After:**
> † select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† ...

---

## Algorithm 169: rule 4 .5) (p. 114)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIc...

**Algorithm:**

```
rule 4.5) (p. 114)
5. selectRespond (rule 4.26) (p. 147)
6. selectFromPlan
7. reraiseIssue (rule 4.25) (p. 144)
† select icm
1. selectIcmConNeg (rule 4.9) (p. 120)
2. selectIcmPerNeg (rule 4.11) (p. 121)
3. selectIcmSemNeg (rule 4.12) (p. 122)
4. selectIcmUndNeg (rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
```

**Context After:**
> 2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves...

---

## Algorithm 170: rule 4 .26) (p. 147)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIc...

**Algorithm:**

```
rule 4.26) (p. 147)
6. selectFromPlan
7. reraiseIssue (rule 4.25) (p. 144)
† select icm
1. selectIcmConNeg (rule 4.9) (p. 120)
2. selectIcmPerNeg (rule 4.11) (p. 121)
3. selectIcmSemNeg (rule 4.12) (p. 122)
4. selectIcmUndNeg (rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
```

**Context After:**
> 2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves...

---

## Algorithm 171: rule 4 .25) (p. 144)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIc...

**Algorithm:**

```
rule 4.25) (p. 144)
† select icm
1. selectIcmConNeg (rule 4.9) (p. 120)
2. selectIcmPerNeg (rule 4.11) (p. 121)
3. selectIcmSemNeg (rule 4.12) (p. 122)
4. selectIcmUndNeg (rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
```

**Context After:**
> † (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves...

---

## Algorithm 172: rule 4 .9) (p. 120)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIc...

**Algorithm:**

```
rule 4.9) (p. 120)
2. selectIcmPerNeg (rule 4.11) (p. 121)
3. selectIcmSemNeg (rule 4.12) (p. 122)
4. selectIcmUndNeg (rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
```

**Context After:**
> B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves...

---

## Algorithm 173: rule 4 .11) (p. 121)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIc...

**Algorithm:**

```
rule 4.11) (p. 121)
3. selectIcmSemNeg (rule 4.12) (p. 122)
4. selectIcmUndNeg (rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
```

**Context After:**
> B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves...

---

## Algorithm 174: rule 4 .12) (p. 122)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIc...

**Algorithm:**

```
rule 4.12) (p. 122)
4. selectIcmUndNeg (rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves
```

---

## Algorithm 175: rule 4 .13) (p. 123)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 284 APPENDIX B. RULES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIc...

**Algorithm:**

```
rule 4.13) (p. 123)
5. selectIcmOther (rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves
```

---

## Algorithm 176: rule 4 .2) (p. 111)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> LES AND CLASSES
B.2.2 IBiS2 select module
† select action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIcmUndIntAnswer (rul...

**Algorithm:**

```
rule 4.2) (p. 111)
† select move
1. selectAnswer (rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves
```

---

## Algorithm 177: rule 4 .27) (p. 147)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> action
1. rejectIssue (rule 4.15) (p. 129)
2. rejectProp (rule 4.14) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIcmUndIntAnswer (rule 4.5) (p. 114)
5. selectRespond (rule 4.26) (p. 14...

**Algorithm:**

```
rule 4.27) (p. 147)
2. selectAsk
3. selectOther
4. selectIcmOther (rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves
```

---

## Algorithm 178: rule 4 .2) (p. 111)

**Section:** 13. SubAlg
**Page:** 306

**Context Before:**
> 4) (p. 127)
3. selectIcmUndIntAsk (rule 4.3) (p. 112)
4. selectIcmUndIntAnswer (rule 4.5) (p. 114)
5. selectRespond (rule 4.26) (p. 147)
6. selectFromPlan
7. reraiseIssue (rule 4.25) (p. 144)
† select...

**Algorithm:**

```
rule 4.2) (p. 111)
† (none)
{ backupShared (rule 4.17) (p. 131)
B.3 IBiS3
B.3.1 IBiS3 update module
† grounding
{ getLatestMoves
```

---

## Algorithm 179: rule 5 .7) (p. 180)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> B.3. IBIS3 285
† integrate
1. retract (...

**Algorithm:**

```
rule 5.7) (p. 180)
2. integrateUsrAsk
3. integrateSysAsk
4. integrateNegIcmAnswer (rule 5.10) (p. 184)
5. integratePosIcmAnswer (rule 5.11) (p. 189)
6. integrateUsrAnswer
7. integrateSysAnswer
8. integrateAccommodationICM
9. integrateUndPosICM
10. integrateUndIntICM
11. integrateUsrPerNegICM
12. integrateUsrAccNegICM
13. integrateOtherICM
14. integrateGreet
15. integrateSysQuit
16. integrateUsrQuit
17. integrateNoMove
† accommodate
1. accommodateIssues2QUD (rule 5.2) (p. 169)
```

**Context After:**
> 2. accommodateQUD2Issues (rule 5.9) (p. 183)
3. accommodatePlan2Issues (rule 5.1) (p. 166)
4. accommodateCom2Issues (rule 5.6) (p. 179)
5. accommodateCom2IssuesDependent (rule 5.8) (p. 182)
6. accommo...

---

## Algorithm 180: rule 5 .10) (p. 184)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> B.3. IBIS3 285
† integrate
1. retract (rule 5.7) (p. 180)
2. integrateUsrAsk
3. integrateSysAsk
4. integrateNegIcmAnswer (...

**Algorithm:**

```
rule 5.10) (p. 184)
5. integratePosIcmAnswer (rule 5.11) (p. 189)
6. integrateUsrAnswer
7. integrateSysAnswer
8. integrateAccommodationICM
9. integrateUndPosICM
10. integrateUndIntICM
11. integrateUsrPerNegICM
12. integrateUsrAccNegICM
13. integrateOtherICM
14. integrateGreet
15. integrateSysQuit
16. integrateUsrQuit
17. integrateNoMove
† accommodate
1. accommodateIssues2QUD (rule 5.2) (p. 169)
```

**Context After:**
> 2. accommodateQUD2Issues (rule 5.9) (p. 183)
3. accommodatePlan2Issues (rule 5.1) (p. 166)
4. accommodateCom2Issues (rule 5.6) (p. 179)
5. accommodateCom2IssuesDependent (rule 5.8) (p. 182)
6. accommo...

---

## Algorithm 181: rule 5 .11) (p. 189)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> B.3. IBIS3 285
† integrate
1. retract (rule 5.7) (p. 180)
2. integrateUsrAsk
3. integrateSysAsk
4. integrateNegIcmAnswer (rule 5.10) (p. 184)
5. integratePosIcmAnswer (...

**Algorithm:**

```
rule 5.11) (p. 189)
6. integrateUsrAnswer
7. integrateSysAnswer
8. integrateAccommodationICM
9. integrateUndPosICM
10. integrateUndIntICM
11. integrateUsrPerNegICM
12. integrateUsrAccNegICM
13. integrateOtherICM
14. integrateGreet
15. integrateSysQuit
16. integrateUsrQuit
17. integrateNoMove
† accommodate
1. accommodateIssues2QUD (rule 5.2) (p. 169)
```

**Context After:**
> 2. accommodateQUD2Issues (rule 5.9) (p. 183)
3. accommodatePlan2Issues (rule 5.1) (p. 166)
4. accommodateCom2Issues (rule 5.6) (p. 179)
5. accommodateCom2IssuesDependent (rule 5.8) (p. 182)
6. accommo...

---

## Algorithm 182: rule 5 .2) (p. 169)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> .3. IBIS3 285
† integrate
1. retract (rule 5.7) (p. 180)
2. integrateUsrAsk
3. integrateSysAsk
4. integrateNegIcmAnswer (rule 5.10) (p. 184)
5. integratePosIcmAnswer (rule 5.11) (p. 189)
6. integrateU...

**Algorithm:**

```
rule 5.2) (p. 169)
2. accommodateQUD2Issues (rule 5.9) (p. 183)
3. accommodatePlan2Issues (rule 5.1) (p. 166)
4. accommodateCom2Issues (rule 5.6) (p. 179)
5. accommodateCom2IssuesDependent (rule 5.8) (p. 182)
6. accommodateDependentIssue (rule 5.4) (p. 172)
† downdate issues
{ downdateISSUES
{ downdateISSUES2 (similar to downdateQUD2 in IBiS1)
† downdate qud
{ downdateQUD
```

---

## Algorithm 183: rule 5 .9) (p. 183)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> 7) (p. 180)
2. integrateUsrAsk
3. integrateSysAsk
4. integrateNegIcmAnswer (rule 5.10) (p. 184)
5. integratePosIcmAnswer (rule 5.11) (p. 189)
6. integrateUsrAnswer
7. integrateSysAnswer
8. integrateAc...

**Algorithm:**

```
rule 5.9) (p. 183)
3. accommodatePlan2Issues (rule 5.1) (p. 166)
4. accommodateCom2Issues (rule 5.6) (p. 179)
5. accommodateCom2IssuesDependent (rule 5.8) (p. 182)
6. accommodateDependentIssue (rule 5.4) (p. 172)
† downdate issues
{ downdateISSUES
{ downdateISSUES2 (similar to downdateQUD2 in IBiS1)
† downdate qud
{ downdateQUD
```

---

## Algorithm 184: rule 5 .1) (p. 166)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> Ask
4. integrateNegIcmAnswer (rule 5.10) (p. 184)
5. integratePosIcmAnswer (rule 5.11) (p. 189)
6. integrateUsrAnswer
7. integrateSysAnswer
8. integrateAccommodationICM
9. integrateUndPosICM
10. integ...

**Algorithm:**

```
rule 5.1) (p. 166)
4. accommodateCom2Issues (rule 5.6) (p. 179)
5. accommodateCom2IssuesDependent (rule 5.8) (p. 182)
6. accommodateDependentIssue (rule 5.4) (p. 172)
† downdate issues
{ downdateISSUES
{ downdateISSUES2 (similar to downdateQUD2 in IBiS1)
† downdate qud
{ downdateQUD
```

---

## Algorithm 185: rule 5 .6) (p. 179)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> 184)
5. integratePosIcmAnswer (rule 5.11) (p. 189)
6. integrateUsrAnswer
7. integrateSysAnswer
8. integrateAccommodationICM
9. integrateUndPosICM
10. integrateUndIntICM
11. integrateUsrPerNegICM
12. i...

**Algorithm:**

```
rule 5.6) (p. 179)
5. accommodateCom2IssuesDependent (rule 5.8) (p. 182)
6. accommodateDependentIssue (rule 5.4) (p. 172)
† downdate issues
{ downdateISSUES
{ downdateISSUES2 (similar to downdateQUD2 in IBiS1)
† downdate qud
{ downdateQUD
```

---

## Algorithm 186: rule 5 .8) (p. 182)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> integrateUsrAnswer
7. integrateSysAnswer
8. integrateAccommodationICM
9. integrateUndPosICM
10. integrateUndIntICM
11. integrateUsrPerNegICM
12. integrateUsrAccNegICM
13. integrateOtherICM
14. integra...

**Algorithm:**

```
rule 5.8) (p. 182)
6. accommodateDependentIssue (rule 5.4) (p. 172)
† downdate issues
{ downdateISSUES
{ downdateISSUES2 (similar to downdateQUD2 in IBiS1)
† downdate qud
{ downdateQUD
```

---

## Algorithm 187: rule 5 .4) (p. 172)

**Section:** 13. SubAlg
**Page:** 307

**Context Before:**
> rateAccommodationICM
9. integrateUndPosICM
10. integrateUndIntICM
11. integrateUsrPerNegICM
12. integrateUsrAccNegICM
13. integrateOtherICM
14. integrateGreet
15. integrateSysQuit
16. integrateUsrQuit...

**Algorithm:**

```
rule 5.4) (p. 172)
† downdate issues
{ downdateISSUES
{ downdateISSUES2 (similar to downdateQUD2 in IBiS1)
† downdate qud
{ downdateQUD
```

---

## Algorithm 188: rule 5 .12) (p. 190)

**Section:** 13. SubAlg
**Page:** 308

**Context Before:**
> 286 APPENDIX B. RULES AND CLASSES
† load plan
1. recoverPlan
2. flndPlan
† exec plan
1. removeFindout
2. exec consultDB
† select action
1. selectIcmUndIntAsk
2. selectIcmUndIntAnswer
3. selectIcmUndIn...

**Algorithm:**

```
rule 5.12) (p. 190)
{ backupSharedUsr (rule 5.13) (p. 193)
B.3.2 IBiS3 select module
† select action
1. clarifyIssue (rule 5.3) (p. 170)
2. clarifyDependentIssue (rule 5.5) (p. 176)
3. selectRespond
4. selectFromPlan
5. reraiseIssue
† select icm
1. selectIcmConNeg
```

---

## Algorithm 189: rule 5 .13) (p. 193)

**Section:** 13. SubAlg
**Page:** 308

**Context Before:**
> 286 APPENDIX B. RULES AND CLASSES
† load plan
1. recoverPlan
2. flndPlan
† exec plan
1. removeFindout
2. exec consultDB
† select action
1. selectIcmUndIntAsk
2. selectIcmUndIntAnswer
3. selectIcmUndIn...

**Algorithm:**

```
rule 5.13) (p. 193)
B.3.2 IBiS3 select module
† select action
1. clarifyIssue (rule 5.3) (p. 170)
2. clarifyDependentIssue (rule 5.5) (p. 176)
3. selectRespond
4. selectFromPlan
5. reraiseIssue
† select icm
1. selectIcmConNeg
```

---

## Algorithm 190: rule 5 .3) (p. 170)

**Section:** 13. SubAlg
**Page:** 308

**Context Before:**
> 286 APPENDIX B. RULES AND CLASSES
† load plan
1. recoverPlan
2. flndPlan
† exec plan
1. removeFindout
2. exec consultDB
† select action
1. selectIcmUndIntAsk
2. selectIcmUndIntAnswer
3. selectIcmUndIn...

**Algorithm:**

```
rule 5.3) (p. 170)
2. clarifyDependentIssue (rule 5.5) (p. 176)
3. selectRespond
4. selectFromPlan
5. reraiseIssue
† select icm
1. selectIcmConNeg
```

---

## Algorithm 191: rule 5 .5) (p. 176)

**Section:** 13. SubAlg
**Page:** 308

**Context Before:**
> 286 APPENDIX B. RULES AND CLASSES
† load plan
1. recoverPlan
2. flndPlan
† exec plan
1. removeFindout
2. exec consultDB
† select action
1. selectIcmUndIntAsk
2. selectIcmUndIntAnswer
3. selectIcmUndIn...

**Algorithm:**

```
rule 5.5) (p. 176)
3. selectRespond
4. selectFromPlan
5. reraiseIssue
† select icm
1. selectIcmConNeg
```

---

## Algorithm 192: rule 6 .1) (p. 216)

**Section:** 13. SubAlg
**Page:** 309

**Context Before:**
> B.4. IBIS4 287
2. selectIcmPerNeg
3. selectIcmSemNeg
4. selectIcmUndNeg
5. selectIcmOther
† select move
1. selectQuit
2. selectAnswer
3. selectAsk
4. selectGreet
5. selectIcmOther
† none
{ backupShare...

**Algorithm:**

```
rule 6.1) (p. 216)
5. integrateConflrm (rule 6.6) (p. 218)
6. integrateNegIcmAnswer
7. integratePosIcmAnswer
8. integrateUsrAnswer
9. integrateSysAnswer
10. integrateAccommodationICM
```

---

## Algorithm 193: rule 6 .6) (p. 218)

**Section:** 13. SubAlg
**Page:** 309

**Context Before:**
> B.4. IBIS4 287
2. selectIcmPerNeg
3. selectIcmSemNeg
4. selectIcmUndNeg
5. selectIcmOther
† select move
1. selectQuit
2. selectAnswer
3. selectAsk
4. selectGreet
5. selectIcmOther
† none
{ backupShare...

**Algorithm:**

```
rule 6.6) (p. 218)
6. integrateNegIcmAnswer
7. integratePosIcmAnswer
8. integrateUsrAnswer
9. integrateSysAnswer
10. integrateAccommodationICM
```

---

## Algorithm 194: rule 6 .8) (p. 221)

**Section:** 13. SubAlg
**Page:** 310

**Context Before:**
> 288 APPENDIX B. RULES AND CLASSES
11. integrateUndPosICM
12. integrateUndIntICM
13. integrateUsrPerNegICM
14. integrateUsrAccNegICM
15. integrateOtherICM
16. integrateGreet
17. integrateSysQuit
18. in...

**Algorithm:**

```
rule 6.8) (p. 221)
† downdate issues
1. downdateISSUES
2. downdateISSUES2
3. downdateISSUES3 (downdates resolved action-issue)
4. downdateActions (rule 6.7) (p. 218)
† downdate qud
{ downdateQUD
† load plan
1. flndPlan
2. flndActionPlan
† exec plan
1. recoverPlan
2. recoverActionPlan
```

---

## Algorithm 195: rule 6 .7) (p. 218)

**Section:** 13. SubAlg
**Page:** 310

**Context Before:**
> . integrateUsrPerNegICM
14. integrateUsrAccNegICM
15. integrateOtherICM
16. integrateGreet
17. integrateSysQuit
18. integrateUsrQuit
19. integrateNoMove
† accommodate
1. accommodateIssues2QUD
2. accom...

**Algorithm:**

```
rule 6.7) (p. 218)
† downdate qud
{ downdateQUD
† load plan
1. flndPlan
2. flndActionPlan
† exec plan
1. recoverPlan
2. recoverActionPlan
```

---

## Algorithm 196: rule 6 .3) (p. 217)

**Section:** 13. SubAlg
**Page:** 311

**Context Before:**
> B.4. IBIS4 289
3. removeFindout
4. exec consultDB
5. exec dev get
6. exec dev set
7. exec dev do (...

**Algorithm:**

```
rule 6.3) (p. 217)
8. exec dev query
† select action
1. selectIcmUndIntAsk
2. selectIcmUndIntAnswer
3. selectIcmUndIntRequest
4. rejectIssue
5. rejectProp
6. rejectAction (rule 6.2) (p. 216)
† (none)
{ backupSharedUsr
{ irrelevantFollowup
{ irrelevantFollowup
{ unclearFollowup
{ failedFollowup
{ noFollowup
{ declineProp
B.4.2 IBiS4 select module
† select action
1. clarifyIssue
2. clarifyIssueAction (rule 6.9) (p. 221)
```

**Context After:**
> 3. selectConflrmAction (rule 6.4) (p. 217)
4. selectRespond
5. reraiseIssue
6. selectFromPlan...

---

## Algorithm 197: rule 6 .2) (p. 216)

**Section:** 13. SubAlg
**Page:** 311

**Context Before:**
> B.4. IBIS4 289
3. removeFindout
4. exec consultDB
5. exec dev get
6. exec dev set
7. exec dev do (rule 6.3) (p. 217)
8. exec dev query
† select action
1. selectIcmUndIntAsk
2. selectIcmUndIntAnswer
3....

**Algorithm:**

```
rule 6.2) (p. 216)
† (none)
{ backupSharedUsr
{ irrelevantFollowup
{ irrelevantFollowup
{ unclearFollowup
{ failedFollowup
{ noFollowup
{ declineProp
B.4.2 IBiS4 select module
† select action
1. clarifyIssue
2. clarifyIssueAction (rule 6.9) (p. 221)
```

**Context After:**
> 3. selectConflrmAction (rule 6.4) (p. 217)
4. selectRespond
5. reraiseIssue
6. selectFromPlan...

---

## Algorithm 198: rule 6 .9) (p. 221)

**Section:** 13. SubAlg
**Page:** 311

**Context Before:**
> .4. IBIS4 289
3. removeFindout
4. exec consultDB
5. exec dev get
6. exec dev set
7. exec dev do (rule 6.3) (p. 217)
8. exec dev query
† select action
1. selectIcmUndIntAsk
2. selectIcmUndIntAnswer
3. ...

**Algorithm:**

```
rule 6.9) (p. 221)
3. selectConflrmAction (rule 6.4) (p. 217)
4. selectRespond
5. reraiseIssue
6. selectFromPlan
```

---

