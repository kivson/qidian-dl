# qidian-dl
Library for downloading information and chapters of qidian internations novels

```python
import qidian

#List all novels (return generator)
for novel in qidian.novels():
    print(novel)
...
{'bookId': 6831850602000905, 'bookName': "Library of Heaven's Path", 'categoryId': 20001, 'categoryName': 'Xuanhuan', 'totalScore': '4.2', 'description': 'Zhang Xuan...'}
...

#List chapters summary info (return generator)
for chap in qidian.charpters_list('6831850602000905'):
    print(chap)
...
{'chapterId': '18339109613388345', 'chapterName': 'Swindler ', 'chapterIndex': 1}
...

#Get full charpter content, with the translation content
full_chapter = qidian.chapter('6831850602000905', '19654531444951530')
{
  'chapterId': '19654531444951530',
  'chapterName': 'Death Aura',
  'chapterIndex': 111,
  'groupItems': [],
  'translatorItems': [
    {
      'id': '18339947115233299',
      'name': 'StarveCleric'
    }
  ],
  'editorItems': [
    {
      'id': '18339947115233306',
      'name': 'Frappe'
    }
  ],
  'preChapterId': '19631048174389680',
  'nextChapterId': '19677978761940259',
  'content': "<Charpter content here>",
  'firstChapterId': 18339109613388345,
  'firstChapterIndex': 1
}

# Return full charpter content of all chapters from one novel
qidian.all_chapters('6831850602000905', poolsize=10)
```
