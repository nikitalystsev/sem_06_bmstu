# компилятор тот же, что использует ядро (передаем параметром)
# /usr/bin/x86_64-linux-gnu-gcc-12

obj-m := my_vfs.o

all: 
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules 

test:
	sudo dmesg -C
	sudo insmod my_vfs.ko
	sudo dmesg

clean:	
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
	sudo rmmod my_vfs
