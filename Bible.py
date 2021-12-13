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
        if verseData is not None:
            self.__path = BiblePath(verseData.book, verseData.chapter,
                                    verseData.verse)
            self.__style = VerseStyling(verseData.paragraph,
                                        verseData.microheading,
                                        verseData.style)
            self.__texts = Texts(
                verseData.heading, verseData.versetext, verseData.footnotes,
                commentaryData.commentary
                if commentaryData is not None else '')
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
    __slots__ = ('__old_testament', '__new_testament', '__appendices')
    __old_testament: dict[BiblePath, Verse]
    __new_testament: dict[BiblePath, Verse]
    __appendices: dict[str, Verse]

    def __init__(self, bibleJson, commentaryJson, appendixJson) -> None:
        self.__old_testament = {}
        self.__new_testament = {}
        self.__appendices = {}

        commentary = commentaryJson['REV_Commentary']
        commentaryDict = {}

        for comment in commentary:
            commentaryDict[BiblePath(comment.book, comment.chapter,
                                     comment.verse)] = comment.commentary

        bible = bibleJson['REV_Bible']
        new_testament = False
        for verse in bible:
            if verse.book.startswith('Matt'):
                new_testament = True
            path = BiblePath(verse.book, verse.chapter, verse.verse)
            commentaryData = commentaryDict.get(path, None)
            if new_testament:
                self.__new_testament[path] = Verse(
                    verseData=verse, commentaryData=commentaryData)
            else:
                self.__old_testament[path] = Verse(
                    verseData=verse, commentaryData=commentaryData)

        appendices = appendixJson['REV_Appendices']

        for appendix in appendices:
            self.__appendices[appendix.title] = Verse(appendixData=appendix)

    @property
    def books(self):
        def book(path: BiblePath):
            return path.book

        return (path.book for path in set(
            map(book,
                self.__old_testament.keys()
                | self.__new_testament.keys())))

    def chapters(self, book: str):
        def check_book(path: BiblePath):
            return path.book == book

        return (path.chapter for path in filter(
            check_book,
            self.__old_testament.keys() | self.__new_testament.keys()))

    def verses(self, book: str, chapter: int):
        def check_chapter(path: BiblePath):
            return path.book == book and path.chapter == chapter

        return (path.verse for path in filter(
            check_chapter,
            self.__old_testament.keys() | self.__new_testament.keys()))
