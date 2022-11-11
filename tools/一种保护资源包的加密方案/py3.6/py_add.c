#include <Python.h>
#include <stdio.h>

//调用Add函数,传两个int型参数
void Add(){
  int x=6,y=8;
  Py_Initialize();
 
  PyObject * pModule = NULL;
  PyObject * pFunc = NULL;
  PyObject *pReturn = NULL;
  
  PyRun_SimpleString("import sys");
  PyRun_SimpleString("sys.path.append('./')");
    //加载python模块
  pModule = PyImport_ImportModule("Test001");//Test001:Python文件名
    //加载对应的Python函数
  pFunc = PyObject_GetAttrString(pModule, "Add");//Add:Python文件中的函数名
 
  //创建参数:
  PyObject *pArgs = PyTuple_New(2);//函数调用的参数传递均是以元组的形式打包的,2表示参数个数
  PyTuple_SetItem(pArgs, 0, Py_BuildValue("i", x));//0--序号,i表示创建int型变量
  PyTuple_SetItem(pArgs, 1, Py_BuildValue("i", y));//1--序号
 
  //返回值
  pReturn = PyEval_CallObject(pFunc, pArgs);//调用函数
 
  //将返回值转换为int类型
  int result;
  PyArg_Parse(pReturn, "i", &result);//i表示转换成int型变量
  printf("返回的结果result：%d + %d + 3= %d\n",x,y,result);
  //cout << "6 + 8 = " << result << endl;
 
  Py_Finalize();
}
char *pRes;
void Hello(){
 
  Py_Initialize();//调用Py_Initialize()进行初始化
  PyObject * pModule = NULL;
  PyObject * pFunc = NULL;
  PyObject *pReturn = NULL;
  PyRun_SimpleString("import sys");
  PyRun_SimpleString("sys.path.append('./')");
 
  pModule = PyImport_ImportModule("Test001");//调用的Python文件名
  pFunc = PyObject_GetAttrString(pModule, "Hello");//调用的函数名
  //创建参数:
  //PyObject *pArgs = PyTuple_New(1);
  //PyTuple_SetItem(pArgs, 0, Py_BuildValue("s", "Hello Python!!"));
  
  //pReturn=PyEval_CallObject(pFunc, pArgs);//调用函数,并传入参数pArgs
  pReturn=PyEval_CallObject(pFunc, NULL);
  //char * result;
  PyArg_Parse(pReturn, "s", &pRes);
  printf("返回值：%s\n",pRes);
  Py_Finalize();//调用Py_Finalize,和Py_Initialize相对应的.
 
}

int main(int argc, char **argv)
{
  Add();
  Hello();
  printf("main:%s\n", pRes);
}
