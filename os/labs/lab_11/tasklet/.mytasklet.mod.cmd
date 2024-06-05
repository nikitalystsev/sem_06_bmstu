savedcmd_/home/fool/OS/lab_9/tasklet/mytasklet.mod := printf '%s\n'   mytasklet.o | awk '!x[$$0]++ { print("/home/fool/OS/lab_9/tasklet/"$$0) }' > /home/fool/OS/lab_9/tasklet/mytasklet.mod
