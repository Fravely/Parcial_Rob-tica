// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
// generated code does not contain a copyright notice
#include "laya_ordenes_interfaces/srv/detail/interpretar_orden__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `frase`
#include "rosidl_runtime_c/string_functions.h"

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Request__init(laya_ordenes_interfaces__srv__InterpretarOrden_Request * msg)
{
  if (!msg) {
    return false;
  }
  // frase
  if (!rosidl_runtime_c__String__init(&msg->frase)) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Request__fini(msg);
    return false;
  }
  return true;
}

void
laya_ordenes_interfaces__srv__InterpretarOrden_Request__fini(laya_ordenes_interfaces__srv__InterpretarOrden_Request * msg)
{
  if (!msg) {
    return;
  }
  // frase
  rosidl_runtime_c__String__fini(&msg->frase);
}

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Request__are_equal(const laya_ordenes_interfaces__srv__InterpretarOrden_Request * lhs, const laya_ordenes_interfaces__srv__InterpretarOrden_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // frase
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->frase), &(rhs->frase)))
  {
    return false;
  }
  return true;
}

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Request__copy(
  const laya_ordenes_interfaces__srv__InterpretarOrden_Request * input,
  laya_ordenes_interfaces__srv__InterpretarOrden_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // frase
  if (!rosidl_runtime_c__String__copy(
      &(input->frase), &(output->frase)))
  {
    return false;
  }
  return true;
}

laya_ordenes_interfaces__srv__InterpretarOrden_Request *
laya_ordenes_interfaces__srv__InterpretarOrden_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  laya_ordenes_interfaces__srv__InterpretarOrden_Request * msg = (laya_ordenes_interfaces__srv__InterpretarOrden_Request *)allocator.allocate(sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Request));
  bool success = laya_ordenes_interfaces__srv__InterpretarOrden_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
laya_ordenes_interfaces__srv__InterpretarOrden_Request__destroy(laya_ordenes_interfaces__srv__InterpretarOrden_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence__init(laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  laya_ordenes_interfaces__srv__InterpretarOrden_Request * data = NULL;

  if (size) {
    data = (laya_ordenes_interfaces__srv__InterpretarOrden_Request *)allocator.zero_allocate(size, sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = laya_ordenes_interfaces__srv__InterpretarOrden_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        laya_ordenes_interfaces__srv__InterpretarOrden_Request__fini(&data[i - 1]);
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
laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence__fini(laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence * array)
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
      laya_ordenes_interfaces__srv__InterpretarOrden_Request__fini(&array->data[i]);
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

laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence *
laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence * array = (laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence *)allocator.allocate(sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence__destroy(laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence__are_equal(const laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence * lhs, const laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!laya_ordenes_interfaces__srv__InterpretarOrden_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence__copy(
  const laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence * input,
  laya_ordenes_interfaces__srv__InterpretarOrden_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    laya_ordenes_interfaces__srv__InterpretarOrden_Request * data =
      (laya_ordenes_interfaces__srv__InterpretarOrden_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!laya_ordenes_interfaces__srv__InterpretarOrden_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          laya_ordenes_interfaces__srv__InterpretarOrden_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!laya_ordenes_interfaces__srv__InterpretarOrden_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `accion`
// Member `objeto`
// Member `color`
// Member `fuente`
// Member `motivo`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Response__init(laya_ordenes_interfaces__srv__InterpretarOrden_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accion
  if (!rosidl_runtime_c__String__init(&msg->accion)) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(msg);
    return false;
  }
  // objeto
  if (!rosidl_runtime_c__String__init(&msg->objeto)) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(msg);
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__init(&msg->color)) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(msg);
    return false;
  }
  // prioridad
  // permitido
  // degradada
  // fuente
  if (!rosidl_runtime_c__String__init(&msg->fuente)) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(msg);
    return false;
  }
  // motivo
  if (!rosidl_runtime_c__String__init(&msg->motivo)) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(msg);
    return false;
  }
  // latencia_http_ms
  // inferencia_ms
  // resto_http_ms
  return true;
}

void
laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(laya_ordenes_interfaces__srv__InterpretarOrden_Response * msg)
{
  if (!msg) {
    return;
  }
  // accion
  rosidl_runtime_c__String__fini(&msg->accion);
  // objeto
  rosidl_runtime_c__String__fini(&msg->objeto);
  // color
  rosidl_runtime_c__String__fini(&msg->color);
  // prioridad
  // permitido
  // degradada
  // fuente
  rosidl_runtime_c__String__fini(&msg->fuente);
  // motivo
  rosidl_runtime_c__String__fini(&msg->motivo);
  // latencia_http_ms
  // inferencia_ms
  // resto_http_ms
}

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Response__are_equal(const laya_ordenes_interfaces__srv__InterpretarOrden_Response * lhs, const laya_ordenes_interfaces__srv__InterpretarOrden_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accion
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->accion), &(rhs->accion)))
  {
    return false;
  }
  // objeto
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->objeto), &(rhs->objeto)))
  {
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->color), &(rhs->color)))
  {
    return false;
  }
  // prioridad
  if (lhs->prioridad != rhs->prioridad) {
    return false;
  }
  // permitido
  if (lhs->permitido != rhs->permitido) {
    return false;
  }
  // degradada
  if (lhs->degradada != rhs->degradada) {
    return false;
  }
  // fuente
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->fuente), &(rhs->fuente)))
  {
    return false;
  }
  // motivo
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->motivo), &(rhs->motivo)))
  {
    return false;
  }
  // latencia_http_ms
  if (lhs->latencia_http_ms != rhs->latencia_http_ms) {
    return false;
  }
  // inferencia_ms
  if (lhs->inferencia_ms != rhs->inferencia_ms) {
    return false;
  }
  // resto_http_ms
  if (lhs->resto_http_ms != rhs->resto_http_ms) {
    return false;
  }
  return true;
}

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Response__copy(
  const laya_ordenes_interfaces__srv__InterpretarOrden_Response * input,
  laya_ordenes_interfaces__srv__InterpretarOrden_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accion
  if (!rosidl_runtime_c__String__copy(
      &(input->accion), &(output->accion)))
  {
    return false;
  }
  // objeto
  if (!rosidl_runtime_c__String__copy(
      &(input->objeto), &(output->objeto)))
  {
    return false;
  }
  // color
  if (!rosidl_runtime_c__String__copy(
      &(input->color), &(output->color)))
  {
    return false;
  }
  // prioridad
  output->prioridad = input->prioridad;
  // permitido
  output->permitido = input->permitido;
  // degradada
  output->degradada = input->degradada;
  // fuente
  if (!rosidl_runtime_c__String__copy(
      &(input->fuente), &(output->fuente)))
  {
    return false;
  }
  // motivo
  if (!rosidl_runtime_c__String__copy(
      &(input->motivo), &(output->motivo)))
  {
    return false;
  }
  // latencia_http_ms
  output->latencia_http_ms = input->latencia_http_ms;
  // inferencia_ms
  output->inferencia_ms = input->inferencia_ms;
  // resto_http_ms
  output->resto_http_ms = input->resto_http_ms;
  return true;
}

laya_ordenes_interfaces__srv__InterpretarOrden_Response *
laya_ordenes_interfaces__srv__InterpretarOrden_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  laya_ordenes_interfaces__srv__InterpretarOrden_Response * msg = (laya_ordenes_interfaces__srv__InterpretarOrden_Response *)allocator.allocate(sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Response));
  bool success = laya_ordenes_interfaces__srv__InterpretarOrden_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
laya_ordenes_interfaces__srv__InterpretarOrden_Response__destroy(laya_ordenes_interfaces__srv__InterpretarOrden_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence__init(laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  laya_ordenes_interfaces__srv__InterpretarOrden_Response * data = NULL;

  if (size) {
    data = (laya_ordenes_interfaces__srv__InterpretarOrden_Response *)allocator.zero_allocate(size, sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = laya_ordenes_interfaces__srv__InterpretarOrden_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(&data[i - 1]);
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
laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence__fini(laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence * array)
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
      laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(&array->data[i]);
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

laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence *
laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence * array = (laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence *)allocator.allocate(sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence__destroy(laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence__are_equal(const laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence * lhs, const laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!laya_ordenes_interfaces__srv__InterpretarOrden_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence__copy(
  const laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence * input,
  laya_ordenes_interfaces__srv__InterpretarOrden_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(laya_ordenes_interfaces__srv__InterpretarOrden_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    laya_ordenes_interfaces__srv__InterpretarOrden_Response * data =
      (laya_ordenes_interfaces__srv__InterpretarOrden_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!laya_ordenes_interfaces__srv__InterpretarOrden_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          laya_ordenes_interfaces__srv__InterpretarOrden_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!laya_ordenes_interfaces__srv__InterpretarOrden_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
