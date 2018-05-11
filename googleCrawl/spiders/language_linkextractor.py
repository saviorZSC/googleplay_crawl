from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class LanguageLinkExtractor(LxmlLinkExtractor):
    # def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(),
    #              canonicalize=True,
    #              unique=True, process_value=None, deny_extensions=None, restrict_css=()):
    #     super(LxmlLinkExtractor, self).__init__(allow=allow, deny=deny,
    #         allow_domains=allow_domains, deny_domains=deny_domains,
    #         restrict_xpaths=restrict_xpaths, canonicalize=canonicalize,
    #         deny_extensions=deny_extensions, restrict_css=restrict_css)
    @staticmethod
    def addParams(url):
        if url.find('?') >= 0:
            return url+'&hl=en'
        else:
            return url +'?hl=en'

    def extract_links(self, response):
        links = LxmlLinkExtractor.extract_links(self, response)
        for x in links:
            x.url = LanguageLinkExtractor.addParams(x.url)
        # links = super(LxmlLinkExtractor, self).extract_links(response);
        return links
