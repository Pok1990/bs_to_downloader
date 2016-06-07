#!/usr/bin/env python3

import time
import re
import argparse
import logging
from urllib.request import urlopen
import os

class wgetsubstitute:
    def __init__(self, loglevel=logging.INFO, filename=""):
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(loglevel)
        self.__logger.propagate = False
        shandler = logging.StreamHandler()
        shandler.setLevel(loglevel)
        formatter = logging.Formatter('%(levelname)s \t- %(name)s \t: %(message)s')
        shandler.setFormatter(formatter)
        self.__logger.addHandler(shandler)

        self.__op = ""
        self.__usrlogin = ""
        self.__id = ""
        self.__fname = ""
        self.__referer = ""
        self.__hash = ""

        if filename is None:
            self.__episodename = ""
        else:
            self.__episodename = filename

    def getwebsite(self, url, post=False):
        if not post:
            self.__logger.debug("open GET request for website")
            response = urlopen(url)
            htmlbytes = response.read()
            htmlstring = htmlbytes.decode("utf-8")
            return htmlstring
        else:
            self.__logger.debug("open POST reuest with data for website")
            data = self.buildstring(url)
            data = data.encode()
            response = urlopen(url, data)
            htmlbytes = response.read()
            htmlstring = htmlbytes.decode("utf-8")
            return htmlstring

    def getdata(self,website):
        re_op = re.compile(r"<input type=\"hidden\" name=\"op\" value=\"(?P<value>.*?)\">")
        re_usrlogin = re.compile(r"<input type=\"hidden\" name=\"usr_login\" value=\"(?P<value>.*)\">")
        re_id = re.compile(r"<input type=\"hidden\" name=\"id\" value=\"(?P<value>.*)\">")
        re_fname = re.compile(r"<input type=\"hidden\" name=\"fname\" value=\"(?P<value>.*)\">")
        re_referer = re.compile(r"<input type=\"hidden\" name=\"referer\" value=\"(?P<value>.*)\">")
        re_hash = re.compile(r"<input type=\"hidden\" name=\"hash\" value=\"(?P<value>.*)\">")

        op = re_op.search(website, re.MULTILINE)
        if op is not None:
            self.__op = op.group("value")
            self.__logger.info("op was set:" + self.__op)

        usr_login = re_usrlogin.search(website, re.MULTILINE)
        if usr_login is not None:
            self.__usrlogin = usr_login.group("value")
            self.__logger.info("usr_login was set:" + self.__usrlogin)

        id = re_id.search(website, re.MULTILINE)
        if id is not None:
            self.__id = id.group("value")
            self.__logger.info("id was set:" + self.__id)

        fname = re_fname.search(website, re.MULTILINE)
        if fname is not None:
            self.__fname = fname.group("value")
            self.__logger.info("fname was set:" + self.__fname)

        referer = re_referer.search(website, re.MULTILINE)
        if referer is not None:
            self.__referer = referer.group("value")
            self.__logger.info("referer was set:" + self.__referer)

        hashdata = re_hash.search(website, re.MULTILINE)
        if hashdata is not None:
            self.__hash = hashdata.group("value")
            self.__logger.info("hash was set:" + self.__hash)

    def buildstring(self, website):
        result = "op={}&usr_login={}&id={}&fname={}&referer={}&url={}&method_free={}".format(self.__op, self.__usrlogin, self.__id, self.__fname, self.__referer, website,  self.__hash)
        self.__logger.debug(result)
        self.__logger.debug("datastring was build")
        return result

    def downloadvid(self, website):
        """
        Download the whole video with wget.
        search with a regex the file: "<stuff>" und get the stuff.
        then start wget and load the stuff.

        problem with fname and setting episodennamefuture stuff
        :param website:
        :return:
        """
        re_furl = re.compile(r"file: \"(?P<furl>.*)\"")
        furl = re_furl.search(website)
        if furl is not None:
            self.__logger.debug(furl.group())
            self.__logger.debug(furl.group("furl"))
            self.__logger.debug(" episodenname :" + self.__episodename)

            filename = self.__fname

            self.__logger.info("filename set to" + filename)
            os.system("echo \"\033[1;32mDescargando \033[0;34m " + self.__id + " \033[1;36m " + self.__fname + " : \033[1;0m\"")

            os.system("wget -c --output-document=" + filename + " " + furl.group("furl"))

        else:
            self.__logger.debug("nichts gefunden")
        pass

    def fulldownload(self, url):
        website = self.getwebsite(url)
        self.getdata(website)
        time.sleep(12)
        website = self.getwebsite(url, True)
        self.downloadvid(website)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="Usage: -u <url>  ", description="targeturl must be a streamcloud url")
    parser.add_argument('-u', dest='url', help="target url")
    parseCollect = parser.parse_args()
    targeturl = parseCollect.url



    unit = wgetsubstitute()

    unit.fulldownload(targeturl)

