// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice

#ifndef LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__TRAITS_HPP_
#define LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace laya_ordenes_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const InterpretarOrden_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: frase
  {
    out << "frase: ";
    rosidl_generator_traits::value_to_yaml(msg.frase, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const InterpretarOrden_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: frase
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frase: ";
    rosidl_generator_traits::value_to_yaml(msg.frase, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const InterpretarOrden_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace laya_ordenes_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use laya_ordenes_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const laya_ordenes_interfaces::srv::InterpretarOrden_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  laya_ordenes_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use laya_ordenes_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const laya_ordenes_interfaces::srv::InterpretarOrden_Request & msg)
{
  return laya_ordenes_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<laya_ordenes_interfaces::srv::InterpretarOrden_Request>()
{
  return "laya_ordenes_interfaces::srv::InterpretarOrden_Request";
}

template<>
inline const char * name<laya_ordenes_interfaces::srv::InterpretarOrden_Request>()
{
  return "laya_ordenes_interfaces/srv/InterpretarOrden_Request";
}

template<>
struct has_fixed_size<laya_ordenes_interfaces::srv::InterpretarOrden_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<laya_ordenes_interfaces::srv::InterpretarOrden_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<laya_ordenes_interfaces::srv::InterpretarOrden_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace laya_ordenes_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const InterpretarOrden_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accion
  {
    out << "accion: ";
    rosidl_generator_traits::value_to_yaml(msg.accion, out);
    out << ", ";
  }

  // member: objeto
  {
    out << "objeto: ";
    rosidl_generator_traits::value_to_yaml(msg.objeto, out);
    out << ", ";
  }

  // member: color
  {
    out << "color: ";
    rosidl_generator_traits::value_to_yaml(msg.color, out);
    out << ", ";
  }

  // member: prioridad
  {
    out << "prioridad: ";
    rosidl_generator_traits::value_to_yaml(msg.prioridad, out);
    out << ", ";
  }

  // member: permitido
  {
    out << "permitido: ";
    rosidl_generator_traits::value_to_yaml(msg.permitido, out);
    out << ", ";
  }

  // member: degradada
  {
    out << "degradada: ";
    rosidl_generator_traits::value_to_yaml(msg.degradada, out);
    out << ", ";
  }

  // member: fuente
  {
    out << "fuente: ";
    rosidl_generator_traits::value_to_yaml(msg.fuente, out);
    out << ", ";
  }

  // member: motivo
  {
    out << "motivo: ";
    rosidl_generator_traits::value_to_yaml(msg.motivo, out);
    out << ", ";
  }

  // member: latencia_http_ms
  {
    out << "latencia_http_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.latencia_http_ms, out);
    out << ", ";
  }

  // member: inferencia_ms
  {
    out << "inferencia_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.inferencia_ms, out);
    out << ", ";
  }

  // member: resto_http_ms
  {
    out << "resto_http_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.resto_http_ms, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const InterpretarOrden_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accion
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accion: ";
    rosidl_generator_traits::value_to_yaml(msg.accion, out);
    out << "\n";
  }

  // member: objeto
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "objeto: ";
    rosidl_generator_traits::value_to_yaml(msg.objeto, out);
    out << "\n";
  }

  // member: color
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "color: ";
    rosidl_generator_traits::value_to_yaml(msg.color, out);
    out << "\n";
  }

  // member: prioridad
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "prioridad: ";
    rosidl_generator_traits::value_to_yaml(msg.prioridad, out);
    out << "\n";
  }

  // member: permitido
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "permitido: ";
    rosidl_generator_traits::value_to_yaml(msg.permitido, out);
    out << "\n";
  }

  // member: degradada
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "degradada: ";
    rosidl_generator_traits::value_to_yaml(msg.degradada, out);
    out << "\n";
  }

  // member: fuente
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fuente: ";
    rosidl_generator_traits::value_to_yaml(msg.fuente, out);
    out << "\n";
  }

  // member: motivo
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "motivo: ";
    rosidl_generator_traits::value_to_yaml(msg.motivo, out);
    out << "\n";
  }

  // member: latencia_http_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "latencia_http_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.latencia_http_ms, out);
    out << "\n";
  }

  // member: inferencia_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "inferencia_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.inferencia_ms, out);
    out << "\n";
  }

  // member: resto_http_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "resto_http_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.resto_http_ms, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const InterpretarOrden_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace laya_ordenes_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use laya_ordenes_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  laya_ordenes_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use laya_ordenes_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
{
  return laya_ordenes_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<laya_ordenes_interfaces::srv::InterpretarOrden_Response>()
{
  return "laya_ordenes_interfaces::srv::InterpretarOrden_Response";
}

template<>
inline const char * name<laya_ordenes_interfaces::srv::InterpretarOrden_Response>()
{
  return "laya_ordenes_interfaces/srv/InterpretarOrden_Response";
}

template<>
struct has_fixed_size<laya_ordenes_interfaces::srv::InterpretarOrden_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<laya_ordenes_interfaces::srv::InterpretarOrden_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<laya_ordenes_interfaces::srv::InterpretarOrden_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<laya_ordenes_interfaces::srv::InterpretarOrden>()
{
  return "laya_ordenes_interfaces::srv::InterpretarOrden";
}

template<>
inline const char * name<laya_ordenes_interfaces::srv::InterpretarOrden>()
{
  return "laya_ordenes_interfaces/srv/InterpretarOrden";
}

template<>
struct has_fixed_size<laya_ordenes_interfaces::srv::InterpretarOrden>
  : std::integral_constant<
    bool,
    has_fixed_size<laya_ordenes_interfaces::srv::InterpretarOrden_Request>::value &&
    has_fixed_size<laya_ordenes_interfaces::srv::InterpretarOrden_Response>::value
  >
{
};

template<>
struct has_bounded_size<laya_ordenes_interfaces::srv::InterpretarOrden>
  : std::integral_constant<
    bool,
    has_bounded_size<laya_ordenes_interfaces::srv::InterpretarOrden_Request>::value &&
    has_bounded_size<laya_ordenes_interfaces::srv::InterpretarOrden_Response>::value
  >
{
};

template<>
struct is_service<laya_ordenes_interfaces::srv::InterpretarOrden>
  : std::true_type
{
};

template<>
struct is_service_request<laya_ordenes_interfaces::srv::InterpretarOrden_Request>
  : std::true_type
{
};

template<>
struct is_service_response<laya_ordenes_interfaces::srv::InterpretarOrden_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__TRAITS_HPP_
