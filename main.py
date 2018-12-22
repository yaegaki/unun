import os
import sys
import codecs
import random
import numpy as np

import MeCab
from wordcloud import WordCloud
from PIL import Image

from normalize_neologd import normalize_neologd

# ストップワード
# このURLのものを使用: https://qiita.com/kenmatsu4/items/9b6ac74f831443d29074
stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して',
            u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',
            u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で',
            u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']

# どの放送でもよく出てくるワード
additional_stop_words = [
    u'イオリン', u'かわいい', u'すごい', u'かしこい', u'えらい', u'好き', u'すき', u'だいじょうぶ', u'大丈夫', u'いい',
    u'w', u'ww', u'www', u'wwww', u'wwwww', u'wwwwww',
]

stop_words2 = stop_words + additional_stop_words


mask_image_pathes = [
    './iori_mask.png',
    './mokotaiori_mask.png',
]

masks = [np.array(Image.open(f)) for f in mask_image_pathes]

files = [os.path.join('livechat', f) for f in os.listdir('livechat')
    if os.path.isfile(os.path.join('livechat', f))]
m = MeCab.Tagger('-u ./dotlive.dic')

def check_accept(word, cols):
    if (word == 'EOS' or len(cols) < 2):
        return False

    # 品詞
    part = cols[1].split(',')[0]

    # 動詞は微妙なやつが紛れてしまうことが多いのでとりあえずこの二つだけ
    return part == '名詞' or part == '形容詞'


def get_keywords_text(path):
    with codecs.open(path, encoding='utf-8') as f:
        keywords = []
        # 1行ずつパースしていく
        for line in f.readlines():
            # 正規化してからMeCabに渡す
            rows = m.parse(normalize_neologd(line))
            # 形態素が行ごとにあるのでそれで分割していく
            for row in rows.split('\n'):
                cols = row.split('\t')
                if (len(cols) == 0):
                    continue

                word = cols[0]
                if check_accept(word, cols):
                    keywords.append(word)
                
        # ランダムにしておかないとなぜか同じ単語が近い位置に出てきてしまうことがあるのでその対策
        random.shuffle(keywords)

        # WordCloud用に空白区切りの文字列にする
        return ' '.join(keywords)

settings = [
    [stop_words, masks[0], 'all'],
    [stop_words2, masks[1], 'part'],
]

def make_wordcloud(path, font, background_color, contour_color):
    print('start wordcloud for {}.'.format(path))
    keywords_text = get_keywords_text(path)
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

for file in files:
    make_wordcloud(file, sys.argv[1], 'white', 'hsl(193, 96%, 82%)')
