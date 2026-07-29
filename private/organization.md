## Course PM

EDA093 / DIT401 Operating Systems, LP1 HT25 (7.5 hp)

The course is offered by the Department of Computer Science and Engineering. It includes both self-managed activities and live interaction with the teacher.

### Course purpose

The course introduces the design and implementation of operating systems. Topics include concurrent processes, resource management, deadlocks, memory management, virtual memory, processor scheduling, file systems, and security issues. The labs provide hands-on experience with operating system design through essential OS modules such as multiprogramming, UNIX-like shell functionality, and concurrency.

### Learning objectives

After successful completion of the course, participants will be able to demonstrate knowledge and understanding of:

- the core functionality of modern operating systems: processes/threads, scheduling, virtual memory, file systems, parallelism, kernels, shells, microkernels, and virtual machines;
- key concepts and algorithms in operating system implementations: synchronization, deadlock avoidance/prevention, memory management, processor scheduling, disk scheduling, virtual machines, and file system organization; and
- the implementation of simple OS components.

Participants will also be able to:

- appreciate the design space and trade-offs involved in implementing an operating system;
- write C programs that interface with the operating system at the system call level;
- implement system-level code in C; and
- program using multithread synchronization constructs.

### Course literature

Modern Operating Systems by Andrew S. Tanenbaum, fifth edition.

### Course staff

Teacher: Vincenzo Gulisano, [vincenzo.gulisano@chalmers.se](mailto:vincenzo.gulisano@chalmers.se)

Teaching assistants:

- Jingyu Liu, [jingyu.liu@chalmers.se](mailto:jingyu.liu@chalmers.se)
- Jacob Stacey Garby, [garby@chalmers.se](mailto:garby@chalmers.se)
- Andrea Pistelli, [pistelli@student.chalmers.se](mailto:pistelli@student.chalmers.se)

### Student representatives

TBA

### Exam dates

- 2026/10/27, 08:30-12:30 (registration period: 2026/08/10 - 2026/10/11)
- 2027/01/04, 08:30-12:30 (registration period: 2026/11/23 - 2026/12/14)
- 2027/08/16, 14:00-18:00 (registration period: 2027/07/05 - 2027/08/01)

### Schedule

See the bottom of the page.

### Course organization

The course has two main live activities: in-person sessions for discussion and exercises, and in-person laboratory sessions. The schedule is below.

Each session is dedicated to a specific topic. Before each session, students are expected to watch all videos and read all slides related to the topics discussed in that session. For example, before "Introduction to OSs / Processes", students should watch the videos and read the slides for "Introduction" and "Processes".

### Course material

Videos, slides, and exercises are available in the [course-material repository](https://github.com/vincenzo-gulisano/os_material).

The exercises for each topic are at the end of the corresponding slides. Answers are in the presenter notes. Students are strongly encouraged to solve the exercises before reading the solutions. The PDF slides can be used for this, since they do not contain the answers.

During in-person sessions, topics may be discussed further, with extra examples and exercises not found in the slides.

Slides and videos may also be updated during the course. Check the repository commits to see whether updates have been made.

### Final examination

The final examination can cover everything shared and discussed at any point during the course, including live discussion during in-person sessions.

### Questions and contact

Ask questions live during the in-person sessions. If you have a general question, ask it during the session itself, not during the break.

Contact the examiner by email.

Before opening a new lab discussion, check the relevant lab FAQ or question page and existing discussions to see whether your question has already been answered.

If not, use the dedicated discussion page in Canvas. For Lab 1 questions, start the topic with "Lab 1:" followed by a brief, descriptive summary of the issue.

Use the lab sessions to interact with the TAs.

You may also help your classmates by answering their questions. If an answer is incorrect, the course staff will correct it.

### Labs

There will be three labs. For each lab:

- The material is available in the [course-material repository](https://github.com/vincenzo-gulisano/os_material).
- Groups should use the pool of Linux student computers on the Chalmers remote servers (`distans.cdal.chalmers.se:33899`) while developing and testing their code. Groups may practice on other computers, but they must compile and run their final solutions on the remote servers. The TAs' final evaluation is carried out only on those servers, so ensure that your solution is compatible with them.
- [Instructions for connecting via RDP or VNC](https://chalmers.topdesk.net/tas/public/ssp/content/detail/knowledgeitem?unid=304967f9ad004d3293b986a976e39833) are available online. SSH access to these servers is not available. Read the instructions carefully, especially those explaining how to exit the session when you are finished.
- A script will be provided to check, on `distans.cdal.chalmers.se`, whether the lab compiles, runs, and passes a certain set of tests.
- Successfully running the script does not mean that the group has passed the lab.
- Passing the script only means that the group can be inspected further by a TA. There can be manual inspection, groups may need to explain decisions and/or modify their code, and any group member can be asked to explain or comment on the code. Who is asked is decided by the TAs and/or examiner.
- Once the script runs successfully, groups must upload their source files, the message generated by the script, and a report to Canvas.
- Each lab has an internal deadline (see the schedule).
- Each group is strongly recommended to book at least one lab-session slot in Canvas, using the group ID.
- Students may ask TAs questions without booking, but only if the TAs are not booked at that time. Priority is given to booked groups.
- For questions about previous labs, do not use booking. Enter and wait for a TA. Priority is always given to the current lab.
- If a group fails a lab, resubmission will be at the next re-exam for that specific lab.

### Important information about group work

Group-allocation dates and deadlines are published on the dedicated **Group Allocation Schedule** page in Canvas.

Labs are a fundamental part of the Operating Systems course. Besides the course-specific learning objectives, they provide practice in peer collaboration, teamwork with people who may not be known from before, and student interaction that accounts for Equality, Diversity, and Inclusion (EDI).

For this reason, groups are created randomly and cannot be rearranged according to student preferences. Chalmers' basic stance is that students should learn to cooperate with different people, because that is required in the workplace and is in accordance with the Higher Education Ordinance.

If a student is registered for the course, the examiner assumes that the student has the time needed to take it, that this time overlaps sufficiently with normal teaching hours, and that the student is aware of the course prerequisites.

Exceptions are granted extremely seldom and only for very specific cases. Students may contact the examiner if they believe an exception should be granted, but the following examples do not grant exceptions:

- "I do not know / do not cooperate optimally with person X." This is an opportunity to get to know that person or learn how to cooperate in a group, even if the setup is not "optimal".
- "My time schedule / daily routine is not common." The examiner assumes that students registered for the course because, among other things, they can attend it.
- "My programming skills are non-existent; I prefer to work alone." The examiner assumes that students checked the course prerequisites before deciding to take it.
- "I had such a great time working with person X in the past that I would like to be with X again." This is an opportunity to get to know more people.
- "All the people in these X groups and I have agreed to reshuffle like this." This is not a feature of this course; see the previous points.

Labs are designed for groups of three students, but groups of two may be created if necessary. This does not mean that students can choose groups of two. It means that if the number of active lab participants is not divisible by three, some groups may have two members and can still complete the labs successfully.

Initial group suggestions are not final because we do not yet know whether all students in a group, for example A, B, and C, are actively taking the course. If B and C are not participating, group changes may still happen. Students may contact their lab partners now, but the group may still change even if all three currently assigned students intend to do the labs.

Since Chalmers/GU offers this course with live in-person lectures, the examiner assumes that enrolled students have the time and possibility to take it. If a student's personal schedule/life does not allow attendance, that is unfortunate, but the course will not be adapted because of that. With more than 150 registered students, individual adjustments do not scale. Therefore, each student must acknowledge in Canvas that they have seen the group to which they have been assigned.

If a student does not acknowledge, the examiner assumes that the student is not interested in taking the labs right now, for example because the student registered but decided not to take the course, or because the student is retaking the course to prepare for the exam but has already completed the labs. The student can still complete the labs, but the case will be handled after regular groups have been handled. Belonging to a group of three, or two in some cases, is still required; lack of acknowledgment is not an exemption from group work.

Some students may acknowledge while other students in the same group do not. Therefore, students who have acknowledged and belong to groups with fewer than three acknowledged members will be compacted into groups of three acknowledged students. As before, the examiner may need to create some groups of two, depending on the case.

Once most students are in groups ready to begin, each group must upload a "contract" specifying how they will work together. The purpose of the contract is to ensure that students meet and discuss how they plan to work before starting. It does not need to be formal: students can have a coffee, meet in person, meet online, or both. They should meet in one way or another and think about how they will work together.

### Final information students need to be aware of

The examiner is aware that "stuff happens", and the examiner/TAs are here to help. However, the course team has limited people and time, and there may be around 150 unique cases to handle.

Even after agreeing on how to work through the contract, "stuff happens" in groups. As soon as a group member thinks something is not working, that member should discuss it with the whole group and use the contract to identify what is not going according to plan. If that does not solve the issue, the member should escalate it to the examiner as soon as possible, so that the examiner can help/decide how to proceed. This must be done respectfully and through supportive dialogue. The assessment of whether a student passes or fails the labs and/or the course is up to the examiner only.

Agreements such as "A does lab 1, B does lab 2" are not acceptable group collaboration. What is shared by the group is assumed to have been done by the group. If that is not the case, the group is sharing work while knowing that it contradicts the rules, and this will be taken into account if examiner intervention is required to solve a problem/conflict.

As part of a group, what each member does represents what the group does. Once a student submits/shares something as a group, the student acknowledges that it has been done by the group in accordance with the contract. There is no retroactive handling of problems once a lab has been uploaded. Problems must be shared before uploading the lab. Genuine technical errors can still be fixed promptly if reported.

### Template for the contract

Groups may add other points, but the document uploaded to Canvas is expected to include the points below. Use this as an opportunity to learn how to work in groups. All members must meaningfully contribute to every lab.

- Members of the group.
- Day(s) on which the discussion happened.
- Form in which the discussion happened (in person/remotely/both).
- Strengths of each member, for example: very good at C, likes writing reports, good at coordination/task distribution.
- Aspects each member is less good with, for example: very bad at C, dislikes writing reports, bad at coordination/task distribution.
- Each member's preferred way to tackle problems, for example: brainstorm together, or think alone first and then discuss.
- Anything important that members want to share with the group, for example: punctuality, food, or other things.
- Agreement on working together:
  - How will you combine each member's strengths/weaknesses and work together?
  - How will you meet: in person, remotely, or both?
  - How frequently will you meet?
  - What are the preferred days?
  - How will you communicate, for example by email, Slack, Teams, Discord, or other channels?
- Any other point.
