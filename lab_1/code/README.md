Compiling and Running
---------------------

Use CMake:
```sh
cmake -Bbuild
cmake --build build
./build/lsh
```

The starter code has been tested on:
- Ubuntu 22.04
- Debian 6.1.94-1 (StuDAT)
- macOS 12.x / 13.x (Apple silicon)

Local Development Setup
-----------------------

If you choose to develop locally, ensure that you have the necessary packages installed: a compiler, CMake, Readline, and ncurses (which includes termcap functionality).
For example, on Ubuntu, you can install them using:

```sh
sudo apt-get update
sudo apt-get install build-essential cmake libreadline-dev libncurses5-dev libncursesw5-dev
```
