
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
- Include learner events from the primary VS Code extension (`source = extension`) and any supported web-client activity (`source = web`).
- Exclude `source = smoke` and `source = usability-test` from product metrics.
- Use the production OpenPanel project for production reporting.

The staging dashboard may use the same metric logic to validate instrumentation, but staging data must not be combined with production data.

## Counter-Metric

The counter-metric is **Exercise Verification Pass Rate**.

Definition:

- Numerator: number of `verification_run` events where `passed = true`.
- Denominator: total number of `verification_run` events.
- Calculation: successful verification runs divided by all verification runs, multiplied by 100.
- Include learner events with `source = extension` or `source = web`; exclude `smoke` and `usability-test` traffic from production reporting.

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

- `web`: Normal application usage.
- `usability-test`: Facilitated usability testing.
- `extension`: Normal learner activity initiated by the VS Code extension.
- `smoke`: Deployment smoke testing.

| Event | Required properties | Description |
| --- | --- | --- |
| `app_opened` | `first_visit`, `source` | Learner opens the web application or activates the extension for a new/returning session. |
| `exercise_generated` | `exercise_id`, `kind`, `generator`, `source` | An exercise is generated. |
| `exercise_started` | `exercise_id`, `kind`, `source` | Learner requests the launch configuration. |
| `verification_run` | `exercise_id`, `passed`, `source` | Learner submits a fix for verification. |
| `exercise_completed` | `exercise_id`, `kind`, `source` | Learner successfully passes verification. |

The `source` property is required for every event and identifies the origin of the activity. The VS Code extension is the primary learner interface (DEC-014 and DEC-015); `web` remains a supported secondary client while it is retained.

### Event Triggers

- `app_opened`: Recorded when the learner opens the web client or activates the VS Code extension. For the extension, record activation once per extension host session, not on every sidebar refresh.
- `exercise_generated`: Recorded after the backend successfully generates and stores an exercise. Include the stored exercise's `id`, `kind`, and `generator`.
- `exercise_started`: Recorded when the extension retrieves/opens an exercise for solving. Include the exercise's `id` and `kind`.
- `verification_run`: Recorded after each verification attempt finishes, with the boolean `passed` result.
- `exercise_completed`: Recorded only when verification succeeds. Include the exercise's `id` and `kind`.

The VS Code extension calls the FastAPI backend; event attribution must therefore be propagated by the extension client (currently the `x-client-source: extension` request header) and preserved by backend instrumentation. Do not infer extension activity from a browser page view.

A smoke test uses the existing `app_opened` event with `first_visit = true` and `source = smoke`. It must be sent to staging only. It is an operational pipeline check, not a learner visit, and must be excluded from every product metric. Do not add a separate `smoke` event name.

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
| Successful completions | `exercise_completed` | Count events | `source IN (extension, web)` |

All production queries must use the production project and exclude smoke and usability-test traffic.

Exact saved OpenPanel query configurations and dashboard screenshots will be added after deployment in Sprint 7.

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

Production learner metrics must include normal extension activity (`source = extension`) and exclude `smoke` and `usability-test` events. Web activity may be included while the web client remains supported.

## Environment Separation

Staging and production must have separate OpenPanel projects or equivalent isolated scopes.

Each deployment must use its own credentials.

- Staging events must be sent only to the staging project.
- Production events must be sent only to the production project.
- Smoke-test events must be sent only to staging.
- Production dashboard queries must exclude smoke and usability-test traffic.
- Credentials must be stored in deployment environment configuration and must never be committed to the repository.

## Evidence and Deployment

The VS Code extension is the primary learner interface; the web application is a secondary client and the backend remains the shared event-collection service. The team reports that the university-hosted analytics service and event delivery are operational. Treat that as deployment status, not as a substitute for the verification evidence below. Do not describe dashboard work as complete until the saved charts have been checked in both isolated projects.

The following evidence must be recorded for the staging and production environments:

- Staging and production project configuration.
- Confirmation that each environment uses separate credentials.
- A staging-only `app_opened` event with `source = smoke` visible in the staging event list.
- Confirmation that the smoke event is absent from every product metric chart/query.
- A successful extension-generated exercise, exercise start, verification attempt, and successful completion visible in staging events with `source = extension` and the documented properties.
- Staging and production dashboard screenshots.
- Links to the dashboards and corresponding metric definitions.

Required screenshot locations:

- `reports/week-06/images/analytics-staging.png`
- `reports/week-06/images/analytics-production.png`

Capture the complete dashboard with its project/environment identity visible, the focus metric chart and its seven-day window visible, and the query/filter configuration visible where the provider UI permits. The staging screenshot must additionally show the staging event list containing the smoke event and a separate chart view demonstrating that smoke traffic is excluded. The production screenshot must show the same focus-metric chart in the production project and no smoke/test traffic. Crop or redact hostnames, private dashboard URLs, tokens, credentials, learner identifiers, and any other sensitive values.
