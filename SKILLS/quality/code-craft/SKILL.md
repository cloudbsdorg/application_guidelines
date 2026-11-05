---
name: code-craft
description: >-
  Apply the enduring lessons of the Gang of Four "Design Patterns" and Knuth's
  "The Art of Computer Programming" to code you write, refactor, or review. Use
  at the start of any non-trivial code change and again as a checklist before
  finishing, and in every code review. Not for one-line edits or config tweaks.
keywords:
  - design pattern
  - GoF
  - Knuth
  - TAOCP
  - complexity
  - invariant
  - refactor
  - code review
---

# Code craft - GoF patterns and TAOCP rigor

A standing discipline, not a one-off task. The goal is code that is well
structured (Gang of Four) and algorithmically sound (Knuth). Name the pattern or
principle you are applying in the comment, the commit message, or the review
note, so the reasoning is visible to the next reader. Rigor over cleverness;
clarity over brevity.

## Gang of Four - structure and responsibility

- **Program to an interface, not an implementation. Favor composition over
  inheritance.** These two maxims outrank any individual pattern.
- **Recognise the problem first, then apply the pattern that fits - and name
  it.** Keep the catalog in view:
  - *Creational*: Factory Method, Abstract Factory, Builder, Prototype,
    Singleton (sparingly - a Singleton is global state).
  - *Structural*: Adapter, Bridge, Composite, Decorator, Facade, Flyweight,
    Proxy.
  - *Behavioral*: Chain of Responsibility, Command, Interpreter, Iterator,
    Mediator, Memento, Observer, State, Strategy, Template Method, Visitor.
- **Calls that are usually right:** Strategy for a family of interchangeable
  behaviors; Template Method or Factory for repeated near-identical
  construction; Observer, a reactive stream, or signals instead of ad-hoc
  polling and manual notification; Adapter to turn an external shape (JSON, a
  provider API) into a clean internal model; State to replace status-flag soup;
  Facade to hide a messy subsystem.
- **Smells to fix:** a class or function reaching outside its own scope to
  mutate shared, global, or DOM state; duplicated branching on the same
  type or status enum; a switch that grows with every new case; deep
  inheritance where composition fits; a "manager" or "utils" god object.
- **Do not over-pattern.** The simplest thing that is open to the change you
  actually expect. A pattern earns its place by removing real duplication or
  isolating a real axis of change, never for its own sake.

## Knuth - algorithms and correctness

- **Analyse before writing.** State the input size, the data structure chosen,
  and the time and space complexity of each non-trivial operation. Prefer the
  structure that makes the operation natural; one well-chosen structure beats
  repeated O(n*m) rescans.
- **Correctness first, and be able to argue it.** For every loop and recursion,
  know the invariant and why it terminates. Handle the boundaries explicitly:
  empty input, one element, missing or null fields, overflow, invalid dates,
  off-by-one.
- **Measure, do not guess.** Premature optimization is the root of all evil -
  write it clearly, then optimise the part a measurement shows is hot. Equally,
  do not ship a gratuitously worse algorithm than the obvious one.
- **Prefer a single pass and the right structure** over recomputing the same
  derivation on every event or render. Cache deliberately, invalidate
  correctly. Use a stable sort when order within a key matters.
- **Say what you mean.** Small sharp functions, honest names, comments that
  state the invariant or the *why* rather than the obvious *what*. Determinism
  and reproducibility. No undefined behaviour, no silent truncation, no
  swallowed errors.

## Checklist before finishing any non-trivial change or review

1. Every axis of change I expect is isolated behind a seam, and I named it.
2. No object mutates state it does not own; dependencies point at interfaces.
3. No duplicated enum or type branching that a Strategy, State, or
   polymorphism would remove.
4. Each non-trivial operation's complexity is known and appropriate; no
   needless rescans or per-render recomputation.
5. Every loop and recursion has a clear invariant and terminates; boundary
   cases are handled.
6. Input from outside - JSON, an API, a user - is adapted to a typed internal
   model and validated at the boundary.
7. It reads clearly, the names are honest, and the *why* is documented.
8. It is not over-engineered: the simplest design that satisfies 1-7.

In a code review, cite each finding by `file:line`, name the pattern or
principle it relates to, and give a concrete refactor. Rank findings
should-fix / would-improve / nice-to-have.

## Related

- [review](../../workflow/review/SKILL.md) - the review workflow this discipline feeds
- [code-quality-analyzer](../../analysis/code-quality-analyzer/SKILL.md) - finding the duplication in the first place
- `Unit-Testing/UNITTESTS.md` - the red-green evidence requirement that goes with it
