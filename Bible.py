from enum import Enum
from typing import NamedTuple


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


class BiblePath(NamedTuple):
    book: str
    chapter: int
    verse: int


class VerseStyling(NamedTuple):
    paragraph: bool
    microheading: bool
    style: Style


class Texts(NamedTuple):
    heading: str
    verse: str
    footnotes: list[str]
    commentary: str


class MissingDataException(Exception):
    pass


class Appendix(NamedTuple):
    title: str
    appendix: str


class Verse:
    __slots__ = ('__path', '__style', '__texts')

    __path: BiblePath
    __style: VerseStyling
    __texts: Texts

    def __init__(
        self,
        verseData,
        commentaryData,
    ) -> None:
        if verseData is not None:
            self.__path = BiblePath(verseData['book'], verseData['chapter'],
                                    verseData['verse'])
            self.__style = VerseStyling(verseData['paragraph'],
                                        verseData['microheading'],
                                        verseData['style'])
            self.__texts = Texts(verseData['heading'], verseData['versetext'],
                                 verseData['footnotes'], commentaryData)
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
    __slots__ = ('__bible', '__appendices')
    __bible: list[Verse]
    __appendices: list[Appendix]

    def __init__(self, bibleJson: dict, commentaryJson: dict,
                 appendixJson: dict) -> None:
        self.__bible = []
        self.__appendices = []

        commentary = commentaryJson['REV_Commentary']
        commentaryDict: dict[BiblePath, str] = {}

        for comment in commentary:
            commentaryDict[BiblePath(comment['book'], comment['chapter'],
                                     comment['verse'])] = comment['commentary']

        bible = bibleJson['REV_Bible']
        for verse in bible:
            path = BiblePath(verse['book'], verse['chapter'], verse['verse'])
            commentaryData = commentaryDict.get(path, '')
            self.__bible.append(Verse(verse, commentaryData))

        appendices = appendixJson['REV_Appendices']

        for appendix in appendices:
            self.__appendices.append(
                Appendix(appendix['title'], appendix['appendix']))

    @property
    def books(self):
        def book(verse: Verse):
            return verse.path.book

        return (path for path in set(map(book, self.__bible)))

    def chapters(self, book: str):
        def check_book(verse: Verse):
            return verse.path.book == book

        return (verse.path.chapter
                for verse in set(filter(check_book, self.__bible)))

    def verses(self, book: str, chapter: int):
        def check_chapter(verse: Verse):
            return verse.path.book == book and verse.path.chapter == chapter

        return (verse.path.verse
                for verse in set(filter(check_chapter, self.__bible)))
