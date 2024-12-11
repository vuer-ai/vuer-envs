from robosuite.environments.base import register_env
from .living_room import LivingRoom
from .living_room_lift import LivingRoomLift

register_env(LivingRoom)
register_env(LivingRoomLift)