#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <sys/wait.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv)
{

    int sockets[2];
    char buf[1024];
    pid_t pid;

    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) < 0)
    {
        perror("Ошибка socketpair");
        return EXIT_FAILURE;
    }

    if ((pid = fork()) == -1)
    {
        perror("Ошибка fork");
        exit(EXIT_FAILURE);
    }
    else if (pid == 0)
    {
        // код процесса потомка
        char msg[] = "aaaaaaaaa";
        close(sockets[1]); // закрываем для другого процесса

        printf("Child send: %s\n", msg);
        write(sockets[0], msg, sizeof(msg));
        read(sockets[0], buf, sizeof(buf));
        printf("Child recieve: %s\n", buf);

        close(sockets[0]);

        exit(EXIT_SUCCESS);
    }
    else
    {
        // код процесса предка
        char msg[] = "bbbbbbb";
        close(sockets[0]); // закрываем для другого процесса

        read(sockets[1], buf, sizeof(buf));
        printf("Parent send: %s\n", msg);
        write(sockets[1], msg, sizeof(msg));
        printf("Parent recieve: %s\n", buf);

        close(sockets[1]);
    }

    pid_t w_pid;
    int status;

    w_pid = wait(&status);

    if (w_pid == -1)
    {
        perror("Ошибка wait");
        exit(EXIT_FAILURE);
    }

    if (WIFEXITED(status))
    {
        printf("Child process: PID = %d завершился с кодом %d\n", w_pid, WEXITSTATUS(status));
    }
    else if (WIFSIGNALED(status))
    {
        printf("Child process: PID = %d killed by signal %d\n", w_pid, WTERMSIG(status));
    }
    else if (WIFSTOPPED(status))
    {
        printf("Child process: PID = %d stopped by signal %d\n", w_pid, WSTOPSIG(status));
    }

    return EXIT_SUCCESS;
}