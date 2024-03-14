#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

#define BUFF_SIZE 32

int main()
{
    int port = 5000;
    struct sockaddr_in srv_addr;
    int sock;
    char msg_to[BUFF_SIZE], msg_from[BUFF_SIZE];

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == 1)
    {
        perror("Ошибка sock");
        exit(EXIT_FAILURE);
    }

    srv_addr.sin_family = AF_INET;
    srv_addr.sin_port = htons(port);

    if (connect(sock, &srv_addr, sizeof(srv_addr)) == -1)
    {
        perror("Ошибка connect");
        exit(EXIT_FAILURE);
    }

    msg_to[BUFF_SIZE - 1] = 0;
    msg_from[BUFF_SIZE - 1] = 0;

    sprintf(msg_to, "%d", getpid());

    if (send(sock, msg_to, BUFF_SIZE, 0) == -1)
    {
        perror("Ошибка send");
        exit(EXIT_FAILURE);
    }

    printf("Client (pid = %d) send: %s\n", getpid(), msg_to);

    if (read(sock, msg_from, BUFF_SIZE) == -1)
    {
        perror("Ошибка read");
        exit(EXIT_FAILURE);
    }

    printf("Client (pid  = %d) received: %s\n", getpid(), msg_from);

    close(sock);

    return 0;
}