import os
import math
import networkx as nx
import numpy as np
import sys

sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
allow_speech_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng', 'x']

text_type    = str
string_types = (str,)

def as_text(v):  ## 生成unicode字符串
    if v is None:
        return None
    elif isinstance(v, bytes):
        return v.decode('utf-8', errors='ignore')
    elif isinstance(v, str):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))


def is_text(v):
    return isinstance(v, text_type)


class AttrDict(dict):
    """Dict that can get attribute by dot"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def combine(word_list, window=2):
    """构造在window下的单词组合，用来构造单词之间的边。

    Keyword arguments:
    word_list  --  list of str, 由单词组成的列表。
    windows    --  int, 窗口大小。
    """
    if window < 2: window = 2
    for x in range(1, window):
        if x >= len(word_list):
            break
        word_list2 = word_list[x:]
        res = zip(word_list, word_list2)
        for r in res:
            yield r


def sort_words(vertex_source, edge_source, window=2, pagerank_config={'alpha': 0.85, }):
    """将单词按关键程度从大到小排序

    Keyword arguments:
    vertex_source   --  二维列表，子列表代表句子，子列表的元素是单词，这些单词用来构造pagerank中的节点
    edge_source     --  二维列表，子列表代表句子，子列表的元素是单词，根据单词位置关系构造pagerank中的边
    window          --  一个句子中相邻的window个单词，两两之间认为有边
    pagerank_config --  pagerank的设置
    """
    sorted_words = []
    word_index = {}
    index_word = {}
    _vertex_source = vertex_source
    _edge_source = edge_source
    words_number = 0
    for word_list in _vertex_source:
        for word in word_list:
            if not word in word_index:
                word_index[word] = words_number  # 给word编号
                index_word[words_number] = word
                words_number += 1

    graph = np.zeros((words_number, words_number))

    for word_list in _edge_source:
        for w1, w2 in combine(word_list, window):
            if w1 in word_index and w2 in word_index:
                index1 = word_index[w1]
                index2 = word_index[w2]
                graph[index1][index2] = 1.0
                graph[index2][index1] = 1.0

    print('graph:\n', graph)

    nx_graph = nx.from_numpy_matrix(graph)
    scores = nx.pagerank(nx_graph, **pagerank_config)  # this is a dict
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    for index, score in sorted_scores:
        item = AttrDict(word=index_word[index], weight=score)
        sorted_words.append(item)

    return sorted_words


# 分词
# def segment(text, lower=True, use_stop_words=True, use_speech_tags_filter=False):
#     """对一段文本进行分词，返回list类型的分词结果
#
#     Keyword arguments:
#     lower                  -- 是否将单词小写（针对英文）
#     use_stop_words         -- 若为True，则利用停止词集合来过滤（去掉停止词）
#     use_speech_tags_filter -- 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。
#     """
#     text = as_text(text)
#     jieba_result = pseg.cut(text)
#
#     if use_speech_tags_filter == True:
#         jieba_result = [w for w in jieba_result if w.flag in self.default_speech_tag_filter]
#     else:
#         jieba_result = [w for w in jieba_result]
#
#     # 去除特殊符号
#     word_list = [w.word.strip() for w in jieba_result if w.flag != 'x']
#     word_list = [word for word in word_list if len(word) > 0]
#
#     if lower:
#         word_list = [word.lower() for word in word_list]
#
#     if use_stop_words:
#         word_list = [word.strip() for word in word_list if word.strip() not in self.stop_words]
#
#     return word_list
