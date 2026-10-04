# Meeting report — Customer kickoff

> **Customer:** course instructor (referred to only as *Customer* in all
> artifacts).
> **Date:** 2026-10-02.
> **Team (all attending):** Tedor49, Magel0n, NikitaRUniverse, Doosuur14.
> **Attendees (roles):** Interviewer — Magel0n · Note taker — Doosuur14 ·
> Observer — Tedor49.
> **Permissions:** asked and granted before recording — audio/video recording:
> quoting in public artifacts: **granted** · naming the meeting in the
> week report: **granted**.

## 1. Objective

The project is a debugging-practice tool: it generates buggy programs
automatically and runs them in a reproducible environment where a learner can
practice debugging with modern tooling (IDE, debugger, language server,
agent), with an extra element of openness — published solutions and questions
supporting the system. Before the meeting we compared market alternatives
(CodinGame, LeetCode, Rustlings) and identified a research gap: no deployable
tool lets a user train debugging in their own VS Code with generated problems.

The meeting was meant to test our GAP/VP assumptions with the customer: who
the target audience really is, how they practice today, where they get stuck,
which parts of our proposed direction matter most, and what hard constraints
(infrastructure, budget, language scope) we must design around.

## 2. Summary of the discussion

**Competitors / gap.** We presented our analysis of CodinGame, LeetCode and
Rustlings; LeetCode was deemed the closest because it could generalize its
problem database, but doing so requires significant effort they have not made.
The customer added **Codааeforces**, which lets you "hack" another participant's
solution by crafting a failing test after a contest — but noted you cannot
really debug with modern tooling there; you still have to load the code into
your own IDE. This strengthened the case for our "debug in your own IDE"
direction.

**Business goals & outcome.** Asked how success would be known, the customer
said that for *students* they could run paper-based exams where debugging is
done without the tool, then see who spots bugs quickly. For a *general
audience* there is no reasonable test that confidently shows learning, because
a learner could ask an agent to complete the task for them. The customer was
explicit that "using an agent to debug a task is not the point of this
exercise."

**Target audience.** University students (bachelor and, depending on program,
master) most acutely feel the pain of repeating the same kind of bug. Masters
learning a new language (e.g. Prolog) or advanced debugging topics are also
candidates. We may assume novices who are *not complete beginners* — they have
experience with the language they want to practice. A practical constraint: if
users supply their own API key, they should be over 18 (age at which they can
legally make such transactions).

**Metrics.** The customer rejected time-spent-debugging as unreliable
(ambiguous — a user may walk away or keep thinking; no commands run). More
promising: diversity of problems solved tied to a goal (e.g. cover concurrency
in Go) and how many topics/lessons/prompts a learner completes. The customer
had no definitive metric in mind; we agreed to gather statistics and figure it
out once we have tests.

**Current practice.** No deliberate debugging courses exist at the university.
People typically contribute to established GitHub projects or solve tasks from
scratch on Codeforces/LeetCode. General audience is assumed (people who at
least know what debugging is), but only students allow controlled assessment.

**Workflow envisioning.** The customer described: a website where the learner
chooses a topic/parameters and generates a setup; the site sends a link that
opens their IDE with all tools ready (compiler, language server, debugger
extensions, a terminal, and probably an agent to guide). A harness is generated
alongside the buggy code so the learner can observe the bug; running tests
shows whether the bug is gone. On completion the learner runs a "finish"
command, the session is assessed, and they return to the site. A simpler
alternative is the GitHub-style "press `.` → CodeSpace" flow that opens the
code in a browser VS Code with pre-installed extensions (noting some
extensions aren't supported in the browser).

**Where users get stuck.** The customer listed several failure points: not
understanding how to run the tests / not discovering the harness; container
memory exhaustion making the system unresponsive; lost server connection;
infinite loops that cannot be killed; not knowing the finish command; not
knowing how to invoke the agent (or that an agent even exists); and not knowing
to go back to the site afterward. This implies we should provide clear
instructions and links at each step.

**Instructor-side.** Sessions may not be supervised. The most frustrating part
of current practice for an instructor is figuring out what state a student's
environment is in — but with an invariable, simple environment this should be
minor. Technical failures (disconnections) and API-key budget limits (a student
burning a shared key) can frustrate instructors; tracking limits may be
necessary.

**What learners do when stuck.** In the toolkit course they prompt the agent
more fiercely until it solves the bug; failure occurs when the agent's context
is exhausted with no result, and the student wastes ~20 minutes watching the
agent debug — again confirming agent-as-solver is not the goal.

**Constraints.** We will likely get a university VM with **16 GB RAM / 8 CPUs**
(more possible but not yet negotiated). Expected tooling: Docker containers or
NixOS VMs for reproducible environments. Budget: **$5–$10 API key**, with a
recommendation to use cheaper models for prototyping. Student prerequisites
should be minimal — they enter the site and connect to an environment. Options:
VS Code installed with extensions, VS Code in the browser (limitations), or
another editor (e.g. CodeMirror) with debugging/language-server plugins.
Problems must be **self-contained** (harness and program runnable, and ideally
copyable to run locally outside our environment).

**Priority in v1.** Asked to choose one thing to do well, the customer picked
**debugging in the user's own IDE** because it is the most technically risky
part (can we connect to a VM from the user's VS Code or browser?). **Exercise
generation** ranked second — prompt tweaking and exercise layout/VM layout
matter. On removal: the customer is "greedy" and would remove nothing yet;
scope will be discussed in later meetings.

**Language scope.** A **single language (e.g. Python) is fine for the
prototype**, but the **MVP must support several languages** (mainstream — Python,
TypeScript, possibly Java or Scala), and the system must be designed to be
multi-language from the start.

**Other contacts.** The customer knows no one thinking about exactly this
problem, but suggested talking to admins or active participants / contest
creators of platforms like LeetCode or Codeforces.

## 3. Decisions

| # | Decision | Source (GAP/VP) | Who it affects |
|---|----------|-----------------|----------------|
| D1 | First release should do "debugging in the user's own IDE" well; exercise generation is second priority; public gallery is lower priority. | VP-03 | Engineering, product |
| D2 | Target audience: university students and non-beginners who know debugging; not complete beginners; general audience possible but only students allow controlled assessment. | VP-01 | Product, research |
| D3 | Problems must be self-contained (program + harness), reproducible via Docker containers or NixOS VMs on the provided 16 GB / 8 CPU VM, with minimal student prerequisites. | GAP-03 | Engineering |

## 4. Action points

| # | Action | Owner | Due date (Week 2) |
|---|--------|-------|-------------------|
| A1 | Build a single-language (Python) prototype focused on debugging in the user's own IDE. | Magel0n | Fri of Week 2 |
| A2 | Design the system so it is extensible to multiple languages (language server, debugger, extensions pluggable per language). | Tedor49 | Fri of Week 2 |
| A3 | Define the exercise layout (buggy code + harness) and the reproducible container/VM setup within the 16 GB / 8 CPU constraints. | NikitaRUniverse | Fri of Week 2 |
| A4 | Draft a statistics/metrics plan (topic/goal coverage, not time-based) and a budget/spend-tracking approach for the $5–$10 API key. | Doosuur14 | Fri of Week 2 |

## 5. Disagreements

| Position we held | Customer's objection | How we will respond |
|------------------|----------------------|---------------------|
| LeetCode is the closest competitor worth watching. | Codeforces also offers similar "hack a solution" practice after contests. | Add Codeforces to the competitive landscape; position our differentiator as modern in-IDE debugging. |
| Success can be measured by time spent debugging. | Time is unreliable (ambiguous idle vs. thinking); no confident learning signal. | Drop time-based metrics; measure topic/problem coverage tied to goals. |
| An agent in the environment can help learners debug. | Using an agent to solve the task defeats the purpose of the exercise. | Design the agent as a guide that coaches the learner rather than solving the bug for them. |
| (Implicit) exercise generation is the core of v1. | The user's-own-IDE debugging is the most technically risky part and should come first. | Prioritize the in-IDE experience in the first release; treat generation as second. |

## 6. Open questions

Questions we could not resolve in the meeting. The week report does not
repeat these; it links here.

- Which exact languages should the MVP support? (Customer: "decide later" —
  candidates Python, TypeScript, possibly Java or Scala.)
- Who provides the API key and how are spend limits tracked to avoid a student
  exhausting a shared key?
- Will debugging sessions be supervised by an instructor at all?
- Browser VS Code vs. installed extensions vs. a third editor (CodeMirror):
  which UX should v1 target, given browser extension limitations?
- What is a reliable metric for "the learner learned to debug" for a general
  (non-student) audience?
- Can the university IT department provide more than 16 GB RAM / 8 CPUs?
- Should we reach out to Codeforces/LeetCode admins or contest creators for
  further input, as the customer suggested?

---

## Changes to the value proposition

None