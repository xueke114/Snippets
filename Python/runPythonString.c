//
// Created by xueke on 2023/10/20.
//
#define PY_SSIZE_T_CLEAN

#include <Python.h>

int main(int argc, char *argv[]) {
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    wprintf(L"%ls\n", program);
    Py_SetProgramName(program);
    Py_Initialize();
    PyRun_SimpleString("from time import time, ctime\n"
                       "import numpy as np\n"
                       "print('你好，Python')\n"
                       "print(np.random.randint(10, size=(5,5)))\n"
                       "print('Today is', ctime(time()))\n");
    if (Py_FinalizeEx() < 0)
        exit(120);
    PyMem_RawFree(program);

    return 0;
}
