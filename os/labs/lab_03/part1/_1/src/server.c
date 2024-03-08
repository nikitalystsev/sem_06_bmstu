#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/wait.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <inttypes.h>
#include <strings.h>
#include <signal.h>

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

    if (bind(sock, &srv_addr, sizeof(srv_addr)) == -1)
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
    }

    return EXIT_SUCCESS;
}