---
name: process-model-threads
description: Threading models — pthread creation, thread attributes, thread pools, thread vs task parallelism patterns.
---

# Process Model Analyzer — Threading Models

## 3. Threading Models

### 3.1 Thread Creation

```markdown
## Pthreads

```c
#include <pthread.h>

void *worker(void *arg) {
    int *value = (int *)arg;
    // Do work
    return result;
}

pthread_t tid;
int arg = 42;
pthread_create(&tid, NULL, worker, &arg);
pthread_join(tid, NULL);  // Wait for thread
```

## Thread Attributes

```c
// Set thread stack size
pthread_attr_t attr;
pthread_attr_init(&attr);
pthread_attr_setstacksize(&attr, 2 * 1024 * 1024);  // 2MB

// Set detached state
pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

// Create with custom attributes
pthread_create(&tid, &attr, worker, &arg);
pthread_attr_destroy(&attr);
```

## Thread vs Task Parallelism

```markdown
| Approach | When to Use | Example |
|----------|-------------|---------|
| Thread per request | Blocking I/O, long-lived requests | Web servers |
| Thread pool | Bounded concurrency, resource control | Database connections |
| Worker threads | Work queue, task distribution | Build systems |
| Async/Event-driven | High concurrency, I/O-bound | Network servers |
| Process pool | CPU isolation, security | Plugin sandboxing |
```

### 3.2 Thread Pools

```markdown
## Thread Pool Pattern

```
┌─────────────────────────────────────────────────┐
│                 Thread Pool                      │
│                                                  │
│  Task Queue                                      │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │Task1│ │Task2│ │Task3│ │Task4│ │Task5│      │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘      │
│     │       │       │       │       │          │
│     ▼       ▼       ▼       ▼       ▼          │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │ Thr1│ │ Thr2│ │ Thr3│ │ Thr4│ │ Thr5│      │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘      │
└─────────────────────────────────────────────────┘
```

## Thread Pool Implementation

```c
// Thread pool structure
typedef struct {
    pthread_t *threads;
    int num_threads;
    TaskQueue *queue;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int shutdown;
} ThreadPool;

// Worker loop
void *worker(void *arg) {
    ThreadPool *pool = (ThreadPool *)arg;
    while (1) {
        pthread_mutex_lock(&pool->mutex);
        while (TAILQ_EMPTY(pool->queue) && !pool->shutdown) {
            pthread_cond_wait(&pool->cond, &pool->mutex);
        }
        if (pool->shutdown) {
            pthread_mutex_unlock(&pool->mutex);
            break;
        }
        Task *task = TAILQ_FIRST(pool->queue);
        TAILQ_REMOVE(pool->queue, task, next);
        pthread_mutex_unlock(&pool->mutex);
        task->fn(task->arg);
    }
    return NULL;
}
```
