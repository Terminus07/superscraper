# superscraper

Superscraper is a web scraping tool that allows you to extract data from the web in a programmer friendly format. It combines [Scrapy](https://docs.scrapy.org/en/latest/), [Selenium](https://selenium-python.readthedocs.io/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) libraries together, to make web crawling as easy as executing a single command!

## Installation

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

It can either be used as a CLI tool to execute commands manually, or as a module that can be imported in your personal projects.

### Create a spiders.json file

In order to scrape data from the web we need to create a `spiders.json` file, which is divided into spider objects. Each spider object contains a set of properties which can be modified depending on your use case. Run the `spider` command to create it.

### Modify your newly created spiders.json file

Edit your `spiders.json` file to your liking. You can read the documentation, for more information about the template structure.

### Run spiders

Execute the crawl command. An `output.json` file will be created with the extracted data.

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
