from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
import gzip

from defusedxml import ElementTree as DefusedElementTree

SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
IMAGE_NS = "{http://www.google.com/schemas/sitemap-image/1.1}"
NEWS_NS = "{http://www.google.com/schemas/sitemap-news/0.9}"


class ImageEntry:
    def __init__(self, loc: str):
        self.loc = loc


class NewsEntry:
    def __init__(
        self,
        publication_name: str | None = None,
        publication_language: str | None = None,
        publication_date: str | None = None,
        title: str | None = None,
    ):
        self.publication_name = publication_name
        self.publication_language = publication_language
        self.publication_date = publication_date
        self.title = title


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
        self.images: list[ImageEntry] = []
        self.news_entry: NewsEntry = None

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

    def add_image(self, image: str | ImageEntry) -> "URLEntry":
        """Append image element to URLEntry"""
        self._add_element(image, ImageEntry)

        return self

    def add_news_entry(self, news_entry: NewsEntry) -> "URLEntry":
        """Append news element to URLEntry - requires NewsEntry object"""
        self._add_element(news_entry, NewsEntry)

        return self

    def _add_element(self, data, class_type, **kwargs):
        """handler to append element to XML tree by type"""
        if isinstance(data, ImageEntry):
            self.images.append(data)
            return
        elif isinstance(data, NewsEntry):
            self.news_entry = data
            return

        constructors = {
            ImageEntry: lambda d, **kw: ImageEntry(loc=d),
        }

        handler = constructors[class_type]
        if handler:
            self._get_collections(class_type).append(handler(data, **kwargs))
        else:
            raise TypeError(f"Unsupported type: {class_type}")

    def _get_collections(self, class_type):
        collections = {ImageEntry: self.images}
        return collections[class_type]


class HreflangAlternate:
    def __init__(self, hreflang: str, href: str):
        self.rel = "alternate"
        self.hreflang = hreflang
        self.href = href


class Sitemap:
    def __init__(self):
        self.urls: list[URLEntry] = []

    @classmethod
    def from_file(cls, path: str | Path) -> "Sitemap":
        """
        Builds sitemap object from provided XML file

        Args:
            path (str or Path): the filepath to the XML file

        Returns:
            Sitemap: instance of Sitemap
        """
        instance = cls()

        path = Path(path)

        et = DefusedElementTree.parse(path)
        root = et.getroot()
        for element in root.findall(f".//{SITEMAP_NS}url"):
            url_entry = cls._build_url_entry(url_element=element)
            instance.urls.append(url_entry)

        return instance

    @classmethod
    def from_list(cls, urls: list[str | URLEntry]) -> "Sitemap":
        """Builds basic sitemap from list of URLs, with no additonal attributes"""
        instance = cls()

        if not isinstance(urls, list):
            raise TypeError(f"URLs must be in list. Recieved: {type(urls).__name__}")

        for url in urls:
            if isinstance(url, str):
                entry = URLEntry(
                    loc=url,
                )
                instance.urls.append(entry)
            elif isinstance(url, URLEntry):
                instance.urls.append(url)

        return instance

    @classmethod
    def _build_url_entry(cls, url_element: ET.Element) -> "URLEntry":
        """Construct a URL Element"""
        loc_element = url_element.find(f"{SITEMAP_NS}loc")
        if loc_element is not None and loc_element.text:
            url_entry = URLEntry(loc=loc_element.text)

            lastmod_element = url_element.find(f"{SITEMAP_NS}lastmod")

            if lastmod_element is not None and lastmod_element.text:
                url_entry.lastmod = lastmod_element.text

            priority_element = url_element.find(f"{SITEMAP_NS}priority")

            if priority_element is not None and priority_element.text:
                url_entry.priority = float(priority_element.text)

            changefreq_element = url_element.find(f"{SITEMAP_NS}changefreq")

            if changefreq_element is not None and changefreq_element.text:
                url_entry.changefreq = changefreq_element.text

            # Handle image elements
            image_element = url_element.find(f"{IMAGE_NS}image")
            if image_element:
                image_entry = cls._build_image_entry(image_element)
                url_entry.images.append(image_entry)

            # Handle news elements
            news_element = url_element.find(f"{NEWS_NS}news")
            if news_element:
                news_entry = cls._build_news_entry(news_element)
                url_entry.news_entry = news_entry

        return url_entry

    @classmethod
    def _build_image_entry(cls, image_element: ET.Element) -> "ImageEntry":
        """Construct an Image element"""
        loc_element = image_element.find(f"{IMAGE_NS}loc")
        if loc_element is not None and loc_element.text:
            image_entry = ImageEntry(loc=loc_element.text)

        return image_entry

    @classmethod
    def _build_news_entry(cls, news_element: ET.Element) -> "NewsEntry":
        """Construct a News element"""
        publication_element = news_element.find(f"{NEWS_NS}publication")
        date_element = news_element.find(f"{NEWS_NS}publication_date")
        title_element = news_element.find(f"{NEWS_NS}title")

        name_element = publication_element.find(f"{NEWS_NS}name")
        language_element = publication_element.find(f"{NEWS_NS}language")

        news_entry = NewsEntry(
            publication_name=name_element.text,
            publication_language=language_element.text,
            publication_date=date_element.text,
            title=title_element.text,
        )

        return news_entry

    def add_url(self, url: str | URLEntry, **kwargs) -> "Sitemap":
        """Add URL entry to sitemap"""
        if isinstance(url, URLEntry):
            self.urls.append(url)
        else:
            self.urls.append(URLEntry(loc=url, **kwargs))

        return self

    def remove_url(self, url: str | URLEntry) -> "Sitemap":
        """Remove URL from sitemap"""
        if isinstance(url, str):
            self.urls = [u for u in self.urls if u.loc != url]
        elif isinstance(url, URLEntry):
            self.urls = [u for u in self.urls if u.loc != url.loc]

        return self

    def get_urls_by_pattern(self, pattern: str) -> list["URLEntry"]:
        """Get list of URLEntry objects matching regex pattern"""
        import re

        regex = re.compile(pattern)
        res = [u for u in self.urls if regex.search(u.loc)]

        return res

    def deduplicate(self) -> "Sitemap":
        """Remove duplicate all elements by URLs"""

        seen = set()
        unique = []
        for i in self.urls:
            if i.loc not in seen:
                seen.add(i.loc)
                unique.append(i)
        self.urls = unique

        return self

    def write_to_file(self, output_filename: str = None) -> "Sitemap":
        """Write a sitemap XML file from current instance.

        Args:
            output_filename (str) [Optional]: The desired name of the XML file. Default = "sitemap.xml

        Returns:
            sitemap: an instance of Sitemap
        """
        if not output_filename:
            output_filename = "sitemap.xml"

        urlset_attrib = self._get_required_namespaces()

        root = ET.Element(
            "urlset",
            xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
            attrib=urlset_attrib,
        )

        for url_entry in self.urls:
            self._append_url_element(root=root, url_entry=url_entry)

        tree = ET.ElementTree(root)
        ET.indent(tree, space="   ")  # 3 spaces
        tree.write(output_filename, encoding="UTF-8", xml_declaration=True)

        return self

    def write_compressed(self, output_filename: str = None) -> "Sitemap":
        """
        Write compressed sitemap file (.xml.gz).

        Args:
            output_filename: Output filename (will add .gz if not present)

        Returns:
            Path to created file
        """
        if not output_filename:
            output_filename = "sitemap.xml.gz"
        elif not output_filename.endswith(".gz"):
            output_filename += ".gz"

        root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for url_entry in self.urls:
            self._append_url_element(root=root, url_entry=url_entry)

        tree = ET.ElementTree(root)
        ET.indent(tree, space="   ")

        with gzip.open(output_filename, "wb") as f:
            tree.write(f, encoding="UTF-8", xml_declaration=True)

        return output_filename

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

        if url_entry.images:
            for image in url_entry.images:
                self._append_image_element(url_elem=url_elem, image_entry=image)

        if url_entry.news_entry:
            self._append_news_element(
                url_elem=url_elem, news_entry=url_entry.news_entry
            )

    def _append_image_element(self, url_elem: ET.Element, image_entry: ImageEntry):
        """Append Image element to URL element"""
        image = ET.SubElement(url_elem, "image:image")
        image_loc = ET.SubElement(image, "image:loc")
        image_loc.text = image_entry.loc

    def _append_news_element(self, url_elem: ET.Element, news_entry: NewsEntry):
        """Append News element to URL element"""
        news_parent_element = ET.SubElement(url_elem, "news:news")

        if news_entry.publication_name or news_entry.publication_language:
            publication_parent_element = ET.SubElement(
                news_parent_element, "news:publication"
            )

            if news_entry.publication_name:
                pub_name_element = ET.SubElement(
                    publication_parent_element, "news:name"
                )
                pub_name_element.text = news_entry.publication_name

            if news_entry.publication_language:
                pub_language_element = ET.SubElement(
                    publication_parent_element, "news:language"
                )
                pub_language_element.text = news_entry.publication_language

        if news_entry.publication_date:
            pub_date_element = ET.SubElement(
                news_parent_element, "news:publication_date"
            )
            pub_date_element.text = news_entry.publication_date

        if news_entry.title:
            title_element = ET.SubElement(news_parent_element, "news:title")
            title_element.text = news_entry.title

    def _get_required_namespaces(self):
        """Return XML namespace per element type to be written to file"""
        namespaces = {}
        if any(url.images for url in self.urls):
            namespaces["xmlns:image"] = (
                "http://www.google.com/schemas/sitemap-image/1.1"
            )
        if any(url.news_entry for url in self.urls):
            namespaces["xmlns:news"] = "http://www.google.com/schemas/sitemap-news/0.9"

        return namespaces

    def __len__(self):
        return len(self.urls)

    def __iter__(self):
        return iter(self.urls)


class IndexEntry:
    def __init__(self, loc: str, lastmod: str = None):
        self.loc: str = loc
        self.lastmod: str = lastmod


class SitemapIndex:
    def __init__(self):
        self.index_entries: list[IndexEntry] = []

    @classmethod
    def from_file(cls, path: str | Path) -> "SitemapIndex":
        """
        Builds SitemapIndex object from provided XML file

        Args:
            path (str or Path): the filepath to the XML file

        Returns:
            SitemapIndex: instance of SitemapIndex
        """
        instance = cls()

        path = Path(path)

        et = DefusedElementTree.parse(path)
        root = et.getroot()
        for element in root.findall(f".//{SITEMAP_NS}sitemap"):
            loc_element = element.find(f"{SITEMAP_NS}loc")
            if loc_element is not None and loc_element.text:
                index_entry = IndexEntry(loc=loc_element.text)

                lastmod_element = element.find(f"{SITEMAP_NS}lastmod")
                if lastmod_element is not None and lastmod_element.text:
                    index_entry.lastmod = lastmod_element.text

                instance.index_entries.append(index_entry)

        return instance

    @classmethod
    def from_list(cls, urls: list[str | IndexEntry]) -> "SitemapIndex":
        """Builds basic sitemap index from list of URLs, with no additonal attributes"""
        instance = cls()

        if not isinstance(urls, list):
            raise TypeError(f"URLs must be in list. Recieved: {type(urls).__name__}")

        for url in urls:
            if isinstance(url, str):
                entry = IndexEntry(loc=url)
                instance.index_entries.append(entry)
            elif isinstance(url, IndexEntry):
                instance.index_entries.append(url)

        return instance

    def add_sitemap(self, url: str | IndexEntry, **kwargs) -> "SitemapIndex":
        """Add sitemap URL entry to index"""
        if isinstance(url, IndexEntry):
            self.index_entries.append(url)
        else:
            self.index_entries.append(IndexEntry(loc=url, **kwargs))

        return self

    def remove_sitemap(self, url: str) -> "SitemapIndex":
        """Remove sitemap from sitemap index by URL"""
        self.index_entries = [u for u in self.index_entries if u.loc != url]

        return self

    def write_to_file(self, output_filename: str = None) -> "SitemapIndex":
        """Write a sitemap index XML file from current instance.

        Args:
            output_filename (str) [Optional]: The desired name of the XML file. Default = "sitemap-index.xml

        Returns:
            sitemap: an instance of SitemapIndex
        """
        if not output_filename:
            output_filename = "sitemap-index.xml"

        root = ET.Element(
            "sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        )

        for sitemap in self.index_entries:
            self._append_sitemap_element(root=root, index_entry=sitemap)

        tree = ET.ElementTree(root)
        ET.indent(tree, space="   ")  # 3 spaces
        tree.write(output_filename, encoding="UTF-8", xml_declaration=True)

        return self

    def _append_sitemap_element(self, root: ET.Element, index_entry: IndexEntry):
        """Append Sitemap element to given root element"""
        sitemap_element = ET.SubElement(root, "sitemap")
        loc = ET.SubElement(sitemap_element, "loc")

        loc.text = index_entry.loc

        if index_entry.lastmod is not None:
            lastmod = ET.SubElement(sitemap_element, "lastmod")
            lastmod.text = index_entry.lastmod

    def __len__(self):
        return len(self.index_entries)

    def __iter__(self):
        return iter(self.index_entries)
