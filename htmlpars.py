import html.parser
import logging
from html.entities import name2codepoint
import re

class HtmlParserHelper(html.parser.HTMLParser):

    def __init__(self, loglevel=logging.INFO):
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
            # deniy multiple prints if the class initiated multiple

        self.__currenttag_td = False
        self.__epfound = False
        self.__beginngathering = False
        self.__episodes = {}
        self.__currentepisode = 0

    def correctnumber(self,number):
        self.__logger.debug("number modifiiyng {}".format(number))
        if len(number) == 3:
            return number
        elif len(number) == 2:
            return "0" + number
        elif len(number) == 1:
            return "00" + number

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.__currenttag_td = True
            for attr in attrs:
                if attr[0] == "class":
                    self.__logger.debug("attr[0] == class  passed")
                    if attr[1] == "nowrap":
                        self.__logger.debug("begingathering is true")
                        self.__beginngathering = True

        if tag == "a" and self.__epfound is True:
            title = None
            self.__logger.debug("a and epfound passing ")
            for attr in attrs:
                if  attr[0] == "title" and self.__beginngathering is True:
                    self.__episodes[self.__currentepisode][attr[1]] = None
                    title = attr[1]
                if attr[0] == "href" and self.__beginngathering is True:
                    if title == "Streamcloud":
                        self.__logger.info("Streamcloudlink found: " + "http://bs.to/" + attr[1])
                    self.__episodes[self.__currentepisode][title] = "http://bs.to/" + attr[1]
                    title = None
        self.__logger.debug("Start tag:"+ tag)
        for attr in attrs:
            self.__logger.debug("     attr:"+ str(attr))


    def handle_endtag(self, tag):
        if tag == "td":
            self.__currenttag_td = False
        if tag == "tr":
            self.__epfound = False
            self.__currentepisode = None
            self.__beginngathering = False
        self.__logger.debug("End tag  :"+ tag)

    def handle_data(self, data):
        if self.__currenttag_td and self.__epfound is False:
            isnumber = re.match(r"\d+",data)
            if isnumber:
                self.__epfound = True
                self.__currentepisode = isnumber.group()
                self.__currentepisode = self.correctnumber(self.__currentepisode)
                # here from 1 digit to 3 dits... its important for formatter
                self.__logger.debug(self.__currentepisode)
                self.__logger.debug("found a episode: " + self.__currentepisode)
                self.__episodes[self.__currentepisode] = {}
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

    def get_episodes(self):
        self.__logger.debug(self.__episodes)
        return self.__episodes
