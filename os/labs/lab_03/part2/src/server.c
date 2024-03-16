#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>

#define MAX_EVENTS 10
#define BUFF_SIZE 32
#define PORT 5000

int main(void)
{
    struct sockaddr_in srv_addr;
    struct sockaddr cln_addr;
    socklen_t cln_len;
    struct epoll_event ev, events[MAX_EVENTS];
    int listen_sock, conn_sock, nfds, epollfd;
    char buff_to[BUFF_SIZE], buff_from[BUFF_SIZE];
    int rc;

    if ((listen_sock = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("Ошибка socket");
        exit(EXIT_FAILURE);
    }

    srv_addr.sin_family = AF_INET;
    srv_addr.sin_addr = (struct in_addr){.s_addr = INADDR_ANY};
    srv_addr.sin_port = htons(PORT);

    if (bind(listen_sock, (struct sockaddr *)&srv_addr, sizeof(srv_addr)) == -1)
    {
        perror("Ошибка bind");
        close(listen_sock);
        exit(EXIT_FAILURE);
    }

    if (listen(listen_sock, 1) == -1)
    {
        perror("Ошибка listen");
        close(listen_sock);
        exit(EXIT_FAILURE);
    }

    if ((epollfd = epoll_create1(0)) == -1)
    {
        perror("epoll_create1");
        close(listen_sock);
        exit(EXIT_FAILURE);
    }

    ev.events = EPOLLIN;
    ev.data.fd = listen_sock;
    if (epoll_ctl(epollfd, EPOLL_CTL_ADD, listen_sock, &ev) == -1)
    {
        perror("epoll_ctl: listen_sock");
        close(listen_sock);
        exit(EXIT_FAILURE);
    }

    for (;;)
    {
        if ((nfds = epoll_wait(epollfd, events, MAX_EVENTS, -1)) == -1)
        {
            perror("Ошибка epoll_wait");
            close(listen_sock);
            exit(EXIT_FAILURE);
        }

        for (int i = 0; i < nfds; i++)
        {
            if (events[i].data.fd == listen_sock)
            {
                if ((conn_sock = accept(listen_sock, (struct sockaddr *)&cln_addr, &cln_len)) == -1)
                {
                    perror("accept");
                    exit(EXIT_FAILURE);
                }

                ev.events = EPOLLIN | EPOLLET;
                ev.data.fd = conn_sock;

                if (epoll_ctl(epollfd, EPOLL_CTL_ADD, conn_sock, &ev) == -1)
                {
                    perror("epoll_ctl: conn_sock");
                    exit(EXIT_FAILURE);
                }
            }
            else
            {
                buff_to[BUFF_SIZE - 1] = 0;
                buff_from[BUFF_SIZE - 1] = 0;

                if ((rc = read(events[i].data.fd, buff_from, sizeof(buff_from))) == -1)
                {
                    perror("Ошибка read");
                    exit(EXIT_FAILURE);
                }

                printf("\nServer received: %s\n", buff_from);
                sprintf(buff_to, "server pid = %d", getpid());

                if (send(events[i].data.fd, buff_to, sizeof(buff_to), 0) == -1)
                {
                    perror("Ошибка send");
                    exit(EXIT_FAILURE);
                }

                printf("Server send: %s\n", buff_to);

                close(events[i].data.fd);
            }
        }
    }

    close(listen_sock);

    return EXIT_SUCCESS;
}