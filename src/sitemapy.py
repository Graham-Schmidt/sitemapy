import xml.etree.ElementTree as ET

class Sitemap:
    def __init__(self):
        pass
        
    def write_sitemap_to_file(self, input_urls: list[str], output_filename: str = None):
        """Write a sitemap XML file.

        Args:
            input_urls (list[str]): A list of URLs to pupulate the sitemap with
            output_filename (str) [Optional]: The desired name of the XML file. Default = "sitemap.xml

        Returns:
            bool: Operation success
        """
        try:
            if len(input_urls) < 1:
                return ValueError("List of URLs must have at least one value")

            if not output_filename:
                output_filename = "sitemap.xml"

            root = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

            
            for url in input_urls:
                self._append_url_element(root=root, url=url)

            tree = ET.ElementTree(root)
            ET.indent(tree, space="   ")
            tree.write(output_filename, encoding="utf-8", xml_declaration=True)
            return True
        except:
            return False

    def _append_url_element(self, root: ET.Element, url: str):
        """Append URL element to given root element"""
        url_elem = ET.SubElement(root, 'url')
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = url
