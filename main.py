#!/usr/bin/python
import sys, re, os, urllib.request
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
l_f = os.path.join(BASE_DIR, '.list.txt')

def main():
    args = sys.argv
    genres = []
    cmd = ""
    song = ""

    # remove the file path
    args.pop(0)

    # check cli arguments for stuff
    for argument in args:
        if argument.startswith('+'):
            genres.append(argument)
        elif argument.lower() == "a" or argument.lower() == "l" or argument.lower() == "p":
            cmd = argument
        else:
            song = argument

    # add song
    if cmd == "a":
        f = open(l_f, "a")
        fr = open(l_f, "r")
        songs = []

        genres = " ".join(genres)

        for line in fr:
            songs.append(line)

        # get the title
        soup = urllib.request.urlopen(song)
        soup = BeautifulSoup(soup, "html.parser")
        title = soup.title.text.replace(" - YouTube", "")

        # put everything together
        line = str(len(songs)+1) + " " + title + " url:" + song + " " + genres
        pline = "\033[1;33m#" + str(len(songs)+1) + "\033[1;m " + title + " \033[1;31m" + genres + "\033[1;m"

        # write to file and print the ad
        f.write(line + "\n")
        print(pline)

    # list songs
    elif cmd == "l":
        f = open(l_f, "r")
        lines = []

        # search with genres
        if genres:
            for line in f:
                for genre in genres:
                    if genre.lower() in line.lower():
                        lines.append(line)

        # search for string match
        elif song:
            for line in f:
                if song.lower() in line.lower():
                    lines.append(line)

        # else display all lines
        else:
            for line in f:
                lines.append(line)

        # display whatever was found
        for line in lines:
            line = re.match("(\d) (.+) url:.*? +(.*)", line)
            number = line.group(1)
            title = line.group(2)
            genress = line.group(3)
            print("\033[1;33m#" + number + "\033[1;m " + title + " \033[1;31m" + genress + "\033[1;m")

    # play song
    elif cmd == "p": # play
        f = open(l_f, "r")

        for line in f:
            if line.startswith(song):
                url = line.split("url:")[1].split(" ")[0]
                # this still streams the video but doesnt display it
                os.system("mpv --vo=null " + url)
    else:
        print("Bad command\nTry: [A]dd, [L]ist & [P]lay")

if __name__ == '__main__':
    main()
