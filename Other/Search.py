import googlesearch


class LinkScraper:

    """
    LinkScraper class is used to gather the highest ranking websites
    for the arg:search based on googlesearch (google's search algorithm)
    """

    def __init__(self, search, n):
        # List of returned urls
        self.urls = []
        # for each url returned append to list of urls
        for url in googlesearch.search(search, stop=n):
            self.urls.append(url)