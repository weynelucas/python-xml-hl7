import six
import re
from xml.etree import ElementTree as ET

from . import constants
from .datatypes import (
    parse_value, 
    parse_numeric,
    parse_datetime, 
)


ALLOWED_CONTENT_TYPES = (str, bytes, ET.Element)


def parse_content(content):
    if not isinstance(content, ALLOWED_CONTENT_TYPES):
        raise AttributeError(
            "Invalid content. Expected one of theese types: %s, but got %s" % 
            (", ".join(str(ct) for ct in ALLOWED_CONTENT_TYPES), six.text_type(content))
        )

    try: 
        return content if isinstance(content, ET.Element) else  ET.fromstring(content)
    except ET.ParseError:
        raise AttributeError("Invalid content. Could not parse XML string.")


class Container(object):
    """
    Abstract root class for the parts of the HL7 message.
    """
    item_class = None
    unique_items = False
    display_property = 'name'
    
    def __init__(self, content):
        self.etree = content
    
    def __repr__(self):
        try:
            display = getattr(self, self.display_property)
        except (AttributeError, TypeError):
            display = None
        
        classname = '%s.%s' % (self.__module__, self.__class__.__qualname__)

        return '<%s: %s>' % (classname, display) if display else '<%s>' % (classname)
    
    @property
    def name(self):
        return self.etree.tag
    
    @property
    def etree(self):
        return self._etree
    
    @etree.setter
    def etree(self, val):
        self._etree = parse_content(val)

    def findall(self, item):
        return [self._getitem(el) for el in self.etree.findall(item)]

    def find(self, item):
        el = self.etree.find(item)
        if el is not None:
            return self._getitem(el)
        return None

    def _getitem_class(self):
        return self.item_class or self.__class__

    def _getitem(self, elem):
        return self._getitem_class()(elem)
    
    def __getitem__(self, item):
        if isinstance(item, str):
            return self.find(item) if self.unique_items else self.findall(item)
        return self._getitem(self.etree[item])
    
    def __iter__(self):
        for el in self.etree:
            yield self._getitem(el)
    

class Field(Container): 
    """
    Representation of an HL7 Field
    """
    props = ('name', 'value')
    
    @property
    def value(self):
        return self.etree.text

    def __iter__(self):
        for attr in self.props:
            yield (attr, getattr(self, attr))
    
    def __str__(self):
        return "(%s, %s)" % (
            self.name,
            self.value
        )

        
class Segment(Container):
    """
    Representation of an HL7 segment. It contains a list of 
    `hl7.Field` instances
    """
    unique_items = True
    item_class = Field

    @classmethod
    def subclassess_dict(cls):
        return {
            subclass.__name__: subclass
            for subclass in cls.__subclasses__() 
        }
    
    @classmethod
    def create(cls, content):
        etree = parse_content(content)
        segment_class = cls.subclassess_dict().get(etree.tag) or cls
        return segment_class(etree)

    def get_field_value(self, field, cast=None):
        val = self[field]
        if val:
            return cast(val.value) if cast else val.value
        return None


def segment_field(field, datatype=None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            assert isinstance(self, Segment), (
                "`segment_field` must decorate an %s " +
                "instance method, but was applied to %s"
            ) % (Segment, six.text_type(self))

            val = self.get_field_value(field)
            return parse_value(val, datatype) if datatype else val
        return wrapper
    return decorator


class MSH(Segment):
    """
    Representation of an HL7 MSH segment
    """
    display_property = None

    @property
    @segment_field('MSH.1')
    def field_separator(self):
        pass
    
    @property
    @segment_field('MSH.2')
    def encoding_chars(self):
        pass
    
    @property
    @segment_field('MSH.3')
    def sending_application(self):
        pass
    
    @property
    @segment_field('MSH.7', datatype='TS')
    def datetime(self):   
        pass
    
    @property
    @segment_field('MSH.12')
    def version(self):
        pass   
    
    @property
    def message_type(self):
        return tuple(el.text for el in self['MSH.9'].etree)


class PID(Segment):
    """
    Representation of an HL7 PID segment
    """
    display_property = None

    @property
    @segment_field('PID.2')
    def id(self):
        pass

    @property
    @segment_field('PID.3')
    def id_list(self):
        pass

    @property
    @segment_field('PID.5')
    def name(self):
        pass

    @property
    @segment_field('PID.7', datatype='TS')
    def birthdate(self):
        pass

    @property
    @segment_field('PID.8')
    def gender(self):
        pass


class PV1(Segment):
    """
    Representation of an HL7 PV1 segment
    """
    display_property = None

    @property
    @segment_field('PV1.2')
    def patient_class(self):
        pass

    @property
    def patient_class_display(self):
        return dict(constants.PATIENT_CLASS).get(self.patient_class)

    @property
    @segment_field('PV1.3')
    def assigned_patient_location(self):
        pass

    @property
    @segment_field('PV1.18')
    def patient_type(self):
        pass

    @property
    def patient_type_display(self):
        ptype = self.patient_type
        if ptype:
            return dict(constants.PATIENT_TYPE).get(ptype.lower(), ptype)
        return None

    @property
    @segment_field('PV1.44', datatype='TS')
    def admit_datetime(self):
        pass


class OBR(Segment):
    """
    Representation of an HL7 OBR segment
    """
    display_property = None

    @property
    @segment_field('OBR.7', datatype='TS')
    def datetime(self):
        pass


class OBX(Segment):
    """
    Representation of an HL7 OBX segment
    """
    display_property = 'identifier'

    @property
    @segment_field('OBX.2')
    def value_type(self):
        pass

    @property
    @segment_field('OBX.3')
    def identifier(self):
        pass

    @property
    @segment_field('OBX.6')
    def units(self):
        pass

    @property
    def reference_range(self):
        val = self.get_field_value('OBX.7')
        if val:
            limits = tuple(
                parse_numeric(v) 
                for v in re.split('-|>|<', val)
            )
            return tuple(reversed(limits)) if '>' in val else limits
        return None

    @property
    def value(self):
        return parse_value(self.get_field_value('OBX.5'), self.value_type)

    @property
    @segment_field('OBX.14', datatype='TS')
    def datetime(self):
        pass


class Message(Container):
    """
    Representation of an HL7 message. It contains a list of 
    `hl7.Segment` instances
    """
    item_class = Segment

    def _getitem(self, elem):
        return self._getitem_class().create(elem)
    
    def get_obx(self, identifier):
        """
        Returns an OBX instance in the message which identifier 
        matches to the `identifier` argument
        """
        try:
            return  next(filter(
                lambda obx: str(obx.identifier) == str(identifier), 
                self['OBX']
            ))
        except StopIteration:
            return None      

    def get_obx_value(self, identifier):
        """
        Returns the value of an OBX segment in the message 
        which identifier matches to the `identifier` argument
        """
        obx = self.get_obx(identifier)
        return obx.value if obx else None