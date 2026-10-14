// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from arm_broker_interfaces:msg/QueueState.idl
// generated code does not contain a copyright notice
#include "arm_broker_interfaces/msg/detail/queue_state__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "arm_broker_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "arm_broker_interfaces/msg/detail/queue_state__struct.h"
#include "arm_broker_interfaces/msg/detail/queue_state__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "builtin_interfaces/msg/detail/time__functions.h"  // stamp
#include "rosidl_runtime_c/primitives_sequence.h"  // queued_priorities, queued_wait_s
#include "rosidl_runtime_c/primitives_sequence_functions.h"  // queued_priorities, queued_wait_s
#include "rosidl_runtime_c/string.h"  // executing_client, executing_goal_id, queued_clients, queued_goal_ids
#include "rosidl_runtime_c/string_functions.h"  // executing_client, executing_goal_id, queued_clients, queued_goal_ids

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_arm_broker_interfaces
size_t get_serialized_size_builtin_interfaces__msg__Time(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_arm_broker_interfaces
size_t max_serialized_size_builtin_interfaces__msg__Time(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_arm_broker_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, builtin_interfaces, msg, Time)();


using _QueueState__ros_msg_type = arm_broker_interfaces__msg__QueueState;

static bool _QueueState__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _QueueState__ros_msg_type * ros_message = static_cast<const _QueueState__ros_msg_type *>(untyped_ros_message);
  // Field name: stamp
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, builtin_interfaces, msg, Time
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->stamp, cdr))
    {
      return false;
    }
  }

  // Field name: executing_client
  {
    const rosidl_runtime_c__String * str = &ros_message->executing_client;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: executing_goal_id
  {
    const rosidl_runtime_c__String * str = &ros_message->executing_goal_id;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: executing_elapsed_s
  {
    cdr << ros_message->executing_elapsed_s;
  }

  // Field name: queue_length
  {
    cdr << ros_message->queue_length;
  }

  // Field name: queued_goal_ids
  {
    size_t size = ros_message->queued_goal_ids.size;
    auto array_ptr = ros_message->queued_goal_ids.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      const rosidl_runtime_c__String * str = &array_ptr[i];
      if (str->capacity == 0 || str->capacity <= str->size) {
        fprintf(stderr, "string capacity not greater than size\n");
        return false;
      }
      if (str->data[str->size] != '\0') {
        fprintf(stderr, "string not null-terminated\n");
        return false;
      }
      cdr << str->data;
    }
  }

  // Field name: queued_clients
  {
    size_t size = ros_message->queued_clients.size;
    auto array_ptr = ros_message->queued_clients.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      const rosidl_runtime_c__String * str = &array_ptr[i];
      if (str->capacity == 0 || str->capacity <= str->size) {
        fprintf(stderr, "string capacity not greater than size\n");
        return false;
      }
      if (str->data[str->size] != '\0') {
        fprintf(stderr, "string not null-terminated\n");
        return false;
      }
      cdr << str->data;
    }
  }

  // Field name: queued_priorities
  {
    size_t size = ros_message->queued_priorities.size;
    auto array_ptr = ros_message->queued_priorities.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: queued_wait_s
  {
    size_t size = ros_message->queued_wait_s.size;
    auto array_ptr = ros_message->queued_wait_s.data;
    cdr << static_cast<uint32_t>(size);
    cdr.serializeArray(array_ptr, size);
  }

  // Field name: total_accepted
  {
    cdr << ros_message->total_accepted;
  }

  // Field name: total_rejected
  {
    cdr << ros_message->total_rejected;
  }

  // Field name: total_completed
  {
    cdr << ros_message->total_completed;
  }

  return true;
}

static bool _QueueState__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _QueueState__ros_msg_type * ros_message = static_cast<_QueueState__ros_msg_type *>(untyped_ros_message);
  // Field name: stamp
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, builtin_interfaces, msg, Time
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->stamp))
    {
      return false;
    }
  }

  // Field name: executing_client
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->executing_client.data) {
      rosidl_runtime_c__String__init(&ros_message->executing_client);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->executing_client,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'executing_client'\n");
      return false;
    }
  }

  // Field name: executing_goal_id
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->executing_goal_id.data) {
      rosidl_runtime_c__String__init(&ros_message->executing_goal_id);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->executing_goal_id,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'executing_goal_id'\n");
      return false;
    }
  }

  // Field name: executing_elapsed_s
  {
    cdr >> ros_message->executing_elapsed_s;
  }

  // Field name: queue_length
  {
    cdr >> ros_message->queue_length;
  }

  // Field name: queued_goal_ids
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->queued_goal_ids.data) {
      rosidl_runtime_c__String__Sequence__fini(&ros_message->queued_goal_ids);
    }
    if (!rosidl_runtime_c__String__Sequence__init(&ros_message->queued_goal_ids, size)) {
      fprintf(stderr, "failed to create array for field 'queued_goal_ids'");
      return false;
    }
    auto array_ptr = ros_message->queued_goal_ids.data;
    for (size_t i = 0; i < size; ++i) {
      std::string tmp;
      cdr >> tmp;
      auto & ros_i = array_ptr[i];
      if (!ros_i.data) {
        rosidl_runtime_c__String__init(&ros_i);
      }
      bool succeeded = rosidl_runtime_c__String__assign(
        &ros_i,
        tmp.c_str());
      if (!succeeded) {
        fprintf(stderr, "failed to assign string into field 'queued_goal_ids'\n");
        return false;
      }
    }
  }

  // Field name: queued_clients
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->queued_clients.data) {
      rosidl_runtime_c__String__Sequence__fini(&ros_message->queued_clients);
    }
    if (!rosidl_runtime_c__String__Sequence__init(&ros_message->queued_clients, size)) {
      fprintf(stderr, "failed to create array for field 'queued_clients'");
      return false;
    }
    auto array_ptr = ros_message->queued_clients.data;
    for (size_t i = 0; i < size; ++i) {
      std::string tmp;
      cdr >> tmp;
      auto & ros_i = array_ptr[i];
      if (!ros_i.data) {
        rosidl_runtime_c__String__init(&ros_i);
      }
      bool succeeded = rosidl_runtime_c__String__assign(
        &ros_i,
        tmp.c_str());
      if (!succeeded) {
        fprintf(stderr, "failed to assign string into field 'queued_clients'\n");
        return false;
      }
    }
  }

  // Field name: queued_priorities
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->queued_priorities.data) {
      rosidl_runtime_c__uint8__Sequence__fini(&ros_message->queued_priorities);
    }
    if (!rosidl_runtime_c__uint8__Sequence__init(&ros_message->queued_priorities, size)) {
      fprintf(stderr, "failed to create array for field 'queued_priorities'");
      return false;
    }
    auto array_ptr = ros_message->queued_priorities.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: queued_wait_s
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);
    if (ros_message->queued_wait_s.data) {
      rosidl_runtime_c__double__Sequence__fini(&ros_message->queued_wait_s);
    }
    if (!rosidl_runtime_c__double__Sequence__init(&ros_message->queued_wait_s, size)) {
      fprintf(stderr, "failed to create array for field 'queued_wait_s'");
      return false;
    }
    auto array_ptr = ros_message->queued_wait_s.data;
    cdr.deserializeArray(array_ptr, size);
  }

  // Field name: total_accepted
  {
    cdr >> ros_message->total_accepted;
  }

  // Field name: total_rejected
  {
    cdr >> ros_message->total_rejected;
  }

  // Field name: total_completed
  {
    cdr >> ros_message->total_completed;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_arm_broker_interfaces
size_t get_serialized_size_arm_broker_interfaces__msg__QueueState(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _QueueState__ros_msg_type * ros_message = static_cast<const _QueueState__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name stamp

  current_alignment += get_serialized_size_builtin_interfaces__msg__Time(
    &(ros_message->stamp), current_alignment);
  // field.name executing_client
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->executing_client.size + 1);
  // field.name executing_goal_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->executing_goal_id.size + 1);
  // field.name executing_elapsed_s
  {
    size_t item_size = sizeof(ros_message->executing_elapsed_s);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name queue_length
  {
    size_t item_size = sizeof(ros_message->queue_length);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name queued_goal_ids
  {
    size_t array_size = ros_message->queued_goal_ids.size;
    auto array_ptr = ros_message->queued_goal_ids.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (array_ptr[index].size + 1);
    }
  }
  // field.name queued_clients
  {
    size_t array_size = ros_message->queued_clients.size;
    auto array_ptr = ros_message->queued_clients.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (array_ptr[index].size + 1);
    }
  }
  // field.name queued_priorities
  {
    size_t array_size = ros_message->queued_priorities.size;
    auto array_ptr = ros_message->queued_priorities.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name queued_wait_s
  {
    size_t array_size = ros_message->queued_wait_s.size;
    auto array_ptr = ros_message->queued_wait_s.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    (void)array_ptr;
    size_t item_size = sizeof(array_ptr[0]);
    current_alignment += array_size * item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name total_accepted
  {
    size_t item_size = sizeof(ros_message->total_accepted);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name total_rejected
  {
    size_t item_size = sizeof(ros_message->total_rejected);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name total_completed
  {
    size_t item_size = sizeof(ros_message->total_completed);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _QueueState__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_arm_broker_interfaces__msg__QueueState(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_arm_broker_interfaces
size_t max_serialized_size_arm_broker_interfaces__msg__QueueState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: stamp
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_builtin_interfaces__msg__Time(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: executing_client
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: executing_goal_id
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: executing_elapsed_s
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: queue_length
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: queued_goal_ids
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: queued_clients
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: queued_priorities
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: queued_wait_s
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: total_accepted
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: total_rejected
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: total_completed
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = arm_broker_interfaces__msg__QueueState;
    is_plain =
      (
      offsetof(DataType, total_completed) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _QueueState__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_arm_broker_interfaces__msg__QueueState(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_QueueState = {
  "arm_broker_interfaces::msg",
  "QueueState",
  _QueueState__cdr_serialize,
  _QueueState__cdr_deserialize,
  _QueueState__get_serialized_size,
  _QueueState__max_serialized_size
};

static rosidl_message_type_support_t _QueueState__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_QueueState,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, arm_broker_interfaces, msg, QueueState)() {
  return &_QueueState__type_support;
}

#if defined(__cplusplus)
}
#endif
