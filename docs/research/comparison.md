# Comparison of the alternatives

**Problem space.** Software developers and programming-language learners want
targeted, hands-on practice that trains a specific debugging skill, but the
existing platforms offer general exercises rather than exercises for a
particular kind of debugging problem.

This table compares the three researched alternatives on the six properties we
fixed **before** evaluating anything. The column for Debugging Gym is what our
project intends to be; it is derived from the value proposition
([`value-proposition.md`](./value-proposition.md)) and the gap analysis
([`gap-analysis.md`](./gap-analysis.md)), not from an existing product.

Every cell traces back to an `ALT-nn` observation in
[`alternatives.md`](./alternatives.md) — we separate what we *observed* from
what we *concluded*.

| Property | ALT-01 CodinGame | ALT-02 LeetCode | ALT-03 Rustlings | Debugging Gym (intended) |
|----------|------------------|-----------------|------------------|--------------------------|
| **1. Debugging specificity** | Observed: puzzles are "write a program that passes"; no debugging category (ALT-01). *Conclusion:* teaches coding, not debugging. | Observed: no debugging mode; a failing submission shows a failed test but no debugging guidance (ALT-02). *Conclusion:* debugging is incidental, not taught. | Observed: exercises are broken files the user repairs; grouped by topic (ALT-03). *Conclusion:* the closest to a debugging exercise, but binary compile/test only. | Generates an existing program with a planted defect for a *named* problem category (e.g. null pointer, off-by-one, race condition) and coaches the skill of finding it. |
| **2. Exercise generation** | Observed: hand-curated fixed set, no way to request a category (ALT-01). *Conclusion:* no generation. | Observed: fixed catalogue, user picks from what exists (ALT-02). *Conclusion:* no generation. | Observed: hand-written fixed files (ALT-03). *Conclusion:* no generation. | LLM generates a fresh exercise on request for the chosen category. |
| **3. User's own environment** | Observed: browser editor only (ALT-01). *Conclusion:* not the user's IDE. | Observed: web editor by default; IDE plugins secondary (ALT-02). *Conclusion:* mostly not the user's IDE. | Observed: runs locally, user edits in own editor (ALT-03). *Conclusion:* fully in the user's environment. | User connects from VS Code and debugs with their own tooling (breakpoints, stack traces). |
| **4. Grading / feedback** | Observed: instant pass/fail + leaderboard in a game world (ALT-01). *Conclusion:* strong engagement feedback, but pass/fail on the program, not on debugging method. | Observed: hidden tests give objective pass/fail (ALT-02). *Conclusion:* good objective signal, no coaching on how to debug. | Observed: compile/test pass/fail with hints (ALT-03). *Conclusion:* binary result, no analysis of the debugging process. | Auto-checks whether the defect was found/fixed and can give the user a hint ladder; feedback is about the debugging process, not just the score. |
| **5. Target audience** | Observed: gamified challenges, broad developer audience (ALT-01). *Conclusion:* hobby/competitive developers. | Observed: developers preparing for coding interviews (ALT-02). *Conclusion:* interview-prep audience. | Observed: Rust learners following a track (ALT-03). *Conclusion:* Rust learners specifically. | Software developers and programming-language learners who want to train a specific debugging skill. |
| **6. Openness / cost** | Observed: free + paid tiers, closed source (ALT-01). *Conclusion:* not open, not self-hostable. | Observed: free + paid tiers, closed source (ALT-02). *Conclusion:* not open, not self-hostable. | Observed: MIT open source, runs locally (ALT-03). *Conclusion:* open and self-hostable. | Openly documented and deployable on a VPS; the exercise *generator* and *gallery* are the product, not a locked-in client. |

## Reading the table as a whole

- **No existing product combines the three things we want.** CodinGame and
  LeetCode have the audience and the feedback loop but not debugging
  specificity and not the user's environment. Rustlings has the environment
  and the "broken code" model but not generation, breadth, or a gallery.
- **The strongest existing pieces are in different products.** Engagement
  (CodinGame), topic-by-category practice + objective pass/fail (LeetCode),
  own-environment "fix the broken file" (Rustlings). No single alternative
  offers more than one of these together.
- **The columns differ most sharply on rows 1, 2, and 3** — debugging
  specificity, generation, and the user's own environment. Those three rows
  are where the alternatives are weakest together, which is where a gap can
  live (see [`gap-analysis.md`](./gap-analysis.md)).

*Conclusion:* the alternatives are strong *examples of one piece* of what we
want but none is a direct competitor, because none sells "generate a debugging
exercise for a chosen category and debug it in your own IDE". That absence is
either an opportunity (if someone needs it) or a warning (if nobody has built
it because it is hard or unneeded) — the gap analysis decides which.