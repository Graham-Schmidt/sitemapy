import xml.etree.ElementTree as ET

from pytest import fixture

from sitemapy import SitemapIndex, IndexEntry


@fixture
def sitemap_text():
    return "https://www.example.com/sitemap-index.xml"


@fixture
def index_entry():
    return IndexEntry(loc="https://www.example.com/second-index.xml")


def test_add_sitemap_string(sitemap_text):
    index = SitemapIndex.from_list([sitemap_text])
    assert len(index) == 1
    index.add_sitemap(sitemap_text)
    assert len(index) == 2


def test_add_sitemap_entry(sitemap_text, index_entry):
    index = SitemapIndex.from_list([sitemap_text])
    assert len(index) == 1
    index.add_sitemap(index_entry)
    assert len(index) == 2


def test_remove_sitemap(index_entry):
    index = SitemapIndex.from_list([index_entry])
    url = index_entry.loc
    index.remove_sitemap(url)

    assert len(index) == 0


def test_write_to_file_creates_file(tmp_path, index_entry):
    """Test that a file is created"""
    index = SitemapIndex.from_list([index_entry])
    filename = tmp_path / "output.xml"
    index.write_to_file(str(filename))

    assert filename.exists()


def test_write_to_file_default_filename(tmp_path, index_entry, monkeypatch):
    """Test that default filename 'sitemap-index.xml' is uesd when none provided"""
    index = SitemapIndex.from_list([index_entry])
    monkeypatch.chdir(tmp_path)

    index.write_to_file()

    assert (tmp_path / "sitemap-index.xml").exists()


def test_write_to_file_content_accuracy(tmp_path):
    """Test that written XML contains correct index entries"""
    urls = ["https://example.com/sitemap.xml", "http://example.com/posts-sitemap.xml"]
    index = SitemapIndex.from_list(urls)
    output_file = tmp_path / "output.xml"

    index.write_to_file(str(output_file))

    tree = ET.parse(output_file)
    root = tree.getroot()

    loc_elements = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    written_urls = [loc.text for loc in loc_elements]

    assert written_urls == urls


def test_write_to_file_with_metadata(tmp_path):
    """Test that IndexEntry metadata (lastmod) is written correctly"""
    index = SitemapIndex()
    index.add_sitemap("https://example.com/sitemap.xml", lastmod="2025-12-01")
    output_file = tmp_path / "output.xml"

    index.write_to_file(str(output_file))

    tree = ET.parse(output_file)
    root = tree.getroot()

    index_element = root.find(".//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap")
    lastmod = index_element.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")

    assert lastmod.text == "2025-12-01"
