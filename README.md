# Bs_to Dowloader

This little programm allows you to download streamcloud files from CLI from [bs.to](http://bs.to).
This is a german website so stream series and animes and other stuff like:

+ Castle
+ NCIS
+ Fairy Tail
+ Sword art Online
+ RWBY

note that all these vids habe a German reference. they are Ger dub or Ger sub.


## Usage

like
    
    ./scdownload -d http://bs.to/serie/Game-of-Thrones
    
and the Download will begin. 

with **-l <streamcloud-url>** you can give a streamcloud-url to download this one file (like the script from koji3)
and **-f <file-with-urls>** you can give a file with urls that the programm should be download. 

## notice

only streamcloud-references can be Downloaded. in some times they aren't streamcloud references and the programm will skip
these. you get not a message from that.

the programm works straight line, no threading or other fancy magic.

## references

thanks for [koji3](https://github.com/koji3/Streaming-dl) that little script is the base for my programm. maybe is will
improove it. or migrate it in python. 