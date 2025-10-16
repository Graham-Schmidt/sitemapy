**Sitemapy** is a Python package that generates SEO-friendly XML sitemaps.


## Basic Usage

To create a sitemap a basic sitemap:

```python
from sitemapy import Sitemap

sitemap = Sitemap()

sitemap.load_from_list(
    urls=[
       "https://example.com/",
        "https://example.org/", 
    ]
)

sitemap.write_sitemap_to_file(
    output_filename="custom-sitemap.xml"
)
```

Set all lastmod values to today's date with `lastmod_now`

```python
sitemap.write_sitemap_to_file(
    output_filename="today-sitemap.xml",
    lastmod_now=True,
)
