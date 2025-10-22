from datetime import datetime
from pathlib import Path
from typing import Union
import xml.etree.ElementTree as ET

from defusedxml import ElementTree as DET

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


class URLEntry:
    def __init__(
        self,
        loc: str,
        lastmod: str | None = None,
        changefreq: str | None = None,
        priority: float | None = None,
    ):
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = priority
        self.hreflang_alts: list[HreflangAlternate] = []

    def add_alternate(
        self, href_alt=None, hreflang: str = "", href: str = ""
    ) -> "URLEntry":
        """Add single hreflang alternate to URL"""
        if (not href_alt) and (not hreflang and not href):
            raise ValueError(
                "Either HreflangAlternate or both hreflang and href are required"
            )
        if isinstance(href_alt, HreflangAlternate):
            self.hreflang_alts.append(href_alt)
        else:
            self.hreflang_alts.append(HreflangAlternate(hreflang=hreflang, href=href))

        return self

    def add_alternates(self, alternates: list[dict]) -> "URLEntry":
        """Add multiple hreflang alternates to URL via dictionary"""
        for alt in alternates:
            href = alt.get("href")
            hreflang = alt.get("hreflang")

            if not href and not hreflang:
                raise ValueError("Missing both required fields: href and hreflang")
            if not href or not hreflang:
                raise ValueError(
                    f"Missing required field: {'href' if not href else 'hreflang'}"
                )

            href_alt = HreflangAlternate(hreflang=hreflang, href=href)
            self.hreflang_alts.append(href_alt)

        return self


class HreflangAlternate:
    def __init__(self, hreflang: str, href: str):
        self.rel = "alternate"
        self.hreflang = hreflang
        self.href = href


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

        if not isinstance(urls, list):
            raise TypeError(f"URLs must be in list. Recieved: {type(urls)}")

        if len(urls) < 1:
            raise ValueError("URL list must contain at least 1 URL")

        for url in urls:
            entry = URLEntry(
                loc=url,
            )
            instance.urls.append(entry)

        return instance

    def add_url(self, url: str | URLEntry, **kwargs) -> "Sitemap":
        """Add URL entry to sitemap"""
        if isinstance(url, URLEntry):
            self.urls.append(url)
        else:
            self.urls.append(URLEntry(loc=url, **kwargs))

        return self

    def remove_url(self, url: str) -> "Sitemap":
        """Remove URL from sitemap"""
        self.urls = [u for u in self.urls if u.loc != url]
        return self

    def get_urls_by_pattern(self, pattern: str) -> "URLEntry":
        """Get list of URLEntries matching pattern"""
        import re

        regex = re.compile(pattern)
        res = [u for u in self.urls if regex.search(u.loc)]
        return res

    def deduplicate(self) -> "Sitemap":
        """Remove duplicate URLs"""
        seen = set()
        unique = []
        for u in self.urls:
            if u.loc not in seen:
                seen.add(u.loc)
                unique.append(u)
        self.urls = unique
        return self

    def write_to_file(self, output_filename: str = None) -> "Sitemap":
        """Write a sitemap XML file from current instance.

        Args:
            output_filename (str) [Optional]: The desired name of the XML file. Default = "sitemap.xml

        Returns:
            bool: Operation success
        """
        if not output_filename:
            output_filename = "sitemap.xml"

        root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        for url_entry in self.urls:
            self._append_url_element(root=root, url_entry=url_entry)

        tree = ET.ElementTree(root)
        ET.indent(tree, space="   ")
        tree.write(output_filename, encoding="utf-8", xml_declaration=True)

        return self

    def set_all_lastmod(self, date: str) -> "Sitemap":
        """Set lastmod for all URLs to the specified date"""
        for url in self.urls:
            url.lastmod = date
        return self

    def set_all_lastmod_to_today(self) -> "Sitemap":
        """Set lastmod for all URLs to today's date"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.set_all_lastmod(today)

    def _append_url_element(self, root: ET.Element, url_entry: URLEntry):
        """Append URL element to given root element"""
        url_elem = ET.SubElement(root, "url")
        loc = ET.SubElement(url_elem, "loc")

        loc.text = url_entry.loc

        if url_entry.lastmod is not None:
            lastmod = ET.SubElement(url_elem, "lastmod")
            lastmod.text = url_entry.lastmod

        if url_entry.changefreq is not None:
            changefreq = ET.SubElement(url_elem, "changefreq")
            changefreq.text = url_entry.changefreq

        if url_entry.priority is not None:
            priority = ET.SubElement(url_elem, "priority")
            priority.text = str(url_entry.priority)

        if url_entry.hreflang_alts:
            for alt in url_entry.hreflang_alts:
                _ = ET.SubElement(
                    url_elem,
                    "{http://www.w3.org/1999/xhtml}link",
                    rel="alternate",
                    hreflang=alt.hreflang,
                    href=alt.href,
                )

    def __len__(self):
        return len(self.urls)

    def __iter__(self):
        return iter(self.urls)
