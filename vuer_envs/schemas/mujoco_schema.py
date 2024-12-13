from .base import Xml, XmlTemplate


class Mjcf(XmlTemplate):
    tag = "mujoco"
    template = """
    <mujoco {attributes}>
        <worldbody>
            {children}
        </worldbody>
    </mujoco>
    """


# absorbed into the template class!
# class Worldbody(Xml):
#     tag = "worldbody"


class Link(Xml):
    tag = "link"

    def __init__(self, name, pos, climit, damping, **kwargs):
        super().__init__(name=name, pos=pos, climit=climit, damping=damping, **kwargs)
