#include <fcntl.h>
#include <unistd.h>
#include <pthread.h>
#include <stdio.h>
#include <sys/stat.h>
struct stat statbuf;
#define PRINT_STAT(action, i) \
  do { \
    stat("q.txt", &statbuf); \
    fprintf(stdout, action " %d: inode number = %ld, size = %ld bytes\n", \
      i, statbuf.st_ino, statbuf.st_size); \
  } while (0);
struct thread_arg {
  int fd;
  int i;
};
void *thread_start(void *arg)
{
  struct thread_arg *targ = arg;
  for (char c = 'a'; c <= 'z'; c++)
    if (c % 2 == targ->i)
    {
      write(targ->fd, &c, 1);
      PRINT_STAT("write", targ->i);
    }
  return NULL;
}
int main()
{
  int fd[2] = {open("q.txt", O_RDWR),
               open("q.txt", O_RDWR)};
  pthread_t thr[2];
  struct thread_arg targ[2];
