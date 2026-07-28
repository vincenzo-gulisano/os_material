#include "tests/threads/tests.h"
#include <debug.h>
#include <string.h>
#include <stdio.h>

struct test 
  {
    const char *name;
    test_func *function;
  };

static const struct test tests[] = 
  {
    {"alarm-single", test_alarm_single},
    {"alarm-multiple", test_alarm_multiple},
    {"alarm-simultaneous", test_alarm_simultaneous},
    {"alarm-zero", test_alarm_zero},
    {"alarm-negative", test_alarm_negative},
    {"batch-scheduler", test_batch_scheduler},
  };

static const char *test_name;

/* Runs the test named NAME. */
void
run_test (const char *name) 
{
  const struct test *t;

  for (t = tests; t < tests + sizeof tests / sizeof *tests; t++)
    if (!strcmp (name, t->name))
      {
        test_name = name;
        msg ("begin");
        t->function ();
        msg ("end");
        return;
      }
  PANIC ("no test named \"%s\"", name);
}

/* Prints FORMAT as if with printf(),
   prefixing the output by the name of the test
   and following it with a new-line character. */
void
msg (const char *format, ...) 
{
  va_list args;
  
  printf ("(%s) ", test_name);
  va_start (args, format);
  vprintf (format, args);
  va_end (args);
  putchar ('\n');
}

/* Prints failure message FORMAT as if with printf(),
   prefixing the output by the name of the test and FAIL:
   and following it with a new-line character,
   and then panics the kernel. */
void
fail (const char *format, ...) 
{
  va_list args;
  
  printf ("(%s) FAIL: ", test_name);
  va_start (args, format);
  vprintf (format, args);
  va_end (args);
  putchar ('\n');

  PANIC ("test failed");
}

/* Prints a message indicating the current test passed. */
void
pass (void) 
{
  printf ("(%s) PASS\n", test_name);
}

