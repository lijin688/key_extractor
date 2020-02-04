import jieba
jieba.add_word('三井株式会社')
import jieba.posseg as pseg
jieba.add_word("美国证监会")

# s = '阿里巴巴集团董事局主席马云在阿里巴巴集团标志前（2013年11月12日摄）。2014年5月7日早间，阿里巴巴集团向美国证监会提交首次公开募股（IPO）申请文件。'
s = '4月19日，上海海事法院依法扣押了商船三井株式会社所有的、停泊于浙江省舟山市嵊泗马迹山港的226434吨“BAOSTEEL EMOTION”货轮，引发日本政坛关注。'
words = pseg.cut(s)
for w in words:
    print("%s %s" %(w.word, w.flag))

