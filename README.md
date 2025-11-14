# Sitemapy
[![PyPI - Version](https://img.shields.io/pypi/v/sitemapy)](https://pypi.org/project/sitemapy/)
[![Python Support](https://img.shields.io/pypi/pyversions/sitemapy.svg)](https://pypi.org/project/sitemapy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sitemapy** is a Python package for generating SEO-friendly XML sitemaps.

## Features

- 🚀 Simple and intuitive API for sitemap generation
- 📝 Support for all standard sitemap attributes (priority, changefreq, lastmod)
- 🌍 Full hreflang support for multilingual sites
- 📦 Sitemap index support for large sites
- 🗜️ Built-in compression (gzip) support
- 🔒 Safe XML parsing with defusedxml
- ⚡ Method chaining for cleaner code
- 🔄 Load and modify existing sitemaps

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Adding URLs Incrementally](#adding-urls-incrementally)
  - [Setting Dates](#setting-dates)
  - [Using URLEntry Objects](#using-urlentry-objects-for-more-control)
  - [Working with Existing Sitemaps](#working-with-existing-sitemaps)
  - [Hreflang Support](#hreflang-support)
  - [Sitemap Index](#sitemap-index)
  - [Compression](#compression)
- [Sitemap Extensions](#sitemap-extensions)
    - [Images](#images)
    - [News](#news)
- [Real-World Examples](#real-world-examples)
- [API Reference](#api-reference)
- [Best Practices](#best-practices)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

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

## Usage Examples

### Adding URLs Incrementally

```python
from sitemapy import Sitemap

sitemap = Sitemap()
sitemap.add_url("https://example.com/", lastmod="2025-01-15")
sitemap.add_url("https://example.com/blog/", priority=0.8)
sitemap.write_to_file()
```

### Setting Dates

```python
from sitemapy import Sitemap

sitemap = Sitemap.from_list([
    "https://example.com/",
    "https://example.com/about/"
])

# Set all URLs to a specific date
sitemap.set_all_lastmod("2025-12-01")

# Or set all URLs to today's date
sitemap.set_all_lastmod_to_today().write_to_file("today-sitemap.xml")
```

### Using URLEntry Objects for More Control

```python
from sitemapy import Sitemap, URLEntry

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
from sitemapy import Sitemap

# Load, modify, and save
sitemap = Sitemap.from_file("existing-sitemap.xml")
sitemap.add_url("https://example.com/new-page/")
sitemap.deduplicate()
sitemap.write_to_file("updated-sitemap.xml")
```

### Hreflang Support

Sitemapy makes creating hreflang alternates for multilingual sites easy:

```python
from sitemapy import Sitemap, URLEntry, HreflangAlternate

# Create a URL with language alternates
url = URLEntry(loc="https://www.example.com/")

# Add alternates individually
url.add_alternate(href="https://www.example.de/", hreflang="de-de")

# Or using HreflangAlternate objects
href_alt = HreflangAlternate(href="https://www.example.es/", hreflang="es-es")
url.add_alternate(href_alt)

# Or add multiple alternates at once
url.add_alternates([
    {"href": "https://www.example.de/", "hreflang": "de-de"},
    {"href": "https://www.example.es/", "hreflang": "es-es"},
    {"href": "https://www.example.fr/", "hreflang": "fr-fr"},
])

# Add to sitemap
sitemap = Sitemap()
sitemap.add_url(url)
sitemap.write_to_file()
```

### Sitemap Index

For large sites with multiple sitemaps, use a sitemap index:

```python
from sitemapy import SitemapIndex

# Create an index of multiple sitemaps
index = SitemapIndex.from_list([
    "https://example.com/sitemap-posts.xml",
    "https://example.com/sitemap-pages.xml",
    "https://example.com/sitemap-products.xml",
])

# Add more sitemaps with metadata
index.add_sitemap(
    "https://example.com/sitemap-images.xml",
    lastmod="2025-10-27"
)

index.write_to_file("sitemap-index.xml")
```

### Compression

Generate compressed sitemaps for better performance and reduced bandwidth:

```python
from sitemapy import Sitemap

sitemap = Sitemap.from_list([
    "https://example.com/",
    "https://example.com/about/",
])

# Creates sitemap.xml.gz
sitemap.write_compressed("sitemap.xml.gz")

# Or let it use the default name
sitemap.write_compressed()  # Creates sitemap.xml.gz
```

## Sitemap Extensions
Google recognizes a [set of extensions](https://developers.google.com/search/docs/crawling-indexing/sitemaps/combine-sitemap-extensions) for sitemaps. Sitemapy can intake and create News and Image elements (Video coming soon...)

URLEntry can contain an arrays of ImageEntry. URLEntry can contain a single NewsEntry.

### Images

```python
from sitemapy import URLEntry, ImageEntry
url = URLEntry(loc="https://www.example.com/")

# Create image(s) with just a URL string
url.add_image(image="https://www.example.com/cat.png/")
url.add_image(image="https://www.example.com/dog.png/")

# Create image(s) from an ImageEntry
image_entry_one = ImageEntry(image="https://www.example.com/cat.png/")
image_entry_two = ImageEntry(image="https://www.example.com/dog.png/")
url.add_image(image_entry_one)
url.add_image(image_entry_two)
```

### News
News elements can only be added by building a NewsEntry object.

```python
from sitemapy import URLEntry, NewsEntry
url = URLEntry(loc="https://www.example.com/")

news_entry = NewsEntry(
        publication_name="The New York Times",
        publication_language="en",
        publication_date="2025-12-01",
        title="First Contact Made"
    )

url.add_news_entry(news_entry)
```

## Real-World Examples

### Generate Sitemap from Database

```python
from sitemapy import Sitemap, URLEntry
from datetime import datetime

sitemap = Sitemap()

# Example: Blog posts from database
for post in get_blog_posts():  # Your database query
    sitemap.add_url(
        URLEntry(
            loc=f"https://example.com/blog/{post.slug}/",
            lastmod=post.updated_at.strftime("%Y-%m-%d"),
            changefreq="monthly",
            priority=0.8
        )
    )

sitemap.deduplicate().write_to_file("blog-sitemap.xml")
```

### Generate from Multiple Sources

```python
from sitemapy import Sitemap, SitemapIndex

# Create separate sitemaps for different content types
posts_sitemap = Sitemap()
for post in get_posts():
    posts_sitemap.add_url(f"https://example.com/posts/{post.id}/")
posts_sitemap.write_compressed("sitemap-posts.xml.gz")

pages_sitemap = Sitemap()
for page in get_pages():
    pages_sitemap.add_url(f"https://example.com/{page.slug}/", priority=0.9)
pages_sitemap.write_compressed("sitemap-pages.xml.gz")

# Create an index
index = SitemapIndex.from_list([
    "https://example.com/sitemap-posts.xml.gz",
    "https://example.com/sitemap-pages.xml.gz",
])
index.write_to_file("sitemap-index.xml")
```

### Filter and Update URLs

```python
from sitemapy import Sitemap

# Load existing sitemap
sitemap = Sitemap.from_file("sitemap.xml")

# Find all blog URLs
blog_urls = sitemap.get_urls_by_pattern(r"/blog/")

# Update their lastmod date
for url in blog_urls:
    url.lastmod = "2025-10-27"
    url.changefreq = "weekly"

sitemap.write_to_file("updated-sitemap.xml")
```

### Create Multilingual Sitemap

```python
from sitemapy import Sitemap, URLEntry

sitemap = Sitemap()

# Add homepage with language alternates
homepage = URLEntry(loc="https://example.com/en/")
homepage.add_alternates([
    {"href": "https://example.com/en/", "hreflang": "en"},
    {"href": "https://example.com/de/", "hreflang": "de"},
    {"href": "https://example.com/es/", "hreflang": "es"},
    {"href": "https://example.com/fr/", "hreflang": "fr"},
])
sitemap.add_url(homepage)

# Add more pages...
for page in get_pages():
    url = URLEntry(loc=f"https://example.com/en/{page.slug}/")
    url.add_alternates([
        {"href": f"https://example.com/en/{page.slug}/", "hreflang": "en"},
        {"href": f"https://example.com/de/{page.slug}/", "hreflang": "de"},
        {"href": f"https://example.com/es/{page.slug}/", "hreflang": "es"},
        {"href": f"https://example.com/fr/{page.slug}/", "hreflang": "fr"},
    ])
    sitemap.add_url(url)

sitemap.write_to_file("multilingual-sitemap.xml")
```

## API Reference

### Sitemap

Main class for creating and managing sitemaps.

**Class Methods:**
- `from_list(urls)` - Create sitemap from list of URL strings or URLEntry objects
- `from_file(path)` - Load existing sitemap from XML file

**Instance Methods:**
- `add_url(url, **kwargs)` - Add single URL (string or URLEntry)
- `remove_url(url)` - Remove URL by location string
- `get_urls_by_pattern(pattern)` - Filter URLs by regex pattern
- `deduplicate()` - Remove duplicate URLs
- `set_all_lastmod(date)` - Set lastmod for all URLs to specified date
- `set_all_lastmod_to_today()` - Set lastmod for all URLs to today's date
- `write_to_file(filename)` - Save as uncompressed XML (default: "sitemap.xml")
- `write_compressed(filename)` - Save as compressed .xml.gz (default: "sitemap.xml.gz")

**Special Methods:**
- `__len__()` - Returns number of URLs in sitemap
- `__iter__()` - Allows iteration over URLEntry objects

### URLEntry

Represents a single URL in a sitemap with optional metadata.

**Constructor:**
```python
URLEntry(
    loc: str,                    # Required: URL location
    lastmod: str = None,         # Last modification date (YYYY-MM-DD)
    changefreq: str = None,      # Change frequency (always, hourly, daily, weekly, monthly, yearly, never)
    priority: float = None       # Priority 0.0-1.0
)
```

**Methods:**
- `add_alternate(href_alt=None, hreflang="", href="")` - Add single hreflang alternate
- `add_alternates(alternates)` - Add multiple hreflang alternates from list of dicts
- `add_image(image)` - Add single image element from string or ImageEntry object
- `add_news_entry(news_entry)` - Add single news element from NewsEntry object

### HreflangAlternate

Represents a language/region alternate for a URL.

**Constructor:**
```python
HreflangAlternate(
    hreflang: str,  # Language code (e.g., "en-us", "de-de")
    href: str       # Alternate URL
)
```

### SitemapIndex

Class for creating and managing sitemap index files.

**Class Methods:**
- `from_list(urls)` - Create index from list of sitemap URLs or IndexEntry objects
- `from_file(path)` - Load existing sitemap index from XML file

**Instance Methods:**
- `add_sitemap(url, **kwargs)` - Add sitemap URL (string or IndexEntry)
- `remove_sitemap(url)` - Remove sitemap by location string
- `write_to_file(filename)` - Save as XML (default: "sitemap-index.xml")

**Special Methods:**
- `__len__()` - Returns number of sitemaps in index
- `__iter__()` - Allows iteration over IndexEntry objects

### IndexEntry

Represents a single sitemap reference in a sitemap index.

**Constructor:**
```python
IndexEntry(
    loc: str,              # Required: Sitemap URL location
    lastmod: str = None    # Last modification date (YYYY-MM-DD)
)
```

## Best Practices

### Sitemap Limits
- **Maximum 50,000 URLs** per sitemap file
- **Maximum 50MB** uncompressed size per sitemap
- Use a sitemap index for sites with more than 50,000 URLs
- Consider splitting large sitemaps by content type or date

### URL Guidelines
- Use absolute URLs (include protocol and domain)
- URLs should be canonical (no duplicates or redirects)
- Update `lastmod` when content actually changes
- Use `priority` (0.0-1.0) to indicate relative importance within your site
  - Note: Priority is relative to other URLs on *your* site, not the entire web

### Change Frequency
Valid `changefreq` values:
- `always` - Changes with every access
- `hourly` - Changes every hour
- `daily` - Changes daily
- `weekly` - Changes weekly
- `monthly` - Changes monthly
- `yearly` - Changes yearly
- `never` - Archived URLs that never change

### Performance Tips
- Use compression (`write_compressed()`) for large sitemaps
- Generate sitemaps incrementally during off-peak hours
- Submit sitemap location to search engines via robots.txt:
  ```
  Sitemap: https://example.com/sitemap.xml
  ```

### Hreflang Best Practices
- Each language version should reference all other versions (including itself)
- Use correct language codes (ISO 639-1) and optional region codes (ISO 3166-1 Alpha 2)
- Ensure all alternate URLs are accessible and return 200 status codes
- Common format: `en-US`, `de-DE`, `es-ES`, `fr-FR`
- See Google's documentation [here](https://developers.google.com/search/docs/specialty/international/localized-versions#sitemap).

## Requirements

- Python 3.10+
- defusedxml 0.7.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Security

Sitemapy uses [defusedxml](https://pypi.org/project/defusedxml/) instead of Python's standard XML library when parsing external sitemap files. This protects against XML vulnerabilities like billion laughs attacks and XML external entity (XXE) attacks that could occur when loading untrusted sitemap files.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Graham-Schmidt/sitemapy.git
cd sitemapy

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **PyPI**: https://pypi.org/project/sitemapy/
- **Source Code**: https://github.com/Graham-Schmidt/sitemapy
- **Issue Tracker**: https://github.com/Graham-Schmidt/sitemapy/issues
- **Sitemap Protocol**: https://www.sitemaps.org/protocol.html

---

**Made with ❤️ by Graham Schmidt**
