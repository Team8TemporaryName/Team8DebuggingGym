# Decisions

This file records each decision the team has made, one `DEC-nnn` section per
decision, in identifier order. A decision is written here before anything
cites it, and any artifact it changes cites it back.

## DEC-001

Debugging in the user's own IDE is the first priority.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:** [the kickoff meeting](../reports/week-01/meeting-report.md)
- **Why:** the customer judged "debugging in the user's own IDE" the most
  technically risky part — can the user's VS Code or browser connect to a VM
  we host? — and so the part to de-risk first.
  Exercise generation is second priority; the public gallery is lower.

## DEC-002

Target university students and non-beginners, not complete beginners.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:** [the kickoff meeting](../reports/week-01/meeting-report.md)
- **Why:** university students (bachelor and, depending on program, master)
  feel the pain of repeating the same kind of bug most acutely, and masters
  learning a new language are also candidates; a general audience is possible,
  but only students allow controlled assessment, which we need to show
  learning.

## DEC-003

Problems are self-contained and reproducible on the provided VM.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:** [the kickoff meeting](../reports/week-01/meeting-report.md)
- **Why:** problems must be self-contained (program + harness), reproducible
  via Docker containers or NixOS VMs on the provided 16 GB / 8 CPU VM, with
  minimal student prerequisites, so the environment stays invariable and the
  student's environment state is a non-issue for instructors.

## DEC-004

Debugging stays in the learner's own installed IDE, as a local debugging experience, with files available locally.

- **Status:** Active
- **Date:** 2026-10-14
- **Made by:** Customer
- **Source:** [the Week 2 validation meeting](../reports/week-02/meeting-report.md)
- **Why:** after the prototype demo the customer confirmed that debugging in
  VS Code installed locally is the right priority: "I think this code is a
  very capable IDE. And so yeah, let's keep it as a debugging tool, debugging
  environment." The standalone-application-vs-browser question is left open,
  but having the files available locally and a local debugging experience is
  closed.

## DEC-005

Accept the minimum usable product candidate, pulling the multi-language and public-gallery stories out of it.

- **Status:** Active
- **Date:** 2026-10-14
- **Made by:** Customer
- **Source:** [the Week 2 validation meeting](../reports/week-02/meeting-report.md)
- **Why:** the customer advised making the story set "a bit less ambitious"
  so a minimal usable product is reached more easily, and said both the
  multi-language story and the public-gallery story can be pulled out of the
  candidate. The core task they defined is: go to the site, get an exercise,
  connect to the server, solve the bug, get the harness verdict, and finish.

## DEC-006

The harness must not be modifiable by the student, so the success state is fixed.

- **Status:** Active
- **Date:** 2026-10-14
- **Made by:** Customer (agrees with the team)
- **Source:** [the Week 2 validation meeting](../reports/week-02/meeting-report.md)
- **Why:** the team argued that if a student can change the check for success,
  they could just tell themselves they succeeded; the customer agreed: "the
  part that checks whether we have fixed the bug shouldn't be modifiable."

## DEC-007

Add a "choose an exercise you have not yet practiced" story; the public gallery exists so students can pick from a public pool and teachers can reuse exercises.

- **Status:** Active
- **Date:** 2026-10-14
- **Made by:** Customer
- **Source:** [the Week 2 validation meeting](../reports/week-02/meeting-report.md)
- **Why:** the customer reworded the "choose a problem kind" story into
  choosing an exercise not yet practiced ("as a user, I want to choose an
  exercise that I don't practice / what I already saw"), and justified the
  gallery by letting a student "choose exercises from a public pool... solve
  the same problems that my friend solves" and letting a teacher "select
  exercises prepared by someone else".

## DEC-008

Task authors may not modify the containers; the server controls what runs.

- **Status:** Active
- **Date:** 2026-10-14
- **Made by:** Customer
- **Source:** [the Week 2 validation meeting](../reports/week-02/meeting-report.md)
- **Why:** the customer agreed with the team that allowing task authors to
  supply their own container tools invites malicious software: "let's not give
  regular task creators options to modify the containers in any way so that we
  can control what's running on our server."
