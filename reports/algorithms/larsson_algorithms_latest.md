# Larsson (2002) - IBDM Algorithmic Reference

**Source**: Larsson, S. (2002). Issue-Based Dialogue Management. Doctoral dissertation.
**Status**: Extracted from `docs/Larsson_Tesis_full.txt` via `algorithm_miner.py`
**Total Items**: 70

---

## Table of Contents

- [Semantic Operations](#semantic-operations) (1 items)
- [Update Rules](#update-rules) (25 items)
- [Selection Rules](#selection-rules) (15 items)
- [Other Algorithms](#other-algorithms) (29 items)

---

## Semantic Operations

### Rule 3.22: irrelevantFollowup

**Source**: Page 163 (Section Unknown)

```
(rule 3.22) rule: irrelevantFollowup
            class:
                  none
                 
                 
                 
                    1 $/private/nim=M oves
                 
                 
                 
                   2 $/shared/lu/speaker==usr
                    3 not A/elem=icm:
                 
                 
                 
                 
                 
                  4 in($/shared/pm, P revM ove)
                 
            pre:
                 
                 
                   5 P revM ove=ask(Q) or
                       ( P revM ove=icm:und*int:DP *C and Q=und(DP *C) )
                 
                 
                 
                 
                    6 not M oves/elem=ask(Q0 ) and $domain :: depends(Q, Q0 )
                 
                 
                 
                 
                 
                 
                 
                 (
                    7 not A/elem=answer(A) and $domain :: relevant(A, Q)
                    /shared/QUD := $/private/tmp/QUD
            eff:
                    /shared/com := $/private/tmp/com


(Since this rule is called “by name” from the update algorithm, there is no need for including
it in a rule class.) Condition 3 checks that no ICM was included in the latest move.
Condition 4 and 5 tries to find a question Q raised by the previous move, possibly an
understanding-question. Note here that we do not check QUD; in IBiS2, questions remain
on QUD only for one turn but it may be the case that we want questions to remain on
QUD over several turns. What we are interested here is thus not which questions are on
QUD but which questions were raised by the previous utterance, and this is the reason
for looking in pm rather than QUD. Conditions 6 and 7 check that no move performed in
the latest utterance is relevant to Q, neither by answering it nor by asking a question on
which Q depends. The updates are similar to those for integration of negative acceptance
feedback (Section 3.6.7).

```

---

## Update Rules

### Rule 2.11: exec consultDB

**Source**: Page 72 (Section Unknown)

```
(rule 2.11) rule: exec consultDB
            class:n exec plan
            pre: fst($/private/plan, consultDB(Q))
                     ! $/shared/com=B
                 
                 
                 
                  ! $database :: consultDB(Q, B, C)
                 
            eff: 
                 
                    add(/private/bel, C)
                     pop(/private/plan)
                 


```

---

### Rule 2.16: downdateQUD2

**Source**: Page 85 (Section Unknown)

```
(rule 2.16) rule: downdateQUD2
            class: downdate QUD
                  in($/shared/QUD, IssueQ)
                 
            pre:  fst($/shared/QUD, Q)
                 
                 n
                     $domain :: resolves(Q, IssueQ)
            eff: del(/shared/QUD, IssueQ)


We also need to define resolvedness conditions for issue-questions (for example, an issue-
question cannot be resolved by an issue-question). In addition, rules for removing findout
and raise actions from the plan based on the contents of QUD would need to be added.

```

---

### Rule 2.2: integrateSysAsk

**Source**: Page 65 (Section Unknown)

```
 (rule 2.2)    rule: integrateSysAsk
               class:( integrate
                        $/shared/lu/speaker==sys
               pre:
                        in($/shared/lu/moves, ask(Q))
                    n
               eff: push(/shared/QUD, Q)


The conditions of the rule in (2.14) checks that the latest speaker is sys and that the latest
move was an ask move with content Q. The update pushes Q on /shared/QUD.

```

---

### Rule 2.3: integrateUsrAsk

**Source**: Page 66 (Section Unknown)

```
 (rule 2.3)       rule: integrateUsrAsk
                  class:( integrate
                           $/shared/lu/speaker==usr
                  pre:
                           in($/shared/lu/moves, ask(Q))
                       (
                           push(/shared/QUD, Q)
                  eff:
                           push(/private/agenda, respond(Q))

The update rule in (rule 2.3) for integrating user queries is slightly different: if the user
asks a question q, the system will also push respond(q) on the agenda. This does not
happen if the system asks the question, since it is the user who is expected to answer this
question.

Eventually, the findPlan (see Section 2.8.6) rule will load the appropriate plan for dealing
with Q. This assumes that for any user question that the system is able to interpret, there
is a plan for dealing with that question. If this were not the case, IBiS would somehow
have to reject Q; in Chapter 3 we will discuss this further.


Reasons for answering questions


The solution of pushing respond(Q) on the agenda when integrating a user ask(Q) move is
not the only possible option. It can be seen as a simple “intention-based” strategy involving
minimal reasoning; “If the user asked q, I’m going to respond to q”. Alternatively, one
could opt for a more indirect link between the user asking a question and the system
intending to respond to it.

One such indirect approach is to not push respond(Q) on the agenda when integrating a
user ask(Q) move, but only push Q on QUD7. A separate rule would then push respond(Q)
on the agenda given that Q is on QUD and the system has a plan for responding to Q.
This reasoning behind this rule could be paraphrased roughly as “If q is under discussion
and I know a way of dealing with q, I should try to respond to q”. On this approach,
it would be assumed that DPs do not care about who asked a question; they will simply
attempt to answer any question that is under discussion, regardless of who raised it.

A second indirect approach is to assume that asking a question introduces obligations on
the addressee. This “obligation-based approach” would require representing obligations as
part of the shared information. For an obligation-based account of dialogue, see Traum
(1996); for a comparison of QUD-based and obligation-based approaches, see Kreutel and
     7
    If the system can understand user questions which it cannot respond to (which IBiS1 does not), the
integration rule for user ask moves would still need to check that there is a plan for dealing with Q, or else
reject Q; issue rejection is discussed further in Chapter 3.

```

---

### Rule 2.4: integrateAnswer

**Source**: Page 69 (Section Unknown)

```
 (rule 2.4)   rule: integrateAnswer
              class: integrate
                    in($/shared/lu/moves, answer(A))
                   
              pre:  fst($/shared/QUD, Q)
                   
                   (
                        $domain :: relevant(A, Q)
                       ! $domain :: combine(Q, A, P )
              eff:
                       add(/shared/com, P )

The first condition checks that the latest move was an answer move with content A, and
the next two conditions check that A is relevant to some question Q topmost on QUD.
The first updates combines Q and A to form a proposition P according to the definition
in Section 2.4.7. Finally, P is added to the shared commitments.


```

---

### Rule 2.5: downdateQUD

**Source**: Page 70 (Section Unknown)

```
 (rule 2.5)    rule: downdateQUD
               class: downdate QUD
                     fst($/shared/QUD, Q)
                    
               pre:  in($/shared/com, P )
                    
                    n
                        $domain :: resolves(P, Q)
               eff: pop(/shared/QUD)

The paraphrase of this rule is straightforward and is left as an exercise to the reader.

This rule is perhaps inefficient in the sense that it may require checking all propositions in
/shared/com every time the update algorithm is executed. However, in the systems we
are concerned with the number of propositions is not very high, and in addition we favour
clarity and simplicity in the implementation over efficiency.


```

---

### Rule 2.6: integrateGreet

**Source**: Page 70 (Section Unknown)

```
 (rule 2.6)    rule: integrateGreet
               class:n integrate
               pre: in($/shared/lu/moves, greet)
               eff: {


The update rules for integrating quit moves performed by the user or system are shown in
```

---

### Rule 2.7: integrateUsrQuit

**Source**: Page 70 (Section Unknown)

```
 (rule 2.7)    rule: integrateUsrQuit
               class:( integrate
                        $/shared/lu/speaker==usr
               pre:
                        in($/shared/lu/moves, quit)
                    n
               eff: push(/private/agenda, quit)

If the quit move is performed by the user, the effect is that the system puts quit on the
agenda so that it gets to say “Goodbye” to the user before the dialogue ends.

```

---

### Rule 2.8: integrateSysQuit

**Source**: Page 71 (Section Unknown)

```
 (rule 2.8)   rule: integrateSysQuit
              class:( integrate
                       $/shared/lu/speaker==sys
              pre:
                       in($/shared/lu/moves, quit)
                   n
              eff: program state := quit


Integrating a quit move performed by the system causes the program state variable to
be set to quit. This will eventually cause the program to halt.

The greet move does not have any effect on the information state, and thus no update rule
is needed to integrate it.


```

---

### Rule 3.1: integrateUsrAsk

**Source**: Page 132 (Section Unknown)

```
 (rule 3.1)    rule: integrateUsrAsk
               class: integrate
                    
                    
                    
                        $/shared/lu/speaker==usr
                     fst($/private/nim, ask(Q))
                    
                    
                    
               pre:  $score=Score
                    
                    
                    
                       Score > 0.7
                     $domain :: plan(Q, P lan)
                    

                        1 pop(/private/nim)
                    
                    
                    
                        2 push(/private/agenda, icm:acc*pos)
                    
                    
                    
                    
                    
                        3 add(/shared/lu/moves, ask(Q))
                    
                    
                    
                    
                    
                     4 if do(Score ≤ 0.9,
                    
                    
                    
               eff:        push(/private/agenda, icm:und*pos:usr*issue(Q)))
                    
                    
                    
                       5 if do(in($/shared/QUD, Q) and not fst($/shared/QUD, Q),
                            push(/private/agenda, icm:reraise:Q))
                    
                    
                    
                    
                    
                        6 push(/shared/QUD, Q)
                    
                    
                    
                    
                    
                        7 push(/private/agenda, respond(Q))
                    


```

---

### Rule 3.10: integrateOtherICM

**Source**: Page 143 (Section Unknown)

```
(rule 3.10) rule: integrateOtherICM
            class:n integrate
            pre: fst($/private/nim, icm:A)
                 (
                     pop(/private/nim)
            eff:
                     add(/shared/lu/moves, icm:A)


The condition and updates in this rule are straightforward.


```

---

### Rule 3.18: integrateSysAsk

**Source**: Page 154 (Section Unknown)

```
(rule 3.18) rule: integrateSysAsk
            class:( integrate
                     $/shared/lu/speaker==sys
            pre:
                     fst($/private/nim, ask(A))
                 
                  pop(/private/nim)
                 
            eff:     add(/shared/lu/moves, ask(A))
                     push(/shared/QUD, A)
                 
                 


```

---

### Rule 3.19: integrateSysAnswer

**Source**: Page 154 (Section Unknown)

```
(rule 3.19) rule: integrateSysAnswer
            class: integrate
                 
                 
                 
                     fst($/private/nim, answer(A))
                  $/shared/lu/speaker==sys
                 
                 
                 
            pre:  $domain :: proposition(A)
                 
                 
                 
                    fst($/shared/QUD, B)
                  $domain :: relevant(A, B)
                 
                 
                  pop(/private/nim)
                 
            eff:  add(/shared/lu/moves, answer(A))
                 
                     add(/shared/com, A)

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


In this section we review user feedback to system utterances and how these affect the
optimistic grounding assumptions.


Negative user perception feedback If the system makes an utterance, it will assume
it is grounded and accepted. If the user indicates that she did not understand the utterance,
the rule in (rule 3.20) makes it possible to retract the effects of the system’s latest move,
thus cancelling the assumptions of grounding and acceptance.

```

---

### Rule 3.20: integrateUsrPerNegICM

**Source**: Page 155 (Section Unknown)

```
(rule 3.20) rule: integrateUsrPerNegICM
            class:( integrate
                     $/shared/lu/speaker==usr
            pre:
                     fst($/private/nim, icm:per*neg)
                 
                 
                 
                 
                     pop(/private/nim)
                  /shared/QUD := $/private/tmp/QUD
                 
                 
                 
            eff:     /shared/com := $/private/tmp/com
                     /private/agenda := $/private/tmp/agenda
                 
                 
                 
                 
                 
                  /private/plan := $/private/tmp/plan
                 


```

---

### Rule 3.21: integrateUsrAccNegICM

**Source**: Page 157 (Section Unknown)

```
(rule 3.21) rule: integrateUsrAccNegICM
            class: integrate
                  $/shared/lu/speaker==usr
                 
            pre:     fst($/private/nim, icm:acc*neg:issue)
                     in($/shared/pm, ask(Q))
                 
                 

                     pop(/private/nim)
                 
                 
                 
                  add(/shared/lu/moves, icm:acc*neg:issue)
                 
            eff: 
                 
                    /shared/QUD := $/private/tmp/QUD
                     /shared/com := $/private/tmp/com
                 

```

---

### Rule 3.4: integrateUsrAnswer

**Source**: Page 135 (Section Unknown)

```
 (rule 3.4)    rule: integrateUsrAnswer
               class: integrate
                    
                    
                    
                        1 fst($/private/nim, answer(A))
                    
                    
                    
                       2 $/shared/lu/speaker==usr
                        3 ! $score=Score
                    
                    
                    
                    
                    
                     4 Score > 0.7
                    
               pre:
                    
                    
                       5 fst($/shared/QUD, Q)
                        6 $domain :: relevant(A, Q)
                    
                    
                    
                    
                    
                        7 $domain :: combine(Q, A, P )
                    
                    
                    
                    
                    
                    
                        8 $database :: validDBparameter(P ) or P =not(X)
                    
                    
                       1 pop(/private/nim)
                        2 add(/shared/lu/moves, answer(P ))
                    
                    
                    
                    
                    
                     3 push(/private/agenda, icm:acc*pos)
                    
               eff: 
                    
                       4 if do(Score ≤ 0.9 and A 6= yes and A 6= no,
                            push(/private/agenda, icm:und*pos:usr*P ))
                    
                    
                    
                    
                    
                        5 add(/shared/com, P )
                    


Conditions 1-4 are similar to those for the integrateUsrAsk rule. The relevance of the
content of the answer to a question on QUD is checked in condition 6.

The acceptability condition in the condition 8 makes sure that the propositional content
resulting from combining the question topmost on QUD with the content of the answer-
move is either


   • a valid database parameter, or
   • a negated proposition

```

---

### Rule 3.6: integrateUndIntICM

**Source**: Page 137 (Section Unknown)

```
 (rule 3.6)    rule: integrateUndIntICM
               class:n integrate
               pre: fst($/private/nim, icm:und*int:DP *C)
                    
                     pop(/private/nim)
                    
               eff:  add(/shared/lu/moves, icm:und*int:DP *C)
                    
                        push(/shared/QUD, und(DP *C))

The condition simply checks that there is an icm:und*int:DP *C move on nim, which is
then popped off by the first update and added to /shared/lu/moves by the second
update. The third update pushes the understanding question ?und(DP *C) on QUD.


Integrating positive answer to understanding-question When the system raises
an understanding question (e.g. by saying “To Paris, is that correct?”), the user can either
say “yes” or “no”. (The case where the user does not give a relevant answer to the inter-
rogative feedback is treated in Section 3.6.8). In IBiS2, we do not represent propositions
related to the understanding of utterances in the same way as other propositions (which
are stored in /shared/com). Therefore, special rules are needed for dealing with answers
to understanding-questions.

The rule for integrating a negative answer to an understanding-question is shown in (rule
3.7).


```

---

### Rule 3.7: integrateNegIcmAnswer

**Source**: Page 137 (Section Unknown)

```
 (rule 3.7)    rule: integrateNegIcmAnswer
               class:( integrate
                        fst($/private/nim, answer(no))
               pre:
                        fst($/shared/QUD, und(DP *C))
                        pop(/private/nim)
                    
                    
                    
                     add(/shared/lu/moves, answer(und(DP *C)))
                    
               eff: 
                    
                       pop(/shared/QUD)
                        push(/private/agenda, icm:und*pos:DP *not(C))
                    


```

---

### Rule 3.8: integratePosIcmAnswer

**Source**: Page 138 (Section Unknown)

```
 (rule 3.8)     rule: integratePosIcmAnswer
                class:( integrate
                         fst($/private/nim, answer(yes))
                pre:
                     
                         fst($/shared/QUD,  und(DP *Content))
                     
                     
                        pop(/private/nim)
                         add(/shared/lu/moves, answer(und(DP *Content)))
                     
                     
                     
                     
                     
                      pop(/shared/QUD)
                     
                     
                     
                eff:  if then else(Content=issue(Q), [
                     
                     
                     
                           push(/shared/QUD, Q)
                            push(/private/agenda, respond(Q)) ],
                     
                     
                     
                     
                     
                      add(/shared/com, Content))
                     


```

---

### Rule 4.10: integrateNegIcmAnswer

**Source**: Page 206 (Section Unknown)

```
(rule 4.10) rule: integrateNegIcmAnswer
            class: integrate
                 
                     $/private/nim/fst/snd=answer(A)
                      fst($/shared/issues,   Q)
                 
                 
                 
                 
                 
                  $domain :: resolves(A, Q)
                 
            pre:
                 
                 
                     fst($/shared/QUD, Q)
                      $domain :: combine(Q, A, P )
                 
                 
                 
                 
                 
                      P =not(und(DP *C))
                 
                 
                 
                 
                    pop(/private/nim)
                     pop(/shared/issues)
                 
                 
                 
                 
                 
                     if do(in($/shared/com, C) or
                 
                 
                 
                 
                         C=issue(Q0 ) and in($/shared/issues, Q0 ), [
                 
                 
                 
                 
                 
                         /shared/QUD := $/private/tmp/DP /QUD
                 
                 
                 
                 
                 
                         /shared/issues := $/private/tmp/DP /issues
                 
                 
            eff: 
                 
                        /shared/com := $/private/tmp/DP /com
                         /private/agenda := $/private/tmp/DP /agenda
                 
                 
                 
                 
                 
                         /private/plan   := $/private/tmp/DP /plan ])
                 
                 
                 
                 
                 
                 
                 
                 
                    push(/private/agenda, icm:und*pos:DP *not(C))
                     clear(/private/nim)
                 
                 
                 
                 
                 
                  init shift(/private/nim)
                 


```

---

### Rule 4.11: integratePosIcmAnswer

**Source**: Page 211 (Section Unknown)

```
(rule 4.11) rule: integratePosIcmAnswer
            class: integrate
                 
                     $/private/nim/fst/snd=answer(A)
                      fst($/shared/issues,   Q)
                 
                 
                 
                 
                 
                  $domain :: resolves(A, Q)
                 
            pre:
                 
                 
                     fst($/shared/QUD, Q)
                      $domain :: combine(Q, A, P )
                 
                 
                 
                 
                 
                      P =und(DP *Content)
                 

                     pop(/private/nim)
                 
                 
                 
                     pop(/shared/issues)
                 
                 
                 
                 
                     if then else(Content=issue(Q0 ), [
                 
                 
                 
                 
                 
                         push(/private/tmp/DP /QUD, Q0 )
                 
                 
                 
                 
                 
                         push(/private/tmp/DP /issues, Q0 )
                 
                 
                 
                 
                 
                         push(/private/tmp/DP /agenda, respond(Q0 )) ],
                 
                 
                 
                 
                 
                         add(/private/tmp/DP /com, Content))
                 
                 
            eff: 
                    if do(not ( in($/shared/com, Content) or
                         Content=issue(Q0 ) and in($/shared/issues, Q0 ) ),
                 
                 
                 
                 
                 
                         if then else(Content=issue(Q0 ), [
                 
                 
                 
                 
                 
                             push(/shared/QUD, Q0 )
                 
                 
                 
                 
                 
                             push(/shared/issues, Q0 )
                 
                 
                 
                 
                 
                             push(/private/agenda, respond(Q0 )) ],
                 
                 
                 
                 
                 
                         add(/shared/com, Content)))
                 


```

---

### Rule 5.1: integrateUsrRequest

**Source**: Page 238 (Section Unknown)

```
 (rule 5.1)   rule: integrateUsrRequest
              class: integrate
                   
                   
                   
                       $/private/nim/fst/snd=request(A)
                    $/shared/lu/speaker==usr
                   
                   
                   
              pre:  $score=Score
                   
                   
                   
                      Score > 0.7
                    $domain :: plan(A, P lan)
                   
                   
                   
                   
                      pop(/private/nim)
                       add(/shared/lu/moves,   request(A))
                   
                   
                   
                   
                   
                    push(/private/agenda, icm:acc*pos)
                   
                   
                   
              eff:  if do(Score ≤ 0.9,
                   
                   
                   
                         push(/private/agenda, icm:und*pos:usr*action(A)))
                       push(/shared/actions, A)
                   
                   
                   
                   
                   
                    push(/private/agenda, A)
                   


```

---

### Rule 5.3: exec dev do

**Source**: Page 239 (Section Unknown)

```
 (rule 5.3)   rule: exec dev do
              class:n exec plan
              pre: fst($/private/plan, dev do(Dev, Adev ))
                       pop(/private/plan)
                   
                   
                   
                    ! $/shared/com=P ropSet
                   
              eff: 
                   
                      devices/Dev :: dev do(P ropSet, Adev )
                       add(/private/bel, done(Adev ))
                   


The condition looks for a dev do upnp action in the plan, with arguments Dev, the device
path name, and Adev, the device action. The updates pop the action off the plan, and
applies the corresponding update dev do(P ropSet, Adev ) to the device Dev. Finally, the
proposition done(Adev ) is added the the private beliefs.

In addition, we have implemented rules for executing the dev get, dev set and dev query
actions.


```

---

### Rule 5.6: integrateConfirm

**Source**: Page 240 (Section Unknown)

```
 (rule 5.6)        rule: integrateConfirm
                   class:n integrate
                   pre: $/private/nim/fst/snd=confirm(A)
                        (
                            pop(/private/nim)
                   eff:
                            add(/shared/com, done(A))


This rule adds the proposition done(A) to the shared commitments which enables the
downdateActions rule in (rule 5.7) to trigger.


```

---

### Rule 5.7: downdateActions

**Source**: Page 240 (Section Unknown)

```
 (rule 5.7)        rule: downdateActions
                   class: downdate issues
                         fst($/shared/actions, A)
                        
                   pre:  $domain :: postcond(A, P C)
                        
                        n
                            in($/shared/com, P C )
                   eff: pop(/shared/actions)


This rule removes an action A whose postcondition is jointly believed to be true from
actions2.


```

---

## Selection Rules

### Rule 2.12: selectFromPlan

**Source**: Page 73 (Section 2.9 IBiS)

```
(rule 2.12) rule: selectFromPlan
            class:( select action
                     is empty($/private/agenda)
            pre:
                     fst($/private/plan, Action)
                 n
            eff: push(/private/agenda, Action)

```

---

### Rule 2.13: selectAsk

**Source**: Page 74 (Section Unknown)

```
(rule 2.13) rule: selectAsk
            class:
                 ( select move
                    fst($/private/agenda, findout(Q)) or fst($/private/agenda,
            pre:
                        raise(Q))
                 (
                   add(next moves, ask(Q))
            eff:
                   if do(fst($/private/plan, raise(A)), pop(/private/plan))

```

---

### Rule 2.14: selectRespond

**Source**: Page 75 (Section Unknown)

```
(rule 2.14) rule: selectRespond
            class: select action
                 
                    is empty($/private/agenda)
                     is empty($/private/plan)
                 
                 
                 
                 
                 
                  fst($/shared/QUD, Q)
                 
            pre: 
                 
                    in($/private/bel, P )
                     not in($/shared/com, P )
                 
                 
                 
                 
                 
                     $domain :: relevant(P, Q)
                 
                 n
            eff: push(/private/agenda, respond(Q))


The first two conditions check that there is nothing else that currently needs to be done.
The remaining conditions check that some question Q is topmost on QUD, the system
knows a relevant answer P to Q which is not yet shared.

```

---

### Rule 2.15: selectAnswer

**Source**: Page 76 (Section Unknown)

```
(rule 2.15) rule: selectAnswer
            class: select move
                 
                    fst($/private/agenda, respond(Q))
                  in($/private/bel, P )
                 
            pre:
                 
                 
                 
                     not in($/shared/com, P )
                     $domain :: relevant(Å, Q)
                 
                 n
            eff: add(next moves, answer(P ))


```

---

### Rule 3.11: selectIcmPerNeg

**Source**: Page 143 (Section Unknown)

```
(rule 3.11) rule: selectIcmPerNeg
            class:( select icm
                     $input=’FAIL’
            pre:
                     not in($next moves, icm:per*neg)
                 n
            eff: push(next moves, icm:per*neg)


The purpose of the second condition is to prevent selecting negative perception feedback
more than once in the selection phase. As with negative system contact feedback, negative
system perception feedback is integrated by the integrateOtherICM rule.


```

---

### Rule 3.12: selectIcmSemNeg

**Source**: Page 144 (Section Unknown)

```
(rule 3.12) rule: selectIcmSemNeg
            class: select icm
                  $latest moves=failed
                 
            pre:  $input=String
                 
                 (
                     not in($next moves, icm:sem*neg)
                    push(next moves, icm:per*pos:String)
            eff:
                    push(next moves, icm:sem*neg)


The purpose of the third condition is to prevent negative semantic understanding feedback
from being selected more than one time. Since only one string is recognized per turn,
there is never any reason to apply the rule more than once; and if anything at all can be
interpreted, the rule will not trigger at all even if some material was not used in interpreta-
tion. In a system with a wide-coverage recognizer and a more sophisticated interpretation
module, one may consider producing negative semantic understanding feedback for any
material which cannot be interpreted (e.g. “I understand that you want to go to Paris,
but I don’t understand what you mean by ‘Londres’.”).

The first update in this rule selects positive perception ICM to show the user what the
system heard. The second update selects negative semantic understanding ICM.


```

---

### Rule 3.13: selectIcmUndNeg

**Source**: Page 145 (Section Unknown)

```
(rule 3.13) rule: selectIcmUndNeg
                  select icm
            class:
                 
                   not in($next moves, icm:und*neg)
                    in($latest moves, answer(A))
                 
                 
                 
                 
                 
                  forall($latest moves/elem=M ove,
                 
            pre: 
                      $/private/nim/elem=M ove)
                    forall($latest moves/elem=answer(A0 ),
                 
                 
                 
                 
                 
                       not fst($/shared/QUD, D) and $domain :: relevant(A0, Q))
                 
                 
                 
                  forall do($latest moves/elem=M ove,
                 
            eff:      push(next moves, icm:sem*pos:M ove))
                 
                    push(next moves, icm:und*neg)

The first rule checks that negative pragmatic understanding feedback has not already been
selected. The second condition checks that the latest utterance contained an answer move,
and the third checks that none of the moves performed in the latest utterance has been
integrated; all moves in latest moves are still on nim. Finally, the fourth condition
checks that no answer is relevant to any question on QUD.

The first update selects positive feedback on the semantic understanding level for each move
performed in the latest utterance, to show that the utterance was at least understood to
some extent. The second update selects negative feedback and pushes it on next moves.

The system is thus able to make a distinction between utterances it cannot interpret (and
thus not ground), and utterances that it can interpret and ground but not integrate. The
rule in (3.15) triggers when integration fails because the system cannot see the relevance
of the user utterance in the current dialogue context. Negative pragmatic understanding
feedback is currently realized as “I don’t quite understand”; the idea is to indicate that
the utterance was almost fully understood, but not quite. Again, it can be argued what
the best realization is.


```

---

### Rule 3.2: selectIcmOther

**Source**: Page 133 (Section Unknown)

```
 (rule 3.2)     rule: selectIcmOther
                class:( select icm
                         in($/private/agenda, icm:A)
                pre:
                         not in($next moves, B) and B=ask(C)
                     (
                        push(next moves, icm:A)
                eff:
                        del(/private/agenda, icm:A)


Dialogue example: integrating user ask-move The dialogue below shows how a user
ask move with a score of 0.76 is successfully integrated, and positive understanding and
acceptance feedback is produced.


(dialogue 3.3)

S> Welcome to the travel agency!

U> price information please [0.76]

getLatestMoves


  set(/private/nim, oqueue([ask(?A.price(A))]))
   set(/shared/lu/speaker, usr)


  clear(/shared/lu/moves)
   set(/shared/pm, set([greet]))

integrateUsrAsk

```

---

### Rule 3.26: selectRespond

**Source**: Page 169 (Section Unknown)

```
(rule 3.26) rule: selectRespond
            class: select action
                 
                    is empty($/private/plan)
                     fst($/shared/QUD, A)
                 
                 
                 
                 
                 
                  in($/private/bel, B)
                 
            pre: 
                 
                    not in($/shared/com, B)
                     $domain :: resolves(B, A)
                 
                 
                 
                 
                 
                     not  in($/private/agenda, respond(A))
                 
                 n
            eff: push(/private/agenda, respond(A))


Similarly, the move selection rules in IBiS2 are repeatedly applied, popping actions off the
agenda queue and pushing the corresponding moves on next moves. As an example,
the selectAnswer rule is shown in (rule 3.27).


```

---

### Rule 3.27: selectAnswer

**Source**: Page 169 (Section Unknown)

```
(rule 3.27) rule: selectAnswer
            class: select move
                 
                    fst($/private/agenda, respond(A))
                  in($/private/bel, B)
                 
            pre: 
                 
                    not in($/shared/com, B)
                     $domain   :: resolves(B, A)
                 
                 (
                    push(next moves, answer(B))
            eff:
                    pop(/private/agenda)


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
system in each utterance. The IBiS2 selection algorithm first checks if some question-
raising action is already on the agenda; if not, it tries to select a new action. Then, it
selects moves and ICM repeatedly until nothing more can be selected.

```

---

### Rule 3.3: selectIcmUndIntAsk

**Source**: Page 134 (Section Unknown)

```
    (rule 3.3)     rule: selectIcmUndIntAsk
                   class: select icm
                         $/shared/lu/speaker==usr
                        
                   pre:  fst($/private/nim, ask(Q))
                        
                        (
                            $score ≤ 0.7
                           pop(/private/nim)
                   eff:
                           push(next moves, icm:und*int:usr*issue(Q))

```

---

### Rule 3.5: selectIcmUndIntAnswer

**Source**: Page 136 (Section Unknown)

```
 (rule 3.5)    rule: selectIcmUndIntAnswer
               class: select icm
                    
                       fst($/private/nim, answer(A))
                        $/shared/lu/speaker==usr
                    
                    
                    
                    
                    
                     $score ≤ 0.7
                    
               pre: 
                    
                       fst($/shared/QUD, B)
                        $domain :: relevant(A, B)
                    
                    
                    
                    
                    
                        $domain :: combine(B, A, C)
                    
                    (
                       pop(/private/nim)
               eff:
                       push(next moves, icm:und*int:usr*C)


The conditions check that there is a user answer move on nim whose content is relevant
to and combines with a question on QUD, and that the recognition score was less than or
equal to 0.7. If these conditions are true, the move is popped off nim and interrogative
understanding feedback is selected.


```

---

### Rule 3.9: selectIcmConNeg

**Source**: Page 142 (Section Unknown)

```
 (rule 3.9)    rule: selectIcmConNeg
               class: select icm
                     $input= ‘TIMED OUT’
                    
               pre:  is empty($next moves)
                    
                    n
                        is empty($/private/agenda)
               eff: push(next moves, icm:con*neg)


Unless the system has something else to do, this will trigger negative contact ICM by the
system, realised e.g. as “I didn’t hear anything from you.”. The purpose of this is primarily
to indicate to the user that nothing was heard, but perhaps also to elicit some response
from the user to show that she is still there. Admittedly, this is a rather undeveloped
aspect of ICM in the current IBiS implementation, and alternative strategies could be
explored. For example, the system could increase the timeout span successively instead of
repeating negative contact ICM every five seconds. Other formulations with more focus on
the eliciting function could also be considered, e.g. “Are you there?” or simply “Hello?”.

The second and third condition check that nothing is on the agenda or in next moves.
The motivation for this is that there is no reason to address contact explicitly in this case,
since any utterance from the system implicitly tries to establish contact.


Default ICM integration rule Since contact is not explicitly represented in the infor-
mation state proper, integration of negative system contact ICM moves have no specific
effect on the information state, and are therefore integrated by the default ICM integration
rule shown in (rule 3.10). Unless an ICM move has a specific integration rule defined for
it, it will be integrated by this rule.

```

---

### Rule 5.4: selectConfirmAction

**Source**: Page 239 (Section Unknown)

```
 (rule 5.4)   rule: selectConfirmAction
              class: select action
                   
                      fst($/shared/actions, A)
                    $domain :: postcond(A, P C)
                   
              pre: 
                   
                      in($/private/bel, P C)
                       not in($/shared/com, P C)
                   
                   n
              eff: push(/private/agenda, confirm(A))


The conditions in this rule check that the there is an action in /shared/actions whose
postcondition is believed by the system to be true, however, this is not yet shared infor-
mation. If this is true, a confirm action is pushed on the agenda. Eventually, this action
(which also is a dialogue move) is moved to next moves by (rule 5.5).


```

---

### Rule 5.5: selectConfirm

**Source**: Page 239 (Section Unknown)

```
 (rule 5.5)   rule: selectConfirm
              class:n select move
              pre: fst($/private/agenda, confirm(A))
                   (
                      push(next moves, confirm(A))
              eff:
                      pop(/private/agenda)

```

---

## Other Algorithms

### Rule 2.1: getLatestMove

**Source**: Page 63 (Section Unknown)

```
 (rule 2.1)   rule: getLatestMove
              class:( grounding
                       $latest moves=M oves
              pre:
                       $latest speaker=DP
                   (
                      /shared/lu/moves := M oves
              eff:
                      /shared/lu/speaker := DP

This rule copies the information about the latest utterance from the latest moves and
latest speaker to the /shared/lu field. The first condition picks out the (singleton)
set of moves stored by the interpretation module, and the second condition gets the value
of the latest speaker variable. The updates set the values of the two subfields of the
/shared/lu record correspondingly.


```

---

### Rule 2.10: removeFindout

**Source**: Page 72 (Section Unknown)

```
(rule 2.10) rule: removeFindout
            class: exec plan
                  fst($/private/plan, findout(Q))
                 
            pre:  in($/shared/com, P )
                 
                 n
                     $domain :: resolves(P, Q)
            eff: pop(/private/plan)


This rule removes a findout(Q) action from the plan in case there is a resolving proposition
P in /shared/com.

If there is a consultDB action topmost on the plan, (rule 2.11) will trigger a database
search.


```

---

### Rule 2.17: recoverPlan

**Source**: Page 86 (Section Unknown)

```
(rule 2.17) rule: recoverPlan
            class: exec plan
                 
                    fst($/shared/QUD, Q)
                  is empty($/private/agenda)
                 
            pre: 
                 
                    is empty($/private/plan)
                     $domain :: plan(Q, P lan)
                 
                 n
            eff: set(/private/plan, P lan)

However, this solution has a problem. If, when dealing with a question q, the system
asks a question qu and the user does not answer this question but instead raises a new
question q1, both q and qu will remain on QUD when q1 has been resolved. Now, if the
user simply answers qu immediately after q1 has been resolved, everything is fine and the
system will reload the plan for dealing with q. However, if the user does not answer q u,

```

---

### Rule 2.18: reraiseIssue

**Source**: Page 87 (Section Unknown)

```
(rule 2.18) rule: reraiseIssue
            class:( select action
                     fst($/shared/QUD, Q)
            pre:
                     not $domain :: plan(Q, SomeP lan)
                 n
            eff: push(/private/agenda, raise(A))


```

---

### Rule 2.19: removeRaise

**Source**: Page 88 (Section Unknown)

```
(rule 2.19) rule: removeRaise
            class: exec plan
                  fst($/private/plan, raise(A))
                 
            pre:  in($/shared/com, B)
                 
                 n
                     $domain :: resolves(B, A)
            eff: pop(/private/plan)


This rule is needed to avoid asking the same question twice in case it is first reraised and
then also included in a recovered plan.

A sample dialogue involving the system reraising an issue and recovering a plan is shown
in (dialogue 2.4). Incidentally, this dialogue also demonstrates information sharing be-
tween dialogue plans; when the user asks about visa, the system already knows what the
destination city is and thus does not ask this again. By contrast, in VoiceXML (McGlashan
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
     9
    Information sharing in VoiceXML is only possible in the case where a form F 1 calls another form F2.
When F2 is finished and control is passed back to F1, information may be sent from F2 to F1. Information
sharing is not supported e.g. in cases where user initiative leads to the adoption of F 2 while F1 is being
executed.

```

---

### Rule 2.7: and (rule 2.8,) respectively.

**Source**: Page 70 (Section Unknown)

```
(rule 2.7) and (rule 2.8,) respectively.


```

---

### Rule 2.9: findPlan

**Source**: Page 71 (Section Unknown)

```
 (rule 2.9)   rule: findPlan
                    find plan
              class:
                    fst($/private/agenda, respond(Q))
                   
              pre:  $domain :: plan(Q, P lan)
                   
                   (
                      not in($/private/bel, P ) and $domain :: resolves(P, Q)
                      pop(/private/agenda)
              eff:
                      set(/private/plan, P lan)

The first two conditions check that there is an action respond(Q) on the agenda and that
the system has a plan for dealing with Q. The third condition checks that the system does
not already know an answer to Q (if it does, the system should instead respond to Q). If
these conditions hold, the updates pop respond(Q) off the agenda and load the plan.

```

---

### Rule 3.14: rejectProp

**Source**: Page 149 (Section Unknown)

```
(rule 3.14) rule: rejectProp
            class: select action
                 
                    in($/private/nim, answer(A))
                     $/shared/lu/speaker=usr
                 
                 
                 
                 
                 
                  fst($/shared/QUD, Q)
                 
            pre: 
                 
                    $domain :: relevant(A, Q)
                     $domain :: combine(Q, A, P )
                 
                 
                 
                 
                 
                     not $database :: validDBparameter(P )
                 
                 
                  del(/private/nim, answer(A))
                 
            eff:  push(/private/agenda, icm:und*pos:usr*P )
                 
                     push(/private/agenda, icm:acc*neg:P )

The first five conditions are identical to those for the rule for integrating user answers,
integrateUsrAnswer (Section 3.6.6). The final condition checks that the proposition P,
resulting from combining a question on QUD with the content of the answer move, is not
a valid database parameter. The updates remove the move from nim and selects positive
understanding feedback to show what the system understood, and negative acceptance
feedback.

Of course, it is not optimally efficient that the same sequence of conditions is checked by
several different rules; an alternative approach would be to let one rule determine e.g. how
an answer move is relevant, combine it with a question on QUD, and store the result in
a datastructure containing pragmatically interpreted material. This datastructure could
then be inspected by both integration and rejection rules. (See also Section 6.5.1.)


```

---

### Rule 3.15: rejectIssue

**Source**: Page 151 (Section Unknown)

```
(rule 3.15) rule: rejectIssue
            class: select action
                  in($/private/nim, ask(Q))
                 
            pre:  $/shared/lu/speaker=usr
                 
                     not $domain :: plan(Q, P lan)
                 
                  del(/private/nim, ask(Q))
                 
            eff:  push(/private/agenda, icm:und*pos:usr*issue(Q))
                 
                     push(/private/agenda, icm:acc*neg:issue(Q))

The rule is similar to the rejectProp rule. The third condition checks that there is no
plan for dealing with the question Q.


Dialogue example: system issue rejection In the following dialogue, the user’s re-
quest for information about connecting flights is rejected on the grounds that the system
does not know how to address that issue.


(dialogue 3.9)

S> Okay.       The price is      123    crowns.

U> what about connecting flights

getLatestMoves
backupShared
rejectIssue

 del(/private/nim, ask(?A.con flight(A)))
   push(/private/agenda, )
   push(/private/agenda, icm:acc*neg:issue(?A.con flight(A)))

selectIcmOther
½
   push(next moves, icm:und*pos:usr*issue(?A.con flight(A)))
   del(/private/agenda, icm:und*pos:usr*issue(?A.con flight(A)))
selectIcmOther
½
   push(next moves, icm:acc*neg:issue(?A.con flight(A)))
   del(/private/agenda, icm:acc*neg:issue(?A.con flight(A)))

S> You asked about connecting flights.                Sorry, I cannot answer questions

```

---

### Rule 3.16: getLatestMoves

**Source**: Page 152 (Section Unknown)

```
(rule 3.16) rule: getLatestMoves
            class: grounding
                  $latest moves=M oves
                 
            pre:  $latest speaker=DP
                 
                     $/shared/lu/moves=P revM oves
                    set(/private/nim, M oves)
                 
                 
                 
                  set(/shared/lu/speaker, DP )
                 
            eff: 
                 
                   clear(/shared/lu/moves)
                    set(/shared/pm, P revM oves)
                 


```

---

### Rule 3.17: backupShared

**Source**: Page 153 (Section Unknown)

```
(rule 3.17) rule: backupShared
            class: none
            pre: 
                 {
                 
                  /private/tmp/QUD := $/shared/QUD
                  /private/tmp/com := $/shared/com
                 
            eff:
                 
                 
                  /private/tmp/agenda := $/private/agenda
                   /private/tmp/plan := $/private/plan
                 


```

---

### Rule 3.23: findPlan

**Source**: Page 165 (Section Unknown)

```
(rule 3.23) rule: findPlan
                  load plan
            class:
                  in($/private/agenda, respond(Q))
                 
            pre:  $domain :: plan(Q, P lan)
                 
                    not in($/private/bel, P ) and $domain :: resolves(P, Q)
                 
                  del(/private/agenda, respond(Q))
                 
            eff:  set(/private/plan, P lan)
                 
                    push(/private/agenda, icm:loadplan))

This rule is identical to that in IBiS1 (Section 2.8.6), expect for the final update which
pushes the icm:loadplan move on the agenda.


Reraising issues


System reraising of issue associated with plan If the user raises a question Q and
then raises Q0 before Q has been resolved, the system should return to dealing with Q once
Q0 is resolved; this was described in Section 3.6.9. The recoverPlan rule in IBiS2, shown
in (3.20), is almost identical to the one in IBiS1, except that ICM is produced to indicate
that an issue (q1) is being reraised. This ICM is formalized as icm:reraise:q where q is the
question being reraised, and expressed e.g. as “Returning to the issue of price”.


```

---

### Rule 3.24: recoverPlan

**Source**: Page 165 (Section Unknown)

```
(rule 3.24) rule: recoverPlan
            class:
                  load plan
                 
                 
                 
                    in($/shared/QUD, Q)
                  is empty($/private/agenda)
                 
                 
                 
            pre:  is empty($/private/plan)
                 
                 
                 
                   $domain :: plan(Q, P lan)
                  not in($/private/bel, P ) and $domain :: resolves(P, Q)
                 
                 
                  set(/private/plan, P lan)
                 
            eff:  push(/private/agenda, icm:reraise:Q)
                 
                    push(/private/agenda, icm:loadplan))


Issue reraising by user In the case where the user reraises an open issue, an icm:reraise:Q
move is selected by the integrateUsrAsk described in Section 3.6.6.


System reraising of issue not associated with plan The IBiS1 reraiseIssue rule
described in Section 2.12.3 reraises any questions on QUD which are not associated with

```

---

### Rule 3.25: reraiseIssue

**Source**: Page 166 (Section Unknown)

```
(rule 3.25) rule: reraiseIssue
            class:( select action
                     fst($/shared/issues, Q)
            pre:
                     not $domain :: plan(Q, P )
                 (
                    push(/private/agenda, icm:reraise)
            eff:
                    push(/private/agenda, raise(Q))

The conditions of this rule checks that there is a question Q on issues for which the system
has no plan, i.e. one that the system needs to ask the user.

The first update adds an icm:reraise (without an argument) to signal that it is reraising
a question; this is currently generated as prefixing “so” to the next ask move, which is
an ordinary raising of the question (placed on the agenda by the second update in the
rule). In a more sophisticated implementation one could consider abbreviating the original
raising of the question to make an appropriate reraising, e.g. “So, from what city?” But
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

### Rule 3.4: is similar to that for ask moves, except that answers are checked for relevance

**Source**: Page 135 (Section Unknown)

```
(rule 3.4) is similar to that for ask moves, except that answers are checked for relevance
as well as reliability and acceptability.


```

---

### Rule 4.1: accommodatePlan2Issues

**Source**: Page 188 (Section Unknown)

```
 (rule 4.1)      rule: accommodatePlan2Issues
                 class: accommodate
                      
                      
                      
                          $/private/nim/elem/snd = answer(A)
                      
                      
                      
                         not $lexicon :: yn answer(A)
                          in($/private/plan,   findout(Q))
                      
                      
                      
                      
                      
                       $domain :: relevant(A, Q)
                      
                 pre: 
                         $domain :: default question(Q) or
                             not ( in($/private/plan, findout(Q0 ))
                      
                      
                      
                      
                      
                      
                                    and Q 6= C
                      
                      
                      
                      
                                    and $domain :: relevant(A, Q0 ) )
                      
                      
                      n
                 eff: push(/shared/issues, B)

The first condition picks out a non-integrated answer move with content A. The second
condition checks that A is not a y/n answer (e.g. yes, no, maybe etc.), and thus im-
plements an assumption that such answers cannot trigger question accommodation, since
they are too ambiguous6. The third and fourth conditions check if there is a findout action
with content Q in the currently loaded plan, such that A is relevant to Q. The final con-
dition checks that there is no other question in the plan that the answer is relevant to, or
alternatively that Q has the status of a default question. If this condition does not hold, a
clarification question should be raised by the system; this is described in Section 4.6.3. The
“default question” option allows encoding of the fact that one issue may be significantly
more salient in a certain domain. For example, in a travel agency setting the destination
city may be regarded as more salient than the departure city question. If this is encoded
as a default question, then if the user says simply “Paris” it is interpreted as answering
the destination city question; no clarification is triggered7


```

---

### Rule 4.12: noFollowup

**Source**: Page 212 (Section Unknown)

```
(rule 4.12) rule: noFollowup
            class:( (none)
                     $input, ’TIMED OUT’
            pre:
                     in($/shared/pm, icm:und*pos:usr*Content)
                 
                 
                 
                 
                    if then else(Content=issue(Q), [
                        push(/private/tmp/usr/QUD, Q)
                 
                 
                 
                 
            eff:       push(/private/tmp/usr/issues, Q)
                 
                 
                 
                       push(/private/tmp/usr/agenda, respond(Q)) ],
                  add(/private/tmp/usr/com, Content))
                 


```

---

### Rule 4.13: backupSharedUsr

**Source**: Page 215 (Section Unknown)

```
(rule 4.13) rule: backupSharedUsr
            class: (none)
                 
                 
                    $latest speaker=usr
                     $latest moves=M oves
                 
                 
                 
                 
                 
                  not in(M oves, icm:X)
                 
                 
                 
            pre:     not in(M oves, no move)
                     not ( fst($/shared/QUD, und(usr*C)) and
                 
                 
                 
                 
                 
                        in(A, answer(D)) and
                 
                 
                 
                 
                 
                        $domain :: relevant(D, und(usr*C)))
                 
                 
                 
                 
                 
                 
                    /private/tmp/usr/QUD     := $/shared/QUD
                  /private/tmp/usr/issues := $/shared/issues
                 
                 
                 
            eff:    /private/tmp/usr/com := $/shared/com
                    /private/tmp/usr/agenda := $/private/agenda
                 
                 
                 
                 
                 
                  /private/tmp/usr/plan := $/private/plan
                 


```

---

### Rule 4.2: accommodateIssues2QUD

**Source**: Page 191 (Section Unknown)

```
 (rule 4.2)    rule: accommodateIssues2QUD
               class: accommodate
                    
                       $/private/nim/elem=usr-answer(A)
                        $domain :: short answer(A)
                    
                    
                    
                    
                    
                     not $lexicon :: yn answer(A)
                    
               pre: 
                    
                       in($/shared/issues, Q)
                        not in($/shared/QUD, Q)
                    
                    
                    
                    
                    
                        $domain   :: relevant(A, Q)
                    
                    (
                       push(/shared/QUD, Q)
               eff:
                       raise(/shared/issues, Q)


The second condition in (rule 4.2) checks that the content of the answer move picked out
by condition 1 is semantically underspecified. The third condition imposes a constraint
on local question accommodation, excluding short answers to y/n-questions (“yes”, “no”,
“maybe” etc.). The remaining conditions check that the answer-content is relevant to an
issue which is on issues but not on QUD. The first operation pushes the accommodated
question on QUD, and the final update raises the question to the top of the stack of open
issues.


```

---

### Rule 4.3: clarifyIssue

**Source**: Page 192 (Section Unknown)

```
 (rule 4.3)      rule: clarifyIssue
                 class: select action
                      
                         in($/private/nim, usr-answer(A))
                       setof(C, in($/private/plan, findout(Q)) and
                      
                 pre:
                      
                      
                            $domain :: relevant(A, Q), QSet)
                          $$arity(QSet) > 1
                      
                      
                       ! setof(?P, in(QSet, Q) and $domain :: combine(Q, A, P ), AltQ)
                      
                 eff:  push(/private/agenda, findout(AltQ))
                      
                         del(/private/nim, usr-answer(A))

The first condition picks out the answer-move from the nim queue. The second and third
conditions check that there is more than one question in the plan to which the answer
is relevant, by constructing the set of such questions. The first operation constructs the
alternative-question by applying each question in the set constructed in condition 2 to the
answer to get a proposition and prefixing the question operator ’ ?’ to each proposition
to get a y/n-question. The alternative question is this set of y/n-questions. The second
operation pushes the action to raise the alternative question on the agenda, and the final
operation removes the answer move from nim; this is motivated above.

A sample dialogue with issue clarification is shown in (dialogue 4.2).


(dialogue 4.2)

S> Welcome to the travel agency!
U> price information please
S> Okay. I need some information. How do you want to travel?
U> flight um paris
S> OK, by flight. Do you mean from paris or to paris?
   8
    IBiS3 only handles full answers to clarification questions, i.e. “To Paris.” or “From Paris.”. A slightly
more advanced semantics would be required to handle cases where the user again gives an underspecified
response which resolves the question, i.e. “To.” or “From.”.

```

---

### Rule 4.4: accommodateDependentIssue

**Source**: Page 194 (Section Unknown)

```
 (rule 4.4)    rule: accommodateDependentIssue
               class:
                     accommodate
                    
                    
                    
                       setof(A, $/private/nim/elem/snd=answer(A), AnsSet)
                       $$arity(AnsSet) > 0
                    
                    
                    
                    
                    
                    
                    
                    
                      is empty($/private/plan)
                       $domain :: plan(DepQ, P lan)
                    
                    
                    
                    
                    
                     forall(in(AnsSet, A), in(P lan, findout(Q)) and
                    
               pre: 
                          $domain :: relevant(A, Q))
                       not ( $domain :: plan(DepQ0, P lan0 ) and DepQ0 6= DepQ and
                    
                    
                    
                    
                    
                           forall(in(AnswerSet, A), in(P lan0, findout(Q)) and
                    
                    
                    
                    
                    
                    
                    
                    
                    
                             $domain :: relevant(A, Q)) )
                       not  in($/private/agenda,    icm:und*int:usr*issue(DepQ))
                    
                    
                    
                    
                    
                    
                      push(/shared/issues, DepQ)
                     push(/private/agenda, icm:accommodate:DepQ)
                    
                    
                    
               eff:  push(/private/agenda, icm:und*pos:usr*issue(DepQ))
                    
                    
                    
                     set(/private/plan, P lan)
                     push(/private/agenda, icm:loadplan)
                    


```

---

### Rule 4.5: clarifyDependentIssue

**Source**: Page 198 (Section Unknown)

```
    (rule 4.5)   rule: clarifyDependentIssue
                 class: select action
                      
                      
                         in($/private/nim, pair(usr, answer(A)))
                          setof(Q0, $domain :: plan(Q0, P lan) and
                      
                      
                      
                      
                      
                             in(P lan, findout(SomeQ)) and
                      
                      
                      
                      
                 pre:       $domain :: relevant(A, SomeQ),
                      
                      
                      
                         QSet0 )
                          remove unifiables(QSet0, QSet)
                      
                      
                      
                      
                      
                       $$arity(QSet) > 1
                      
                      (
                         ! setof(IssueQ, in(QSet, I) and IssueQ=?issue(I), AltQ)
                 eff:
                         push(/private/agenda, findout(AltQ))

```

---

### Rule 4.6: accommodateCom2Issues

**Source**: Page 201 (Section Unknown)

```
 (rule 4.6)     rule: accommodateCom2Issues
                class: accommodate
                     
                     
                     
                         $/private/nim/elem/snd=answer(A)
                         in($/shared/com,   P)
                     
                     
                     
                     
                pre:  $domain :: question(Q)
                     
                     
                     
                        $domain :: relevant(A, Q)
                      $domain :: relevant(P, Q)
                     
                     n
                eff: push(/shared/issues, Q)


This accommodation rule looks for an answer A among the moves which have not yet been
integrated (first condition). It then looks for a proposition among the shared commitments
established in the dialogue so far (second condition) which according to the system’s domain
resource is an appropriate answer to some question for which A is also an answer (third to
fifth conditions). Given that in this simple system answers can only be relevant to a single
question10, this strategy will be successful in identifying cases where we have two answers
to the same question. A system that deals with more complex dialogues where this is not
the case would need to keep track of closed issues in a separate list of closed issues. Thus
the conditions will succeed if there is a question such that both the user answer and a stored
proposition are relevant answers to it; in the example dialogue above, “departure date is
the fourth” and “departure date is the fifth” are both relevant answers to the question
“which day do you want to travel?”. If such a question is found it is accommodated to
issues, that is, it becomes an open issue again.

When accommodateCom2Issues has been successfully applied, the retract rule in (rule
  10
    That is, in the full form in which they appear in $/shared/com. “Chicago” can be an answer to
“Which city do you want to go to?” and “Which city do you want to go from?” but when it has been
combined with the questions the result will be “destination(Chicago)” and “from(Chicago)” respectively
and it is this which is entered into the commitments.

```

---

### Rule 4.7: retract

**Source**: Page 202 (Section Unknown)

```
 (rule 4.7)    rule: retract
               class: integrate
                    
                    
                       $/private/nim/elem/snd=answer(A)
                        in($/shared/com,   P 0)
                    
                    
                    
                    
                    
                     fst($/shared/issues, Q)
                    
                    
                    
               pre:  $domain :: relevant(P, Q)
                    
                    
                    
                       $domain :: relevant(A, Q)
                        $domain :: combine(Q, A, P )
                    
                    
                    
                    
                    
                     $domain :: incompatible(P, P 0 )
                    
                    n
               eff: del(/shared/com, P 0 )


The conditions here are similar to those in (rule 4.6). We look for an unintegrated
answer (first condition) which is relevant to a question at the head of the list of open issues
(third and fifth conditions) and for which there is already a relevant answer in the shared
commitments (second and fourth conditions). Finally, we determine that the result of
combining the answer with the question (sixth condition) is incompatible with the answer
already found (seventh condition). If all this is true we delete the answer which is currently
in the shared commitments. This will finally allow the new answer to be integrated by a
rule that integrates an answer from the user, and a further rule will remove the resolved
issue from QUD. Note that this rule is of class integrate. As is indicated in Appendix B, it
is tried before any other integration rule, to avoid integration of conflicting information.

Note also that the “incompatible” relation is defined as a part of the domain resource, and
can thus be domain specific. The simple kind of revision that IBiS currently deals with
is also handled by some form-based systems (although they usually do not give feedback
indicating that information has been removed or replaced, as IBiS does). For example,
Chu-Carroll (2000) achieves a similar result by extracting parameter values from the latest
user utterance and subsequently (if possible) copying values from the previous form for
any parameters not specified in the latest utterance. A similar mechanism is referred to
as “overlay” by Alexandersson and Becker (2000). While we are dealing only with very
simple revision here, the rule in (rule 4.7) and the “incompatible” relation can be seen as
placeholders for a more sophisticated mechanism of belief revision.

It is also possible to remove the old answer by denying it (asserting its negation) as in
(dialogue 4.7).


(dialogue 4.7)

```

---

### Rule 4.8: accommodateCom2IssuesDependent

**Source**: Page 204 (Section Unknown)

```
 (rule 4.8)    rule: accommodateCom2IssuesDependent
               class: accommodate
                    
                       $/private/nim/elem/snd=answer(A)
                        in($/shared/com, P )
                    
                    
                    
                    
                    
                        $domain :: question(Q)
                    
                    
                    
                    
                    
                     $domain :: relevant(A, Q)
                    
                    
                    
               pre:  $domain :: relevant(P, Q)
                    
                    
                    
                       is empty($/shared/issues)
                        $domain :: depends(Q0, Q)
                    
                    
                    
                    
                    
                        in($/shared/com, P 0 )
                    
                    
                    
                    
                    
                        $domain :: relevant(P 0, Q0 )
                    
                    
                    
                       del(/private/bel, P 0 )
                                             0
                    
                     del(/shared/com, P )
                    
                    
                    
               eff:  push(/shared/issues, Q0 )
                    
                    
                    
                       push(/shared/issues, Q)
                     push(/private/agenda, respond(Q0 ))
                    


```

---

### Rule 4.9: accommodateQUD2Issues

**Source**: Page 205 (Section Unknown)

```
 (rule 4.9)    rule: accommodateQUD2Issues
               class: accommodate
                    
                       $/private/nim/elem/snd=answer(A)
                     in($/shared/QUD, Q)
                    
               pre: 
                    
                       $domain :: relevant(A, Q)
                        not in($/shared/issues, Q)
                    
                    n
               eff: push(/shared/issues, Q)


The rule in (rule 4.9) picks out a non-integrated answer-move which is relevant to a
question on QUD which is not currently an open issue, and pushes it on issues.

To handle integration responses to positive understanding feedback, we also need to mod-
ify the integrateNegIcmAnswer rule described in Section 3.6.6. A significant difference
between positive and interrogative feedback in IBiS is that the former is associated with
cautiously optimistic grounding, while the latter is used in the pessimistic grounding strat-
egy. This means that a negative response to feedback on the understanding level must be
handled differently depending on whether the content in question has been added to the
dialogue gameboard or not. Specifically, if the positive feedback is rejected the optimistic
grounding assumption must be retracted.

```

---

### Rule 5.2: rejectAction

**Source**: Page 238 (Section Unknown)

```
 (rule 5.2)   rule: rejectAction
              class: select action
                    in($/private/nim, request(A))
                   
              pre:  $/shared/lu/speaker=usr
                   
                       not $domain :: plan(A, P lan)
                   
                    del(/private/nim, request(A))
                   
              eff:  push(/private/agenda, icm:und*pos:usr*action(A))
                   
                       push(/private/agenda, icm:acc*neg:action(A))


```

---

### Rule 5.8: accommodateAction

**Source**: Page 243 (Section Unknown)

```
 (rule 5.8)    rule: accommodateAction
               class:
                     accommodate
                    
                    
                    
                       setof(A, $/private/nim/elem/snd=answer(A), AnsSet)
                       $$arity(AnsSet) > 0
                    
                    
                    
                    
                    
                    
                    
                    
                      $domain    :: plan(Action, P lan)
                       $domain :: action(Action)
                    
                    
                    
                    
                    
                     forall(in(AnsSet, A), in(P lan, findout(Q)) and
                    
               pre: 
                         $domain :: relevant(A, Q))
                       not $domain :: plan(Action0, P lan0 ) and Action0 6=Action and
                    
                    
                    
                    
                    
                          forall(in(AnsSet, A), in(P lan0, findout(Q)) and
                    
                    
                    
                    
                    
                    
                    
                    
                    
                         $domain :: relevant(A, Q))
                       not in($/private/agenda, icm:und*int:usr*action(Action))
                    
                    
                    
                    
                    
                    
                      push(/shared/actions,       Action)
                     push(/private/agenda, icm:accommodate:Action)
                    
                    
                    
               eff:  push(/private/agenda, icm:und*pos:usr*action(action))
                    
                    
                    
                     set(/private/plan, P lan)
                     push(/private/agenda, icm:loadplan)
                    


```

---

### Rule 5.9: clarifyIssueAction

**Source**: Page 243 (Section Unknown)

```
 (rule 5.9)    rule: clarifyIssueAction
               class: select action
                    
                    
                    
                        in($/private/nim, pair(usr, answer(A)))
                     setof(Action, $domain :: depends(α, Q) and
                    
                    
                    
               pre:        $domain :: relevant(A, Q), ActionSet)
                    
                    
                    
                       remove unifiables(Actions, Actions0 )
                     $$arity(Actions0 ) > 1
                    

                        ! setof(?IssueP rop, in(Actions0, Issue0 ) and
                    
                    
                    
                           not $domain :: action(Issue0 ) and
                    
                    
                    
                    
                    
                           IssueP rop=issue(Issue0 ), IssueQuestions)
                    
                    
                    
                    
                    
                     ! setof(?ActionP rop, in(Actions0, Action0 ) and
                    
               eff: 
                    
                          $domain :: action(Action0 ) and
                           ActionP rop=action(Action), ActionQuestions)
                    
                    
                    
                    
                    
                        ! union(IssueQuestions, ActionQuestions, AltQ)
                    
                    
                    
                    
                    
                    
                        push(/private/agenda, findout(AltQ))

```

---

