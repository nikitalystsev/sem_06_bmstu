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

all: app.exe

app.exe: $(PREF_OUT)main.o 
	$(CC) $^ $(LINKFLAGS) -o app.exe

$(PREF_OUT)main.o: $(PREF_SRC)main.c
	$(CC) $(CFLAGS) -c -MD $< -o $@

include $(wildcard $(PREF_OUT)*.d)

clean : 
	rm -Rf $(PREF_OUT) ./*.exe 