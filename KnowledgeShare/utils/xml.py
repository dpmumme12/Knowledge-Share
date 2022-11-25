import xml.etree.ElementTree as ET


class XMLParse:
    """
    Takes in a filepath to xml document when class instantiated
    and parses the document.
    """
    def __init__(self, filepath: str) -> None:
        with open(filepath) as f:
            self.parsed_xml = ET.fromstringlist(['<root>', f.read(), '</root>'])

    def serialize_xml(self) -> list[dict]:
        """
        Serialize's the parsed XML into a list of dictionaries.
        Example XML to be serialized:

        <root>
            <record><recordtext>text</recordtext></record>
            <record>text</record>
        </root>

        Outputs: [{'record': {'recordtext': 'text'}}, {'record': 'text'}]

        Known flaws to fix:
        1. Does not currently serialize the attributes of tags.
        2. If duplicate tags exists in same tag except for root it will
            only return item for the last appearing of the same tags.
        3. If tag has text and child tags it will only return the serialized
            child tags and not the text in the tag.
        """
        out_list = []

        for node in self.parsed_xml:
            if len(node):
                out_list.append({node.tag: self.getchildrenobjects(node)})
            else:
                out_list.append({node.tag: node.text})

        return out_list

    def getchildrenobjects(self, node: ET.Element) -> dict:
        out_dict = {}
        for child in node:
            if len(child):
                out_dict[child.tag] = self.getchildrenobjects(child)
            else:
                out_dict[child.tag] = child.text

        return out_dict
