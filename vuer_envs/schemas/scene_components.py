from vuer_envs.schemas.base import XmlTemplate

class RobotBase(XmlTemplate):

    preamble = ""
    template = ""

    @property
    def _xml(self):
        pass



class MobilePanda(XmlTemplate):
    preamble = """
    """
    template = """
    
    """

    def __init__(self, name, pos, quat, **kwargs):
        super().__init__(name=name, pos=pos, quat=quat, **kwargs)
