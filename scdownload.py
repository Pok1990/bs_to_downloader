#!/usr/bin/env python3

import argparse
import os
import logging
import urlcrawler
import wgetsubstitute


class ScDownload:
    def __init__(self, loglevel=logging.DEBUG):
        self.__urls = []
        self.__dirname = ""
        self.__nameandurls = {}
        self.__errorepisodes = []
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(loglevel)
        self.__logger.propagate = False
        shandler = logging.StreamHandler()
        shandler.setLevel(loglevel)
        formatter = logging.Formatter('%(levelname)s \t- %(name)s \t: %(message)s')
        shandler.setFormatter(formatter)
        self.__logger.addHandler(shandler)

    def downloadlist(self):
        """
        uses all urls-strings and downloaded them
        after this make a directory and copy all downloaded files in the new dir
        :return:
        """
        if not self.__dirname:
            self.__logger.warning("no dirname set")
            return
        try:
            os.mkdir(self.__dirname)
        except FileExistsError:
            self.__logger.info("directory already exists")
        home = os.getcwd()
        os.chdir(self.__dirname)

        for key in self.__nameandurls:
            self.__logger.debug("Downloading {}  Link: {}".format(key, self.__nameandurls[key]))
            downloadunit = wgetsubstitute.Wgetsubstitute(filename=key)
            done = downloadunit.fulldownload(self.__nameandurls[key])


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
                        fullname = "{}_S{}_E{}".format(self.__dirname, str(staffel), str(episode))
                        self.__nameandurls[fullname] = linkdict[str(staffel)][str(episode)]["Streamcloud"]
                        self.__logger.debug(staffel + "/" + episode + " :" + linkdict[str(staffel)][str(episode)]["Streamcloud"])
                    else:
                        self.__errorepisodes.append(staffel + "/" + episode)
                        self.__logger.warning(staffel + "/" + episode + " no Streamcloud-link found")

    def downloadafile(self, httpside):
        self.__dirname = "singlefile"
        self.__urls.append(httpside)
        self.downloadlist()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="Usage: -f <urlfile>  ",
                                     description="Download urls from a given series from bs.to")
    parser.add_argument('--download', dest="url", help="a single streamcloud-url that you want downloaded")
    parser.add_argument('--series', dest="seriesurl", help=" URL from bs.to ")
    parseCollect = parser.parse_args()
    url = parseCollect.url
    seriesurl = parseCollect.seriesurl

    unit = ScDownload()
    logging.basicConfig(level=logging.DEBUG)

    if url is not None:
        unit.downloadafile(url)

    if seriesurl is not None:
        spider = urlcrawler.ListCrawler()
        staffdict, seriesname = spider.readurl(seriesurl)
        unit.readfromlist(staffdict, seriesname)
        unit.downloadlist()

