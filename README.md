[![PyPi version](https://img.shields.io/pypi/v/python-xml-hl7.svg)](https://pypi.python.org/pypi/python-xml-hl7) [![Build Status](https://travis-ci.org/weynelucas/python-xml-hl7.svg?branch=master)](https://travis-ci.org/weynelucas/python-xml-hl7) [![codecov](https://codecov.io/gh/weynelucas/python-xml-hl7/branch/master/graph/badge.svg)](https://codecov.io/gh/weynelucas/python-xml-hl7)

# python-xml-hl7
A library for parsing HL7 (version 2.x) messages in XML format into Python objects


## Instalation

You can install this library using pip:
```
pip install python-xml-hl7
```

or from the git repository:
```
git clone https://github.com/weynelucas/python-xml-hl7.git
cd python-xml-hl7
python setup.py install
```

## Quickstart

As an example, let’s create a HL7 message:

```python
message = """
<ORU_R01>
<MSH><MSH.1>|</MSH.1><MSH.2>^~\\&amp;</MSH.2><MSH.3>hospital</MSH.3><MSH.7>20180703111743</MSH.7><MSH.9><MSH.9.1>ORU</MSH.9.1><MSH.9.2>R01</MSH.9.2></MSH.9><MSH.12>2.3.1</MSH.12></MSH>
<PID><PID.2>shenzhen</PID.2><PID.3>1</PID.3><PID.5>libang</PID.5><PID.7>20091010</PID.7><PID.8>M</PID.8></PID>
<PV1><PV1.2>U</PV1.2><PV1.18>adult</PV1.18><PV1.44>20180726181346</PV1.44></PV1>
<OBR><OBR.7>20180703111743</OBR.7></OBR>
<OBX><OBX.2>NM</OBX.2><OBX.3>SPO2</OBX.3><OBX.5>96</OBX.5><OBX.6>%</OBX.6><OBX.7>90-100</OBX.7></OBX>
<OBX><OBX.2>NM</OBX.2><OBX.3>PR</OBX.3><OBX.5>68</OBX.5><OBX.6>bpm</OBX.6><OBX.7>50-120</OBX.7></OBX>
<OBX><OBX.2>NM</OBX.2><OBX.3>SYS</OBX.3><OBX.5>131</OBX.5><OBX.6>mmHg</OBX.6><OBX.7>90-160</OBX.7><OBX.14>20180703111713</OBX.14></OBX>
<OBX><OBX.2>NM</OBX.2><OBX.3>DIA</OBX.3><OBX.5>85</OBX.5><OBX.6>mmHg</OBX.6><OBX.7>50-90</OBX.7><OBX.14>20180703111713</OBX.14></OBX>
<OBX><OBX.2>NM</OBX.2><OBX.3>MAP</OBX.3><OBX.5>100</OBX.5><OBX.6>mmHg</OBX.6><OBX.7>60-110</OBX.7><OBX.14>20180703111713</OBX.14></OBX>
<OBX><OBX.2>NM</OBX.2><OBX.3>NIBP_PR</OBX.3><OBX.5>73</OBX.5><OBX.6>bpm</OBX.6><OBX.7>50-120</OBX.7><OBX.14>20180703111713</OBX.14></OBX>
</ORU_R01>
"""
```

Call `hl7.xml.parse()` command to convert the string message

```python
from hl7.xml import parse

h = parse(message)
```

This command returns a `Message` instance, wrapping a series of `Segment` objects. Is possible iterate over segments or match for specific ones:

```python
>>> list(h) # List all message segments
[<hl7.xml.containers.MSH>,
 <hl7.xml.containers.PID>,
 <hl7.xml.containers.PV1>,
 <hl7.xml.containers.OBR>,
 <hl7.xml.containers.OBX: SPO2>,
 <hl7.xml.containers.OBX: PR>,
 <hl7.xml.containers.OBX: SYS>,
 <hl7.xml.containers.OBX: DIA>,
 <hl7.xml.containers.OBX: MAP>,
 <hl7.xml.containers.OBX: NIBP_PR>]

>>> h[0]  # Get 1st message segment
<hl7.xml.containers.MSH>

>>> h['OBX'] # Find all OBX segments
[<hl7.xml.containers.OBX: SPO2>,
 <hl7.xml.containers.OBX: PR>,
 <hl7.xml.containers.OBX: SYS>,
 <hl7.xml.containers.OBX: DIA>,
 <hl7.xml.containers.OBX: MAP>,
 <hl7.xml.containers.OBX: NIBP_PR>]
```

A `Segment` instance wraps a serie of `Field` objects, you can iterate over them:

```python
>>> list(h[2]) # List all fields for 3rd message segment (PV1)
[<hl7.xml.containers.Field: PV1.2>,
 <hl7.xml.containers.Field: PV1.18>,
 <hl7.xml.containers.Field: PV1.44>]

>>> list(h[5]) # List all fields for 6th message segment (OBX)
[<hl7.xml.containers.Field: OBX.2>,
 <hl7.xml.containers.Field: OBX.3>,
 <hl7.xml.containers.Field: OBX.5>,
 <hl7.xml.containers.Field: OBX.6>,
 <hl7.xml.containers.Field: OBX.7>]

>>> h[5][0].value
'NM'

>>> h[5][2].value
'62'
```

There are different types of `Segment`, they are: `MSH`, `PID`, `PV1`, `OBR` and `OBX`. Each of them has helper methods to retrieve data from its respective HL7 segment without iterate over his `Field` objects

#### MSH

```python
>>> msh = h['MSH'][0]
>>> (msh.field_separator,
     msh.encoding_chars,
     msh.sending_application,
     msh.datetime,
     msh.version,
     msh.message_type)
('|', '^~\\&', 'hospital', datetime.datetime(2018, 7, 3, 11, 17, 43), '2.3.1', ('ORU', 'R01'))
```

#### PID
``` python
>>> pid = h['PID'][0]
>>> (pid.id,
     pid.id_list,
     pid.name,
     pid.birthdate,
     pid.gender)
('shenzhen', '1', 'libang', datetime.datetime(2009, 10, 10, 0, 0), 'M')
```

#### PV1
```python
>>> pv1 = h['PV1'][0]
>>> (pv1.patient_class,
     pv1.patient_class_display,
     pv1.patient_type,
     pv1.patient_type_display,
     pv1.assigned_patient_location,
     pv1.admit_datetime)
('U', 'Unknown', 'adult', 'Adult', None, datetime.datetime(2018, 7, 26, 18, 13, 46))
```

#### OBR
```python
>>> obr = h['OBR'][0]
>>> obr.datetime
datetime.datetime(2018, 7, 3, 11, 17, 43)
```

#### OBX
```python
>>> obx = h['OBX'][3] # 4th OBX instance
>>> (obx.identifier,
     obx.value_type,
     obx.value,
     obx.units,
     obx.reference_range,
     obx.datetime)
('DIA', 'NM', 85, 'mmHg', (50, 90), datetime.datetime(2018, 7, 3, 11, 17, 13))
```

To find a `OBX` segment or value inside a `Message` by its identifier, use `get_obx` and `get_obx_value` methods:

```python
>>> h.get_obx('DIA')
<hl7.xml.containers.OBX: DIA>

>>> h.get_obx('DIA').value
85

>>> h.get_obx_value('SPO2')
96
```

## Network client
`python-xml-hl7` provides a simple network (TCP/IP) client, wich reads HL7 messages from [Alfamed](http://www.alfamed.com/) patient monitors like [VITA 200e](http://www.alfamed.com/monitor-multiparametro-vita-200.html)

```python
from hl7.xml.client import AlfamedClient

client = AlfamedClient('169.254.215.35') # Default communication port is 9100
client.read_message()  # By default, HL7 messages are converted into Message objects
client.read_message(parse_message=False) # Returns the original HL7 message as string
```

`AlfamedClient` objects instantiated with invalid host addresses will raises `AttributeError`

## Testing
You can run tests locally using `unittest` module

```
cd python-xml-hl7
python -m unittest tests
```

If all the tests pass you will see a success message like this:
```
.................
----------------------------------------------------------------------
Ran 17 tests in 0.007s

OK
```

## Notes

* Specification for XML encoding rules of HL7 v2 messages can be found [here](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=83)
* For any suggestion, feature or bug fix, you can report an issue [here](https://github.com/weynelucas/python-xml-hl7/issues). Or submit a pull request
* For handle HL7 messages in original stream format, use solutions like [python-hl7](http://python-hl7.readthedocs.io/en/latest/) or [HL7apy](http://hl7apy.org/)

## Release Notes

* 1.0.0 - First release
* 1.1.0 - Find `OBX` segments with `get_obx` and `get_obx_value`
* 1.2.0 - String representation for client and container objects
* 1.3.0 - Add Travis and Codecov support