// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "laya_ordenes_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.h"
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // frase
#include "rosidl_runtime_c/string_functions.h"  // frase

// forward declare type support functions


using _InterpretarOrden_Request__ros_msg_type = laya_ordenes_interfaces__srv__InterpretarOrden_Request;

static bool _InterpretarOrden_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _InterpretarOrden_Request__ros_msg_type * ros_message = static_cast<const _InterpretarOrden_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: frase
  {
    const rosidl_runtime_c__String * str = &ros_message->frase;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _InterpretarOrden_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _InterpretarOrden_Request__ros_msg_type * ros_message = static_cast<_InterpretarOrden_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: frase
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->frase.data) {
      rosidl_runtime_c__String__init(&ros_message->frase);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->frase,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'frase'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_laya_ordenes_interfaces
size_t get_serialized_size_laya_ordenes_interfaces__srv__InterpretarOrden_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _InterpretarOrden_Request__ros_msg_type * ros_message = static_cast<const _InterpretarOrden_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name frase
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->frase.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _InterpretarOrden_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_laya_ordenes_interfaces__srv__InterpretarOrden_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_laya_ordenes_interfaces
size_t max_serialized_size_laya_ordenes_interfaces__srv__InterpretarOrden_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: frase
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = laya_ordenes_interfaces__srv__InterpretarOrden_Request;
    is_plain =
      (
      offsetof(DataType, frase) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _InterpretarOrden_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_laya_ordenes_interfaces__srv__InterpretarOrden_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_InterpretarOrden_Request = {
  "laya_ordenes_interfaces::srv",
  "InterpretarOrden_Request",
  _InterpretarOrden_Request__cdr_serialize,
  _InterpretarOrden_Request__cdr_deserialize,
  _InterpretarOrden_Request__get_serialized_size,
  _InterpretarOrden_Request__max_serialized_size
};

static rosidl_message_type_support_t _InterpretarOrden_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_InterpretarOrden_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, laya_ordenes_interfaces, srv, InterpretarOrden_Request)() {
  return &_InterpretarOrden_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "laya_ordenes_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.h"
// already included above
// #include "laya_ordenes_interfaces/srv/detail/interpretar_orden__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // accion, color, fuente, motivo, objeto
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // accion, color, fuente, motivo, objeto

// forward declare type support functions


using _InterpretarOrden_Response__ros_msg_type = laya_ordenes_interfaces__srv__InterpretarOrden_Response;

static bool _InterpretarOrden_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _InterpretarOrden_Response__ros_msg_type * ros_message = static_cast<const _InterpretarOrden_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: accion
  {
    const rosidl_runtime_c__String * str = &ros_message->accion;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: objeto
  {
    const rosidl_runtime_c__String * str = &ros_message->objeto;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: color
  {
    const rosidl_runtime_c__String * str = &ros_message->color;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: prioridad
  {
    cdr << ros_message->prioridad;
  }

  // Field name: permitido
  {
    cdr << (ros_message->permitido ? true : false);
  }

  // Field name: degradada
  {
    cdr << (ros_message->degradada ? true : false);
  }

  // Field name: fuente
  {
    const rosidl_runtime_c__String * str = &ros_message->fuente;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: motivo
  {
    const rosidl_runtime_c__String * str = &ros_message->motivo;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: latencia_http_ms
  {
    cdr << ros_message->latencia_http_ms;
  }

  // Field name: inferencia_ms
  {
    cdr << ros_message->inferencia_ms;
  }

  // Field name: resto_http_ms
  {
    cdr << ros_message->resto_http_ms;
  }

  return true;
}

static bool _InterpretarOrden_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _InterpretarOrden_Response__ros_msg_type * ros_message = static_cast<_InterpretarOrden_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: accion
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->accion.data) {
      rosidl_runtime_c__String__init(&ros_message->accion);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->accion,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'accion'\n");
      return false;
    }
  }

  // Field name: objeto
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->objeto.data) {
      rosidl_runtime_c__String__init(&ros_message->objeto);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->objeto,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'objeto'\n");
      return false;
    }
  }

  // Field name: color
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->color.data) {
      rosidl_runtime_c__String__init(&ros_message->color);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->color,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'color'\n");
      return false;
    }
  }

  // Field name: prioridad
  {
    cdr >> ros_message->prioridad;
  }

  // Field name: permitido
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->permitido = tmp ? true : false;
  }

  // Field name: degradada
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->degradada = tmp ? true : false;
  }

  // Field name: fuente
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->fuente.data) {
      rosidl_runtime_c__String__init(&ros_message->fuente);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->fuente,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'fuente'\n");
      return false;
    }
  }

  // Field name: motivo
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->motivo.data) {
      rosidl_runtime_c__String__init(&ros_message->motivo);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->motivo,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'motivo'\n");
      return false;
    }
  }

  // Field name: latencia_http_ms
  {
    cdr >> ros_message->latencia_http_ms;
  }

  // Field name: inferencia_ms
  {
    cdr >> ros_message->inferencia_ms;
  }

  // Field name: resto_http_ms
  {
    cdr >> ros_message->resto_http_ms;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_laya_ordenes_interfaces
size_t get_serialized_size_laya_ordenes_interfaces__srv__InterpretarOrden_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _InterpretarOrden_Response__ros_msg_type * ros_message = static_cast<const _InterpretarOrden_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name accion
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->accion.size + 1);
  // field.name objeto
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->objeto.size + 1);
  // field.name color
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->color.size + 1);
  // field.name prioridad
  {
    size_t item_size = sizeof(ros_message->prioridad);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name permitido
  {
    size_t item_size = sizeof(ros_message->permitido);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name degradada
  {
    size_t item_size = sizeof(ros_message->degradada);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name fuente
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->fuente.size + 1);
  // field.name motivo
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->motivo.size + 1);
  // field.name latencia_http_ms
  {
    size_t item_size = sizeof(ros_message->latencia_http_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name inferencia_ms
  {
    size_t item_size = sizeof(ros_message->inferencia_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name resto_http_ms
  {
    size_t item_size = sizeof(ros_message->resto_http_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _InterpretarOrden_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_laya_ordenes_interfaces__srv__InterpretarOrden_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_laya_ordenes_interfaces
size_t max_serialized_size_laya_ordenes_interfaces__srv__InterpretarOrden_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: accion
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: objeto
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: color
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: prioridad
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: permitido
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: degradada
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: fuente
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: motivo
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: latencia_http_ms
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: inferencia_ms
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: resto_http_ms
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = laya_ordenes_interfaces__srv__InterpretarOrden_Response;
    is_plain =
      (
      offsetof(DataType, resto_http_ms) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _InterpretarOrden_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_laya_ordenes_interfaces__srv__InterpretarOrden_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_InterpretarOrden_Response = {
  "laya_ordenes_interfaces::srv",
  "InterpretarOrden_Response",
  _InterpretarOrden_Response__cdr_serialize,
  _InterpretarOrden_Response__cdr_deserialize,
  _InterpretarOrden_Response__get_serialized_size,
  _InterpretarOrden_Response__max_serialized_size
};

static rosidl_message_type_support_t _InterpretarOrden_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_InterpretarOrden_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, laya_ordenes_interfaces, srv, InterpretarOrden_Response)() {
  return &_InterpretarOrden_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "laya_ordenes_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "laya_ordenes_interfaces/srv/interpretar_orden.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t InterpretarOrden__callbacks = {
  "laya_ordenes_interfaces::srv",
  "InterpretarOrden",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, laya_ordenes_interfaces, srv, InterpretarOrden_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, laya_ordenes_interfaces, srv, InterpretarOrden_Response)(),
};

static rosidl_service_type_support_t InterpretarOrden__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &InterpretarOrden__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, laya_ordenes_interfaces, srv, InterpretarOrden)() {
  return &InterpretarOrden__handle;
}

#if defined(__cplusplus)
}
#endif
