#!/usr/bin/env python3

import re
import argparse
from urllib.request import urlopen
import logging
import htmlpars

class ListCrawler:
    def __init__(self, loglevel=logging.DEBUG):
        self.__staffelurls = []
        self.__sc_links = []
        self.__screfefence = []
        self.__errourls = []
        self.__seriesname = ""
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(loglevel)
        self.__logger.propagate = False
        shandler = logging.StreamHandler()
        shandler.setLevel(loglevel)
        formatter = logging.Formatter('%(levelname)s \t- %(name)s \t: %(message)s')
        shandler.setFormatter(formatter)
        self.__logger.addHandler(shandler)

    def getstaffelurl(self, url):
        """
            gives me all staffels
        :param url: first thin you need.
        :return:
        """
        urltext = self.getwebsite(url)
        staffeln = re.findall(r"serie/.*/\d\"", urltext)  # a " for takes ONLY the staffels...
        for item in staffeln:
            staffellinks = "http://bs.to/" + item[0:-1]
            self.__staffelurls.append(staffellinks)
        self.__logger.info("these staffels.links detected:")
        for item in self.__staffelurls:
            self.__logger.info(item)
        print()

    def getparts(self):
        """
            get all parts of a staffel
        :return:
        """

    def getscref(self, staffel_url):
        """
            get all sc-refs for a website from bs.to
        :param staffel_url:
        :return:
        """
        urltext = self.getwebsite(staffel_url)


        parser = htmlpars.HtmlParserHelper()
        parser.feed(urltext)

        """
        urltext = self.getwebsite(staffel_url)
        self.__logger.info("get all references from " + staffel_url)
        targets = re.findall(r"serie.*/Streamcloud-1", urltext)
        for item in targets:
            scref = "http://bs.to/" + item
            self.__screfefence.append(scref)
        """

    def getsc_link(self):
        if not self.__screfefence:
            return
        for url in self.__screfefence:
            pass
            htmlstring = self.getwebsite(url)
            match2 = re.search(r"http://streamcloud.*\" ", htmlstring)
            if not match2:
                self.__logger.warning("not Streamcloudmatch in " + url)
            else:
                self.__logger.info("found: " + match2.group())
                self.__sc_links.append(match2.group()[0:-2])

    @staticmethod
    def getwebsite(targethttpurl):
        """
            what happens with response if the webside is unavailable??
            errorhandling is needed
        :param targethttpurl: a http:// somewhat
        :return: the html-text
        """
        response = urlopen(targethttpurl)
        htmlbytes = response.read()
        htmlstring = htmlbytes.decode("utf-8")
        return htmlstring

    def readurl(self, url, spez=0):
        """
            if you want download a series, with 5 staffels and you have the first 3
            you can set spez to 4 and then the 4th and higher will be downloaded
        :param url: url to the series you want downloaded
        :param spez=0: number of staffel your download should begin.
        :return: the html-text
        """
        orders = url.split("/")
        self.__seriesname = orders[-1]
        self.getstaffelurl(url)
        for i in range(0, spez):
            self.__staffelurls.pop(0)
        self.__logger.info("these will be Downloaded:")
        self.__logger.info(self.__staffelurls)
        for surl in self.__staffelurls:
            self.getscref(surl)
        self.getsc_link()
        self.__logger.info("the seriesname is " + self.__seriesname)
        return self.__sc_links, self.__seriesname


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="Usage: -u <url>  ", description="targeturl")
    parser.add_argument('-u', dest='url', help="target url")
    parser.add_argument('-s', dest='staff', help="start with this staff")
    parseCollect = parser.parse_args()
    targeturl = parseCollect.url
    startshere = parseCollect.staff

    if startshere is None:
        startshere = 0

    unit = ListCrawler()
    unit.readurl(targeturl, int(startshere))
    # unit.getsc_link()

    """
    match = re.search(r"serie.*/Streamcloud(-1)?",htmlString)
    if match is not None:
        newurl = "http://bs.to/"+match.group()
        print(newurl)
        response2 = urlopen(newurl)
        urlbytes = response2.read()
        urlstring = urlbytes.decode("utf-8")
        print(urlstring)
        match2 = re.search(r"http://streamcloud.*html", urlstring)
        if match2 is not None:
            print(match2.group())
    else:
        print("kein Match")
    """
