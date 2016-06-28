#!/usr/bin/env python3

import re
import argparse
from urllib.request import urlopen
import logging
import htmlpars

class ListCrawler:
    def __init__(self, loglevel=logging.DEBUG):
        self.__staffeln = {}
        self.__seriesname = ""
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


    def correctnumber(self,number):
        self.__logger.debug("number modifiiyng {}".format(number))
        if len(number) == 3:
            return number
        elif len(number) == 2:
            return "0" + number
        elif len(number) == 1:
            return "00" + number


    def getstaffelurl(self, url):
        """
            gives me all staffels
        :param url: first thin you need.
        :return:
        """
        urltext = self.getwebsite(url)
        staffeln = re.findall(r"serie/.*/\d\"", urltext)  # a " for takes ONLY the staffels...
        for item in staffeln:
            staffel = self.correctnumber(item[-2])
            self.__staffeln[staffel] = "http://bs.to/" + item[0:-1]
        for staffel in self.__staffeln:
            self.__logger.debug(staffel + " " + self.__staffeln[staffel])

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
        staffel = parser.get_episodes()
        return staffel

    def getsc_link(self, url):
        htmlstring = self.getwebsite(url)
        match2 = re.search(r"http://streamcloud.*\" ", htmlstring)
        if match2:
            self.__logger.info("found: " + match2.group())
            return match2.group()[0:-2]
        else:
            self.__logger.warning("not Streamcloudmatch in " + url)
            return None

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

    def readurl(self, url):
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
        if self.__staffeln:
            self.__logger.info("these will be Downloaded:")
            for staffel in self.__staffeln:
                self.__logger.info(staffel + " " + self.__staffeln[staffel])
                episodes = self.getscref(self.__staffeln[staffel])
                self.__logger.debug("episodes for " + staffel + " Downloaded")
                self.__staffeln[staffel] = episodes

        for staffel in self.__staffeln:
            for episode in self.__staffeln[staffel]:
                if "Streamcloud" in self.__staffeln[staffel][episode]:
                    self.__staffeln[staffel][episode]["Streamcloud"] = self.getsc_link(self.__staffeln[staffel][episode]["Streamcloud"])
                    self.__logger.debug(staffel + "/" + episode + " :" + self.__staffeln[staffel][episode]["Streamcloud"])
                else:
                    self.__logger.debug(staffel + "/" + episode + " no Streamcloud-link found")
        self.__logger.info("the seriesname is " + self.__seriesname)
        return self.__staffeln, self.__seriesname


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="Usage: -u <url>  ", description="targeturl")
    parser.add_argument('-u', dest='url', help="target url")
    parseCollect = parser.parse_args()
    targeturl = parseCollect.url

    unit = ListCrawler()
    unit.readurl(targeturl)
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
