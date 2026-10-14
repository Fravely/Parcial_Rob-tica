// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_broker_interfaces:action/MoveArm.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__STRUCT_H_
#define ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'joint_positions'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'client_id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/MoveArm in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__MoveArm_Goal
{
  rosidl_runtime_c__double__Sequence joint_positions;
  rosidl_runtime_c__String client_id;
  uint8_t priority;
} arm_broker_interfaces__action__MoveArm_Goal;

// Struct for a sequence of arm_broker_interfaces__action__MoveArm_Goal.
typedef struct arm_broker_interfaces__action__MoveArm_Goal__Sequence
{
  arm_broker_interfaces__action__MoveArm_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__MoveArm_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/MoveArm in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__MoveArm_Result
{
  bool success;
  rosidl_runtime_c__String message;
  double wait_time_s;
  double exec_time_s;
} arm_broker_interfaces__action__MoveArm_Result;

// Struct for a sequence of arm_broker_interfaces__action__MoveArm_Result.
typedef struct arm_broker_interfaces__action__MoveArm_Result__Sequence
{
  arm_broker_interfaces__action__MoveArm_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__MoveArm_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'state'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/MoveArm in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__MoveArm_Feedback
{
  rosidl_runtime_c__String state;
  int32_t queue_position;
  double elapsed_s;
} arm_broker_interfaces__action__MoveArm_Feedback;

// Struct for a sequence of arm_broker_interfaces__action__MoveArm_Feedback.
typedef struct arm_broker_interfaces__action__MoveArm_Feedback__Sequence
{
  arm_broker_interfaces__action__MoveArm_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__MoveArm_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "arm_broker_interfaces/action/detail/move_arm__struct.h"

/// Struct defined in action/MoveArm in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__MoveArm_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  arm_broker_interfaces__action__MoveArm_Goal goal;
} arm_broker_interfaces__action__MoveArm_SendGoal_Request;

// Struct for a sequence of arm_broker_interfaces__action__MoveArm_SendGoal_Request.
typedef struct arm_broker_interfaces__action__MoveArm_SendGoal_Request__Sequence
{
  arm_broker_interfaces__action__MoveArm_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__MoveArm_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/MoveArm in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__MoveArm_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} arm_broker_interfaces__action__MoveArm_SendGoal_Response;

// Struct for a sequence of arm_broker_interfaces__action__MoveArm_SendGoal_Response.
typedef struct arm_broker_interfaces__action__MoveArm_SendGoal_Response__Sequence
{
  arm_broker_interfaces__action__MoveArm_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__MoveArm_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/MoveArm in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__MoveArm_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} arm_broker_interfaces__action__MoveArm_GetResult_Request;

// Struct for a sequence of arm_broker_interfaces__action__MoveArm_GetResult_Request.
typedef struct arm_broker_interfaces__action__MoveArm_GetResult_Request__Sequence
{
  arm_broker_interfaces__action__MoveArm_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__MoveArm_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "arm_broker_interfaces/action/detail/move_arm__struct.h"

/// Struct defined in action/MoveArm in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__MoveArm_GetResult_Response
{
  int8_t status;
  arm_broker_interfaces__action__MoveArm_Result result;
} arm_broker_interfaces__action__MoveArm_GetResult_Response;

// Struct for a sequence of arm_broker_interfaces__action__MoveArm_GetResult_Response.
typedef struct arm_broker_interfaces__action__MoveArm_GetResult_Response__Sequence
{
  arm_broker_interfaces__action__MoveArm_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__MoveArm_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "arm_broker_interfaces/action/detail/move_arm__struct.h"

/// Struct defined in action/MoveArm in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__MoveArm_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  arm_broker_interfaces__action__MoveArm_Feedback feedback;
} arm_broker_interfaces__action__MoveArm_FeedbackMessage;

// Struct for a sequence of arm_broker_interfaces__action__MoveArm_FeedbackMessage.
typedef struct arm_broker_interfaces__action__MoveArm_FeedbackMessage__Sequence
{
  arm_broker_interfaces__action__MoveArm_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__MoveArm_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_BROKER_INTERFACES__ACTION__DETAIL__MOVE_ARM__STRUCT_H_
