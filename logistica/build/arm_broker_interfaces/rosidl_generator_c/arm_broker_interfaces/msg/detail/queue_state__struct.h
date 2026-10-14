// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_broker_interfaces:msg/QueueState.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__STRUCT_H_
#define ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'executing_client'
// Member 'executing_goal_id'
// Member 'queued_goal_ids'
// Member 'queued_clients'
#include "rosidl_runtime_c/string.h"
// Member 'queued_priorities'
// Member 'queued_wait_s'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/QueueState in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__msg__QueueState
{
  builtin_interfaces__msg__Time stamp;
  rosidl_runtime_c__String executing_client;
  rosidl_runtime_c__String executing_goal_id;
  double executing_elapsed_s;
  int32_t queue_length;
  rosidl_runtime_c__String__Sequence queued_goal_ids;
  rosidl_runtime_c__String__Sequence queued_clients;
  rosidl_runtime_c__uint8__Sequence queued_priorities;
  rosidl_runtime_c__double__Sequence queued_wait_s;
  int32_t total_accepted;
  int32_t total_rejected;
  int32_t total_completed;
} arm_broker_interfaces__msg__QueueState;

// Struct for a sequence of arm_broker_interfaces__msg__QueueState.
typedef struct arm_broker_interfaces__msg__QueueState__Sequence
{
  arm_broker_interfaces__msg__QueueState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__msg__QueueState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__STRUCT_H_
