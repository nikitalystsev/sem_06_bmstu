#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>

#define PORT 5000

int main(void)
{
    struct sockaddr_in srv_addr;
    int sock;
    char buff_to[256], buff_from[256];
    int bytes_read;

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

    snprintf(buff_to, 256, "child pid = %d", getpid());

    if (send(sock, buff_to, sizeof(buff_to), 0) == -1)
    {
        perror("Ошибка send");
        exit(EXIT_FAILURE);
    }

    printf("Client (pid = %d) send: %s\n", getpid(), buff_to);

    if ((bytes_read = read(sock, buff_from, sizeof(buff_from))) == -1)
    {
        perror("Ошибка read");
        exit(EXIT_FAILURE);
    }

    buff_from[bytes_read] = '\0';

    printf("Client (pid = %d) received: %s\n", getpid(), buff_from);

    close(sock);

    return EXIT_SUCCESS;
}