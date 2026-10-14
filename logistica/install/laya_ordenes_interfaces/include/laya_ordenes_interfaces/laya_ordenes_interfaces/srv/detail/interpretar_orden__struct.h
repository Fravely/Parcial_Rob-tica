// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice

#ifndef LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__STRUCT_H_
#define LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'frase'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/InterpretarOrden in the package laya_ordenes_interfaces.
typedef struct laya_ordenes_interfaces__srv__InterpretarOrden_Request
{
  rosidl_runtime_c__String frase;
} laya_ordenes_interfaces__srv__InterpretarOrden_Request;

// Struct for a sequence of laya_ordenes_interfaces__srv__InterpretarOrden_Request.
typedef struct laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence
{
  laya_ordenes_interfaces__srv__InterpretarOrden_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'accion'
// Member 'objeto'
// Member 'color'
// Member 'fuente'
// Member 'motivo'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/InterpretarOrden in the package laya_ordenes_interfaces.
typedef struct laya_ordenes_interfaces__srv__InterpretarOrden_Response
{
  rosidl_runtime_c__String accion;
  rosidl_runtime_c__String objeto;
  rosidl_runtime_c__String color;
  uint8_t prioridad;
  bool permitido;
  bool degradada;
  rosidl_runtime_c__String fuente;
  rosidl_runtime_c__String motivo;
  double latencia_http_ms;
  double inferencia_ms;
  double resto_http_ms;
} laya_ordenes_interfaces__srv__InterpretarOrden_Response;

// Struct for a sequence of laya_ordenes_interfaces__srv__InterpretarOrden_Response.
typedef struct laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence
{
  laya_ordenes_interfaces__srv__InterpretarOrden_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__STRUCT_H_
