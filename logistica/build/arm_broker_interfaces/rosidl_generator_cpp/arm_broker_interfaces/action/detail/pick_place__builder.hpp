// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_broker_interfaces:action/PickPlace.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__BUILDER_HPP_
#define ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "arm_broker_interfaces/action/detail/pick_place__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_Goal_fuente
{
public:
  explicit Init_PickPlace_Goal_fuente(::arm_broker_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::PickPlace_Goal fuente(::arm_broker_interfaces::action::PickPlace_Goal::_fuente_type arg)
  {
    msg_.fuente = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_degradada
{
public:
  explicit Init_PickPlace_Goal_degradada(::arm_broker_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Goal_fuente degradada(::arm_broker_interfaces::action::PickPlace_Goal::_degradada_type arg)
  {
    msg_.degradada = std::move(arg);
    return Init_PickPlace_Goal_fuente(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_permitido
{
public:
  explicit Init_PickPlace_Goal_permitido(::arm_broker_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Goal_degradada permitido(::arm_broker_interfaces::action::PickPlace_Goal::_permitido_type arg)
  {
    msg_.permitido = std::move(arg);
    return Init_PickPlace_Goal_degradada(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_zona
{
public:
  explicit Init_PickPlace_Goal_zona(::arm_broker_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Goal_permitido zona(::arm_broker_interfaces::action::PickPlace_Goal::_zona_type arg)
  {
    msg_.zona = std::move(arg);
    return Init_PickPlace_Goal_permitido(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_color
{
public:
  explicit Init_PickPlace_Goal_color(::arm_broker_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Goal_zona color(::arm_broker_interfaces::action::PickPlace_Goal::_color_type arg)
  {
    msg_.color = std::move(arg);
    return Init_PickPlace_Goal_zona(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_objeto
{
public:
  explicit Init_PickPlace_Goal_objeto(::arm_broker_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Goal_color objeto(::arm_broker_interfaces::action::PickPlace_Goal::_objeto_type arg)
  {
    msg_.objeto = std::move(arg);
    return Init_PickPlace_Goal_color(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_accion
{
public:
  explicit Init_PickPlace_Goal_accion(::arm_broker_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Goal_objeto accion(::arm_broker_interfaces::action::PickPlace_Goal::_accion_type arg)
  {
    msg_.accion = std::move(arg);
    return Init_PickPlace_Goal_objeto(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_priority
{
public:
  explicit Init_PickPlace_Goal_priority(::arm_broker_interfaces::action::PickPlace_Goal & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Goal_accion priority(::arm_broker_interfaces::action::PickPlace_Goal::_priority_type arg)
  {
    msg_.priority = std::move(arg);
    return Init_PickPlace_Goal_accion(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

class Init_PickPlace_Goal_client_id
{
public:
  Init_PickPlace_Goal_client_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_Goal_priority client_id(::arm_broker_interfaces::action::PickPlace_Goal::_client_id_type arg)
  {
    msg_.client_id = std::move(arg);
    return Init_PickPlace_Goal_priority(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::PickPlace_Goal>()
{
  return arm_broker_interfaces::action::builder::Init_PickPlace_Goal_client_id();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_Result_position_error_mm
{
public:
  explicit Init_PickPlace_Result_position_error_mm(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::PickPlace_Result position_error_mm(::arm_broker_interfaces::action::PickPlace_Result::_position_error_mm_type arg)
  {
    msg_.position_error_mm = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_stage_time_s
{
public:
  explicit Init_PickPlace_Result_stage_time_s(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Result_position_error_mm stage_time_s(::arm_broker_interfaces::action::PickPlace_Result::_stage_time_s_type arg)
  {
    msg_.stage_time_s = std::move(arg);
    return Init_PickPlace_Result_position_error_mm(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_stages
{
public:
  explicit Init_PickPlace_Result_stages(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Result_stage_time_s stages(::arm_broker_interfaces::action::PickPlace_Result::_stages_type arg)
  {
    msg_.stages = std::move(arg);
    return Init_PickPlace_Result_stage_time_s(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_exec_time_s
{
public:
  explicit Init_PickPlace_Result_exec_time_s(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Result_stages exec_time_s(::arm_broker_interfaces::action::PickPlace_Result::_exec_time_s_type arg)
  {
    msg_.exec_time_s = std::move(arg);
    return Init_PickPlace_Result_stages(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_wait_time_s
{
public:
  explicit Init_PickPlace_Result_wait_time_s(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Result_exec_time_s wait_time_s(::arm_broker_interfaces::action::PickPlace_Result::_wait_time_s_type arg)
  {
    msg_.wait_time_s = std::move(arg);
    return Init_PickPlace_Result_exec_time_s(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_message
{
public:
  explicit Init_PickPlace_Result_message(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Result_wait_time_s message(::arm_broker_interfaces::action::PickPlace_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_PickPlace_Result_wait_time_s(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_physical_verified
{
public:
  explicit Init_PickPlace_Result_physical_verified(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Result_message physical_verified(::arm_broker_interfaces::action::PickPlace_Result::_physical_verified_type arg)
  {
    msg_.physical_verified = std::move(arg);
    return Init_PickPlace_Result_message(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_planning_only
{
public:
  explicit Init_PickPlace_Result_planning_only(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Result_physical_verified planning_only(::arm_broker_interfaces::action::PickPlace_Result::_planning_only_type arg)
  {
    msg_.planning_only = std::move(arg);
    return Init_PickPlace_Result_physical_verified(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_simulated
{
public:
  explicit Init_PickPlace_Result_simulated(::arm_broker_interfaces::action::PickPlace_Result & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Result_planning_only simulated(::arm_broker_interfaces::action::PickPlace_Result::_simulated_type arg)
  {
    msg_.simulated = std::move(arg);
    return Init_PickPlace_Result_planning_only(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

class Init_PickPlace_Result_success
{
public:
  Init_PickPlace_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_Result_simulated success(::arm_broker_interfaces::action::PickPlace_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PickPlace_Result_simulated(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::PickPlace_Result>()
{
  return arm_broker_interfaces::action::builder::Init_PickPlace_Result_success();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_Feedback_elapsed_s
{
public:
  explicit Init_PickPlace_Feedback_elapsed_s(::arm_broker_interfaces::action::PickPlace_Feedback & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::PickPlace_Feedback elapsed_s(::arm_broker_interfaces::action::PickPlace_Feedback::_elapsed_s_type arg)
  {
    msg_.elapsed_s = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Feedback msg_;
};

class Init_PickPlace_Feedback_queue_position
{
public:
  explicit Init_PickPlace_Feedback_queue_position(::arm_broker_interfaces::action::PickPlace_Feedback & msg)
  : msg_(msg)
  {}
  Init_PickPlace_Feedback_elapsed_s queue_position(::arm_broker_interfaces::action::PickPlace_Feedback::_queue_position_type arg)
  {
    msg_.queue_position = std::move(arg);
    return Init_PickPlace_Feedback_elapsed_s(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Feedback msg_;
};

class Init_PickPlace_Feedback_state
{
public:
  Init_PickPlace_Feedback_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_Feedback_queue_position state(::arm_broker_interfaces::action::PickPlace_Feedback::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_PickPlace_Feedback_queue_position(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::PickPlace_Feedback>()
{
  return arm_broker_interfaces::action::builder::Init_PickPlace_Feedback_state();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_SendGoal_Request_goal
{
public:
  explicit Init_PickPlace_SendGoal_Request_goal(::arm_broker_interfaces::action::PickPlace_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::PickPlace_SendGoal_Request goal(::arm_broker_interfaces::action::PickPlace_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_SendGoal_Request msg_;
};

class Init_PickPlace_SendGoal_Request_goal_id
{
public:
  Init_PickPlace_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_SendGoal_Request_goal goal_id(::arm_broker_interfaces::action::PickPlace_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PickPlace_SendGoal_Request_goal(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::PickPlace_SendGoal_Request>()
{
  return arm_broker_interfaces::action::builder::Init_PickPlace_SendGoal_Request_goal_id();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_SendGoal_Response_stamp
{
public:
  explicit Init_PickPlace_SendGoal_Response_stamp(::arm_broker_interfaces::action::PickPlace_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::PickPlace_SendGoal_Response stamp(::arm_broker_interfaces::action::PickPlace_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_SendGoal_Response msg_;
};

class Init_PickPlace_SendGoal_Response_accepted
{
public:
  Init_PickPlace_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_SendGoal_Response_stamp accepted(::arm_broker_interfaces::action::PickPlace_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_PickPlace_SendGoal_Response_stamp(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::PickPlace_SendGoal_Response>()
{
  return arm_broker_interfaces::action::builder::Init_PickPlace_SendGoal_Response_accepted();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_GetResult_Request_goal_id
{
public:
  Init_PickPlace_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::arm_broker_interfaces::action::PickPlace_GetResult_Request goal_id(::arm_broker_interfaces::action::PickPlace_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::PickPlace_GetResult_Request>()
{
  return arm_broker_interfaces::action::builder::Init_PickPlace_GetResult_Request_goal_id();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_GetResult_Response_result
{
public:
  explicit Init_PickPlace_GetResult_Response_result(::arm_broker_interfaces::action::PickPlace_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::PickPlace_GetResult_Response result(::arm_broker_interfaces::action::PickPlace_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_GetResult_Response msg_;
};

class Init_PickPlace_GetResult_Response_status
{
public:
  Init_PickPlace_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_GetResult_Response_result status(::arm_broker_interfaces::action::PickPlace_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_PickPlace_GetResult_Response_result(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::PickPlace_GetResult_Response>()
{
  return arm_broker_interfaces::action::builder::Init_PickPlace_GetResult_Response_status();
}

}  // namespace arm_broker_interfaces


namespace arm_broker_interfaces
{

namespace action
{

namespace builder
{

class Init_PickPlace_FeedbackMessage_feedback
{
public:
  explicit Init_PickPlace_FeedbackMessage_feedback(::arm_broker_interfaces::action::PickPlace_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::arm_broker_interfaces::action::PickPlace_FeedbackMessage feedback(::arm_broker_interfaces::action::PickPlace_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_FeedbackMessage msg_;
};

class Init_PickPlace_FeedbackMessage_goal_id
{
public:
  Init_PickPlace_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PickPlace_FeedbackMessage_feedback goal_id(::arm_broker_interfaces::action::PickPlace_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PickPlace_FeedbackMessage_feedback(msg_);
  }

private:
  ::arm_broker_interfaces::action::PickPlace_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_broker_interfaces::action::PickPlace_FeedbackMessage>()
{
  return arm_broker_interfaces::action::builder::Init_PickPlace_FeedbackMessage_goal_id();
}

}  // namespace arm_broker_interfaces

#endif  // ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__BUILDER_HPP_
