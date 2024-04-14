#include <linux/init_task.h>
#include <linux/module.h>
#include <linux/sched.h>
#include <linux/fs_struct.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Guru Linux");

static int __init md_init(void)
{
    struct task_struct *task = &init_task;

    do
    {
        printk(KERN_INFO "TASK: state - %5d, on_cpu - %5d, flags - %10d, prio - %5d, policy - %d, migration_flags - %d, exit_code - %d, in_execve - %d, pid - %5d, pcomm - %15s, ppid - %5d, utime - %13d, stime - %13d\n",
               task->__state,
               task->on_cpu,
               task->flags,
               task->prio,
               task->policy,
               task->migration_flags,
               task->exit_code,
               task->in_execve,
               task->pid,
               task->parent->comm,
               task->parent->pid,
               task->utime,
               task->stime);

    } while ((task = next_task(task)) != &init_task);

    printk(KERN_INFO "CURRENT: state - %5d, on_cpu - %5d, flags - %10d, prio - %5d, policy - %d, migration_flags - %d, exit_code - %d, in_execve - %d, pid - %5d, pcomm - %15s, ppid - %5d, utime - %13d, stime - %13d\n",
           current->__state,
           current->on_cpu,
           current->flags,
           current->prio,
           current->policy,
           current->migration_flags,
           current->exit_code,
           current->in_execve,
           current->pid,
           current->parent->comm,
           current->parent->pid,
           current->utime,
           current->stime);

    return 0;
}

static void __exit md_exit(void)
{
    printk(KERN_INFO "TASK_INFO: Good buy!\n");
}

module_init(md_init);
module_exit(md_exit);