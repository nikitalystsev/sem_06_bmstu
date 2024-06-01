#include <linux/fs.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/slab.h>
#include <linux/version.h>

MODULE_LICENSE("GPL");

static int limit = 10;

#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
#define HAVE_PROC_OPS
#endif

static struct proc_dir_entry *seq_dir;
static struct proc_dir_entry *seq_file;
static struct proc_dir_entry *seq_symlink;

static void free_all(void)
{
    if (seq_symlink != NULL)
        remove_proc_entry("seq_symlink", NULL);

    if (seq_file != NULL)
        remove_proc_entry("seq_file", seq_dir);

    if (seq_dir != NULL)
        remove_proc_entry("seq_dir", NULL);
}

/**
 * start
 */
static void *ct_seq_start(struct seq_file *s, loff_t *pos)
{
    printk(KERN_INFO "seq: call seq_start");

    if (*pos >= limit)
    { // are we done?
        printk(KERN_INFO "Apparently, we're done.\n");
        return NULL;
    }

    // Выделяем память для числа
    loff_t *spos = kmalloc(sizeof(loff_t), GFP_KERNEL);

    if (!spos)
        return NULL;

    seq_printf(s, "current:\ncomm - %s\npid - %d\nparent comm - %s\nppid - %d\nstate - %d\non_cpu - %d\nflags - %x\nprio - %d\npolicy - %d\nexit_state - %d\nexit_code - %d\nin_execve - %x\nutime - %llu\n",
               current->comm,
               current->pid,
               current->parent->comm,
               current->parent->pid,
               current->__state,
               current->on_cpu,
               current->flags,
               current->prio,
               current->policy,
               current->exit_state,
               current->exit_code,
               current->in_execve,
               current->utime);

    *spos = *pos;
    return spos;
}

/**
 * show
 */
static int ct_seq_show(struct seq_file *s, void *v)
{
    printk(KERN_INFO "seq: call seq_show");

    loff_t *spos = v;
    seq_printf(s, "%lld \n", (long long)*spos);

    return 0;
}

/**
 * next
 */
static void *ct_seq_next(struct seq_file *s, void *v, loff_t *pos)
{
    printk(KERN_INFO "seq: call seq_next");

    loff_t *spos = v;
    *pos = ++*spos;

    if (*pos >= limit) // заканчиваем?
        return NULL;

    return v;
}

/**
 * stop
 */
static void ct_seq_stop(struct seq_file *s, void *v)
{
    printk(KERN_INFO "seq: call seq_stop");

    kfree(v);
}

/**
 * Эта структура собирает функции для управления последовательным чтением
 */
static struct seq_operations ct_seq_ops = {
    .start = ct_seq_start,
    .next = ct_seq_next,
    .stop = ct_seq_stop,
    .show = ct_seq_show};

/**
 * Эта функция вызывается при открытии файла из /proc
 */
static int ct_seq_open(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "seq: call seq_open\n");

    return seq_open(file, &ct_seq_ops);
};

static ssize_t ct_seq_read(struct file *file, char __user *buf, size_t size, loff_t *ppos)
{
    printk(KERN_INFO "seq: call seq_read\n");

    return seq_read(file, buf, size, ppos);
}

static int ct_seq_release(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "seq: call seq_release\n");

    return seq_release(inode, file);
}

static loff_t ct_seq_lseek(struct file *file, loff_t offset, int whence)
{
    printk(KERN_INFO "seq: call seq_lseek\n");

    return seq_lseek(file, offset, whence);
}

/**
 * Эта структура собирает функции для управления файлом из /proc
 */
#ifdef HAVE_PROC_OPS
static const struct proc_ops ct_file_ops = {
    .proc_read = ct_seq_read,
    .proc_open = ct_seq_open,
    .proc_release = ct_seq_release,
    .proc_lseek = ct_seq_lseek};
#else
static struct file_operations ct_file_ops = {
    .owner = THIS_MODULE,
    .open = ct_seq_open,
    .read = ct_seq_read,
    .llseek = ct_seq_lseek,
    .release = ct_seq_release};
#endif

/**
 * Эта функция вызывается, когда этот модуль загружается в ядро
 */
static int __init ct_init(void)
{
    printk(KERN_INFO "seq: call ct_init\n");

    if ((seq_dir = proc_mkdir("seq_dir", NULL)) == NULL)
    {
        free_all();
        printk(KERN_ERR "seq: [ERROR] [can't create fortune dir]\n");

        return -ENOMEM;
    }

    if ((seq_file = proc_create("seq_file", 0666, seq_dir, &ct_file_ops)) == NULL)
    {
        free_all();
        printk(KERN_ERR "seq: [ERROR] [can't create fortune file]\n");

        return -ENOMEM;
    }

    if ((seq_symlink = proc_symlink("seq_symlink", NULL, "seq_dir/seq_file")) == NULL)
    {
        free_all();
        printk(KERN_ERR "seq: [ERROR] [can't create fortune symlink]\n");

        return -ENOMEM;
    }

    printk(KERN_INFO "seq: loaded\n");

    return 0;
}

/**
 * Эта функция вызывается, когда этот модуль удаляют из ядра
 */
static void __exit ct_exit(void)
{
    free_all();

    printk(KERN_INFO "seq: сall md_exit\n");
}

module_init(ct_init);
module_exit(ct_exit);
