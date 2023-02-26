# superscraper

`superscraper` allows you to extract data from the web in JSON format, using the Selenium and Scrapy libraries. You can either use it as a CLI tool, or as a Python library to generate data on the fly.

## Installation

### Pip (Linux, Windows)

```bash
pip install git+https://github.com/Terminus07/superscraper@main
```

### Manual installation

1. Clone the git repository:

```bash
git clone https://github.com/Terminus07/superscraper.git
```

2. Install all package dependencies:

```bash
pip install -r requirements.txt
```

3. Create an alias in your .bashrc:

```bash
chmod +x /path-to-release/superscraper/scraper/scraper/main.sh
alias superscraper="/path-to-release/superscraper/scraper/scraper/superscraper.sh"
```

## Usage

### CLI Commands

```bash
spider [-h] {scrapy,selenium} - Create spiders.json file
crawl [-h] [spiders.json] - Run spiders using a spiders.json file
history - View command history
settings - Shell settings
help - Shell manual
clear - Clears terminal
exit - Exit
```

### Create a spiders.json file

A `spiders.json` file is divided into `Spider` objects, which can be used to define what data you wish to extract from any given website.
To create it manually, run:

```bash
bash superscraper.sh
spider {scrapy,selenium} # type can be either 'scrapy', 'selenium' or a .json file of your choice
```

Which is the same as running:

```bash
python main.py spider {scrapy,selenium}
```

It can also be run within a Python script:

```python
TEST_DIRECTORY = 'test.json'
SuperScraper.spider({'type': ['scrapy', 'selenium', TESTDIRECTORY]})
```

`Spider` objects will be created and appended to the `spiders.json` file based on the `type` parameter. `type` represents a `scrapy.json` or a `selenium.json` file.
If a custom .json file is passed in, it must be structured appropriately.

#### scrapy.json example

```json
{
  "name": "base",
  "custom_settings": {
    "LOG_ENABLED": false,
    "COOKIES_ENABLED": true,
    "COOKIES_DEBUG": false,
    "IMAGES_STORE": "images"
  },
  "start_urls": ["https://en.wikipedia.org/wiki/Eiffel_Tower"],
  "meta": {},
  "xpaths": ["//title/text()"],
  "selectors": [],
  "form_data": {},
  "follow_urls": [],
  "wget_urls": [],
  "media_urls": [
    "//*[@id='mw-content-text']/div[1]/table[1]/tbody/tr[3]/td/a/img/@src"
  ],
  "url_rules": [
    {
      "target_var": "image_urls",
      "function": "split",
      "args": {
        "index": 0,
        "value": ""
      }
    }
  ],
  "image_urls": [],
  "video_urls": [],
  "m3u8_urls": [],
  "segment_urls": [],
  "image_store_urls": [],
  "extracted_items": {
    "titles": "//title/text()",
    "has": "//h1//text()",
    "red": "//h2//text()"
  },
  "extracted_xpaths": [],
  "extracted_selectors": [],
  "requests": [],
  "responses": [],
  "save_requests": false
}
```

#### selenium.json example

```json
{
  "name": "selenium",
  "start_urls": ["https://www.imdb.com/title/tt11126994/"],
  "custom_settings": {
    "LOG_ENABLED": false
  },
  "driver_settings": {
    "driver_type": "Chrome",
    "options": {
      "experimental_options": [
        {
          "name": "detach",
          "value": true
        }
      ],
      "arguments": [
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
      ]
    },
    "executable_path": "",
    "capabilities": {},
    "proxy": ""
  },
  "delay": 0,
  "events": [
    {
      "function": "find_element",
      "args": {
        "by": "xpath",
        "value": "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div/div[2]/div[2]/a[2]"
      },
      "output": "link"
    },
    {
      "target": "link",
      "function": "click",
      "args": {}
    },
    {
      "function": "find_element",
      "args": {
        "by": "xpath",
        "value": "//*[@id='imdbnext-vp-jw-single']/div[2]/div[4]/video"
      },
      "output": "video"
    },
    {
      "target": "video",
      "function": "click",
      "args": {}
    },
    {
      "target": "video",
      "function": "click",
      "args": {}
    },
    {
      "function": "quit",
      "args": {}
    }
  ],
  "requests": [],
  "responses": [],
  "request_params": {},
  "save_requests": true,
  "xpaths": ["//title/text()"],
  "selectors": [],
  "follow_urls": [],
  "wget_urls": [],
  "media_urls": ["//*[@id='imdbnext-vp-jw-single']/div[2]/div[4]/video/@src"],
  "image_urls": [],
  "video_urls": [],
  "m3u8_urls": [],
  "segment_urls": [],
  "item_fields": {},
  "extracted_items": {},
  "extracted_xpaths": [],
  "extracted_selectors": []
}
```

For more information about how to define spiders, see [Spider Definition](#spider-definition)

### Crawl with spiders.json

```python
SPIDERS_DIRECTORY = 'spiders.json'
SuperScraper.crawl({'json': SPIDERS_DIRECTORY}) # optional json parameter, if you want to pass spiders.json file
```

An `output.json` file will be created with the extracted data from all the spiders, as previously defined in `spiders.json`.

## Spider Definition

### Scrapy Spider
