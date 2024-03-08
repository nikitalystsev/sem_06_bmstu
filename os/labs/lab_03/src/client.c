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
    struct sockaddr cln_addr;
    char buf[1024], bufAns[1024];
    int bytes_read;

    if ((sock = socket(AF_UNIX, SOCK_DGRAM, 0)) == -1)
    {
        perror("Ошибка socket");
        exit(1);
    }

    cln_addr.sa_family = AF_UNIX;
    strcpy(cln_addr.sa_data, "./test_sock");

    snprintf(buf, 1024, "Client (pid %d) send message", getpid());

    if (sendto(sock, buf, strlen(buf) + 1, 0, &addr, sizeof(addr)) == -1)
    {
        perror("Ошибка sendto");
        exit(1);
    }

    if ((bytes_read = recvfrom(sock, bufAns, 1024, 0, NULL, NULL)) == -1)
    {
        perror("Ошибка recvfrom");
        exit(1);
    }

    bufAns[bytes_read] = '\0';
    printf("Cliend (pid %d) get answer from Server: %s\n", getpid(), buf);

    close(sock);

    return 0;
}
