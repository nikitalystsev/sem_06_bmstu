#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

// простейший модуль ядра

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Guru Linux");

static int __init mod_init(void)
{
    printk("Hello, world!\n");

    return 0;
}

static void __exit mod_exit(void)
{
    printk("Goodbye!\n");
}

module_init(mod_init);
module_exit(mod_exit);