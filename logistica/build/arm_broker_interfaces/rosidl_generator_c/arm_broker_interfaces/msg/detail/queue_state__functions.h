// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from arm_broker_interfaces:msg/QueueState.idl
// generated code does not contain a copyright notice

#ifndef ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__FUNCTIONS_H_
#define ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "arm_broker_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "arm_broker_interfaces/msg/detail/queue_state__struct.h"

/// Initialize msg/QueueState message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * arm_broker_interfaces__msg__QueueState
 * )) before or use
 * arm_broker_interfaces__msg__QueueState__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
bool
arm_broker_interfaces__msg__QueueState__init(arm_broker_interfaces__msg__QueueState * msg);

/// Finalize msg/QueueState message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
void
arm_broker_interfaces__msg__QueueState__fini(arm_broker_interfaces__msg__QueueState * msg);

/// Create msg/QueueState message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * arm_broker_interfaces__msg__QueueState__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
arm_broker_interfaces__msg__QueueState *
arm_broker_interfaces__msg__QueueState__create();

/// Destroy msg/QueueState message.
/**
 * It calls
 * arm_broker_interfaces__msg__QueueState__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
void
arm_broker_interfaces__msg__QueueState__destroy(arm_broker_interfaces__msg__QueueState * msg);

/// Check for msg/QueueState message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
bool
arm_broker_interfaces__msg__QueueState__are_equal(const arm_broker_interfaces__msg__QueueState * lhs, const arm_broker_interfaces__msg__QueueState * rhs);

/// Copy a msg/QueueState message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
bool
arm_broker_interfaces__msg__QueueState__copy(
  const arm_broker_interfaces__msg__QueueState * input,
  arm_broker_interfaces__msg__QueueState * output);

/// Initialize array of msg/QueueState messages.
/**
 * It allocates the memory for the number of elements and calls
 * arm_broker_interfaces__msg__QueueState__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
bool
arm_broker_interfaces__msg__QueueState__Sequence__init(arm_broker_interfaces__msg__QueueState__Sequence * array, size_t size);

/// Finalize array of msg/QueueState messages.
/**
 * It calls
 * arm_broker_interfaces__msg__QueueState__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
void
arm_broker_interfaces__msg__QueueState__Sequence__fini(arm_broker_interfaces__msg__QueueState__Sequence * array);

/// Create array of msg/QueueState messages.
/**
 * It allocates the memory for the array and calls
 * arm_broker_interfaces__msg__QueueState__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
arm_broker_interfaces__msg__QueueState__Sequence *
arm_broker_interfaces__msg__QueueState__Sequence__create(size_t size);

/// Destroy array of msg/QueueState messages.
/**
 * It calls
 * arm_broker_interfaces__msg__QueueState__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
void
arm_broker_interfaces__msg__QueueState__Sequence__destroy(arm_broker_interfaces__msg__QueueState__Sequence * array);

/// Check for msg/QueueState message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
bool
arm_broker_interfaces__msg__QueueState__Sequence__are_equal(const arm_broker_interfaces__msg__QueueState__Sequence * lhs, const arm_broker_interfaces__msg__QueueState__Sequence * rhs);

/// Copy an array of msg/QueueState messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_arm_broker_interfaces
bool
arm_broker_interfaces__msg__QueueState__Sequence__copy(
  const arm_broker_interfaces__msg__QueueState__Sequence * input,
  arm_broker_interfaces__msg__QueueState__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ARM_BROKER_INTERFACES__MSG__DETAIL__QUEUE_STATE__FUNCTIONS_H_
