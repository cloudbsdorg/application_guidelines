---
name: language-idioms
description: >-
  Per-language traps that turn a correct algorithm into a wrong or slow program,
  for C, Java, Python, TypeScript, Go, and x86-64 / arm64 assembly. Use while
  implementing anything from the code-craft technique map in a specific language
  (binary search, heaps, hashing, bit manipulation, sorting, recursion, ring
  buffers), when porting an algorithm between languages, and when reviewing
  such code.
keywords:
  - C integer overflow
  - Java PriorityQueue comparator
  - Python heapq deque
  - TypeScript sort comparator
  - Go slices maps
  - x86-64 arm64 assembly
  - language idioms
  - porting an algorithm
---

# Language idioms for algorithms

The same algorithm can fail differently in each language. Check the traps for
your language before using a technique from the
[code-craft technique map](../code-craft/SKILL.md). Each trap below is also an
edge case your [oracle test](../../testing/oracle-and-property-tests/SKILL.md)
should cover.

## Every language

- Compute a midpoint as `lo + (hi - lo) / 2`, not `(lo + hi) / 2`. That is
  safe only while `hi - lo` fits the type, which holds for array indices. For
  arbitrary signed values (`lo = INT_MIN`, `hi = INT_MAX`), take the
  difference in unsigned or wider arithmetic. In C:
  `lo + (int)(((unsigned)hi - (unsigned)lo) / 2)`. In Java, `(lo + hi) >>> 1` is
  correct for non-negative `int` indices. The sum may wrap negative, but the
  unsigned shift reads it back as the true value halved. For signed ranges,
  use `long` arithmetic.
- Choose a half-open `[lo, hi)` or a closed `[lo, hi]` interval and say which.
  Most binary-search bugs come from mixing the two.
- A comparator must be consistent: return a negative, zero or positive number.
  Never compute it as `a - b` on integers, which can overflow.
- Recursion depth grows with the input. Convert deep DFS and recursive descent
  over untrusted input to an explicit stack.
- Hash maps are O(1) **on average**. If an attacker controls the keys, use a
  keyed or randomised hash, or a balanced tree.

## C

- **Signed overflow is undefined behaviour,** and the compiler may delete
  your overflow check. Use `__builtin_add_overflow` and its relatives, or do the
  check in unsigned arithmetic.
- **`size_t` going down:** `for (size_t i = n - 1; i >= 0; i--)` never ends.
  Write `for (size_t i = n; i-- > 0; )`.
- **Bit scans:**
  - `ffs`, `fls` and `flsll` (FreeBSD libc and kernel) are 1-based and return 0
    when no bit is set.
  - `__builtin_ctz` and `__builtin_clz` are undefined at 0, so guard them.
  - Shifting by the type's width or more is undefined: `1u << 32` is UB on a
    32-bit `unsigned`. Use `1ULL << k` with `k < 64`.
- **Ring buffers:** make the size a power of two, enforce it with
  `_Static_assert((N & (N - 1)) == 0, ...)`, and use `& (N - 1)`. With an
  unsigned head and count, wraparound is then defined.
- **`qsort` and `bsearch`:** the comparator receives pointers to elements. Use
  `(a > b) - (a < b)` and never `a - b`. `qsort` is not stable, so add a
  tie-break field when order matters.
- **Kernel code:**
  - No floating point, and no unbounded recursion: the stack is a few pages.
  - Hot paths cannot sleep, so no `M_WAITOK` there.
  - Build tables at module load (SYSINIT) rather than behind a lazy flag that
    several CPUs may race on.
- **Statistics:** a high-water mark or a counter updated from several CPUs
  needs `atomic_*` or per-CPU counters (`counter(9)`).

## Java

- Comparing boxed `Integer` objects with `==` compares references. It works
  for -128..127 because of caching and fails above that. Use `.equals` or unbox.
- `PriorityQueue` is a min-heap. For a max-heap pass
  `Comparator.reverseOrder()`, not `(a, b) -> b - a`, which overflows.
- `int` arithmetic wraps silently. Use `Math.addExact` and `Math.multiplyExact`
  where overflow is a bug, and `long` for sums.
- `ArrayDeque` is the stack and queue. `Stack` is synchronized legacy, and
  `LinkedList` has poor locality.
- `s += x` on a local `String` in a simple loop is compiled to
  `StringBuilder` or `StringConcatFactory` calls, but each iteration still
  copies the whole string built so far, so the loop is O(n²) in total length.
  Use one `StringBuilder` outside the loop. `String.concat` in a loop and
  `s = prefix + s` are O(n²) too. `substring` copies.
- `HashMap` iteration order is unspecified. Use `LinkedHashMap` when order
  matters, which is also the quick way to build an LRU cache.

## Python

- `heapq` is a min-heap only. For a max-heap push negated keys, or
  `(-priority, seq, item)` tuples. The `seq` tie-break avoids comparing items.
- `list.pop(0)` and `insert(0, x)` are O(n). Use `collections.deque`.
- `x in list` is O(n). Build a `set` or `dict` once, outside the loop.
- The default recursion limit is about 1000. Use an explicit stack for deep
  DFS, and do not just raise the limit.
- `bisect` gives binary search over a sorted list. `sortedcontainers` is not
  in the standard library, so check the dependency is allowed first.
- Integers are unbounded, so overflow never happens. When porting to C or Java,
  that is exactly where the bugs appear, so add limit-value cases to the oracle.
- Mutable default arguments (`def f(seen=set())`) are shared between calls.
- A `str +=` loop can be quadratic; collect the parts and `''.join(parts)`.

## TypeScript / JavaScript

- **`Array.prototype.sort()` with no comparator sorts as strings:** `[10, 9,
  1].sort()` gives `[1, 10, 9]`. Always pass `(a, b) => a - b`, which is safe
  for finite numbers.
- `number` is a double, so integers are exact only up to 2⁵³ − 1
  (`Number.MAX_SAFE_INTEGER`). Use `bigint` for 64-bit IDs, counters and bit
  masks wider than 32 bits.
- Bitwise operators truncate to signed 32 bits: `1 << 31` is negative, and
  `>>>` is the unsigned shift.
- `Array.shift()` is O(n) in general. Use an index or a ring buffer for a
  queue.
- `Map` keeps insertion order and allows any key type. Plain objects coerce
  keys to strings, so `obj[1]` and `obj['1']` are the same entry.
- There is no built-in heap; write one or use a vetted dependency. Do not sort
  on every insert.

## Go

- `append` may or may not reallocate. Two slices taken from the same backing
  array can overwrite each other's elements.
- Iteration order over a map is randomised on purpose. Sort the keys when the
  output order matters.
- `container/heap` needs the five interface methods (`Len`, `Less`, `Swap`,
  `Push`, `Pop`) implemented on your own type.
- Integer overflow wraps silently. `math/bits` provides `Add64`, `Mul64`,
  `LeadingZeros` and `TrailingZeros`.
- Do not sleep-poll a condition that is protected by a mutex. Use a channel or
  `sync.Cond`, and pass `context.Context` for cancellation.
- Retry with `time.Sleep(backoff)`, doubling up to a cap with jitter. Never
  retry in a hot loop.

## Assembly (x86-64 and arm64)

- **Calling convention:** know which registers are callee-saved and keep the
  stack aligned.
  - SysV x86-64: arguments in `rdi, rsi, rdx, rcx, r8, r9`; callee-saved
    `rbx, rbp, r12–r15`; 16-byte alignment at `call`.
  - AAPCS64: arguments in `x0–x7`; callee-saved `x19–x28`; `sp` 16-byte
    aligned.
- **Flags:**
  - x86: `cmp` sets CF for unsigned and SF/OF for signed. `jb`/`ja` are the
    unsigned jumps and `jl`/`jg` the signed ones, so choose by type.
  - arm64: `cmp` sets NZCV. `b.lo`/`b.hi` are unsigned and `b.lt`/`b.gt` are
    signed.
  - On arm64, a carry after subtraction means *no borrow*, the opposite of x86.
- **Bit scans:**
  - x86 `bsr`/`bsf` leave the destination undefined when the source is zero.
    `lzcnt`/`tzcnt` are defined there but need BMI or LZCNT support.
  - arm64 `clz` is defined at zero and returns 64. arm64 has no `ctz`; use
    `rbit` then `clz`.
- **Writing a 32-bit register zero-extends into the 64-bit register:** on x86
  `mov eax, …` clears the upper half of `rax`, and on arm64 `w0` clears the
  upper half of `x0`. That is often what you want, and occasionally a bug.
- **Memory ordering:** x86 is TSO, while arm64 is weakly ordered. Code that is
  correct on x86 without barriers may need `dmb`/`ldar`/`stlr` on arm64. Prefer
  the C11 atomics or the kernel's `atomic_*` over hand-written barriers.
- Keep a C reference for every assembly routine. It is both the specification
  and the oracle.

## Related

- [code-craft](../code-craft/SKILL.md) - the technique map these traps apply to
- [oracle-and-property-tests](../../testing/oracle-and-property-tests/SKILL.md) - turn each trap into a test case
- [secure-coding](../../security/secure-coding/SKILL.md) - bug classes from untrusted input (paths, commands, sizes, archives, secrets)
