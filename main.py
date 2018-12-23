import os
import sys
import codecs
import random
import numpy as np

import MeCab
from wordcloud import WordCloud
from PIL import Image

from normalize_neologd import normalize_neologd
import vocabulary

font = sys.argv[1]

# ストップワード
# このURLのものを使用: https://qiita.com/kenmatsu4/items/9b6ac74f831443d29074
stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して',
            u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',
            u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で',
            u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']


# 使用されている用語を探し出す
print('get vocabulary from files.')
vocabulary_dic = vocabulary.get_vocabulary_dic()
# 使用されている単語が配信でどれくらいの割合で使用されているのかを計算する
print('calc vocabulary use rate.')
vocabulary_use_rate = vocabulary.calc_total_use_rate(vocabulary_dic)

# 全体の6割以上で使用されているものはストップワードとする
additional_stop_words = [keyword for keyword, rate in vocabulary_use_rate.items() if rate > 0.6]
# デバッグ用
# print(additional_stop_words)

stop_words2 = stop_words + additional_stop_words


mask_image_pathes = [
    './iori_mask.png',
    './mokotaiori_mask.png',
]

masks = [np.array(Image.open(f)) for f in mask_image_pathes]

def get_keywords_text(keywords):
    # ランダムにしておかないとなぜか同じ単語が近い位置に出てきてしまうことがあるのでその対策
    random.shuffle(keywords)

    # WordCloud用に空白区切りの文字列にする
    return ' '.join(keywords)

settings = [
    [stop_words, masks[0], 'all'],
    [stop_words2, masks[1], 'part'],
]



def make_wordcloud(path, vocabulary, font, background_color, contour_color):
    print('start wordcloud for {}.'.format(path))
    
    keywords = []
    for keyword, count in vocabulary.items():
        keywords.extend([keyword] * count)

    keywords_text = get_keywords_text(keywords)
    file_name_without_ext = os.path.splitext(os.path.basename(path))[0]
    

    for setting in settings:
        sw = setting[0]
        mask = setting[1]
        desc = setting[2]

        # マスク画像使うとそのサイズになるのでwidthとheightは指定しない
        wordcloud = WordCloud(
            background_color=background_color,
            contour_width=3,
            contour_color=contour_color,
            font_path=font,
            stopwords=set(sw),
            mask=mask,
        ).generate(keywords_text)

        wordcloud.to_file('./wc/{}-{}.png'.format(file_name_without_ext, desc))

# 出力先ディレクトリがなければ作る
if not os.path.isdir('./wc'):
    os.makedirs('./wc')

for file, vocabulary in vocabulary_dic.items():
    make_wordcloud(file, vocabulary, font, 'white', 'hsl(193, 96%, 82%)')
