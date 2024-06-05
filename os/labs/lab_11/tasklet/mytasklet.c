#include <linux/interrupt.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <linux/time.h>
#include <asm/io.h>
#include "ascii.h"
#define IRQ_NUM 1

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Yusupov F");

char *my_tasklet_data = "interrupt_1 data";
struct tasklet_struct* interrupt_1;


void my_tasklet_function(unsigned long data)
{
    printk( ">> interrupt_1: Bottom-half handled time=%llu\n", ktime_get());
    int code = interrupt_1->data;
    if (interrupt_1->data < 84)
        printk(">> interrupt_1: Key is %s\n", ascii[code]);
    printk(">> interrupt_1: ------------------------------------\n");
}

irqreturn_t my_handler(int irq, void *dev)
{
    printk(">> interrupt_1: Top-half start time=%llu\n", ktime_get());
    int code;
    if (irq == IRQ_NUM)
    {
        code = inb(0x60);
        interrupt_1->data = code;
        printk(">> interrupt_1: Key code is %d\n", code);
        tasklet_schedule(interrupt_1);
		printk(">> interrupt_1: Bottom-half sheduled time=%llu\n", ktime_get());
        return IRQ_HANDLED;
    }
    printk(">> interrupt_1: irq wasn't handled\n");
    return IRQ_NONE;
}

static int __init my_init(void)
{
    if (request_irq(IRQ_NUM, my_handler, IRQF_SHARED, "interrupt_1", &my_handler))
    {
        printk(">> interrupt_1: ERROR request_irq\n");
        return -1;
    }
    interrupt_1 = kmalloc(sizeof(struct tasklet_struct), GFP_KERNEL);
    if (!interrupt_1)
    {
        printk(">> interrupt_1: ERROR kmalloc!\n");
        return -1;
    }
    tasklet_init(interrupt_1, my_tasklet_function, (unsigned long)my_tasklet_data);

    printk(">> interrupt_1: module loaded\n");
    return 0;
}

static void __exit my_exit(void)
{
    tasklet_kill(interrupt_1);
    kfree(interrupt_1);
    free_irq(IRQ_NUM, &my_handler);
    printk(">> interrupt_1: " "module unloaded\n");
}

module_init(my_init)
module_exit(my_exit)