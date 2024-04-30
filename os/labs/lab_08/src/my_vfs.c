#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/init_task.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/time.h>

MODULE_LICENSE("GPL");

#define MYFS_MAGIC_NUMBER 0x13131313

struct myfs_inode
{
    int i_mode;
    unsigned long i_ino;
} myfs_inode;

static void myfs_put_super(struct super_block *sb)
{
    printk(KERN_DEBUG "MYFS super block destroyed!\n");
}

static struct super_operations const myfs_super_ops = {
    .put_super = myfs_put_super,
    .statfs = simple_statfs,
    .drop_inode = generic_delete_inode,
};

static struct inode *myfs_make_inode(struct super_block *sb, int mode)
{
    struct inode *ret = new_inode(sb);
    if (ret)
    {
        inode_init_owner(&nop_mnt_idmap, ret, NULL, mode);
        ret->i_size = PAGE_SIZE;
        ret->i_atime = ret->i_mtime = ret->i_ctime = current_time(ret);
        ret->i_private = &myfs_inode;
    }

    return ret;
}

static int myfs_fill_sb(struct super_block *sb, void *data, int silent)
{
    struct inode *root = NULL;

    sb->s_blocksize = PAGE_SIZE;
    sb->s_blocksize_bits = PAGE_SHIFT;
    sb->s_magic = MYFS_MAGIC_NUMBER;
    sb->s_op = &myfs_super_ops;

    root = myfs_make_inode(sb, S_IFDIR | 0755);
    if (!root)
    {
        printk(KERN_ERR "MYFS inode allocation failed !\n");
        return -ENOMEM;
    }

    root->i_op = &simple_dir_inode_operations;
    root->i_fop = &simple_dir_operations;

    sb->s_root = d_make_root(root);
    if (!sb->s_root)
    {
        printk(KERN_ERR " MYFS root creation failed !\n");
        iput(root);
        return -ENOMEM;
    }

    return 0;
}

static struct dentry *myfs_mount(struct file_system_type *type, int flags, char const *dev, void *data)
{
    struct dentry *const entry = mount_nodev(type, flags, data, myfs_fill_sb);

    if (IS_ERR(entry))
        printk(KERN_ERR "MYFS mounting failed !\n");
    else
        printk(KERN_DEBUG "MYFS mounted!\n");

    return entry;
}

static struct file_system_type myfs_type = {
    .owner = THIS_MODULE,
    .name = "myfs", // название файловой системы
    .mount = myfs_mount,
    .kill_sb = kill_block_super,
};

static int __init myfs_init(void)
{
    int ret = register_filesystem(&myfs_type);
    if (ret != 0)
    {
        printk(KERN_ERR "MYFS_MODULE cannot register filesystem!\n");
        return ret;
    }
    printk(KERN_DEBUG "MYFS_MODULE loaded !\n");
    return 0;
}

static void __exit myfs_exit(void)
{
    int ret = unregister_filesystem(&myfs_type);

    if (ret != 0)
    {
        printk(KERN_ERR "MYFS_MODULE cannot unregister filesystem !\n");
        return;
    }

    printk(KERN_DEBUG "MYFS_MODULE unloaded !\n");
}

module_init(myfs_init);
module_exit(myfs_exit);
