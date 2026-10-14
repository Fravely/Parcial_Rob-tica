// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from arm_broker_interfaces:msg/QueueState.idl
// generated code does not contain a copyright notice
#include "arm_broker_interfaces/msg/detail/queue_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `executing_client`
// Member `executing_goal_id`
// Member `queued_goal_ids`
// Member `queued_clients`
#include "rosidl_runtime_c/string_functions.h"
// Member `queued_priorities`
// Member `queued_wait_s`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
arm_broker_interfaces__msg__QueueState__init(arm_broker_interfaces__msg__QueueState * msg)
{
  if (!msg) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    arm_broker_interfaces__msg__QueueState__fini(msg);
    return false;
  }
  // executing_client
  if (!rosidl_runtime_c__String__init(&msg->executing_client)) {
    arm_broker_interfaces__msg__QueueState__fini(msg);
    return false;
  }
  // executing_goal_id
  if (!rosidl_runtime_c__String__init(&msg->executing_goal_id)) {
    arm_broker_interfaces__msg__QueueState__fini(msg);
    return false;
  }
  // executing_elapsed_s
  // queue_length
  // queued_goal_ids
  if (!rosidl_runtime_c__String__Sequence__init(&msg->queued_goal_ids, 0)) {
    arm_broker_interfaces__msg__QueueState__fini(msg);
    return false;
  }
  // queued_clients
  if (!rosidl_runtime_c__String__Sequence__init(&msg->queued_clients, 0)) {
    arm_broker_interfaces__msg__QueueState__fini(msg);
    return false;
  }
  // queued_priorities
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->queued_priorities, 0)) {
    arm_broker_interfaces__msg__QueueState__fini(msg);
    return false;
  }
  // queued_wait_s
  if (!rosidl_runtime_c__double__Sequence__init(&msg->queued_wait_s, 0)) {
    arm_broker_interfaces__msg__QueueState__fini(msg);
    return false;
  }
  // total_accepted
  // total_rejected
  // total_completed
  return true;
}

void
arm_broker_interfaces__msg__QueueState__fini(arm_broker_interfaces__msg__QueueState * msg)
{
  if (!msg) {
    return;
  }
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
  // executing_client
  rosidl_runtime_c__String__fini(&msg->executing_client);
  // executing_goal_id
  rosidl_runtime_c__String__fini(&msg->executing_goal_id);
  // executing_elapsed_s
  // queue_length
  // queued_goal_ids
  rosidl_runtime_c__String__Sequence__fini(&msg->queued_goal_ids);
  // queued_clients
  rosidl_runtime_c__String__Sequence__fini(&msg->queued_clients);
  // queued_priorities
  rosidl_runtime_c__uint8__Sequence__fini(&msg->queued_priorities);
  // queued_wait_s
  rosidl_runtime_c__double__Sequence__fini(&msg->queued_wait_s);
  // total_accepted
  // total_rejected
  // total_completed
}

bool
arm_broker_interfaces__msg__QueueState__are_equal(const arm_broker_interfaces__msg__QueueState * lhs, const arm_broker_interfaces__msg__QueueState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  // executing_client
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->executing_client), &(rhs->executing_client)))
  {
    return false;
  }
  // executing_goal_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->executing_goal_id), &(rhs->executing_goal_id)))
  {
    return false;
  }
  // executing_elapsed_s
  if (lhs->executing_elapsed_s != rhs->executing_elapsed_s) {
    return false;
  }
  // queue_length
  if (lhs->queue_length != rhs->queue_length) {
    return false;
  }
  // queued_goal_ids
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->queued_goal_ids), &(rhs->queued_goal_ids)))
  {
    return false;
  }
  // queued_clients
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->queued_clients), &(rhs->queued_clients)))
  {
    return false;
  }
  // queued_priorities
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->queued_priorities), &(rhs->queued_priorities)))
  {
    return false;
  }
  // queued_wait_s
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->queued_wait_s), &(rhs->queued_wait_s)))
  {
    return false;
  }
  // total_accepted
  if (lhs->total_accepted != rhs->total_accepted) {
    return false;
  }
  // total_rejected
  if (lhs->total_rejected != rhs->total_rejected) {
    return false;
  }
  // total_completed
  if (lhs->total_completed != rhs->total_completed) {
    return false;
  }
  return true;
}

bool
arm_broker_interfaces__msg__QueueState__copy(
  const arm_broker_interfaces__msg__QueueState * input,
  arm_broker_interfaces__msg__QueueState * output)
{
  if (!input || !output) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  // executing_client
  if (!rosidl_runtime_c__String__copy(
      &(input->executing_client), &(output->executing_client)))
  {
    return false;
  }
  // executing_goal_id
  if (!rosidl_runtime_c__String__copy(
      &(input->executing_goal_id), &(output->executing_goal_id)))
  {
    return false;
  }
  // executing_elapsed_s
  output->executing_elapsed_s = input->executing_elapsed_s;
  // queue_length
  output->queue_length = input->queue_length;
  // queued_goal_ids
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->queued_goal_ids), &(output->queued_goal_ids)))
  {
    return false;
  }
  // queued_clients
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->queued_clients), &(output->queued_clients)))
  {
    return false;
  }
  // queued_priorities
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->queued_priorities), &(output->queued_priorities)))
  {
    return false;
  }
  // queued_wait_s
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->queued_wait_s), &(output->queued_wait_s)))
  {
    return false;
  }
  // total_accepted
  output->total_accepted = input->total_accepted;
  // total_rejected
  output->total_rejected = input->total_rejected;
  // total_completed
  output->total_completed = input->total_completed;
  return true;
}

arm_broker_interfaces__msg__QueueState *
arm_broker_interfaces__msg__QueueState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_broker_interfaces__msg__QueueState * msg = (arm_broker_interfaces__msg__QueueState *)allocator.allocate(sizeof(arm_broker_interfaces__msg__QueueState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(arm_broker_interfaces__msg__QueueState));
  bool success = arm_broker_interfaces__msg__QueueState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
arm_broker_interfaces__msg__QueueState__destroy(arm_broker_interfaces__msg__QueueState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    arm_broker_interfaces__msg__QueueState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
arm_broker_interfaces__msg__QueueState__Sequence__init(arm_broker_interfaces__msg__QueueState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_broker_interfaces__msg__QueueState * data = NULL;

  if (size) {
    data = (arm_broker_interfaces__msg__QueueState *)allocator.zero_allocate(size, sizeof(arm_broker_interfaces__msg__QueueState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = arm_broker_interfaces__msg__QueueState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        arm_broker_interfaces__msg__QueueState__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
arm_broker_interfaces__msg__QueueState__Sequence__fini(arm_broker_interfaces__msg__QueueState__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      arm_broker_interfaces__msg__QueueState__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

arm_broker_interfaces__msg__QueueState__Sequence *
arm_broker_interfaces__msg__QueueState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  arm_broker_interfaces__msg__QueueState__Sequence * array = (arm_broker_interfaces__msg__QueueState__Sequence *)allocator.allocate(sizeof(arm_broker_interfaces__msg__QueueState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = arm_broker_interfaces__msg__QueueState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
arm_broker_interfaces__msg__QueueState__Sequence__destroy(arm_broker_interfaces__msg__QueueState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    arm_broker_interfaces__msg__QueueState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
arm_broker_interfaces__msg__QueueState__Sequence__are_equal(const arm_broker_interfaces__msg__QueueState__Sequence * lhs, const arm_broker_interfaces__msg__QueueState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!arm_broker_interfaces__msg__QueueState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
arm_broker_interfaces__msg__QueueState__Sequence__copy(
  const arm_broker_interfaces__msg__QueueState__Sequence * input,
  arm_broker_interfaces__msg__QueueState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(arm_broker_interfaces__msg__QueueState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    arm_broker_interfaces__msg__QueueState * data =
      (arm_broker_interfaces__msg__QueueState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!arm_broker_interfaces__msg__QueueState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          arm_broker_interfaces__msg__QueueState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!arm_broker_interfaces__msg__QueueState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
