#!/usr/bin/env python3

import argparse
import os
import logging
import urlcrawler


class ScDownload:
    def __init__(self, loglevel=logging.DEBUG):
        self.__urls = []
        self.__dirname = ""
        self.__errorepisodes = []
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(loglevel)
        self.__logger.propagate = False
        shandler = logging.StreamHandler()
        shandler.setLevel(loglevel)
        formatter = logging.Formatter('%(levelname)s \t- %(name)s \t: %(message)s')
        shandler.setFormatter(formatter)
        self.__logger.addHandler(shandler)

    def readfromfile(self, filewithurls):
        """
        takes urls from a file and appended to the list
        :param filewithurls:
        :return:
        """
        dirname = filewithurls.split(".")
        self.__dirname = dirname[0]
        file = open(filewithurls, "r")
        for line in file:
            self.__urls.append(line)
        file.close()

    def downloadlist(self):
        """
        uses all urls-strings and downloaded them
        after this make a directory and copy all downloaded files in the new dir
        :return:
        """
        if not self.__urls:
            self.__logger.warning("empty list for Download")
            return
        if not self.__dirname:
            self.__logger.warning("no dirname set")
            return
        try:
            os.mkdir(self.__dirname)
        except FileExistsError:
            self.__logger.info("directory already exists")
        os.system("cp Streaming-dl/streaming-dl.sh " + self.__dirname)
        home = os.getcwd()
        os.chdir(self.__dirname)
        for item in self.__urls:
            self.__logger.debug("Downloading " + item)
            value = os.system("./streaming-dl.sh " + item)
            if value is not 0:
                self.__logger.warning("downloading breaks")
                exit(0)
        os.remove("streaming-dl.sh")
        os.chdir(home)
        ok = os.system("mv " + self.__dirname + " ~/Videos/")
        if ok is 0:
            self.__logger.info("copy from directory in ~/Videos/ are ok.")
        else:
            self.__logger.debug("this is failed: " + "cp " + self.__dirname + " ~/Videos/")

    def readfromlist(self, linkdict, dirname):
        if not linkdict:
            return
        self.__logger.info("set dirname : " + dirname)
        self.__dirname = dirname
        self.__logger.info("reading urls from a given list")

        for staffel in linkdict:
                for episode in linkdict[staffel]:
                    if "Streamcloud" in linkdict[staffel][episode]:
                        self.__urls.append(linkdict[str(staffel)][str(episode)]["Streamcloud"])
                        self.__logger.debug(staffel + "/" + episode + " :" + linkdict[str(staffel)][str(episode)]["Streamcloud"])
                    else:
                        self.__errorepisodes.append(staffel + "/" + episode)
                        self.__logger.warning(staffel + "/" + episode + " no Streamcloud-link found")

    def downloadafile(self, httpside):
        self.__urls.append(httpside)
        self.downloadlist()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="Usage: -f <urlfile>  ",
                                     description="Download urls from a given series from bs.to")
    parser.add_argument('--urlfile', dest='urlfile', help="file with urls u want downloaded must be streamcloud-urls")
    parser.add_argument('--download', dest="url", help="a single streamcloud-url that you want downloaded")
    parser.add_argument('--series', dest="seriesurl", help=" URL from bs.to ")
    parseCollect = parser.parse_args()
    urlfile = parseCollect.urlfile
    url = parseCollect.url
    seriesurl = parseCollect.seriesurl

    unit = ScDownload()
    logging.basicConfig(level=logging.DEBUG)

    if seriesurl is not None:
        spider = urlcrawler.ListCrawler()
        staffdict, seriesname = spider.readurl(seriesurl)
        unit.readfromlist(staffdict, seriesname)
        unit.downloadlist()

