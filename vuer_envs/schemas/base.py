import inspect

from vuer_envs.utility import minimize_xml_lxml


class Xml:
    """This is the base class for all XML elements."""

    tag = "mujoco"
    _attributes: dict
    _children: list

    def __init__(self, *_children, tag=None, children=[], **attributes):
        self.tag = tag or self.tag
        self._attributes = attributes
        self._children = list(_children) + children

    @property
    def attributes(self) -> str:
        """Return the string representation of the attributes."""
        return " ".join([f'{key}="{value}"' for key, value in self._attributes.items()])

    @property
    def children(self) -> str:
        """Return the string representation of the children."""
        return "\n".join([child._xml for child in self._children])

    @property
    def _xml(self) -> str:
        """Return the XML representation of the model."""
        return f"""
        <{self.tag} {self.attributes}>{
        self.children
        }</{self.tag}>
        """

    @property
    def _minimized(self) -> str:
        """Return the minimized XML representation of the model."""
        raw_xml = self._xml
        minimized_xml = minimize_xml_lxml(raw_xml)
        return minimized_xml


class XmlTemplate(Xml):
    """Template-based XML element.

    You can use template strings to define the XML structure. This
    way, you don't have to nest unnecessarily.

    Here is an example of the base Mjcf class:

    .. code:: python

            class Mjcf(XmlTemplate):
                tag = "mujoco"
                template = \"\"\"
                <mujoco {attributes}>
                    <worldbody>
                        {children}
                    </worldbody>
                </mujoco>
                \"\"\"

    Now, for a room scene, you can do something like

    .. code:: python

        from vuer_envs.schemas.rooms import Room, Fixtures, Walls

        Room(name="room1", children=[
            Fixtures(position=[0, 0, 1]),
            Walls(size=[10, 10, 10]... ),
        ])

    """

    template = ""

    @property
    def _xml(self) -> str:
        all_properties = {}

        for name, value in inspect.getmembers(type(self), lambda x: isinstance(x, property)):
            if not name.startswith("_"):
                all_properties[name] = getattr(self, name)

        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                all_properties[key] = value

        return self.template.format(**all_properties)
