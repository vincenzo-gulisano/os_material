/* Tests cetegorical mutual exclusion with different numbers of threads.
 * Automatic checks only catch severe problems like crashes.
 */
#include <stdio.h>
#include "tests/threads/tests.h"
#include "threads/malloc.h"
#include "threads/synch.h"
#include "threads/thread.h"

#include "devices/batch-scheduler.c"

void test_batch_scheduler (void)
{
    init_bus ();
    batch_scheduler (3, 4, 3, 3);
}
