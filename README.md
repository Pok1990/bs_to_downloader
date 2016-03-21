# Bs_to Downloader

This little program allows you to download streamcloud files from CLI from [bs.to](http://bs.to).
This is a German website so stream series and animes and other stuff like:

+ Castle
+ NCIS
+ Fairy Tail
+ Sword art Online
+ RWBY

note that all these videos have a German reference. they are Ger dub or Ger sub.


## Usage

like
    
    ./scdownload -d http://bs.to/serie/Game-of-Thrones
    
and the Download will begin. 

with **--urlfile ** you can give a streamcloud-url to download this one file (like the script from koji3)
and **--download ** you can give a file with urls that the program should be download. 

after a finish Download the directory will be moved in your 

    ~/Videos

directory.

## notice

only streamcloud-references can be Downloaded. in some times they aren't streamcloud references and the program will skip
these. you get not a message from that.

the program works straight line, no threading or other fancy magic.

## references

thanks for [koji3](https://github.com/koji3/Streaming-dl) that little script is the base for my program. maybe is will
improve it. or migrate it in python. 