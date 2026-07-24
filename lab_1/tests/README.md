# Dependencies

Open a your terminal and navigate to this directory:
```sh
cd <path to this directory>
```

Use `python3` to create a virtual environment.
Use any version of Python >= 3.9
```sh
python3 -m venv venv
```

Install dependencies in your newly created virtual environment:
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

The test report is stored in `html` file:
`./reports/report_<date & time>/report_<date & time>.html`

Immediately after test execution, you should be redirected automatically to the `html` page containing the results.

In some environments, f.e. if you are using KDE, the automatic redirection may fail.

# In Case of Failure

1. Identify the failing test case from the test report. Each test case has a name that starts with `test_`, for example, `test_date`.

2. Open `test_lsh.py` and find the corresponding test method, like `def test_date(self):`.

3. Read the documentation under the method definition to understand what the test case is checking for.

4. Manually run the test case to reproduce the failure. Once you've identified the issue, go ahead and fix the bug!

To skip a test case, if for example is crashing the entire test suite, you can decorate it with `@unittest.skip`.
