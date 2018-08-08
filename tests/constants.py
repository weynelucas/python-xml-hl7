import datetime


HL7_MESSAGE = """
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

EXPECTED_VALUES = {
    'MSH': ('|', '^~\\&', 'hospital', datetime.datetime(2018, 7, 3, 11, 17, 43), ('ORU', 'R01'), '2.3.1'),
    'PID': ('shenzhen', '1', 'libang', datetime.datetime(2009,10,10), 'M'),
    'PV1': ('U', 'adult', datetime.datetime(2018, 7, 26,18, 13, 46)),
    'OBR': (datetime.datetime(2018, 7, 3, 11, 17, 43), ),
    'OBX': (
        ('NM', 'SPO2',    96,  '%',    (90, 100), None),
        ('NM', 'PR',      68,  'bpm',  (50, 120), None),
        ('NM', 'SYS',     131, 'mmHg', (90, 160), datetime.datetime(2018, 7, 3, 11, 17, 13)),
        ('NM', 'DIA',     85,  'mmHg', (50, 90),  datetime.datetime(2018, 7, 3, 11, 17, 13)),
        ('NM', 'MAP',     100, 'mmHg', (60, 110), datetime.datetime(2018, 7, 3, 11, 17, 13)),
        ('NM', 'NIBP_PR', 73,  'bpm',  (50, 120), datetime.datetime(2018, 7, 3, 11, 17, 13)),
    ),
}