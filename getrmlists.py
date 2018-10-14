#!/usr/bin/env python

# Download a wikipedia page, scrape it for the titles of rick and morty episodes,
# map the episode numbers to the titles, then rename my rick and morty episodes
# adding the titles before the filename suffixes.

import bs4
import shutil
import pathlib
import glob

# actually download the page to file
# import requests
# page = requests.get('https://en.wikipedia.org/wiki/List_of_Rick_and_Morty_episodes')
# pathlib.Path(filename).write_bytes(page.content)

# filename of html file
filename = str(pathlib.Path.cwd()) + '/wikipedia_rickandmorty.html'
# bytes from html file
page = pathlib.Path(filename).read_bytes()
# parsed html content
content = bs4.BeautifulSoup(page, 'html.parser')
# all table rows <tr class=vevent > rick and morty episode titles
episodeRowsBulk = content.find_all('tr', class_='vevent')
# paths of local files named S0*E**
paths = glob.glob('/home/sky/Nextcloud/Media/Rick*/Rick*')
# dictionary for mapping episode names to episode numbers
episodeMapping = dict()

# season number
senum = 1
for idx, row in enumerate(episodeRowsBulk, start=1):
    # only care about 1 - 31
    if(idx < 32):
        # get episode number from <td> element
        epnum = row.contents[1].text
        key = 'S0' + str(senum)
        # if episode number is 2 digits
        if (int(epnum) == 10 or int(epnum) == 11):
            key += 'E' + epnum
        else:
            key += 'E0' + epnum
        # map S0*E** string to episode name
        episodeMapping[key] = row.contents[2].text
        if(idx == 11 or idx == 21 ):
            senum += 1

# look for map in each path
for map in episodeMapping:
    for path in paths:
        if(map in path):
            # create a path object
            aPath = pathlib.Path(path)
            # generate a new path name inserting the episode title before the suffix
            newPath = str(aPath.parent) + '/' + str(aPath.stem).replace(' ','') +  '_' \
            + str(episodeMapping[map]).replace(' ','').replace('\"','').replace('[b]','').replace('\'','') \
            + str(aPath.suffix)
            # print the paths
            print("\nOld Path: " + str(path) + "\nNew Path: " + newPath)
            #print("\nmoving...")
            #shutil.move(str(aPath), newPath)
            break