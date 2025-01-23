from typing import List

from lxml import etree

from vuer_envs.schemas.base import XmlTemplate
from vuer_envs.utils.tree_merge import merge_many


def mujoco_hash(e: etree.Element) -> str:
    # this means it is a comment component.
    if not isinstance(e.tag, str):  # .func_name == 'Comment':
        return str(e)

    values = dict(
        k=e.attrib.get("key", ""),
        n=e.attrib.get("name", ""),
        c=e.attrib.get("class", ""),
        f=e.attrib.get("file", ""),
        m=e.attrib.get("mesh", ""),
        j=e.attrib.get("joint1", ""),
        j2=e.attrib.get("joint2", ""),
        o=e.attrib.get("object1", ""),
        o2=e.attrib.get("object2", ""),
    )
    return f"<{e.tag}[{values}]/>"


class MjNode(XmlTemplate):
    def __init__(
        self,
        *_children,
        attributes=None,
        preamble: str = None,
        postamble: str = None,
        children: List[str] = None,
        **kwargs,
    ):
        super().__init__(
            *_children,
            preamble=preamble,
            children=children,
            postamble=postamble,
            **attributes or {},
        )

        for k, v in kwargs.items():
            setattr(self, k, v)

    def join(self, *s):
        return merge_many(*s, hash_fn=mujoco_hash)


class Body(MjNode):
    """
    Robot link element.

    Inside link.content, you can define the body of the link, including the inertial properties, joint properties, and geometry properties.
    Inside link.asset, you can define the material, mesh or texture properties.

    name should be a unique identifier for the link.
    """

    tag = "body"
    template = """
    <body {attributes}>
        {children}
    </body>
    """


class Mjcf(MjNode):
    """
    This is the root element of the MuJoCo XML file.

    """

    tag = "mujoco"
    template = """
    <mujoco {attributes}>
        {preamble}
        <worldbody>
            {children}
        </worldbody>
        {postamble}
    </mujoco>
    """


# class BoxExample(Body):
#     name = "box-1"
#     """this is a placeholder name."""
#
#     @property
#     def preamble(self):
#         return f"""
#         <asset>
#             <texture name="{self.name}" type="2d" builtin="checker" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3" mark="cross" width="200" height="200"/>
#             <material name="matplane" reflectance="0.5" texture="texplane" texrepeat="1 1" texuniform="true"/>
#         </asset>
#         """
