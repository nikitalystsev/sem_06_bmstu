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

static void *ct_seq_start(struct seq_file *s, loff_t *pos)
{
    printk(KERN_INFO "Entering start(), *pos = %Ld, seq-file pos = %lu.\n",
           *pos, s->count);

    printk(KERN_INFO "sizeof(loff_t) = %lu\n", sizeof(loff_t));

    if (*pos >= limit)
    { // are we done?
        printk(KERN_INFO "Apparently, we're done.\n");
        return NULL;
    }

    loff_t *spos = kmalloc(sizeof(loff_t), GFP_KERNEL);
    if (!spos)
        return NULL;

    printk(KERN_INFO "In start(), spos = %pX.\n", spos);

    *spos = *pos;
    return spos;
}

static void *ct_seq_next(struct seq_file *s, void *v, loff_t *pos)
{
    printk(KERN_INFO "In next(), v pointer = %pX, v = %d, pos = %Ld, seq-file pos = %lu.\n",
           v, *(int *)v, *pos, s->count);

    loff_t *spos = v;
    *pos = ++*spos;

    if (*pos >= limit) // заканчиваем?
        return NULL;

    return spos;
}

static void ct_seq_stop(struct seq_file *s, void *v)
{
    printk(KERN_INFO "Entering stop().\n");

    kfree(v);
}

static int ct_seq_show(struct seq_file *s, void *v)
{
    printk(KERN_INFO "In show(), v = %d, seq-file pos = %lu.\n", *(int *)v, s->count);

    loff_t *spos = v;
    seq_printf(s, "%lld \n", (long long)*spos);
    return 0;
}

static const struct seq_operations ct_seq_ops = {
    .start = ct_seq_start,
    .next = ct_seq_next,
    .stop = ct_seq_stop,
    .show = ct_seq_show};

static int ct_open(struct inode *inode, struct file *file)
{
    return seq_open(file, &ct_seq_ops);
};

static const struct proc_ops ct_file_ops = {
    .proc_read = seq_read,
    .proc_open = ct_open,
    .proc_release = seq_release,
    .proc_lseek = seq_lseek};

/**
 * Эта функция вызывается, когда этот модуль загружается в ядро
 */
static int __init ct_init(void)
{
    proc_create("my_seqfile", 0, NULL, &ct_file_ops);
    return 0;
}

/**
 * Эта функция вызывается, когда этот модуль удаляют из ядра
 */
static void __exit ct_exit(void)
{
    remove_proc_entry("my_seqfile", NULL);
}

module_init(ct_init);
module_exit(ct_exit);
