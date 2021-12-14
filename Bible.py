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

    def __eq__(self, __o) -> bool:
        return (self.book == __o.book and self.chapter == __o.chapter
                and self.verse == __o.verse)


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
            self.__texts = Texts(
                verseData['heading'], verseData['versetext'],
                verseData['footnotes'], commentaryData['Commentary']
                if commentaryData is not None else '')
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

        bible = bibleJson['REV_Bible']
        for verse in bible:
            path = BiblePath(verse['book'], verse['chapter'], verse['verse'])

            def check_commentary(comment):
                return (path.book == comment['book']
                        and path.chapter == comment['chapter']
                        and path.verse == comment['verse'])

            commentaryData = next(filter(check_commentary, commentary), None)
            self.__bible.append(Verse(verse, commentaryData))

        appendices = appendixJson['REV_Appendices']

        for appendix in appendices:
            self.__appendices.append(
                Appendix(appendix['title'], appendix['appendix']))

    @property
    def books(self):
        def book(verse: Verse):
            return verse.path.book

        bookList = []

        for path in map(book, self.__bible):
            if path in bookList:
                continue
            bookList.append(path)

        return bookList

    def chapters(self, book: str):
        def check_book(verse: Verse):
            return verse.path.book == book

        chapterList: list[int] = []

        for verse in filter(check_book, self.__bible):
            if verse.path.chapter in chapterList:
                continue
            chapterList.append(verse.path.chapter)

        return chapterList

    def verses(self, book: str, chapter: int):
        def check_chapter(verse: Verse):
            return verse.path.book == book and verse.path.chapter == chapter

        verseList: list[int] = []

        for verse in filter(check_chapter, self.__bible):
            if verse.path.verse in verseList:
                continue
            verseList.append(verse.path.verse)

        return verseList

    @property
    def appendices(self):
        def title(appendix: Appendix):
            return appendix.title

        return [appendix for appendix in map(title, self.__appendices)]

    def appendix(self, title: str):
        def check_appendix(app: Appendix):
            return app.title == title

        return next(filter(check_appendix, self.__appendices)).appendix

    @property
    def texts(self):
        def get_text(verse: Verse):
            return verse.texts

        return [text for text in map(get_text, self.__bible)]
