# superscraper

Command line interface environment for scraping anything from the web. SuperScraper combines [Scrapy](https://docs.scrapy.org/en/latest/), [Selenium](https://selenium-python.readthedocs.io/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) libraries together, to make web crawling as easy as executing a single command!

## Installation

### Prerequisites

Make sure you have installed all of the following prerequisites on your development machine:

- Python 3 - [Download & Install Python 3](https://docs.python-guide.org/starting/install3/linux/)
- Git - [Download & Install Git](https://git-scm.com/downloads)

### Step 1: Clone Github repository

`git clone https://github.com/Terminus07/superscraper.git`

### Step 2: Install Python requirements

Run `setup.sh` with the following command:
`bash setup.sh`

### Step 3 (Optional): Create an alias

An alias is an easy way to access `superscraper` from anywhere in your terminal. </br>
Creating an alias:

- Press <kbd>Ctrl</kbd> + <kbd>H</kbd> to view all hidden files in your home directory.
- Add the following line to the `.bashrc` file: </br>
  `alias {INSERT ALIAS NAME HERE}='(cd {INSERT HOME DIRECTORY HERE}/superscraper/scraper/scraper} && bash ./main.sh)'` </br>
- Save `.bashrc` and then reload settings: </br>
  `source ~/.bashrc`

### Step 4: Run main.sh

If you created an alias, simply type the alias name that was added in your `.bashrc` file. </br>
Otherwise, you can run `main.sh` directly: </br>

    cd superscraper/scraper/scraper
    bash main.sh

## Usage

### Create a spiders.json file

In order to scrape data from the web we need to create a `spiders.json` file, which is divided into spider objects. Each spider object contains a set of properties which can be modified depending on your use case. Run the `spider` command to create it.

### Modify your newly created spiders.json file

Edit your `spiders.json` file to your liking.

### Run spiders

Execute the crawl command. An `output.json` file will be created with extracted data.

## Commands

```
COMMANDS:
spider [-h] {base,selenium} - Create spiders.json file
crawl [-h] [spider.json] - Run spiders using a spiders.json file
history - View command history
settings - Shell settings
help - Shell manual
clear - Clears terminal
exit - Exit
```

#### base.json spider template

```
{
    "name": "base",
    "start_urls": [
        "https://quotes.toscrape.com/page/1/"
    ],
    "xpaths": [
        "//title/text()"
    ],
    "selectors": [
        "h2::text"
    ],
    "xpath_selectors": [],
    "form_data": {},
    "custom_settings": {
        "LOG_ENABLED": false
    },
    "links": [],
    "download_links": [],
    "download_link_xpaths": [],
    "output_xpaths": [],
    "output_selectors": [],
    "request": {},
    "response": {},
    "response_urls": [],
    "response_url_xpaths": []
}
```

#### selenium.json template

```
  {
        "name": "selenium",
        "start_urls": [
            "https://quotes.toscrape.com/page/1/"
        ],
        "driver_settings": {
            "driver_type": "Chrome",
            "options": {
                "experimental_options": [
                    {
                        "name": "detach",
                        "value": true
                    }
                ],
                "arguments": []
            },
            "capabilities": {
                "platform": "WINDOWS",
                "version": "10"
            }
        },
        "events": [
            {
                "function": "find_element",
                "args": {
                    "by": "name",
                    "value": "_user"
                },
                "output": "username"
            },
            {
                "target": "username",
                "function": "send_keys",
                "args": "username"
            },
            {
                "object_type": "Select",
                "object_input": "select",
                "args": {},
                "output": "select_target"
            },
            {
                "target": "select_target",
                "function": "select_by_index",
                "args": "1"
            },
            {
                "target": "password",
                "function": "send_keys",
                "args": "\ue007"
            }
        ],
        "custom_settings": {
            "LOG_ENABLED": false
        }
    }


```

#### spiders.json template

```
[
    {
    "name": "base",
    "start_urls": [
        "https://quotes.toscrape.com/page/1/"
    ],
    "xpaths": [
        "//title/text()"
    ],
    "selectors": [
        "h2::text"
    ],
    "xpath_selectors": [],
    "form_data": {},
    "custom_settings": {
        "LOG_ENABLED": false
    },
    "links": [],
    "download_links": [],
    "download_link_xpaths": [],
    "output_xpaths": [],
    "output_selectors": [],
    "request": {},
    "response": {},
    "response_urls": [],
    "response_url_xpaths": []
},
{
    "name": "base",
    "start_urls": [
        "https://quotes.toscrape.com/page/1/"
    ],
    "xpaths": [
        "//title/text()"
    ],
    "selectors": [
        "h2::text"
    ],
    "xpath_selectors": [],
    "form_data": {},
    "custom_settings": {
        "LOG_ENABLED": false
    },
    "links": [],
    "download_links": [],
    "download_link_xpaths": [],
    "output_xpaths": [],
    "output_selectors": [],
    "request": {},
    "response": {},
    "response_urls": [],
    "response_url_xpaths": []
},
{
        "name": "selenium",
        "start_urls": [
            "https://quotes.toscrape.com/page/1/"
        ],
        "driver_settings": {
            "driver_type": "Chrome",
            "options": {
                "experimental_options": [
                    {
                        "name": "detach",
                        "value": true
                    }
                ],
                "arguments": []
            },
            "capabilities": {
                "platform": "WINDOWS",
                "version": "10"
            }
        },
        "events": [
            {
                "function": "find_element",
                "args": {
                    "by": "name",
                    "value": "_user"
                },
                "output": "username"
            },
            {
                "target": "username",
                "function": "send_keys",
                "args": "username"
            },
            {
                "object_type": "Select",
                "object_input": "select",
                "args": {},
                "output": "select_target"
            },
            {
                "target": "select_target",
                "function": "select_by_index",
                "args": "1"
            },
            {
                "target": "password",
                "function": "send_keys",
                "args": "\ue007"
            }
        ],
        "custom_settings": {
            "LOG_ENABLED": false
        }
    }
]

```
