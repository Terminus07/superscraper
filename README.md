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

### Modify your Spider objects

Once your `spiders.json` file is created, you can directly modify it if you choose to do so, before starting the crawling process.

### Crawl with spiders.json

```python
SPIDERS_DIRECTORY = 'spiders.json'
SuperScraper.crawl({'json': SPIDERS_DIRECTORY}) # optional json parameter, if you want to pass spiders.json file
```

An `output.json` file will be created with the extracted data from all the spiders, as previously defined in `spiders.json`.

## CLI Commands

```
COMMANDS:
spider [-h] {scrapy,selenium} - Create spiders.json file
crawl [-h] [spiders.json] - Run spiders using a spiders.json file
history - View command history
settings - Shell settings
help - Shell manual
clear - Clears terminal
exit - Exit
```
