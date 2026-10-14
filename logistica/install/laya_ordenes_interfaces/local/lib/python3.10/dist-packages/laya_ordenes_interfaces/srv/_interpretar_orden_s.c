// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.h"
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool laya_ordenes_interfaces__srv__interpretar_orden__request__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[72];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("laya_ordenes_interfaces.srv._interpretar_orden.InterpretarOrden_Request", full_classname_dest, 71) == 0);
  }
  laya_ordenes_interfaces__srv__InterpretarOrden_Request * ros_message = _ros_message;
  {  // frase
    PyObject * field = PyObject_GetAttrString(_pymsg, "frase");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->frase, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * laya_ordenes_interfaces__srv__interpretar_orden__request__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of InterpretarOrden_Request */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("laya_ordenes_interfaces.srv._interpretar_orden");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "InterpretarOrden_Request");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  laya_ordenes_interfaces__srv__InterpretarOrden_Request * ros_message = (laya_ordenes_interfaces__srv__InterpretarOrden_Request *)raw_ros_message;
  {  // frase
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->frase.data,
      strlen(ros_message->frase.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "frase", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
// already included above
// #include <Python.h>
// already included above
// #include <stdbool.h>
// already included above
// #include "numpy/ndarrayobject.h"
// already included above
// #include "rosidl_runtime_c/visibility_control.h"
// already included above
// #include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.h"
// already included above
// #include "laya_ordenes_interfaces/srv/detail/interpretar_orden__functions.h"

// already included above
// #include "rosidl_runtime_c/string.h"
// already included above
// #include "rosidl_runtime_c/string_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool laya_ordenes_interfaces__srv__interpretar_orden__response__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[73];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("laya_ordenes_interfaces.srv._interpretar_orden.InterpretarOrden_Response", full_classname_dest, 72) == 0);
  }
  laya_ordenes_interfaces__srv__InterpretarOrden_Response * ros_message = _ros_message;
  {  // accion
    PyObject * field = PyObject_GetAttrString(_pymsg, "accion");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->accion, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // objeto
    PyObject * field = PyObject_GetAttrString(_pymsg, "objeto");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->objeto, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // color
    PyObject * field = PyObject_GetAttrString(_pymsg, "color");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->color, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // prioridad
    PyObject * field = PyObject_GetAttrString(_pymsg, "prioridad");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->prioridad = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // permitido
    PyObject * field = PyObject_GetAttrString(_pymsg, "permitido");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->permitido = (Py_True == field);
    Py_DECREF(field);
  }
  {  // degradada
    PyObject * field = PyObject_GetAttrString(_pymsg, "degradada");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->degradada = (Py_True == field);
    Py_DECREF(field);
  }
  {  // fuente
    PyObject * field = PyObject_GetAttrString(_pymsg, "fuente");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->fuente, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // motivo
    PyObject * field = PyObject_GetAttrString(_pymsg, "motivo");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->motivo, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // latencia_http_ms
    PyObject * field = PyObject_GetAttrString(_pymsg, "latencia_http_ms");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->latencia_http_ms = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // inferencia_ms
    PyObject * field = PyObject_GetAttrString(_pymsg, "inferencia_ms");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->inferencia_ms = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // resto_http_ms
    PyObject * field = PyObject_GetAttrString(_pymsg, "resto_http_ms");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->resto_http_ms = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * laya_ordenes_interfaces__srv__interpretar_orden__response__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of InterpretarOrden_Response */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("laya_ordenes_interfaces.srv._interpretar_orden");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "InterpretarOrden_Response");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  laya_ordenes_interfaces__srv__InterpretarOrden_Response * ros_message = (laya_ordenes_interfaces__srv__InterpretarOrden_Response *)raw_ros_message;
  {  // accion
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->accion.data,
      strlen(ros_message->accion.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "accion", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // objeto
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->objeto.data,
      strlen(ros_message->objeto.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "objeto", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // color
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->color.data,
      strlen(ros_message->color.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "color", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // prioridad
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->prioridad);
    {
      int rc = PyObject_SetAttrString(_pymessage, "prioridad", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // permitido
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->permitido ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "permitido", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // degradada
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->degradada ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "degradada", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // fuente
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->fuente.data,
      strlen(ros_message->fuente.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "fuente", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // motivo
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->motivo.data,
      strlen(ros_message->motivo.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "motivo", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // latencia_http_ms
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->latencia_http_ms);
    {
      int rc = PyObject_SetAttrString(_pymessage, "latencia_http_ms", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // inferencia_ms
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->inferencia_ms);
    {
      int rc = PyObject_SetAttrString(_pymessage, "inferencia_ms", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // resto_http_ms
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->resto_http_ms);
    {
      int rc = PyObject_SetAttrString(_pymessage, "resto_http_ms", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
