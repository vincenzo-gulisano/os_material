# Narrow Bridge Problem

This document is a digital version of the handwritten notes in
[`narrow_bridge_problem.pdf`](narrow_bridge_problem.pdf). It first introduces
condition variables through the producer-consumer problem and then applies them
to the narrow-bridge problem.

## The Exercise

A two-way east-west road contains a narrow bridge with only one lane. An
eastbound or westbound car may cross the bridge only if there is no oncoming
car on it.

Traffic may cross the bridge in only one direction at a time. Furthermore, the
bridge collapses if more than three vehicles are on it simultaneously.

Each car is represented by one thread, which executes:

```text
OneVehicle(Direction direction)
{
    ArriveBridge(direction);
    CrossBridge(direction);
    ExitBridge(direction);
}
```

`direction` specifies the direction in which the vehicle crosses the bridge.

Implement `ArriveBridge()` and `ExitBridge()`.

- `ArriveBridge()` must not return until the car can cross safely in the given
  direction. It must prevent both head-on collisions and bridge collapse.
- `ExitBridge()` indicates that the caller has finished crossing. It must take
  the necessary steps to allow additional cars to cross.

```text
WEST                         NARROW BRIDGE                         EAST

[car -->]          +================================+      [<-- car] [<-- car]
                   |          [car -->]             |
                   +================================+
```

## Condition Variables, Part 1: Producer-Consumer with Semaphores

Consider a bounded buffer shared by producers and consumers.

```text
Producer                                                Consumer

wait("has space") <------------------------------- signal("has space")

lock buffer                                             lock buffer
deposit                                                 retrieve
unlock buffer                                           unlock buffer

signal("has items") ------------------------------> wait("has items")
```

Three semaphores are sufficient:

```text
binary semaphore mutex       = 1
general semaphore has_items  = 0
general semaphore has_space  = N
```

The producer and consumer can then be written as follows:

```text
Producer
{
    while (true)
    {
        produce();
        wait(has_space);
        wait(mutex);
        add();
        signal(mutex);
        signal(has_items);
    }
}
```

```text
Consumer
{
    while (true)
    {
        wait(has_items);
        wait(mutex);
        retrieve();
        signal(mutex);
        signal(has_space);
        consume();
    }
}
```

The correspondence between the operations is:

```text
Producer wait(has_space)   <---->   Consumer signal(has_space)
Producer signal(has_items) <---->   Consumer wait(has_items)
Producer signal(mutex)     <---->   Consumer wait(mutex)
Producer wait(mutex)       <---->   Consumer signal(mutex)
```

## Condition Variables, Part 2: Producer-Consumer with Locks

A lock is a token that can be held by at most one thread at a time.

- `acquire(lock)` obtains the lock if it is free and waits otherwise.
- `release(lock)` marks the lock as free.
- The thread calling `release(lock)` must own the lock.

### Attempt 1: Shared Counter without a Lock

Suppose the buffer is represented by:

```text
shared count     = 0
shared max_size  = N
```

The first attempt is:

```text
Producer
{
    while (true)
    {
        produce();

        while (count == max_size)
        {
        }

        add();
        count++;
    }
}
```

```text
Consumer
{
    while (true)
    {
        while (count == 0)
        {
        }

        get();
        count--;
        consume();
    }
}
```

This does not work. For example, let `N = 20`, `count = 19`, and let two
producers, `P1` and `P2`, execute concurrently:

```text
time --------------------------------------------------------------->

count = 19
      P1 checks count < max_size
                    P2 checks count < max_size
                              P1 adds an item
                                        P2 adds an item
                                                  count = 21
```

Both producers observe an available slot before either updates `count`, so the
buffer capacity can be exceeded.

### Attempt 2: Protect the Counter with a Lock

Add a shared lock `l`:

```text
shared count     = 0
shared max_size  = N
shared lock l
```

```text
Producer
{
    while (true)
    {
        produce();
        acquire(l);

        while (count == max_size)
        {
        }

        add();
        count++;
        release(l);
    }
}
```

```text
Consumer
{
    while (true)
    {
        acquire(l);

        while (count == 0)
        {
        }

        get();
        count--;
        release(l);
        consume();
    }
}
```

This also fails. If `count == 0` and a consumer acquires `l`, it waits forever
while still holding the lock. No producer can acquire the lock to add an item:

```text
Consumer C1: acquire(l) -- waits while count == 0 ------------------>
Producer P1:              blocked trying to acquire(l)
```

### Attempt 3: Release the Lock While Waiting

The next attempt releases and reacquires the lock while the condition is false:

```text
Producer
{
    while (true)
    {
        produce();
        acquire(l);

        while (count == max_size)
        {
            release(l);
            acquire(l);
        }

        add();
        count++;
        release(l);
    }
}
```

```text
Consumer
{
    while (true)
    {
        acquire(l);

        while (count == 0)
        {
            release(l);
            acquire(l);
        }

        get();
        count--;
        release(l);
        consume();
    }
}
```

This can work, but only through repeated polling:

```text
Producer                              Consumer

release(l) -------------------------> acquire(l)
acquire(l) <------------------------- release(l)
release(l) -------------------------> acquire(l)
    ... repeated until the condition changes ...
```

All producers and consumers repeatedly contend for the lock, including threads
that do not need to wake. A better mechanism should put a thread to sleep until
the condition it needs may have become true.

## Condition Variables

A condition variable is an object associated with a lock. A thread uses it to
wait until a condition may have become true.

`cond_wait(condition, lock)`:

1. releases `lock`;
2. puts the calling thread to sleep in the condition's waiting queue; and
3. reacquires `lock` before returning after the thread is awakened.

`cond_signal(condition, lock)` wakes one thread waiting on `condition`, if one
exists. The awakened thread reacquires `lock` before returning from
`cond_wait()`.

`cond_broadcast(condition, lock)` is similar to `cond_signal()`, except that it
wakes all threads waiting on `condition`.

The thread calling any of these operations must hold the associated lock.
Condition variables provide fine-grained control over which class of waiting
threads should be awakened.

```text
Semaphore waiting queue                 Condition-variable waiting queue

         wait                                    wait(cv, lock)
T1 -----------------> [ semaphore ]     T1 -----------------> [ condition ]
                            |                                       |
T2 <---------------- signal()           T2 <-------------- signal(cv, lock)

Any thread may signal the semaphore.     The signaler holds the associated
                                         lock, and a waiter reacquires it
                                         before continuing.
```

### Attempt 4: Producer-Consumer with Condition Variables

Use one lock and two condition variables:

```text
shared count              = 0
shared max_size           = N
shared lock l
condition has_space
condition has_items
```

```text
Producer
{
    while (true)
    {
        produce();
        acquire(l);

        while (count == max_size)
        {
            cond_wait(has_space, l);
        }

        add();
        count++;
        cond_signal(has_items, l);
        release(l);
    }
}
```

```text
Consumer
{
    while (true)
    {
        acquire(l);

        while (count == 0)
        {
            cond_wait(has_items, l);
        }

        get();
        count--;
        cond_signal(has_space, l);
        release(l);
        consume();
    }
}
```

The signaling relationships are:

```text
Producer cond_signal(has_items, l) ---> Consumer cond_wait(has_items, l)
Consumer cond_signal(has_space, l) ---> Producer cond_wait(has_space, l)
```

## Applying Condition Variables to the Narrow Bridge

The bridge imposes these constraints:

- At most three cars may be on the bridge: `0 <= cars <= 3`.
- All cars on the bridge must travel in the same direction.
- A car may enter an empty bridge.
- A car may enter a nonempty, non-full bridge only if it travels in the current
  bridge direction.

```text
Can a car enter?

Bridge empty
    |
    +-- yes ----------------------------------------------> enter
    |
    +-- no --> bridge full?
                  |
                  +-- yes -------------------------------> wait
                  |
                  +-- no --> same direction?
                                |
                                +-- yes -----------------> enter
                                |
                                +-- no ------------------> wait
```

Use the following shared state:

```text
shared integer cars             = 0
shared Direction bridge_dir     = 0
shared lock bridge
condition waiting_to_go[2]
shared integer waiting[2]       = {0, 0}
```

The handwritten pseudocode uses `waitingToGo[d]` both for the condition queue
and for the number of waiting cars. The version below separates those roles as
`waiting_to_go[d]` and `waiting[d]`.

### `ArriveBridge`

```text
ArriveBridge(Direction d)
{
    acquire(bridge);

    while (cars == 3 || (cars > 0 && bridge_dir != d))
    {
        waiting[d]++;
        cond_wait(waiting_to_go[d], bridge);
        waiting[d]--;
    }

    cars++;
    bridge_dir = d;
    release(bridge);
}
```

The car traverses the bridge only after `ArriveBridge()` returns:

```text
CrossBridge(d);
```

### `ExitBridge`

```text
ExitBridge(Direction d)
{
    acquire(bridge);
    cars--;

    if (waiting[d] > 0)
    {
        cond_signal(waiting_to_go[d], bridge);
    }
    else if (cars == 0)
    {
        cond_broadcast(waiting_to_go[1 - d], bridge);
    }

    release(bridge);
}
```

If another car traveling in the current direction is waiting, one such car is
awakened. Otherwise, when the bridge becomes empty, all cars waiting in the
opposite direction are awakened. Each awakened car rechecks the `while`
condition before entering.
