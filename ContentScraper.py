import urllib.request
import bs4 as bs


class ContentScraper:

    """
    WebScraper class is used to parse the HTML of a url to extract data from
    certain tags
    """

    # TODO: Extract text from a pdf
    def __init__(self, url):
        # Adds a User-Agent Header to the url Request
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/'
                '537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        # Opens a url request for initialized urllib.request.Request (req)
        scraped_data = urllib.request.urlopen(req)
        # Raw Scraped Text
        article = scraped_data.read()
        # Parses with bs4 and xml
        parsed_article = bs.BeautifulSoup(article, 'lxml')
        # Find all paragraphs
        paragraphs = parsed_article.find_all('p')
        # Article text string to append parsed HTML
        self.article_text = ""
        # Append all paragraphs to article_text variable
        for p in paragraphs:
            # article_text+='\n' # For readability of raw data
            self.article_text += p.text
        # print(article_text, '\n\n') # For readability of raw data