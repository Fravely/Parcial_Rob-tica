// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__rosidl_typesupport_introspection_c.h"
#include "laya_ordenes_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__functions.h"
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.h"


// Include directives for member types
// Member `frase`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  laya_ordenes_interfaces__srv__InterpretarOrden_Request__init(message_memory);
}

void laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_fini_function(void * message_memory)
{
  laya_ordenes_interfaces__srv__InterpretarOrden_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_member_array[1] = {
  {
    "frase",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Request, frase),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_members = {
  "laya_ordenes_interfaces__srv",  // message namespace
  "InterpretarOrden_Request",  // message name
  1,  // number of fields
  sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Request),
  laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_member_array,  // message members
  laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_type_support_handle = {
  0,
  &laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_laya_ordenes_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, laya_ordenes_interfaces, srv, InterpretarOrden_Request)() {
  if (!laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_type_support_handle.typesupport_identifier) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &laya_ordenes_interfaces__srv__InterpretarOrden_Request__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "laya_ordenes_interfaces/srv/detail/interpretar_orden__rosidl_typesupport_introspection_c.h"
// already included above
// #include "laya_ordenes_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "laya_ordenes_interfaces/srv/detail/interpretar_orden__functions.h"
// already included above
// #include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.h"


// Include directives for member types
// Member `accion`
// Member `objeto`
// Member `color`
// Member `fuente`
// Member `motivo`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  laya_ordenes_interfaces__srv__InterpretarOrden_Response__init(message_memory);
}

void laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_fini_function(void * message_memory)
{
  laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_member_array[11] = {
  {
    "accion",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, accion),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "objeto",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, objeto),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "color",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, color),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "prioridad",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, prioridad),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "permitido",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, permitido),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "degradada",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, degradada),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "fuente",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, fuente),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "motivo",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, motivo),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "latencia_http_ms",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, latencia_http_ms),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "inferencia_ms",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, inferencia_ms),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "resto_http_ms",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(laya_ordenes_interfaces__srv__InterpretarOrden_Response, resto_http_ms),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_members = {
  "laya_ordenes_interfaces__srv",  // message namespace
  "InterpretarOrden_Response",  // message name
  11,  // number of fields
  sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Response),
  laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_member_array,  // message members
  laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_type_support_handle = {
  0,
  &laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_laya_ordenes_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, laya_ordenes_interfaces, srv, InterpretarOrden_Response)() {
  if (!laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_type_support_handle.typesupport_identifier) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &laya_ordenes_interfaces__srv__InterpretarOrden_Response__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "laya_ordenes_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "laya_ordenes_interfaces/srv/detail/interpretar_orden__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_service_members = {
  "laya_ordenes_interfaces__srv",  // service namespace
  "InterpretarOrden",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_Request_message_type_support_handle,
  NULL  // response message
  // laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_Response_message_type_support_handle
};

static rosidl_service_type_support_t laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_service_type_support_handle = {
  0,
  &laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, laya_ordenes_interfaces, srv, InterpretarOrden_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, laya_ordenes_interfaces, srv, InterpretarOrden_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_laya_ordenes_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, laya_ordenes_interfaces, srv, InterpretarOrden)() {
  if (!laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_service_type_support_handle.typesupport_identifier) {
    laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, laya_ordenes_interfaces, srv, InterpretarOrden_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, laya_ordenes_interfaces, srv, InterpretarOrden_Response)()->data;
  }

  return &laya_ordenes_interfaces__srv__detail__interpretar_orden__rosidl_typesupport_introspection_c__InterpretarOrden_service_type_support_handle;
}
