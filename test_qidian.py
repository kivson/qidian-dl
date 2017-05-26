from unittest import TestCase

from funcy.seqs import first

import qidian


class Test_qidian(TestCase):
    def test__get_token(self):
        token = qidian._get_csrftoken()
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)

    def test_get_novels(self):
        novels = list(qidian.novels())

        self.assertGreater(len(novels), 0)
        self.assertIn('bookId', novels[0])
        self.assertIn('bookName', novels[0])

    def test_get_charpters(self):
        chapters = list(qidian.charpters_list('6831850602000905'))

        self.assertGreater(len(chapters), 0)
        self.assertIn('chapterId', chapters[0])
        self.assertIn('chapterIndex', chapters[0])
        self.assertIn('chapterName', chapters[0])

    def test_chapter(self):
        chapter = qidian.chapter('6831850602000905', '19654531444951530')
        self.assertIn('chapterId', chapter)
        self.assertIn('chapterName', chapter)
        self.assertIn('content', chapter)
        self.assertIn('chapterIndex', chapter)

    def test_all_chapters(self):

        all_chapters = qidian.all_chapters('6831850602000905')

        chapter = first(all_chapters)

        self.assertIn('chapterId', chapter)
        self.assertIn('chapterName', chapter)
        self.assertIn('content', chapter)
        self.assertIn('chapterIndex', chapter)
