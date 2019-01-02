# 配信を特徴となるようなチャットを抜き出す
import codecs
import os
import json

import vocabulary

dic = vocabulary.get_vocabulary_dic()
use_rate_dic = vocabulary.calc_total_use_rate(dic)

basedir = './ch'

# 出力先ディレクトリがなければ作る
if not os.path.isdir(basedir):
    os.makedirs(basedir)


g_word_dict = {}
for file, v in dic.items():
    basename = os.path.basename(file)
    video_id, _ = os.path.splitext(basename)
    with codecs.open('{}/{}'.format(basedir, basename), 'w', 'utf-8') as f:
        dic = {}

        total_count = 0
        for count in v.values():
            total_count += count

        for keyword, count in v.items():
            if keyword not in use_rate_dic:
                continue

            rate = count / total_count
            dic[keyword] = rate

        w = sorted(dic.items(), key=lambda x: x[1], reverse=True)

        words = []
        for keyword, rate in w:
            local_per_global = rate / use_rate_dic[keyword]
            if local_per_global > 2:
                words.append(keyword)
        
        g_word_dict[video_id] = words
        f.write(json.dumps(words, ensure_ascii=False))
        

with codecs.open('./ch/all.json', 'w', 'utf-8') as f:
    f.write(json.dumps(g_word_dict, ensure_ascii=False))