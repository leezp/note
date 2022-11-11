#include <Python.h>

#define min(a,b)    (((a) < (b)) ? (a) : (b))

char data[1024];

void SetData(const char *str)
{
	strncpy(data, str, min(strlen(str) + 1, 1024));
}

const char *GetData()
{
	return data;
}

PyDoc_STRVAR(PySetData_doc__, "\
测试\n\
\n\
PySetData(str)\n\
str: 出入的字符串\n\
返回: \n\
null \n\
");
static PyObject* PySetData(PyObject *self, PyObject *args)
{
	const char* str = NULL;
	if ( !PyArg_ParseTuple(args, "s", &str) )
	{
		return 0;
	}
	SetData(str);
	Py_RETURN_NONE;
}

PyDoc_STRVAR(PyGetData_doc__, "\
打印数据\n\
\n\
PyGetData()\n\
返回: \n\
data \n\
");
static PyObject* PyGetData(PyObject *self, PyObject *args)
{
	const char* str = NULL;
	return PyString_FromString(GetData());
}

static PyMethodDef module_methods[] = {
	{"py_set_data", PySetData, METH_VARARGS, PySetData_doc__},
	{"py_get_data", PyGetData, METH_VARARGS, PyGetData_doc__},
	{NULL}
	};

void InitCCallPy()
{
	PyObject *module = Py_InitModule3("pycallc", module_methods,
		"python call c");
}
void PyError(const char *err_str)
{
	printf("py error : %s", err_str);
}

static int ConvertResult(PyObject *presult, const char *result_format, void *result)
{
	if (!presult)
	{
		if (PyErr_Occurred())
		{
			PyError("ConvertResult");
			return -1;
		}
		return 0;
	}

	if (!result)
	{
		Py_DECREF(presult);
		return 0;
	}

	if (!PyArg_Parse(presult, (char *)(result_format), result))
	{
		PyError("ConvertResult");
		Py_DECREF(presult);
		return -1;
	}

	if (strcmp(result_format, "O") != 0)
	{
		Py_DECREF(presult);
	}

	return 0;
}

int PyModuleRunFunction(const char *module, const char *function,
						const char *result_format, void *result, const char *args_format, ...)
{

	PyObject *pmodule, *pfunction, *args, *presult;

	pmodule = PyImport_ImportModule((char *)(module));
	if (!pmodule)
	{
		PyObject *type = PyErr_Occurred();
		if (type == PyExc_NameError)
		{
			PyErr_Clear();
			return 0;
		}

		PyError("PyModuleRunFunction");
		return -1;
	}

	pfunction = PyObject_GetAttrString(pmodule, (char *)(function));
	Py_DECREF(pmodule);
	if (!pfunction)
	{
		PyObject *type = PyErr_Occurred();
		if (type == PyExc_AttributeError)
		{
			PyErr_Clear();
			return 0;
		}

		PyError("PyModuleRunFunction");
		return -2;
	}

	if (pfunction == Py_None)
	{
		return 0;
	}

	va_list args_list;
	va_start(args_list, args_format);
	args = Py_VaBuildValue((char *)(args_format), args_list);
	va_end(args_list);

	if (!args)
	{
		Py_DECREF(pfunction);
		return -3;
	}

	presult = PyObject_CallObject(pfunction, args);
	if (presult == 0)
	{
		PyError("PyModuleRunFunction");
		Py_XDECREF(pfunction);
		Py_XDECREF(args);
		return -1;
	}

	Py_XDECREF(pfunction);
	Py_XDECREF(args);

	return ConvertResult(presult, result_format, result);
}

int PyObjectRunMethod(void *object, const char *method,
					  const char *result_format, void *result, char *args_format, ...)
{
	PyObject *pmethod, *pargs, *presult;
	PyObject *pobject = (PyObject *)object;

	pmethod = PyObject_GetAttrString(pobject, (char *)(method));
	if (!pmethod)
	{
		PyErr_Clear();
		PyError("PyObjectRunMethod");
		return -1;
	}

	va_list args_list;
	va_start(args_list, args_format);
	pargs = Py_VaBuildValue(args_format, args_list);
	va_end(args_list);

	if (!pargs)
	{
		Py_DECREF(pmethod);
		return -1;
	}

	presult = PyEval_CallObject(pmethod, pargs);
	if (presult == 0)
	{
		PyError("PyObjectRunMethod");
		Py_XDECREF(pmethod);
		Py_XDECREF(pargs);
		return -1;
	}

	Py_DECREF(pmethod);
	Py_DECREF(pargs);

	return ConvertResult(presult, result_format, result);
}

int GetGlobal(const char *module, const char *variable,
			  const char *result_format, void *result)
{
	PyObject *pmodule, *pvariable;

	pmodule = PyImport_ImportModule((char *)(module));
	if (!pmodule)
	{
		PyError("GetGlobal");
		return -1;
	}

	pvariable = PyObject_GetAttrString(pmodule, (char *)(variable));
	Py_DECREF(pmodule);

	if (!pvariable)
	{
		PyError("GetGlobal");
		return -1;
	}

	return ConvertResult(pvariable, result_format, result);
}

void InitPy()
{
	//Py_SetPythonHome("./");
	Py_Initialize();

	PyObject *pPath = 0;
	GetGlobal("sys", "path", "O", &pPath);
	if (pPath)
	{
		PyList_SetSlice(pPath, 0, PyList_Size(pPath), 0);
		PyObjectRunMethod(pPath, "append", "", 0, "(s)", "./");
		InitCCallPy();
		SetData("hello world!");
		PyModuleRunFunction("hello", "test", "", 0, "()");
		printf("in c : %s", GetData());
		Py_DECREF(pPath);
	}
}

void EndPy()
{
	Py_Finalize();
}
int main(int argc, char **argv)
{
	InitPy();
	EndPy();
	getchar();
	return 0;
}