// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_broker_interfaces:msg/QueueState.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__TRAITS_HPP_
#define ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "arm_broker_interfaces/msg/detail/queue_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace arm_broker_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const QueueState & msg,
  std::ostream & out)
{
  out << "{";
  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: executing_client
  {
    out << "executing_client: ";
    rosidl_generator_traits::value_to_yaml(msg.executing_client, out);
    out << ", ";
  }

  // member: executing_goal_id
  {
    out << "executing_goal_id: ";
    rosidl_generator_traits::value_to_yaml(msg.executing_goal_id, out);
    out << ", ";
  }

  // member: executing_elapsed_s
  {
    out << "executing_elapsed_s: ";
    rosidl_generator_traits::value_to_yaml(msg.executing_elapsed_s, out);
    out << ", ";
  }

  // member: queue_length
  {
    out << "queue_length: ";
    rosidl_generator_traits::value_to_yaml(msg.queue_length, out);
    out << ", ";
  }

  // member: queued_goal_ids
  {
    if (msg.queued_goal_ids.size() == 0) {
      out << "queued_goal_ids: []";
    } else {
      out << "queued_goal_ids: [";
      size_t pending_items = msg.queued_goal_ids.size();
      for (auto item : msg.queued_goal_ids) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: queued_clients
  {
    if (msg.queued_clients.size() == 0) {
      out << "queued_clients: []";
    } else {
      out << "queued_clients: [";
      size_t pending_items = msg.queued_clients.size();
      for (auto item : msg.queued_clients) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: queued_priorities
  {
    if (msg.queued_priorities.size() == 0) {
      out << "queued_priorities: []";
    } else {
      out << "queued_priorities: [";
      size_t pending_items = msg.queued_priorities.size();
      for (auto item : msg.queued_priorities) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: queued_wait_s
  {
    if (msg.queued_wait_s.size() == 0) {
      out << "queued_wait_s: []";
    } else {
      out << "queued_wait_s: [";
      size_t pending_items = msg.queued_wait_s.size();
      for (auto item : msg.queued_wait_s) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: total_accepted
  {
    out << "total_accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.total_accepted, out);
    out << ", ";
  }

  // member: total_rejected
  {
    out << "total_rejected: ";
    rosidl_generator_traits::value_to_yaml(msg.total_rejected, out);
    out << ", ";
  }

  // member: total_completed
  {
    out << "total_completed: ";
    rosidl_generator_traits::value_to_yaml(msg.total_completed, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const QueueState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }

  // member: executing_client
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "executing_client: ";
    rosidl_generator_traits::value_to_yaml(msg.executing_client, out);
    out << "\n";
  }

  // member: executing_goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "executing_goal_id: ";
    rosidl_generator_traits::value_to_yaml(msg.executing_goal_id, out);
    out << "\n";
  }

  // member: executing_elapsed_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "executing_elapsed_s: ";
    rosidl_generator_traits::value_to_yaml(msg.executing_elapsed_s, out);
    out << "\n";
  }

  // member: queue_length
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "queue_length: ";
    rosidl_generator_traits::value_to_yaml(msg.queue_length, out);
    out << "\n";
  }

  // member: queued_goal_ids
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.queued_goal_ids.size() == 0) {
      out << "queued_goal_ids: []\n";
    } else {
      out << "queued_goal_ids:\n";
      for (auto item : msg.queued_goal_ids) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: queued_clients
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.queued_clients.size() == 0) {
      out << "queued_clients: []\n";
    } else {
      out << "queued_clients:\n";
      for (auto item : msg.queued_clients) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: queued_priorities
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.queued_priorities.size() == 0) {
      out << "queued_priorities: []\n";
    } else {
      out << "queued_priorities:\n";
      for (auto item : msg.queued_priorities) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: queued_wait_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.queued_wait_s.size() == 0) {
      out << "queued_wait_s: []\n";
    } else {
      out << "queued_wait_s:\n";
      for (auto item : msg.queued_wait_s) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: total_accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "total_accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.total_accepted, out);
    out << "\n";
  }

  // member: total_rejected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "total_rejected: ";
    rosidl_generator_traits::value_to_yaml(msg.total_rejected, out);
    out << "\n";
  }

  // member: total_completed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "total_completed: ";
    rosidl_generator_traits::value_to_yaml(msg.total_completed, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const QueueState & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace arm_broker_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use arm_broker_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const arm_broker_interfaces::msg::QueueState & msg,
  std::ostream & out, size_t indentation = 0)
{
  arm_broker_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use arm_broker_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const arm_broker_interfaces::msg::QueueState & msg)
{
  return arm_broker_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<arm_broker_interfaces::msg::QueueState>()
{
  return "arm_broker_interfaces::msg::QueueState";
}

template<>
inline const char * name<arm_broker_interfaces::msg::QueueState>()
{
  return "arm_broker_interfaces/msg/QueueState";
}

template<>
struct has_fixed_size<arm_broker_interfaces::msg::QueueState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<arm_broker_interfaces::msg::QueueState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<arm_broker_interfaces::msg::QueueState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__TRAITS_HPP_
