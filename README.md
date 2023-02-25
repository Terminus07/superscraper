# superscraper

`superscraper` allows you to extract data from the web in JSON format. You can either use it as a CLI tool, or as a library in your own scripts to generate data on the fly.

## Installation

### Pip (macOS, linux, unix, Windows)

`pip install git+https://github.com/Terminus07/superscraper@main`

## Usage

### CLI

### Create a spiders.json file

In order to scrape data from the web we need to create a `spiders.json` file, which is divided into spider objects. Each spider object contains a set of properties which can be modified depending on your use case. Run the `spider` command to create it.

### Modify your newly created spiders.json file

Edit your `spiders.json` file to your liking. You can read the [documentation](https://www.google.com), for more information about the template structure.

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
