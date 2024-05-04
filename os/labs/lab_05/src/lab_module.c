#include <linux/dcache.h>
#include <linux/fs_struct.h>
#include <linux/init_task.h>
#include <linux/module.h>
#include <linux/sched.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Guru Linux");

static int __init md_init(void)
{
    struct task_struct *task = &init_task;

    do
    {
        printk(KERN_INFO "TASK: state - %5d, on_cpu - %5d, flags - %10d, prio - %5d, policy - %d, migration_flags - %d, exit_code - %d, exit_state - %d, in_execve - %d, comm - %15s, pid - %5d, pcomm - %15s, ppid - %5d, utime - %13llu, stime - %13llu, root - %s, thread level - %d\n",
               task->__state,
               task->on_cpu,
               task->flags,
               task->prio,
               task->policy,
               task->migration_flags,
               task->exit_code,
               task->exit_state,
               task->in_execve,
               task->comm,
               task->pid,
               task->parent->comm,
               task->parent->pid,
               task->utime,
               task->stime,
               task->fs->root.dentry->d_name.name);

    } while ((task = next_task(task)) != &init_task);

    printk(KERN_INFO "CURR: state - %5d, on_cpu - %5d, flags - %10d, prio - %5d, policy - %d, migration_flags - %d, exit_code - %d, exit_state - %d, in_execve - %d, comm - %15s, pid - %5d, pcomm - %15s, ppid - %5d, utime - %13llu, stime - %13llu, root - %s\n",
           task->__state,
           task->on_cpu,
           task->flags,
           task->prio,
           task->policy,
           task->migration_flags,
           task->exit_code,
           task->exit_state,
           task->in_execve,
           task->comm,
           task->pid,
           task->parent->comm,
           task->parent->pid,
           task->utime,
           task->stime,
           task->fs->root.dentry->d_name.name);

    return 0;
}

static void __exit md_exit(void) {}

module_init(md_init);
module_exit(md_exit);
