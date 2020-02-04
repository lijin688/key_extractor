from textrank import text_rank
from textrank.segmentation import WordSegmentation

def fun_1():
    text = "视频里，我们的杰宝热情地用英文和全场观众打招呼并清唱了一段《Heal The World》。我们的世界充满了未知数。"
    text = ''
    r = text_rank.segment_sentence(text)
    print(r)
    return r


def fun_2():
    ws = WordSegmentation()
    sts = fun_1()
    r = ws.segment_words(sts, lower=False, use_stop_words=True, use_speech_tags_filter=True)
    print(r)


if __name__ == '__main__':
    fun_2()