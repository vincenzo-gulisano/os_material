from datetime import datetime
from os import mkdir, setsid, kill, killpg, getpgid
from pathlib import Path
from signal import SIGINT, SIGTERM
from socket import gethostname
from subprocess import run, PIPE, Popen, TimeoutExpired
from tempfile import gettempdir
from time import sleep, time
import unittest
from typing import Optional

from HTMLTestRunner.runner import HTMLTestRunner
from psutil import Process as ProcessInfo
from psutil import STATUS_ZOMBIE


class TestLsh(unittest.TestCase):

    lsh_path: Path
    lsh: Optional[Popen]

    @classmethod
    def setUpClass(cls) -> None:
        """
        Compile lsh from source before running the tests.
        """
        code_dir = Path.joinpath(Path(__file__).parent.parent, "code")
        build_dir = cls.make_tmp_dir()
        run(["cmake", "-B", build_dir, "-S", code_dir], check=True)
        run(["cmake", "--build", build_dir], check=True)
        cls.lsh_path = build_dir.joinpath("lsh")

    def setUp(self):
        """
        Initializes before each test; ensures that no leftover lsh process exists.
        """
        self.lsh = None

    def tearDown(self):
        """
        Cleanup after each test; checks if the lsh process is still running and terminates it if necessary.
        """
        self.assertIsNotNone(self.lsh)
        if self.lsh.poll() is None:
            print("tearDown: lsh is still running, killing it now.")
            self.lsh.kill()

            # Ensure that the process is cleaned up
            self.lsh.wait(timeout=3)

    def check_for_zombies(self):
        """
        Verifies that no child processes of lsh have become zombies.
        """
        self.assertIsNotNone(self.lsh)
        lsh_info = ProcessInfo(pid=self.lsh.pid)
        for child in lsh_info.children():
            self.assertNotEqual(STATUS_ZOMBIE, child.status(), msg=f"Zombie detected!")

    @staticmethod
    def make_tmp_dir() -> Path:
        """
        Creates a temporary directory.
        """
        tmp_dir = Path(gettempdir()).joinpath("test_lab1_" + str(time()))
        mkdir(tmp_dir)
        return tmp_dir

    @staticmethod
    def make_test_txt(cwd: Path):
        """
        Generates test.txt that contains "hello" to use for input/output redirection tests.
        """
        with open(cwd.joinpath("test.txt"), "w") as f:
            f.write("hello")

    def check_test_txt(self, file: Path):
        """
        Validates that the content of a file is "hello\n".
        """
        try:
            with open(file, "r") as f:
                content = f.readlines()
            self.assertListEqual(content, ["hello\n"], msg="Redirected output was not in file")
        except FileNotFoundError:
            self.assertTrue(file.exists(), msg="Failed to detect output file")

    def start_lsh(self, cwd: Path = None):
        """
        Launches the lsh process, setting it up to run commands with optional custom working directory.
        """
        self.assertIsNone(self.lsh)
        self.lsh = Popen(str(self.lsh_path), stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd, preexec_fn=setsid)

    def run_cmd(self, cmd: str):
        """
        Writes a command to lsh's stdin and ensures the command is processed by flushing the stream.
        """
        self.assertIsNotNone(self.lsh)
        self.lsh.stdin.write(f"{cmd}\n".encode())
        self.lsh.stdin.flush()

        # At this point, the command is written to stdin of lsh
        # Give lsh some time to start and invoke the cmd
        sleep(1)

    def exit_with_eof(self) -> str:
        """
        Signals EOF to lsh and checks for graceful termination, including process exit code validation.
        """
        is_lsh_exiting_with_eof = True
        try:
            # Will place EOF in lsh's STDIN
            out, err = self.lsh.communicate(timeout=3)
            self.assertEqual("", err.decode())
            self.assertEqual(0, self.lsh.returncode,
                             msg="lsh should return 0 after exiting with EOF. \n"
                             "If the return code is not 0, it may be due to a runtime assertion failing within your implementation. \n"
                             "Please check your assertions and ensure they are not triggering any faults.")

            return out.decode()
        except TimeoutExpired:
            is_lsh_exiting_with_eof = False

        self.assertTrue(is_lsh_exiting_with_eof,
                        "lsh did not terminate upon EOF. \n"
                        "This might indicate that the feature is missing (exit on EOF) or that lsh has become non-responsive. \n"
                        "Ensure 'waitpid' calls are targeting the correct PID. ")

    def run_cmd_and_exit(self, cmd: str, check_for_zombies: bool = False) -> str:
        """
        Runs a command in lsh, optionally checks for zombie processes, and handles process termination with EOF.
        """
        self.run_cmd(cmd)
        if check_for_zombies:
            self.check_for_zombies()
        return self.exit_with_eof()

    def test_exit_command(self):
        """
        Tests that the 'exit' command properly terminates 'lsh'.
        """
        self.start_lsh()
        self.run_cmd("exit")

        # wait for max 3 seconds for lsh to exit
        try:
            self.lsh.wait(3)
        except TimeoutExpired:
            self.assertTrue(False, msg="It looks like you don't have an implementation "
                                             "for the build-in command exit")

        self.assertEqual(0, self.lsh.returncode, msg="lsh should return 0 after executing exit")

    def test_exit_with_CTRL_D(self):
        """
        Tests that lsh terminates correctly when EOF (Ctrl-D) is sent to stdin.
        """
        self.start_lsh()
        self.exit_with_eof()

    def test_date(self):
        r"""
        Runs "date" and then check if the current year appears in stdout.
        """
        self.start_lsh()
        current_year = str(datetime.now().year)
        self.assertIn(current_year, self.run_cmd_and_exit("date"))

    def test_output_redirection(self):
        """
        Tests lsh's ability to handle output redirection.
        Runs 'echo hello > hello.txt' and verifies the content of the resulting file.
        """
        cwd = self.make_tmp_dir()
        self.start_lsh(cwd)

        out = cwd.joinpath("hello.txt")
        self.run_cmd_and_exit("echo hello > ./hello.txt")
        self.check_test_txt(out)

    def test_input_redirection(self):
        """
        Tests the input redirection capability.
        Creates a file with known content (test.txt) and uses 'grep el < ./test.txt' to search within the file.
        """
        cwd = self.make_tmp_dir()
        self.start_lsh(cwd)

        self.make_test_txt(cwd)
        out = self.run_cmd_and_exit("grep el < ./test.txt")
        self.assertIn("hello", out)

    def test_in_and_out_redirection(self):
        """
        Tests both input and output redirection together.
        Creates a file with known content (test.tx) and using 'grep hello < test.txt > test_out.txt'
        to filter its content and redirect the output to another file.
        """
        cwd = self.make_tmp_dir()
        self.start_lsh(cwd)

        self.make_test_txt(cwd)
        out = cwd.joinpath("test_out.txt")
        self.run_cmd_and_exit("grep hello < test.txt > test_out.txt")
        self.check_test_txt(out)

    def test_cd(self):
        """
        Verifies the functionality of the 'cd' command in lsh.
        The test involves creating a temporary directory and a test file within this directory.
        It runs the 'cd' command by changing to this temporary directory
        and using 'ls' to confirm the presence of the test file.
        """
        tmp_dir = self.make_tmp_dir()
        with open(tmp_dir.joinpath("hello.txt"), "w") as f:
            f.write("")
        cwd = tmp_dir.parent
        self.start_lsh(cwd)

        out = self.run_cmd_and_exit(f"cd {tmp_dir}\nls")

        # Check if ls output has hello.txt to verify that cd works
        self.assertIn("hello.txt", out)

    def test_for_zombies(self):
        """
        Run two consecutive commands and check for their output and for zombie processes.
        """
        self.start_lsh()
        self.run_cmd("hostname")
        self.run_cmd("date")
        self.check_for_zombies()
        out = self.exit_with_eof()
        self.assertIn(gethostname(), out, msg="Did not find expected output from the first command")
        current_year = str(datetime.now().year)
        self.assertIn(current_year, out, msg="Did not find expected output from the first command")

    def test_echo_rev(self):
        """
        Tests the pipeline functionality.
        Reverses a string using 'echo ananab | rev' and expexting 'banana' in the output.
        """
        self.start_lsh()
        out = self.run_cmd_and_exit('echo ananab | rev', check_for_zombies=True)
        self.assertIn("banana", out)

    def test_echo_grep_wc(self):
        """
        Validates a complex command pipeline involving 'echo', 'grep', and 'wc'.
        """
        self.start_lsh()
        out = self.run_cmd_and_exit("echo hello world | grep hello | wc -w\n", check_for_zombies=True)
        self.assertIn("2", out)

    def test_bg_and_fg(self):
        """
        Runs a background job and a foreground command simultaneously.
        """
        self.start_lsh()
        self.run_cmd("sleep 3 &")

        # Check if bg process started
        lsh_info = ProcessInfo(self.lsh.pid)
        self.assertEqual(1, len(lsh_info.children()), msg="Could not detect bg process")

        # Execute a foreground command
        self.run_cmd("echo hello")

        # Wait for background command to complete
        sleep(3)

        self.check_for_zombies()
        self.exit_with_eof()

    def test_CTRL_C(self):
        """
        Simulates a CTRL-C interrupt to test lsh's signal handling by running a long sleep command and interrupting it.
        """
        self.start_lsh()
        self.run_cmd("sleep 60")

        # Give lsh some time to start and invoke the cmd
        sleep(1)

        # Simulate pressing CTRL-C by sending SIGINT to the entire lsh process group
        killpg(getpgid(self.lsh.pid), SIGINT)

        # Check if fg process terminated
        lsh_info = ProcessInfo(self.lsh.pid)
        self.assertEqual(0, len(lsh_info.children()),
                         msg="Expected no child processes to remain after sending SIGINT to simulate CTRL-C, \n"
                             "indicating that all foreground processes should be terminated.")

        self.exit_with_eof()

    def test_CTRL_C_with_fg_and_bg(self):
        """
        Tests lsh's response to a CTRL-C signal with concurrent foreground and background processes.
        Ensure that only the foreground process is terminated, and the background process remains running.
        """
        self.start_lsh()
        self.run_cmd(cmd="sleep 60 &")

        # Store pid of background process
        lsh_info = ProcessInfo(self.lsh.pid)
        self.assertEqual(1, len(lsh_info.children()), msg="I did not expect to see more than 1 child processes "
                                                          "after executing a background command")
        bg_pid = lsh_info.children()[0].pid

        # Start foreground process
        self.run_cmd("sleep 60")
        self.assertEqual(2, len(lsh_info.children()), msg="You do not seem to support a foreground process "
                                                          "and a background process at the same time")

        # Simulate pressing "Ctrl-C" by sending SIGINT to the entire lsh process group
        killpg(getpgid(self.lsh.pid), SIGINT)
        sleep(1)

        self.assertEqual(1, len(lsh_info.children()), msg="There should be only one child process after Ctrl+C")
        self.assertEqual(bg_pid, lsh_info.children()[0].pid, msg="You should not have terminated the background process")

        kill(bg_pid, SIGTERM)
        self.exit_with_eof()

if __name__ == "__main__":
    unittest.main(testRunner=HTMLTestRunner(report_name="test-lsh", open_in_browser=True, description="Lab 1 tests"))
