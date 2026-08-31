**<u>Do I need to implement utilities like ls, date, who, sleep, etc.?</u>**
**No.**
These are standard UNIX utilities, available on macOS and Linux. Your code should spawn a process to run them.


**<u>Should I bother with manual testing if automated tests are available?</u>**
**Absolutely.** 
While automated tests offer immediate feedback, they can't catch every issue.
Manual testing provides an additional layer of scrutiny that's often essential.
Don't rely solely on automated tests; they're useful but not foolproof.


**<u>Does passing all automated tests guarantee that I'll pass the lab?</u>**
**Yes, as long as...**
you also submit a comprehensive report and are able to successfully explain your solution in a potential oral examination.


**<u>My solution only works on my personal machine. Is this acceptable?</u>**
**No.** 
Your solution needs to be compatible with the StuDAT computers, as they are the standard testing environment.


**<u>GitHub Actions reports test failures that I can't reproduce on the StuDAT computers. Is this a problem?</u>**
**No.** 
The StuDAT computers are our point of reference for grading.
If your code works there, you're in the clear.


**<u>What happens when I debug a forked process using gdb?</u>**
When you debug a program that forks using gdb, **by default gdb will continue to debug the parent process after the fork.**
The child process will run independently, and gdb will not automatically attach to it.
This behavior might not be helpful if the issues you are trying to debug occur in the child process.

You can instruct gdb to follow the child process immediately after a fork by using the `set follow-fork-mode` command within gdb.


**<u>What is the expected behaviour of "grep apa | ls" ?</u>**
This command checks if processes spawned by the custom shell wait correctly for the termination of their children when using pipes.

***About grep***

First of all, consider the first part, **grep apa** 

As described in the grep man entry, "***grep** searches the named input FILEs (or standard input if no files are named) for lines containing a match to the given PATTERN. By default, grep prints the matching lines.*" 

Since we only provide a PATTERN argument (apa), grep will read the standard input, searching for our pattern.
It will end the search when it reads the EOF character.
You can insert this character is by pressing <Ctrl - D>.
You can verify this behavior by running **grep apa** and then typing various lines of text, some of which contain the "apa" pattern. 
The lines containing the pattern will be (re)printed by grep.
The process is terminated when you insert the EOF character. 

***Waiting grep + pipe***

If your custom shell is working correctly, grep should still wait for the EOF even if you pipe its output to some other command such as ls.
The output of the ls command might be printed either before or after grep is terminated (in bash it comes before), but ideally **grep should wait until it receives the EOF**.
Returning to the shell prompt immediately and leaving grep running (and reading input) might lead make your shell behave strangely (e.g. ignore typed characters) or even completely unusable.
**Such solutions will not be accepted.**

***<font size="4">When compiling on my machine, I am getting this error message</font>***: `fatal error: 'readline/readline.h' file not found`

This likely means you haven't installed the `readline` library.
You can install it using package managers like `apt` for Ubuntu (`sudo apt install libreadline-dev`) or `brew` for macOS (`brew install readline`).
Then try compiling again.