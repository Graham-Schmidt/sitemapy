from pytest import fixture

from sitemapy import URLEntry, HreflangAlternate, ImageEntry, NewsEntry


@fixture
def example_url():
    return "https://www.example.com/"


@fixture
def german_url():
    return "https://www.example.de/"


@fixture
def spanish_url():
    return "https://www.example.es/"


@fixture
def image_url():
    return "https://www.example.com/cat.png"


@fixture
def news_entry():
    entry = NewsEntry(
        publication_name="The New York Times",
        publication_language="en",
        publication_date="2025-12-01",
        title="First Contact Made",
    )
    return entry


def test_add_alternate(example_url, german_url, spanish_url):
    """Test adding single Hreflang alternates via kwargs and HreflangAlternate object"""
    url = URLEntry(loc=example_url)
    url.add_alternate(href=german_url, hreflang="de-de")

    assert len(url.hreflang_alts) == 1

    alt = HreflangAlternate(hreflang="es-es", href=spanish_url)
    url.add_alternate(alt)

    assert len(url.hreflang_alts) == 2


def test_add_alternates(example_url, german_url, spanish_url):
    """Test adding multiple Hreflang alternates to URLEntry via dictionary"""
    url = URLEntry(loc=example_url)

    url.add_alternates(
        [
            {"hreflang": "de-de", "href": german_url},
            {"hreflang": "es-es", "href": spanish_url},
        ]
    )

    assert len(url.hreflang_alts) == 2


def test_add_image(example_url):
    """Test adding ImageEntry to Sitemap"""
    url = URLEntry(loc=example_url)
    assert len(url.images) == 0

    res = url.add_image(image="https://www.example.com/test-one.png")
    assert len(url.images) == 1
    assert "one" in url.images[0].loc
    assert type(res) == URLEntry

    image = ImageEntry(loc="https://www.example.com/test-two.png")
    url.add_image(image=image)
    assert len(url.images) == 2
    assert "two" in url.images[1].loc
    assert type(res) == URLEntry


def test_add_news(news_entry, example_url):
    """Test adding NewsEntry to Sitemap"""
    url = URLEntry(loc=example_url)
    assert not url.news_entry

    res = url.add_news_entry(news_entry=news_entry)
    assert url.news_entry
    assert type(res) == URLEntry
