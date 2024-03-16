#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

#define BUFF_SIZE 32
#define PORT 5000

int main(void)
{
    struct sockaddr_in srv_addr;
    int sock;
    char buff_to[BUFF_SIZE], buff_from[BUFF_SIZE];

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == 1)
    {
        perror("Ошибка sock");
        exit(EXIT_FAILURE);
    }

    srv_addr.sin_family = AF_INET;
    srv_addr.sin_port = htons(PORT);

    if (connect(sock, (struct sockaddr *)&srv_addr, sizeof(srv_addr)) == -1)
    {
        perror("Ошибка connect");
        exit(EXIT_FAILURE);
    }

    buff_to[BUFF_SIZE - 1] = 0;
    buff_from[BUFF_SIZE - 1] = 0;

    sprintf(buff_to, "child pid = %d", getpid());

    if (send(sock, buff_to, BUFF_SIZE, 0) == -1)
    {
        perror("Ошибка send");
        exit(EXIT_FAILURE);
    }

    printf("Client (pid = %d) send: %s\n", getpid(), buff_to);

    if (read(sock, buff_from, BUFF_SIZE) == -1)
    {
        perror("Ошибка read");
        exit(EXIT_FAILURE);
    }

    printf("Client (pid = %d) received: %s\n", getpid(), buff_from);

    close(sock);

    return 0;
}