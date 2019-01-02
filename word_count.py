import codecs
import os
import json
import MeCab

import mecab_helper

m = MeCab.Tagger('-u ./dotlive.dic')

input_dir = './livechat'
accept_parts = ['名詞','形容詞','感動詞']

for file_name in os.listdir(input_dir):
    if not file_name.endswith('.json'):
        continue


    # 10秒ごとにまとめる
    aggregate_msec = 10000

    dic = {}
    with codecs.open('{}/{}'.format(input_dir, file_name)) as f:
        chats = json.loads(f.read())
        for chat in chats:
            message = chat['message']
            offsetMsec = chat['offsetMsec']
            mecab_result = m.parse(message)
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
    
    # 多く使われているワード30に制限する
    dic2 = {}
    for key_msec, word_count_dic in dic.items():
        sorted_word_count = sorted(word_count_dic.items(), key=lambda x: x[1], reverse=True)
        dic2[key_msec] = sorted_word_count[0:10]
        
            
    str = json.dumps(dic2, ensure_ascii=False)
    with codecs.open('./word_count/{}'.format(file_name), 'w', 'utf-8') as f:
        f.write(str)
    
