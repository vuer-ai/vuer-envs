from lxml import etree


def remove_unused_mesh(file_path, to=None):
    try:
        print(f"Reading file: {file_path}")

        # Parse the XML file
        tree = etree.parse(file_path)
        root = tree.getroot()

        # Gather all used <mesh> elements
        used_mesh_names = {mesh.attrib.get("mesh", "") for mesh in root.findall(".//geom")}

        # Identify and remove unused <mesh> elements
        for mesh in root.findall(".//mesh"):
            mesh_name = mesh.attrib.get("name", "")
            if mesh_name not in used_mesh_names:  # Check if the mesh is unused
                print(f"Removing unused mesh element: <mesh name='{mesh_name}'/>")
                parent = mesh.getparent()
                if parent is not None:
                    parent.remove(mesh)

        # # Filter <geom> elements with 'group' == 0 or unused 'mesh' attribute
        # for geom in root.findall(".//geom"):
        #     mesh_name = geom.attrib.get("mesh", "")
        #     group = geom.attrib.get("group", 0)
        #     if group == 0:
        #         parent = geom.getparent()
        #         if parent is not None:
        #             parent.remove(geom)
        #             print(f"Removed geom element: <geom mesh='{mesh_name}' group={group}/>")

        save_location = to or file_path

        # Save changes back to the XML file
        tree.write(save_location, encoding="utf-8", xml_declaration=True, pretty_print=True)
        print(f"Updated XML file saved successfully: {save_location}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except OSError as e:
        print(f"OS error occurred: {e}")
    except etree.XMLSyntaxError as e:
        print(f"XML parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Provide the correct path
    file_path = "/assets/scene0001/scene.mjcf.xml"
    remove_unused_mesh(file_path)
