from collections import namedtuple
from enum import Enum


class Style(Enum):
    Prose = 1
    Poetry = 2
    PoetryNoPostGap = 3
    PoetryPreGap = 4
    PoetryPreGapNoPostGap = 5
    List = 6
    ListNoPostGap = 7
    ListPreGap = 8
    ListPreGapNoPostGap = 9


class ViewMode(Enum):
    Paragraph = 0
    VerseBreak = 1
    Reading = 2


BiblePath = namedtuple('BiblePath', [('book', str), ('chapter', int),
                                     ('verse', int)])

VerseStyling = namedtuple('VerseStyling', [('paragraph', bool),
                                           ('microheading', bool),
                                           ('style', Style)])

Texts = namedtuple('Texts', [('heading', str), ('verse', str),
                             ('footnotes', list[str]), ('commentary', str)])


class MissingDataException(Exception):
    pass


class Verse:
    __slots__ = ('__path', '__style', '__texts')

    __path: BiblePath | str
    __style: VerseStyling | None
    __texts: Texts | str

    def __init__(self,
                 verseData=None,
                 commentaryData=None,
                 appendixData=None) -> None:
        if verseData is not None and commentaryData is not None:
            self.__path = BiblePath(verseData.book, verseData.chapter,
                                    verseData.verse)
            self.__style = VerseStyling(verseData.paragraph,
                                        verseData.microheading,
                                        verseData.style)
            self.__texts = Texts(verseData.heading, verseData.versetext,
                                 verseData.footnotes,
                                 commentaryData.commentary)
        elif appendixData is not None:
            self.__path = appendixData.title
            self.__style = None
            self.__texts = appendixData.appendix
        else:
            raise MissingDataException()

    @property
    def path(self):
        return self.__path

    @property
    def style(self):
        return self.__style

    @property
    def texts(self):
        return self.__texts


class Bible:
    __slots__ = ('__verses', '__appendices')
    __verses: dict[BiblePath, Verse]
    __appendices: dict[str, Verse]

    def __init__(self, bibleJson, commentaryJson, appendixJson) -> None:
        pass
