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

.PHONY: clean 

all: app.exe

app.exe: $(PREF_OUT)main.o $(PREF_OUT)error.o $(PREF_OUT)pathalloc.o
	$(CC) $^ $(LINKFLAGS) -o app.exe

$(PREF_OUT)main.o: $(PREF_SRC)main.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

$(PREF_OUT)error.o: $(PREF_LIB)error.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

$(PREF_OUT)pathalloc.o: $(PREF_LIB)pathalloc.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

include $(wildcard $(PREF_OUT)*.d)

clean : 
	rm -Rf $(PREF_OUT) ./*.exe 