from lxml import etree


class MetaFile(type):
    def __matmul__(cls, filepath: str):
        """
        Opens the given file in read mode and returns its content.

        Args:
            filepath (str): Path to the file to be opened.

        Returns:
            str: Contents of the file as a string.
        """
        try:
            with open(filepath, "r") as f:
                return f.read()
        except Exception as e:
            print(f"Error opening file: {e}")
            return ""


class File(metaclass=MetaFile):
    pass


# Function to walk through leaves
def walk_leaves(element, fn):
    fn(element)
    for child in element:
        walk_leaves(child, fn)


class Minimize:
    @staticmethod
    def __call__(xml_string: str) -> str:
        """
        Minimizes an XML string using lxml by removing unnecessary whitespace and
        collapsing long empty strings between angle brackets.

        Args:
            xml_string (str): The original XML string.

        Returns:
            str: The minimized XML string.
        """
        try:
            # Parse the XML string
            parser = etree.XMLParser(remove_blank_text=True)
            root = etree.XML(xml_string, parser)

            def strip_whitespace(element: etree.Element):
                if element.text:
                    element.text = element.text.strip() or None
                if element.tail:
                    element.tail = element.tail.strip() or None

            walk_leaves(root, strip_whitespace)

            # Convert the parsed XML back to a single minimized string
            minimized_xml = etree.tostring(root, encoding="unicode", method="xml", pretty_print=False).strip()

            return minimized_xml
        except Exception as e:
            print(f"Error minimizing XML with lxml: {e}")
            return ""

    @staticmethod
    def _strip_whitespace_recursively(element):
        """
        Recursively strips whitespace from XML elements' text and tail,
        including their nested children.

        Args:
            element: The current XML element to process.
        """
        if element.text:
            element.text = element.text.strip()
        if element.tail:
            element.tail = element.tail.strip()

        # Process all child elements
        for child in element:
            Minimize._strip_whitespace_recursively(child)

    def __ror__(self, s: str) -> str:
        return self(s)


minimize = Minimize()

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
    assert minimized == "<root><person><name>John Doe</name><age>30</age></person></root>"
