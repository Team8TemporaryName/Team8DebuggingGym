# Week 6 validation meeting script

## Context

The weekly meeting is SPRINT-06's Sprint Review. The team shows the deployed product with the analytics dashboards, the observability dashboards, the observability `QRT-01`'s result with its `SLI`, and each runtime `QRT`'s result at its level, then presents the threshold proposal.

## Agenda

1. Opening: permission questions (recording, transcript publication, personal data). (2 min)
2. Show the deployed product. (3 min)
3. Show the analytics staging and production dashboards. (3 min)
4. Show the observability staging and production dashboards. (3 min)
5. Show the observability `QRT-01` result: the failed request's log point, its `request_id`, route, and failure labels, the `SLI-01` P95 query result, and the dashboard screenshot. (4 min)
6. Present the threshold proposal and record the customer's decision as a `DEC-nnn`. (3 min)
7. Close: read back the decisions and action points. (1 min)

## Questions

- (open) Does the telemetry answer the questions you recognise about how the product is used and how it operates?
- (open) Does the diagnosability requirement hold in staging — can you find the failed request from its `request_id`?
- (closed) Should the threshold measure change, or stay as proposed?

## Roles

- **Interviewer:** Magel0n
- **Note taker:** Doosuur14
- **Observer:** Tedor49
- **Facilitator:** NikitaRUniverse

## Key improvements

This script keeps the meeting to the sprint-review essentials: the deployed product, the four dashboards, the observability test result, and the threshold decision, so the customer's verdict is settled in a short meeting rather than an hour.
The telemetry and threshold questions are the only open ones because they are the decisions this week's sprint must record; the product and dashboard demos are shown, not discussed at length.
