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

The fixed, non-modifiable test that runs a learner's source and reports pass or fail on whether the planted defect is gone.

**Defined by:** [`FR-003`](functional-requirements/fr/FR-003.md).

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
