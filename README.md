# superscraper

Command line interface environment for scraping anything from the web. Super scraper combines [Scrapy](https://docs.scrapy.org/en/latest/), [Selenium](https://selenium-python.readthedocs.io/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) libraries to make web crawling more accessible.

## Usage

```
COMMANDS:
spider [-h] {base,selenium} - Create spiders.json file that can be used with the crawl command
crawl [-h] [spider.json ...] - Run spiders.json file to extract or automate tasks on the web
history - View command history
settings - Shell settings
help - Shell manual
clear - Clears terminal
exit - Exit
```

## Prerequisites

Make sure you have installed all of the following prerequisites on your development machine:

- Python 3 - [Download & Install Python 3](https://docs.python-guide.org/starting/install3/linux/)
- Git - [Download & Install Git](https://git-scm.com/downloads)

## Installation

#### Step 1: Clone Github repository

`git clone https://github.com/Terminus07/superscraper.git`

#### Step 2: Install Python requirements

Run `setup.sh` with the following command:
`bash setup.sh`

#### Step 3 (Optional): Create an alias

An alias is an easy way to access `superscraper` from anywhere in your terminal. You can read more about aliases [here](https://www.tecmint.com/create-alias-in-linux/). </br>
Creating an alias:

- Press <kbd>Ctrl</kbd> + <kbd>H</kbd> to view all hidden files in your home directory.
- Add the following line to the `.bashrc` file: </br>
  `alias {INSERT ALIAS NAME HERE}='(cd {INSERT HOME DIRECTORY HERE}/superscraper/scraper/scraper} && bash ./main.sh)'` </br>
- Save `.bashrc` and then reload settings: </br>
  `source ~/.bashrc`

#### Step 4: Run main.sh

If you created an alias, simply type the alias name that was added in your `.bashrc` file. </br>
Otherwise, you can run `main.sh` directly: </br>

    cd superscraper/scraper/scraper
    bash main.sh

#### Step 5: Change default download/JSON directory

Type the command `settings` to modify your default download and JSON directories.
