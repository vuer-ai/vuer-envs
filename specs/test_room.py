from vuer_envs.schemas.room_xmls.room_1 import Room
from vuer_envs.utils.file import File
from vuer_envs.utils.minimizer import minimize


def test_room_1():
    room = Room()

    assert room._minimized == File @ "room_content_expected.xml" | minimize

    assert room.preamble == File @ "room_preamble_expected.xml"


if __name__ == "__main__":
    test_room_1()
