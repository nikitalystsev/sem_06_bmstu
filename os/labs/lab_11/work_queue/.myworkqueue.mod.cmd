savedcmd_/home/fool/OS/lab_9/work_queue/myworkqueue.mod := printf '%s\n'   myworkqueue.o | awk '!x[$$0]++ { print("/home/fool/OS/lab_9/work_queue/"$$0) }' > /home/fool/OS/lab_9/work_queue/myworkqueue.mod