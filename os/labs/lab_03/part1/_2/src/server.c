#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

int sock;

void signal_handler()
{
    close(sock);
    unlink("./sock.srv");
    exit(EXIT_SUCCESS);
}

int main(void)
{
    struct sockaddr srv_addr, cln_addr;
    char buf[1024], bufAns[1024];
    int bytes_read;
    int addr_size;

    if ((sock = socket(AF_UNIX, SOCK_DGRAM, 0)) == -1)
    {
        perror("Ошибка socket");
        exit(EXIT_FAILURE);
    }

    srv_addr.sa_family = AF_UNIX;
    strcpy(srv_addr.sa_data, "./sock.srv");

    if (bind(sock, &srv_addr, sizeof(srv_addr)))
    {
        perror("Ошибка bind");
        exit(EXIT_FAILURE);
    }

    if (signal(SIGINT, signal_handler) == (void *)-1)
    {
        perror("Ошибка signal");
        exit(EXIT_FAILURE);
    }

    while (1)
    {
        if ((bytes_read = recvfrom(sock, buf, 1024, 0, &cln_addr, &addr_size)) == -1)
        {
            perror("Ошибка recvfrom");
            exit(EXIT_FAILURE);
        }

        buf[bytes_read] = '\0';
        printf("Server receive: %s\n", buf);

        snprintf(bufAns, 1024, "server pid %d", getpid());

        if (sendto(sock, bufAns, sizeof(bufAns), 0, &cln_addr, addr_size) == -1)
        {
            perror("Ошибка sendto");
            exit(EXIT_FAILURE);
        }
    }

    unlink("./sock.srv");

    return EXIT_SUCCESS;
}