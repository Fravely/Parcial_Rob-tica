// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_broker_interfaces:action/MoveArm.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__TRAITS_HPP_
#define ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "arm_broker_interfaces/action/detail/move_arm__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace arm_broker_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const MoveArm_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: joint_positions
  {
    if (msg.joint_positions.size() == 0) {
      out << "joint_positions: []";
    } else {
      out << "joint_positions: [";
      size_t pending_items = msg.joint_positions.size();
      for (auto item : msg.joint_positions) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: client_id
  {
    out << "client_id: ";
    rosidl_generator_traits::value_to_yaml(msg.client_id, out);
    out << ", ";
  }

  // member: priority
  {
    out << "priority: ";
    rosidl_generator_traits::value_to_yaml(msg.priority, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveArm_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: joint_positions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_positions.size() == 0) {
      out << "joint_positions: []\n";
    } else {
      out << "joint_positions:\n";
      for (auto item : msg.joint_positions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: client_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "client_id: ";
    rosidl_generator_traits::value_to_yaml(msg.client_id, out);
    out << "\n";
  }

  // member: priority
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "priority: ";
    rosidl_generator_traits::value_to_yaml(msg.priority, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveArm_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::action::MoveArm_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::action::MoveArm_Goal & msg)
{
  return arm_broker_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_Goal>()
{
  return "arm_broker_interfaces::action::MoveArm_Goal";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_Goal>()
{
  return "arm_broker_interfaces/action/MoveArm_Goal";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_broker_interfaces::action::MoveArm_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace arm_broker_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const MoveArm_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << ", ";
  }

  // member: wait_time_s
  {
    out << "wait_time_s: ";
    rosidl_generator_traits::value_to_yaml(msg.wait_time_s, out);
    out << ", ";
  }

  // member: exec_time_s
  {
    out << "exec_time_s: ";
    rosidl_generator_traits::value_to_yaml(msg.exec_time_s, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveArm_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }

  // member: wait_time_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "wait_time_s: ";
    rosidl_generator_traits::value_to_yaml(msg.wait_time_s, out);
    out << "\n";
  }

  // member: exec_time_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "exec_time_s: ";
    rosidl_generator_traits::value_to_yaml(msg.exec_time_s, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveArm_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::action::MoveArm_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::action::MoveArm_Result & msg)
{
  return arm_broker_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_Result>()
{
  return "arm_broker_interfaces::action::MoveArm_Result";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_Result>()
{
  return "arm_broker_interfaces/action/MoveArm_Result";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_broker_interfaces::action::MoveArm_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace arm_broker_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const MoveArm_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: state
  {
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << ", ";
  }

  // member: queue_position
  {
    out << "queue_position: ";
    rosidl_generator_traits::value_to_yaml(msg.queue_position, out);
    out << ", ";
  }

  // member: elapsed_s
  {
    out << "elapsed_s: ";
    rosidl_generator_traits::value_to_yaml(msg.elapsed_s, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveArm_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << "\n";
  }

  // member: queue_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "queue_position: ";
    rosidl_generator_traits::value_to_yaml(msg.queue_position, out);
    out << "\n";
  }

  // member: elapsed_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "elapsed_s: ";
    rosidl_generator_traits::value_to_yaml(msg.elapsed_s, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveArm_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::action::MoveArm_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::action::MoveArm_Feedback & msg)
{
  return arm_broker_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_Feedback>()
{
  return "arm_broker_interfaces::action::MoveArm_Feedback";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_Feedback>()
{
  return "arm_broker_interfaces/action/MoveArm_Feedback";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_broker_interfaces::action::MoveArm_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "arm_broker_interfaces/action/detail/move_arm__traits.hpp"

namespace arm_broker_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const MoveArm_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveArm_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveArm_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::action::MoveArm_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::action::MoveArm_SendGoal_Request & msg)
{
  return arm_broker_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_SendGoal_Request>()
{
  return "arm_broker_interfaces::action::MoveArm_SendGoal_Request";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_SendGoal_Request>()
{
  return "arm_broker_interfaces/action/MoveArm_SendGoal_Request";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<arm_broker_interfaces::action::MoveArm_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<arm_broker_interfaces::action::MoveArm_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<arm_broker_interfaces::action::MoveArm_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace arm_broker_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const MoveArm_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveArm_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveArm_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::action::MoveArm_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::action::MoveArm_SendGoal_Response & msg)
{
  return arm_broker_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_SendGoal_Response>()
{
  return "arm_broker_interfaces::action::MoveArm_SendGoal_Response";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_SendGoal_Response>()
{
  return "arm_broker_interfaces/action/MoveArm_SendGoal_Response";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<arm_broker_interfaces::action::MoveArm_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_SendGoal>()
{
  return "arm_broker_interfaces::action::MoveArm_SendGoal";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_SendGoal>()
{
  return "arm_broker_interfaces/action/MoveArm_SendGoal";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<arm_broker_interfaces::action::MoveArm_SendGoal_Request>::value &&
    has_fixed_size<arm_broker_interfaces::action::MoveArm_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<arm_broker_interfaces::action::MoveArm_SendGoal_Request>::value &&
    has_bounded_size<arm_broker_interfaces::action::MoveArm_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<arm_broker_interfaces::action::MoveArm_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<arm_broker_interfaces::action::MoveArm_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<arm_broker_interfaces::action::MoveArm_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace arm_broker_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const MoveArm_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveArm_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveArm_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::action::MoveArm_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::action::MoveArm_GetResult_Request & msg)
{
  return arm_broker_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_GetResult_Request>()
{
  return "arm_broker_interfaces::action::MoveArm_GetResult_Request";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_GetResult_Request>()
{
  return "arm_broker_interfaces/action/MoveArm_GetResult_Request";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<arm_broker_interfaces::action::MoveArm_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "arm_broker_interfaces/action/detail/move_arm__traits.hpp"

namespace arm_broker_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const MoveArm_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveArm_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveArm_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::action::MoveArm_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::action::MoveArm_GetResult_Response & msg)
{
  return arm_broker_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_GetResult_Response>()
{
  return "arm_broker_interfaces::action::MoveArm_GetResult_Response";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_GetResult_Response>()
{
  return "arm_broker_interfaces/action/MoveArm_GetResult_Response";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<arm_broker_interfaces::action::MoveArm_Result>::value> {};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<arm_broker_interfaces::action::MoveArm_Result>::value> {};

template<>
struct is_message<arm_broker_interfaces::action::MoveArm_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_GetResult>()
{
  return "arm_broker_interfaces::action::MoveArm_GetResult";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_GetResult>()
{
  return "arm_broker_interfaces/action/MoveArm_GetResult";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<arm_broker_interfaces::action::MoveArm_GetResult_Request>::value &&
    has_fixed_size<arm_broker_interfaces::action::MoveArm_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<arm_broker_interfaces::action::MoveArm_GetResult_Request>::value &&
    has_bounded_size<arm_broker_interfaces::action::MoveArm_GetResult_Response>::value
  >
{
};

template<>
struct is_service<arm_broker_interfaces::action::MoveArm_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<arm_broker_interfaces::action::MoveArm_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<arm_broker_interfaces::action::MoveArm_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "arm_broker_interfaces/action/detail/move_arm__traits.hpp"

namespace arm_broker_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const MoveArm_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveArm_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveArm_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::action::MoveArm_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::action::MoveArm_FeedbackMessage & msg)
{
  return arm_broker_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::action::MoveArm_FeedbackMessage>()
{
  return "arm_broker_interfaces::action::MoveArm_FeedbackMessage";
}

template<>
inline const char * name<arm_broker_interfaces::action::MoveArm_FeedbackMessage>()
{
  return "arm_broker_interfaces/action/MoveArm_FeedbackMessage";
}

template<>
struct has_fixed_size<arm_broker_interfaces::action::MoveArm_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<arm_broker_interfaces::action::MoveArm_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<arm_broker_interfaces::action::MoveArm_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<arm_broker_interfaces::action::MoveArm_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<arm_broker_interfaces::action::MoveArm_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<arm_broker_interfaces::action::MoveArm>
  : std::true_type
{
};

template<>
struct is_action_goal<arm_broker_interfaces::action::MoveArm_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<arm_broker_interfaces::action::MoveArm_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<arm_broker_interfaces::action::MoveArm_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__TRAITS_HPP_
