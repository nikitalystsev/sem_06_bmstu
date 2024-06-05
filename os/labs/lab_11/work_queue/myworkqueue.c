#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/interrupt.h>
#include <linux/slab.h>
#include <asm/io.h>
#include <linux/stddef.h>
#include <linux/workqueue.h>
#include <linux/delay.h>

#include "ascii.h"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Yusupov F");

typedef struct
{
    struct work_struct work;
    int code;
} my_work_struct_t;

static struct workqueue_struct *interrupt_2;

static my_work_struct_t *work1;
static my_work_struct_t *work2;

int keyboard_irq = 1;

void work1_func(struct work_struct *work)
{
    my_work_struct_t *my_work = (my_work_struct_t *)work;
    int code = my_work->code;

    printk(KERN_INFO "MyWorkQueue: work1 begin");

    if (code < 84)
        printk(KERN_INFO "MyWorkQueue: work1 the key is %s", ascii[code]);

    printk(KERN_INFO "MyWorkQueue: work1 end");
}

void work2_func(struct work_struct *work)
{
    my_work_struct_t *my_work = (my_work_struct_t *)work;
    int code = my_work->code;

    printk(KERN_INFO "MyWorkQueue: work2 begin");
    if (code < 84)
    {
        printk(KERN_INFO "+ MyWorkQueue: work2: time = %llu", ktime_get());
        msleep(10);
        printk(KERN_INFO "MyWorkQueue: work2 the key is %s", ascii[code]);
    }
    printk(KERN_INFO "MyWorkQueue: work2 end");
}

irqreturn_t my_irq_handler(int irq, void *dev)
{
    int code;
    printk(KERN_INFO "MyWorkQueue: my_irq_handler");

    code = inb(0x60);
    work1->code = code;
    work2->code = code;

    if (irq == keyboard_irq)
    {
        // printk(KERN_INFO "MyWorkQueue: called by keyboard_irq");
        // printk(KERN_INFO "MyWorkQueue: key code is %d", code);

        queue_work(interrupt_2, (struct work_struct *)work1);
        queue_work(interrupt_2, (struct work_struct *)work2);

        return IRQ_HANDLED;
    }

    printk(KERN_INFO "MyWorkQueue: called not by keyboard_irq");

    return IRQ_NONE;
}

static int __init my_workqueue_init(void)
{
    int ret;

    ret = request_irq(keyboard_irq, my_irq_handler, IRQF_SHARED,
                      "test_my_irq_handler", (void *) my_irq_handler);

    printk(KERN_INFO "MyWorkQueue: init");
    if (ret)
    {
        printk(KERN_ERR "MyWorkQueue: request_irq error");
        return ret;
    }
    else
    {
        interrupt_2 = alloc_workqueue("%s", __WQ_LEGACY | WQ_MEM_RECLAIM, 1, "interrupt_2");

        if  (interrupt_2 == NULL)
        {
            printk(KERN_ERR "MyWorkQueue: create queue error");
            return -ENOMEM;
        }

        work1 = kmalloc(sizeof(my_work_struct_t), GFP_KERNEL);
        if (work1 == NULL)
        {
            printk(KERN_ERR "MyWorkQueue: work1 alloc error");
            destroy_workqueue(interrupt_2);
            return -ENOMEM;
        }

        work2 = kmalloc(sizeof(my_work_struct_t), GFP_KERNEL);
        if (work2 == NULL)
        {
            printk(KERN_ERR "MyWorkQueue: work2 alloc error");
            destroy_workqueue(interrupt_2);
            kfree(work1);
            return -ENOMEM;
        }

        INIT_WORK((struct work_struct *)work1, work1_func);
        INIT_WORK((struct work_struct *)work2, work2_func);
        printk(KERN_INFO "MyWorkQueue: loaded");
    }
    return 0;
}

static void __exit my_workqueue_exit(void)
{
    printk(KERN_INFO "MyWorkQueue: exit");

    synchronize_irq(keyboard_irq); // ожидание завершения обработчика
    free_irq(keyboard_irq, my_irq_handler); // освобождение линии от обработчика

    flush_workqueue(interrupt_2);
    destroy_workqueue(interrupt_2);
    kfree(work1);
    kfree(work2);
    
    printk(KERN_INFO "MyWorkQueue: unloaded");
}

module_init(my_workqueue_init);
module_exit(my_workqueue_exit);
