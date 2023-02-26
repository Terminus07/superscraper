# superscraper

`superscraper` allows you to extract data from the web in JSON format. You can either use it as a CLI tool, or as a Python library to generate data on the fly.

## Installation

### Pip

```bash
pip install git+https://github.com/Terminus07/superscraper@main
```

## Usage

### Create a spiders.json file

A `spiders.json` file is divided into `Spider` objects, which can be used to define what data you wish to extract from any given website.
To create it manually, run:

```bash
bash main.sh
spider {base,selenium} # type can be either 'base', 'selenium' or a .json file of your choice
```

Which is the same as running:

```bash
python main.py spider {base,selenium}
```

It can also be run within a Python script:

```python
TEST_DIRECTORY = 'test.json'
SuperScraper.spider({'type': ['base', 'selenium', TESTDIRECTORY]})
```

You can either use the default JSON templates, or create custom ones.

### Crawl with `spiders.json`

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
