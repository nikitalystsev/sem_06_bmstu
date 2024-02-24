#include "apue.h"
#include <dirent.h>
#include <limits.h>
#include <string.h>

/* тип функции, которая будет вызываться для каждого встреченного файла */
typedef int Myfunc(const char *, int, int);

static Myfunc myfunc;
static int myftw(char *, Myfunc *);
static int dopath(const char *, Myfunc *, int);

int main(int argc, char *argv[])
{
    int ret;

    if (argc != 2)
        err_quit("Использование: ftw <начальный_каталог>");

    ret = myftw(argv[1], myfunc); /* выполняет всю работу */

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
    size_t len;

    // fullpath = path_alloc(&len); /* выделить память для PATH_MAX+1 байт */
    /* (листинг 2.3) */

    // strncpy(fullpath, pathname, len);
    // fullpath[len - 1] = 0;

    int level = 0;

    return (dopath(pathname, func, level));
}
/*
 * Выполняет обход дерева каталогов, начиная с "pathname".
 * Если "pathname" не является каталогом, для него вызывается lstat(),
 * func() и затем выполняется возврат.
 * Для каталогов производится рекурсивный вызов функции.
 */
static int /* возвращает то, что вернула функция func() */
dopath(const char *pathname, Myfunc *func, int level)
{
    struct stat statbuf;
    struct dirent *dirp;
    DIR *dp;
    int ret;
    char *fullpath;

    size_t len;

    if ((fullpath = path_alloc(&len)) == NULL)
        return (func(pathname, level, FTW_NS)); // Ошибка выделения памяти

    /*
        получаем информацию о файле, указанном в pathname
    */
    if (lstat(pathname, &statbuf) < 0) /* ошибка вызова функции stat */
    {
        free(fullpath);
        return (func(pathname, level, FTW_NS));
    }

    if (S_ISDIR(statbuf.st_mode) == 0) /* не каталог */
    {
        free(fullpath);
        return (func(pathname, level, FTW_F));
    }

    /*
     * Это каталог. Сначала вызвать функцию func(),
     * а затем обработать все файлы в этом каталоге.
     */
    if ((ret = func(pathname, level++, FTW_D)) != 0)
    {
        free(fullpath);
        return (ret);
    }

    if ((dp = opendir(pathname)) == NULL) /* каталог недоступен */
    {
        free(fullpath);
        return (func(pathname, level, FTW_DNR));
    }

    while ((dirp = readdir(dp)) != NULL)
    {
        if (strcmp(dirp->d_name, ".") == 0 || strcmp(dirp->d_name, "..") == 0)
            continue; /* пропустить каталоги "." и ".." */

        snprintf(fullpath, len, "%s/%s", pathname, dirp->d_name);

        if ((ret = dopath(fullpath, func, level)) != 0) /* рекурсия */
            break;                                      /* выход по ошибке */
    }

    if (closedir(dp) < 0)
    {
        free(fullpath);
        return (func(pathname, level, FTW_NS));
    }

    free(fullpath);

    return (ret);
}

static int myfunc(const char *pathname, int level, int type)
{
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
