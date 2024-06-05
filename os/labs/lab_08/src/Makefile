# компилятор тот же, что использует ядро (передаем параметром)
# /usr/bin/x86_64-linux-gnu-gcc-12

MODULES := my_fs.c

obj-m := $(MODULES:.c=.o)

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

test:
	sudo dmesg -C
	sudo insmod $(MODULES:.o=.ko)
	sudo dmesg

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
	sudo rmmod $(MODULES:.o=)