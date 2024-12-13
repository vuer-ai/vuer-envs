from vuer_envs.utility import minimize_xml_lxml


class Xml:
    tag = "mujoco"
    attributes: dict
    children: list

    def __init__(self, *_children, tag=None, children=[], **attributes):
        self.tag = tag or self.tag
        self.attributes = attributes
        self.children = list(_children) + children

    @property
    def _attribute_str(self) -> str:
        """Return the string representation of the attributes."""
        return " ".join([f'{key}="{value}"' for key, value in self.attributes.items()])

    @property
    def _children_str(self) -> str:
        """Return the string representation of the children."""
        return "\n".join([child.xml for child in self.children])

    @property
    def xml(self) -> str:
        """Return the XML representation of the model."""
        return f"""
        <{self.tag} {self._attribute_str}>{
        self._children_str
        }</{self.tag}>
        """

    @property
    def xml_minimized(self) -> str:
        raw_xml = self.xml
        minimized = minimize_xml_lxml(raw_xml)
        return minimized


class XmlTemplate(Xml):
    template = ""

    @property
    def xml(self) -> str:
        return self.template.format(
            children=self._children_str,
            attributes=self._attribute_str,
        )
