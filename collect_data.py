import os
import sys
import codecs
import json

import vocabulary
from vocabulary import get_mecab
from create_wordcloud import create_wordcloud
from get_characterize_chat import get_characterize_chat
from get_aggregate_words import get_aggregate_words

font = sys.argv[1]

# 使用されている用語を探し出す
print('get vocabulary from files.')
vocabulary_dic = vocabulary.get_vocabulary_dic()
# 使用されている単語が配信でどれくらいの割合で使用されているのかを計算する
print('calc vocabulary use rate.')
vocabulary_use_rate = vocabulary.calc_total_use_rate(vocabulary_dic)

# 出力先ディレクトリがなければ作る
output_base_dir = './video_src'
if not os.path.isdir(output_base_dir):
    os.makedirs(output_base_dir)

mecab = get_mecab()

for file, vocabulary in vocabulary_dic.items():
    id = os.path.splitext(os.path.basename(file))[0]
    output_dir = '{}/{}'.format(output_base_dir, id)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    # vocabulary_use_rateは新しい配信が追加されるたびに代わるので毎回作り直すというのが正しいかもしれないが、
    # そこまで更新する意味はないと思うので新規のものだけを出力する
    # なお、これによって同じワードクラウドが後から復元できない可能性が高い(どのvocabulary_use_rateから作られたかが保存されないため)が
    # そのときはそのときで新しく作り直せばいいと思う

    # ワードクラウド
    wordcloud_path = '{}/wc.png'.format(output_dir)
    if not os.path.exists(wordcloud_path):
        create_wordcloud(font, vocabulary, vocabulary_use_rate, wordcloud_path)

    # 検索用のチャット抜き出し
    characterize_path = '{}/characterize.json'.format(output_dir)
    if not os.path.exists(characterize_path):
        characterize_chat = get_characterize_chat(mecab, id, vocabulary, vocabulary_use_rate)
        with codecs.open(characterize_path, 'w', 'utf-8') as f:
            f.write(json.dumps(characterize_chat, ensure_ascii=False))

    # ビデオ詳細用の単語抜き出し
    aggregate_path = '{}/aggregate.json'.format(output_dir)
    if not os.path.exists(aggregate_path):
        aggregate = get_aggregate_words(mecab, id)
        with codecs.open(aggregate_path, 'w', 'utf-8') as f:
            f.write(json.dumps(aggregate, ensure_ascii=False))
    
    print('{} done.'.format(id))
