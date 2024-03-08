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

int main(void)
{
    int sock;
    struct sockaddr addr;
    char buf[1024];
    int bytes_read;

    if ((sock = socket(AF_UNIX, SOCK_DGRAM, 0)) == -1)
    {
        perror("Ошибка socket");
        exit(1);
    }

    addr.sa_family = AF_UNIX;
    strcpy(addr.sa_data, "./test_sock");

    if (bind(sock, &addr, sizeof(addr)))
    {
        perror("Ошибка bind");
        exit(1);
    }

    while (1)
    {
        if ((bytes_read = recvfrom(sock, buf, 1024, 0, NULL, NULL)) == -1)
        {
            perror("Ошибка recvfrom");
            exit(1);
        }

        buf[bytes_read] = '\0';
        printf("Server get message: %s\n", buf);

        sleep(1);
    }

    close(sock);

    return 0;
}