# Dependencies

Open a terminal and navigate to this directory:
```sh
cd <path to this directory>
```

Use `python3` to create a virtual environment.
Use Python 3.9 or later:
```sh
python3 -m venv venv
```

Install the dependencies in your new virtual environment:
```sh
# Activate the virtual environment
source ./venv/bin/activate

# Install dependencies
pip install -r ./requirements.txt
```

# Run the tests

```sh
# Activate the virtual environment
source ./venv/bin/activate

# Execute tests
python test_lsh.py
```

The test report is stored in an HTML file at:
`./reports/report_<date & time>/report_<date & time>.html`

After the tests finish, the HTML report should open automatically in your browser.

In some environments, such as KDE, the report may not open automatically.

# In Case of Failure

1. Identify the failing test case in the test report. Each test case has a name that starts with `test_`, such as `test_date`.

2. Open `test_lsh.py` and find the corresponding test method, such as `def test_date(self):`.

3. Read the documentation under the method definition to understand what the test case is checking for.

4. Manually run the test case to reproduce the failure. Once you have identified the issue, fix the bug.

To skip a test case—for example, if it crashes the entire test suite—decorate it with `@unittest.skip`.
