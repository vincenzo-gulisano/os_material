### Introduction

Follow the common lab environment and connection instructions on the main Canvas page.

1. Complete Lab 2: You need a `timer_sleep()` implementation that does not rely on busy waiting.
2. Read carefully the narrow_bridge_problem.pdf you find in the lab_3 folder.
3. Complete the "Lab 3 - Warm-up" quiz.
4. Read this page thoroughly, as it contains all the information needed to complete the lab successfully.
5. **Critical: Update your Pintos files:**
   - **A.** Copy the file `lab_3/replacements/devices/batch-scheduler.c` from the folder lab_3/replacements and replace `lab_2/pintos/src/devices/batch-scheduler.c` in the lab_2 folder.
   - **B.** Copy the file `lab_3/replacements/tests/threads/batch-scheduler.c` and replace `lab_2/pintos/src/tests/threads/batch-scheduler.c` in the lab_2 folder.
   - **C.** Copy the file `lab_3/replacements/tests/threads/batch-scheduler.ck` and replace `lab_2/pintos/src/tests/threads/batch-scheduler.ck` in the lab_2 folder.

### Key Concepts and Specifications

In this lab, you will tackle thread synchronization challenges centered on a hypothetical half-duplex communication bus.

The bus has limited slots and supports tasks at two priority levels:

- **Tasks:** Each task represents data communication over the bus. You may imagine that this communication occurs between the processor and an accelerator, such as a GPU.
- **Direction:** A task can either send or receive data. Its direction specifies whether data is being sent from or received by the processor. The bus operates in half-duplex mode, meaning that it can only send or receive data at any given moment. This is referred to as the bus direction.
- **Limited capacity:** The bus has only three slots, allowing a maximum of three tasks to use it simultaneously.
- **Priority levels:** Tasks have one of two priority levels: normal or priority. Priority tasks take precedence; normal tasks shall not acquire a slot if priority tasks are waiting.
- **Unfair scheduling:** Bus direction shall change under two conditions:
  - If a higher-priority task is waiting in the opposite direction.
  - If no tasks remain in the current direction but tasks are waiting in the opposite direction.

### Functions to Implement

All the functions you need to implement are located in `pintos/src/devices/batch-scheduler.c`:

- `init_bus()`: Initialize global or static variables, such as condition variables, locks, and counters.
- `get_slot()`: Acquire a slot on the bus. According to the previous section, a task may have to wait.
- `release_slot()`: Release the slot once the data transfer is complete and take any necessary actions, such as notifying waiting tasks, according to the rules in the previous section.

Look for the `TODO` comments in the file to identify where to insert your implementation.

You should not need to modify or add any other files for this lab exercise.

The provided code template also includes a `batch_scheduler()` function that creates a batch of tasks with different directions and priorities. You should not modify this function.

### Example

Consider the call `batch_scheduler(4, 1, 1, 0)`, which creates the following tasks:

- 4 priority send tasks
- 1 priority receive task
- 1 normal send task

The correct sequence in which the tasks acquire bus slots shall be:

1. First, the 4 priority sending tasks secure slots, as they are the initial tasks created by `batch_scheduler()`.
2. The priority receiving task is next.
3. Finally, the normal sending task gets its turn.

Resist the urge to schedule the normal sending task just to maximize bus occupancy while a priority receiving task is waiting!

### Tips

- You need only condition variables and locks as thread synchronization primitives.
- Do not confuse a task's priority with a thread's priority.
- The former is managed by your implementation, while the latter is handled by the operating system.
- Focus only on managing task priorities for this exercise.

### Testing

To validate your work, ensure that all tests pass by running the following commands (from the lab_2 folder):

```sh
cd pintos/src/threads
make clean && make check
```

If your Lab 2 code was implemented correctly, you should also pass the final test, located at `pintos/src/tests/threads/batch-scheduler.c`.

The test performs a simple call to `batch_scheduler(3, 4, 3, 3)`.

The test passes if the output messages printed during its execution match the expected messages in `pintos/src/tests/threads/batch-scheduler.ck`.

Feel free to modify the test if you wish to validate your implementation under different scenarios.

To examine the output messages generated during the test execution, use the following command:

```sh
# Make sure you are in pintos/src/threads
cat build/tests/threads/batch-scheduler.output
```

### Asking Questions

Follow the common instructions for asking lab questions on the main Canvas page.

### Submission and Report Structure

Submit `batch_scheduler.c` and your report here: Lab 3 Submission.

In your report (at least 700 words), address the following questions:

How does your implementation ensure each of the following?

- A maximum of three tasks are on the bus at any given time.
- Only tasks traveling in the same direction use the bus.
- Priority tasks take precedence over normal tasks.

The lab specifies that the scheduling of tasks is unfair:

- What makes your implementation unfair? Give an example that demonstrates this.
- Could your design be easily modified to make it fair? What changes would be necessary?
