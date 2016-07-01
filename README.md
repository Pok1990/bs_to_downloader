# Bs_to Downloader

This little program allows you to download streamcloud files from CLI from [bs.to](http://bs.to).
This is a German website so stream series and animes and other stuff like:

+ Castle
+ NCIS
+ Fairy Tail
+ Sword art Online
+ RWBY

note that all these videos have a German reference. they are Ger dub or Ger sub.

## required environment

this program is tested with python3.5
should run also on python3.4

## Usage

like

    ./scdownload.py --series http://bs.to/serie/Game-of-Thrones

and the Download will begin.

with ** --series < link > ** you can give a Bs.to link that the program should be download.

with ** --log <1|2|3|4|5> ** you can set a verbose-level for debug and info output.

after a finish Download the directory will be moved in your

    ~/Videos

directory.

## Notice

only streamcloud-references can be Downloaded. in some cases they aren't streamcloud references and the program will skip
these.

the program works straight line, no threading or other fancy magic.

## References

thanks for [koji3](https://github.com/koji3/Streaming-dl) that little script is the base for my program. maybe is will

The script from Koji3 is not longer nessesary, since is write my own module for the job.
