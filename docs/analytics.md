
# Analytics Plan

## Purpose

Debugging Gym uses privacy-conscious product analytics to understand how learners and teachers use the system and whether they find it useful.

The focus metric is user satisfaction across learners and teachers, measured through surveys. Product telemetry remains useful for diagnosing exercise usage and verification outcomes, but it is supporting evidence rather than a substitute for satisfaction data.

Analytics must not interfere with exercise generation, debugging, or verification.

## Analytics Provider

The application uses OpenPanel for event collection.

Configuration is provided through environment variables:

- `OPENPANEL_API_URL`: OpenPanel tracking endpoint.
- `OPENPANEL_CLIENT_ID`: OpenPanel client ID.
- `OPENPANEL_CLIENT_SECRET`: OpenPanel client secret.
- `COOKIE_SECURE`: Set to `true` when running behind HTTPS.

Analytics delivery is disabled when OpenPanel credentials are missing.

Staging and production must use separate OpenPanel projects and credentials to prevent test activity from contaminating production metrics.

## Focus Metric

The focus metric is **User Satisfaction Across Learners And Teachers**.

It measures whether both learner and teacher users find the system useful and usable, using survey responses. This was selected at the Week 6 customer review ([DEC-029](decisions.md#dec-029)) because weekly learner activity may fall to zero when a course ends, even if the product remains useful.

The customer asked the team to define the survey instrument and the numerical success threshold after usability testing. The example of four out of five respondents being satisfied was illustrative, not an agreed target. The exact questions, scale, aggregation method, sample size, and threshold therefore remain open. There is no satisfaction value yet.

### Supporting Usage Metric

**Weekly Active Learners Completing an Exercise** remains a supporting usage metric, not the focus metric.

Definition:

- Count distinct learner identifiers (`profileId`) that generate an `exercise_completed` event.
- Use a rolling seven-day reporting window.
- Include only events with `source = web`.
- Exclude events with `source = smoke` and `source = usability-test`.
- Use the production OpenPanel project for production reporting.

This metric provides context about exercise usage and completion while satisfaction is measured separately through surveys. Staging data must not be combined with production data.

## Counter-Metric

The counter-metric is **Exercise Verification Pass Rate**.

Definition:

- Numerator: number of `verification_run` events where `passed = true`.
- Denominator: total number of `verification_run` events.
- Calculation: successful verification runs divided by all verification runs, multiplied by 100.
- Include only events with `source = web` for production reporting.

This metric acts as a quality guardrail. An increase in exercise completions should not come at the expense of exercise difficulty or verification quality.

A sudden increase in pass rate may indicate that exercises have become too easy, while a significant decrease may indicate unclear instructions, faulty exercises, or verification problems.

## Supporting Usage Metric Tree

The supporting usage metric tree connects learner activity to successful exercise completion. It does not replace the survey-based focus metric.

```text
Weekly Active Learners Completing an Exercise
|
+-- Active Learners
|   |
|   +-- First Visits
|   +-- Returning Learners
|
+-- Exercise Engagement
|   |
|   +-- Exercises Generated
|   +-- Exercises Started
|
+-- Verification Activity
    |
    +-- Verification Attempts
    +-- Successful Verification Runs
    +-- Exercise Completions
```

Supporting measures include:

- Unique active learners.
- First visits and returning learners.
- Exercises generated.
- Exercises started.
- Verification attempts.
- Successful verification runs.
- Exercise completion count.
- Verification pass rate.
- Exercise usage by kind.
- Exercise generator distribution.

## Rejected Vanity Metric

**Total Application Opens** was considered but rejected as the focus metric.

Although `app_opened` events are useful for understanding visits and first-time usage, total application opens do not demonstrate that learners are completing exercises or receiving value from the application.

Repeated visits, refreshes, and automated tests could increase this number without improving the learner experience.

Application opens will therefore remain a supporting metric rather than the primary measure of product success.

## The Events

Every event name follows `object_action` in snake case. Every event carries a required `source` field with one of the values `web`, `usability-test`, or `smoke`. All events are emitted by the `webapp` container in staging and production.

The OpenPanel envelope also carries the randomly generated opaque learner identifier as `profileId`; it is not a field in the event's `properties` object and is not derived from personal information.

| Event | Fires when | Fields | Collected at |
| --- | --- | --- | --- |
| `app_opened` | A learner requests the application's root page with an HTTP GET. | `first_visit` (boolean, required); `source` (enum `web` / `usability-test` / `smoke`, required). | `webapp`, staging and production |
| `exercise_generated` | Exercise generation succeeds and the generated exercise has been saved to server storage. | `exercise_id` (string, required); `generator` (string, required); `source` (enum, required). | `webapp`, staging and production |
| `exercise_started` | A stored exercise is retrieved or its VS Code launch configuration is requested. | `exercise_id` (string, required); `source` (enum, required). | `webapp`, staging and production |
| `verification_run` | A local or stored-exercise verification request finishes. | `exercise_id` (string, required; `local` for the local-harness endpoint); `passed` (boolean, required); `source` (enum, required). | `webapp`, staging and production |
| `exercise_completed` | Official verification of a stored exercise succeeds. | `exercise_id` (string, required); `source` (enum, required). | `webapp`, staging and production |

The implementation's event names, required properties, and source validation are defined in `app/telemetry.py`; the event calls are made by `app/main.py`. Every production metric excludes `source=smoke` and `source=usability-test`, and reads only `source=web` traffic. Test traffic must be sent to staging, never to the production OpenPanel project.

## Logical Metric Query Definitions

The following definitions describe the intended query logic independently of OpenPanel's exact query-builder syntax.

| Metric | Event | Calculation | Filters |
| --- | --- | --- | --- |
| Weekly active learners completing an exercise | `exercise_completed` | Distinct learner identifiers over seven days | `source = web` |
| First visits | `app_opened` | Count events where `first_visit = true` | `source = web` |
| Exercises generated | `exercise_generated` | Count events | `source = web` |
| Exercises started | `exercise_started` | Count events | `source = web` |
| Verification attempts | `verification_run` | Count events | `source = web` |
| Verification pass rate | `verification_run` | Passed attempts / all attempts × 100 | `source = web` |
| Successful completions | `exercise_completed` | Count events | `source = web` |

All production queries must use the production project and exclude smoke and usability-test traffic.

The staging and production OpenPanel dashboards have since been deployed and captured. Their sanitized screenshots are linked from the [Week 6 report](../reports/week-06/README.md#dashboard-evidence). The screenshots show event-derived usage metrics; they do not provide a value for the survey-based satisfaction focus metric.

## Learner Identification

Each learner receives a randomly generated opaque identifier using UUID4.

The identifier is stored in the `dg_learner_id` cookie:

- HTTP-only.
- SameSite=Lax.
- One-year expiry.
- Secure flag configurable through `COOKIE_SECURE`.

The identifier is reused across visits and is not derived from names, email addresses, or other personal information.

## Privacy Requirements

Analytics events must not contain:

- Learner source code.
- Exercise solution contents.
- Passwords, API keys, or authentication tokens.
- Names, email addresses, or other direct personal identifiers.

Only event metadata required for product analysis should be collected.

## Reliability

Analytics is best-effort.

- Missing credentials disable event delivery.
- Network and HTTP delivery failures must not interrupt application functionality.
- Invalid event names, required properties, or sources must be rejected by schema validation.
- Analytics failures must not prevent exercise generation, launching, or verification.

## Dashboard Metrics

### Staging Dashboard

The staging dashboard should support validation of event instrumentation and deployment smoke tests.

Suggested metrics:

- Events received by event name.
- Exercise generation count.
- Verification attempts and pass rate.
- Events grouped by source.
- Weekly active learners completing an exercise.

A staging smoke event must be visible in the staging event list to confirm that event delivery works.

Smoke-test events must be excluded from all learner engagement, completion, and product metric queries.

### Production Dashboard

The production dashboard should provide an overview of actual learner activity.

Suggested metrics:

- Weekly active learners completing an exercise.
- Unique learners.
- First visits.
- Exercises generated.
- Exercises started.
- Verification attempts.
- Successful exercise completions.
- Verification pass rate.
- Exercise usage by kind.
- Exercise generator distribution.

Production learner metrics must exclude `smoke` and `usability-test` events.

## Environment Separation

Staging and production must have separate OpenPanel projects or equivalent isolated scopes.

Each deployment must use its own credentials.

- Staging events must be sent only to the staging project.
- Production events must be sent only to the production project.
- Smoke-test events must be sent only to staging.
- Production dashboard queries must exclude smoke and usability-test traffic.
- Credentials must be stored in deployment environment configuration and must never be committed to the repository.

## Evidence and Deployment

The analytics instrumentation and both OpenPanel environment dashboards are deployed. Staging and production use separate projects/scopes and distinct credentials; real credentials and dashboard addresses remain private-only. The dashboard captures are included in the [Week 6 report](../reports/week-06/README.md#dashboard-evidence):

- `reports/week-06/images/analytics-staging.jpg`
- `reports/week-06/images/analytics-production.jpg`

The production dashboard includes the supporting **Weekly Active Learners Completing an Exercise** metric, computed from distinct learner identifiers with `exercise_completed` events over a rolling seven-day window and filtered to `source = web`. The customer-selected satisfaction focus metric still has no value because the survey instrument, sample, aggregation method, and success threshold have not yet been finalized or run. Dashboard activity must not be presented as a satisfaction result.
