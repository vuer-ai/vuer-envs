import os
from vuer_envs.schemas.room_xmls.room_1 import Room
from vuer_envs.utility import minimize_xml_lxml

def test_room_1():
    room = Room()
    spec_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(spec_dir, 'room_content_expected.xml'), 'r') as expected_raw_xml:
        expected_xml = minimize_xml_lxml(expected_raw_xml.read())
        assert room._minimized == expected_xml

    with open(os.path.join(spec_dir, 'room_preamble_expected.xml'), 'r') as expected_raw_xml:
        expected_xml = expected_raw_xml.read()
        assert room.preamble == expected_xml
        
    
if __name__ == "__main__":
    test_room_1()