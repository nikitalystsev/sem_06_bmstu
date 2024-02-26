#include "apue.h"
#include <dirent.h>
#include <limits.h>
#include <string.h>
#include <time.h>

/* тип функции, которая будет вызываться для каждого встреченного файла */
typedef int Myfunc(const char *, int, int);

static Myfunc myfunc;

static int myftw(char *, Myfunc *);
static int myftw_with_chdir(char *, Myfunc *);

static int dopath(Myfunc *, int);
static int dopath_with_chdir(Myfunc *, int, char *);

void cmp_time(char *);

static long long getCpuTimeNs();

int is_print_tree = 1;

int main(int argc, char *argv[])
{
    int ret;

    if (argc != 2)
        err_quit("Использование: ftw <начальный_каталог>");

    ret = myftw(argv[1], myfunc); /* выполняет всю работу */

    cmp_time(argv[1]);

    // подсчитывать количества файлов по типам не нужно

    exit(ret);
}

/*
 * Выполняет обход дерева каталогов, начиная с каталога "pathname".
 * Для каждого встреченного файла вызывает пользовательскую функцию func().
 */
#define FTW_F 1   /* файл, не являющийся каталогом */
#define FTW_D 2   /* каталог */
#define FTW_DNR 3 /* каталог, который недоступен для чтения */
#define FTW_NS 4  /* файл, информацию о котором */
                  /* невозможно получить с помощью stat */

static char *fullpath; /* полный путь к каждому из файлов */

static int /* возвращает то, что вернула функция func() */
myftw(char *pathname, Myfunc *func)
{
    int ret;
    size_t len;

    long long beg, end;
    double cpu_time_used;

    beg = getCpuTimeNs();
    fullpath = path_alloc(&len); /* выделить память для PATH_MAX+1 байт */
    /* (листинг 2.3) */
    end = getCpuTimeNs();

    cpu_time_used = (double)(end - beg);
    printf("\nВремя работы функции path_alloc (без chdir): %3.f нс\n", cpu_time_used);

    strncpy(fullpath, pathname, len);
    fullpath[len - 1] = 0;

    int level = 0;

    ret = dopath(func, level);

    free(fullpath);

    return (ret);
}

static int /* возвращает то, что вернула функция func() */
myftw_with_chdir(char *pathname, Myfunc *func)
{
    int ret;
    size_t len;

    long long beg, end;
    double cpu_time_used;

    beg = getCpuTimeNs();
    fullpath = path_alloc(&len); /* выделить память для PATH_MAX+1 байт */
    /* (листинг 2.3) */
    end = getCpuTimeNs();

    cpu_time_used = (double)(end - beg);
    printf("\nВремя работы функции path_alloc (chdir): %3.f нс\n", cpu_time_used);

    fullpath = path_alloc(&len); /* выделить память для PATH_MAX+1 байт */
    /* (листинг 2.3) */

    strncpy(fullpath, pathname, len);
    fullpath[len - 1] = 0;

    int level = 0;

    ret = dopath_with_chdir(func, level, fullpath);

    free(fullpath);

    return (ret);
}

/*
 * Выполняет обход дерева каталогов, начиная с "pathname".
 * Если "pathname" не является каталогом, для него вызывается lstat(),
 * func() и затем выполняется возврат.
 * Для каталогов производится рекурсивный вызов функции.
 */
static int /* возвращает то, что вернула функция func() */
dopath(Myfunc *func, int level)
{
    struct stat statbuf;
    struct dirent *dirp;
    DIR *dp;
    int ret;
    char *ptr;

    /*
        получаем информацию о файле, указанном в pathname
    */
    if (lstat(fullpath, &statbuf) < 0) /* ошибка вызова функции stat */
        return (func(fullpath, level, FTW_NS));

    if (S_ISDIR(statbuf.st_mode) == 0) /* не каталог */
        return (func(fullpath, level, FTW_F));

    /*
     * Это каталог. Сначала вызвать функцию func(),
     * а затем обработать все файлы в этом каталоге.
     */
    if ((ret = func(fullpath, level++, FTW_D)) != 0)
        return (ret);

    ptr = fullpath + strlen(fullpath);

    *ptr++ = '/';
    *ptr = 0;

    if ((dp = opendir(fullpath)) == NULL) /* каталог недоступен */
        return (func(fullpath, level, FTW_DNR));

    while ((dirp = readdir(dp)) != NULL)
    {
        if (strcmp(dirp->d_name, ".") == 0 || strcmp(dirp->d_name, "..") == 0)
            continue; /* пропустить каталоги "." и ".." */

        strcpy(ptr, dirp->d_name);

        if ((ret = dopath(func, level)) != 0) /* рекурсия */
            break;                            /* выход по ошибке */
    }

    ptr[-1] = 0; /* стереть часть строки от слэша и до конца */

    if (closedir(dp) < 0)
        err_ret("невозможно закрыть каталог %s", fullpath);

    return (ret);
}

/*
 * Выполняет обход дерева каталогов, начиная с "pathname".
 * Если "pathname" не является каталогом, для него вызывается lstat(),
 * func() и затем выполняется возврат.
 * Для каталогов производится рекурсивный вызов функции.
 */
static int /* возвращает то, что вернула функция func() */
dopath_with_chdir(Myfunc *func, int level, char *partname)
{
    struct stat statbuf;
    struct dirent *dirp;
    DIR *dp;
    int ret;
    char *ptr;

    /*
        получаем информацию о файле, указанном в pathname
    */
    if (lstat(partname, &statbuf) < 0) /* ошибка вызова функции stat */
        return (func(partname, level, FTW_NS));

    if (S_ISDIR(statbuf.st_mode) == 0) /* не каталог */
        return (func(partname, level, FTW_F));

    /*
     * Это каталог. Сначала вызвать функцию func(),
     * а затем обработать все файлы в этом каталоге.
     */

    if ((ret = func(partname, level++, FTW_D)) != 0)
        return (ret);

    ptr = partname + strlen(partname);

    *ptr++ = '/';
    *ptr = 0;

    if ((dp = opendir(partname)) == NULL) /* каталог недоступен */
        return (func(partname, level, FTW_DNR));

    chdir(partname);

    while ((dirp = readdir(dp)) != NULL)
    {
        if (strcmp(dirp->d_name, ".") == 0 || strcmp(dirp->d_name, "..") == 0)
            continue; /* пропустить каталоги "." и ".." */

        strcpy(ptr, dirp->d_name);

        if ((ret = dopath_with_chdir(func, level, ptr)) != 0) /* рекурсия */
            break;                                            /* выход по ошибке */
    }

    ptr[-1] = 0; /* стереть часть строки от слэша и до конца */

    if (closedir(dp) < 0)
        err_ret("невозможно закрыть каталог %s", fullpath);

    chdir("..");

    return (ret);
}

static int myfunc(const char *pathname, int level, int type)
{
    if (!is_print_tree)
        return 0;

    if (type == FTW_F || type == FTW_D)
    {
        const char *filename;
        int i = 0;

        for (int i = 0; i < level; ++i)
        {
            if (i != level - 1)
                printf("│   ");
            else
                printf("└───");
        }

        if (level > 0)
        {
            filename = strrchr(pathname, '/');

            if (filename != NULL)
                printf("%s\n", filename + 1);
            else
                printf("%s\n", pathname);
        }
        else
            printf("%s\n", pathname);
    }
    else if (type == FTW_DNR)
        err_ret("закрыт доступ к каталогу %s", pathname);
    else if (type == FTW_NS)
        err_ret("ошибка вызова функции stat для %s", pathname);
    else
        err_dump("неизвестный тип %d для файла %s", type, pathname);

    return (0);
}

static long long getCpuTimeNs()
{
    struct timespec t;

    if (clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t))
    {
        perror("clock_gettime");
        return 0;
    }

    return t.tv_sec * 1000000000LL + t.tv_nsec;
}

void cmp_time(char *pathname)
{
    is_print_tree = 0;

    long long beg, end;
    double cpu_time_used;

    int nreps = 1;

    beg = getCpuTimeNs();
    for (int i = 0; i < nreps; ++i)
        myftw(pathname, myfunc);
    end = getCpuTimeNs();

    cpu_time_used = ((double)(end - beg)) / nreps;
    printf("\nВремя обхода дерева каталогов без chdir: %3.f нс\n", cpu_time_used);

    beg = getCpuTimeNs();
    for (int i = 0; i < nreps; ++i)
        myftw_with_chdir(pathname, myfunc);
    end = getCpuTimeNs();

    cpu_time_used = ((double)(end - beg)) / nreps;
    printf("Время обхода дерева каталогов с chdir: %3.f нс\n", cpu_time_used);
}