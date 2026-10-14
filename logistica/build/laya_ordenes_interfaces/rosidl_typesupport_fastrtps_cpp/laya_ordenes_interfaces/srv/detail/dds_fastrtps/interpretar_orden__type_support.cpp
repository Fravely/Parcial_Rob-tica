// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__rosidl_typesupport_fastrtps_cpp.hpp"
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace laya_ordenes_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_laya_ordenes_interfaces
cdr_serialize(
  const laya_ordenes_interfaces::srv::InterpretarOrden_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: frase
  cdr << ros_message.frase;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_laya_ordenes_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  laya_ordenes_interfaces::srv::InterpretarOrden_Request & ros_message)
{
  // Member: frase
  cdr >> ros_message.frase;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_laya_ordenes_interfaces
get_serialized_size(
  const laya_ordenes_interfaces::srv::InterpretarOrden_Request & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: frase
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.frase.size() + 1);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_laya_ordenes_interfaces
max_serialized_size_InterpretarOrden_Request(
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


  // Member: frase
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
    using DataType = laya_ordenes_interfaces::srv::InterpretarOrden_Request;
    is_plain =
      (
      offsetof(DataType, frase) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _InterpretarOrden_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const laya_ordenes_interfaces::srv::InterpretarOrden_Request *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _InterpretarOrden_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<laya_ordenes_interfaces::srv::InterpretarOrden_Request *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _InterpretarOrden_Request__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const laya_ordenes_interfaces::srv::InterpretarOrden_Request *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _InterpretarOrden_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_InterpretarOrden_Request(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _InterpretarOrden_Request__callbacks = {
  "laya_ordenes_interfaces::srv",
  "InterpretarOrden_Request",
  _InterpretarOrden_Request__cdr_serialize,
  _InterpretarOrden_Request__cdr_deserialize,
  _InterpretarOrden_Request__get_serialized_size,
  _InterpretarOrden_Request__max_serialized_size
};

static rosidl_message_type_support_t _InterpretarOrden_Request__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_InterpretarOrden_Request__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace laya_ordenes_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_laya_ordenes_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<laya_ordenes_interfaces::srv::InterpretarOrden_Request>()
{
  return &laya_ordenes_interfaces::srv::typesupport_fastrtps_cpp::_InterpretarOrden_Request__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, laya_ordenes_interfaces, srv, InterpretarOrden_Request)() {
  return &laya_ordenes_interfaces::srv::typesupport_fastrtps_cpp::_InterpretarOrden_Request__handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include <limits>
// already included above
// #include <stdexcept>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
// already included above
// #include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace laya_ordenes_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_laya_ordenes_interfaces
cdr_serialize(
  const laya_ordenes_interfaces::srv::InterpretarOrden_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: accion
  cdr << ros_message.accion;
  // Member: objeto
  cdr << ros_message.objeto;
  // Member: color
  cdr << ros_message.color;
  // Member: prioridad
  cdr << ros_message.prioridad;
  // Member: permitido
  cdr << (ros_message.permitido ? true : false);
  // Member: degradada
  cdr << (ros_message.degradada ? true : false);
  // Member: fuente
  cdr << ros_message.fuente;
  // Member: motivo
  cdr << ros_message.motivo;
  // Member: latencia_http_ms
  cdr << ros_message.latencia_http_ms;
  // Member: inferencia_ms
  cdr << ros_message.inferencia_ms;
  // Member: resto_http_ms
  cdr << ros_message.resto_http_ms;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_laya_ordenes_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  laya_ordenes_interfaces::srv::InterpretarOrden_Response & ros_message)
{
  // Member: accion
  cdr >> ros_message.accion;

  // Member: objeto
  cdr >> ros_message.objeto;

  // Member: color
  cdr >> ros_message.color;

  // Member: prioridad
  cdr >> ros_message.prioridad;

  // Member: permitido
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.permitido = tmp ? true : false;
  }

  // Member: degradada
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.degradada = tmp ? true : false;
  }

  // Member: fuente
  cdr >> ros_message.fuente;

  // Member: motivo
  cdr >> ros_message.motivo;

  // Member: latencia_http_ms
  cdr >> ros_message.latencia_http_ms;

  // Member: inferencia_ms
  cdr >> ros_message.inferencia_ms;

  // Member: resto_http_ms
  cdr >> ros_message.resto_http_ms;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_laya_ordenes_interfaces
get_serialized_size(
  const laya_ordenes_interfaces::srv::InterpretarOrden_Response & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: accion
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.accion.size() + 1);
  // Member: objeto
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.objeto.size() + 1);
  // Member: color
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.color.size() + 1);
  // Member: prioridad
  {
    size_t item_size = sizeof(ros_message.prioridad);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: permitido
  {
    size_t item_size = sizeof(ros_message.permitido);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: degradada
  {
    size_t item_size = sizeof(ros_message.degradada);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: fuente
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.fuente.size() + 1);
  // Member: motivo
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.motivo.size() + 1);
  // Member: latencia_http_ms
  {
    size_t item_size = sizeof(ros_message.latencia_http_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: inferencia_ms
  {
    size_t item_size = sizeof(ros_message.inferencia_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: resto_http_ms
  {
    size_t item_size = sizeof(ros_message.resto_http_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_laya_ordenes_interfaces
max_serialized_size_InterpretarOrden_Response(
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


  // Member: accion
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

  // Member: objeto
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

  // Member: color
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

  // Member: prioridad
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: permitido
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: degradada
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: fuente
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

  // Member: motivo
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

  // Member: latencia_http_ms
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: inferencia_ms
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: resto_http_ms
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
    using DataType = laya_ordenes_interfaces::srv::InterpretarOrden_Response;
    is_plain =
      (
      offsetof(DataType, resto_http_ms) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _InterpretarOrden_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const laya_ordenes_interfaces::srv::InterpretarOrden_Response *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _InterpretarOrden_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<laya_ordenes_interfaces::srv::InterpretarOrden_Response *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _InterpretarOrden_Response__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const laya_ordenes_interfaces::srv::InterpretarOrden_Response *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _InterpretarOrden_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_InterpretarOrden_Response(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _InterpretarOrden_Response__callbacks = {
  "laya_ordenes_interfaces::srv",
  "InterpretarOrden_Response",
  _InterpretarOrden_Response__cdr_serialize,
  _InterpretarOrden_Response__cdr_deserialize,
  _InterpretarOrden_Response__get_serialized_size,
  _InterpretarOrden_Response__max_serialized_size
};

static rosidl_message_type_support_t _InterpretarOrden_Response__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_InterpretarOrden_Response__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace laya_ordenes_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_laya_ordenes_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<laya_ordenes_interfaces::srv::InterpretarOrden_Response>()
{
  return &laya_ordenes_interfaces::srv::typesupport_fastrtps_cpp::_InterpretarOrden_Response__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, laya_ordenes_interfaces, srv, InterpretarOrden_Response)() {
  return &laya_ordenes_interfaces::srv::typesupport_fastrtps_cpp::_InterpretarOrden_Response__handle;
}

#ifdef __cplusplus
}
#endif

#include "rmw/error_handling.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support_decl.hpp"

namespace laya_ordenes_interfaces
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

static service_type_support_callbacks_t _InterpretarOrden__callbacks = {
  "laya_ordenes_interfaces::srv",
  "InterpretarOrden",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, laya_ordenes_interfaces, srv, InterpretarOrden_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, laya_ordenes_interfaces, srv, InterpretarOrden_Response)(),
};

static rosidl_service_type_support_t _InterpretarOrden__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_InterpretarOrden__callbacks,
  get_service_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace laya_ordenes_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_laya_ordenes_interfaces
const rosidl_service_type_support_t *
get_service_type_support_handle<laya_ordenes_interfaces::srv::InterpretarOrden>()
{
  return &laya_ordenes_interfaces::srv::typesupport_fastrtps_cpp::_InterpretarOrden__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, laya_ordenes_interfaces, srv, InterpretarOrden)() {
  return &laya_ordenes_interfaces::srv::typesupport_fastrtps_cpp::_InterpretarOrden__handle;
}

#ifdef __cplusplus
}
#endif
