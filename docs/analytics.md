
# Analytics Plan

## Purpose

Debugging Gym uses privacy-conscious product analytics to understand learner engagement, exercise usage, and verification outcomes.

The primary goal is to measure whether learners successfully complete debugging exercises, rather than simply counting application visits or generated exercises.

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

## North Star Metric

The North Star Metric is **Weekly Active Learners Completing an Exercise**.

It measures the number of unique learners who successfully complete at least one debugging exercise within a rolling seven-day period.

This metric was selected because:

- It measures meaningful learner activity rather than passive application visits.
- It reflects successful completion of the product's core task.
- It can be calculated from the `exercise_completed` event.
- It supports monitoring learner engagement over time.
- It does not require collecting personally identifying information.

### North Star Metric Criteria

The selected metric:

1. Reflects value delivered to learners.
2. Is directly connected to the product's core functionality.
3. Can be measured using existing analytics events.
4. Can inform product and development decisions.
5. Is not inflated by repeated page visits or automated smoke tests.
6. Can be measured without collecting sensitive personal information.

## Focus Metric

The focus metric for the analytics dashboard is **Weekly Active Learners Completing an Exercise**.

Definition:

- Count distinct learner identifiers (`profileId`) that generate an `exercise_completed` event.
- Use a rolling seven-day reporting window.
- Include normal learner events from the primary VS Code extension (`source = extension`) and any supported web-client activity (`source = web`).
- Exclude `source = smoke` and `source = usability-test` from product metrics.
- Use the production OpenPanel project for production reporting.

The staging dashboard may use the same metric logic to validate instrumentation, but staging data must not be combined with production data.

## Counter-Metric

The counter-metric is **Exercise Verification Pass Rate**.

Definition:

- Numerator: number of `verification_run` events where `passed = true`.
- Denominator: total number of `verification_run` events.
- Calculation: successful verification runs divided by all verification runs, multiplied by 100.
- Include learner events with `source = extension` or `source IN (extension, web)`; exclude `smoke` and `usability-test` traffic from production reporting.

This metric acts as a quality guardrail. An increase in exercise completions should not come at the expense of exercise difficulty or verification quality.

A sudden increase in pass rate may indicate that exercises have become too easy, while a significant decrease may indicate unclear instructions, faulty exercises, or verification problems.

## Metric Tree

The metric tree connects learner activity to successful exercise completion.

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

**Total Application Opens** was considered but rejected as the North Star Metric.

Although `app_opened` events are useful for understanding visits and first-time usage, total application opens do not demonstrate that learners are completing exercises or receiving value from the application.

Repeated visits, refreshes, and automated tests could increase this number without improving the learner experience.

Application opens will therefore remain a supporting metric rather than the primary measure of product success.

## Event Schema

Every event includes a valid `source` property.

Allowed sources:

- `extension`: Normal learner activity initiated by the VS Code extension (primary client).
- `web`: Normal activity from the retained web client (secondary client).
- `usability-test`: Facilitated usability testing.
- `smoke`: Staging-only deployment smoke testing.

| Event | Required properties | Description |
| --- | --- | --- |
| `app_opened` | `first_visit`, `source` | Learner opens the web client or activates the VS Code extension. |
| `exercise_generated` | `exercise_id`, `generator`, `source` | An exercise is generated. |
| `exercise_started` | `exercise_id`, `source` | Learner opens/retrieves an exercise to solve it. |
| `verification_run` | `exercise_id`, `passed`, `source` | Learner submits a fix for verification. |
| `exercise_completed` | `exercise_id`, `source` | Learner successfully passes verification. |

The `source` property is required for every event and identifies the origin of the activity.

### Event Triggers

- `app_opened`: Recorded when a learner opens the web client or activates the VS Code extension. For the extension, record once per extension-host session, not on every sidebar refresh.
- `exercise_generated`: Recorded after the backend successfully generates and stores an exercise. Include the stored exercise identifier and generator.
- `exercise_started`: Recorded when the extension retrieves or opens an exercise for solving. Include the exercise identifier.
- `verification_run`: Recorded after each verification attempt finishes, including its pass/fail result.
- `exercise_completed`: Recorded only when verification succeeds. Include the exercise identifier.

The VS Code extension is the primary learner interface (DEC-014 and DEC-015); the web client is secondary. The extension must identify its requests as `source = extension`, and backend instrumentation must preserve that attribution.

A smoke test uses the existing `app_opened` event with `first_visit = true` and `source = smoke`. It must be sent to staging only. It is an operational pipeline check, not a learner visit, and must be excluded from every product metric. Do not introduce a separate smoke event name.

## Logical Metric Query Definitions

The following definitions describe the intended query logic independently of OpenPanel's exact query-builder syntax.

| Metric | Event | Calculation | Filters |
| --- | --- | --- | --- |
| Weekly active learners completing an exercise | `exercise_completed` | Distinct learner identifiers over seven days | `source IN (extension, web)`; exclude `smoke`, `usability-test` |
| First visits | `app_opened` | Count events where `first_visit = true` | `source IN (extension, web)`; exclude `smoke`, `usability-test` |
| Exercises generated | `exercise_generated` | Count events | `source IN (extension, web)` |
| Exercises started | `exercise_started` | Count events | `source IN (extension, web)` |
| Verification attempts | `verification_run` | Count events | `source IN (extension, web)` |
| Verification pass rate | `verification_run` | Passed attempts / all attempts × 100 | `source IN (extension, web)` |
| Successful completions | `exercise_completed` | Count events | `source = web` |

All production queries must use the production project, include normal extension activity (and web activity only while that client remains supported), and exclude smoke and usability-test traffic.

The saved OpenPanel query configurations and screenshots are deployment evidence and must be captured separately for staging and production.

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

Production learner metrics must include normal extension activity (`source = extension`) and exclude `smoke` and `usability-test` events. Web activity may be included as secondary-client traffic.

## Environment Separation

Staging and production must have separate OpenPanel projects or equivalent isolated scopes.

Each deployment must use its own credentials.

- Staging events must be sent only to the staging project.
- Production events must be sent only to the production project.
- Smoke-test events must be sent only to staging.
- Production dashboard queries must exclude smoke and usability-test traffic.
- Credentials must be stored in deployment environment configuration and must never be committed to the repository.

## Evidence and Deployment

The team reports that the university-hosted OpenPanel service is deployed and event delivery is operational. The VS Code extension is the primary learner client; the web client is secondary. Deployment status does not by itself prove that the required events, filters, and dashboards have been verified. The following evidence must be captured from the live staging and production projects:

- Staging and production project configuration.
- Confirmation that each environment uses separate credentials.
- A staging-only `app_opened` event with `source = smoke` visible in the staging event explorer.
- Confirmation that the smoke event is excluded from every product metric chart/query.
- An extension-originated learner journey visible in staging: exercise generated, exercise opened, verification run, and successful completion, with `source = extension`.
- Staging and production dashboard screenshots.
- Links to the dashboards and corresponding metric definitions.

Required screenshot locations:

- `reports/week-06/images/analytics-staging.png` — staging dashboard and focus metric.
- `reports/week-06/images/analytics-production.png` — production dashboard and the same focus metric.
- `reports/week-06/images/analytics-staging-smoke.png` — staging event explorer showing the smoke event and the metric view proving it is excluded.

For each dashboard image, show the environment/project identity, focus metric, rolling seven-day window, and query/filter configuration where available. The smoke image must show `app_opened`, `source = smoke`, and `first_visit = true`, plus the metric view excluding smoke traffic. Redact credentials, tokens, private dashboard URLs, and learner identifiers.
