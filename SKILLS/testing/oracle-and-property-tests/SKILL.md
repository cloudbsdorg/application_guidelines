---
name: oracle-and-property-tests
description: >-
  Prove that an algorithm gives the right answer on inputs nobody thought to
  write down. Use whenever you replace a simple algorithm with a faster one,
  write a parser, encoder, lookup table, page-table walker, scheduler, or any
  function with a large input space, and in the red step of red-green when one
  example-based test cannot cover the space. Covers brute-force oracles,
  differential tests, property-based tests, fuzzing, and complexity checks, in
  C, Java, Python, TypeScript, Go, and assembly.
keywords:
  - oracle test
  - differential test
  - property-based test
  - fuzzing
  - reference implementation
  - brute force
  - red-green
  - Hypothesis
  - fast-check
  - jqwik
---

# Oracle and property tests

Red-green TDD (rule 15, `Unit-Testing/UNITTESTS.md`) says to write the failing
test first. This skill covers what that test should be when an example or two
cannot cover the input space, which is usually the case for any algorithm worth
optimising.

An example test checks the cases you thought of. An oracle test checks the
cases you did not think of.

## 1. The oracle: keep the slow version

When a faster algorithm replaces a simple one, keep the simple one as the
**reference** in the test tree. The reference stays obvious: a linear scan, a
nested loop, an exhaustive search or a bit-by-bit loop. It should be correct by
inspection, and its speed does not matter.

```
for each input in (every edge case) + (N seeded random inputs):
    assert fast(input) == reference(input)
```

- **Edge cases first, chosen by hand:** empty, one element, all equal, sorted,
  reverse-sorted, maximum size, values at type limits (0, -1, `INT_MAX`,
  `UINT64_MAX`), and every invalid input class.
- **Exhaust small spaces.** If the domain has 256 values, or 2¹⁶, test them
  all. Exhaustive beats random whenever it fits in about a second.
- **Seed the generator and print the seed** on failure, so that every failure
  can be replayed. A random test with an unseeded generator is not evidence.
- **Make the reference independent.** If it shares a helper or a table with
  the code under test, a bug in that helper will pass both.

## 2. Red first, for real

An oracle test counts only once it has failed for the right reason. A red
means a failed **assertion** that prints the expected and actual values. A
compile error, a missing symbol or a crash in setup is not a red.

1. **New code.** Before the real implementation exists, run the test against
   a stub that compiles and returns a wrong answer. The assertion must fail.
2. **Replacing a working algorithm.** Here the old code is the oracle, so it
   passes from the start, and step 1 cannot happen. Step 3 is the red that
   counts.
3. **Seed a bug** into the fast path, for example an off-by-one, a wrong
   table entry or a dropped boundary check, and confirm that the oracle test
   catches it. If it does not, the generator does not reach that part of the
   input space; fix the generator.
   - Where practical, keep the mutant in the tree behind a **compile-time**
     switch that only the test build sets, such as `-DSEED_BUG` in the test
     target or a Go build tag. Never use a runtime environment variable,
     which would put the mutant in shipped code. Make the release build
     refuse the flag outright, for example
     `#if defined(SEED_BUG) && !defined(TEST_BUILD)` then `#error`. In Go,
     put the mutant in a non-test file guarded by `//go:build seedbug`, with
     the real code guarded by `//go:build !seedbug`. Only the mutant job
     passes `-tags seedbug`. A mutant inside a `_test.go` file cannot change
     the code under test.
   - Count a run as `mutant killed` only when the mutant was really compiled
     in, for example because it prints or exports a sentinel the job checks,
     **and** the oracle assertion failed. A build error, a missing flag, a
     timeout or a crash in setup counts as `not run`.
   - CI builds the mutant in a separate job that **expects** the oracle test
     to fail. The job reports one of three results: `mutant killed` (the
     proof held), `mutant survived` (a defect), or `not run`. Only
     `mutant killed` passes the job, so "never ran" cannot pass as "held".
     The normal test job stays green. That way the
     proof is re-run, not just remembered.
   - Otherwise, inject the bug in a scratch edit, capture the failing output
     as evidence (rule 23), and revert it.
   - A seeded bug is never committed to the production path.

A test that has failed on a seeded bug is a test that can fail.

## 3. Properties, when there is no oracle

Sometimes nothing is simple enough to be a reference. Test laws that must hold
for every input instead:

| Property | Example |
|---|---|
| Round trip | `decode(encode(x)) == x`; write a field, read it back |
| Invariant preserved | the heap property after every push and pop; ranges stay sorted and non-overlapping after a merge |
| Idempotence | `normalize(normalize(x)) == normalize(x)` |
| Equivalent paths | the batched update equals N single updates |
| Bounds | the result lies in range; output length ≤ input length |
| Metamorphic | permuting the input does not change a sum; scaling input by k scales output by k |

## 4. Fuzz anything that parses outside input

Rule 19 says to validate every input. A fuzzer is how you find out whether you
did. Fuzz parsers, decoders, protocol handlers and anything that reads a file
or a socket. Run it in CI with a time budget, and add every crash it finds to
the corpus as a regression test.

## 5. Complexity as a check

To keep an O(n) function from regressing to O(n²), measure it at n and at 4n
and assert on the **ratio**, never on wall time. Derive the threshold from the
multiplier: at 4n, linear gives about 4, n log n about 4.5 and quadratic about
16. A threshold chosen for 4n is wrong for 2n, where quadratic gives only
about 4.

```
t1 = time(f, n); t2 = time(f, 4n)
assert t2 / t1 < 8        # linear allows about 4; quadratic gives about 16
```

- Take the median of several runs, and choose an n large enough that timer
  noise does not matter.
- Run it as its own CI job on a quiet machine (a scheduled benchmark job), not
  in the ordinary unit-test job, but run it. Make "not measured" a distinct
  result from PASS, so that a check that never ran cannot look like one that
  passed.
- A wall-time threshold such as "must finish in 50 ms" fails on a busy CI host
  and passes on a fast laptop. It proves nothing.

## 6. Per language

| Language | Oracle / differential | Property-based | Fuzz |
|---|---|---|---|
| C | the reference as a `static` function in the test file; a seeded xorshift or splitmix64 generator; ATF (`atf-c`) or the project's test module | the hand-rolled generator plus the property loop | libFuzzer (`clang -fsanitize=fuzzer,address`) or AFL++ |
| C kernel code | an in-kernel test module, or compile the pure function into a userland ATF test against the same header | as for C | userland harness over the pure function |
| Java | JUnit 5 with a parameterized source | jqwik (`@Property`) | Jazzer |
| Python | pytest with a parametrized table | Hypothesis (`@given`) | Atheris |
| TypeScript | Vitest or Jest with a table | fast-check (`fc.assert(fc.property(...))`) | fast-check, or jsfuzz |
| Go | table tests | `testing/quick`, or rapid | native `go test -fuzz` |
| Assembly | drive the routine from a C harness and compare with a C reference over the same inputs | as for C | libFuzzer over the C wrapper |

- **Assembly:** the C reference is the specification. Test every input class
  that touches a flag, a carry or a sign extension, in particular 0, all ones,
  the high bit set, and the high bit clear.
- **Sanitizers and resource limits:** AddressSanitizer reserves terabytes of
  virtual address space at start-up, so it aborts under `RLIMIT_AS`
  (`ulimit -v`) on both FreeBSD and Linux. `RLIMIT_DATA` is no fix either. On
  Linux since 4.7 it aborts ASan too. On FreeBSD ASan runs under it, but there
  `RLIMIT_DATA` counts only the break segment, not mmap, so it caps neither
  the plain build's malloc (jemalloc uses mmap) nor ASan's allocator. Measured
  2026-11-05 on FreeBSD 16-CURRENT and Linux 7.0. Test memory limits on the
  plain build with `RLIMIT_AS`, and run the sanitized build under the time
  limit only. A memory cap on a sanitized build needs `rctl` on FreeBSD
  (boot tunable `kern.racct.enable=1`) or a cgroup on Linux. A sanitizer
  report is its own failure class; never count it as a wrong answer. A
  sanitizer that could not start is a third outcome ("unavailable"), not a
  clean run.
- **Kernel code:** factor the pure part (table lookup, bit math, the walker
  over a page-table image) out of the part that touches hardware. Only then can
  it be oracle-tested in userland.

## Checklist

- [ ] The slow reference exists in the test tree and is obviously correct.
- [ ] Hand-picked edge cases are tested, plus an exhaustive or seeded-random
      sweep, and the seed is printed on failure.
- [ ] The test failed with an assertion (not a build error) on a stub for new
      code, and on a seeded bug in every case. The mutant is kept behind a
      test-only switch that CI runs, or its failing output is captured as
      evidence.
- [ ] Where there is no oracle, properties (round trip, invariant,
      idempotence, metamorphic) are tested.
- [ ] Every parser of outside input has a fuzz target, and crashes are kept as
      regressions.
- [ ] Any complexity check asserts a growth ratio, not a wall time.

## Related

- `Unit-Testing/UNITTESTS.md` - red-green and evidence, the rule this serves
- [code-craft](../../quality/code-craft/SKILL.md) - the technique map; "keep the naive version as the oracle"
- [language-idioms](../../quality/language-idioms/SKILL.md) - traps the edge cases should target
