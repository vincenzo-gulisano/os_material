# -*- perl -*-
use tests::tests;
check_expected ([<<'EOF']);
(batch-scheduler) begin
(batch-scheduler) sender-prio acquired slot
(batch-scheduler) sender-prio acquired slot
(batch-scheduler) sender-prio acquired slot
(batch-scheduler) receiver-prio acquired slot
(batch-scheduler) receiver-prio acquired slot
(batch-scheduler) receiver-prio acquired slot
(batch-scheduler) receiver-prio acquired slot
(batch-scheduler) receiver acquired slot
(batch-scheduler) receiver acquired slot
(batch-scheduler) receiver acquired slot
(batch-scheduler) sender acquired slot
(batch-scheduler) sender acquired slot
(batch-scheduler) sender acquired slot
(batch-scheduler) end
EOF
pass;
