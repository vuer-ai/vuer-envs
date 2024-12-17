from vuer_envs.schemas.base import Xml, XmlTemplate


class Link(XmlTemplate):
    """
    Robot link element.

    Inside link.content, you can define the body of the link, including the inertial properties, joint properties, and geometry properties.
    Inside link.asset, you can define the material, mesh or texture properties.

    name should be a unique identifier for the link.
    """

    tag = "body"
    content = ""
    asset = ""
    template = """
    <body {attributes}>
        {content}
        {children}
    </body>
    """

    @property
    def preamble(self):
        """Return the preamble of the link."""
        self.asset = self.asset.format(name=self.name)

        gathered = []
        for child in self._children:
            try:
                gathered.append(child.preamble)
            except AttributeError:
                continue

        return self.asset + "\n".join(gathered)

    def __init__(self, *_children, name, children=[], **rest):
        self.name = name
        self.content = self.content.format(name=name)
        super().__init__(*_children, tag=self.tag, children=children, name=name, **rest)
