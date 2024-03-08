$(shell mkdir -p out)

# $@ Имя цели обрабатываемого правила
# $< Имя первой зависимости обрабатываемого правила
# $^ Список всех зависимостей обрабатываемого правила

CC := gcc

CFLAGS := -Iexamples/include/

PREF_SRC := ./src/
PREF_INC := ./inc/
PREF_OUT := ./out/

.PHONY: clean 

all: server.exe client.exe

server.exe: $(PREF_OUT)server.o 
	$(CC) $^ $(LINKFLAGS) -o server.exe

$(PREF_OUT)server.o: $(PREF_SRC)server.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

client.exe: $(PREF_OUT)client.o 
	$(CC) $^ $(LINKFLAGS) -o client.exe

$(PREF_OUT)client.o: $(PREF_SRC)client.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

include $(wildcard $(PREF_OUT)*.d)

clean : 
	rm -Rf $(PREF_OUT) ./*.exe ./*.cln ./*.srv