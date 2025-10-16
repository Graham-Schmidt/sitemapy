**Sitemapy** is a Python package that generates SEO-friendly XML sitemaps.


## Basic Usage

To create a sitemap a basic sitemap:

```python
from sitemapy import Sitemap

sitemap = Sitemap()

sitemap.write_sitemap_to_file(
    input_urls=[
        "https://example.com/",
        "https://example.org/",
    ],
    output_filename="custom-sitemap.xml"
)
```

Set all lastmod values to today's date with `lastmod_now`

```python
sitemap.write_sitemap_to_file(
    input_urls=[
        "https://example.com/",
        "https://example.org/",
    ],
    output_filename="today-sitemap.xml",
    lastmod_now=True,
)
