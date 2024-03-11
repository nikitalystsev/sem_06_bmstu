#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>

int main(void)
{
    int sock;
    struct sockaddr cln_addr, srv_addr;
    char buf[1024], bufAns[1024];
    int bytes_read;
    int addr_size;

    if ((sock = socket(AF_UNIX, SOCK_DGRAM, 0)) == -1)
    {
        perror("Ошибка socket");
        exit(EXIT_FAILURE);
    }

    cln_addr.sa_family = AF_UNIX;
    sprintf(cln_addr.sa_data, "./%d.cln", getpid());

    if (bind(sock, &cln_addr, sizeof(cln_addr)))
    {
        perror("Ошибка bind");
        exit(EXIT_FAILURE);
    }

    srv_addr.sa_family = AF_UNIX;
    sprintf(srv_addr.sa_data, "./sock.srv");

    snprintf(buf, 1024, "%d", getpid());

    if (sendto(sock, buf, strlen(buf) + 1, 0, &srv_addr, sizeof(srv_addr)) == -1)
    {
        perror("Ошибка sendto");
        exit(EXIT_FAILURE);
    }

    if ((bytes_read = recvfrom(sock, bufAns, 1024, 0, &srv_addr, &addr_size)) == -1)
    {
        perror("Ошибка recvfrom");
        exit(EXIT_FAILURE);
    }

    bufAns[bytes_read] = '\0';

    printf("Cliend (pid %d) receive from Server: %s\n", getpid(), bufAns);

    unlink(cln_addr.sa_data);
    close(sock);

    return EXIT_SUCCESS;
}
