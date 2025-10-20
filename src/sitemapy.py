from datetime import datetime
from pathlib import Path
from typing import Union
import xml.etree.ElementTree as ET

from defusedxml import ElementTree as DET

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


class URLEntry:
    def __init__(self, loc: str):
        self.loc = loc
        self.lastmod = ""


class Sitemap:
    def __init__(self):
        self.urls: list[URLEntry] = []

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "Sitemap":
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
        for element in root.findall(
            ".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"
        ):
            loc_element = element.find(f"{SITEMAP_NS}loc")
            if loc_element is not None and loc_element.text:
                url_entry = URLEntry(loc=loc_element.text)

                lastmod_elem = element.find(f"{SITEMAP_NS}lastmod")
                if lastmod_elem is not None and lastmod_elem.text:
                    url_entry.lastmod = lastmod_elem.text

                instance.urls.append(url_entry)

        return instance

    @classmethod
    def from_list(cls, urls: list[str]) -> "Sitemap":
        """Builds basic sitemap from list of URLs, with no additonal attributes"""
        instance = cls()

        if len(urls) < 1:
            raise ValueError("URL list must contain at least 1 URL")

        for url in urls:
            entry = URLEntry(
                loc=url,
            )
            instance.urls.append(entry)

        return instance

    def write_to_file(
        self, output_filename: str = None, lastmod_now: bool = False
    ) -> "Sitemap":
        """Write a sitemap XML file from current instance.

        Args:
            output_filename (str) [Optional]: The desired name of the XML file. Default = "sitemap.xml
            lastmod_now (bool): Create lastmod attribute per URL, set to today's date. Default = False

        Returns:
            bool: Operation success
        """
        if not output_filename:
            output_filename = "sitemap.xml"

        root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        for url_entry in self.urls:
            self._append_url_element(
                root=root, url=url_entry.loc, lastmod_now=lastmod_now
            )

        tree = ET.ElementTree(root)
        ET.indent(tree, space="   ")
        tree.write(output_filename, encoding="utf-8", xml_declaration=True)

        return self

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
