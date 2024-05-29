#include <linux/init.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/version.h> // for versions
#include <linux/vmalloc.h>

MODULE_LICENSE("GPL");

#define COOKIE_BUF_SIZE PAGE_SIZE

#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 6, 0)
#define HAVE_PROC_OPS
#endif

static struct proc_dir_entry *fortune_dir;
static struct proc_dir_entry *fortune_file;
static struct proc_dir_entry *fortune_symlink;

static char *cookie_buf = NULL; // буфер в пространстве ядра

char tmp_buf[COOKIE_BUF_SIZE];

unsigned int read_index;
unsigned int write_index;

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

static ssize_t fortune_read(struct file *file, char __user *buf, size_t len, loff_t *fPos)
{
    printk(KERN_INFO "fortune: fortune_read called\n");

    if ((*fPos > 0) || (write_index == 0))
        return 0;

    if (read_index >= write_index)
        read_index = 0;

    int readLen = snprintf(tmp_buf, COOKIE_BUF_SIZE, "%s\n", &cookie_buf[read_index]);

    if (copy_to_user(buf, tmp_buf, readLen) != 0)
    {
        printk(KERN_ERR "fortune: copy_to_user error\n");
        return -EFAULT;
    }

    read_index += readLen;
    *fPos += readLen;

    return readLen;
}

static ssize_t fortune_write(struct file *file, const char __user *buf, size_t len, loff_t *fPos)
{
    printk(KERN_INFO "fortune: fortune_write called\n");

    if (len > COOKIE_BUF_SIZE - write_index + 1)
    {
        printk(KERN_ERR "fortune: [ERROR] [buffer overflow]\n");
        return -ENOSPC;
    }

    if (copy_from_user(&cookie_buf[write_index], buf, len) != 0)
    {
        printk(KERN_ERR "fortune: [ERROR] [can't copy_from_user]\n");
        return -EFAULT;
    }

    write_index += len;
    cookie_buf[write_index - 1] = '\0';

    return len;
}

static int fortune_open(struct inode *spInode, struct file *spFile)
{
    printk(KERN_INFO "fortune: fortune_open called\n");
    return 0;
}

static int fortune_release(struct inode *spInode, struct file *spFile)
{
    printk(KERN_INFO "fortune: fortune_release called\n");
    return 0;
}

#ifdef HAVE_PROC_OPS
static const struct proc_ops fops = {
    .proc_read = fortune_read,
    .proc_write = fortune_write,
    .proc_open = fortune_open,
    .proc_release = fortune_release};

#else
static const struct file_operations fops = {
    .owner = THIS_MODULE,
    .read = fortune_read,
    .write = fortune_write,
    .open = fortune_open,
    .release = fortune_release};
#endif

static int __init md_init(void)
{
    printk(KERN_INFO "fortune: call md_init\n");

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

    read_index = 0;
    write_index = 0;

    printk(KERN_INFO "fortune: loaded\n");

    return 0;
}

static void __exit md_exit(void)
{
    free_all();
    printk(KERN_INFO "fortune: сall md_exit\n");
}

module_init(md_init);
module_exit(md_exit);
