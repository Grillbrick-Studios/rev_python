""" This is simply the timestamp check for the online REV json files to see
if there is an update.

>>> ts = Timestamp()
Timestamp(...)

>>> ts.needs_update
True | False
"""

import datetime
import pickle
import os
import sys

import requests

_URL = 'https://www.revisedenglishversion.com/jsondload.php?fil=200'
_FILENAME = 'timestamp.dat'


class Timestamp:
    """ holds time data to be compared with the server """
    __slots__ = ('__server_time', '__local_time')

    __server_time: datetime.datetime
    __local_time: datetime.datetime | None

    def __init__(self) -> None:
        request = requests.get(_URL)
        timestamp = request.json()['REV_Timestamp'][0]['timestamp']
        self.__server_time = datetime.datetime.fromisoformat(timestamp)
        self.load()

    @property
    def needs_update(self) -> bool:
        return self.__local_time is None or self.__local_time < self.__server_time

    @property
    def server_time(self):
        """ returns the server date for when the server data was last updated """
        return self.__server_time

    @property
    def local_time(self):
        """ returns the local_time from a file or None if there is none. """
        return self.__local_time

    def save(self):
        """ Save the server timestamp indicating that you have the most
        recent files """
        try:
            with open(_FILENAME, 'wb') as file:
                pickle.dump(self.__server_time, file, pickle.HIGHEST_PROTOCOL)
                return True
        except (EnvironmentError, pickle.PicklingError) as err:
            print(f"{0}: export error: {1}".format(
                os.path.basename(sys.argv[0]), err))
            return False

    def load(self):
        """ Load the local timestamp from a file if it exists """
        try:
            with open(_FILENAME, 'rb') as file:
                self.__local_time = pickle.load(file)
                return True
        except (EnvironmentError, pickle.UnpicklingError):
            self.__local_time = None
            return False
