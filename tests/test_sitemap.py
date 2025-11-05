from pathlib import Path
from unittest.mock import patch
import xml.etree.ElementTree as ET

from pytest import fixture

from sitemapy import Sitemap, URLEntry


@fixture
def url_text():
    return "https://www.example.com/"


@fixture
def url_entry():
    return URLEntry(loc="https://www.test.com/")


def test_add_url_list(url_text):
    sitemap = Sitemap.from_list([url_text])
    sitemap.add_url("https://www.example.org")
    assert len(sitemap) == 2


def test_add_url_entry(url_entry, url_text):
    sitemap = Sitemap.from_list([url_text])
    sitemap.add_url(url_entry)
    assert len(sitemap) == 2
    assert "test" in sitemap.urls[1].loc


def test_remove_url(url_text):
    sitemap = Sitemap.from_list([url_text])
    sitemap.remove_url(url_text)
    assert len(sitemap) == 0


def test_get_urls_by_pattern(url_text):
    sitemap = Sitemap.from_list([url_text, "nomatch.com"])
    assert len(sitemap) == 2
    filtered = sitemap.get_urls_by_pattern("exa")
    assert len(sitemap) == 2
    assert len(filtered) == 1
    assert "exa" in filtered[0].loc


def test_deduplicate(url_text):
    sitemap = Sitemap.from_list([url_text, url_text, url_text])
    assert len(sitemap) == 3
    sitemap.deduplicate()
    assert len(sitemap) == 1


def test_plain_urls_from_list(url_text):
    sitemap = Sitemap.from_list([url_text])
    assert type(sitemap) == Sitemap
    assert len(sitemap) == 1


def test_plain_urls_from_file():
    # From string
    sitemap = Sitemap.from_file("tests/test-sitemap.xml")
    assert type(sitemap) == Sitemap
    assert sitemap.urls[0].loc is not None
    assert sitemap.urls[0].lastmod is not None
    assert sitemap.urls[0].priority is not None
    assert sitemap.urls[0].changefreq is not None

    # From Path
    path = Path("tests/test-sitemap.xml")
    second_sitemap = Sitemap.from_file(path=path)
    assert type(second_sitemap) == Sitemap
    assert second_sitemap.urls[0].loc is not None
    assert second_sitemap.urls[0].lastmod is not None
    assert second_sitemap.urls[0].priority is not None
    assert second_sitemap.urls[0].changefreq is not None


def test_write_to_file_creates_file(tmp_path, url_entry):
    """Test that a file is created"""
    sitemap = Sitemap.from_list([url_entry])
    filename = tmp_path / "output.xml"
    sitemap.write_to_file(filename)

    assert filename.exists()


def test_write_to_file_default_filename(tmp_path, url_entry, monkeypatch):
    """Test that default filename 'sitemap.xml' is used when none provided"""
    sitemap = Sitemap.from_list([url_entry])
    monkeypatch.chdir(tmp_path)

    sitemap.write_to_file()

    assert (tmp_path / "sitemap.xml").exists()


def test_write_to_file_content_accuracy(tmp_path):
    """Test that written XML contains correct URL entries"""
    urls = ["https://example.com/", "https://example.com/about/"]
    sitemap = Sitemap.from_list(urls)

    # Append image
    image_url = "https://example.com/cat.png"
    first = sitemap.urls[0]
    first.add_image(image_url)

    output_file = tmp_path / "output.xml"

    sitemap.write_to_file(str(output_file))

    tree = ET.parse(output_file)
    root = tree.getroot()

    loc_elements = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    written_urls = [loc.text for loc in loc_elements]
    # PICKUP write actual test for images
    # I dont' currently grab url elements
    image_urls = []

    assert written_urls == urls


def test_write_to_file_with_metadata(tmp_path):
    """Test that URLEntry metadata (lastmod, priority, etc.) is written correctly"""
    sitemap = Sitemap()
    sitemap.add_url("https://example.com/", lastmod="2025-10-25", priority=0.9)
    output_file = tmp_path / "metadata.xml"

    sitemap.write_to_file(str(output_file))

    tree = ET.parse(output_file)
    root = tree.getroot()

    url_elem = root.find(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    lastmod = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")
    priority = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}priority")

    assert lastmod.text == "2025-10-25"
    assert priority.text == "0.9"


def test_write_to_file_namespaces(tmp_path, url_text):
    """Test that appropriate namespaces get written per element included in sitemap"""
    sitemap = Sitemap()
    url = URLEntry(loc=url_text)
    url.add_image(image="https://www.example.com/cat.png/")
    sitemap.add_url(url)
    output_file = tmp_path / "namespaces.xml"

    sitemap.write_to_file(str(output_file))

    with open(output_file, "r") as f:
        content = f.read()

    # Image namespace
    assert 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' in content
    assert "xmlns:image" in content
    assert "http://www.google.com/schemas/sitemap-image/1.1" in content
