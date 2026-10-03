# Week 1 — Candidate list

**Problem space.** Software developers and programming-language learners want
targeted, hands-on practice that trains a specific debugging skill, but the
existing platforms offer general exercises rather than exercises for a
particular kind of debugging problem.

## How we searched

We searched for: debugging exercises, debugging practice, coding challenge
platforms (LeetCode-style), live-coding interview training, bug-bounty
sandboxes, game-style debugging tools, and debugging-specific MOOCs and
documentation. Search date: **2026-10-01**. We used general web search and
GitHub topic searches. Every candidate below has a URL and one line on why it
might be relevant.

## Candidates (wide list)

| # | Candidate | URL | Why it might be relevant |
|---|-----------|-----|--------------------------|
| C01 | LeetCode The reference coding-problem platform; debugging happens incidentally, not as a first-class mode. |
| C02 | Exercism | https://exercism.org | Free practice tracks with mentoring; exercises, but not debugging-specific. |
| C03 | Codewars | https://www.codewars.com | Ranked kata; no debugging focus. |
| C04 | HackerRank Coding challenges; debugging is a side effect. |
| C05 | Codecademy | https://www.codecademy.com | Guided courses; learners, but content is tutorial-style, not debugging training. |
| C06 | freeCodeCamp | https://www.freecodecamp.org | Free curriculum; wide, not debugging-specific. |
| C07 | Pramp | https://www.pramp.com | Peer mock interviews; debugging of the candidate's own code under pressure. |
| C08 | Interviewing.io | https://interviewing.io | Live technical interviews, some with bug-fixing rounds; audience is interview prep. |
| C09 | HackerEarth | https://www.hackerearth.com | Hackathons and challenges; debugging not a category. |
| C10 | GDB / LLDB tutorials | https://sourceware.org/gdb/ | Tool documentation, not a practice site; teaches the debugger, not debugging. |
| C11 | "How to Debug" — Julia Evans (jvns.ca) Legendary zine on debugging; reading material, not hands-on exercises. |
| C12 | Rustlings | https://github.com/rustlings/rustlings | Rust practice by fixing compiler/lint errors; closest structured "fix the errors" model, but narrow (Rust only). |
| C13 | "fix-it" / buggy-code repos (e.g. `inspired-vs-inspirer`, `debugging-practice` on GitHub) | https://github.com/search?q=debugging+practice&type=repositories | Open-source collections of buggy programs; no generator, no grading, no gallery. |
| C14 | SQLZoo | https://sqlzoo.net | Query exercises; debugging not the focus. |
| C15 | CodinGame | https://www.codingame.com | Game-based challenges; gamification precedent, not debugging-specific. |
| C16 | Jupyter "debugging" courses / University of Helsinki Python MOOC | https://programming-24.mooc.fi/ | MOOC; debugging practice appears in passing. |
| C17 | Exercism "debugging" mentoring threads | https://exercism.org | Community mentoring occasionally covers debugging; not structured. |
| C18 | Xcode / Android Studio built-in exercises | https://developer.apple.com/ | IDE documentation; learning the IDE, not debugging skill. |
| C19 | CodeSignal | https://codesignal.com | Assessment platform; general challenges. |
| C20 | "Dojo" debugging games (e.g. `debugger-gym`-style side projects) | https://github.com/topics/debugging | Small hobby projects; the exact gap but not a product. |

## Cut candidates (kept for later reuse)

| # | Candidate | Why we cut it |
|---|-----------|----------------|
| C01 LeetCode, C03 Codewars, C04 HackerRank, C19 CodeSignal | Generic coding platforms; debugging is incidental, so they cannot be the direct competitor for "debugging-specific practice". Kept as the *adjacent substitute* baseline. |
| C02 Exercism, C05 Codecademy, C06 freeCodeCamp, C16 MOOCs | Tutorial-style learning; they teach by example, not by letting the learner debug under failure conditions. Cut as not debugging-focused. |
| C07 Pramp, C08 Interviewing.io | Audience is job-interview prep, not general skill-building; grading is human and expensive. Cut for scope. |
| C10 GDB/LLDB docs, C11 Julia Evans zine, C18 IDE docs | Read-only documentation; they explain tools, they do not give exercises. Cut because the problem is hands-on practice. |
| C12 Rustlings | The closest "fix the broken code" model; but single language and toolchain-bound. Revisit as an open-source reference. |
| C13 buggy-repo collections | Community collections of bugs; no generator, no auto-grading, no gallery. Strong evidence for the gap. |
| C15 CodinGame, C20 hobby debugging games | Gamification ideas worth borrowing; not a debugging training product. |
| C14 SQLZoo, C17 Exercism threads | Not debugging-specific. |

## Candidates chosen for deep research

From the wide list we picked three to research as `ALT-01`..`ALT-03`,
covering a direct competitor, an adjacent substitute, and an open-source /
self-hosted option:

- **ALT-01** — CodinGame (game-based challenges; closest interactive-training model) — *adjacent substitute*.
- **ALT-02** — LeetCode (the generic coding-problem platform developers already use) — *adjacent substitute / general baseline*.
- **ALT-03** — Rustlings (open-source "fix the broken code" track) — *open-source option*.

> We deliberately have no strong *direct* competitor: no mainstream product
> sells "generate a debugging exercise for a chosen problem category and debug
> it in your own IDE". That absence is the central finding and the seed of the
> gap analysis.

*Search date: 2026-10-01.*