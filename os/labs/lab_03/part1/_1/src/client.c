#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>

int main(void)
{
    int sock;
    struct sockaddr srv_addr;
    char buf[1024];
    int bytes_read;

    if ((sock = socket(AF_UNIX, SOCK_DGRAM, 0)) == -1)
    {
        perror("Ошибка socket");
        exit(EXIT_FAILURE);
    }

    srv_addr.sa_family = AF_UNIX;
    sprintf(srv_addr.sa_data, "./sock.srv");

    snprintf(buf, 1024, "client pid = %d", getpid());

    if (sendto(sock, buf, strlen(buf) + 1, 0, &srv_addr, sizeof(srv_addr)) == -1)
    {
        perror("Ошибка sendto");
        exit(EXIT_FAILURE);
    }

    close(sock);

    return EXIT_SUCCESS;
}
