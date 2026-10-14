// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from arm_broker_interfaces:action/PickPlace.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__STRUCT_HPP_
#define ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_Goal __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_Goal __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickPlace_Goal_
{
  using Type = PickPlace_Goal_<ContainerAllocator>;

  explicit PickPlace_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->client_id = "";
      this->priority = 0;
      this->accion = "";
      this->objeto = "";
      this->color = "";
      this->zona = "";
      this->permitido = false;
      this->degradada = false;
      this->fuente = "";
    }
  }

  explicit PickPlace_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : client_id(_alloc),
    accion(_alloc),
    objeto(_alloc),
    color(_alloc),
    zona(_alloc),
    fuente(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->client_id = "";
      this->priority = 0;
      this->accion = "";
      this->objeto = "";
      this->color = "";
      this->zona = "";
      this->permitido = false;
      this->degradada = false;
      this->fuente = "";
    }
  }

  // field types and members
  using _client_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _client_id_type client_id;
  using _priority_type =
    uint8_t;
  _priority_type priority;
  using _accion_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _accion_type accion;
  using _objeto_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _objeto_type objeto;
  using _color_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _color_type color;
  using _zona_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _zona_type zona;
  using _permitido_type =
    bool;
  _permitido_type permitido;
  using _degradada_type =
    bool;
  _degradada_type degradada;
  using _fuente_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _fuente_type fuente;

  // setters for named parameter idiom
  Type & set__client_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->client_id = _arg;
    return *this;
  }
  Type & set__priority(
    const uint8_t & _arg)
  {
    this->priority = _arg;
    return *this;
  }
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
  Type & set__zona(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->zona = _arg;
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

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_Goal
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_Goal
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickPlace_Goal_ & other) const
  {
    if (this->client_id != other.client_id) {
      return false;
    }
    if (this->priority != other.priority) {
      return false;
    }
    if (this->accion != other.accion) {
      return false;
    }
    if (this->objeto != other.objeto) {
      return false;
    }
    if (this->color != other.color) {
      return false;
    }
    if (this->zona != other.zona) {
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
    return true;
  }
  bool operator!=(const PickPlace_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickPlace_Goal_

// alias to use template instance with default allocator
using PickPlace_Goal =
  arm_broker_interfaces::action::PickPlace_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace arm_broker_interfaces


#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_Result __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_Result __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickPlace_Result_
{
  using Type = PickPlace_Result_<ContainerAllocator>;

  explicit PickPlace_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->simulated = false;
      this->planning_only = false;
      this->physical_verified = false;
      this->message = "";
      this->wait_time_s = 0.0;
      this->exec_time_s = 0.0;
      this->position_error_mm = 0.0;
    }
  }

  explicit PickPlace_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->simulated = false;
      this->planning_only = false;
      this->physical_verified = false;
      this->message = "";
      this->wait_time_s = 0.0;
      this->exec_time_s = 0.0;
      this->position_error_mm = 0.0;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _simulated_type =
    bool;
  _simulated_type simulated;
  using _planning_only_type =
    bool;
  _planning_only_type planning_only;
  using _physical_verified_type =
    bool;
  _physical_verified_type physical_verified;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _wait_time_s_type =
    double;
  _wait_time_s_type wait_time_s;
  using _exec_time_s_type =
    double;
  _exec_time_s_type exec_time_s;
  using _stages_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _stages_type stages;
  using _stage_time_s_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _stage_time_s_type stage_time_s;
  using _position_error_mm_type =
    double;
  _position_error_mm_type position_error_mm;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__simulated(
    const bool & _arg)
  {
    this->simulated = _arg;
    return *this;
  }
  Type & set__planning_only(
    const bool & _arg)
  {
    this->planning_only = _arg;
    return *this;
  }
  Type & set__physical_verified(
    const bool & _arg)
  {
    this->physical_verified = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__wait_time_s(
    const double & _arg)
  {
    this->wait_time_s = _arg;
    return *this;
  }
  Type & set__exec_time_s(
    const double & _arg)
  {
    this->exec_time_s = _arg;
    return *this;
  }
  Type & set__stages(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->stages = _arg;
    return *this;
  }
  Type & set__stage_time_s(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->stage_time_s = _arg;
    return *this;
  }
  Type & set__position_error_mm(
    const double & _arg)
  {
    this->position_error_mm = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_Result
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_Result
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickPlace_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->simulated != other.simulated) {
      return false;
    }
    if (this->planning_only != other.planning_only) {
      return false;
    }
    if (this->physical_verified != other.physical_verified) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->wait_time_s != other.wait_time_s) {
      return false;
    }
    if (this->exec_time_s != other.exec_time_s) {
      return false;
    }
    if (this->stages != other.stages) {
      return false;
    }
    if (this->stage_time_s != other.stage_time_s) {
      return false;
    }
    if (this->position_error_mm != other.position_error_mm) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickPlace_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickPlace_Result_

// alias to use template instance with default allocator
using PickPlace_Result =
  arm_broker_interfaces::action::PickPlace_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace arm_broker_interfaces


#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_Feedback __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickPlace_Feedback_
{
  using Type = PickPlace_Feedback_<ContainerAllocator>;

  explicit PickPlace_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = "";
      this->queue_position = 0l;
      this->elapsed_s = 0.0;
    }
  }

  explicit PickPlace_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : state(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = "";
      this->queue_position = 0l;
      this->elapsed_s = 0.0;
    }
  }

  // field types and members
  using _state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _state_type state;
  using _queue_position_type =
    int32_t;
  _queue_position_type queue_position;
  using _elapsed_s_type =
    double;
  _elapsed_s_type elapsed_s;

  // setters for named parameter idiom
  Type & set__state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->state = _arg;
    return *this;
  }
  Type & set__queue_position(
    const int32_t & _arg)
  {
    this->queue_position = _arg;
    return *this;
  }
  Type & set__elapsed_s(
    const double & _arg)
  {
    this->elapsed_s = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_Feedback
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_Feedback
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickPlace_Feedback_ & other) const
  {
    if (this->state != other.state) {
      return false;
    }
    if (this->queue_position != other.queue_position) {
      return false;
    }
    if (this->elapsed_s != other.elapsed_s) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickPlace_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickPlace_Feedback_

// alias to use template instance with default allocator
using PickPlace_Feedback =
  arm_broker_interfaces::action::PickPlace_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace arm_broker_interfaces


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "arm_broker_interfaces/action/detail/pick_place__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_SendGoal_Request __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickPlace_SendGoal_Request_
{
  using Type = PickPlace_SendGoal_Request_<ContainerAllocator>;

  explicit PickPlace_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit PickPlace_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const arm_broker_interfaces::action::PickPlace_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_SendGoal_Request
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_SendGoal_Request
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickPlace_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickPlace_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickPlace_SendGoal_Request_

// alias to use template instance with default allocator
using PickPlace_SendGoal_Request =
  arm_broker_interfaces::action::PickPlace_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace arm_broker_interfaces


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_SendGoal_Response __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickPlace_SendGoal_Response_
{
  using Type = PickPlace_SendGoal_Response_<ContainerAllocator>;

  explicit PickPlace_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit PickPlace_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_SendGoal_Response
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_SendGoal_Response
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickPlace_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickPlace_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickPlace_SendGoal_Response_

// alias to use template instance with default allocator
using PickPlace_SendGoal_Response =
  arm_broker_interfaces::action::PickPlace_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace arm_broker_interfaces

namespace arm_broker_interfaces
{

namespace action
{

struct PickPlace_SendGoal
{
  using Request = arm_broker_interfaces::action::PickPlace_SendGoal_Request;
  using Response = arm_broker_interfaces::action::PickPlace_SendGoal_Response;
};

}  // namespace action

}  // namespace arm_broker_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_GetResult_Request __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickPlace_GetResult_Request_
{
  using Type = PickPlace_GetResult_Request_<ContainerAllocator>;

  explicit PickPlace_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit PickPlace_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_GetResult_Request
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_GetResult_Request
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickPlace_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickPlace_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickPlace_GetResult_Request_

// alias to use template instance with default allocator
using PickPlace_GetResult_Request =
  arm_broker_interfaces::action::PickPlace_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace arm_broker_interfaces


// Include directives for member types
// Member 'result'
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_GetResult_Response __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickPlace_GetResult_Response_
{
  using Type = PickPlace_GetResult_Response_<ContainerAllocator>;

  explicit PickPlace_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit PickPlace_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const arm_broker_interfaces::action::PickPlace_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_GetResult_Response
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_GetResult_Response
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickPlace_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickPlace_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickPlace_GetResult_Response_

// alias to use template instance with default allocator
using PickPlace_GetResult_Response =
  arm_broker_interfaces::action::PickPlace_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace arm_broker_interfaces

namespace arm_broker_interfaces
{

namespace action
{

struct PickPlace_GetResult
{
  using Request = arm_broker_interfaces::action::PickPlace_GetResult_Request;
  using Response = arm_broker_interfaces::action::PickPlace_GetResult_Response;
};

}  // namespace action

}  // namespace arm_broker_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__action__PickPlace_FeedbackMessage __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct PickPlace_FeedbackMessage_
{
  using Type = PickPlace_FeedbackMessage_<ContainerAllocator>;

  explicit PickPlace_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit PickPlace_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const arm_broker_interfaces::action::PickPlace_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_FeedbackMessage
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__action__PickPlace_FeedbackMessage
    std::shared_ptr<arm_broker_interfaces::action::PickPlace_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PickPlace_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const PickPlace_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PickPlace_FeedbackMessage_

// alias to use template instance with default allocator
using PickPlace_FeedbackMessage =
  arm_broker_interfaces::action::PickPlace_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace arm_broker_interfaces

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace arm_broker_interfaces
{

namespace action
{

struct PickPlace
{
  /// The goal message defined in the action definition.
  using Goal = arm_broker_interfaces::action::PickPlace_Goal;
  /// The result message defined in the action definition.
  using Result = arm_broker_interfaces::action::PickPlace_Result;
  /// The feedback message defined in the action definition.
  using Feedback = arm_broker_interfaces::action::PickPlace_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = arm_broker_interfaces::action::PickPlace_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = arm_broker_interfaces::action::PickPlace_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = arm_broker_interfaces::action::PickPlace_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct PickPlace PickPlace;

}  // namespace action

}  // namespace arm_broker_interfaces

#endif  // ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__STRUCT_HPP_
