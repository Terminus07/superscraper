DIRECTORY = "json_templates/secret"
BASE_DIRECTORY = DIRECTORY + "/base.json"
OUTPUT_DIRECTORY = DIRECTORY + "/output.json"
SELENIUM_DIRECTORY = DIRECTORY + "/selenium.json"
SPIDERS_DIRECTORY = DIRECTORY + "/spiders.json"

# selenium tests
AMAZON_DIRECTORY = DIRECTORY + '/selenium/amazon.json'
GOOGLE_DIRECTORY = DIRECTORY + '/selenium/google.json'
TEST_DIRECTORY = DIRECTORY + '/selenium/test.json'
FRED_DIRECTORY = DIRECTORY + '/selenium/fred.json'
MAIL_DIRECTORY = DIRECTORY + '/selenium/webmail.json'


# base tests
TEST_DIRECTORY2 = DIRECTORY + '/base/test.json'
QUOTES_DIRECTORY = DIRECTORY + '/base/quotes.json'

# "quotes": "//div[contains(@class, 'quote')]/span[contains(@class, 'text')]/text()",
# "authors": "//div[contains(@class, 'quote')]/span/small/text()",
# "tags": "//div[contains(@class, 'quote')]/div[contains(@class, 'tags')]/a/text()"
