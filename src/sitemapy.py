from datetime import datetime
from pathlib import Path
from typing import Union
import xml.etree.ElementTree as ET

from defusedxml import ElementTree as DET


class URLEntry:
    def __init__(self, full_url: str):
        self.full_url = full_url
        self.lastmod = ""


class Sitemap:
    def __init__(self):
        self.urls: list[URLEntry] = []

    @classmethod
    def from_file(cls, path: Union[str, Path]):
        """
        Builds sitemap object from provided XML file

        Args:
            path (str or Path): the filepath to the XML file

        Returns:
            Sitemap: instance of Sitemap
        """
        instance = cls()

        path = Path(path)

        et = DET.parse(path)
        root = et.getroot()
        for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
            url_entry = None
            for sub_elem in elem:
                if "loc" in sub_elem.tag:
                    url_entry = URLEntry(full_url=sub_elem.text)
                elif "lastmod" in sub_elem.tag:
                    url_entry.lastmod = sub_elem.text
            instance.urls.append(url_entry)

        return instance

    @classmethod
    def from_list(self, urls: list[str]):
        """Builds basic sitemap from list of URLs, with no additonal attributes"""
        if len(urls) < 1:
            return ValueError("URL list must contain at least 1 URL")

        for url in urls:
            entry = URLEntry(
                full_url=url,
            )
            self.urls.append(entry)

    def write_to_file(self, output_filename: str = None, lastmod_now: bool = False):
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
