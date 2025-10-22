from pytest import fixture

from sitemapy import URLEntry, HreflangAlternate


@fixture
def german_url():
    return "https://www.example.de/"


@fixture
def spanish_url():
    return "https://www.example.es/"


def test_add_alternate(german_url, spanish_url):
    url = URLEntry(loc="https://www.example.com/")
    url.add_alternate(href=german_url, hreflang="de-de")

    assert len(url.hreflang_alts) == 1

    alt = HreflangAlternate(hreflang="es-es", href=spanish_url)
    url.add_alternate(alt)

    assert len(url.hreflang_alts) == 2


def test_add_alternates(german_url, spanish_url):
    url = URLEntry(loc="https://www.example.com/")

    url.add_alternates(
        [
            {"hreflang": "de-de", "href": german_url},
            {"hreflang": "es-es", "href": spanish_url},
        ]
    )

    assert len(url.hreflang_alts) == 2
