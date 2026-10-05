# Lab 3: Synchronization

## Overview

In this lab, you will implement synchronization for a hypothetical half-duplex communication bus in Pintos.

Each task represents a data transfer between the processor and another component, such as an accelerator. Tasks may send or receive data, but the bus can operate in only one direction at a time. The bus also has limited capacity and supports two task-priority levels.

Before starting:

1. Complete Lab 2. Your `timer_sleep()` implementation must not use busy waiting.
2. Read [narrow_bridge_problem.pdf](./narrow_bridge_problem.pdf). The accompanying [PowerPoint](./narrow_bridge_problem.pptx) covers the same synchronization concepts.
3. Complete the **Lab 3 - Warm-up** quiz on Canvas.
4. Read this document completely.
5. Replace the three Pintos files described below before implementing the lab.

Follow the common environment and connection instructions on the main Canvas page.

## Update the Pintos Files

The files under [`replacements`](./replacements) provide the Lab 3 template and test. Copy them into the Pintos tree used for Lab 2.

From the repository root, run:

```sh
cp lab_3/replacements/devices/batch-scheduler.c \
   lab_2/pintos/src/devices/batch-scheduler.c

cp lab_3/replacements/tests/threads/batch-scheduler.c \
   lab_2/pintos/src/tests/threads/batch-scheduler.c

cp lab_3/replacements/tests/threads/batch-scheduler.ck \
   lab_2/pintos/src/tests/threads/batch-scheduler.ck
```

These commands replace the existing `batch-scheduler` template and test files in the Lab 2 Pintos tree.

## Bus Specification

The bus has the following properties:

- **Tasks:** Each task represents one data transfer over the bus.
- **Direction:** A task either sends or receives data. Because the bus is half-duplex, all tasks using it simultaneously must have the same direction.
- **Capacity:** The bus has three slots. At most three tasks may use it simultaneously.
- **Priority:** Each task is either normal or priority. A normal task must not acquire a slot while any priority task is waiting.
- **Unfair scheduling:** You do not need to guarantee fairness or freedom from starvation. In particular, you may continue scheduling priority tasks in the current direction even when priority tasks are waiting in the opposite direction.

Your implementation must therefore maintain all of the following invariants:

1. No more than three tasks use the bus at the same time.
2. All tasks currently using the bus have the same direction.
3. A normal task does not acquire the bus while a priority task is waiting.

## Functions to Implement

Implement the functions marked with `TODO` in:

```text
lab_2/pintos/src/devices/batch-scheduler.c
```

The relevant functions are:

- `init_bus()`: Initialize the locks, condition variables, counters, and other shared state used by your implementation.
- `get_slot()`: Wait until the task may safely acquire a bus slot, then update the shared state.
- `release_slot()`: Release the task's slot, update the shared state, and wake any tasks that may now proceed.

The supplied `batch_scheduler()` function creates tasks with different directions and priorities. Do not modify it.

You should not need to modify or add any other files for this exercise.

## Example

Consider:

```c
batch_scheduler(4, 1, 1, 0);
```

The arguments create:

- four priority send tasks;
- one priority receive task; and
- one normal send task.

The priority send tasks must be served before the normal send task. Although the normal task has the current bus direction, it must not acquire a slot while the priority receive task is waiting. After the priority send tasks finish, the bus changes direction and serves the priority receive task. The normal send task is served last.

Do not schedule the normal send task merely to keep all bus slots occupied while a priority receive task is waiting.

## Implementation Guidance

- Use locks and condition variables. Semaphores are not required.
- Protect every shared counter and scheduling decision with the appropriate lock.
- Check waiting conditions in a loop after waking from a condition variable.
- Track task priorities yourself. A task's priority is separate from the Pintos thread priority used by the operating-system scheduler.
- Think carefully about which class of waiting tasks should be signalled when a slot is released or the bus becomes empty.
- Fairness is not required, but the three invariants in the bus specification must always hold.

## Testing

Run the Pintos tests from `lab_2/pintos/src/threads`:

```sh
cd lab_2/pintos/src/threads
make clean && make check
```

A correct Lab 2 implementation should continue to pass the `alarm-*` tests. Your Lab 3 implementation must also pass `batch-scheduler`.

The supplied test calls:

```c
batch_scheduler(3, 4, 3, 3);
```

It compares the messages printed by the tasks with the expected output in:

```text
pintos/src/tests/threads/batch-scheduler.ck
```

To inspect the generated output directly, run the following command from `pintos/src/threads`:

```sh
cat build/tests/threads/batch-scheduler.output
```

You may modify the test locally to explore additional combinations of directions and priorities. Restore the supplied test before using it as the basis for your final validation.

## Submission and Report

Submit the following through **Lab 3 Submission** on Canvas:

1. your completed `batch_scheduler.c`; and
2. a report of at least 700 words.

The report must explain how your implementation ensures:

- that no more than three tasks use the bus simultaneously;
- that all simultaneous tasks travel in the same direction; and
- that priority tasks take precedence over normal tasks.

The scheduling policy is intentionally unfair. Your report must also answer:

- What makes your implementation unfair? Give an example.
- Could the design be modified to provide fairness? What would need to change?

## Asking Questions

Follow the common instructions for asking lab questions on the main Canvas page.
