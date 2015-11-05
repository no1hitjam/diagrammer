#include <Python.h>
#include "WordNet-3.0/include/wn.h"


static PyObject* py_search(PyObject* self, PyObject* args)
{
    findtheinfo_ds("test", 0, 0, 0);
    int i = 5;
    return Py_BuildValue("i", i);
}



/* Bind Python function names to our C functions */

static PyMethodDef wordnet_c_methods[] = {
    {"search", py_search, METH_VARARGS},
    {NULL, NULL}
};

/* Python calls this to let us initialize our module */
void initwordnet_c()
{
    (void) Py_InitModule("wordnet_c", wordnet_c_methods);
}
