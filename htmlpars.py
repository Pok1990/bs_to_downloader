import html.parser
import logging
from html.entities import name2codepoint

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
        if len(self.__logger.handlers) <= 0:
            self.__logger.addHandler(shandler)

    def getepisodes(self, htmltext):

        pass

    def handle_starttag(self, tag, attrs):
        self.__logger.debug("Start tag:"+ tag)
        for attr in attrs:
            self.__logger.debug("     attr:"+ str(attr))
    def handle_endtag(self, tag):
        self.__logger.debug("End tag  :"+ tag)
    def handle_data(self, data):
        self.__logger.debug("Data     :"+ data)
    def handle_comment(self, data):
        self.__logger.debug("Comment  :"+ data)
    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        self.__logger.debug("Named ent:"+ c)
    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        self.__logger.debug("Num ent  :"+ c)
    def handle_decl(self, data):
        self.__logger.debug("Decl     :"+ data)
