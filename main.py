#!/usr/bin/env python3
""" The REV app for reading and managing scripture from the Revised English
Version bible

Currently in it's infancy it will eventually be a command line utility for
quick bible lookups as well as saving and exporting sections of scripture.

A command line style usage should be sufficient with a minimum of

> help

commands:
    help - display this help screen
    quit - exit the program

    books - list books of the bible

    find SEARCH_PARAM - search the bible for a word or phrase
    lookup BIBLE_REF - find a section of scripture using a standard bible ref
    (i.e. Jn 3:16)
"""

from Rev_Data import RevData

if __name__ == '__main__':
    data = RevData()
    print(data.bible.books)
    print(data.bible.chapters('Genesis'))
    print(data.bible.verses('Genesis', 1))
