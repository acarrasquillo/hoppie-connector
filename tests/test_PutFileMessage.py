from hoppie_connector.Messages import PutFileMessage, HoppieMessage, HoppieMessage as Super
import unittest

class TestValidDataReqMessage(unittest.TestCase):
    _EXPECTED_FROM: str = '123'
    _EXPECTED_TO: str = 'CALLSIGN.LSH'
    _EXPECTED_TYPE: HoppieMessage.MessageType = HoppieMessage.MessageType.PUTFILE
    _EXPECTED_PACKET: str = f"""
    ACARS BEGIN

    05/08/24
    WBCM DOUBLE CLASS
    LOADSHEET FLIGHT {_EXPECTED_TO}
    LM LOADSHEET FINAL
    SGAS/MPTO // CMP206
    VERSION B738

    LOAD PLANNER
    ZFW 130839 MAX 138300
    TOF 40916
    TOW 171755 MAX 174200
    TIF 34604
    LAW 137220 MAX 146300
    UNDLD 7461
    MACTOW 22.6%
    DOI 21.7%
    PAX/10/121 TTL/131
    ADULT/130 CHLD/0 INF/0
    DHC 1
    CARGO 5748/7026
    TTL CARGO 12774

    ACARS END
    """
    _EXPECTED_MSG_PARAM: dict = {
        'from': _EXPECTED_FROM,
        'to': _EXPECTED_TO,
        'type': _EXPECTED_TYPE.value,
        'packet': _EXPECTED_PACKET
    }

    def setUp(self) -> None:
        super().setUp()
        self._UUT = PutFileMessage(self._EXPECTED_FROM, self._EXPECTED_TO,self._EXPECTED_PACKET)

    def test_get_from_name(self):      self.assertEqual(self._EXPECTED_FROM,      self._UUT.get_from_name())
    def test_get_to_name(self):        self.assertEqual(self._EXPECTED_TO,        self._UUT.get_to_name())
    def test_get_msg_type(self):       self.assertEqual(self._EXPECTED_TYPE,      self._UUT.get_msg_type())
    def test_get_packet_content(self): self.assertEqual(self._EXPECTED_PACKET,  self._UUT.get_packet_content())
    def test_get_msg_params(self):     self.assertEqual(self._EXPECTED_MSG_PARAM, self._UUT.get_msg_params())

class TestPutFileMessageInputValidation(unittest.TestCase):
    def test_invalid_station(self):         self.assertRaises(ValueError, lambda: PutFileMessage('123456789', 'CALLSIGN.LSH', 25 * 'a' ))
    def test_invalid_filename(self): self.assertRaises(ValueError, lambda: PutFileMessage('123','CALLSIGN', 25 * 'a'))
    def test_invalid_file_size(self):       self.assertRaises(ValueError, lambda: PutFileMessage('123','CALLSIGN.LSH', 501 * 'a'))

class TestPutFileMessageRepresentation(unittest.TestCase):
    def test_repr(self):
        expected = PutFileMessage('STATION','CALLSIGN.LSH','ACARS LOADSHEET')
        actual = eval(repr(expected))
        self.assertEqual(expected, actual)