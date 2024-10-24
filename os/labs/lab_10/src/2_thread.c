#include <fcntl.h>
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void *thread_start(void *arg)
{
    int *fd = arg;
    char c;

    while (read(*fd, &c, 1))
        write(1, &c, 1);

    return NULL;
}

int main()
{
    int fd[2] = {open("alphabet.txt", O_RDONLY),
                 open("alphabet.txt", O_RDONLY)};
    pthread_t thr[2];

    for (int i = 0; i < 2; i++)
        if (pthread_create(&thr[i], NULL, thread_start, &fd[i]))
        {
            perror("pthread_create");
            return 1;
        }

    for (int i = 0; i < 2; i++)
        if (pthread_join(thr[i], NULL))
        {
            perror("pthread_join");
            return 1;
        }

    close(fd[0]);
    close(fd[1]);

    return 0;
}
