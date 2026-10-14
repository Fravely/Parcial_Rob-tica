// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from arm_broker_interfaces:action/PickPlace.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
#include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "arm_broker_interfaces/action/detail/pick_place__functions.h"
#include "arm_broker_interfaces/action/detail/pick_place__struct.h"


// Include directives for member types
// Member `client_id`
// Member `accion`
// Member `objeto`
// Member `color`
// Member `zona`
// Member `fuente`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__action__PickPlace_Goal__init(message_memory);
}

void arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_fini_function(void * message_memory)
{
  arm_broker_interfaces__action__PickPlace_Goal__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_message_member_array[9] = {
  {
    "client_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, client_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "priority",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, priority),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "accion",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, accion),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "objeto",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, objeto),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "color",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, color),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "zona",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, zona),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "permitido",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, permitido),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "degradada",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, degradada),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "fuente",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Goal, fuente),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_message_members = {
  "arm_broker_interfaces__action",  // message namespace
  "PickPlace_Goal",  // message name
  9,  // number of fields
  sizeof(arm_broker_interfaces__action__PickPlace_Goal),
  arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_message_member_array,  // message members
  arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_message_type_support_handle = {
  0,
  &arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_Goal)() {
  if (!arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__action__PickPlace_Goal__rosidl_typesupport_introspection_c__PickPlace_Goal_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__functions.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"


// Include directives for member types
// Member `message`
// Member `stages`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `stage_time_s`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__action__PickPlace_Result__init(message_memory);
}

void arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_fini_function(void * message_memory)
{
  arm_broker_interfaces__action__PickPlace_Result__fini(message_memory);
}

size_t arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__size_function__PickPlace_Result__stages(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_const_function__PickPlace_Result__stages(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_function__PickPlace_Result__stages(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__fetch_function__PickPlace_Result__stages(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_const_function__PickPlace_Result__stages(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__assign_function__PickPlace_Result__stages(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_function__PickPlace_Result__stages(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__resize_function__PickPlace_Result__stages(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__size_function__PickPlace_Result__stage_time_s(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_const_function__PickPlace_Result__stage_time_s(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_function__PickPlace_Result__stage_time_s(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__fetch_function__PickPlace_Result__stage_time_s(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_const_function__PickPlace_Result__stage_time_s(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__assign_function__PickPlace_Result__stage_time_s(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_function__PickPlace_Result__stage_time_s(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__resize_function__PickPlace_Result__stage_time_s(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_message_member_array[10] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "simulated",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, simulated),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "planning_only",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, planning_only),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "physical_verified",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, physical_verified),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "wait_time_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, wait_time_s),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "exec_time_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, exec_time_s),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stages",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, stages),  // bytes offset in struct
    NULL,  // default value
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__size_function__PickPlace_Result__stages,  // size() function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_const_function__PickPlace_Result__stages,  // get_const(index) function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_function__PickPlace_Result__stages,  // get(index) function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__fetch_function__PickPlace_Result__stages,  // fetch(index, &value) function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__assign_function__PickPlace_Result__stages,  // assign(index, value) function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__resize_function__PickPlace_Result__stages  // resize(index) function pointer
  },
  {
    "stage_time_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, stage_time_s),  // bytes offset in struct
    NULL,  // default value
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__size_function__PickPlace_Result__stage_time_s,  // size() function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_const_function__PickPlace_Result__stage_time_s,  // get_const(index) function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__get_function__PickPlace_Result__stage_time_s,  // get(index) function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__fetch_function__PickPlace_Result__stage_time_s,  // fetch(index, &value) function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__assign_function__PickPlace_Result__stage_time_s,  // assign(index, value) function pointer
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__resize_function__PickPlace_Result__stage_time_s  // resize(index) function pointer
  },
  {
    "position_error_mm",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Result, position_error_mm),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_message_members = {
  "arm_broker_interfaces__action",  // message namespace
  "PickPlace_Result",  // message name
  10,  // number of fields
  sizeof(arm_broker_interfaces__action__PickPlace_Result),
  arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_message_member_array,  // message members
  arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_message_type_support_handle = {
  0,
  &arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_Result)() {
  if (!arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__action__PickPlace_Result__rosidl_typesupport_introspection_c__PickPlace_Result_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__functions.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"


// Include directives for member types
// Member `state`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__action__PickPlace_Feedback__init(message_memory);
}

void arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_fini_function(void * message_memory)
{
  arm_broker_interfaces__action__PickPlace_Feedback__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_message_member_array[3] = {
  {
    "state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Feedback, state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "queue_position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Feedback, queue_position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "elapsed_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_Feedback, elapsed_s),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_message_members = {
  "arm_broker_interfaces__action",  // message namespace
  "PickPlace_Feedback",  // message name
  3,  // number of fields
  sizeof(arm_broker_interfaces__action__PickPlace_Feedback),
  arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_message_member_array,  // message members
  arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_message_type_support_handle = {
  0,
  &arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_Feedback)() {
  if (!arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__action__PickPlace_Feedback__rosidl_typesupport_introspection_c__PickPlace_Feedback_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__functions.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `goal`
#include "arm_broker_interfaces/action/pick_place.h"
// Member `goal`
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__action__PickPlace_SendGoal_Request__init(message_memory);
}

void arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_fini_function(void * message_memory)
{
  arm_broker_interfaces__action__PickPlace_SendGoal_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_SendGoal_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "goal",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_SendGoal_Request, goal),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_members = {
  "arm_broker_interfaces__action",  // message namespace
  "PickPlace_SendGoal_Request",  // message name
  2,  // number of fields
  sizeof(arm_broker_interfaces__action__PickPlace_SendGoal_Request),
  arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_member_array,  // message members
  arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_type_support_handle = {
  0,
  &arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_SendGoal_Request)() {
  arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_Goal)();
  if (!arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__action__PickPlace_SendGoal_Request__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__functions.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__action__PickPlace_SendGoal_Response__init(message_memory);
}

void arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_fini_function(void * message_memory)
{
  arm_broker_interfaces__action__PickPlace_SendGoal_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_member_array[2] = {
  {
    "accepted",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_SendGoal_Response, accepted),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_SendGoal_Response, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_members = {
  "arm_broker_interfaces__action",  // message namespace
  "PickPlace_SendGoal_Response",  // message name
  2,  // number of fields
  sizeof(arm_broker_interfaces__action__PickPlace_SendGoal_Response),
  arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_member_array,  // message members
  arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_type_support_handle = {
  0,
  &arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_SendGoal_Response)() {
  arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__action__PickPlace_SendGoal_Response__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_service_members = {
  "arm_broker_interfaces__action",  // service namespace
  "PickPlace_SendGoal",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Request_message_type_support_handle,
  NULL  // response message
  // arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_Response_message_type_support_handle
};

static rosidl_service_type_support_t arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_service_type_support_handle = {
  0,
  &arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_SendGoal_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_SendGoal_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_SendGoal)() {
  if (!arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_service_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_SendGoal_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_SendGoal_Response)()->data;
  }

  return &arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_SendGoal_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__functions.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__action__PickPlace_GetResult_Request__init(message_memory);
}

void arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_fini_function(void * message_memory)
{
  arm_broker_interfaces__action__PickPlace_GetResult_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_member_array[1] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_GetResult_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_members = {
  "arm_broker_interfaces__action",  // message namespace
  "PickPlace_GetResult_Request",  // message name
  1,  // number of fields
  sizeof(arm_broker_interfaces__action__PickPlace_GetResult_Request),
  arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_member_array,  // message members
  arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_type_support_handle = {
  0,
  &arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_GetResult_Request)() {
  arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  if (!arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__action__PickPlace_GetResult_Request__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__functions.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"


// Include directives for member types
// Member `result`
// already included above
// #include "arm_broker_interfaces/action/pick_place.h"
// Member `result`
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__action__PickPlace_GetResult_Response__init(message_memory);
}

void arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_fini_function(void * message_memory)
{
  arm_broker_interfaces__action__PickPlace_GetResult_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_member_array[2] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_GetResult_Response, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_GetResult_Response, result),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_members = {
  "arm_broker_interfaces__action",  // message namespace
  "PickPlace_GetResult_Response",  // message name
  2,  // number of fields
  sizeof(arm_broker_interfaces__action__PickPlace_GetResult_Response),
  arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_member_array,  // message members
  arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_type_support_handle = {
  0,
  &arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_GetResult_Response)() {
  arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_Result)();
  if (!arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__action__PickPlace_GetResult_Response__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_service_members = {
  "arm_broker_interfaces__action",  // service namespace
  "PickPlace_GetResult",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_Request_message_type_support_handle,
  NULL  // response message
  // arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_Response_message_type_support_handle
};

static rosidl_service_type_support_t arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_service_type_support_handle = {
  0,
  &arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_GetResult_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_GetResult_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_GetResult)() {
  if (!arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_service_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_GetResult_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_GetResult_Response)()->data;
  }

  return &arm_broker_interfaces__action__detail__pick_place__rosidl_typesupport_introspection_c__PickPlace_GetResult_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"
// already included above
// #include "arm_broker_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__functions.h"
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `feedback`
// already included above
// #include "arm_broker_interfaces/action/pick_place.h"
// Member `feedback`
// already included above
// #include "arm_broker_interfaces/action/detail/pick_place__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  arm_broker_interfaces__action__PickPlace_FeedbackMessage__init(message_memory);
}

void arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_fini_function(void * message_memory)
{
  arm_broker_interfaces__action__PickPlace_FeedbackMessage__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_FeedbackMessage, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "feedback",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(arm_broker_interfaces__action__PickPlace_FeedbackMessage, feedback),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_members = {
  "arm_broker_interfaces__action",  // message namespace
  "PickPlace_FeedbackMessage",  // message name
  2,  // number of fields
  sizeof(arm_broker_interfaces__action__PickPlace_FeedbackMessage),
  arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_member_array,  // message members
  arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_type_support_handle = {
  0,
  &arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_FeedbackMessage)() {
  arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, arm_broker_interfaces, action, PickPlace_Feedback)();
  if (!arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_type_support_handle.typesupport_identifier) {
    arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &arm_broker_interfaces__action__PickPlace_FeedbackMessage__rosidl_typesupport_introspection_c__PickPlace_FeedbackMessage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
