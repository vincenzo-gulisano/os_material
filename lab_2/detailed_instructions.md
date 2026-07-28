# Detailed Lab 2 Instructions: Alarm Clock in Pintos

> Operating Systems Course
>
> Chalmers and Gothenburg University

## 1. Introduction to Pintos

In this lab, as well as Lab 3, your job is to extend the functionality of Pintos. Pintos is a simple operating system for the 80x86 architecture, built for educational purposes. It supports kernel threads, loading and running user programs, and a file system, but it implements all of these in a very simple way. In the Pintos projects, you will strengthen the support of Pintos in some of these areas.

For practical reasons, we will run Pintos projects in the Bochs system simulator. Bochs simulates an 80x86 CPU and its peripheral devices accurately enough that unmodified operating systems and software can run under it.

This document explains how to get started with Pintos on Chalmers StuDAT machines, describes the source-code structure, and provides instructions for building, running, debugging, testing, and submitting Lab 2. Read the entire document before starting the assignment.

### 1.1 Getting Started

To get started, log in to a machine on which Pintos can be built. The officially supported Pintos development machines for EDA093/DIT401 are the StuDAT Linux machines. We will test your code on these machines, and the instructions given here assume this environment. We cannot provide support for installing and working with Pintos on your own machine.

Once you have logged in to one of these machines, either locally or remotely, fetch the Pintos source code from the course Canvas page and extract it into your home directory.

Add the required binary directories to your `PATH`. Under Bash, the standard login shell, add the following line to `$HOME/.bashrc`, creating the file if it does not exist:

```sh
export PATH=/chalmers/sw/unsup64/phc/b/pkg/bochs-2.6.6/bin:$HOME/pintos/src/utils:$PATH
```

Files whose names begin with a dot are hidden and may not appear in file managers. Reload the configuration:

```sh
source $HOME/.bashrc
```

Alternatively, restart the terminal.

Make sure the programs in `pintos/src/utils/` are executable:

```sh
chmod +x pintos/src/utils/pintos*
chmod +x pintos/src/utils/backtrace
```

### 1.2 Source Tree Overview

The `pintos/src` directory contains the following:

- `threads/`: Source code for the base kernel, which you will modify in this lab.
- `userprog/`: Source code for the user-program loader, which you will not need to modify.
- `vm/`: An almost empty directory, which you will not need to modify.
- `filesys/`: Source code for a basic file system, which you will not need to modify.
- `devices/`: Source code for interfacing with I/O devices, including the keyboard, timer, disk, and batch scheduler. You will modify `timer.c` for Lab 2 and `batch-scheduler.c` for Lab 3.
- `lib/`: An implementation of a subset of the standard C library. Code in this directory is compiled into both the Pintos kernel and the user programs that run under it. In kernel code and user programs, headers in this directory can be included using `#include <...>`. You should not need to modify this code.
- `lib/kernel/`: Parts of the C library included only in the Pintos kernel. This directory also includes implementations of data types that you may use in your kernel code, including bitmaps, doubly linked lists, and hash tables. Headers can be included using `#include <...>`.
- `lib/user/`: Parts of the C library included only in Pintos user programs. Headers can be included using `#include <...>`.
- `tests/`: Tests for each project. You may modify this code if it helps you test your submission, but we will replace it with the original version before running the tests.
- `examples/`: Example user programs for general-purpose use. You should not need them for this assignment.
- `misc/`, `utils/`: Files that may be useful if you decide to work with Pintos on your own machine. Otherwise, you can ignore them.

### 1.3 Building Pintos

First, change to the `threads` directory and run `make`:

```sh
cd pintos/src/threads
make
```

This creates a `build` directory under `threads`, populates it with a `Makefile` and several subdirectories, and builds the kernel. The complete build should take less than 30 seconds.

The following files in the `build` directory are particularly relevant:

- `Makefile`: A copy of `pintos/src/Makefile.build`. It describes how to build the kernel.
- `kernel.o`: The object file for the entire kernel. It results from linking the object files compiled from each kernel source file. It contains debugging information, so you can use it with GDB or `backtrace`.
- `kernel.bin`: The kernel's memory image: the exact bytes loaded into memory when the kernel runs. It is `kernel.o` with debugging information removed. This saves space and prevents the kernel from exceeding the 512 kB size limit imposed by the kernel loader.
- `loader.bin`: The memory image for the kernel loader. This is a small assembly-language program that reads the kernel from disk into memory and starts it. It is exactly 512 bytes long, a size fixed by the PC BIOS.

The subdirectories of `build` contain object files (`.o`) and dependency files (`.d`) produced by the compiler. Dependency files tell `make` which source files must be recompiled when other source files or headers change.

### 1.4 Running Pintos

The supplied `pintos` program provides a convenient way to run Pintos in a simulator. In the simplest case, invoke it as `pintos argument...`, where each argument is passed to the Pintos kernel.

Change to the newly created `build` directory and run the `alarm-multiple` test:

```sh
cd pintos/src/threads/build
pintos run alarm-multiple
```

This passes the arguments `run alarm-multiple` to the Pintos kernel. The `run` argument instructs the kernel to execute a test, and `alarm-multiple` identifies the test.

Pintos boots and runs the test, which produces several screens of output. When it finishes, you can close Bochs using the **Power** button in the upper-right corner of the window or rerun the process using the **Reset** button beside it.

If no window appears, you are probably logged in remotely and X forwarding is not configured correctly. You can correct the X configuration or disable graphical output with `-v`:

```sh
pintos -v -- run alarm-multiple
```

Pintos sends its output to both the VGA display and the first serial port. By default, the serial port is connected to Bochs's standard input and output, so the same output appears in the terminal. You can redirect the serial output to a file:

```sh
pintos run alarm-multiple > logfile
```

The `pintos` program provides options for configuring the simulator and its virtual hardware. Options must precede the commands passed to the Pintos kernel and be separated from them by `--`:

```text
pintos option... -- argument...
```

Invoke `pintos` without arguments to see the available options.

The Pintos kernel also has commands and options other than `run`. To display them, use:

```sh
pintos -h
```

### 1.5 Debugging versus Testing

When debugging code, it is useful to run a program repeatedly and have it behave in exactly the same way. On later runs, you can make new observations without discarding or rechecking earlier ones. This property is called *reproducibility*. Bochs can be configured for reproducibility, and `pintos` uses this mode by default.

A simulation can be reproducible only when its input is identical on every run. When simulating a complete computer, every part of the computer must therefore remain the same. For example, you must use the same command-line arguments, disks, and Bochs version, and you must not press keys during execution because you cannot reproduce the exact timing of those key presses.

Although reproducibility is useful for debugging, it is a problem when testing thread synchronization. In reproducible mode, timer interrupts occur at the same points on every run, and so do thread switches. Running the same test repeatedly therefore provides no more confidence than running it once.

No number of runs can guarantee that your synchronization is perfect. However, testing with varied timing can increase your confidence that the code has no major flaws.

### 1.6 Legal and Ethical Issues

Pintos is distributed under a liberal license that permits free use, modification, and distribution. Students and others who work on Pintos own the code they write and may use it for any purpose. Pintos comes with **no warranty**, including no warranty of merchantability or fitness for a particular purpose.

In the context of the Chalmers EDA093/DIT401 course, respect the spirit and letter of the honor code by refraining from reading homework solutions available online or elsewhere. You may read the source code of other operating-system kernels, such as Linux or FreeBSD, but do not copy code from them literally. Cite in your report any code that inspired your solution.

### 1.7 Acknowledgements

The Pintos core and its documentation were originally written by Ben Pfaff (`blp@cs.stanford.edu`). Additional features were contributed by Anthony Romano (`chz@vt.edu`).

The supplied GDB macros were written by Godmar Back (`gback@cs.vt.edu`), and their documentation is adapted from his work.

The original structure and form of Pintos were inspired by the Nachos instructional operating system from the University of California, Berkeley [1].

The Pintos projects and documentation originated with projects designed for Nachos by current and former CS 140 teaching assistants at Stanford University, including Yu Ping, Greg Hutchins, Kelly Shaw, Paul Twohey, Sameer Qureshi, and John Rector.

This version was edited and adapted to the requirements of the EDA093/DIT401 Operating Systems course at Chalmers University of Technology by Hannaneh Najdataei and Dimitris Palyvos, in collaboration with Vincenzo Gulisano and Marina Papatriantafilou.

### 1.8 Trivia

Pintos originated as a replacement for Nachos with a similar design, but it has since diverged substantially. Pintos differs from Nachos in two important ways:

1. Pintos runs on real or simulated 80x86 hardware, whereas Nachos runs as a process on a host operating system.
2. Pintos is written in C, like most real-world operating systems, whereas Nachos is written in C++.

The name *Pintos* has three explanations:

1. Like nachos, pinto beans are a common Mexican food.
2. Pintos is small, and a pint is a small amount.
3. Like drivers of the eponymous car, students are likely to have trouble with blow-ups.

## 2. Assignment Description

One classic synchronization method is busy waiting: spinning in a loop until information from another thread or process causes the loop to end. An obvious drawback, especially on uniprocessor machines, is that CPU cycles are wasted without useful work being performed.

In this lab, you will study the synchronization implementation and provide an alternative implementation of a sleep function.

Your assignment is to reimplement `timer_sleep()`, defined in `devices/timer.c`. Although a working implementation is provided, it busy-waits by repeatedly checking the current time and calling `thread_yield()` until enough time has passed. Reimplement this function without busy waiting.

```c
void timer_sleep(int64_t ticks);
```

This function suspends execution of the calling thread until time has advanced by at least `ticks` timer ticks. Unless the system is otherwise idle, the thread does not need to wake after exactly `ticks` ticks. It is sufficient to place it on the ready queue after it has waited for the required amount of time.

`timer_sleep()` is useful for threads that perform real-time activities, such as blinking a cursor once per second.

The argument to `timer_sleep()` is expressed in timer ticks, not milliseconds or another unit. There are `TIMER_FREQ` timer ticks per second, where `TIMER_FREQ` is a macro defined in `devices/timer.h`. Its default value is 100. Do not change this value, because doing so is likely to cause many tests to fail.

The separate functions `timer_msleep()`, `timer_usleep()`, and `timer_nsleep()` sleep for a specified number of milliseconds, microseconds, or nanoseconds. They call `timer_sleep()` automatically when necessary, so you do not need to modify them.

If delays appear too short or too long, reread the explanation of the `-r` option in [Section 1.5](#15-debugging-versus-testing).

> **Hint:** To avoid busy waiting after calling `timer_sleep()`, the thread must block, changing its state from running to blocked. The processor does not store information about each thread's state; the blocked thread must store information about how long it has been blocked.

For each clock tick, a timer interrupt is triggered and its handler, `timer_interrupt()`, executes. Use this interrupt handler to activate sleeping threads and update thread statistics.

Use `thread_foreach()` to iterate over all blocked threads. Check whether each blocked thread is ready to wake and call `thread_unblock()` to activate it, or update its sleep timer.

## 3. Testing and Submission

Your assignment will be graded based on both test results and design quality. The grade is Pass or Fail.

### 3.1 Testing

To test your complete submission, invoke `make check` from the project's `build` directory:

```sh
cd pintos/src/threads/build
make check
```

This builds and runs each test and prints a **pass** or **fail** message for each one. When a test fails, `make check` also reports details about the failure. After all tests have run, it prints a summary of the results.

You can run and grade an individual test by explicitly building its `.result` file. For example:

```sh
make tests/threads/alarm-multiple.result
```

A test `t` writes its output to `t.output`. A script then grades that output as pass or fail and writes the verdict to `t.result`.

If `make` reports that the result is up to date but you want to rerun the test, run `make clean` or delete the corresponding `.output` file.

By default, each test provides feedback only when it finishes. To observe its progress, set `VERBOSE=1`:

```sh
make check VERBOSE=1
```

You can also pass options to the `pintos` command used by the tests. For example, to select a jitter value of 1:

```sh
make check PINTOSOPTS='-j 1'
```

All tests and related files are under `pintos/src/tests`. Before testing your submission, we will replace that directory with a pristine, unmodified copy to ensure that the original tests are used. You may modify tests while debugging, but we will run the originals.

All software has bugs, so some supplied tests may be flawed. If you believe a failure is caused by a bug in a test rather than your code, point it out so that we can investigate and correct it if necessary.

Do not write code that works only for the supplied test cases. For example, explicitly basing the kernel's behavior on the name of the running test is unacceptable and will receive no credit. If you are unsure whether a solution falls into a gray area, ask us.

### 3.2 Submission

We will judge your design from both the report and the source code you submit. To pass the lab, you must:

1. Implement all requested specifications.
2. Verify your code using the supplied self-tests.
3. Write a report describing the design and behavior of your solution.
4. Upload both the report and your code to Canvas.

#### 3.2.1 Writing the Report

Begin by describing the implementation of your solution. Briefly analyze each of the following:

- **Data structures:** Highlight your actual changes to data structures and briefly describe the purpose of every new or changed data structure. The limit of 25 words per description is a guideline intended to save time and avoid duplication with later sections.
- **Algorithms:** Explain how your code works. Write at a level below the high-level requirements in the assignment but above a line-by-line account of the code. Do not repeat or rephrase the assignment. Instead, explain how your implementation satisfies its requirements.
- **Synchronization:** Explain explicitly how you synchronize the relevant activity in this multithreaded operating-system kernel.
- **Time and space complexity:** State the time and space complexity of your implementation. An informal complexity analysis is sufficient; formal notation and proofs are not required.

#### 3.2.2 Preparing the Code

Your design will also be evaluated by examining the source code. We will typically compare the original Pintos source tree with your submission using a command such as:

```sh
diff -urpb pintos.orig pintos.submitted
```

We will compare the report's description with the submitted code. Important discrepancies will be penalized, as will bugs found through spot checks.

Pintos uses a consistent coding style. Make additions and modifications in existing source files blend in with the existing code. In new files, preferably use the Pintos style and, at minimum, keep your code internally consistent. The code should not look like a patchwork written in several unrelated styles.

Use horizontal and vertical whitespace to make the code readable. Add a brief comment to every structure, structure member, global or static variable, `typedef`, enumeration, and function definition. Update existing comments when modifying code.

Do not comment out code or use the preprocessor to ignore blocks of code; remove unused code entirely. Use assertions to document important invariants and decompose code into functions for clarity. Code that is difficult to understand because it violates these or other common software-engineering practices will be penalized.

Remember that code is written primarily to be read by people. It must also be accepted by the compiler, but the compiler does not care how readable it is.

#### 3.2.3 Final Submission

After verifying that your code works correctly on the StuDAT machines, prepare an archive containing only:

- Pintos files that contain your modifications; and
- the report file.

Upload the archive to Canvas.

## 4. FAQ

### Do I need to account for timer values overflowing?

No. Timer values are signed 64-bit numbers. At 100 ticks per second, they will last for almost 2,924,712,087 years. By then, Pintos is expected to have been phased out of the EDA093/DIT401 curriculum.

## Bibliography

1. W. A. Christopher, S. J. Procter, and T. E. Anderson. "The Nachos Instructional Operating System." In *Proceedings of the USENIX Winter 1993 Conference*, USENIX'93, page 4, USA, 1993. USENIX Association.
