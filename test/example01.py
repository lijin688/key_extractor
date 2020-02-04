import codecs
from textrank.text_rank import TextRank4Keyword
from conf.config import filename


text = codecs.open(filename, 'r', 'utf-8').read()
tr4w = TextRank4Keyword()

tr4w.analyze(text=text, lower=False, window=5)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

print('关键词：' )
for item in tr4w.get_keywords(10, word_min_len=2):
    print(item.word, item.weight)
