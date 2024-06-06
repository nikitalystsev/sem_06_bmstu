  for (int i = 0; i < 2; i++)
  {
    targ[i].fd = fd[i];
    targ[i].i = i;
    if (pthread_create(&thr[i], NULL, thread_start, &targ[i]))
    {
      perror("pthread_create");
      return 1;
    }
  }
  close(fd[0]);
  close(fd[1]);
  return 0;
}