# 10秒ごとによく使われている単語をまとめる

import codecs
import os
import json
import MeCab

import mecab_helper

accept_parts = ['名詞','形容詞','感動詞']

def get_aggregate_words(mecab, id):
    # 10秒ごとにまとめる
    aggregate_msec = 10000

    dic = {}
    with codecs.open('./livechat/{}.json'.format(id)) as f:
        chats = json.loads(f.read())
        for chat in chats:
            message = chat['message']
            offsetMsec = chat['offsetMsec']
            mecab_result = mecab.parse(message)
            array = mecab_helper.parse_mecab_result(mecab_result)
            array = [x for x in array if x['part'] in accept_parts]

            key_msec = offsetMsec - offsetMsec % aggregate_msec
            if key_msec not in dic:
                word_count_dic = {}
                dic[key_msec] = word_count_dic
            else:
                word_count_dic = dic[key_msec]
            
            for item in array:
                if item['word'] in word_count_dic:
                    word_count_dic[item['word']] += 1
                else:
                    word_count_dic[item['word']] = 1
                
    # 時間でソートする
    items = sorted(dic.items(), key=lambda x: x[0])
    
    # 多く使われているワード30に制限する
    result = []
    for key_msec, word_count_dic in items:
        sorted_word_count = sorted(word_count_dic.items(), key=lambda x: x[1], reverse=True)
        words = [{'word': word, 'count': count} for word, count in sorted_word_count]
        result.append({'msec':key_msec, 'words':words})
        
    return result
    
