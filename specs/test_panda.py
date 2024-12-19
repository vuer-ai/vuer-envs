import os
from vuer_envs.schemas.robot_xmls.panda import Panda
from vuer_envs.utility import minimize

def test_panda():
    panda = Panda(name="test_panda", pos="0 0 0", quat="0 0 0 1")
    spec_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(spec_dir, 'panda_content_expected.xml'), 'r') as expected_raw_xml:
        expected_xml = minimize(expected_raw_xml.read())
        assert panda._minimized == expected_xml
    
    with open(os.path.join(spec_dir, 'panda_preamble_expected.xml'), 'r') as expected_raw_xml:
        expected_xml = expected_raw_xml.read()
        assert panda.preamble == expected_xml
        
    
if __name__ == "__main__":
    test_panda()