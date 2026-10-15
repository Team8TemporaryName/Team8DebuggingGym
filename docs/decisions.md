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
