// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_broker_interfaces:msg/QueueState.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__BUILDER_HPP_
#define ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_broker_interfaces/msg/detail/queue_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_broker_interfaces
{

namespace msg
{

namespace builder
{

class Init_QueueState_total_completed
{
public:
  explicit Init_QueueState_total_completed(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::msg::QueueState total_completed(::arm_broker_interfaces::msg::QueueState::_total_completed_type arg)
  {
    msg_.total_completed = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_total_rejected
{
public:
  explicit Init_QueueState_total_rejected(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_total_completed total_rejected(::arm_broker_interfaces::msg::QueueState::_total_rejected_type arg)
  {
    msg_.total_rejected = std::move(arg);
    return Init_QueueState_total_completed(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_total_accepted
{
public:
  explicit Init_QueueState_total_accepted(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_total_rejected total_accepted(::arm_broker_interfaces::msg::QueueState::_total_accepted_type arg)
  {
    msg_.total_accepted = std::move(arg);
    return Init_QueueState_total_rejected(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_queued_wait_s
{
public:
  explicit Init_QueueState_queued_wait_s(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_total_accepted queued_wait_s(::arm_broker_interfaces::msg::QueueState::_queued_wait_s_type arg)
  {
    msg_.queued_wait_s = std::move(arg);
    return Init_QueueState_total_accepted(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_queued_priorities
{
public:
  explicit Init_QueueState_queued_priorities(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_queued_wait_s queued_priorities(::arm_broker_interfaces::msg::QueueState::_queued_priorities_type arg)
  {
    msg_.queued_priorities = std::move(arg);
    return Init_QueueState_queued_wait_s(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_queued_clients
{
public:
  explicit Init_QueueState_queued_clients(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_queued_priorities queued_clients(::arm_broker_interfaces::msg::QueueState::_queued_clients_type arg)
  {
    msg_.queued_clients = std::move(arg);
    return Init_QueueState_queued_priorities(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_queued_goal_ids
{
public:
  explicit Init_QueueState_queued_goal_ids(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_queued_clients queued_goal_ids(::arm_broker_interfaces::msg::QueueState::_queued_goal_ids_type arg)
  {
    msg_.queued_goal_ids = std::move(arg);
    return Init_QueueState_queued_clients(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_queue_length
{
public:
  explicit Init_QueueState_queue_length(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_queued_goal_ids queue_length(::arm_broker_interfaces::msg::QueueState::_queue_length_type arg)
  {
    msg_.queue_length = std::move(arg);
    return Init_QueueState_queued_goal_ids(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_executing_elapsed_s
{
public:
  explicit Init_QueueState_executing_elapsed_s(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_queue_length executing_elapsed_s(::arm_broker_interfaces::msg::QueueState::_executing_elapsed_s_type arg)
  {
    msg_.executing_elapsed_s = std::move(arg);
    return Init_QueueState_queue_length(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_executing_goal_id
{
public:
  explicit Init_QueueState_executing_goal_id(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_executing_elapsed_s executing_goal_id(::arm_broker_interfaces::msg::QueueState::_executing_goal_id_type arg)
  {
    msg_.executing_goal_id = std::move(arg);
    return Init_QueueState_executing_elapsed_s(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_executing_client
{
public:
  explicit Init_QueueState_executing_client(::arm_broker_interfaces::msg::QueueState & msg)
  : msg_(msg)
  {}
  Init_QueueState_executing_goal_id executing_client(::arm_broker_interfaces::msg::QueueState::_executing_client_type arg)
  {
    msg_.executing_client = std::move(arg);
    return Init_QueueState_executing_goal_id(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

class Init_QueueState_stamp
{
public:
  Init_QueueState_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_QueueState_executing_client stamp(::arm_broker_interfaces::msg::QueueState::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_QueueState_executing_client(msg_);
  }

private:
  ::arm_broker_interfaces::msg::QueueState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::msg::QueueState>()
{
  return arm_broker_interfaces::msg::builder::Init_QueueState_stamp();
}

}  // namespace arm_broker_interfaces

#endif  // ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__BUILDER_HPP_
