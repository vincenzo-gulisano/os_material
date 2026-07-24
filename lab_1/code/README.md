Compiling and Running
---------------------

Use `cmake`:
```sh
cmake -Bbuild
cmake --build build
./build/lsh
```

Has been tested on:
- Ubuntu 22.04
- Debian 6.1.94-1 (StuDAT)
- macOS 12.x / 13.x (apple silicon)

Local Development Setup
-----------------------

If you choose to develop locally, ensure you have the necessary packages installed for the compiler, `cmake`, `readline`, and `ncurses` (which includes termcap functionality). 
For example, on Ubuntu systems, you can install these using:

```sh
sudo apt-get update
sudo apt-get install build-essential cmake libreadline-dev libncurses5-dev libncursesw5-dev
```
