import os
import jieba
from comentropy.model import TrieNode
from comentropy.utils import get_stopwords, load_dictionary, generate_ngram, save_model, load_model
from comentropy.config import basedir

root_name = basedir + "/data/root.pkl"
stopwords = get_stopwords()
if os.path.exists(root_name):
    root = load_model(root_name)
else:
    dict_name = basedir + '/data/dict.txt'
    word_freq = load_dictionary(dict_name)
    root = TrieNode('*', word_freq)
    save_model(root, root_name)

# filename = '../test/doc/06.txt'
def load_data(filename, stopwords):
    """

    :param filename:
    :param stopwords:
    :return: 二维数组,[[句子1分词list], [句子2分词list],...,[句子n分词list]]
    """
    data = []
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            word_list = [x for x in jieba.cut(line.strip(), cut_all=False) if x not in stopwords]
            data.append(word_list)
    return data


def load_data_2_root(data):
    print('------> 插入节点')
    for word_list in data:
        # tmp 表示每一行自由组合后的结果（n gram）
        # tmp: [['它'], ['是'], ['小'], ['狗'], ['它', '是'], ['是', '小'], ['小', '狗'], ['它', '是', '小'], ['是', '小', '狗']]
        ngrams = generate_ngram(word_list, 3)
        for d in ngrams:
            root.add(d)
    print('------> 插入成功')


def get_new_words(filename, topN=5):
    # 加载新的文章
    data = load_data(filename, stopwords)
    # 将新的文章插入到Root中
    load_data_2_root(data)

    result, add_word = root.find_word(topN)
    print(add_word)
    # 如果想要调试和选择其他的阈值，可以print result来调整
    # print("\n----\n", result)
    print("\n----\n", '增加了 %d 个新词, 词语和得分分别为: \n' % len(add_word))
    print('#############################')
    for word, score in add_word.items():
        print(word + ' ---->  ', score)
    print('#############################')
    return add_word.keys()

if __name__ == "__main__":
    filename = '../test/doc/06.txt'
    nw = get_new_words(filename)
    print(nw)
    pass

    # # 前后效果对比
    # test_sentence = '蔡英文在昨天应民进党当局的邀请，准备和陈时中一道前往世界卫生大会，和谈有关九二共识问题'
    # print('添加前：')
    # print("".join([(x + '/ ') for x in jieba.cut(test_sentence, cut_all=False) if x not in stopwords]))
    #
    # for word in add_word.keys():
    #     jieba.add_word(word)
    # print("添加后：")
    # print("".join([(x + '/ ') for x in jieba.cut(test_sentence, cut_all=False) if x not in stopwords]))