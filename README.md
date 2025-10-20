**Sitemapy** is a Python package that generates SEO-friendly XML sitemaps.


## Basic Usage

To create a basic sitemap:

```python
from sitemapy import Sitemap

map = Sitemap.from_list(
    urls=[
       "https://example.com/",
        "https://example.com/about/", 
    ]
)

map.write_to_file(output_filename="custom-sitemap.xml")
```

Set all lastmod values to today's date with `lastmod_now`

```python
map.write_to_file(
    output_filename="today-sitemap.xml",
    lastmod_now=True,
)
