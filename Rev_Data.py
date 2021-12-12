""" This is the collection of all data that will be stored and used
throughout the program """

import pickle
import os
import sys

import requests

from Bible import Bible
from Timestamp import Timestamp

_APPENDIX_URL = 'https://www.revisedenglishversion.com/jsondload.php?fil=203'
_BIBLE_URL = 'https://www.revisedenglishversion.com/jsondload.php?fil=201'
_COMMENTARY_URL = 'https://www.revisedenglishversion.com/jsondload.php?fil=202'

_FILENAME = 'RevData.dat'


class RevData:
    """ Contains the bible, commentary, and appendix together. """
    __slots__ = ('__bible', '__timestamp')

    __bible: Bible
    __timestamp: Timestamp

    def __init__(self) -> None:
        self.__timestamp = Timestamp()

        if self.__timestamp.needs_update:
            self.__download_bible()
        else:
            self.__load_bible()

    def __download_bible(self) -> bool:
        bibleJson = requests.get(_BIBLE_URL).json()
        commentaryJson = requests.get(_COMMENTARY_URL).json()
        appendixJson = requests.get(_APPENDIX_URL).json()

        self.__bible = Bible(bibleJson, commentaryJson, appendixJson)
        if self.__save_bible():
            self.__timestamp.save()
            return True
        return False

    def __load_bible(self) -> bool:
        try:
            with open(_FILENAME, 'rb') as file:
                self.__bible = pickle.load(file)
                return True
        except (EnvironmentError, pickle.UnpicklingError):
            return self.__download_bible()

    def __save_bible(self) -> bool:
        try:
            with open(_FILENAME, 'wb') as file:
                pickle.dump(self.__bible, file, pickle.HIGHEST_PROTOCOL)
                return True
        except (EnvironmentError, pickle.PicklingError) as err:
            print(f"{0}: export error: {1}".format(
                os.path.basename(sys.argv[0]), err))
            return False

    @property
    def bible(self):
        return self.__bible
