# generated from rosidl_generator_py/resource/_idl.py.em
# with input from arm_broker_interfaces:action/PickPlace.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_PickPlace_Goal(type):
    """Metaclass of message 'PickPlace_Goal'."""

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
                'arm_broker_interfaces.action.PickPlace_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__pick_place__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__pick_place__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__pick_place__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__pick_place__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__pick_place__goal

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PickPlace_Goal(metaclass=Metaclass_PickPlace_Goal):
    """Message class 'PickPlace_Goal'."""

    __slots__ = [
        '_client_id',
        '_priority',
        '_accion',
        '_objeto',
        '_color',
        '_zona',
        '_permitido',
        '_degradada',
        '_fuente',
    ]

    _fields_and_field_types = {
        'client_id': 'string',
        'priority': 'uint8',
        'accion': 'string',
        'objeto': 'string',
        'color': 'string',
        'zona': 'string',
        'permitido': 'boolean',
        'degradada': 'boolean',
        'fuente': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.client_id = kwargs.get('client_id', str())
        self.priority = kwargs.get('priority', int())
        self.accion = kwargs.get('accion', str())
        self.objeto = kwargs.get('objeto', str())
        self.color = kwargs.get('color', str())
        self.zona = kwargs.get('zona', str())
        self.permitido = kwargs.get('permitido', bool())
        self.degradada = kwargs.get('degradada', bool())
        self.fuente = kwargs.get('fuente', str())

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
        if self.client_id != other.client_id:
            return False
        if self.priority != other.priority:
            return False
        if self.accion != other.accion:
            return False
        if self.objeto != other.objeto:
            return False
        if self.color != other.color:
            return False
        if self.zona != other.zona:
            return False
        if self.permitido != other.permitido:
            return False
        if self.degradada != other.degradada:
            return False
        if self.fuente != other.fuente:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def client_id(self):
        """Message field 'client_id'."""
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'client_id' field must be of type 'str'"
        self._client_id = value

    @builtins.property
    def priority(self):
        """Message field 'priority'."""
        return self._priority

    @priority.setter
    def priority(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'priority' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'priority' field must be an unsigned integer in [0, 255]"
        self._priority = value

    @builtins.property
    def accion(self):
        """Message field 'accion'."""
        return self._accion

    @accion.setter
    def accion(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'accion' field must be of type 'str'"
        self._accion = value

    @builtins.property
    def objeto(self):
        """Message field 'objeto'."""
        return self._objeto

    @objeto.setter
    def objeto(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'objeto' field must be of type 'str'"
        self._objeto = value

    @builtins.property
    def color(self):
        """Message field 'color'."""
        return self._color

    @color.setter
    def color(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'color' field must be of type 'str'"
        self._color = value

    @builtins.property
    def zona(self):
        """Message field 'zona'."""
        return self._zona

    @zona.setter
    def zona(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'zona' field must be of type 'str'"
        self._zona = value

    @builtins.property
    def permitido(self):
        """Message field 'permitido'."""
        return self._permitido

    @permitido.setter
    def permitido(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'permitido' field must be of type 'bool'"
        self._permitido = value

    @builtins.property
    def degradada(self):
        """Message field 'degradada'."""
        return self._degradada

    @degradada.setter
    def degradada(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'degradada' field must be of type 'bool'"
        self._degradada = value

    @builtins.property
    def fuente(self):
        """Message field 'fuente'."""
        return self._fuente

    @fuente.setter
    def fuente(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'fuente' field must be of type 'str'"
        self._fuente = value


# Import statements for member types

# Member 'stage_time_s'
import array  # noqa: E402, I100

# already imported above
# import builtins

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_PickPlace_Result(type):
    """Metaclass of message 'PickPlace_Result'."""

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
                'arm_broker_interfaces.action.PickPlace_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__pick_place__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__pick_place__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__pick_place__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__pick_place__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__pick_place__result

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PickPlace_Result(metaclass=Metaclass_PickPlace_Result):
    """Message class 'PickPlace_Result'."""

    __slots__ = [
        '_success',
        '_simulated',
        '_planning_only',
        '_physical_verified',
        '_message',
        '_wait_time_s',
        '_exec_time_s',
        '_stages',
        '_stage_time_s',
        '_position_error_mm',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'simulated': 'boolean',
        'planning_only': 'boolean',
        'physical_verified': 'boolean',
        'message': 'string',
        'wait_time_s': 'double',
        'exec_time_s': 'double',
        'stages': 'sequence<string>',
        'stage_time_s': 'sequence<double>',
        'position_error_mm': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('double')),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.simulated = kwargs.get('simulated', bool())
        self.planning_only = kwargs.get('planning_only', bool())
        self.physical_verified = kwargs.get('physical_verified', bool())
        self.message = kwargs.get('message', str())
        self.wait_time_s = kwargs.get('wait_time_s', float())
        self.exec_time_s = kwargs.get('exec_time_s', float())
        self.stages = kwargs.get('stages', [])
        self.stage_time_s = array.array('d', kwargs.get('stage_time_s', []))
        self.position_error_mm = kwargs.get('position_error_mm', float())

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
        if self.success != other.success:
            return False
        if self.simulated != other.simulated:
            return False
        if self.planning_only != other.planning_only:
            return False
        if self.physical_verified != other.physical_verified:
            return False
        if self.message != other.message:
            return False
        if self.wait_time_s != other.wait_time_s:
            return False
        if self.exec_time_s != other.exec_time_s:
            return False
        if self.stages != other.stages:
            return False
        if self.stage_time_s != other.stage_time_s:
            return False
        if self.position_error_mm != other.position_error_mm:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def simulated(self):
        """Message field 'simulated'."""
        return self._simulated

    @simulated.setter
    def simulated(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'simulated' field must be of type 'bool'"
        self._simulated = value

    @builtins.property
    def planning_only(self):
        """Message field 'planning_only'."""
        return self._planning_only

    @planning_only.setter
    def planning_only(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'planning_only' field must be of type 'bool'"
        self._planning_only = value

    @builtins.property
    def physical_verified(self):
        """Message field 'physical_verified'."""
        return self._physical_verified

    @physical_verified.setter
    def physical_verified(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'physical_verified' field must be of type 'bool'"
        self._physical_verified = value

    @builtins.property
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value

    @builtins.property
    def wait_time_s(self):
        """Message field 'wait_time_s'."""
        return self._wait_time_s

    @wait_time_s.setter
    def wait_time_s(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'wait_time_s' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'wait_time_s' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._wait_time_s = value

    @builtins.property
    def exec_time_s(self):
        """Message field 'exec_time_s'."""
        return self._exec_time_s

    @exec_time_s.setter
    def exec_time_s(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'exec_time_s' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'exec_time_s' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._exec_time_s = value

    @builtins.property
    def stages(self):
        """Message field 'stages'."""
        return self._stages

    @stages.setter
    def stages(self, value):
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
                "The 'stages' field must be a set or sequence and each value of type 'str'"
        self._stages = value

    @builtins.property
    def stage_time_s(self):
        """Message field 'stage_time_s'."""
        return self._stage_time_s

    @stage_time_s.setter
    def stage_time_s(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'd', \
                "The 'stage_time_s' array.array() must have the type code of 'd'"
            self._stage_time_s = value
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
                "The 'stage_time_s' field must be a set or sequence and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._stage_time_s = array.array('d', value)

    @builtins.property
    def position_error_mm(self):
        """Message field 'position_error_mm'."""
        return self._position_error_mm

    @position_error_mm.setter
    def position_error_mm(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'position_error_mm' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'position_error_mm' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._position_error_mm = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import math

# already imported above
# import rosidl_parser.definition


class Metaclass_PickPlace_Feedback(type):
    """Metaclass of message 'PickPlace_Feedback'."""

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
                'arm_broker_interfaces.action.PickPlace_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__pick_place__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__pick_place__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__pick_place__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__pick_place__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__pick_place__feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PickPlace_Feedback(metaclass=Metaclass_PickPlace_Feedback):
    """Message class 'PickPlace_Feedback'."""

    __slots__ = [
        '_state',
        '_queue_position',
        '_elapsed_s',
    ]

    _fields_and_field_types = {
        'state': 'string',
        'queue_position': 'int32',
        'elapsed_s': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.state = kwargs.get('state', str())
        self.queue_position = kwargs.get('queue_position', int())
        self.elapsed_s = kwargs.get('elapsed_s', float())

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
        if self.state != other.state:
            return False
        if self.queue_position != other.queue_position:
            return False
        if self.elapsed_s != other.elapsed_s:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def state(self):
        """Message field 'state'."""
        return self._state

    @state.setter
    def state(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'state' field must be of type 'str'"
        self._state = value

    @builtins.property
    def queue_position(self):
        """Message field 'queue_position'."""
        return self._queue_position

    @queue_position.setter
    def queue_position(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'queue_position' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'queue_position' field must be an integer in [-2147483648, 2147483647]"
        self._queue_position = value

    @builtins.property
    def elapsed_s(self):
        """Message field 'elapsed_s'."""
        return self._elapsed_s

    @elapsed_s.setter
    def elapsed_s(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'elapsed_s' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'elapsed_s' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._elapsed_s = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PickPlace_SendGoal_Request(type):
    """Metaclass of message 'PickPlace_SendGoal_Request'."""

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
                'arm_broker_interfaces.action.PickPlace_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__pick_place__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__pick_place__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__pick_place__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__pick_place__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__pick_place__send_goal__request

            from arm_broker_interfaces.action import PickPlace
            if PickPlace.Goal.__class__._TYPE_SUPPORT is None:
                PickPlace.Goal.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PickPlace_SendGoal_Request(metaclass=Metaclass_PickPlace_SendGoal_Request):
    """Message class 'PickPlace_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'arm_broker_interfaces/PickPlace_Goal',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['arm_broker_interfaces', 'action'], 'PickPlace_Goal'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from arm_broker_interfaces.action._pick_place import PickPlace_Goal
        self.goal = kwargs.get('goal', PickPlace_Goal())

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
        if self.goal_id != other.goal_id:
            return False
        if self.goal != other.goal:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def goal(self):
        """Message field 'goal'."""
        return self._goal

    @goal.setter
    def goal(self, value):
        if __debug__:
            from arm_broker_interfaces.action._pick_place import PickPlace_Goal
            assert \
                isinstance(value, PickPlace_Goal), \
                "The 'goal' field must be a sub message of type 'PickPlace_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PickPlace_SendGoal_Response(type):
    """Metaclass of message 'PickPlace_SendGoal_Response'."""

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
                'arm_broker_interfaces.action.PickPlace_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__pick_place__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__pick_place__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__pick_place__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__pick_place__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__pick_place__send_goal__response

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


class PickPlace_SendGoal_Response(metaclass=Metaclass_PickPlace_SendGoal_Response):
    """Message class 'PickPlace_SendGoal_Response'."""

    __slots__ = [
        '_accepted',
        '_stamp',
    ]

    _fields_and_field_types = {
        'accepted': 'boolean',
        'stamp': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.accepted = kwargs.get('accepted', bool())
        from builtin_interfaces.msg import Time
        self.stamp = kwargs.get('stamp', Time())

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
        if self.accepted != other.accepted:
            return False
        if self.stamp != other.stamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def accepted(self):
        """Message field 'accepted'."""
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'accepted' field must be of type 'bool'"
        self._accepted = value

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


class Metaclass_PickPlace_SendGoal(type):
    """Metaclass of service 'PickPlace_SendGoal'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('arm_broker_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'arm_broker_interfaces.action.PickPlace_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__pick_place__send_goal

            from arm_broker_interfaces.action import _pick_place
            if _pick_place.Metaclass_PickPlace_SendGoal_Request._TYPE_SUPPORT is None:
                _pick_place.Metaclass_PickPlace_SendGoal_Request.__import_type_support__()
            if _pick_place.Metaclass_PickPlace_SendGoal_Response._TYPE_SUPPORT is None:
                _pick_place.Metaclass_PickPlace_SendGoal_Response.__import_type_support__()


class PickPlace_SendGoal(metaclass=Metaclass_PickPlace_SendGoal):
    from arm_broker_interfaces.action._pick_place import PickPlace_SendGoal_Request as Request
    from arm_broker_interfaces.action._pick_place import PickPlace_SendGoal_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PickPlace_GetResult_Request(type):
    """Metaclass of message 'PickPlace_GetResult_Request'."""

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
                'arm_broker_interfaces.action.PickPlace_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__pick_place__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__pick_place__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__pick_place__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__pick_place__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__pick_place__get_result__request

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PickPlace_GetResult_Request(metaclass=Metaclass_PickPlace_GetResult_Request):
    """Message class 'PickPlace_GetResult_Request'."""

    __slots__ = [
        '_goal_id',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())

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
        if self.goal_id != other.goal_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PickPlace_GetResult_Response(type):
    """Metaclass of message 'PickPlace_GetResult_Response'."""

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
                'arm_broker_interfaces.action.PickPlace_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__pick_place__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__pick_place__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__pick_place__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__pick_place__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__pick_place__get_result__response

            from arm_broker_interfaces.action import PickPlace
            if PickPlace.Result.__class__._TYPE_SUPPORT is None:
                PickPlace.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PickPlace_GetResult_Response(metaclass=Metaclass_PickPlace_GetResult_Response):
    """Message class 'PickPlace_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'arm_broker_interfaces/PickPlace_Result',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['arm_broker_interfaces', 'action'], 'PickPlace_Result'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', int())
        from arm_broker_interfaces.action._pick_place import PickPlace_Result
        self.result = kwargs.get('result', PickPlace_Result())

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
        if self.status != other.status:
            return False
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'status' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'status' field must be an integer in [-128, 127]"
        self._status = value

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            from arm_broker_interfaces.action._pick_place import PickPlace_Result
            assert \
                isinstance(value, PickPlace_Result), \
                "The 'result' field must be a sub message of type 'PickPlace_Result'"
        self._result = value


class Metaclass_PickPlace_GetResult(type):
    """Metaclass of service 'PickPlace_GetResult'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('arm_broker_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'arm_broker_interfaces.action.PickPlace_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__pick_place__get_result

            from arm_broker_interfaces.action import _pick_place
            if _pick_place.Metaclass_PickPlace_GetResult_Request._TYPE_SUPPORT is None:
                _pick_place.Metaclass_PickPlace_GetResult_Request.__import_type_support__()
            if _pick_place.Metaclass_PickPlace_GetResult_Response._TYPE_SUPPORT is None:
                _pick_place.Metaclass_PickPlace_GetResult_Response.__import_type_support__()


class PickPlace_GetResult(metaclass=Metaclass_PickPlace_GetResult):
    from arm_broker_interfaces.action._pick_place import PickPlace_GetResult_Request as Request
    from arm_broker_interfaces.action._pick_place import PickPlace_GetResult_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PickPlace_FeedbackMessage(type):
    """Metaclass of message 'PickPlace_FeedbackMessage'."""

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
                'arm_broker_interfaces.action.PickPlace_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__pick_place__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__pick_place__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__pick_place__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__pick_place__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__pick_place__feedback_message

            from arm_broker_interfaces.action import PickPlace
            if PickPlace.Feedback.__class__._TYPE_SUPPORT is None:
                PickPlace.Feedback.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PickPlace_FeedbackMessage(metaclass=Metaclass_PickPlace_FeedbackMessage):
    """Message class 'PickPlace_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'arm_broker_interfaces/PickPlace_Feedback',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['arm_broker_interfaces', 'action'], 'PickPlace_Feedback'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from arm_broker_interfaces.action._pick_place import PickPlace_Feedback
        self.feedback = kwargs.get('feedback', PickPlace_Feedback())

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
        if self.goal_id != other.goal_id:
            return False
        if self.feedback != other.feedback:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def feedback(self):
        """Message field 'feedback'."""
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        if __debug__:
            from arm_broker_interfaces.action._pick_place import PickPlace_Feedback
            assert \
                isinstance(value, PickPlace_Feedback), \
                "The 'feedback' field must be a sub message of type 'PickPlace_Feedback'"
        self._feedback = value


class Metaclass_PickPlace(type):
    """Metaclass of action 'PickPlace'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('arm_broker_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'arm_broker_interfaces.action.PickPlace')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__pick_place

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from arm_broker_interfaces.action import _pick_place
            if _pick_place.Metaclass_PickPlace_SendGoal._TYPE_SUPPORT is None:
                _pick_place.Metaclass_PickPlace_SendGoal.__import_type_support__()
            if _pick_place.Metaclass_PickPlace_GetResult._TYPE_SUPPORT is None:
                _pick_place.Metaclass_PickPlace_GetResult.__import_type_support__()
            if _pick_place.Metaclass_PickPlace_FeedbackMessage._TYPE_SUPPORT is None:
                _pick_place.Metaclass_PickPlace_FeedbackMessage.__import_type_support__()


class PickPlace(metaclass=Metaclass_PickPlace):

    # The goal message defined in the action definition.
    from arm_broker_interfaces.action._pick_place import PickPlace_Goal as Goal
    # The result message defined in the action definition.
    from arm_broker_interfaces.action._pick_place import PickPlace_Result as Result
    # The feedback message defined in the action definition.
    from arm_broker_interfaces.action._pick_place import PickPlace_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from arm_broker_interfaces.action._pick_place import PickPlace_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from arm_broker_interfaces.action._pick_place import PickPlace_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from arm_broker_interfaces.action._pick_place import PickPlace_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')
