#!/bin/sh

# Fetch print views
rm -rf print
mkdir print

touch cookie.txt

curl --cookie-jar cookie.txt "http://staka.zug.ch/default.asp?level=1&BANDid=6"
curl --cookie cookie.txt "http://staka.zug.ch/print.asp" > print/1.html

curl --cookie-jar cookie.txt "http://staka.zug.ch/default.asp?level=1&BANDid=5"
curl --cookie cookie.txt "http://staka.zug.ch/print.asp" > print/2.html

curl --cookie-jar cookie.txt "http://staka.zug.ch/default.asp?level=1&BANDid=7"
curl --cookie cookie.txt "http://staka.zug.ch/print.asp" > print/3.html

curl --cookie-jar cookie.txt "http://staka.zug.ch/default.asp?level=1&BANDid=8"
curl --cookie cookie.txt "http://staka.zug.ch/print.asp" > print/4.html

curl --cookie-jar cookie.txt "http://staka.zug.ch/default.asp?level=1&BANDid=9"
curl --cookie cookie.txt "http://staka.zug.ch/print.asp" > print/5.html

curl --cookie-jar cookie.txt "http://staka.zug.ch/default.asp?level=1&BANDid=10"
curl --cookie cookie.txt "http://staka.zug.ch/print.asp" > print/6.html

rm cookie.txt
