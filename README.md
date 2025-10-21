# Sitemapy

Python package for generating SEO-friendly XML sitemaps.

## Installation
```bash
pip install sitemapy
```

## Quick Start
```python
from sitemapy import Sitemap

sitemap = Sitemap.from_list([
    "https://example.com/",
    "https://example.com/about/", 
])
sitemap.write_to_file("sitemap.xml")
```

**Output (`sitemap.xml`):**
```xml
<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://example.com/</loc>
   </url>
   <url>
      <loc>https://example.com/about/</loc>
   </url>
</urlset>
```


## Common Usage

### Adding URLs Incrementally
```python

sitemap = Sitemap()
sitemap.add_url("https://example.com/", lastmod="2025-01-15")
sitemap.add_url("https://example.com/blog/", priority=0.8)
sitemap.write_to_file()
```

### Setting All Dates to Today
```python
map.set_all_lastmod("2025-12-01")

map.set_all_lastmod_to_today().write_to_file("today-sitemap.xml")
```


### Using URLEntry Objects for More Control
```python
from sitemapy import URLEntry

url = URLEntry(
    loc="https://example.com/important-page/",
    lastmod="2025-10-21",
    changefreq="weekly",
    priority=0.9
)
sitemap = Sitemap()
sitemap.add_url(url)
sitemap.write_to_file()
```

### Working with Existing Sitemaps
```python
# Load, modify, and save
sitemap = Sitemap.from_file("existing-sitemap.xml")
sitemap.add_url("https://example.com/new-page/")
sitemap.deduplicate()
sitemap.write_to_file("updated-sitemap.xml")
```