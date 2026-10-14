# generated from rosidl_generator_py/resource/_idl.py.em
# with input from laya_ordenes_interfaces:srv/InterpretarOrden.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_InterpretarOrden_Request(type):
    """Metaclass of message 'InterpretarOrden_Request'."""

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
            module = import_type_support('laya_ordenes_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'laya_ordenes_interfaces.srv.InterpretarOrden_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__interpretar_orden__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__interpretar_orden__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__interpretar_orden__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__interpretar_orden__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__interpretar_orden__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class InterpretarOrden_Request(metaclass=Metaclass_InterpretarOrden_Request):
    """Message class 'InterpretarOrden_Request'."""

    __slots__ = [
        '_frase',
    ]

    _fields_and_field_types = {
        'frase': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.frase = kwargs.get('frase', str())

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
        if self.frase != other.frase:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def frase(self):
        """Message field 'frase'."""
        return self._frase

    @frase.setter
    def frase(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'frase' field must be of type 'str'"
        self._frase = value


# Import statements for member types

# already imported above
# import builtins

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_InterpretarOrden_Response(type):
    """Metaclass of message 'InterpretarOrden_Response'."""

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
            module = import_type_support('laya_ordenes_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'laya_ordenes_interfaces.srv.InterpretarOrden_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__interpretar_orden__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__interpretar_orden__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__interpretar_orden__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__interpretar_orden__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__interpretar_orden__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class InterpretarOrden_Response(metaclass=Metaclass_InterpretarOrden_Response):
    """Message class 'InterpretarOrden_Response'."""

    __slots__ = [
        '_accion',
        '_objeto',
        '_color',
        '_prioridad',
        '_permitido',
        '_degradada',
        '_fuente',
        '_motivo',
        '_latencia_http_ms',
        '_inferencia_ms',
        '_resto_http_ms',
    ]

    _fields_and_field_types = {
        'accion': 'string',
        'objeto': 'string',
        'color': 'string',
        'prioridad': 'uint8',
        'permitido': 'boolean',
        'degradada': 'boolean',
        'fuente': 'string',
        'motivo': 'string',
        'latencia_http_ms': 'double',
        'inferencia_ms': 'double',
        'resto_http_ms': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.accion = kwargs.get('accion', str())
        self.objeto = kwargs.get('objeto', str())
        self.color = kwargs.get('color', str())
        self.prioridad = kwargs.get('prioridad', int())
        self.permitido = kwargs.get('permitido', bool())
        self.degradada = kwargs.get('degradada', bool())
        self.fuente = kwargs.get('fuente', str())
        self.motivo = kwargs.get('motivo', str())
        self.latencia_http_ms = kwargs.get('latencia_http_ms', float())
        self.inferencia_ms = kwargs.get('inferencia_ms', float())
        self.resto_http_ms = kwargs.get('resto_http_ms', float())

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
        if self.accion != other.accion:
            return False
        if self.objeto != other.objeto:
            return False
        if self.color != other.color:
            return False
        if self.prioridad != other.prioridad:
            return False
        if self.permitido != other.permitido:
            return False
        if self.degradada != other.degradada:
            return False
        if self.fuente != other.fuente:
            return False
        if self.motivo != other.motivo:
            return False
        if self.latencia_http_ms != other.latencia_http_ms:
            return False
        if self.inferencia_ms != other.inferencia_ms:
            return False
        if self.resto_http_ms != other.resto_http_ms:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

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
    def prioridad(self):
        """Message field 'prioridad'."""
        return self._prioridad

    @prioridad.setter
    def prioridad(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'prioridad' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'prioridad' field must be an unsigned integer in [0, 255]"
        self._prioridad = value

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

    @builtins.property
    def motivo(self):
        """Message field 'motivo'."""
        return self._motivo

    @motivo.setter
    def motivo(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'motivo' field must be of type 'str'"
        self._motivo = value

    @builtins.property
    def latencia_http_ms(self):
        """Message field 'latencia_http_ms'."""
        return self._latencia_http_ms

    @latencia_http_ms.setter
    def latencia_http_ms(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'latencia_http_ms' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'latencia_http_ms' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._latencia_http_ms = value

    @builtins.property
    def inferencia_ms(self):
        """Message field 'inferencia_ms'."""
        return self._inferencia_ms

    @inferencia_ms.setter
    def inferencia_ms(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'inferencia_ms' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'inferencia_ms' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._inferencia_ms = value

    @builtins.property
    def resto_http_ms(self):
        """Message field 'resto_http_ms'."""
        return self._resto_http_ms

    @resto_http_ms.setter
    def resto_http_ms(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'resto_http_ms' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'resto_http_ms' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._resto_http_ms = value


class Metaclass_InterpretarOrden(type):
    """Metaclass of service 'InterpretarOrden'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('laya_ordenes_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'laya_ordenes_interfaces.srv.InterpretarOrden')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__interpretar_orden

            from laya_ordenes_interfaces.srv import _interpretar_orden
            if _interpretar_orden.Metaclass_InterpretarOrden_Request._TYPE_SUPPORT is None:
                _interpretar_orden.Metaclass_InterpretarOrden_Request.__import_type_support__()
            if _interpretar_orden.Metaclass_InterpretarOrden_Response._TYPE_SUPPORT is None:
                _interpretar_orden.Metaclass_InterpretarOrden_Response.__import_type_support__()


class InterpretarOrden(metaclass=Metaclass_InterpretarOrden):
    from laya_ordenes_interfaces.srv._interpretar_orden import InterpretarOrden_Request as Request
    from laya_ordenes_interfaces.srv._interpretar_orden import InterpretarOrden_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
