import codecs
import os
import MeCab
import codecs

from get_keywords import get_keywords

files = [os.path.join('livechat', f) for f in os.listdir('livechat')
    if os.path.isfile(os.path.join('livechat', f))]

# ストップワード
# このURLのものを使用: https://qiita.com/kenmatsu4/items/9b6ac74f831443d29074
stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して',
            u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',
            u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で',
            u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']

# どの放送でもよく出てくるワード
additional_stop_words = [
    # u'イオリン', u'かわいい', u'すごい', u'かしこい', u'えらい', u'好き', u'すき', u'だいじょうぶ', u'大丈夫', u'いい',
    u'w', u'ww', u'www', u'wwww', u'wwwww', u'wwwwww',
]

sw_set = set(stop_words + additional_stop_words)
m = MeCab.Tagger('-u ./dotlive.dic')


def get_vocabulary_dic():
    files = [os.path.join('livechat', f) for f in os.listdir('livechat')
        if os.path.isfile(os.path.join('livechat', f))]

    dic = {}
    for file in files:
        vocabulary = {}

        keywords = get_keywords(m, file, ['名詞','形容詞','感動詞'])

        for keyword in keywords:
            # ストップワードか長さ1は除外
            if keyword in sw_set or len(keyword) == 1:
                continue

            if keyword in vocabulary:
                vocabulary[keyword] += 1
            else:
                vocabulary[keyword] = 1

        dic[file] = vocabulary
    
    return dic

def flatten_vocabulary_dic(vocabulary_dic):
    result = {} 
    for _, vocabulary in vocabulary_dic.items():
        for keyword, count in vocabulary.items():
            if keyword in result:
                result[keyword] += count
            else:
                result[keyword] = count
    
    return result

# キーワードが配信全体でどれだけ使用されているかを調べる
def calc_total_use_rate(vocabulary_dic):
    # 配信回数
    total_num = len(vocabulary_dic)
    if total_num == 0:
        return {}

    dic = {}
    for _, vocabulary in vocabulary_dic.items():
        eixsts_set = set()
        for keyword, count in vocabulary.items():
            if not keyword in eixsts_set:
                eixsts_set.add(keyword)
                if keyword in dic:
                    dic[keyword] += 1
                else:
                    dic[keyword] = 1


    result = {}
    for keyword, count in dic.items():
        result[keyword] = count / total_num

    return result