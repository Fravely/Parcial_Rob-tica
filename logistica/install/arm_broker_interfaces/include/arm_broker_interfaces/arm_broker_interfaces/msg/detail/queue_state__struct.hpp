// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from arm_broker_interfaces:msg/QueueState.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__STRUCT_HPP_
#define ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__arm_broker_interfaces__msg__QueueState __attribute__((deprecated))
#else
# define DEPRECATED__arm_broker_interfaces__msg__QueueState __declspec(deprecated)
#endif

namespace arm_broker_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct QueueState_
{
  using Type = QueueState_<ContainerAllocator>;

  explicit QueueState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->executing_client = "";
      this->executing_goal_id = "";
      this->executing_elapsed_s = 0.0;
      this->queue_length = 0l;
      this->total_accepted = 0l;
      this->total_rejected = 0l;
      this->total_completed = 0l;
    }
  }

  explicit QueueState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init),
    executing_client(_alloc),
    executing_goal_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->executing_client = "";
      this->executing_goal_id = "";
      this->executing_elapsed_s = 0.0;
      this->queue_length = 0l;
      this->total_accepted = 0l;
      this->total_rejected = 0l;
      this->total_completed = 0l;
    }
  }

  // field types and members
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;
  using _executing_client_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _executing_client_type executing_client;
  using _executing_goal_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _executing_goal_id_type executing_goal_id;
  using _executing_elapsed_s_type =
    double;
  _executing_elapsed_s_type executing_elapsed_s;
  using _queue_length_type =
    int32_t;
  _queue_length_type queue_length;
  using _queued_goal_ids_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _queued_goal_ids_type queued_goal_ids;
  using _queued_clients_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _queued_clients_type queued_clients;
  using _queued_priorities_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _queued_priorities_type queued_priorities;
  using _queued_wait_s_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _queued_wait_s_type queued_wait_s;
  using _total_accepted_type =
    int32_t;
  _total_accepted_type total_accepted;
  using _total_rejected_type =
    int32_t;
  _total_rejected_type total_rejected;
  using _total_completed_type =
    int32_t;
  _total_completed_type total_completed;

  // setters for named parameter idiom
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__executing_client(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->executing_client = _arg;
    return *this;
  }
  Type & set__executing_goal_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->executing_goal_id = _arg;
    return *this;
  }
  Type & set__executing_elapsed_s(
    const double & _arg)
  {
    this->executing_elapsed_s = _arg;
    return *this;
  }
  Type & set__queue_length(
    const int32_t & _arg)
  {
    this->queue_length = _arg;
    return *this;
  }
  Type & set__queued_goal_ids(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->queued_goal_ids = _arg;
    return *this;
  }
  Type & set__queued_clients(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->queued_clients = _arg;
    return *this;
  }
  Type & set__queued_priorities(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->queued_priorities = _arg;
    return *this;
  }
  Type & set__queued_wait_s(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->queued_wait_s = _arg;
    return *this;
  }
  Type & set__total_accepted(
    const int32_t & _arg)
  {
    this->total_accepted = _arg;
    return *this;
  }
  Type & set__total_rejected(
    const int32_t & _arg)
  {
    this->total_rejected = _arg;
    return *this;
  }
  Type & set__total_completed(
    const int32_t & _arg)
  {
    this->total_completed = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    arm_broker_interfaces::msg::QueueState_<ContainerAllocator> *;
  using ConstRawPtr =
    const arm_broker_interfaces::msg::QueueState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<arm_broker_interfaces::msg::QueueState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<arm_broker_interfaces::msg::QueueState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::msg::QueueState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::msg::QueueState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      arm_broker_interfaces::msg::QueueState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<arm_broker_interfaces::msg::QueueState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<arm_broker_interfaces::msg::QueueState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<arm_broker_interfaces::msg::QueueState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__arm_broker_interfaces__msg__QueueState
    std::shared_ptr<arm_broker_interfaces::msg::QueueState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__arm_broker_interfaces__msg__QueueState
    std::shared_ptr<arm_broker_interfaces::msg::QueueState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const QueueState_ & other) const
  {
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->executing_client != other.executing_client) {
      return false;
    }
    if (this->executing_goal_id != other.executing_goal_id) {
      return false;
    }
    if (this->executing_elapsed_s != other.executing_elapsed_s) {
      return false;
    }
    if (this->queue_length != other.queue_length) {
      return false;
    }
    if (this->queued_goal_ids != other.queued_goal_ids) {
      return false;
    }
    if (this->queued_clients != other.queued_clients) {
      return false;
    }
    if (this->queued_priorities != other.queued_priorities) {
      return false;
    }
    if (this->queued_wait_s != other.queued_wait_s) {
      return false;
    }
    if (this->total_accepted != other.total_accepted) {
      return false;
    }
    if (this->total_rejected != other.total_rejected) {
      return false;
    }
    if (this->total_completed != other.total_completed) {
      return false;
    }
    return true;
  }
  bool operator!=(const QueueState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct QueueState_

// alias to use template instance with default allocator
using QueueState =
  arm_broker_interfaces::msg::QueueState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace arm_broker_interfaces

#endif  // ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__STRUCT_HPP_
