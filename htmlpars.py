import html.parser
import logging

class HtmlParserHelper(html.parser.HTMLParser):

    def __init__(self, loglevel=logging.DEBUG):
        html.parser.HTMLParser.__init__(self)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(loglevel)
        self.__logger.propagate = False
        shandler = logging.StreamHandler()
        shandler.setLevel(loglevel)
        formatter = logging.Formatter('%(levelname)s \t- %(name)s \t: %(message)s')
        shandler.setFormatter(formatter)
        self.__logger.addHandler(shandler)

        self.__currenttag = ""

    def getepisodes(self, htmltext):

        pass

    def handle_starttag(self, tag, attrs):
        if self.__currenttag:
            self.__logger.debug(tag)

        if tag == "tr":
            self.__currenttag = tag
            self.__logger.debug("found one raw")

    def handle_endtag(self, tag):
        if tag == "tr":
            self.__currenttag = ""
            self.__logger.debug("leave raw")

    def handle_data(self, data):
        self.__logger.debug(data)
        if self.__currenttag:
            pass
             # self.__logger.debug(data)
