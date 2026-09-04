---
name: process-model-synchronization
description: Synchronization primitives — mutex types, condition variables, semaphores, read-write locks, spinlocks, anti-patterns.
---

# Process Model Analyzer — Synchronization

## 4. Synchronization

### 4.1 Mutex

```markdown
## Pthread Mutex

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// Lock
pthread_mutex_lock(&mutex);
// Critical section
pthread_mutex_unlock(&mutex);

// Try lock (non-blocking)
if (pthread_mutex_trylock(&mutex) == 0) {
    // Got lock
    pthread_mutex_unlock(&mutex);
} else {
    // Already locked
}
```

## Mutex Types

| Type | Linux | FreeBSD | macOS | Description |
|------|-------|---------|-------|-------------|
| NORMAL | yes | yes | yes | Deadlock if re-locked |
| RECURSIVE | yes | yes | yes | Allows recursive lock |
| ERRORCHECK | yes | yes | yes | Returns error on deadlock |
| DEFAULT | yes | yes | yes | Implementation-defined |

### 4.2 Condition Variables

```markdown
## Condition Variable Pattern

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int ready = 0;

// Waiter
pthread_mutex_lock(&mutex);
while (!ready) {
    pthread_cond_wait(&cond, &mutex);  // Atomically unlocks mutex
}
// Now mutex is locked and ready == true
pthread_mutex_unlock(&mutex);

// Signaler
pthread_mutex_lock(&mutex);
ready = 1;
pthread_cond_signal(&cond);   // Wake one waiter
// or
pthread_cond_broadcast(&cond);  // Wake all waiters
pthread_mutex_unlock(&mutex);
```

## Condition Variable Anti-Patterns

```c
// WRONG: Signal without mutex
pthread_cond_signal(&cond);  // Outside mutex - TOCTOU race

// WRONG: Checking condition outside loop
pthread_mutex_lock(&mutex);
if (!ready) {  // Check outside wait
    pthread_cond_wait(&cond, &mutex);
}
pthread_mutex_unlock(&mutex);

// RIGHT: Always check in loop
while (!ready) {
    pthread_cond_wait(&cond, &mutex);
}
```

### 4.3 Other Synchronization Primitives

```markdown
## Semaphore

| Type | Description | Use Case |
|------|-------------|----------|
| Binary | Like mutex but can be across processes | Process sync |
| Counting | Counts resources | Producer/consumer |

```c
sem_t sem;
sem_init(&sem, 0, 1);  // Initial value = 1

sem_wait(&sem);  // Decrement, block if <= 0
// Critical section
sem_post(&sem);  // Increment, wake waiters
```

## Read-Write Lock

```c
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// Read lock (multiple readers)
pthread_rwlock_rdlock(&rwlock);
// Read shared data
pthread_rwlock_unlock(&rwlock);

// Write lock (exclusive)
pthread_rwlock_wrlock(&rwlock);
// Write exclusive data
pthread_rwlock_unlock(&rwlock);
```

## Spinlock

```c
// Atomic spinlock
volatile int lock = 0;

while (__sync_lock_test_and_set(&lock, 1)) {
    // Spin until we get the lock
    while (lock) {
        __asm__ __volatile__("pause");  // x86 hint
    }
}
// Critical section
__sync_lock_release(&lock, 0);
```
