**Sitemapy** is a Python package that generates SEO-friendly XML sitemaps.


## Basic Usage

To create a sitemap a basic sitemap:

```python
from sitemapy import Sitemap

mapper = Sitemap()

mapper.write_sitemap_to_file(
    input_urls=[
        "https://example.com/",
        "https://example.org/",
    ],
    output_filename="custom-sitemap.xml"
)
```
