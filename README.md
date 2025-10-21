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

Set all lastmod values at once

```python
map.set_all_lastmod("2025-12-01")

map.set_all_lastmod_to_today().write_to_file("today-sitemap.xml")
```
Add a single URL either from a string or a URLEntry object

```python
from sitemapy import URLEntry

map.add_url(url="https://www.example.com/")

url = URLEntry(
    loc="https://www.example.com/,
    lastmod="2025-12-01",
)
map.add_url(url)
```
