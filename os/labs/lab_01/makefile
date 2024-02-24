$(shell mkdir -p out)

# $@ Имя цели обрабатываемого правила
# $< Имя первой зависимости обрабатываемого правила
# $^ Список всех зависимостей обрабатываемого правила

CC := gcc

CFLAGS := -Iexamples/include/

LINKFLAGS := -lpthread -lc

PREF_SRC := ./src/
PREF_INC := ./inc/
PREF_OUT := ./out/
PREF_LIB := ./examples/lib/

.PHONY: ver1 ver2 clean 

all: ver1 ver2

ver1: $(PREF_OUT)ver1.o $(PREF_OUT)error.o $(PREF_OUT)pathalloc.o
	$(CC) $^ $(LINKFLAGS) -o ver1.exe

$(PREF_OUT)ver1.o: $(PREF_SRC)ver1.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

ver2: $(PREF_OUT)ver2.o $(PREF_OUT)error.o $(PREF_OUT)pathalloc.o
	$(CC) $^ $(LINKFLAGS) -o ver2.exe

$(PREF_OUT)ver2.o: $(PREF_SRC)ver2.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

$(PREF_OUT)error.o: $(PREF_LIB)error.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

$(PREF_OUT)pathalloc.o: $(PREF_LIB)pathalloc.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

include $(wildcard $(PREF_OUT)*.d)

clean : 
	rm -Rf $(PREF_OUT) ./*.exe 