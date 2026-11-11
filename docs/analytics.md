# Analytics Plan

## Purpose

Debugging Gym uses privacy-conscious product analytics to understand learner engagement, exercise usage, and verification outcomes. Analytics must not interfere with exercise generation, debugging, or verification.

## Analytics Provider

The application uses OpenPanel for event collection.

Configuration is provided through environment variables:

- `OPENPANEL_API_URL`: OpenPanel tracking endpoint.
- `OPENPANEL_CLIENT_ID`: OpenPanel client ID.
- `OPENPANEL_CLIENT_SECRET`: OpenPanel client secret.
- `COOKIE_SECURE`: Set to `true` when running behind HTTPS.

Analytics delivery is disabled when OpenPanel credentials are missing.

Staging and production must use separate OpenPanel projects and credentials to prevent test activity from contaminating production metrics.

## Event Schema

Every event includes a valid `source` property.

Allowed sources:

- `web`: Normal application usage.
- `usability-test`: Facilitated usability testing.
- `smoke`: Deployment smoke testing.

| Event | Required properties | Description |
|---|---|---|
| `app_opened` | `first_visit` | Learner opens the application. |
| `exercise_generated` | `exercise_id`, `kind`, `generator` | An exercise is generated. |
| `exercise_started` | `exercise_id`, `kind` | Learner requests the launch configuration. |
| `verification_run` | `exercise_id`, `passed` | Learner submits a fix for verification. |
| `exercise_completed` | `exercise_id`, `kind` | Learner successfully passes verification. |

## Learner Identification

Each learner receives a randomly generated opaque identifier using UUID4.

The identifier is stored in the `dg_learner_id` cookie:

- HTTP-only.
- SameSite=Lax.
- One-year expiry.
- Secure flag configurable through `COOKIE_SECURE`.

The application does not use names, email addresses, or other direct personal identifiers for analytics.

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

## Dashboard Metrics

### Staging Dashboard

Staging analytics should support validation of event instrumentation and deployment smoke tests.

Suggested metrics:

- Events received by event name.
- Exercise generation count.
- Verification attempts and pass rate.
- Events grouped by source.

Smoke-test events must be excluded from learner engagement and completion metrics.

### Production Dashboard

Production analytics should provide an overview of actual learner activity.

Suggested metrics:

- Unique learners.
- First visits.
- Exercises generated.
- Exercises started.
- Verification attempts.
- Successful exercise completions.
- Verification pass rate.
- Exercise usage by kind.
- Exercise generator distribution.

Production learner metrics must exclude `smoke` events.

## Environment Separation

Staging and production must have separate OpenPanel projects or equivalent isolated scopes.

Each deployment must use its own credentials. Dashboard queries must filter by environment and exclude smoke-test events where appropriate.

## Evidence and Deployment

Record the following when OpenPanel setup is completed:

- Staging and production project configuration.
- Dashboard screenshots.
- Verification that staging smoke events do not affect production metrics.
- Any outstanding deployment or credential limitations.

