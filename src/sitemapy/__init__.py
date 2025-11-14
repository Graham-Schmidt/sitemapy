# src/__init__.py
from .sitemapy import (
    Sitemap,
    URLEntry,
    HreflangAlternate,
    SitemapIndex,
    IndexEntry,
    ImageEntry,
    NewsEntry,
    SITEMAP_NS,
    IMAGE_NS,
    NEWS_NS,
)

__all__ = [
    "Sitemap",
    "URLEntry",
    "HreflangAlternate",
    "SitemapIndex",
    "IndexEntry",
    "ImageEntry",
    "NewsEntry",
    "SITEMAP_NS",
    "IMAGE_NS",
    "NEWS_NS",
]
__version__ = "0.2.3"
