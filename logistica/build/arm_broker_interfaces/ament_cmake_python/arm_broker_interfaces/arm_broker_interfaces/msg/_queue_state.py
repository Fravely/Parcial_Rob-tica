# generated from rosidl_generator_py/resource/_idl.py.em
# with input from arm_broker_interfaces:msg/QueueState.idl
# generated code does not contain a copyright notice


# Import statements for member types

# Member 'queued_priorities'
# Member 'queued_wait_s'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_QueueState(type):
    """Metaclass of message 'QueueState'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('arm_broker_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'arm_broker_interfaces.msg.QueueState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__queue_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__queue_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__queue_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__queue_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__queue_state

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class QueueState(metaclass=Metaclass_QueueState):
    """Message class 'QueueState'."""

    __slots__ = [
        '_stamp',
        '_executing_client',
        '_executing_goal_id',
        '_executing_elapsed_s',
        '_queue_length',
        '_queued_goal_ids',
        '_queued_clients',
        '_queued_priorities',
        '_queued_wait_s',
        '_total_accepted',
        '_total_rejected',
        '_total_completed',
    ]

    _fields_and_field_types = {
        'stamp': 'builtin_interfaces/Time',
        'executing_client': 'string',
        'executing_goal_id': 'string',
        'executing_elapsed_s': 'double',
        'queue_length': 'int32',
        'queued_goal_ids': 'sequence<string>',
        'queued_clients': 'sequence<string>',
        'queued_priorities': 'sequence<uint8>',
        'queued_wait_s': 'sequence<double>',
        'total_accepted': 'int32',
        'total_rejected': 'int32',
        'total_completed': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from builtin_interfaces.msg import Time
        self.stamp = kwargs.get('stamp', Time())
        self.executing_client = kwargs.get('executing_client', str())
        self.executing_goal_id = kwargs.get('executing_goal_id', str())
        self.executing_elapsed_s = kwargs.get('executing_elapsed_s', float())
        self.queue_length = kwargs.get('queue_length', int())
        self.queued_goal_ids = kwargs.get('queued_goal_ids', [])
        self.queued_clients = kwargs.get('queued_clients', [])
        self.queued_priorities = array.array('B', kwargs.get('queued_priorities', []))
        self.queued_wait_s = array.array('d', kwargs.get('queued_wait_s', []))
        self.total_accepted = kwargs.get('total_accepted', int())
        self.total_rejected = kwargs.get('total_rejected', int())
        self.total_completed = kwargs.get('total_completed', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.stamp != other.stamp:
            return False
        if self.executing_client != other.executing_client:
            return False
        if self.executing_goal_id != other.executing_goal_id:
            return False
        if self.executing_elapsed_s != other.executing_elapsed_s:
            return False
        if self.queue_length != other.queue_length:
            return False
        if self.queued_goal_ids != other.queued_goal_ids:
            return False
        if self.queued_clients != other.queued_clients:
            return False
        if self.queued_priorities != other.queued_priorities:
            return False
        if self.queued_wait_s != other.queued_wait_s:
            return False
        if self.total_accepted != other.total_accepted:
            return False
        if self.total_rejected != other.total_rejected:
            return False
        if self.total_completed != other.total_completed:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def stamp(self):
        """Message field 'stamp'."""
        return self._stamp

    @stamp.setter
    def stamp(self, value):
        if __debug__:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'stamp' field must be a sub message of type 'Time'"
        self._stamp = value

    @builtins.property
    def executing_client(self):
        """Message field 'executing_client'."""
        return self._executing_client

    @executing_client.setter
    def executing_client(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'executing_client' field must be of type 'str'"
        self._executing_client = value

    @builtins.property
    def executing_goal_id(self):
        """Message field 'executing_goal_id'."""
        return self._executing_goal_id

    @executing_goal_id.setter
    def executing_goal_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'executing_goal_id' field must be of type 'str'"
        self._executing_goal_id = value

    @builtins.property
    def executing_elapsed_s(self):
        """Message field 'executing_elapsed_s'."""
        return self._executing_elapsed_s

    @executing_elapsed_s.setter
    def executing_elapsed_s(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'executing_elapsed_s' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'executing_elapsed_s' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._executing_elapsed_s = value

    @builtins.property
    def queue_length(self):
        """Message field 'queue_length'."""
        return self._queue_length

    @queue_length.setter
    def queue_length(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'queue_length' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'queue_length' field must be an integer in [-2147483648, 2147483647]"
        self._queue_length = value

    @builtins.property
    def queued_goal_ids(self):
        """Message field 'queued_goal_ids'."""
        return self._queued_goal_ids

    @queued_goal_ids.setter
    def queued_goal_ids(self, value):
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'queued_goal_ids' field must be a set or sequence and each value of type 'str'"
        self._queued_goal_ids = value

    @builtins.property
    def queued_clients(self):
        """Message field 'queued_clients'."""
        return self._queued_clients

    @queued_clients.setter
    def queued_clients(self, value):
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'queued_clients' field must be a set or sequence and each value of type 'str'"
        self._queued_clients = value

    @builtins.property
    def queued_priorities(self):
        """Message field 'queued_priorities'."""
        return self._queued_priorities

    @queued_priorities.setter
    def queued_priorities(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'B', \
                "The 'queued_priorities' array.array() must have the type code of 'B'"
            self._queued_priorities = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'queued_priorities' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 255]"
        self._queued_priorities = array.array('B', value)

    @builtins.property
    def queued_wait_s(self):
        """Message field 'queued_wait_s'."""
        return self._queued_wait_s

    @queued_wait_s.setter
    def queued_wait_s(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'queued_wait_s' array.array() must have the type code of 'd'"
            self._queued_wait_s = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'queued_wait_s' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._queued_wait_s = array.array('d', value)

    @builtins.property
    def total_accepted(self):
        """Message field 'total_accepted'."""
        return self._total_accepted

    @total_accepted.setter
    def total_accepted(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'total_accepted' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'total_accepted' field must be an integer in [-2147483648, 2147483647]"
        self._total_accepted = value

    @builtins.property
    def total_rejected(self):
        """Message field 'total_rejected'."""
        return self._total_rejected

    @total_rejected.setter
    def total_rejected(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'total_rejected' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'total_rejected' field must be an integer in [-2147483648, 2147483647]"
        self._total_rejected = value

    @builtins.property
    def total_completed(self):
        """Message field 'total_completed'."""
        return self._total_completed

    @total_completed.setter
    def total_completed(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'total_completed' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'total_completed' field must be an integer in [-2147483648, 2147483647]"
        self._total_completed = value
