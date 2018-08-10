import unittest, datetime
from xml.etree import ElementTree as ET

from hl7.xml import containers
from hl7.xml.utils import (
    isinstance_all,
    len_without,
    flatten_matrix,
)
from .constants import HL7_MESSAGE, EXPECTED_VALUES


class ContainerTestCase(unittest.TestCase):
    def setUp(self):
        self.valid = [ HL7_MESSAGE, ET.fromstring(HL7_MESSAGE) ]
        self.invalid = [
            True,
            20180703111743,
            { 'invalid': True },
            'invalid string',
            '<xml><tag>content</tag>',
        ]

    def assert_constructor_raises(self, *args, exception=None):
        for arg in args:
            if exception:
                self.assertRaises(exception, containers.Container, arg)
            else:
                self.assertTrue(containers.Container(arg))

    def test_constructor(self):
        self.assert_constructor_raises(exception=AttributeError, *self.invalid)
        self.assert_constructor_raises(*self.valid)
    
    def test_getitem(self):
        container = containers.Container(HL7_MESSAGE)
        self.assertTrue(container, containers.Container)
        self.assertEqual(len(list(container)), 10)
    

class MessageTestCase(unittest.TestCase):
    def setUp(self):
        self.message = containers.Message(HL7_MESSAGE)
        self.obx_identifiers = [obx_tuple[1] for obx_tuple in EXPECTED_VALUES['OBX']]

    def test_items(self):
        items = list(self.message)
        
        msh = list(filter(lambda m: isinstance(m, containers.MSH), items))
        pid = list(filter(lambda m: isinstance(m, containers.PID), items))
        pv1 = list(filter(lambda m: isinstance(m, containers.PV1), items))
        obr = list(filter(lambda m: isinstance(m, containers.OBR), items))
        obx = list(filter(lambda m: isinstance(m, containers.OBX), items))

        self.assertEqual(len(msh), 1)
        self.assertEqual(len(pid), 1)
        self.assertEqual(len(pv1), 1)
        self.assertEqual(len(obr), 1)
        self.assertEqual(len(obx), len(EXPECTED_VALUES['OBX']))
    
    def test_getitem(self):
        msh = self.message['MSH']
        pid = self.message['PID']
        pv1 = self.message['PV1']
        obr = self.message['OBR']
        obx = self.message['OBX']
        
        self.assertTrue(isinstance_all(msh, containers.MSH))
        self.assertTrue(isinstance_all(pid, containers.PID))
        self.assertTrue(isinstance_all(pv1, containers.PV1))
        self.assertTrue(isinstance_all(obr, containers.OBR))
        self.assertTrue(isinstance_all(obx, containers.OBX))

        self.assertEqual(len(msh), 1)
        self.assertEqual(len(pid), 1)
        self.assertEqual(len(pv1), 1)
        self.assertEqual(len(obr), 1)
        self.assertEqual(len(obx), len(EXPECTED_VALUES['OBX']))
    
    def test_get_obx(self):
        # Invalid identifiers
        self.assertIsNone(self.message.get_obx('INVALID_IDENTIFIER'))
        self.assertIsNone(self.message.get_obx_value('INVALID_IDENTIFIER'))

        # Valid identifiers
        for i in range(len(self.obx_identifiers)):
            identifier = self.obx_identifiers[i]
            expected = EXPECTED_VALUES['OBX'][i]
            
            obx = self.message.get_obx(identifier)
            obx_value = self.message.get_obx_value(identifier)

            self.assertEqual(obx_value, expected[2])
            self.assertEqual((
                obx.value_type, 
                obx.identifier, 
                obx.value, 
                obx.units, 
                obx.reference_range, 
                obx.datetime
            ), expected)


class SegmentTestCase(unittest.TestCase):
    def setUp(self):
        self.expected = list(flatten_matrix(EXPECTED_VALUES.values()))
        self.message = containers.Message(HL7_MESSAGE)

    def test_items(self):
        self.assertTrue(isinstance_all(self.message, containers.Segment))
    
    def test_fields(self):
        segments = list(self.message)
        
        for i in range(len(segments)):
            s = segments[i]
            fields = list(s)
            self.assertTrue(isinstance_all(fields, containers.Field))
            self.assertEqual(len(fields), len_without(self.expected[i]))


class MSHTestCase(unittest.TestCase):
    def setUp(self):
        self.msh = containers.Message(HL7_MESSAGE)['MSH'][0]

    def test_fields(self):
        self.assertEqual(len(list(self.msh)), len(EXPECTED_VALUES['MSH']))
        self.assertEqual((
            self.msh.field_separator,
            self.msh.encoding_chars,
            self.msh.sending_application,
            self.msh.datetime,
            self.msh.message_type,
            self.msh.version,
        ), EXPECTED_VALUES['MSH'])


class PV1TestCase(unittest.TestCase):
    def setUp(self):
        self.pv1 = containers.Message(HL7_MESSAGE)['PV1'][0]
    
    def test_fields(self):
        self.assertEqual(len(list(self.pv1)), len(EXPECTED_VALUES['PV1']))
        self.assertEqual((
            self.pv1.patient_class,
            self.pv1.patient_type,
            self.pv1.admit_datetime,
        ), EXPECTED_VALUES['PV1'])


class PIDTestCase(unittest.TestCase):
    def setUp(self):
        self.pid = containers.Message(HL7_MESSAGE)['PID'][0]
    
    def test_fields(self):
        self.assertEqual(len(list(self.pid)), len(EXPECTED_VALUES['PID']))
        self.assertEqual((
            self.pid.id, 
            self.pid.id_list,
            self.pid.name,
            self.pid.birthdate,
            self.pid.gender,
        ), EXPECTED_VALUES['PID'])


class OBRTestCase(unittest.TestCase):
    def setUp(self):
        self.obr = containers.Message(HL7_MESSAGE)['OBR'][0]
    
    def test_fields(self):
        self.assertEqual(len(list(self.obr)), len(EXPECTED_VALUES['OBR']))
        self.assertEqual((
            self.obr.datetime, 
        ), EXPECTED_VALUES['OBR'])


class OBXTestCase(unittest.TestCase):
    def setUp(self):
        self.obx = containers.Message(HL7_MESSAGE)['OBX']
    
    def test_fields(self):
        for i in range(len(self.obx)):
            source = self.obx[i]
            expected = EXPECTED_VALUES['OBX'][i]
            
            self.assertEqual(len(list(source)), len_without(expected))
            self.assertEqual((
                source.value_type, 
                source.identifier, 
                source.value, 
                source.units, 
                source.reference_range, 
                source.datetime
            ), expected)