from lxml import etree


def minimize(xml_string) -> str:
    """
    Minimizes an XML string using lxml by removing unnecessary whitespace.

    Args:
        xml_string (str): The original XML string.

    Returns:
        str: The minimized XML string.
    """
    xml_string = xml_string.strip()

    try:
        # Parse the XML string
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_string, parser)

        # Serialize the XML back to string without pretty_print
        minimized_xml = etree.tostring(root, encoding="unicode", pretty_print=False)

        return minimized_xml
    except Exception as e:
        print(f"Error minimizing XML with lxml: {e}")
        return ""


if __name__ == "__main__":
    # Example usage
    xml = """
    <root>
        <person>
            <name>John Doe</name>
            <age>30</age>
        </person>
    </root>
    """

    minimized = minimize(xml)
    print(minimized)
    assert minimized == '<root><person><name>John Doe</name><age>30</age></person></root>'
