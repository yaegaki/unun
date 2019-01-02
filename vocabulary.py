import codecs
import os
import MeCab
import codecs

from get_keywords import get_keywords


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

def get_mecab():
    return m

def get_vocabulary_dic():
    files = [os.path.join('livechat', f) for f in os.listdir('livechat')
        if os.path.isfile(os.path.join('livechat', f))]

    json_files = [f for f in files if os.path.splitext(f)[1] == '.json']

    dic = {}
    for file in json_files:
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
    total_key_count = len(vocabulary_dic)
    if total_key_count == 0:
        return {}

    dic = {}
    for _, vocabulary in vocabulary_dic.items():
        # ボキャブラリ内の全単語の全出現数
        total_count = 0
        for _, count in vocabulary.items():
            total_count += count

        for keyword, count in vocabulary.items():
            # 全コメントの内、どれくらいを占めているか
            rate = count / total_count
            if keyword in dic:
                dic[keyword] = dic[keyword] + rate
            else:
                dic[keyword] = rate


    result = {}
    for keyword, rate in dic.items():
        result[keyword] = rate / total_key_count

    return result