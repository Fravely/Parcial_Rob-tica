// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_broker_interfaces:action/PickPlace.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__STRUCT_H_
#define ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'client_id'
// Member 'accion'
// Member 'objeto'
// Member 'color'
// Member 'zona'
// Member 'fuente'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/PickPlace in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__PickPlace_Goal
{
  rosidl_runtime_c__String client_id;
  uint8_t priority;
  rosidl_runtime_c__String accion;
  rosidl_runtime_c__String objeto;
  rosidl_runtime_c__String color;
  rosidl_runtime_c__String zona;
  bool permitido;
  bool degradada;
  rosidl_runtime_c__String fuente;
} arm_broker_interfaces__action__PickPlace_Goal;

// Struct for a sequence of arm_broker_interfaces__action__PickPlace_Goal.
typedef struct arm_broker_interfaces__action__PickPlace_Goal__Sequence
{
  arm_broker_interfaces__action__PickPlace_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__PickPlace_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// Member 'stages'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'stage_time_s'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in action/PickPlace in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__PickPlace_Result
{
  bool success;
  bool simulated;
  bool planning_only;
  bool physical_verified;
  rosidl_runtime_c__String message;
  double wait_time_s;
  double exec_time_s;
  rosidl_runtime_c__String__Sequence stages;
  rosidl_runtime_c__double__Sequence stage_time_s;
  double position_error_mm;
} arm_broker_interfaces__action__PickPlace_Result;

// Struct for a sequence of arm_broker_interfaces__action__PickPlace_Result.
typedef struct arm_broker_interfaces__action__PickPlace_Result__Sequence
{
  arm_broker_interfaces__action__PickPlace_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__PickPlace_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'state'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/PickPlace in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__PickPlace_Feedback
{
  rosidl_runtime_c__String state;
  int32_t queue_position;
  double elapsed_s;
} arm_broker_interfaces__action__PickPlace_Feedback;

// Struct for a sequence of arm_broker_interfaces__action__PickPlace_Feedback.
typedef struct arm_broker_interfaces__action__PickPlace_Feedback__Sequence
{
  arm_broker_interfaces__action__PickPlace_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__PickPlace_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "arm_broker_interfaces/action/detail/pick_place__struct.h"

/// Struct defined in action/PickPlace in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__PickPlace_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  arm_broker_interfaces__action__PickPlace_Goal goal;
} arm_broker_interfaces__action__PickPlace_SendGoal_Request;

// Struct for a sequence of arm_broker_interfaces__action__PickPlace_SendGoal_Request.
typedef struct arm_broker_interfaces__action__PickPlace_SendGoal_Request__Sequence
{
  arm_broker_interfaces__action__PickPlace_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__PickPlace_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/PickPlace in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__PickPlace_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} arm_broker_interfaces__action__PickPlace_SendGoal_Response;

// Struct for a sequence of arm_broker_interfaces__action__PickPlace_SendGoal_Response.
typedef struct arm_broker_interfaces__action__PickPlace_SendGoal_Response__Sequence
{
  arm_broker_interfaces__action__PickPlace_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__PickPlace_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/PickPlace in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__PickPlace_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} arm_broker_interfaces__action__PickPlace_GetResult_Request;

// Struct for a sequence of arm_broker_interfaces__action__PickPlace_GetResult_Request.
typedef struct arm_broker_interfaces__action__PickPlace_GetResult_Request__Sequence
{
  arm_broker_interfaces__action__PickPlace_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__PickPlace_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"

/// Struct defined in action/PickPlace in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__PickPlace_GetResult_Response
{
  int8_t status;
  arm_broker_interfaces__action__PickPlace_Result result;
} arm_broker_interfaces__action__PickPlace_GetResult_Response;

// Struct for a sequence of arm_broker_interfaces__action__PickPlace_GetResult_Response.
typedef struct arm_broker_interfaces__action__PickPlace_GetResult_Response__Sequence
{
  arm_broker_interfaces__action__PickPlace_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__PickPlace_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"

/// Struct defined in action/PickPlace in the package arm_broker_interfaces.
typedef struct arm_broker_interfaces__action__PickPlace_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  arm_broker_interfaces__action__PickPlace_Feedback feedback;
} arm_broker_interfaces__action__PickPlace_FeedbackMessage;

// Struct for a sequence of arm_broker_interfaces__action__PickPlace_FeedbackMessage.
typedef struct arm_broker_interfaces__action__PickPlace_FeedbackMessage__Sequence
{
  arm_broker_interfaces__action__PickPlace_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_broker_interfaces__action__PickPlace_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_BROKER_INTERFACES__ACTION__DETAIL__PICK_PLACE__STRUCT_H_
