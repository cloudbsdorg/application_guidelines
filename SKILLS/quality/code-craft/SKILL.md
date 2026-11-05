---
name: code-craft
description: >-
  Apply the enduring lessons of the Gang of Four "Design Patterns" and Knuth's
  "The Art of Computer Programming" to code you write, refactor, or review,
  including the technique map (problem shape -> technique -> target bound) and
  the Time/Space complexity header. Use at the start of any non-trivial code
  change, before writing a loop, lookup or data-structure choice, again as a
  checklist before finishing, and in every code review. Not for one-line
  edits or config tweaks.
keywords:
  - design pattern
  - GoF
  - Knuth
  - TAOCP
  - complexity
  - invariant
  - data structure
  - algorithm
  - technique map
  - leetcode
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

## Technique map - recognise the shape, reach for the technique

"Know the complexity" is not enough on its own: you also need to know what to
reach for. Most loops that are slow in production are a known problem shape
solved by hand. Find the shape below before writing the loop. If the
technique's target bound beats what you were about to write, use the
technique or say in a comment why not.

The map works the same in every language. Language traps for each row are in
[language-idioms](../language-idioms/SKILL.md).

| Problem shape | Technique | Target | Systems example |
|---|---|---|---|
| Look up by a small dense key (opcode, encoding, MSR, errno) | Direct-index table after a range check | O(1) | MSR or VMCS field number minus a base, then index |
| Look up by a sparse key, many times | Hash map; or a sorted array plus binary search when keys change rarely | hash O(1) average (O(n) worst); sorted O(log n) | Device path to owning VM |
| "Is x in this set?" inside a loop (naive: O(n·m)) | Build the set once, outside the loop | O(n+m) average | Conflict check between two specs |
| Set of small integers (CPUs, IRQ vectors, pages) | Bitmap; `ffs`/`fls`/ctz/clz for first and last | O(words) | Highest pending interrupt vector |
| Highest or lowest priority, changing | Binary heap | O(log n) per op | Timer or expiry queue |
| Top k of n | Size-k heap (streaming); quickselect (all data in memory) | heap O(n log k); quickselect O(n) average | Largest consumers of a resource |
| Fixed-capacity FIFO | Ring buffer, power-of-two size, `& (N-1)` | O(1) | Event queue, log buffer |
| O(1) get and put with eviction | Hash map plus doubly linked list (LRU) | O(1) per op | Cache of parsed configs or shadow roots |
| Contiguous subarray or window with a constraint | Sliding window, two pointers | O(n) | Rate limit over the last N seconds |
| Sum or count over any range, static data | Prefix sums | O(1) per query | Bytes per time bucket |
| Range query plus point update | Fenwick (BIT) or segment tree | O(log n) | Allocation counts per region |
| Next greater or smaller element; window maximum | Monotonic stack or deque | O(n) | Peak load in a sliding window |
| Overlapping intervals, merge, free gaps | Sort by start, then sweep | O(n log n) | Guest physical memory ranges |
| Connectivity, grouping, "same component?" | Union-find (path compression plus rank) | O(α(n)) amortized per op | Hosts linked by shared storage |
| Dependency order; cycle detection | Topological sort (Kahn) | O(V+E) | Build, service-start or migration order |
| Shortest path | Unweighted: BFS. Weights 0 or 1: 0-1 BFS (deque). Non-negative weights: Dijkstra (heap) | BFS and 0-1 BFS O(V+E); Dijkstra O(E log V) | Hop count across a network |
| Monotone predicate over a numeric answer | Binary search on the answer | O(log range × check) | Smallest buffer that never overflows |
| Find a pattern in a stream or text | KMP or Z-function | O(n+m) worst case | Marker search in a console log |
| Many patterns, or substring equality checks | Rabin-Karp rolling hash; verify every hit or use two hashes | O(n+m) expected, O(n·m) worst | Duplicate-block detection |
| Prefix lookups over many strings | Trie | O(key length) | Command or path-prefix routing |
| Choose among subsets of ≤ ~20 items | Bitmask DP | O(2^n · n) | Small assignment or packing search |
| Overlapping subproblems | DP: state, transition, order, base case first | O(states × transitions) | Edit distance, diff, alignment |
| Retry after failure | Exponential backoff with jitter, capped | O(1) per retry | Reconnect, restart loop |
| Wait for a state change | Condition variable, channel or event, not sleep-polling | O(1) per wake-up, no CPU while waiting | "Wait until the VM is gone" |
| One-time initialisation | Static table, init at load, or a once-primitive | O(1) on the hot path | Layout tables built before first use |

Every bound in the Target column is worst case unless it says *average* or
*expected*.

Rules that go with the map:

- **Define n.** A bound means nothing until you say what n counts (fields,
  vCPUs, requests, bytes). Say the realistic size too: an O(n²) pass over 128
  constant entries is fine, but the same pass on every VM exit is not.
- **The hot path decides.** If something runs once at init, prefer the
  clearest code. If it runs per packet, per exit, per request or per frame,
  take the better technique, then measure it (see above).
- **Keep the naive version as the oracle.** When you replace a simple
  algorithm with a faster one, the simple one becomes the reference in the
  test. See [oracle-and-property-tests](../../testing/oracle-and-property-tests/SKILL.md).

## Complexity header - required where it matters

A function needs a header if it loops over input, chooses a data structure, or
sits on a hot path. Put the header directly above it, in the language's own
comment syntax:

```
// Time:  O(n log n), n = number of ranges. (measured: test_merge_growth)
// Space: O(n) for the sorted copy.
```

- Python and shell use `#`. Assembly uses whatever comment syntax the assembler
  takes (`;`, `#`, `//` or `@`). In Java and TypeScript, put the lines in the
  doc comment.
- Define every variable. Add a qualifier where it applies: *amortized*, *per
  operation*, *average* or *worst case*, *expected* for randomized code.
- **Name the rejected alternative.** Before you commit to an algorithm, write
  down the obvious one with its bound, then the one you chose with its bound.
  - In shipped code: only the chosen algorithm, plus at most one comment line
    naming what you rejected and why, for example
    `// Not a heap: k <= 4, linear scan wins.`
  - The full comparison goes in the commit message or a design note.
  - The slow version may live on only in the test tree, as the oracle.

  This one habit stops the most common review finding, "this is quadratic and
  did not need to be".
- **A header is a claim, so give it evidence.** For a hot path, a growth-ratio
  check (oracle-and-property-tests, "Complexity as a check") backs the
  header.
  - When a ratio has been measured, end the header with
    `(measured: <test name>)`.
  - When none has, end it with `(not measured)`.
  - A header with neither marker is incomplete, so a guessed bound never
    looks like a measured one.
- Review flags a missing or wrong header, as it flags a missing test. No hook
  enforces this, because no tool can check it the same way across every
  language.

## Checklist before finishing any non-trivial change or review

1. Every axis of change I expect is isolated behind a seam, and I named it.
2. No object mutates state it does not own; dependencies point at interfaces.
3. No duplicated enum or type branching that a Strategy, State, or
   polymorphism would remove.
4. Each non-trivial operation's complexity is known and appropriate; no
   needless rescans or per-render recomputation. Every function that loops
   over input, chooses a data structure, or sits on a hot path carries a
   Time/Space header, and I checked its shape against the technique map.
   - Where a faster algorithm replaced a simple one, the simple one is kept
     as the test oracle, and the oracle test has been observed failing on a
     seeded bug (oracle-and-property-tests, "Red first, for real").
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
- [oracle-and-property-tests](../../testing/oracle-and-property-tests/SKILL.md) - how to prove a faster algorithm still gives the right answer
- [language-idioms](../language-idioms/SKILL.md) - the per-language traps for each technique

## Sources

The technique taxonomy follows the categories of the problem catalogue
[kamyu104/LeetCode-Solutions](https://github.com/kamyu104/LeetCode-Solutions)
(MIT). Its Time/Space header on every solution is the model for the header
above. Further reading:
- [cp-algorithms.com](https://cp-algorithms.com/) (CC-BY-SA)
- the [AtCoder Library](https://github.com/atcoder/ac-library) (CC0)
- [TheAlgorithms](https://github.com/TheAlgorithms) (MIT; its C repository is GPL-3)
- Sean Anderson's [Bit Twiddling Hacks](https://graphics.stanford.edu/~seander/bithacks.html) (public domain)
- Henry S. Warren, *Hacker's Delight*

**Licence rule:** code from an MIT or CC0 source may be adapted, but only with
attribution and only where the target file's licence allows it. Treat GPL,
CC-BY-SA and unlicensed sources as reading only, and never paste their code.
Our code is BSD 3-Clause (rule 27).
