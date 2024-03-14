#define _GNU_SOURCE

#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>
#include <fcntl.h>

#define MAX_EVENTS 4
#define BUFF_SIZE 32

int main(void)
{
    int port = 5000;

    struct sockaddr_in srv_addr;
    struct sockaddr client_addr;
    socklen_t client_len;
    struct epoll_event ev, events[MAX_EVENTS];
    int listen_sock, conn_sock, nfds, epollfd;
    int conn;
    char msg_to[BUFF_SIZE], msg_from[BUFF_SIZE];
    int rc;

    if ((listen_sock = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("Ошибка socket");
        exit(EXIT_FAILURE);
    }

    srv_addr.sin_family = AF_INET;
    srv_addr.sin_addr = (struct in_addr){.s_addr = INADDR_ANY};
    srv_addr.sin_port = htons(port);

    if (bind(listen_sock, (struct sockaddr *)&srv_addr, sizeof(srv_addr)) == -1)
    {
        perror("Ошибка bind");
        close(listen_sock);
        exit(EXIT_FAILURE);
    }

    if (listen(listen_sock, MAX_EVENTS) == -1)
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

    printf("server_pid: %d\n", getpid());

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
                if ((conn_sock = accept(listen_sock, (struct sockaddr *)&client_addr, &client_len)) == -1)
                {
                    perror("accept");
                    exit(EXIT_FAILURE);
                }

                ev.events = EPOLLIN | EPOLLET;
                ev.data.fd = conn_sock;

                if (epoll_ctl(epollfd, EPOLL_CTL_ADD, conn_sock, &ev) == -1)
                {
                    perror("epoll_ctl: conn_sock");
                    close(listen_sock);
                    exit(EXIT_FAILURE);
                }
            }
            else
            {
                conn = events[i].data.fd;

                msg_to[BUFF_SIZE - 1] = 0;
                msg_from[BUFF_SIZE - 1] = 0;

                if ((rc = read(conn, msg_from, sizeof(msg_from))) == -1)
                {
                    perror("Ошибка read");
                    close(conn);
                    exit(EXIT_FAILURE);
                }

                printf("\nServer received: %s\n", msg_from);
                sprintf(msg_to, "%d_%s", getpid(), msg_from);

                if (send(conn, msg_to, sizeof(msg_to), 0) == -1)
                {
                    perror("Ошибка send");
                    exit(EXIT_FAILURE);
                }

                printf("Server send: %s\n", msg_to);

                close(conn);
            }
        }
    }
}