#include <Python.h>
#include "WordNet-3.0/include/wn.h"


/* Bind Python function names to our C functions */

static PyMethodDef wordnet_c_methods[] = {
  {NULL, NULL}
};

/* Python calls this to let us initialize our module */
void initwordnet_c()
{
    (void) Py_InitModule("wordnet_c", wordnet_c_methods);
}
