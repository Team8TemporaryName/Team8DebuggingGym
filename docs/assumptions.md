# Assumptions

This file records each assumption the project rests on, one `ASM-nn` section
per assumption, in identifier order. A story that rests on an assumption lists
it in its `Rests on` list and links here. An assumption is settled with
evidence, citing the `DEC-nnn` that settled it.

## ASM-01

A real audience wants skill-category debugging practice, not just general coding practice.

- **Status:** Open
- **How to check:** settle with the customer at the kickoff and check the
  "fix-the-bug" demand signals in the candidate list, in Week 1.
- **Outcome:** (not yet settled)

## ASM-02

Learners will accept connecting their IDE for practice, because the setup cost is worth it.

- **Status:** Likely
- **How to check:** ask about willingness to set up VS Code at the kickoff,
  and confirm with the VS Code prototype in Week 2.
- **Outcome:** the VS Code prototype attached successfully and let the team
  debug a buggy program with breakpoints, and the customer confirmed the local
  debugging experience is the right priority ([DEC-004](decisions.md#dec-004)).
  Whether learners themselves accept the setup remains to be seen.

## ASM-03

An LLM can reliably generate exercises that contain the intended bug and are solvable within our quality budget.

- **Status:** Likely
- **How to check:** run a small generation experiment in Week 2 and measure
  defect-presence and solvability rates.
- **Outcome:** the generator now produces LLM-generated exercises with the
  customer's API key and a deterministic fallback; the customer watched a
  generated exercise be solved and verified in the Week 4 meeting. Whether the
  LLM stays within the quality budget at scale remains to be measured.

## ASM-04

Running user-attached debug sessions safely on a VPS is achievable within our time and security budget.

- **Status:** Likely
- **How to check:** spike a container plus Debug Adapter Protocol bridge in
  Week 2.
- **Outcome:** the prototype proved a learner can attach their own VS Code to
  a hosted container over DAP and hit breakpoints on code running remotely.
  The team and customer agreed in Week 4 to run learner code in sandboxed
  containers with capped resources and limited networking
  ([DEC-016](decisions.md#dec-016)), and the team still needs to control what
  task authors can ship ([DEC-008](decisions.md#dec-008)).

## ASM-05

The public gallery is a differentiator worth moderating, not a commodity feature.

- **Status:** Open
- **How to check:** compare the value of a gallery against solo generation with
  the customer at the kickoff.
- **Outcome:** (not yet settled)

## ASM-06

Developers and learners are a single reachable audience, and interview-prep candidates are not the focus.

- **Status:** Partially settled
- **How to check:** ask the customer explicitly about the audience at the
  kickoff.
- **Outcome:** the customer confirmed university students and non-beginners
  are the target (not interview-prep), but then said the system should also
  accommodate complete beginners, as long as instructions are clear, precise,
  and concise ([DEC-002](decisions.md#dec-002)).
