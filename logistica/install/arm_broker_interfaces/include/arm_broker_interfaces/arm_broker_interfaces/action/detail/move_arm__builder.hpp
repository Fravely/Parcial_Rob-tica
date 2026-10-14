// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_broker_interfaces:action/MoveArm.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__BUILDER_HPP_
#define ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_broker_interfaces/action/detail/move_arm__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveArm_Goal_priority
{
public:
  explicit Init_MoveArm_Goal_priority(::arm_broker_interfaces::action::MoveArm_Goal & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::MoveArm_Goal priority(::arm_broker_interfaces::action::MoveArm_Goal::_priority_type arg)
  {
    msg_.priority = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Goal msg_;
};

class Init_MoveArm_Goal_client_id
{
public:
  explicit Init_MoveArm_Goal_client_id(::arm_broker_interfaces::action::MoveArm_Goal & msg)
  : msg_(msg)
  {}
  Init_MoveArm_Goal_priority client_id(::arm_broker_interfaces::action::MoveArm_Goal::_client_id_type arg)
  {
    msg_.client_id = std::move(arg);
    return Init_MoveArm_Goal_priority(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Goal msg_;
};

class Init_MoveArm_Goal_joint_positions
{
public:
  Init_MoveArm_Goal_joint_positions()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveArm_Goal_client_id joint_positions(::arm_broker_interfaces::action::MoveArm_Goal::_joint_positions_type arg)
  {
    msg_.joint_positions = std::move(arg);
    return Init_MoveArm_Goal_client_id(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::MoveArm_Goal>()
{
  return arm_broker_interfaces::action::builder::Init_MoveArm_Goal_joint_positions();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveArm_Result_exec_time_s
{
public:
  explicit Init_MoveArm_Result_exec_time_s(::arm_broker_interfaces::action::MoveArm_Result & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::MoveArm_Result exec_time_s(::arm_broker_interfaces::action::MoveArm_Result::_exec_time_s_type arg)
  {
    msg_.exec_time_s = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Result msg_;
};

class Init_MoveArm_Result_wait_time_s
{
public:
  explicit Init_MoveArm_Result_wait_time_s(::arm_broker_interfaces::action::MoveArm_Result & msg)
  : msg_(msg)
  {}
  Init_MoveArm_Result_exec_time_s wait_time_s(::arm_broker_interfaces::action::MoveArm_Result::_wait_time_s_type arg)
  {
    msg_.wait_time_s = std::move(arg);
    return Init_MoveArm_Result_exec_time_s(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Result msg_;
};

class Init_MoveArm_Result_message
{
public:
  explicit Init_MoveArm_Result_message(::arm_broker_interfaces::action::MoveArm_Result & msg)
  : msg_(msg)
  {}
  Init_MoveArm_Result_wait_time_s message(::arm_broker_interfaces::action::MoveArm_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_MoveArm_Result_wait_time_s(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Result msg_;
};

class Init_MoveArm_Result_success
{
public:
  Init_MoveArm_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveArm_Result_message success(::arm_broker_interfaces::action::MoveArm_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveArm_Result_message(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::MoveArm_Result>()
{
  return arm_broker_interfaces::action::builder::Init_MoveArm_Result_success();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveArm_Feedback_elapsed_s
{
public:
  explicit Init_MoveArm_Feedback_elapsed_s(::arm_broker_interfaces::action::MoveArm_Feedback & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::MoveArm_Feedback elapsed_s(::arm_broker_interfaces::action::MoveArm_Feedback::_elapsed_s_type arg)
  {
    msg_.elapsed_s = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Feedback msg_;
};

class Init_MoveArm_Feedback_queue_position
{
public:
  explicit Init_MoveArm_Feedback_queue_position(::arm_broker_interfaces::action::MoveArm_Feedback & msg)
  : msg_(msg)
  {}
  Init_MoveArm_Feedback_elapsed_s queue_position(::arm_broker_interfaces::action::MoveArm_Feedback::_queue_position_type arg)
  {
    msg_.queue_position = std::move(arg);
    return Init_MoveArm_Feedback_elapsed_s(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Feedback msg_;
};

class Init_MoveArm_Feedback_state
{
public:
  Init_MoveArm_Feedback_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveArm_Feedback_queue_position state(::arm_broker_interfaces::action::MoveArm_Feedback::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_MoveArm_Feedback_queue_position(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::MoveArm_Feedback>()
{
  return arm_broker_interfaces::action::builder::Init_MoveArm_Feedback_state();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveArm_SendGoal_Request_goal
{
public:
  explicit Init_MoveArm_SendGoal_Request_goal(::arm_broker_interfaces::action::MoveArm_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::MoveArm_SendGoal_Request goal(::arm_broker_interfaces::action::MoveArm_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_SendGoal_Request msg_;
};

class Init_MoveArm_SendGoal_Request_goal_id
{
public:
  Init_MoveArm_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveArm_SendGoal_Request_goal goal_id(::arm_broker_interfaces::action::MoveArm_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_MoveArm_SendGoal_Request_goal(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::MoveArm_SendGoal_Request>()
{
  return arm_broker_interfaces::action::builder::Init_MoveArm_SendGoal_Request_goal_id();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveArm_SendGoal_Response_stamp
{
public:
  explicit Init_MoveArm_SendGoal_Response_stamp(::arm_broker_interfaces::action::MoveArm_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::MoveArm_SendGoal_Response stamp(::arm_broker_interfaces::action::MoveArm_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_SendGoal_Response msg_;
};

class Init_MoveArm_SendGoal_Response_accepted
{
public:
  Init_MoveArm_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveArm_SendGoal_Response_stamp accepted(::arm_broker_interfaces::action::MoveArm_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_MoveArm_SendGoal_Response_stamp(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::MoveArm_SendGoal_Response>()
{
  return arm_broker_interfaces::action::builder::Init_MoveArm_SendGoal_Response_accepted();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveArm_GetResult_Request_goal_id
{
public:
  Init_MoveArm_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::arm_broker_interfaces::action::MoveArm_GetResult_Request goal_id(::arm_broker_interfaces::action::MoveArm_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::MoveArm_GetResult_Request>()
{
  return arm_broker_interfaces::action::builder::Init_MoveArm_GetResult_Request_goal_id();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveArm_GetResult_Response_result
{
public:
  explicit Init_MoveArm_GetResult_Response_result(::arm_broker_interfaces::action::MoveArm_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::MoveArm_GetResult_Response result(::arm_broker_interfaces::action::MoveArm_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_GetResult_Response msg_;
};

class Init_MoveArm_GetResult_Response_status
{
public:
  Init_MoveArm_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveArm_GetResult_Response_result status(::arm_broker_interfaces::action::MoveArm_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_MoveArm_GetResult_Response_result(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::MoveArm_GetResult_Response>()
{
  return arm_broker_interfaces::action::builder::Init_MoveArm_GetResult_Response_status();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveArm_FeedbackMessage_feedback
{
public:
  explicit Init_MoveArm_FeedbackMessage_feedback(::arm_broker_interfaces::action::MoveArm_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::MoveArm_FeedbackMessage feedback(::arm_broker_interfaces::action::MoveArm_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_FeedbackMessage msg_;
};

class Init_MoveArm_FeedbackMessage_goal_id
{
public:
  Init_MoveArm_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveArm_FeedbackMessage_feedback goal_id(::arm_broker_interfaces::action::MoveArm_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_MoveArm_FeedbackMessage_feedback(msg_);
  }

private:
  ::arm_broker_interfaces::action::MoveArm_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::MoveArm_FeedbackMessage>()
{
  return arm_broker_interfaces::action::builder::Init_MoveArm_FeedbackMessage_goal_id();
}

}  // namespace arm_broker_interfaces

#endif  // ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__BUILDER_HPP_
