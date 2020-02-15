# Telepath
Welcome! This program is designed as a utility for CS61C students using Ubuntu (or the Windows Subsystem for Linux). It uses data hosted by OCF to compute the current server with the least load and automatically ssh's users in to it.

## What it is actually
Telepath, as you can see, is a very simple Python script that does calculations with OCF's JSON and pipes the output into a bash file that executes the ssh command for you. No bells and whistles here - that's it!

## Downloading
First, download these files onto your machine.
Put the file named "telepath" somewhere accessible to your path.
Then, fill in the path to "telepath.py" in "telepath".
And you should be good to go!

## Usage
Use telepath in one of two equivalent ways:
```
$ telepath xxx
```
or:
```
$ telepath
What's your CS61C 3-letter login (cs61c-xxx)?
xxx
```

## Credits and acknowledgements
This code was made by Ayush Sharma.
The data is hosted by [Berkeley's Open Computing Facility](https://www.ocf.berkeley.edu/) and maintained by [HKN's Compserv Committee](https://hkn.eecs.berkeley.edu/about/officers). The link to the original Hivemind repository can be found [here](https://github.com/compserv/hivemind).
A special thanks to Jared Fung for helping me test and debug this!

### Why "telepath"?
As [Wikipedia](https://en.wikipedia.org/wiki/Group_mind_(science_fiction)) says, a hivemind can be made up of a swarm of beings that communicate directly, sometimes via telepathy. The "path" pun was too good to pass up. :)