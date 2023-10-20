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

    FILE *fp;
    if (!fopen_s(&fp, "testScript.py", "rb")) {
        PyRun_SimpleFile(fp, "testScript.py");
        _fcloseall();
        if (Py_FinalizeEx() < 0)
            exit(120);

        PyMem_RawFree(program);
    }


    return 0;
}
