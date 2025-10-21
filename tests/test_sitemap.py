from pytest import fixture
from sitemapy import Sitemap, URLEntry


@fixture
def url_text():
    return "https://www.example.com/"


@fixture
def url_entry():
    return URLEntry(loc="https://www.test.com/")


def test_add_url_string(url_text):
    sitemap = Sitemap.from_list([url_text])
    sitemap.add_url("https://www.example.org")
    assert len(sitemap) == 2


def test_add_url_entry(url_entry, url_text):
    sitemap = Sitemap.from_list([url_text])
    sitemap.add_url(url_entry)
    assert len(sitemap) == 2


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
