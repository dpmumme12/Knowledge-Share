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

        Known flaws (not fixed — reviewed against the only current consumer,
        the log viewer's XMLLogFormatter output, and found not to apply there):
        1. Does not currently serialize the attributes of tags. The log
            formatter never emits attributes, only nested elements and text.
        2. If duplicate tags exist in the same parent (except root) only the
            last one is kept. Each <log> entry's children (level, time,
            module, process, thread, message, traceback) are all distinct
            tags, so no collisions occur. Repeated <log> entries under
            <root> are unaffected since the root level is returned as a list.
        3. If a tag has both text and child tags, only the child tags are
            returned. No element in the log format mixes text with children
            (each node is either a leaf with text or a parent with only
            element children), so this flaw does not manifest.
        If the log XML schema changes to introduce attributes, duplicate
        sibling tags, or mixed text/children content, revisit this class.
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
