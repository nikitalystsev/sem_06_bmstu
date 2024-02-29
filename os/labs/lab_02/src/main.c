#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

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
        close(sockets[1]);

        printf("Child send: %s\n", msg);
        write(sockets[0], msg, sizeof(msg));
        read(sockets[0], buf, sizeof(buf));
        printf("Child recieve: %s\n", buf);

        close(sockets[0]);
    }
    else
    {
        // код процесса предка
        char msg[] = "bbbbbbb";
        close(sockets[0]);

        read(sockets[1], buf, sizeof(buf));
        printf("Parent send: %s\n", msg);
        write(sockets[1], msg, sizeof(msg));
        printf("Parent recieve: %s\n", buf);

        close(sockets[1]);
    }

    return EXIT_SUCCESS;
}