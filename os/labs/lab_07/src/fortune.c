#include <linux/init.h>
#include <linux/module.h>
#include <linux/vmalloc.h>
#include <linux/proc_fs.h>

MODULE_LICENSE("GPL");

#define COOKIE_BUF_SIZE PAGE_SIZE

static struct proc_dir_entry *fortune_dir;
static struct proc_dir_entry *fortune_file;
static struct proc_dir_entry *fortune_symlink;

static char *cookie_buf = NULL;

char tmp_buf[COOKIE_BUF_SIZE];

static int read_ind = 0;
static int write_ind = 0;

static void free_all(void)
{
    if (fortune_symlink != NULL)
        remove_proc_entry("fortune_symlink", NULL);

    if (fortune_file != NULL)
        remove_proc_entry("fortune_file", fortune_dir);

    if (fortune_dir != NULL)
        remove_proc_entry("fortune_dir", NULL);

    vfree(cookie_buf);
}

static int fortune_open(struct inode *spInode, struct file *spFile)
{
    printk(KERN_INFO "fortune: open called\n");
    return 0;
}

static int fortune_release(struct inode *spInode, struct file *spFile)
{
    printk(KERN_INFO "fortune: release called\n");
    return 0;
}

static ssize_t fortune_write(struct file *file, const char __user *buf, size_t len, loff_t *fPos)
{
    printk(KERN_INFO "fortune: write called\n");

    if (len > COOKIE_BUF_SIZE - write_ind + 1)
    {
        printk(KERN_ERR "fortune: buffer overflow\n");
        return -ENOSPC;
    }

    if (copy_from_user(&cookie_buf[write_ind], buf, len) != 0)
    {
        printk(KERN_ERR "fortune: [ERROR] [can't copy_from_user]\n");
        return -EFAULT;
    }

    write_ind += len;
    cookie_buf[write_ind - 1] = '\0';

    return len;
}

static ssize_t fortune_read(struct file *file, char __user *buf, size_t len, loff_t *fPos)
{
    int readLen;

    printk(KERN_INFO "fortune: read called\n");

    if ((*fPos > 0) || (write_ind == 0))
        return 0;

    if (read_ind >= write_ind)
        read_ind = 0;

    readLen = snprintf(tmp_buf, COOKIE_BUF_SIZE, "%s\n", &cookie_buf[read_ind]);

    if (copy_to_user(buf, tmp_buf, readLen) != 0)
    {
        printk(KERN_ERR "fortune: copy_to_user error\n");
        return -EFAULT;
    }

    read_ind += readLen;
    *fPos += readLen;

    return readLen;
}

static const struct proc_ops fops = {
    .proc_open = fortune_open,
    .proc_read = fortune_read,
    .proc_write = fortune_write,
    .proc_release = fortune_release};

static int __init md_init(void)
{
    printk(KERN_INFO "fortune: init\n");

    cookie_buf = vmalloc(COOKIE_BUF_SIZE);
    if (!cookie_buf)
    {
        printk(KERN_INFO "fortune: [ERROR] [can't malloc cookie buffer]\n");
        return -ENOMEM;
    }

    memset(cookie_buf, 0, COOKIE_BUF_SIZE);

    if ((fortune_dir = proc_mkdir("fortune_dir", NULL)) == NULL)
    {
        free_all();
        printk(KERN_ERR "fortune: [ERROR] [can't create fortune dir]\n");

        return -ENOMEM;
    }

    if ((fortune_file = proc_create("fortune_file", 0666, fortune_dir, &fops)) == NULL)
    {
        free_all();
        printk(KERN_ERR "fortune: [ERROR] [can't create fortune file]\n");

        return -ENOMEM;
    }

    if ((fortune_symlink = proc_symlink("fortune_symlink", NULL, "fortune_dir/fortune_file")) == NULL)
    {
        free_all();
        printk(KERN_ERR "fortune: [ERROR] [can't create fortune symlink]\n");

        return -ENOMEM;
    }

    read_ind = 0;
    write_ind = 0;

    printk(KERN_INFO "fortune: loaded\n");

    return 0;
}

static void __exit md_exit(void)
{
    free_all();
    printk(KERN_INFO "fortune: exit\n");
}

module_init(md_init);
module_exit(md_exit);
