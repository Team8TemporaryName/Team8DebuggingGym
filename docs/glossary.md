# Glossary

The words this project uses in one way only.

## Exercise Flow

### Exercise

A self-contained unit of practice: a program with a planted defect, a problem kind, and a harness that reports whether the defect is gone.

**Defined by:** [`FR-002`](functional-requirements/fr/FR-002.md).

### Problem kind

A named category of debugging problem a learner trains, such as a null pointer, an off-by-one, or a race condition.

**Defined by:** [`FR-001`](functional-requirements/fr/FR-001.md).

### Harness

The learner-accessible test program included with an exercise, which can be run and edited locally, while separate server-side tests determine the official pass/fail verdict.

**Defined by:** [`FR-003`](functional-requirements/fr/FR-003.md), [`FR-009`](functional-requirements/fr/FR-009.md).

## Gallery

### Gallery

The public, instructor-curated list of problems a learner can choose to practice, separate from on-demand generation.

**Defined by:** [`FR-005`](functional-requirements/fr/FR-005.md).

### Instructor

The user who generates and verifies problems for the gallery; only instructors generate exercises, per [`DEC-010`](decisions.md#dec-010).

**Defined by:** [the product vision's boundary](product-vision.md#boundary).

## Debug Environment

### Debug runtime

The isolated container that runs a learner's exercise and harness and exposes a Debug Adapter Protocol server the learner's VS Code attaches to.

**Defined by:** [the container view](architecture/README.md#container-responsibilities).

### VS Code extension

The client that brings the choose, generate, verify, and task flow into the learner's own VS Code, calling the web app's API.

**Defined by:** [`FR-006`](functional-requirements/fr/FR-006.md).

## Product Analytics

### Focus metric

The one number the product's value is read from. It represents the outcome that the product exists to deliver, rather than activity for its own sake.

**Defined by:** [the analytics plan](analytics.md#focus-metric).

### Input metric

A measure of a user or system action that contributes to the focus metric and that the team can influence through product changes.

**Defined by:** [the analytics plan](analytics.md#supporting-usage-metric-tree).

### Counter-metric

A guardrail metric that reveals whether improving the focus metric is causing harm elsewhere. It guards the focus metric; it is not an input that feeds it.

**Defined by:** [the analytics plan](analytics.md#counter-metric).

### Metric tree

A nested map of the focus metric, its counter-metric, and the input metrics that contribute to it. The levels show the relationship between outcomes and the actions or measures beneath them.

**Defined by:** [the analytics plan](analytics.md#supporting-usage-metric-tree).
