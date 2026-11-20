
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

## The Value And The Metrics

### Supporting Usage Metric Tree

The tree makes the customer-selected focus metric explicit and separates its quality guardrail from the product-usage input. The lower-level inputs explain the weekly completion measure; they are not presented as survey responses or as a substitute for satisfaction.

```text
Focus: User Satisfaction Across Learners and Teachers
|
+-- L1 counter-metric: Exercise Verification Pass Rate
|
+-- L1 input metric: Weekly Active Learners Completing an Exercise
    |
    +-- L2 input: Active Learners
    +-- L2 input: Completed Exercises per Active Learner
```

### Focus Metric

**User Satisfaction Across Learners and Teachers**

- **Definition:** The share or level of learner and teacher respondents who report that Debugging Gym is useful and usable. The customer selected this outcome at the Week 6 review ([DEC-029](decisions.md#dec-029)); it expresses [VP-01](research/value-proposition.md#vp-01), targeted debugging practice rather than general coding activity.
- **Source:** Survey responses from learners and teachers collected during usability testing. The survey instrument has not yet been approved.
- **Query:** Not defined yet. The customer deferred the questions, response scale, aggregation method, sample size, and success threshold until usability testing. No satisfaction value is reported; the example of four out of five respondents being satisfied was illustrative, not an agreed target.

### Counter-Metric

**Exercise Verification Pass Rate**

- **Definition:** Successful official verification runs divided by all official verification runs, multiplied by 100. This is a guardrail: higher completion should not be achieved by making exercises trivial or weakening verification.
- **Source:** `verification_run` events with `passed` and `source=web`; exclude `smoke` and `usability-test` events from production.
- **Query:** `100 * count(verification_run where passed = true and source = 'web') / count(verification_run where source = 'web')`.

### L1 Input Metric

**Weekly Active Learners Completing an Exercise**

- **Definition:** Count of distinct opaque learner identifiers with at least one `exercise_completed` event in a rolling seven-day window.
- **Source:** `exercise_completed` events, grouped by the OpenPanel `profileId`; include only `source=web`.
- **Query:** `COUNT(DISTINCT profileId) WHERE event = 'exercise_completed' AND timestamp >= now() - 7d AND source = 'web'`.

### L2 Input Metric: Active Learners

- **Definition:** Count of distinct opaque learner identifiers with at least one `app_opened` event in the rolling seven-day window.
- **Source:** `app_opened` events grouped by `profileId`; include only `source=web`.
- **Query:** `COUNT(DISTINCT profileId) WHERE event = 'app_opened' AND timestamp >= now() - 7d AND source = 'web'`.

### L2 Input Metric: Completed Exercises per Active Learner

- **Definition:** Number of official exercise completions in the rolling seven-day window divided by the number of active learner identifiers in the same window.
- **Source:** `exercise_completed` and `app_opened` events grouped by `profileId`; include only `source=web`.
- **Query:** `COUNT(exercise_completed WHERE source = 'web' AND timestamp >= now() - 7d) / COUNT(DISTINCT profileId from app_opened WHERE source = 'web' AND timestamp >= now() - 7d)`.

### Why This Focus Metric

- **Expresses value:** It asks learners and teachers whether the product is useful and usable, rather than treating activity as value.
- **Represents vision and strategy:** It tests whether the targeted debugging practice in [VP-01](research/value-proposition.md#vp-01) delivers the value the product promises to its learner and teacher audiences.
- **Leading indicator:** Satisfaction after a practice session may indicate willingness to return and recommend the product; this relationship remains a hypothesis until usability data is collected.
- **Actionable:** Results can be reviewed separately for learners and teachers and used to prioritize problems in exercise quality, teacher workflows, onboarding, or verification.
- **Understandable:** The intended concept—whether learners and teachers find the product useful and usable—is plain-language and interpretable. The response scale remains undecided.
- **Measurable:** Not yet operational. The customer has deferred the survey instrument, scale, sample, aggregation method, and target until usability testing; consequently there is no numeric value or query yet.
- **Not a vanity metric:** It measures perceived product value, not raw visits, generated exercises, or other activity counts.

### Rejected Vanity Metric

**Total Application Opens** was considered but rejected as the focus metric. Although `app_opened` events help explain visits and first-time usage, repeated visits, refreshes, and automated tests could increase this number without improving the learner experience. Application opens remain a lower-level usage input, not the product's measure of success.

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
