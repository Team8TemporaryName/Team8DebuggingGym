# Kickoff meeting script

**Date:** *TODO — schedule in Week 1.*
**Duration:** 30 minutes planned, asking for 60.
**Roles:** Interviewer — Magel0n · Note taker — Doosuur14 · Observer — Tedor49.
**Team attending:** Tedor49, Magel0n, NikitaRUniverse, Doosuur14 (all).

> The whole team attends. We ask the three permission questions before
> recording: (1) may we record the audio/video? (2) may we quote you in public
> research artifacts? (3) may we name the meeting in the week report? The
> recording stays out of the repository and goes only in the Moodle
> submission.

## Opening

- Thank the customer and restate the problem space in one sentence.
- Present the proposed direction and its evidence (alt-list → gaps → value
  proposition) in ~5 minutes.
- State the goal: find where our reading of the problem is wrong, not to have
  them design the product.

## 1. Business goals

- **Open.** What outcome would you most want a debugging-practice tool to
  achieve for your students/developers — and how would you know it worked?
- **Open.** Who in your world feels the pain of "I keep hitting the same kind
  of bug" most acutely?
- **Closed.** Would you rather see learners spend more *time* debugging, or
  more *skill* per hour?

## 2. End users

- **Open.** When you imagine a learner using this, what does their current
  debugging session look like, step by step?
- **Open.** What do your users do *today* when they want to get better at
  debugging?
- **Closed.** Are your users more likely to be students in a course, working
  developers, or language learners?

## 3. Current workflow

- **Open.** Walk me through how a learner practises debugging now — what tools
  do they actually open?
- **Open.** Where in that workflow do they give up or get stuck?
- **Closed.** Do they debug mainly in an IDE (like VS Code), or in a browser/
  terminal?

## 4. Pain points and constraints

- **Open.** What is the most frustrating part of current debugging practice —
  for you as the instructor and for the learner?
- **Open.** When a learner gets a bug they cannot solve, what do they do, and
  why does that fail?
- **Closed.** Is there any constraint we should know about — class size,
  environments, tooling students are allowed to install?

## 5. Scope

- **Open.** If we could only do one thing well in the first version, which of
  these would you choose: generated exercises for a chosen category, debugging
  in the user's own IDE, or a public gallery? (And why.)
- **Open.** What would you *remove* from our proposed direction?
- **Closed.** Would a single-language (e.g. Python) first version be
  acceptable, or is multi-language required from the start?

## Closing

- **Open.** Who else should we talk to who knows this problem differently from
  you?
- Restate next steps and thank the customer.

---

## Key improvements

To satisfy the requirement, here are two questions we rewrote and the principle
behind each rewrite.

**Rewrite 1 — turn a leading yes/no into an open behavioural question.**

- *Before:* "Do you agree that learners would benefit from debugging exercises
  in their own IDE?" *(closed, leading, invites agreement.)*
- *After:* "When you imagine a learner using this, what does their current
  debugging session look like, step by step?" *(open, elicits behaviour, does
  not feed the answer.)*
- **Principle:** Closed leading questions confirm our own bias; behavioural
  open questions surface facts we did not predict. (Mom Test-style: ask what
  people do, not what they believe.)

**Rewrite 2 — force a trade-off instead of a wish list.**

- *Before:* "Which features are most important to you?" *(open but invites a
  list of everything; every answer is safe.)*
- *After:* "If we could only do one thing well in the first version, which
  would you choose: generated exercises, debugging in your own IDE, or a
  public gallery? And why?" *(forced-choice; the customer has to give something
  up, so their real priority shows.)*
- **Principle:** People avoid ranking their own ideas unless forced; a
  constrained choice reveals what actually matters and which of our
  assumptions (A6, VP-01..04) they would drop first.