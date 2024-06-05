#include <linux/fs.h>
#include <linux/init.h>
#include <linux/init_task.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/time.h>

MODULE_LICENSE("GPL");

#define MYFS_MAGIC_NUMBER 0x13131313
#define SLABNAME "myfsCache" // имя slab кэша

// переменные, связанные с кэшем
struct kmem_cache *cache = NULL; // slab кэш, наверное
static void **line = NULL;
static int sco = 0;
static int number = 10; // типа сколько кирпичиков?
static int size = 7;    // для наглядности - простые числа

struct myfs_inode
{
    int i_mode;
    unsigned long i_ino;
} myfs_inode;

void co(void *p)
{
    *(int *)p = (int)p;
    sco++;
}

static void myfs_put_super(struct super_block *sb)
{
    printk(KERN_INFO "+ myfs: call myfs_put_super\n");
}

static int myfs_statfs(struct dentry *dentry, struct kstatfs *buf)
{
    printk(KERN_INFO "+ myfs: call myfs_statfs\n");

    return simple_statfs(dentry, buf);
}

int myfs_delete_inode(struct inode *inode)
{
    printk(KERN_INFO "+ myfs: call myfs_delete_inode\n");

    return generic_delete_inode(inode);
}

static struct super_operations const myfs_super_ops = {
    .put_super = myfs_put_super,
    .statfs = myfs_statfs,
    .drop_inode = myfs_delete_inode,
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
    printk(KERN_INFO "+ myfs: call myvfs_fill_super\n");

    struct inode *root = NULL;

    sb->s_blocksize = PAGE_SIZE;
    sb->s_blocksize_bits = PAGE_SHIFT;
    sb->s_magic = MYFS_MAGIC_NUMBER;
    sb->s_op = &myfs_super_ops;

    root = myfs_make_inode(sb, S_IFDIR | 0755);
    if (!root)
    {
        printk(KERN_ERR "+ myfs: inode allocation failed !\n");
        return -ENOMEM;
    }

    root->i_ino = 1;
    root->i_mode = S_IFDIR | 0755;
    root->i_ctime = inode->i_mtime = inode->i_atime = current_time(inode);
    root->i_op = &simple_dir_inode_operations;
    root->i_fop = &simple_dir_operations;
    set_nlink(inode, 2);

    sb->s_root = d_make_root(root);
    if (!sb->s_root)
    {
        printk(KERN_ERR "+ myfs: root creation failed !\n");
        iput(root);
        return -ENOMEM;
    }

    return 0;
}

static struct dentry *myfs_mount(struct file_system_type *type, int flags, char const *dev, void *data)
{
    struct dentry *const entry = mount_nodev(type, flags, data, myfs_fill_sb);

    if (IS_ERR(entry))
        printk(KERN_ERR "+ myfs: mounting failed !\n");
    else
        printk(KERN_DEBUG "+ myfs: mounted!\n");

    return entry;
}

static void myfs_kill_super(struct super_block *sb)
{
    printk(KERN_INFO "+ myfs: call myfs_kill_super\n");

    kill_anon_super(sb);
}

static struct file_system_type myfs_type = {
    .owner = THIS_MODULE,
    .name = "myfs", // название файловой системы
    .mount = myfs_mount,
    .kill_sb = myfs_kill_super,
};

static int __init myfs_init(void)
{
    int ret = register_filesystem(&myfs_type);
    if (ret != 0)
    {
        printk(KERN_ERR "+ myfs: cannot register filesystem!\n");
        return ret;
    }

    line = kmalloc(sizeof(void *) * number, GFP_KERNEL);
    if (!line)
    {
        printk(KERN_ERR "+ myfs: kmalloc error\n");
        goto mout;
    }

    cache = kmem_cache_create(SLABNAME, size, 0, SLAB_HWCACHE_ALIGN, co);
    if (!cache)
    {
        printk(KERN_ERR "+ myfs: kmem_cache_create error\n");
        goto cout;
    }

    for (int i = 0; i < number; i++)
        if (NULL == (line[i] = kmem_cache_alloc(cache, GFP_KERNEL)))
        {
            printk(KERN_ERR "+ myfs: kmem_cache_alloc error\n");
            goto oout;
        }

    printk(KERN_INFO "+ myfs: allocate %d objects into slab: %s\n", number, SLABNAME);
    printk(KERN_INFO "+ myfs: object size %d bytes, full size %ld bytes\n", size, (long)size * number);
    printk(KERN_INFO "+ myfs: constructor called %d times\n", sco);

    printk(KERN_DEBUG "+ myfs: myfs_module loaded !\n");

    return 0;
oout:
    for (int i = 0; i < number; i++)
        kmem_cache_free(cache, line[i]);
cout:
    kmem_cache_destroy(cache);
mout:
    kfree(line);

    return -ENOMEM;
}

static void __exit myfs_exit(void)
{
    int ret = unregister_filesystem(&myfs_type);

    if (ret != 0)
    {
        printk(KERN_ERR "+ myfs: cannot unregister filesystem !\n");
        return;
    }

    for (int i = 0; i < number; i++)
        kmem_cache_free(cache, line[i]);
    kmem_cache_destroy(cache);
    kfree(line);

    printk(KERN_DEBUG "+ myfs: unloaded !\n");
}

module_init(myfs_init);
module_exit(myfs_exit);
