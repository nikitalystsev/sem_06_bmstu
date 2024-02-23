$(shell mkdir -p out)

CC := gcc

CFLAGS := -Iexamples/include/


LINKFLAGS := -lpthread -lc

PREF_SRC := ./src/
PREF_INC := ./inc/
PREF_OUT := ./out/
PREF_LIB := ./examples/lib/

.PHONY: d2 clean 

all: d2 

d2: $(PREF_OUT)main.o $(PREF_OUT)error.o $(PREF_OUT)pathalloc.o
	$(CC) $(PREF_OUT)main.o $(PREF_OUT)error.o $(PREF_OUT)pathalloc.o $(LINKFLAGS) -o main.exe

$(PREF_OUT)main.o: $(PREF_SRC)main.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

$(PREF_OUT)error.o: $(PREF_LIB)error.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

$(PREF_OUT)pathalloc.o: $(PREF_LIB)pathalloc.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

include $(wildcard $(PREF_OUT)*.d)

clean : 
	rm -Rf $(PREF_OUT) ./*.exe 