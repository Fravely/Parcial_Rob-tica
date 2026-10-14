// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice

#ifndef LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__STRUCT_HPP_
#define LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__laya_ordenes_interfaces__srv__InterpretarOrden_Request __attribute__((deprecated))
#else
# define DEPRECATED__laya_ordenes_interfaces__srv__InterpretarOrden_Request __declspec(deprecated)
#endif

namespace laya_ordenes_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct InterpretarOrden_Request_
{
  using Type = InterpretarOrden_Request_<ContainerAllocator>;

  explicit InterpretarOrden_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frase = "";
    }
  }

  explicit InterpretarOrden_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : frase(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frase = "";
    }
  }

  // field types and members
  using _frase_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _frase_type frase;

  // setters for named parameter idiom
  Type & set__frase(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->frase = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__laya_ordenes_interfaces__srv__InterpretarOrden_Request
    std::shared_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__laya_ordenes_interfaces__srv__InterpretarOrden_Request
    std::shared_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const InterpretarOrden_Request_ & other) const
  {
    if (this->frase != other.frase) {
      return false;
    }
    return true;
  }
  bool operator!=(const InterpretarOrden_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct InterpretarOrden_Request_

// alias to use template instance with default allocator
using InterpretarOrden_Request =
  laya_ordenes_interfaces::srv::InterpretarOrden_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace laya_ordenes_interfaces


#ifndef _WIN32
# define DEPRECATED__laya_ordenes_interfaces__srv__InterpretarOrden_Response __attribute__((deprecated))
#else
# define DEPRECATED__laya_ordenes_interfaces__srv__InterpretarOrden_Response __declspec(deprecated)
#endif

namespace laya_ordenes_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct InterpretarOrden_Response_
{
  using Type = InterpretarOrden_Response_<ContainerAllocator>;

  explicit InterpretarOrden_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accion = "";
      this->objeto = "";
      this->color = "";
      this->prioridad = 0;
      this->permitido = false;
      this->degradada = false;
      this->fuente = "";
      this->motivo = "";
      this->latencia_http_ms = 0.0;
      this->inferencia_ms = 0.0;
      this->resto_http_ms = 0.0;
    }
  }

  explicit InterpretarOrden_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : accion(_alloc),
    objeto(_alloc),
    color(_alloc),
    fuente(_alloc),
    motivo(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accion = "";
      this->objeto = "";
      this->color = "";
      this->prioridad = 0;
      this->permitido = false;
      this->degradada = false;
      this->fuente = "";
      this->motivo = "";
      this->latencia_http_ms = 0.0;
      this->inferencia_ms = 0.0;
      this->resto_http_ms = 0.0;
    }
  }

  // field types and members
  using _accion_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _accion_type accion;
  using _objeto_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _objeto_type objeto;
  using _color_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _color_type color;
  using _prioridad_type =
    uint8_t;
  _prioridad_type prioridad;
  using _permitido_type =
    bool;
  _permitido_type permitido;
  using _degradada_type =
    bool;
  _degradada_type degradada;
  using _fuente_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _fuente_type fuente;
  using _motivo_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _motivo_type motivo;
  using _latencia_http_ms_type =
    double;
  _latencia_http_ms_type latencia_http_ms;
  using _inferencia_ms_type =
    double;
  _inferencia_ms_type inferencia_ms;
  using _resto_http_ms_type =
    double;
  _resto_http_ms_type resto_http_ms;

  // setters for named parameter idiom
  Type & set__accion(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->accion = _arg;
    return *this;
  }
  Type & set__objeto(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->objeto = _arg;
    return *this;
  }
  Type & set__color(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->color = _arg;
    return *this;
  }
  Type & set__prioridad(
    const uint8_t & _arg)
  {
    this->prioridad = _arg;
    return *this;
  }
  Type & set__permitido(
    const bool & _arg)
  {
    this->permitido = _arg;
    return *this;
  }
  Type & set__degradada(
    const bool & _arg)
  {
    this->degradada = _arg;
    return *this;
  }
  Type & set__fuente(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->fuente = _arg;
    return *this;
  }
  Type & set__motivo(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->motivo = _arg;
    return *this;
  }
  Type & set__latencia_http_ms(
    const double & _arg)
  {
    this->latencia_http_ms = _arg;
    return *this;
  }
  Type & set__inferencia_ms(
    const double & _arg)
  {
    this->inferencia_ms = _arg;
    return *this;
  }
  Type & set__resto_http_ms(
    const double & _arg)
  {
    this->resto_http_ms = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__laya_ordenes_interfaces__srv__InterpretarOrden_Response
    std::shared_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__laya_ordenes_interfaces__srv__InterpretarOrden_Response
    std::shared_ptr<laya_ordenes_interfaces::srv::InterpretarOrden_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const InterpretarOrden_Response_ & other) const
  {
    if (this->accion != other.accion) {
      return false;
    }
    if (this->objeto != other.objeto) {
      return false;
    }
    if (this->color != other.color) {
      return false;
    }
    if (this->prioridad != other.prioridad) {
      return false;
    }
    if (this->permitido != other.permitido) {
      return false;
    }
    if (this->degradada != other.degradada) {
      return false;
    }
    if (this->fuente != other.fuente) {
      return false;
    }
    if (this->motivo != other.motivo) {
      return false;
    }
    if (this->latencia_http_ms != other.latencia_http_ms) {
      return false;
    }
    if (this->inferencia_ms != other.inferencia_ms) {
      return false;
    }
    if (this->resto_http_ms != other.resto_http_ms) {
      return false;
    }
    return true;
  }
  bool operator!=(const InterpretarOrden_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct InterpretarOrden_Response_

// alias to use template instance with default allocator
using InterpretarOrden_Response =
  laya_ordenes_interfaces::srv::InterpretarOrden_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace laya_ordenes_interfaces

namespace laya_ordenes_interfaces
{

namespace srv
{

struct InterpretarOrden
{
  using Request = laya_ordenes_interfaces::srv::InterpretarOrden_Request;
  using Response = laya_ordenes_interfaces::srv::InterpretarOrden_Response;
};

}  // namespace srv

}  // namespace laya_ordenes_interfaces

#endif  // LAYA_ORDENES_INTERFACES__SRV__DETAIL__INTERPRETAR_ORDEN__STRUCT_HPP_
