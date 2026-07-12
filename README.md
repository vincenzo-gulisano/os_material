# Operating Systems Course Material

This repository contains teaching material for the Operating Systems course EDA093/DIT401. It
includes video lectures, subtitles/transcripts, and slide decks.

## Repository Contents

- Topic folders such as `processes/`, `threads/`, and `virtual_memory/`
  contain the video lectures (`.mp4`) and matching subtitles (`.srt`).
- `slides/` contains the slide decks, usually as both editable `.pptx` files
  and exported `.pdf` files.
- `overview.xlsx` is the source overview used for the suggested lecture order
  below.

The `.mp4` files are tracked with Git LFS. After cloning, run `git lfs pull` if
the videos are missing or appear as pointer files.

## Suggested Order

The order below is the suggested order for the various lectures. For each lecture, use the matching
slide deck in `slides/` and watch the numbered videos in the corresponding
topic folder.

| Order | Lecture | 
| --- | --- | 
| 01 | Introduction |
| 02 | Processes | 
| 03 | Multithreaded Programming | 
| 04 | Scheduling | 
| 05 | Synchronization - Part 1 |
| 06 | Synchronization - Part 2 |
| 07 | Memory Management | 
| 08 | Virtual Memory |
| 09 | File Systems |
| 10 | Security |
| 11 | I/O Systems |
| 12 | Virtualization |

Additional slide-only decks are available for the course introduction and
conclusion.

## Video Part Order

### 01. Introduction

1. Introduction
2. System calls
3. Services
4. OS structures

### 02. Processes

1. Introduction
2. Context switches
3. Process information
4. Scheduling
5. `fork`/`exec`
6. Inter-process communication
7. Pipes

### 03. Multithreaded Programming

1. Introduction
2. Multithreaded processes
3. Concurrent vs. parallel execution
4. Amdahl's Law
5. Multithreading models
6. Pthreads
7. Implicit threading
8. Threading issues

### 04. Scheduling

1. Introduction and CPU-bound vs. I/O-bound processes
2. Scheduling goals in batch systems
3. Scheduling goals in interactive systems
4. Continued discussion on user-level and kernel-level threads
5. Multiprocessor challenges, part 1
6. Multiprocessor challenges, part 2
7. Multiprocessor scheduling

### 05. Synchronization - Part 1

1. Introduction
2. Critical section / check-completion approach
3. Check-order / after-you approach
4. Peterson's algorithm
5. Hardware support / RMW instructions
6. Semaphores
7. Other synchronization techniques

### 06. Synchronization - Part 2

1. Bounded-buffer producer/consumer
2. Resource allocation, deadlocks, and conditions for deadlocks
3. Dining philosophers
4. Dining philosophers - no circular wait
5. Dining philosophers - no no-preemption
6. Dining philosophers - no hold-and-wait
7. Lamport's bakery algorithm
8. Readers/writers
9. Deadlock avoidance

### 07. Memory Management

1. Introduction
2. Base/limit registers
3. Logical/physical addresses
4. Swapping
5. Contiguous allocation
6. Segmentation
7. Paging

### 08. Virtual Memory

1. Introduction
2. Page faults
3. Copy-on-write
4. Page replacement, part 1
5. Page replacement, part 2
6. Allocation of frames
7. Thrashing

### 09. File Systems

1. Introduction
2. Access methods and blocks
3. Disk structure
4. File system structure
5. Allocation methods
6. Free space
7. File sharing and protection

### 10. Security

1. Introduction
2. Protection domains
3. Access control lists
4. Capabilities
5. Authentication
6. Buffer overflow attacks

### 11. I/O Systems

1. Introduction
2. Bus structure
3. Communication ways
4. Interrupts
5. DMA
6. Application I/O interface
7. Kernel I/O subsystem
8. Performance

### 12. Virtualization

1. Introduction
2. Requirements for virtualization
3. Types of hypervisors
4. Efficient virtualization
5. Memory virtualization
6. I/O virtualization
7. Other benefits
8. Virtualization and clouds