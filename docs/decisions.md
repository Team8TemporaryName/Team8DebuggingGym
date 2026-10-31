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

- **Status:** reversed by [DEC-017](#dec-017)
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

## DEC-009

Build the minimum usable product on a Python stack: a FastAPI backend, a minimal web front end, and debugpy-based debug environments, with LLM-based exercise generation.

- **Status:** Active
- **Date:** 2026-10-15
- **Made by:** Team
- **Source:** the stack decision for Week 3
- **Why:** the Week 2 prototype already proved the riskiest part — attaching a
  learner's own VS Code to a hosted runtime over the Debug Adapter Protocol —
  in Python with `debugpy`. Reusing that proven path and keeping one language
  across the backend, the debug environments, and the generator lets the team
  reach a working slice fastest. FastAPI is a small, modern backend; a minimal
  HTML/JS front end is enough to choose a problem kind and get an exercise;
  exercise generation goes through the LLM provider's API with a deterministic
  local fallback for the constrained budget ([RISK-02](risks.md#risk-02)).

## DEC-010

Only instructors generate exercises; students access instructor-curated problems from a public gallery, and do not generate their own.

- **Status:** Active
- **Date:** 2026-10-24
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md)
- **Why:** the customer re-scoped the MUP around the course use case: a teacher
  produces a problem, verifies it, and students practice what is provided. For
  the current version "we should let only instructors to generate problems for
  a given topic... students should not have this opportunity; they should only
  be able to access curated problems." A student's request for a generated
  exercise is not stored or executed on the platform — they only receive the
  code and harness.

## DEC-011

The public gallery, with instructor-curated and instructor-moderated problems, is a core part of the product.

- **Status:** Active
- **Date:** 2026-10-24
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md)
- **Why:** the customer said a public gallery "is a very important part of the
  system": it lets an instructor author problems, pass them to students, and
  reuse them. Only problems verified by instructors can be stored, to keep the
  gallery free from malicious problems; a student's generated exercise is not
  stored or executed on the platform.

## DEC-012

The product moves toward a VS Code extension in future releases, with pre-installed relevant plugins.

- **Status:** Active
- **Date:** 2026-10-24
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md)
- **Why:** the customer concluded that using VS Code "makes it necessary to have
  an extension for VS Code where the user can interact with the system: run some
  tests, click buttons, see the instructions for a problem right inside VS Code."
  The team agreed the product should move toward VS Code in future releases; the
  extension was not included in the MUP because the testing functionality could
  not be finished in time.

## DEC-013

No AI agent inside the learner's environment for now; keep the experience static with clear instructions and read-only code parts.

- **Status:** Active
- **Date:** 2026-10-24
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md)
- **Why:** the customer is not sure an in-environment agent benefits education,
  so "let's keep things more or less static and not introduce an agent." Focus
  first on clear instructions for the learner (probably inside the VS Code
  extension) and on limiting where the learner should expect to find the bug,
  for example by making some parts of the code read-only. An agent, if any,
  comes last.

## DEC-014

Multi-file exercises are required; the web-app's editable code field is deprecated in favour of the VS Code extension.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:** [the Week 4 validation meeting](../reports/week-04/meeting-report.md)
- **Why:** the customer wants multi-file setups because they let students train
  realistic conditions where they jump between files to find bugs: "I think we
  do need multi-file setups." Because VS Code is already a full editor, the
  customer sees no need for the editable code field on the site: "I don't think
  we need this code preview on the site, honestly. Like, we already have an
  editor, like VS Code."

## DEC-015

Prioritize the VS Code extension over the web application for the learner experience.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:** [the Week 4 validation meeting](../reports/week-04/meeting-report.md)
- **Why:** the customer confirmed the product should "move away from a web
  application and focus our efforts on the extension", because the web-app
  editor cannot handle large or multi-file exercises and lacks language-server
  tooling. The extension is the primary surface going forward.

## DEC-016

Learner-submitted code runs on the server inside sandboxed containers with capped resources.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:** [the Week 4 validation meeting](../reports/week-04/meeting-report.md)
- **Why:** the customer and team agreed that remote evaluation is the only way
  to prevent a student from falsely claiming success, and that student-submitted
  code may crash the server unless sandboxed. The decision is to run code in
  separate containers, cap the resources a program may use, and limit networking
  inside containers.

## DEC-017

The harness is editable by the learner, with an option to restore the server version.

- **Status:** Active
- **Reverses:** [DEC-006](#dec-006)
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:** [the Week 4 validation meeting](../reports/week-04/meeting-report.md)
- **Why:** the customer agreed the harness is a learning tool and the learner
  should be able to edit it, while also being able to revert it to the server
  version. The harness as an ordinary, editable file lets the learner run it
  from the terminal, and hidden tests on the server decide the true verdict.

## DEC-018

Each exercise opens as its own folder/workspace with automatic versioning, so learners manage and back up their work.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:** [the Week 4 validation meeting](../reports/week-04/meeting-report.md)
- **Why:** the customer wants a per-exercise folder so a learner can manage and
  delete exercises and see their progress, and wants versioning (a git
  repository per exercise) so learners do not lose progress and can back up to
  GitHub. This also lets teachers review a student's work as proof of work.

## DEC-019

The recommended VS Code settings and language extensions are generated dynamically per exercise.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:** [the Week 4 validation meeting](../reports/week-04/meeting-report.md)
- **Why:** the customer asked for a ready-to-use `settings.json` and recommended
  extensions generated dynamically depending on the languages an exercise
  covers, rather than packaging every language extension up front. Language
  extensions should be recommended (not force-installed) as the learner takes
  exercises in a given language.
