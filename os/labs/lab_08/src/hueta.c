#include <linux/module.h>
#include <linux/slab.h>
#include <linux/version.h>
MODULE_LICENSE("GPL");

MODULE_AUTHOR("Oleg Tsiliuric <olej@front.ru>");
MODULE_VERSION("5.2");

static int size = 7; // для наглядности - простые числа
module_param(size, int, 0);
static int number = 31;
module_param(number, int, 0);
static void **line = NULL;
static int sco = 0;
static
#if LINUX_VERSION_CODE > KERNEL_VERSION(2, 6, 31)
    void
    co(void *p)
{
#else
    void
    co(void *p, kmem_cache_t *c, unsigned long f)
{
#endif
    *(int *)p = (int)p;

    sco++;
}
#define SLABNAME "my_cache"
struct kmem_cache *cache = NULL;
static int __init init(void)
{
    int i;
    if (size < sizeof(void *))
    {
        printk(KERN_ERR "invalid argument\n");
        return -EINVAL;
    }
    line = kmalloc(sizeof(void *) * number, GFP_KERNEL);
    if (!line)
    {
        printk(KERN_ERR "kmalloc error\n");
        goto mout;
    }
    for (i = 0; i < number; i++)
        line[i] = NULL;
#if LINUX_VERSION_CODE < KERNEL_VERSION(2, 6, 32)
    cache = kmem_cache_create(SLABNAME, size, 0, SLAB_HWCACHE_ALIGN, co, NULL);
#else
    cache = kmem_cache_create(SLABNAME, size, 0, SLAB_HWCACHE_ALIGN, co);
#endif
    if (!cache)
    {
        printk(KERN_ERR "kmem_cache_create error\n");
        goto cout;
    }
    for (i = 0; i < number; i++)
        if (NULL == (line[i] = kmem_cache_alloc(cache, GFP_KERNEL)))
        {
            printk(KERN_ERR "kmem_cache_alloc error\n");
            goto oout;
        }
    printk(KERN_INFO "allocate %d objects into slab: %s\n", number, SLABNAME);
    printk(KERN_INFO "object size %d bytes, full size %ld bytes\n", size,
           (long)size * number);
    printk(KERN_INFO "constructor called %d times\n", sco);
    return 0;
oout:
    for (i = 0; i < number; i++)
        kmem_cache_free(cache, line[i]);
cout:
    kmem_cache_destroy(cache);
mout:
    kfree(line);
    return -ENOMEM;
}
module_init(init);
static void __exit exit(void)
{
    int i;
    for (i = 0; i < number; i++)
        kmem_cache_free(cache, line[i]);
    kmem_cache_destroy(cache);
    kfree(line);
}
module_exit(exit);