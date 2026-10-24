# AI usage — Week 03

## Tools

GitHub Copilot, used through the repository's coding agent while writing the
Week 3 deliverables.

## What we used them for

- Drafting the plan documents: the threshold of success, the project plan, and
  the risk register.
- Writing the Definition of Done and the contributing guide.
- Building the minimum usable product slice: the FastAPI application, the
  exercise generator, the harness runner, the front end, and the tests.

## What we did with the output

We reviewed and edited the drafted documents before committing them, and we
checked that each identifier and link resolved.

The product code was verified by running it: the exercise generator was run
against every problem kind, the harness verdict was confirmed to flip from
fail to pass when the planted defect is fixed, the HTTP endpoints were exercised
with a running server, and the test suite passes (`python -m pytest tests/ -q`).

## What was not used

No AI output was used as a customer finding or as evidence of the product
working. The customer-meeting report and any transcript reflect what was
actually said and shown, and were written from the meeting rather than
generated. No generated text was submitted unchecked.
