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

    if ((sock = socket(AF_UNIX, SOCK_DGRAM, 0)) == -1)
    {
        perror("Ошибка socket");
        exit(1);
    }

    addr.sa_family = AF_UNIX;
    strcpy(addr.sa_data, "./test_sock");

    char buf[128];
    snprintf(buf, 128, "Client (pid %d) send message", getpid());

    if (sendto(sock, buf, strlen(buf) + 1, 0, &addr, sizeof(addr)) == -1)
    {
        perror("Ошибка sendto");
        exit(1);
    }

    close(sock);

    return 0;
}
