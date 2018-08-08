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

This command returns a `Message` instance, wrapping a series of `Segment` objects. Is possible iterate over segments or match for specific segments:

```python
>>> list(h)
[<hl7.xml.containers.MSH at 0x52cb668>,
 <hl7.xml.containers.PID at 0x52cb6d8>,
 <hl7.xml.containers.PV1 at 0x52cb828>,
 <hl7.xml.containers.OBR at 0x52cb860>,
 <hl7.xml.containers.OBX at 0x52cb898>,
 <hl7.xml.containers.OBX at 0x52cb8d0>,
 <hl7.xml.containers.OBX at 0x52cb908>,
 <hl7.xml.containers.OBX at 0x52cb940>,
 <hl7.xml.containers.OBX at 0x52cb978>,
 <hl7.xml.containers.OBX at 0x52cb9b0>]

>>> h[0]
<hl7.xml.containers.MSH at 0x52d2080>

>>> h['OBX']
[<hl7.xml.containers.OBX at 0x52cbd30>,
 <hl7.xml.containers.OBX at 0x5265400>,
 <hl7.xml.containers.OBX at 0x5265668>,
 <hl7.xml.containers.OBX at 0x52655c0>,
 <hl7.xml.containers.OBX at 0x5265588>,
 <hl7.xml.containers.OBX at 0x52653c8>]
```

A `Segment` instance wraps a serie of `Field` objects, you can iterate over them:

```python
>>> list(h[5])
[<hl7.xml.containers.Field at 0x502b208>,
 <hl7.xml.containers.Field at 0x502b198>,
 <hl7.xml.containers.Field at 0x502b240>,
 <hl7.xml.containers.Field at 0x502b048>,
 <hl7.xml.containers.Field at 0x502b940>]

>>> h[5][0].value
'NM'

>>> h[5][2].value
'62'
```

There are different types of `Segment`, they are: `MSH`, `PID`, `PV1`, `OBR` and `OBX`. Each of them has helper methods to retrieve data from its respective HL7 segment without iterate over his `Field` objects.

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
>>> obx = h['OBX'][3] # 3rd instance
>>> (obx.identifier,
     obx.value_type,
     obx.value,
     obx.units,
     obx.reference_range,
     obx.datetime)
('DIA', 'NM', 85, 'mmHg', (50, 90), datetime.datetime(2018, 7, 3, 11, 17, 13))
```

## Network client
`python-xml-hl7` provides a simple network (TCP/IP) client, wich reads HL7 messages from [Alfamed](http://www.alfamed.com/) patient monitors like [VITA 200e](http://www.alfamed.com/monitor-multiparametro-vita-200.html).

```python
from hl7.xml.client import AlfamedClient

client = AlfamedClient('169.254.215.35') # Default communication port is 9100
client.read_message()  # By default, HL7 messages are converted into Message objects
client.read_message(parse_message=False) # Returns the original HL7 message as string
```

Invalid host addresses when instantiate `AlfamedClient` objects raises `AtributteError`

## Testing
You can run tests locally using `unittest` module

```
cd python-xml-hl7
python -m unittest tests
```

If all the tests pass you will see a success message like this
```
................
----------------------------------------------------------------------
Ran 16 tests in 0.007s

OK
```

## Notes

* For any suggestion, feature or bug fix, you can report a issue [here](https://github.com/weynelucas/python-xml-hl7/issues). Or submit a pull request
* For handle HL7 messages in original stream format, use solutions like [python-hl7](http://python-hl7.readthedocs.io/en/latest/) or [HL7apy](http://hl7apy.org/)

## Release Notes

* 0.1.0 - First release