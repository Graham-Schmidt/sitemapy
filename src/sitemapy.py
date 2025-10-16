from datetime import datetime
import xml.etree.ElementTree as ET


class URLEntry:
    def __init__(self, full_url: str):
        self.full_url = full_url
        self.lastmod = ""


class Sitemap:
    def __init__(self):
        self.output_filename: str = ""
        self.urls: list[URLEntry] = []

    def load_from_list(self, urls: list[str]):
        """Builds basic sitemap from list of URLs, with no additonal attributes"""
        if len(urls) < 1:
            return ValueError("URL list must contain at least 1 URL")

        for url in urls:
            entry = URLEntry(
                full_url=url,
            )
            self.urls.append(entry)

    # proposal - turn into `build_from_list()`
    def write_sitemap_to_file(
        self, output_filename: str = None, lastmod_now: bool = False
    ):
        """Write a sitemap XML file from current instance.

        Args:
            output_filename (str) [Optional]: The desired name of the XML file. Default = "sitemap.xml
            lastmod_now (bool): Create lastmod attribute per URL, set to today's date. Default = False

        Returns:
            bool: Operation success
        """
        try:
            if not output_filename:
                output_filename = "sitemap.xml"

            root = ET.Element(
                "urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            )

            for url_entry in self.urls:
                self._append_url_element(
                    root=root, url=url_entry.full_url, lastmod_now=lastmod_now
                )

            tree = ET.ElementTree(root)
            ET.indent(tree, space="   ")
            tree.write(output_filename, encoding="utf-8", xml_declaration=True)
            return True
        except:
            return False

    def _append_url_element(
        self, root: ET.Element, url: str, lastmod_now: bool = False
    ):
        """Append URL element to given root element"""
        url_elem = ET.SubElement(root, "url")
        loc = ET.SubElement(url_elem, "loc")

        if lastmod_now:
            lastmod = ET.SubElement(url_elem, "lastmod")
            date_string = datetime.now().strftime("%Y-%m-%d")
            lastmod.text = date_string

        loc.text = url
