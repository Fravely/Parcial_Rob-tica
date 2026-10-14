// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice

#ifndef LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__BUILDER_HPP_
#define LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace laya_ordenes_interfaces
{

namespace srv
{

namespace builder
{

class Init_InterpretarOrden_Request_frase
{
public:
  Init_InterpretarOrden_Request_frase()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Request frase(::laya_ordenes_interfaces::srv::InterpretarOrden_Request::_frase_type arg)
  {
    msg_.frase = std::move(arg);
    return std::move(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::laya_ordenes_interfaces::srv::InterpretarOrden_Request>()
{
  return laya_ordenes_interfaces::srv::builder::Init_InterpretarOrden_Request_frase();
}

}  // namespace laya_ordenes_interfaces


namespace laya_ordenes_interfaces
{

namespace srv
{

namespace builder
{

class Init_InterpretarOrden_Response_resto_http_ms
{
public:
  explicit Init_InterpretarOrden_Response_resto_http_ms(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response resto_http_ms(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_resto_http_ms_type arg)
  {
    msg_.resto_http_ms = std::move(arg);
    return std::move(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_inferencia_ms
{
public:
  explicit Init_InterpretarOrden_Response_inferencia_ms(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_resto_http_ms inferencia_ms(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_inferencia_ms_type arg)
  {
    msg_.inferencia_ms = std::move(arg);
    return Init_InterpretarOrden_Response_resto_http_ms(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_latencia_http_ms
{
public:
  explicit Init_InterpretarOrden_Response_latencia_http_ms(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_inferencia_ms latencia_http_ms(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_latencia_http_ms_type arg)
  {
    msg_.latencia_http_ms = std::move(arg);
    return Init_InterpretarOrden_Response_inferencia_ms(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_motivo
{
public:
  explicit Init_InterpretarOrden_Response_motivo(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_latencia_http_ms motivo(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_motivo_type arg)
  {
    msg_.motivo = std::move(arg);
    return Init_InterpretarOrden_Response_latencia_http_ms(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_fuente
{
public:
  explicit Init_InterpretarOrden_Response_fuente(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_motivo fuente(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_fuente_type arg)
  {
    msg_.fuente = std::move(arg);
    return Init_InterpretarOrden_Response_motivo(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_degradada
{
public:
  explicit Init_InterpretarOrden_Response_degradada(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_fuente degradada(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_degradada_type arg)
  {
    msg_.degradada = std::move(arg);
    return Init_InterpretarOrden_Response_fuente(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_permitido
{
public:
  explicit Init_InterpretarOrden_Response_permitido(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_degradada permitido(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_permitido_type arg)
  {
    msg_.permitido = std::move(arg);
    return Init_InterpretarOrden_Response_degradada(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_prioridad
{
public:
  explicit Init_InterpretarOrden_Response_prioridad(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_permitido prioridad(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_prioridad_type arg)
  {
    msg_.prioridad = std::move(arg);
    return Init_InterpretarOrden_Response_permitido(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_color
{
public:
  explicit Init_InterpretarOrden_Response_color(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_prioridad color(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_color_type arg)
  {
    msg_.color = std::move(arg);
    return Init_InterpretarOrden_Response_prioridad(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_objeto
{
public:
  explicit Init_InterpretarOrden_Response_objeto(::laya_ordenes_interfaces::srv::InterpretarOrden_Response & msg)
  : msg_(msg)
  {}
  Init_InterpretarOrden_Response_color objeto(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_objeto_type arg)
  {
    msg_.objeto = std::move(arg);
    return Init_InterpretarOrden_Response_color(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

class Init_InterpretarOrden_Response_accion
{
public:
  Init_InterpretarOrden_Response_accion()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_InterpretarOrden_Response_objeto accion(::laya_ordenes_interfaces::srv::InterpretarOrden_Response::_accion_type arg)
  {
    msg_.accion = std::move(arg);
    return Init_InterpretarOrden_Response_objeto(msg_);
  }

private:
  ::laya_ordenes_interfaces::srv::InterpretarOrden_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::laya_ordenes_interfaces::srv::InterpretarOrden_Response>()
{
  return laya_ordenes_interfaces::srv::builder::Init_InterpretarOrden_Response_accion();
}

}  // namespace laya_ordenes_interfaces

#endif  // LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__BUILDER_HPP_
