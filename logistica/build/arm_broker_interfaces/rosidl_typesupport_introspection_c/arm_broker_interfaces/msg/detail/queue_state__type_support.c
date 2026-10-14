// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from arm_broker_interfaces:msg/QueueState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "arm_broker_interfaces/msg/detail/queue_state__rosidl_typesupport_introspection_c.h"
#include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "arm_broker_interfaces/msg/detail/queue_state__functions.h"
#include "arm_broker_interfaces/msg/detail/queue_state__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"
// Member `executing_client`
// Member `executing_goal_id`
// Member `queued_goal_ids`
// Member `queued_clients`
#include "rosidl_runtime_c/string_functions.h"
// Member `queued_priorities`
// Member `queued_wait_s`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__msg__QueueState__init(message_memory);
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_fini_function(void * message_memory)
{
  arm_broker_interfaces__msg__QueueState__fini(message_memory);
}

size_t arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__size_function__QueueState__queued_goal_ids(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_goal_ids(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_goal_ids(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__fetch_function__QueueState__queued_goal_ids(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_goal_ids(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__assign_function__QueueState__queued_goal_ids(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_goal_ids(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__resize_function__QueueState__queued_goal_ids(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__size_function__QueueState__queued_clients(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_clients(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_clients(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__fetch_function__QueueState__queued_clients(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_clients(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__assign_function__QueueState__queued_clients(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_clients(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__resize_function__QueueState__queued_clients(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__size_function__QueueState__queued_priorities(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_priorities(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_priorities(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__fetch_function__QueueState__queued_priorities(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_priorities(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__assign_function__QueueState__queued_priorities(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_priorities(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__resize_function__QueueState__queued_priorities(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

size_t arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__size_function__QueueState__queued_wait_s(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_wait_s(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_wait_s(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__fetch_function__QueueState__queued_wait_s(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_wait_s(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__assign_function__QueueState__queued_wait_s(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_wait_s(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__resize_function__QueueState__queued_wait_s(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_member_array[12] = {
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "executing_client",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, executing_client),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "executing_goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, executing_goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "executing_elapsed_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, executing_elapsed_s),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "queue_length",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, queue_length),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "queued_goal_ids",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, queued_goal_ids),  // bytes offset in struct
    NULL,  // default value
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__size_function__QueueState__queued_goal_ids,  // size() function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_goal_ids,  // get_const(index) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_goal_ids,  // get(index) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__fetch_function__QueueState__queued_goal_ids,  // fetch(index, &value) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__assign_function__QueueState__queued_goal_ids,  // assign(index, value) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__resize_function__QueueState__queued_goal_ids  // resize(index) function pointer
  },
  {
    "queued_clients",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, queued_clients),  // bytes offset in struct
    NULL,  // default value
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__size_function__QueueState__queued_clients,  // size() function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_clients,  // get_const(index) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_clients,  // get(index) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__fetch_function__QueueState__queued_clients,  // fetch(index, &value) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__assign_function__QueueState__queued_clients,  // assign(index, value) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__resize_function__QueueState__queued_clients  // resize(index) function pointer
  },
  {
    "queued_priorities",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, queued_priorities),  // bytes offset in struct
    NULL,  // default value
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__size_function__QueueState__queued_priorities,  // size() function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_priorities,  // get_const(index) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_priorities,  // get(index) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__fetch_function__QueueState__queued_priorities,  // fetch(index, &value) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__assign_function__QueueState__queued_priorities,  // assign(index, value) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__resize_function__QueueState__queued_priorities  // resize(index) function pointer
  },
  {
    "queued_wait_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, queued_wait_s),  // bytes offset in struct
    NULL,  // default value
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__size_function__QueueState__queued_wait_s,  // size() function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_const_function__QueueState__queued_wait_s,  // get_const(index) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__get_function__QueueState__queued_wait_s,  // get(index) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__fetch_function__QueueState__queued_wait_s,  // fetch(index, &value) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__assign_function__QueueState__queued_wait_s,  // assign(index, value) function pointer
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__resize_function__QueueState__queued_wait_s  // resize(index) function pointer
  },
  {
    "total_accepted",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, total_accepted),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "total_rejected",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, total_rejected),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "total_completed",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__msg__QueueState, total_completed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_members = {
  "arm_broker_interfaces__msg",  // message namespace
  "QueueState",  // message name
  12,  // number of fields
  sizeof(arm_broker_interfaces__msg__QueueState),
  arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_member_array,  // message members
  arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_type_support_handle = {
  0,
  &arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, msg, QueueState)() {
  arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__msg__QueueState__rosidl_typesupport_introspection_c__QueueState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
